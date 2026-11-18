"""Pruebas de los componentes mecánicos."""

import numpy as np

from protein_motor_sim.mechanics.brownian import brownian_displacement
from protein_motor_sim.mechanics.elasticity import HookeanSpring


def test_hookean_spring_restoring_force():
    """Un resorte estirado ejerce una fuerza restauradora negativa."""
    spring = HookeanSpring(stiffness_N_m=2.0, rest_length_m=1.0)
    assert spring.force_N(1.5) == -1.0


def test_brownian_displacement_is_reproducible():
    """El generador con semilla fija debe reproducir el incremento."""
    first = brownian_displacement(1.0e-12, 0.1, np.random.default_rng(42))
    second = brownian_displacement(1.0e-12, 0.1, np.random.default_rng(42))
    assert first == second
