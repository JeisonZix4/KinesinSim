"""2D, 3D and trajectory-overlaid energy-landscape visualizations."""

from __future__ import annotations

from collections.abc import Mapping

import numpy as np

from protein_motor_sim.core.trajectory import Trajectory
from protein_motor_sim.mechanics.energy_landscape import EnergyLandscape


def plot_energy_landscape_2d(
    landscape: EnergyLandscape,
    x_range_nm: tuple[float, float],
    q_range: tuple[float, float] = (0.0, 1.0),
    resolution: tuple[int, int] = (260, 150),
    opposing_force_pN: float | None = None,
    levels: int = 28,
    ax=None,
):
    """Plot a 2D contour map of the energy landscape.

    Args:
        landscape: Configurable phenomenological energy landscape.
        x_range_nm: Position range in nanometers.
        q_range: Conformational-coordinate range in [0, 1].
        resolution: Number of grid points (nx, nq).
        opposing_force_pN: Optional load override in pN.
        levels: Number of contour levels.
        ax: Optional Matplotlib axes.

    Returns:
        Tuple ``(ax, contour_set)``.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as error:
        raise ImportError("Install Matplotlib to plot energy maps.") from error

    x_grid, q_grid, energy = landscape.grid(
        x_range_nm,
        q_range,
        nx=resolution[0],
        nq=resolution[1],
        opposing_force_pN=opposing_force_pN,
    )
    if ax is None:
        _, ax = plt.subplots(figsize=(11, 5.8), constrained_layout=True)

    contour = ax.contourf(
        x_grid,
        q_grid,
        energy,
        levels=levels,
        cmap="viridis",
        extend="both",
    )
    lines = ax.contour(
        x_grid,
        q_grid,
        energy,
        levels=max(8, levels // 2),
        colors="white",
        linewidths=0.55,
        alpha=0.45,
    )
    ax.clabel(lines, inline=True, fontsize=7, fmt="%.1f")
    colorbar = ax.figure.colorbar(contour, ax=ax, pad=0.02)
    colorbar.set_label(r"Potential energy, $U/(k_B T)$")
    load = landscape.opposing_force_pN if opposing_force_pN is None else opposing_force_pN
    ax.set_xlabel("Longitudinal coordinate, x (nm)")
    ax.set_ylabel("Conformational coordinate, q (dimensionless)")
    ax.set_title(f"Phenomenological energy landscape | opposing load = {load:g} pN")
    return ax, contour


def plot_energy_landscape_3d(
    landscape: EnergyLandscape,
    x_range_nm: tuple[float, float],
    q_range: tuple[float, float] = (0.0, 1.0),
    resolution: tuple[int, int] = (180, 90),
    opposing_force_pN: float | None = None,
    ax=None,
):
    """Plot the energy surface as a 3D Matplotlib surface.

    Args:
        landscape: Energy landscape to visualize.
        x_range_nm: Position range in nanometers.
        q_range: Conformational-coordinate range.
        resolution: Number of grid points (nx, nq).
        opposing_force_pN: Optional load override in pN.
        ax: Optional 3D Matplotlib axes.

    Returns:
        Tuple ``(ax, surface)``.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as error:
        raise ImportError("Install Matplotlib to plot energy surfaces.") from error

    x_grid, q_grid, energy = landscape.grid(
        x_range_nm,
        q_range,
        nx=resolution[0],
        nq=resolution[1],
        opposing_force_pN=opposing_force_pN,
    )
    if ax is None:
        figure = plt.figure(figsize=(11, 7), constrained_layout=True)
        ax = figure.add_subplot(111, projection="3d")

    surface = ax.plot_surface(
        x_grid,
        q_grid,
        energy,
        cmap="viridis",
        linewidth=0,
        antialiased=True,
        alpha=0.96,
    )
    ax.set_xlabel("Position x (nm)", labelpad=10)
    ax.set_ylabel("Conformation q", labelpad=10)
    ax.set_zlabel(r"$U/(k_B T)$", labelpad=8)
    ax.set_title("3D phenomenological energy surface", pad=16)
    ax.figure.colorbar(surface, ax=ax, shrink=0.65, pad=0.10, label=r"$U/(k_B T)$")
    return ax, surface


def plot_energy_profiles(
    landscape: EnergyLandscape,
    x_range_nm: tuple[float, float],
    conformations: Mapping[str, float],
    n_points: int = 500,
    opposing_force_pN: float | None = None,
    ax=None,
):
    """Compare one-dimensional energy profiles at selected q values.

    Args:
        landscape: Energy landscape.
        x_range_nm: Position range in nanometers.
        conformations: Mapping from profile labels to q coordinates.
        n_points: Number of x coordinates.
        opposing_force_pN: Optional load override in pN.
        ax: Optional Matplotlib axes.

    Returns:
        Matplotlib axes containing the profiles.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as error:
        raise ImportError("Install Matplotlib to plot energy profiles.") from error

    if not conformations:
        raise ValueError("Provide at least one conformation to plot.")
    x_values = np.linspace(*x_range_nm, n_points)
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 5.2), constrained_layout=True)

    for label, q_value in conformations.items():
        profile = landscape.energy_profile_kBT(
            x_values, q_value, opposing_force_pN=opposing_force_pN
        )
        ax.plot(x_values, profile, linewidth=2.0, label=f"{label} (q={q_value:g})")

    ax.set_xlabel("Longitudinal coordinate, x (nm)")
    ax.set_ylabel(r"Potential energy, $U/(k_B T)$")
    ax.set_title("Energy profiles at selected conformations")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
    return ax


def plot_trajectory_on_energy_landscape(
    trajectory: Trajectory,
    landscape: EnergyLandscape,
    state_coordinates: Mapping[str, float],
    x_range_nm: tuple[float, float] | None = None,
    opposing_force_pN: float | None = None,
    ax=None,
):
    """Overlay a coarse-grained trajectory on the 2D energy map.

    The caller must explicitly provide a mapping from kinetic state names to
    conformational coordinates q. This avoids implying that the kinetic
    network already contains a physically calibrated structural coordinate.

    Args:
        trajectory: Simulated trajectory.
        landscape: Phenomenological energy landscape.
        state_coordinates: Mapping from each trajectory state to q in [0, 1].
        x_range_nm: Optional displayed position range. Inferred if omitted.
        opposing_force_pN: Optional load override in pN.
        ax: Optional Matplotlib axes.

    Returns:
        Tuple ``(ax, scatter)``.

    Raises:
        ValueError: If the trajectory is empty or a state has no q mapping.
    """
    if not trajectory.times_s:
        raise ValueError("The trajectory is empty.")
    missing = sorted(set(trajectory.states) - set(state_coordinates))
    if missing:
        raise ValueError(
            "Missing conformational coordinates for states: " + ", ".join(missing)
        )

    q_values = np.asarray([state_coordinates[state] for state in trajectory.states])
    if np.any((q_values < 0.0) | (q_values > 1.0)):
        raise ValueError("All state coordinates must lie in [0, 1].")
    x_values = np.asarray(trajectory.positions_nm, dtype=float)
    if x_range_nm is None:
        span = max(float(np.ptp(x_values)), landscape.period_nm)
        margin = max(0.5 * landscape.period_nm, 0.08 * span)
        x_range_nm = (float(np.min(x_values) - margin), float(np.max(x_values) + margin))

    ax, _ = plot_energy_landscape_2d(
        landscape,
        x_range_nm=x_range_nm,
        opposing_force_pN=opposing_force_pN,
        ax=ax,
    )
    scatter = ax.scatter(
        x_values,
        q_values,
        c=trajectory.times_s,
        cmap="plasma",
        edgecolors="white",
        linewidths=0.6,
        s=38,
        zorder=5,
    )
    ax.plot(x_values, q_values, color="white", linewidth=1.4, alpha=0.9, zorder=4)
    colorbar = ax.figure.colorbar(scatter, ax=ax, pad=0.12)
    colorbar.set_label("Simulation time (s)")
    ax.set_title("Trajectory overlaid on an illustrative energy landscape")
    return ax, scatter


def animate_trajectory_on_energy_landscape(
    trajectory: Trajectory,
    landscape: EnergyLandscape,
    state_coordinates: Mapping[str, float],
    x_range_nm: tuple[float, float] | None = None,
    interval_ms: int = 70,
    opposing_force_pN: float | None = None,
):
    """Animate the trajectory marker moving over a 2D energy landscape.

    Args:
        trajectory: Simulated trajectory.
        landscape: Phenomenological energy landscape.
        state_coordinates: Explicit mapping from state names to q values.
        x_range_nm: Optional x-axis range in nanometers.
        interval_ms: Frame interval in milliseconds.
        opposing_force_pN: Optional load override in pN.

    Returns:
        Matplotlib ``FuncAnimation`` object.
    """
    try:
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation
    except ImportError as error:
        raise ImportError("Install Matplotlib to animate an energy map.") from error

    if interval_ms <= 0:
        raise ValueError("interval_ms must be positive.")
    if not trajectory.times_s:
        raise ValueError("The trajectory is empty.")
    missing = sorted(set(trajectory.states) - set(state_coordinates))
    if missing:
        raise ValueError("Missing q coordinates for states: " + ", ".join(missing))

    x_values = np.asarray(trajectory.positions_nm, dtype=float)
    q_values = np.asarray([state_coordinates[state] for state in trajectory.states])
    if np.any((q_values < 0.0) | (q_values > 1.0)):
        raise ValueError("All state coordinates must lie in [0, 1].")
    if x_range_nm is None:
        margin = max(landscape.period_nm, 0.1 * max(float(np.ptp(x_values)), 1.0))
        x_range_nm = (float(np.min(x_values) - margin), float(np.max(x_values) + margin))

    figure, ax = plt.subplots(figsize=(8.8, 4.6), dpi=72, constrained_layout=True)
    plot_energy_landscape_2d(
        landscape,
        x_range_nm=x_range_nm,
        opposing_force_pN=opposing_force_pN,
        ax=ax,
    )
    path_line, = ax.plot([], [], color="white", linewidth=1.8, alpha=0.9, zorder=5)
    marker = ax.scatter([], [], s=130, c="#F94144", edgecolors="white", linewidths=1.5, zorder=6)
    label = ax.text(
        0.02, 0.97, "", transform=ax.transAxes, va="top", color="white",
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "#263238", "alpha": 0.85},
    )

    def update(index: int):
        """Move the marker and extend the visited path."""
        path_line.set_data(x_values[: index + 1], q_values[: index + 1])
        marker.set_offsets(np.array([[x_values[index], q_values[index]]]))
        label.set_text(
            f"t = {trajectory.times_s[index]:.4f} s\n"
            f"state = {trajectory.states[index]}\n"
            f"event = {trajectory.events[index]}"
        )
        return path_line, marker, label

    return FuncAnimation(
        figure,
        update,
        frames=len(trajectory.times_s),
        interval=interval_ms,
        blit=False,
        repeat=False,
    )


def plot_state_energy_diagram(
    state_energies_kbt: Mapping[str, float],
    barriers_kbt: Mapping[tuple[str, str], float] | None = None,
    ax=None,
):
    """Plot a free-energy profile along an explicitly ordered state pathway.

    State order follows the insertion order of ``state_energies_kbt``. Barrier
    values are absolute transition-state energies in kBT and must be supplied
    by the caller to represent a specific mechanochemical model. Missing
    barriers are drawn as visual placeholders and are not physical estimates.

    Args:
        state_energies_kbt: Ordered mapping of state names to relative free
            energies in kBT.
        barriers_kbt: Optional mapping from (source, target) pairs to absolute
            transition-state energies in kBT.
        ax: Optional Matplotlib axes.

    Returns:
        Matplotlib axes containing the energy profile.

    Raises:
        ValueError: If fewer than two states are provided or an energy is not
            finite, or a supplied transition-state energy lies below either
            adjacent state.

    Note:
        Kinetic rates from an irreversible cycle do not uniquely determine a
        thermodynamic energy profile. A thermodynamically consistent model must
        include reversible rates and chemical work from ATP/ADP/Pi.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as error:
        raise ImportError("Install Matplotlib to plot state energies.") from error

    names = list(state_energies_kbt)
    energies = np.asarray(list(state_energies_kbt.values()), dtype=float)
    if len(names) < 2:
        raise ValueError("Provide at least two states.")
    if not np.all(np.isfinite(energies)):
        raise ValueError("All state energies must be finite.")
    barriers = barriers_kbt or {}
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)

    for index, (left_name, right_name) in enumerate(zip(names[:-1], names[1:])):
        left_energy = float(energies[index])
        right_energy = float(energies[index + 1])
        default_barrier = max(left_energy, right_energy) + 1.5
        barrier = float(barriers.get((left_name, right_name), default_barrier))
        if not np.isfinite(barrier) or barrier < max(left_energy, right_energy):
            raise ValueError(
                f"Barrier for {left_name} -> {right_name} must be finite and "
                "not lower than either endpoint energy."
            )
        fraction = np.linspace(0.0, 1.0, 80)
        midpoint = 0.5 * (left_energy + right_energy)
        profile = (
            (1.0 - fraction) * left_energy
            + fraction * right_energy
            + 4.0 * (barrier - midpoint) * fraction * (1.0 - fraction)
        )
        ax.plot(index + fraction, profile, linewidth=2.0)

    x_positions = np.arange(len(names), dtype=float)
    ax.scatter(x_positions, energies, s=65, zorder=4)
    for x_pos, name, energy in zip(x_positions, names, energies):
        ax.annotate(
            f"{name}\n{energy:.2f} kBT",
            (x_pos, energy),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            fontsize=9,
        )
    ax.set_xticks(x_positions, names, rotation=15, ha="right")
    ax.set_ylabel(r"Relative free energy, $G/(k_B T)$")
    ax.set_xlabel("Reaction coordinate (schematic)")
    ax.set_title("Free-energy profile along a state pathway")
    ax.grid(axis="y", alpha=0.25)
    return ax
