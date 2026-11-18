"""Animaciones 2D sencillas de una trayectoria sobre un microtúbulo."""

from protein_motor_sim.core.trajectory import Trajectory


def animate_trajectory(trajectory: Trajectory, interval_ms: int = 50):
    """Crea una animación 2D de la posición registrada del motor.

    La animación es esquemática: no representa la estructura atómica ni las
    conformaciones de las dos cabezas de kinesina.

    Args:
        trajectory: Trayectoria simulada.
        interval_ms: Intervalo entre fotogramas en milisegundos.

    Returns:
        Objeto FuncAnimation de Matplotlib.
    """
    try:
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation
    except ImportError as exc:
        raise ImportError("Instala Matplotlib para crear animaciones.") from exc

    if not trajectory.times_s:
        raise ValueError("La trayectoria está vacía.")
    if interval_ms <= 0:
        raise ValueError("interval_ms debe ser positivo.")

    fig, ax = plt.subplots()
    minimum = min(trajectory.positions_nm)
    maximum = max(trajectory.positions_nm)
    padding = max(10.0, (maximum - minimum) * 0.15)
    ax.set_xlim(minimum - padding, maximum + padding)
    ax.set_ylim(-1.0, 1.0)
    ax.set_yticks([])
    ax.set_xlabel("Posición sobre el microtúbulo (nm)")
    ax.set_title("Movimiento esquemático del motor")
    ax.axhline(0.0, linewidth=5, alpha=0.25)
    motor_dot, = ax.plot([], [], marker="o", markersize=14)

    def initialize():
        """Inicializa el marcador."""
        motor_dot.set_data([], [])
        return (motor_dot,)

    def update(frame: int):
        """Actualiza la posición del marcador."""
        motor_dot.set_data([trajectory.positions_nm[frame]], [0.0])
        return (motor_dot,)

    animation = FuncAnimation(
        fig,
        update,
        frames=len(trajectory.times_s),
        init_func=initialize,
        interval=interval_ms,
        blit=True,
    )
    return animation
