"""Pruebas del modelo de kinesina-1."""

from protein_motor_sim.core.environment import Environment
from protein_motor_sim.models.kinesin.kinesin1 import Kinesin1
from protein_motor_sim.analysis.observables import analyze_trajectory
from protein_motor_sim.simulation.gillespie import GillespieSimulator


def test_kinesin_network_contains_expected_states():
    """La red inicial debe contener estados activos y desprendido."""
    network = Kinesin1().build_network()
    assert network.initial_state == "bound_apo"
    assert "detached" in network.states


def test_analysis_reports_nonnegative_atp():
    """El análisis debe devolver un consumo acumulado no negativo."""
    trajectory = GillespieSimulator().run(
        Kinesin1(), Environment(), t_max=1.0, seed=20
    )
    result = analyze_trajectory(trajectory)
    assert result.atp_consumed >= 0
    assert result.path_length_nm >= 0
