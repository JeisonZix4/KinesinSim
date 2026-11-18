"""Funciones auxiliares para fuerzas mecánicas."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Force:
    """Representa una fuerza escalar sobre el eje de la pista.

    Attributes:
        value_N: Magnitud con signo en newtons.
        label: Descripción de la fuerza.
    """

    value_N: float
    label: str = "external"

    def __post_init__(self) -> None:
        """Valida que el valor de la fuerza sea finito."""
        if self.value_N != self.value_N or abs(self.value_N) == float("inf"):
            raise ValueError("La fuerza debe ser finita.")


def net_force(*forces: Force) -> Force:
    """Suma fuerzas escalares colineales.

    Args:
        *forces: Fuerzas que actúan sobre el eje de movimiento.

    Returns:
        Fuerza resultante en newtons.
    """
    return Force(sum(force.value_N for force in forces), label="net")
