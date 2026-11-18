"""Pruebas de las leyes cinéticas elementales."""

from protein_motor_sim.core.environment import Environment
from protein_motor_sim.kinetics.rate_laws import ATPBindingRate, ConstantRate
from protein_motor_sim.kinetics.force_dependence import BellRate


def test_atp_binding_rate_scales_with_concentration():
    """La tasa de unión de ATP debe ser k_on por concentración."""
    law = ATPBindingRate(2.0e6)
    environment = Environment(atp_concentration=1.0e-3)
    assert law(environment) == 2.0e3


def test_bell_rate_decreases_for_opposing_load():
    """Una fuerza opuesta reduce una tasa con dirección forward."""
    law = BellRate(ConstantRate(10.0), distance_m=1.0e-9)
    unloaded = law(Environment(external_force_N=0.0))
    loaded = law(Environment(external_force_N=2.0e-12))
    assert loaded < unloaded
