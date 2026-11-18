"""Serialización JSON de trayectorias."""

import json
from pathlib import Path

from protein_motor_sim.core.trajectory import Trajectory


def save_trajectory(trajectory: Trajectory, filepath: str | Path) -> None:
    """Guarda una trayectoria como archivo JSON.

    Args:
        trajectory: Trayectoria que se desea almacenar.
        filepath: Ruta de destino.
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(trajectory.to_dict(), file, indent=2, ensure_ascii=False)


def load_trajectory(filepath: str | Path) -> Trajectory:
    """Carga una trayectoria previamente guardada en JSON.

    Args:
        filepath: Ruta del archivo JSON.

    Returns:
        Trayectoria reconstruida.
    """
    with Path(filepath).open("r", encoding="utf-8") as file:
        data = json.load(file)

    trajectory = Trajectory()
    times = data["times_s"]
    positions = data["positions_nm"]
    states = data["states"]
    events = data["events"]
    if not (len(times) == len(positions) == len(states) == len(events)):
        raise ValueError("El archivo contiene listas de distinta longitud.")

    # El consumo acumulado se conserva como metadato global.
    for index, values in enumerate(zip(times, positions, states, events)):
        time_s, position_nm, state, event = values
        trajectory.record(time_s, position_nm, state, event)
    trajectory.atp_consumed_total = int(data.get("atp_consumed_total", 0))
    return trajectory
