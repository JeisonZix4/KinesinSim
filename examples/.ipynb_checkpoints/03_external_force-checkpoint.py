"""Ejemplo: comparar trayectorias bajo distintas fuerzas opuestas."""

from protein_motor_sim import Environment, GillespieSimulator, Kinesin1
from protein_motor_sim.analysis.observables import analyze_trajectory


def main() -> None:
    """Imprime velocidad y recorrido para varias cargas."""
    simulator = GillespieSimulator()
    motor = Kinesin1()

    for force_pN in (0.0, 1.0, 2.0, 4.0):
        environment = Environment(
            atp_concentration=1.0e-3,
            external_force_N=force_pN * 1.0e-12,
            temperature_K=310.0,
        )
        trajectory = simulator.run(
            motor, environment, t_max=2.0, seed=100
        )
        print(
            f"F={force_pN:.1f} pN | "
            f"{analyze_trajectory(trajectory)}"
        )


if __name__ == "__main__":
    main()
