"""Algoritmo estocástico directo de Gillespie (SSA)."""

from math import log
from typing import Optional

import numpy as np

from protein_motor_sim.core.environment import Environment
from protein_motor_sim.core.motor import Motor
from protein_motor_sim.core.trajectory import Trajectory
from protein_motor_sim.simulation.base import SimulationStrategy


class GillespieSimulator(SimulationStrategy):
    """Simula una red de reacciones mediante el algoritmo de Gillespie.

    El algoritmo supone tasas constantes entre eventos para el estado y el
    ambiente actuales. Las tasas se vuelven a evaluar después de cada evento.
    """

    def run(
        self,
        motor: Motor,
        environment: Environment,
        t_max: float,
        seed: Optional[int] = None,
        max_events: int = 1_000_000,
    ) -> Trajectory:
        """Ejecuta una trayectoria estocástica hasta t_max o desprendimiento.

        Args:
            motor: Motor cuya red cinética se va a simular.
            environment: Concentración de ATP, fuerza y temperatura.
            t_max: Tiempo máximo de observación en segundos.
            seed: Semilla para reproducibilidad.
            max_events: Límite de seguridad para el número de eventos.

        Returns:
            Trayectoria con tiempos, posiciones, estados y eventos.

        Raises:
            ValueError: Si t_max o max_events no son positivos.
            RuntimeError: Si se alcanza el máximo de eventos.
        """
        if t_max <= 0:
            raise ValueError("t_max debe ser mayor que cero.")
        if max_events <= 0:
            raise ValueError("max_events debe ser mayor que cero.")

        rng = np.random.default_rng(seed)
        network = motor.build_network()
        current_state = network.initial_state
        current_time = 0.0
        position_nm = 0.0
        trajectory = Trajectory()
        trajectory.record(
            current_time, position_nm, current_state, event="initial"
        )

        for _ in range(max_events):
            if network.states[current_state].is_terminal:
                break

            available = network.rates(current_state, environment)
            positive = [(transition, rate) for transition, rate in available if rate > 0]
            total_rate = sum(rate for _, rate in positive)

            if total_rate <= 0:
                trajectory.record(
                    t_max, position_nm, current_state, event="observation_end"
                )
                break

            # Dos sorteos independientes: espera temporal y selección del evento.
            random_wait = max(float(rng.random()), np.finfo(float).tiny)
            delta_time = -log(random_wait) / total_rate

            if current_time + delta_time > t_max:
                trajectory.record(
                    t_max, position_nm, current_state, event="observation_end"
                )
                break

            current_time += delta_time
            threshold = float(rng.random()) * total_rate
            cumulative_rate = 0.0
            selected = positive[-1][0]

            for transition, rate in positive:
                cumulative_rate += rate
                if threshold <= cumulative_rate:
                    selected = transition
                    break

            current_state = selected.target
            position_nm += selected.displacement_nm
            trajectory.record(
                current_time,
                position_nm,
                current_state,
                event=selected.event_name,
                atp_delta=selected.atp_consumed,
            )

            if network.states[current_state].is_terminal:
                break
        else:
            raise RuntimeError(
                "Se alcanzó max_events. Revisa las tasas o aumenta el límite."
            )

        return trajectory
