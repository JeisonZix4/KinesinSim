"""Leyes cinéticas elementales utilizadas por las redes de reacción."""

from dataclasses import dataclass
from typing import Protocol

from protein_motor_sim.core.environment import Environment


class RateLaw(Protocol):
    """Protocolo de una ley que calcula tasas en función del ambiente."""

    def __call__(self, environment: Environment) -> float:
        """Devuelve una tasa en s^-1."""


@dataclass(frozen=True, slots=True)
class ConstantRate:
    """Ley de tasa constante.

    Attributes:
        rate_s: Tasa constante en s^-1.
    """

    rate_s: float

    def __post_init__(self) -> None:
        """Comprueba que la tasa sea admisible."""
        if self.rate_s < 0 or self.rate_s != self.rate_s:
            raise ValueError("La tasa constante debe ser no negativa y finita.")

    def __call__(self, environment: Environment) -> float:
        """Evalúa la tasa constante.

        Args:
            environment: Ambiente de simulación; no afecta esta ley.

        Returns:
            Tasa en s^-1.
        """
        del environment
        return self.rate_s


@dataclass(frozen=True, slots=True)
class ATPBindingRate:
    """Ley de asociación de ATP de segundo orden.

    La tasa pseudo-primer orden se calcula como k_on por [ATP].

    Attributes:
        association_rate_M_s: Constante de asociación en M^-1 s^-1.
    """

    association_rate_M_s: float

    def __post_init__(self) -> None:
        """Valida la constante de asociación."""
        if self.association_rate_M_s < 0 or self.association_rate_M_s != self.association_rate_M_s:
            raise ValueError("La constante de asociación debe ser no negativa y finita.")

    def __call__(self, environment: Environment) -> float:
        """Calcula la tasa efectiva de unión de ATP.

        Args:
            environment: Condiciones que contienen la concentración de ATP.

        Returns:
            Tasa pseudo-primer orden en s^-1.
        """
        return self.association_rate_M_s * environment.atp_concentration
