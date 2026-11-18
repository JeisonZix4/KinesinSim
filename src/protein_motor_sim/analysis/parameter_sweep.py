"""Barridos de parámetros experimentales."""

from dataclasses import replace
from typing import Iterable

from protein_motor_sim.core.environment import Environment
from protein_motor_sim.core.motor import Motor
from protein_motor_sim.simulation.base import SimulationStrategy
from protein_motor_sim.simulation.ensemble import run_ensemble
from protein_motor_sim.analysis.statistics import summarize_trajectories


def sweep_atp_concentration(
    simulator: SimulationStrategy,
    motor: Motor,
    environment: Environment,
    concentrations_M: Iterable[float],
    t_max: float,
    n_runs: int = 20,
    seed: int | None = None,
) -> list[dict[str, float]]:
    """Evalúa la velocidad media para varias concentraciones de ATP.

    Args:
        simulator: Algoritmo de simulación.
        motor: Modelo del motor proteico.
        environment: Ambiente base; se reemplaza solo la concentración de ATP.
        concentrations_M: Concentraciones de ATP en mol/L.
        t_max: Tiempo máximo por trayectoria en segundos.
        n_runs: Número de réplicas por concentración.
        seed: Semilla maestra opcional.

    Returns:
        Lista de diccionarios con concentración, velocidad y dispersión.
    """
    results: list[dict[str, float]] = []
    for index, concentration in enumerate(concentrations_M):
        condition = replace(environment, atp_concentration=float(concentration))
        ensemble = run_ensemble(
            simulator,
            motor,
            condition,
            t_max,
            n_runs,
            seed=None if seed is None else seed + index,
        )
        summary = summarize_trajectories(ensemble.trajectories)
        results.append(
            {
                "atp_concentration_M": float(concentration),
                "mean_velocity_nm_s": summary.mean_velocity_nm_s,
                "std_velocity_nm_s": summary.std_velocity_nm_s,
            }
        )
    return results
