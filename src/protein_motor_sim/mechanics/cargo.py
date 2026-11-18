"""Representación inicial de una carga transportada por motores."""

from dataclasses import dataclass


@dataclass
class Cargo:
    """Carga puntual simplificada acoplada al motor.

    Attributes:
        position_m: Posición de la carga en metros.
        drag_coefficient_N_s_m: Coeficiente de arrastre lineal en N s/m.
        mass_kg: Masa efectiva en kg, reservada para modelos inerciales.
    """

    position_m: float = 0.0
    drag_coefficient_N_s_m: float = 1.0e-6
    mass_kg: float = 0.0

    def __post_init__(self) -> None:
        """Valida los parámetros de la carga."""
        if self.drag_coefficient_N_s_m < 0 or self.mass_kg < 0:
            raise ValueError("El arrastre y la masa efectiva no pueden ser negativos.")

    def drag_force_N(self, velocity_m_s: float) -> float:
        """Calcula la fuerza de arrastre lineal.

        Args:
            velocity_m_s: Velocidad de la carga en m/s.

        Returns:
            Fuerza de arrastre en newtons, opuesta a la velocidad.
        """
        return -self.drag_coefficient_N_s_m * velocity_m_s
