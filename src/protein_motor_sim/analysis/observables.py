"""Magnitudes observables derivadas de una trayectoria."""

from dataclasses import dataclass

from protein_motor_sim.core.trajectory import Trajectory


@dataclass(frozen=True, slots=True)
class TrajectoryAnalysis:
    """Resumen de observables calculados para una trayectoria."""

    velocity_nm_s: float
    run_length_nm: float
    path_length_nm: float
    duration_s: float
    atp_consumed: int
    forward_steps: int
    backward_steps: int
    detached: bool


def analyze_trajectory(trajectory: Trajectory) -> TrajectoryAnalysis:
    """Calcula observables cinemáticos y bioquímicos.

    El run length se define aquí como el módulo del desplazamiento neto.
    path_length_nm contabiliza la distancia total recorrida, incluidos
    retrocesos. Esta convención se debe tener presente al comparar datos.

    Args:
        trajectory: Trayectoria devuelta por un simulador.

    Returns:
        Resumen de magnitudes de la trayectoria.
    """
    return TrajectoryAnalysis(
        velocity_nm_s=trajectory.mean_velocity_nm_s,
        run_length_nm=abs(trajectory.displacement_nm),
        path_length_nm=trajectory.path_length_nm,
        duration_s=trajectory.duration_s,
        atp_consumed=trajectory.atp_consumed_total,
        forward_steps=trajectory.events.count("forward_step"),
        backward_steps=trajectory.events.count("backward_step"),
        detached="detachment" in trajectory.events,
    )
