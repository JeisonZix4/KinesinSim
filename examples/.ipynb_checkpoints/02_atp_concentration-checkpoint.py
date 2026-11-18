"""Ejemplo: explorar la respuesta del motor a la concentración de ATP."""

from protein_motor_sim import Environment, GillespieSimulator, Kinesin1
from protein_motor_sim.analysis.parameter_sweep import sweep_atp_concentration
from protein_motor_sim.visualization.plots import plot_atp_sweep


def main() -> None:
    """Ejecuta el barrido y representa los resultados."""
    simulator = GillespieSimulator()
    motor = Kinesin1()
    environment = Environment(temperature_K=310.0)
    concentrations = [1.0e-5, 5.0e-5, 1.0e-4, 5.0e-4, 1.0e-3, 2.0e-3]

    results = sweep_atp_concentration(
        simulator, motor, environment, concentrations,
        t_max=2.0, n_runs=30, seed=10
    )
    for row in results:
        print(row)
    plot_atp_sweep(results)

    import matplotlib.pyplot as plt

    plt.show()


if __name__ == "__main__":
    main()
