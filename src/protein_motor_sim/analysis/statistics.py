"""Estadísticas descriptivas de conjuntos de trayectorias."""

from dataclasses import dataclass
from statistics import mean, stdev
from collections.abc import Iterable

from protein_motor_sim.core.trajectory import Trajectory


@dataclass(frozen=True, slots=True)
class EnsembleStatistics:
    """Media y desviación estándar de observables de un conjunto."""

    mean_velocity_nm_s: float
    std_velocity_nm_s: float
    mean_run_length_nm: float
    std_run_length_nm: float
    number_of_trajectories: int


def summarize_trajectories(
    trajectories: Iterable[Trajectory],
) -> EnsembleStatistics:
    """Calcula estadísticas de velocidad y longitud de recorrido.

    Args:
        trajectories: Iterador de trayectorias simuladas.

    Returns:
        Estadísticas descriptivas. Para un único dato, la desviación estándar
        se define como cero.
    """
    items = list(trajectories)
    if not items:
        raise ValueError("Se necesita al menos una trayectoria.")

    velocities = [item.mean_velocity_nm_s for item in items]
    run_lengths = [abs(item.displacement_nm) for item in items]
    return EnsembleStatistics(
        mean_velocity_nm_s=mean(velocities),
        std_velocity_nm_s=stdev(velocities) if len(items) > 1 else 0.0,
        mean_run_length_nm=mean(run_lengths),
        std_run_length_nm=stdev(run_lengths) if len(items) > 1 else 0.0,
        number_of_trajectories=len(items),
    )
