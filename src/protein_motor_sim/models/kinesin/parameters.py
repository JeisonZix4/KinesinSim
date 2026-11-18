"""Parámetros configurables del modelo simplificado de kinesina-1."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KinesinParameters:
    """Parámetros cinéticos iniciales para el prototipo de kinesina-1.

    Estos valores son configuraciones ilustrativas para probar el software.
    No constituyen un conjunto experimental validado ni deben interpretarse
    como parámetros universales de kinesina-1.

    Attributes:
        atp_association_rate_M_s: Asociación de ATP en M^-1 s^-1.
        hydrolysis_rate_s: Tasa efectiva de hidrólisis en s^-1.
        forward_step_rate_s: Tasa de avance sin carga en s^-1.
        backward_step_rate_s: Tasa de retroceso sin carga en s^-1.
        detachment_rate_s: Tasa basal de desprendimiento en s^-1.
        step_size_nm: Tamaño del paso en nm.
        force_distance_m: Distancia efectiva para la dependencia de fuerza.
    """

    atp_association_rate_M_s: float = 1.0e6
    hydrolysis_rate_s: float = 80.0
    forward_step_rate_s: float = 100.0
    backward_step_rate_s: float = 0.05
    detachment_rate_s: float = 0.2
    step_size_nm: float = 8.2
    force_distance_m: float = 1.0e-9

    def __post_init__(self) -> None:
        """Valida los parámetros que deben ser positivos o no negativos."""
        nonnegative = (
            self.atp_association_rate_M_s,
            self.hydrolysis_rate_s,
            self.forward_step_rate_s,
            self.backward_step_rate_s,
            self.detachment_rate_s,
        )
        if any(value < 0 or value != value for value in nonnegative):
            raise ValueError("Las tasas deben ser no negativas y finitas.")
        if self.step_size_nm <= 0 or self.force_distance_m < 0:
            raise ValueError("El tamaño de paso debe ser positivo y la distancia no negativa.")
