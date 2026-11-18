"""Pruebas de las abstracciones fundamentales de ProteinMotorSim."""

import pytest

from protein_motor_sim.core import Environment, State, Track, Trajectory, Transition


def test_environment_rejects_negative_atp_concentration():
    """La concentración de ATP no puede ser negativa."""
    with pytest.raises(ValueError):
        Environment(atp_concentration=-1.0e-3)


def test_state_requires_nonempty_name():
    """Un estado debe poder identificarse dentro de la red cinética."""
    with pytest.raises(ValueError):
        State(name="   ")


def test_transition_rejects_negative_rate():
    """Una tasa de transición no puede tomar valores negativos."""
    transition = Transition(
        source="A",
        target="B",
        rate_law=lambda _environment: -1.0,
        event_name="invalid_event",
    )
    with pytest.raises(ValueError):
        transition.rate(Environment())


def test_track_maps_sites_to_positions_and_back():
    """La geometría de la pista debe respetar espaciamiento y polaridad."""
    track = Track(lattice_spacing_nm=8.2, polarity=-1, origin_nm=2.0)
    position = track.site_position_nm(3)

    assert position == pytest.approx(-22.6)
    assert track.nearest_site_index(position) == 3


def test_trajectory_records_displacement_and_atp_consumption():
    """La trayectoria calcula desplazamiento y consumo acumulado."""
    trajectory = Trajectory()
    trajectory.record(0.0, 0.0, "bound", "initial")
    trajectory.record(0.1, 8.2, "bound", "forward_step", atp_delta=1)

    assert trajectory.displacement_nm == pytest.approx(8.2)
    assert trajectory.mean_velocity_nm_s == pytest.approx(82.0)
    assert trajectory.atp_consumed_total == 1
    assert trajectory.number_of_events == 1
