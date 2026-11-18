"""Ejemplo básico: simular una kinesina-1 individual."""

from protein_motor_sim import Environment, GillespieSimulator, Kinesin1
from protein_motor_sim.analysis.observables import analyze_trajectory
from protein_motor_sim.visualization.plots import plot_trajectory


def main() -> None:
    """Ejecuta y grafica una simulación de ejemplo."""
    motor = Kinesin1()
    environment = Environment(
        atp_concentration=1.0e-3,
        external_force_N=0.0,
        temperature_K=310.0,
    )
    trajectory = GillespieSimulator().run(
        motor=motor,
        environment=environment,
        t_max=2.0,
        seed=42,
    )

    print(analyze_trajectory(trajectory))
    plot_trajectory(trajectory)

    import matplotlib.pyplot as plt

    plt.show()


if __name__ == "__main__":
    main()
