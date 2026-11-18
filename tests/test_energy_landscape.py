"""Tests for the phenomenological energy landscape and visualizations."""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest

from protein_motor_sim.core.environment import Environment
from protein_motor_sim.mechanics.energy_landscape import EnergyLandscape
from protein_motor_sim.models.kinesin.kinesin1 import Kinesin1
from protein_motor_sim.simulation.gillespie import GillespieSimulator
from protein_motor_sim.visualization.animation import AnimationStyle, animate_kinesin_walk
from protein_motor_sim.visualization.energy_landscape import (
    conformational_energy_surface_kbt,
    periodic_potential_kbt,
    plot_conformational_energy_surface,
    plot_periodic_energy_landscape,
    plot_state_energy_diagram,
    thermal_energy_pN_nm,
)
from protein_motor_sim.visualization.energy_maps import (
    animate_trajectory_on_energy_landscape,
    plot_energy_landscape_2d,
    plot_energy_landscape_3d,
    plot_energy_profiles,
    plot_trajectory_on_energy_landscape,
)


def test_energy_landscape_returns_scalar_and_array():
    """Energy evaluation should support scalar and broadcast array inputs."""
    landscape = EnergyLandscape()
    assert isinstance(landscape.energy_kBT(0.0, 0.0), float)
    values = landscape.energy_kBT(np.linspace(0, 20, 10), 0.5)
    assert values.shape == (10,)
    assert np.all(np.isfinite(values))


def test_energy_landscape_grid_shape():
    """The grid method should return aligned 2D arrays."""
    x_grid, q_grid, energy = EnergyLandscape().grid((-10, 20), nx=31, nq=17)
    assert x_grid.shape == q_grid.shape == energy.shape == (17, 31)


def test_energy_load_tilts_surface_uphill():
    """A positive opposing load should increase energy with positive x."""
    landscape = EnergyLandscape(spatial_barrier_kBT=0.0, conformational_barrier_kBT=0.0)
    no_load = landscape.energy_kBT(10.0, 0.0, opposing_force_pN=0.0)
    loaded = landscape.energy_kBT(10.0, 0.0, opposing_force_pN=2.0)
    assert loaded > no_load


def test_energy_rejects_invalid_q():
    """Conformational coordinate must remain within [0, 1]."""
    with pytest.raises(ValueError):
        EnergyLandscape().energy_kBT(0.0, 1.2)


def test_energy_plot_functions_return_axes():
    """2D, 3D and profile plot functions should create their axes."""
    landscape = EnergyLandscape()
    ax2d, _ = plot_energy_landscape_2d(landscape, (-10, 20), resolution=(30, 20))
    assert ax2d.get_xlabel().startswith("Longitudinal")
    ax3d, _ = plot_energy_landscape_3d(landscape, (-10, 20), resolution=(30, 20))
    assert ax3d.name == "3d"
    ax_profiles = plot_energy_profiles(
        landscape, (-10, 20), {"pre": 0.0, "post": 1.0}, n_points=40
    )
    assert len(ax_profiles.lines) == 2
    plt.close("all")


def test_trajectory_overlay_and_animations():
    """Trajectory overlays and both animation builders should initialize."""
    trajectory = GillespieSimulator().run(
        Kinesin1(), Environment(), t_max=0.15, seed=23
    )
    coordinates = {
        "bound_apo": 0.0,
        "atp_bound": 0.35,
        "post_hydrolysis": 1.0,
        "detached": 0.5,
    }
    ax, _ = plot_trajectory_on_energy_landscape(
        trajectory, EnergyLandscape(), coordinates
    )
    assert len(ax.collections) >= 2

    animation = animate_kinesin_walk(
        trajectory, style=AnimationStyle(frames_per_step=4, interval_ms=20)
    )
    animation._func(0)
    assert len(animation._protein_motor_sim_frames) >= 1

    energy_animation = animate_trajectory_on_energy_landscape(
        trajectory, EnergyLandscape(), coordinates
    )
    energy_animation._func(0)
    plt.close("all")


def test_alternative_energy_landscape_helpers():
    """Periodic and conformational energy helpers should return finite values."""
    assert thermal_energy_pN_nm(310.0) > 0
    periodic = periodic_potential_kbt(np.linspace(0.0, 16.4, 20))
    assert periodic.shape == (20,)
    x_grid, q_grid, energy = conformational_energy_surface_kbt(
        np.linspace(0.0, 16.4, 20), np.linspace(-1.0, 1.0, 11)
    )
    assert x_grid.shape == q_grid.shape == energy.shape == (11, 20)
    assert np.all(np.isfinite(energy))


def test_alternative_energy_plots():
    """Energy profile, conformational map and state diagram should plot."""
    ax1 = plot_periodic_energy_landscape(points=30)
    ax2, _ = plot_conformational_energy_surface(x_points=30, q_points=20)
    ax3 = plot_state_energy_diagram(
        {"s0": 0.0, "s1": -0.2, "s2": 0.1},
        {("s0", "s1"): 2.0, ("s1", "s2"): 2.1},
    )
    assert len(ax1.lines) == 2
    assert ax2.collections
    assert len(ax3.lines) >= 2
    plt.close("all")
