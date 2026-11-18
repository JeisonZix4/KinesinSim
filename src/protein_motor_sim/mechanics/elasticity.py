"""Modelos elásticos sencillos para enlaces y elementos flexibles."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HookeanSpring:
    """Resorte lineal que obedece la ley de Hooke.

    Attributes:
        stiffness_N_m: Constante elástica en N/m.
        rest_length_m: Longitud natural del resorte en m.
    """

    stiffness_N_m: float
    rest_length_m: float = 0.0

    def __post_init__(self) -> None:
        """Valida la constante elástica y la longitud natural."""
        if self.stiffness_N_m < 0 or self.rest_length_m < 0:
            raise ValueError("La rigidez y la longitud natural no pueden ser negativas.")

    def force_N(self, length_m: float) -> float:
        """Calcula la fuerza restauradora para una longitud dada.

        Args:
            length_m: Longitud actual del resorte en metros.

        Returns:
            Fuerza restauradora en newtons; positiva si se estira.
        """
        return -self.stiffness_N_m * (length_m - self.rest_length_m)
