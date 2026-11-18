"""Condiciones físicas y bioquímicas del entorno de simulación."""

from dataclasses import dataclass
from math import isfinite
from numbers import Real


@dataclass(frozen=True, slots=True)
class Environment:
    """Contiene las condiciones experimentales que afectan al motor proteico.

    Las unidades se mantienen explícitas para evitar ambigüedades:

    - Concentración de ATP: mol/L (M).
    - Fuerza externa: newtons (N).
    - Temperatura: kelvin (K).

    La convención de signo para ``external_force_N`` es que un valor positivo
    representa una carga que se opone al avance hacia el extremo positivo de
    la pista. Un valor negativo representa una fuerza asistiva.

    Attributes:
        atp_concentration: Concentración de ATP en mol/L.
        external_force_N: Fuerza externa firmada en newtons.
        temperature_K: Temperatura absoluta en kelvin.
    """

    atp_concentration: float = 1.0e-3
    external_force_N: float = 0.0
    temperature_K: float = 310.0

    def __post_init__(self) -> None:
        """Valida que las condiciones sean finitas y físicamente admisibles.

        Raises:
            ValueError: Si algún valor no es finito o viola sus restricciones.
        """
        values = {
            "atp_concentration": self.atp_concentration,
            "external_force_N": self.external_force_N,
            "temperature_K": self.temperature_K,
        }
        for name, value in values.items():
            if isinstance(value, bool) or not isinstance(value, Real):
                raise ValueError(f"{name} debe ser un número real.")
            if not isfinite(float(value)):
                raise ValueError(f"{name} debe ser un número finito.")

        if self.atp_concentration < 0:
            raise ValueError("La concentración de ATP no puede ser negativa.")
        if self.temperature_K <= 0:
            raise ValueError("La temperatura debe ser mayor que cero kelvin.")
