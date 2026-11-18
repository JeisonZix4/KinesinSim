"""Gráficas de trayectorias y resultados."""

from protein_motor_sim.core.trajectory import Trajectory


def plot_trajectory(trajectory: Trajectory, ax=None):
    """Grafica posición frente al tiempo.

    Args:
        trajectory: Trayectoria que se desea visualizar.
        ax: Ejes Matplotlib existentes; si es None, se crean.

    Returns:
        Ejes Matplotlib utilizados.

    Raises:
        ImportError: Si Matplotlib no está instalado.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError(
            "Instala Matplotlib con `pip install protein-motor-sim[viz]`."
        ) from exc

    if ax is None:
        _, ax = plt.subplots()
    ax.step(trajectory.times_s, trajectory.positions_nm, where="post")
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Posición (nm)")
    ax.set_title("Trayectoria del motor proteico")
    ax.grid(True, alpha=0.3)
    return ax


def plot_atp_sweep(results: list[dict[str, float]], ax=None):
    """Grafica velocidad media frente a concentración de ATP.

    Args:
        results: Salida de ``sweep_atp_concentration``.
        ax: Ejes Matplotlib existentes o None.

    Returns:
        Ejes Matplotlib utilizados.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError("Matplotlib es necesario para esta gráfica.") from exc

    if ax is None:
        _, ax = plt.subplots()
    x = [row["atp_concentration_M"] for row in results]
    y = [row["mean_velocity_nm_s"] for row in results]
    yerr = [row["std_velocity_nm_s"] for row in results]
    ax.errorbar(x, y, yerr=yerr, marker="o", linestyle="-")
    ax.set_xlabel("Concentración de ATP (mol/L)")
    ax.set_ylabel("Velocidad media (nm/s)")
    ax.set_title("Velocidad frente a concentración de ATP")
    ax.grid(True, alpha=0.3)
    return ax
