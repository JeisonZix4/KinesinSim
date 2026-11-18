"""Interfaz común para los modelos de motores proteicos."""

from abc import ABC, abstractmethod
from math import isfinite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from protein_motor_sim.kinetics.reaction_network import ReactionNetwork


class Motor(ABC):
    """Clase base de un modelo de motor proteico.

    Esta clase representa la definición del motor y su mecanismo, no el estado
    temporal de una molécula particular. El estado dinámico de una corrida se
    almacena en un objeto ``Trajectory``.

    Cada motor concreto debe proporcionar un nombre, un tamaño de paso nominal
    y un método que construya su red de reacciones.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre legible del modelo de motor."""

    @property
    @abstractmethod
    def step_size_nm(self) -> float:
        """Desplazamiento característico de un paso, en nanómetros."""

    @abstractmethod
    def build_network(self) -> "ReactionNetwork":
        """Construye la red cinética del modelo.

        Returns:
            Red de estados y transiciones que describe el mecanismo.
        """

    def validate(self) -> None:
        """Comprueba los atributos básicos y la red del modelo.

        Este método es útil al desarrollar nuevos motores. La validación
        topológica detallada se delega a ``ReactionNetwork``.

        Raises:
            ValueError: Si el nombre o el tamaño de paso son inválidos.
        """
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("El motor debe tener un nombre no vacío.")
        try:
            step_size = float(self.step_size_nm)
        except (TypeError, ValueError) as error:
            raise ValueError("step_size_nm debe ser un número.") from error
        if not isfinite(step_size) or step_size <= 0:
            raise ValueError("step_size_nm debe ser finito y positivo.")
        self.build_network()
