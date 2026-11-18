"""Fluctuaciones brownianas para coordenadas mecánicas sobreamortiguadas."""

import numpy as np


def brownian_displacement(
    diffusion_coefficient_m2_s: float,
    delta_time_s: float,
    rng: np.random.Generator | None = None,
) -> float:
    """Genera un incremento browniano unidimensional.

    El incremento se distribuye como una normal de media cero y varianza
    2 D dt. Las unidades del resultado son metros.

    Args:
        diffusion_coefficient_m2_s: Coeficiente de difusión en m^2/s.
        delta_time_s: Intervalo temporal en segundos.
        rng: Generador aleatorio opcional.

    Returns:
        Desplazamiento browniano en metros.
    """
    if diffusion_coefficient_m2_s < 0 or delta_time_s < 0:
        raise ValueError("D y dt deben ser no negativos.")
    generator = rng or np.random.default_rng()
    return float(
        generator.normal(
            loc=0.0,
            scale=np.sqrt(2.0 * diffusion_coefficient_m2_s * delta_time_s),
        )
    )
