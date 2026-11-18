"""Pruebas del algoritmo SSA."""

from protein_motor_sim import Environment, GillespieSimulator, Kinesin1


def test_gillespie_is_reproducible():
    """La misma semilla y condiciones deben producir igual trayectoria."""
    simulator = GillespieSimulator()
    motor = Kinesin1()
    environment = Environment()
    first = simulator.run(motor, environment, t_max=0.5, seed=123)
    second = simulator.run(motor, environment, t_max=0.5, seed=123)

    assert first.times_s == second.times_s
    assert first.positions_nm == second.positions_nm
    assert first.events == second.events


def test_trajectory_stays_within_observation_window():
    """La trayectoria no puede superar el tiempo de observación."""
    trajectory = GillespieSimulator().run(
        Kinesin1(), Environment(), t_max=0.1, seed=7
    )
    assert trajectory.times_s[0] == 0.0
    assert trajectory.times_s[-1] <= 0.1
