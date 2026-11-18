"""Ejecución de conjuntos de trayectorias independientes."""

from dataclasses import dataclass
from typing import Optional

from protein_motor_sim.core.environment import Environment
from protein_motor_sim.core.motor import Motor
from protein_motor_sim.core.trajectory import Trajectory
from protein_motor_sim.simulation.base import SimulationStrategy


@dataclass
class EnsembleResult:
    """Contenedor de las trayectorias de un conjunto de simulaciones."""

    trajectories: list[Trajectory]

    @property
    def size(self) -> int:
        """Devuelve el número de trayectorias."""
        return len(self.trajectories)


def run_ensemble(
    simulator: SimulationStrategy,
    motor: Motor,
    environment: Environment,
    t_max: float,
    n_runs: int,
    seed: Optional[int] = None,
) -> EnsembleResult:
    """Ejecuta varias simulaciones con semillas reproducibles distintas.

    Args:
        simulator: Estrategia de simulación que se va a utilizar.
        motor: Modelo del motor proteico.
        environment: Condiciones experimentales.
        t_max: Tiempo máximo de cada simulación en segundos.
        n_runs: Número de trayectorias independientes.
        seed: Semilla maestra opcional.

    Returns:
        Conjunto de trayectorias.

    Raises:
        ValueError: Si n_runs no es positivo.
    """
    import numpy as np

    if n_runs <= 0:
        raise ValueError("n_runs debe ser mayor que cero.")
    seed_sequence = np.random.SeedSequence(seed)
    child_seeds = seed_sequence.spawn(n_runs)
    trajectories = [
        simulator.run(
            motor,
            environment,
            t_max,
            seed=int(child.generate_state(1)[0]),
        )
        for child in child_seeds
    ]
    return EnsembleResult(trajectories)
