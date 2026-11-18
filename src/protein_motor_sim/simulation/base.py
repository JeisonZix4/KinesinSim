"""Interfaces comunes para las estrategias de simulación."""

from abc import ABC, abstractmethod
from typing import Optional

from protein_motor_sim.core.environment import Environment
from protein_motor_sim.core.motor import Motor
from protein_motor_sim.core.trajectory import Trajectory


class SimulationStrategy(ABC):
    """Interfaz de los algoritmos de simulación."""

    @abstractmethod
    def run(
        self,
        motor: Motor,
        environment: Environment,
        t_max: float,
        seed: Optional[int] = None,
    ) -> Trajectory:
        """Ejecuta una simulación y devuelve su trayectoria.

        Args:
            motor: Modelo del motor proteico.
            environment: Condiciones experimentales.
            t_max: Tiempo máximo de simulación en segundos.
            seed: Semilla opcional para reproducibilidad.

        Returns:
            Trayectoria resultante de la simulación.
        """
