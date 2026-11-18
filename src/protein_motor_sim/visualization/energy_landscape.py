"""Alternative energy-profile and state-diagram plotting utilities.

These functions complement the object-oriented ``EnergyLandscape`` model in
``protein_motor_sim.mechanics.energy_landscape``. They use a separate
conformational coordinate q in [-1, 1], where -1 is labelled undocked and +1
docked. All potentials are phenomenological, not experimentally calibrated.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from math import isfinite
from typing import Any

import numpy as np

BOLTZMANN_CONSTANT_J_K = 1.380649e-23


def thermal_energy_pN_nm(temperature_K: float = 310.0) -> float:
    """Calculate k_B T in pN nm.

    Args:
        temperature_K: Absolute temperature in kelvin.

    Returns:
        Thermal energy in pN nm.

    Raises:
        ValueError: If temperature is not finite and positive.
    """
    if not isfinite(float(temperature_K)) or temperature_K <= 0:
        raise ValueError("temperature_K must be finite and positive.")
    return BOLTZMANN_CONSTANT_J_K * temperature_K * 1.0e21


def periodic_potential_kbt(
    x_nm: np.ndarray | Sequence[float] | float,
    lattice_spacing_nm: float = 8.2,
    barrier_kbt: float = 4.0,
    opposing_force_pN: float = 0.0,
    temperature_K: float = 310.0,
    reference_position_nm: float = 0.0,
) -> np.ndarray | float:
    """Evaluate a sinusoidal periodic potential tilted by an opposing load.

    Args:
        x_nm: Axial coordinate or array in nanometers.
        lattice_spacing_nm: Spatial period in nanometers.
        barrier_kbt: Barrier height without load, in k_B T.
        opposing_force_pN: Positive force opposes motion toward +x, in pN.
        temperature_K: Absolute temperature in kelvin.
        reference_position_nm: Position of a zero-load potential minimum.

    Returns:
        Potential U/(k_B T), preserving the input shape.
    """
    if lattice_spacing_nm <= 0 or barrier_kbt < 0:
        raise ValueError("The lattice period must be positive and barrier nonnegative.")
    if not isfinite(float(opposing_force_pN)):
        raise ValueError("opposing_force_pN must be finite.")
    kbt = thermal_energy_pN_nm(temperature_K)
    x_values = np.asarray(x_nm, dtype=float)
    if not np.all(np.isfinite(x_values)):
        raise ValueError("x_nm must contain only finite values.")
    periodic = 0.5 * barrier_kbt * (
        1.0 - np.cos(
            2.0 * np.pi * (x_values - reference_position_nm) / lattice_spacing_nm
        )
    )
    result = periodic + opposing_force_pN * x_values / kbt
    return float(result) if result.ndim == 0 else result


def conformational_energy_surface_kbt(
    x_nm: Sequence[float] | np.ndarray,
    q: Sequence[float] | np.ndarray,
    lattice_spacing_nm: float = 8.2,
    barrier_kbt: float = 5.0,
    conformational_barrier_kbt: float = 2.0,
    docking_bias_kbt: float = 1.0,
    docking_barrier_coupling: float = 0.35,
    opposing_force_pN: float = 0.0,
    temperature_K: float = 310.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Build a phenomenological surface U(x, q) in units of k_B T.

    The dimensionless coordinate q ranges from -1 (undocked) to +1 (docked).
    The model combines a periodic axial potential, a conformational double
    well, a docking bias, a q-dependent axial barrier, and an external-load
    tilt. These terms are illustrative and are not inferred from kinesin rates.

    Args:
        x_nm: One-dimensional axial coordinates in nanometers.
        q: One-dimensional conformational coordinates in [-1, 1].
        lattice_spacing_nm: Period of the axial potential in nanometers.
        barrier_kbt: Base axial barrier in k_B T.
        conformational_barrier_kbt: Double-well barrier in k_B T.
        docking_bias_kbt: Bias favouring q=+1 when positive, in k_B T.
        docking_barrier_coupling: Fraction of axial barrier reduction at q=+1.
        opposing_force_pN: Load opposing +x, in piconewtons.
        temperature_K: Absolute temperature in kelvin.

    Returns:
        Tuple of mesh grids ``(X, Q, U)`` compatible with contour plotting.
    """
    if lattice_spacing_nm <= 0 or barrier_kbt < 0 or conformational_barrier_kbt < 0:
        raise ValueError("Period must be positive and energy barriers nonnegative.")
    if not 0.0 <= docking_barrier_coupling <= 1.0:
        raise ValueError("docking_barrier_coupling must be between 0 and 1.")
    if not isfinite(float(opposing_force_pN)):
        raise ValueError("opposing_force_pN must be finite.")

    x_values = np.asarray(x_nm, dtype=float)
    q_values = np.asarray(q, dtype=float)
    if x_values.ndim != 1 or q_values.ndim != 1:
        raise ValueError("x_nm and q must be one-dimensional arrays.")
    if not np.all(np.isfinite(x_values)) or not np.all(np.isfinite(q_values)):
        raise ValueError("Coordinates must be finite.")
    if np.any((q_values < -1.0) | (q_values > 1.0)):
        raise ValueError("q must lie between -1 and 1.")

    X, Q = np.meshgrid(x_values, q_values)
    kbt = thermal_energy_pN_nm(temperature_K)
    docked_fraction = (Q + 1.0) / 2.0
    effective_barrier = barrier_kbt * (
        1.0 - docking_barrier_coupling * docked_fraction
    )
    axial = 0.5 * effective_barrier * (
        1.0 - np.cos(2.0 * np.pi * X / lattice_spacing_nm)
    )
    conformational = conformational_barrier_kbt * (Q**2 - 1.0) ** 2
    conformational -= 0.5 * docking_bias_kbt * Q
    load = opposing_force_pN * X / kbt
    return X, Q, axial + conformational + load


def plot_periodic_energy_landscape(
    x_range_nm: tuple[float, float] = (-8.2, 32.8),
    lattice_spacing_nm: float = 8.2,
    barrier_kbt: float = 4.0,
    forces_pN: Sequence[float] = (0.0, 2.0),
    temperature_K: float = 310.0,
    points: int = 900,
    ax: Any = None,
):
    """Plot one-dimensional periodic energy profiles for several loads.

    Args:
        x_range_nm: Lower and upper axial bounds in nanometers.
        lattice_spacing_nm: Period in nanometers.
        barrier_kbt: Unloaded barrier in k_B T.
        forces_pN: Opposing loads in piconewtons.
        temperature_K: Absolute temperature in kelvin.
        points: Number of axial samples.
        ax: Optional Matplotlib axes.

    Returns:
        Matplotlib axes containing the profiles.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as error:
        raise ImportError("Matplotlib is required to plot energy.") from error
    if points < 10 or x_range_nm[1] <= x_range_nm[0]:
        raise ValueError("Use at least 10 points and an increasing x range.")
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)
    x = np.linspace(*x_range_nm, points)
    for force in forces_pN:
        energy = periodic_potential_kbt(
            x, lattice_spacing_nm, barrier_kbt, float(force), temperature_K
        )
        ax.plot(x, energy, label=f"Opposing load = {force:g} pN")
    ax.set_xlabel("Axial coordinate x (nm)")
    ax.set_ylabel(r"Potential energy $U/(k_B T)$")
    ax.set_title("Periodic energy landscape under load")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
    return ax


def plot_conformational_energy_surface(
    x_range_nm: tuple[float, float] = (-8.2, 24.6),
    lattice_spacing_nm: float = 8.2,
    barrier_kbt: float = 5.0,
    conformational_barrier_kbt: float = 2.0,
    docking_bias_kbt: float = 1.0,
    docking_barrier_coupling: float = 0.35,
    opposing_force_pN: float = 0.0,
    temperature_K: float = 310.0,
    x_points: int = 260,
    q_points: int = 140,
    levels: int = 30,
    ax: Any = None,
):
    """Plot the two-dimensional axial/conformational energy surface.

    Args:
        x_range_nm: Axial range in nanometers.
        lattice_spacing_nm: Axial period in nanometers.
        barrier_kbt: Base axial barrier in k_B T.
        conformational_barrier_kbt: Double-well barrier in k_B T.
        docking_bias_kbt: Bias for the docked conformation in k_B T.
        docking_barrier_coupling: Coupling fraction between 0 and 1.
        opposing_force_pN: Load opposing +x, in pN.
        temperature_K: Absolute temperature in kelvin.
        x_points: Axial grid resolution.
        q_points: Conformational grid resolution.
        levels: Number of contour levels.
        ax: Optional Matplotlib axes.

    Returns:
        Tuple ``(ax, contour)``.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as error:
        raise ImportError("Matplotlib is required to plot energy.") from error
    if x_range_nm[1] <= x_range_nm[0] or x_points < 10 or q_points < 10:
        raise ValueError("The range must increase and each grid dimension >= 10.")
    if levels < 2:
        raise ValueError("levels must be at least 2.")
    x = np.linspace(*x_range_nm, x_points)
    q = np.linspace(-1.0, 1.0, q_points)
    X, Q, U = conformational_energy_surface_kbt(
        x, q,
        lattice_spacing_nm=lattice_spacing_nm,
        barrier_kbt=barrier_kbt,
        conformational_barrier_kbt=conformational_barrier_kbt,
        docking_bias_kbt=docking_bias_kbt,
        docking_barrier_coupling=docking_barrier_coupling,
        opposing_force_pN=opposing_force_pN,
        temperature_K=temperature_K,
    )
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 5.5), constrained_layout=True)
    contour = ax.contourf(X, Q, U, levels=levels, cmap="viridis")
    ax.contour(X, Q, U, levels=levels, colors="white", linewidths=0.35, alpha=0.45)
    ax.set_xlabel("Axial coordinate x (nm)")
    ax.set_ylabel("Conformational coordinate q")
    ax.set_title("Phenomenological energy surface U(x, q)")
    ax.text(
        0.01, 0.98, "q = -1: undocked\nq = +1: docked",
        transform=ax.transAxes, va="top", ha="left", fontsize=9,
        bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.8},
    )
    return ax, contour


def plot_state_energy_diagram(
    state_energies_kbt: Mapping[str, float],
    barriers_kbt: Mapping[tuple[str, str], float] | None = None,
    ax: Any = None,
):
    """Plot relative state energies and schematic barriers along a pathway.

    Args:
        state_energies_kbt: Ordered mapping of state names to relative energies.
        barriers_kbt: Optional absolute barrier heights for consecutive pairs.
        ax: Optional Matplotlib axes.

    Returns:
        Matplotlib axes with the energy-state diagram.

    Note:
        The kinetic rates alone do not determine this diagram. A consistent
        inference requires thermodynamic constraints and local detailed balance.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as error:
        raise ImportError("Matplotlib is required to plot energy.") from error
    names = list(state_energies_kbt)
    energies = np.asarray(list(state_energies_kbt.values()), dtype=float)
    if len(names) < 2 or not np.all(np.isfinite(energies)):
        raise ValueError("Provide at least two states with finite energies.")
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 5), constrained_layout=True)
    barriers = barriers_kbt or {}

    for index in range(len(names) - 1):
        left, right = names[index], names[index + 1]
        e_left, e_right = energies[index], energies[index + 1]
        barrier = float(barriers.get((left, right), max(e_left, e_right) + 1.5))
        if not isfinite(barrier) or barrier < max(e_left, e_right):
            raise ValueError(f"Barrier {left}->{right} must exceed both state energies.")
        t = np.linspace(0.0, 1.0, 80)
        profile = (
            (1.0 - t) * e_left + t * e_right
            + 4.0 * (barrier - 0.5 * (e_left + e_right)) * t * (1.0 - t)
        )
        ax.plot(index + t, profile, linewidth=2.0)

    x_positions = np.arange(len(names), dtype=float)
    ax.scatter(x_positions, energies, s=65, zorder=3)
    for x_pos, name, energy in zip(x_positions, names, energies):
        ax.annotate(
            f"{name}\n{energy:.2f} kBT", (x_pos, energy),
            xytext=(0, 10), textcoords="offset points", ha="center", fontsize=9,
        )
    ax.set_xticks(x_positions, names, rotation=15, ha="right")
    ax.set_ylabel("Relative free energy (kBT)")
    ax.set_xlabel("Schematic reaction coordinate")
    ax.set_title("State-energy and transition-barrier diagram")
    ax.grid(axis="y", alpha=0.25)
    return ax
