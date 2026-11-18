"""Modelo configurable y simplificado de kinesina-1."""

from dataclasses import dataclass, field

from protein_motor_sim.core.motor import Motor
from protein_motor_sim.kinetics.reaction_network import ReactionNetwork
from protein_motor_sim.models.kinesin.kinetic_network import build_kinesin1_network
from protein_motor_sim.models.kinesin.parameters import KinesinParameters


@dataclass
class Kinesin1(Motor):
    """Modelo efectivo de una kinesina-1 individual.

    Attributes:
        parameters: Parámetros cinéticos del modelo.
    """

    parameters: KinesinParameters = field(default_factory=KinesinParameters)

    @property
    def name(self) -> str:
        """Devuelve el nombre del motor."""
        return "Kinesin-1"

    @property
    def step_size_nm(self) -> float:
        """Devuelve el tamaño nominal del paso en nanómetros."""
        return self.parameters.step_size_nm

    def build_network(self) -> ReactionNetwork:
        """Construye la red cinética a partir de los parámetros actuales."""
        return build_kinesin1_network(self.parameters)
