"""Ejemplo: animar la coordenada unidimensional del motor."""

from protein_motor_sim import Environment, GillespieSimulator, Kinesin1
from protein_motor_sim.visualization.animation import animate_trajectory


def main() -> None:
    """Ejecuta una simulación y muestra su animación esquemática."""
    trajectory = GillespieSimulator().run(
        Kinesin1(), Environment(), t_max=2.0, seed=42
    )
    animation = animate_trajectory(trajectory, interval_ms=80)

    import matplotlib.pyplot as plt

    plt.show()
    # Mantiene una referencia explícita a la animación hasta cerrar la ventana.
    del animation


if __name__ == "__main__":
    main()
