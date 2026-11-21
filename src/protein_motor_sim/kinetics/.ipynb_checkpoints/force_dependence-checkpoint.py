"""Modelos de dependencia de las tasas con la fuerza externa."""

from dataclasses import dataclass
from math import exp

from protein_motor_sim.core.environment import Environment
from protein_motor_sim.kinetics.rate_laws import RateLaw

BOLTZMANN_CONSTANT_J_K = 1.380649e-23


@dataclass(frozen=True, slots=True)
class BellRate:
    """Envuelve una tasa con una dependencia de fuerza tipo Bell.

    Se utiliza k(F) = k(0) exp[-s F delta / (k_B T)], donde F es positiva
    cuando se opone al avance. Con force_direction=+1 la carga reduce la tasa;
    con force_direction=-1 la aumenta. Es una aproximación fenomenológica.

    Attributes:
        base_rate: Ley de tasa sin carga.
        distance_m: Distancia característica de la transición en metros.
        force_direction: Signo de la sensibilidad a la fuerza (+1 o -1).
        load_fraction: Fracción efectiva de la carga que actúa en la transición.
    """

    base_rate: RateLaw
    distance_m: float
    force_direction: int = 1
    load_fraction: float = 1.0

    def __post_init__(self) -> None:
        """Valida los parámetros del modelo de Bell."""
        if self.distance_m < 0:
            raise ValueError("La distancia característica no puede ser negativa.")
        if self.force_direction not in (-1, 1):
            raise ValueError("force_direction debe ser +1 o -1.")
        if not 0 <= self.load_fraction <= 1:
            raise ValueError("load_fraction debe estar entre 0 y 1.")

    def __call__(self, environment: Environment) -> float:
        """Calcula la tasa modificada por la fuerza externa.

        Args:
            environment: Ambiente con fuerza y temperatura.

        Returns:
            Tasa efectiva en s^-1.
        """
        base = float(self.base_rate(environment))
        exponent = (
            -self.force_direction
            * self.load_fraction
            * environment.external_force_N
            * self.distance_m
            / (BOLTZMANN_CONSTANT_J_K * environment.temperature_K)
        )
        # El recorte evita desbordamientos numéricos en cargas extremas.
        exponent = max(-700.0, min(700.0, exponent))
        return base * exp(exponent)
