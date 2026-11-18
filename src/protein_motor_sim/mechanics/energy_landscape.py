"""Phenomenological free-energy landscapes for molecular-motor visualization.

The class in this module provides a configurable mathematical surface for
exploration and visualization. Its parameters are not automatically inferred
from the kinetic network and must not be interpreted as experimentally
calibrated kinesin free energies.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

import numpy as np

BOLTZMANN_CONSTANT_J_K = 1.380649e-23


@dataclass(frozen=True, slots=True)
class EnergyLandscape:
    """Represent an illustrative 2D energy landscape.

    The surface depends on a longitudinal coordinate ``x`` and a dimensionless
    conformational coordinate ``q`` in [0, 1]. Energies are returned in units
    of thermal energy, k_B T.

    The implemented potential is:

        U(x, q) / (k_B T) = U_spatial + U_conformational + U_bias + U_load

    where the spatial periodicity shifts with q, the conformational coordinate
    has a double-well potential, and an opposing load tilts the surface.

    This is a phenomenological teaching/visualization model. It is not a
    molecular-mechanics force field or an experimentally calibrated potential
    of mean force for kinesin.

    Attributes:
        period_nm: Spatial period of the potential in nanometers.
        spatial_barrier_kBT: Amplitude of the periodic spatial barrier in k_B T.
        conformational_barrier_kBT: Barrier between q=0 and q=1 in k_B T.
        conformational_bias_kBT: Energy offset of q=1 relative to q=0 in k_B T.
        phase_shift: Fraction of one spatial period shifted between q=0 and q=1.
        coupling_kBT: Optional coupling amplitude between spatial and
            conformational coordinates in k_B T.
        opposing_force_pN: Positive values tilt the energy upwards with x,
            representing a load opposing motion in the positive x direction.
        temperature_K: Absolute temperature in kelvin.
    """

    period_nm: float = 8.2
    spatial_barrier_kBT: float = 2.5
    conformational_barrier_kBT: float = 3.0
    conformational_bias_kBT: float = 0.0
    phase_shift: float = 0.5
    coupling_kBT: float = 0.0
    opposing_force_pN: float = 0.0
    temperature_K: float = 310.0

    def __post_init__(self) -> None:
        """Validate the landscape parameters.

        Raises:
            ValueError: If a parameter is non-finite or outside its domain.
        """
        numeric_values = {
            "period_nm": self.period_nm,
            "spatial_barrier_kBT": self.spatial_barrier_kBT,
            "conformational_barrier_kBT": self.conformational_barrier_kBT,
            "conformational_bias_kBT": self.conformational_bias_kBT,
            "phase_shift": self.phase_shift,
            "coupling_kBT": self.coupling_kBT,
            "opposing_force_pN": self.opposing_force_pN,
            "temperature_K": self.temperature_K,
        }
        for name, value in numeric_values.items():
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be a real number.")
            if not isfinite(float(value)):
                raise ValueError(f"{name} must be finite.")

        if self.period_nm <= 0:
            raise ValueError("period_nm must be positive.")
        if self.spatial_barrier_kBT < 0:
            raise ValueError("spatial_barrier_kBT cannot be negative.")
        if self.conformational_barrier_kBT < 0:
            raise ValueError("conformational_barrier_kBT cannot be negative.")
        if not 0.0 <= self.phase_shift <= 1.0:
            raise ValueError("phase_shift must be between 0 and 1.")
        if self.temperature_K <= 0:
            raise ValueError("temperature_K must be positive.")

    @property
    def thermal_energy_J(self) -> float:
        """Return k_B T in joules."""
        return BOLTZMANN_CONSTANT_J_K * self.temperature_K

    @property
    def thermal_energy_pN_nm(self) -> float:
        """Return k_B T in pN nm, a convenient nanoscale energy unit."""
        return self.thermal_energy_J * 1.0e21

    def energy_kBT(
        self,
        x_nm: float | np.ndarray,
        q: float | np.ndarray,
        opposing_force_pN: float | None = None,
    ) -> float | np.ndarray:
        """Evaluate the dimensionless potential energy U/(k_B T).

        Args:
            x_nm: Longitudinal position or array of positions in nanometers.
            q: Dimensionless conformational coordinate or array in [0, 1].
            opposing_force_pN: Optional load override in piconewtons. If None,
                the value stored in the landscape is used.

        Returns:
            Potential energy in units of k_B T. A scalar is returned when both
            inputs are scalars; otherwise a NumPy array is returned.

        Raises:
            ValueError: If coordinates or the load are outside their domains.
        """
        x_values = np.asarray(x_nm, dtype=float)
        q_values = np.asarray(q, dtype=float)
        if not np.all(np.isfinite(x_values)):
            raise ValueError("x_nm must contain only finite values.")
        if not np.all(np.isfinite(q_values)):
            raise ValueError("q must contain only finite values.")
        if np.any((q_values < 0.0) | (q_values > 1.0)):
            raise ValueError("q must lie between 0 and 1.")

        force = self.opposing_force_pN if opposing_force_pN is None else float(
            opposing_force_pN
        )
        if not isfinite(force):
            raise ValueError("opposing_force_pN must be finite.")

        x_grid, q_grid = np.broadcast_arrays(x_values, q_values)
        phase = 2.0 * np.pi * (
            x_grid / self.period_nm - self.phase_shift * q_grid
        )
        spatial = 0.5 * self.spatial_barrier_kBT * (1.0 - np.cos(phase))
        conformational = (
            16.0
            * self.conformational_barrier_kBT
            * q_grid**2
            * (1.0 - q_grid) ** 2
        )
        bias = self.conformational_bias_kBT * q_grid
        coupling = (
            self.coupling_kBT
            * np.sin(2.0 * np.pi * x_grid / self.period_nm)
            * q_grid
            * (1.0 - q_grid)
        )
        load = force * x_grid / self.thermal_energy_pN_nm
        result = spatial + conformational + bias + coupling + load
        if result.ndim == 0:
            return float(result)
        return result

    def grid(
        self,
        x_range_nm: tuple[float, float],
        q_range: tuple[float, float] = (0.0, 1.0),
        nx: int = 240,
        nq: int = 120,
        opposing_force_pN: float | None = None,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Generate coordinate grids and evaluate the energy surface.

        Args:
            x_range_nm: Minimum and maximum longitudinal coordinates in nm.
            q_range: Minimum and maximum conformational coordinates.
            nx: Number of points along x.
            nq: Number of points along q.
            opposing_force_pN: Optional opposing load in pN.

        Returns:
            Tuple ``(X, Q, U)`` of 2D arrays. ``U`` is measured in k_B T.

        Raises:
            ValueError: If ranges or grid sizes are invalid.
        """
        if len(x_range_nm) != 2 or x_range_nm[0] >= x_range_nm[1]:
            raise ValueError("x_range_nm must contain increasing bounds.")
        if len(q_range) != 2 or q_range[0] < 0 or q_range[1] > 1:
            raise ValueError("q_range must lie inside [0, 1].")
        if q_range[0] >= q_range[1]:
            raise ValueError("q_range must contain increasing bounds.")
        if nx < 2 or nq < 2:
            raise ValueError("nx and nq must both be at least 2.")

        x_values = np.linspace(x_range_nm[0], x_range_nm[1], nx)
        q_values = np.linspace(q_range[0], q_range[1], nq)
        x_grid, q_grid = np.meshgrid(x_values, q_values)
        energy = self.energy_kBT(x_grid, q_grid, opposing_force_pN)
        return x_grid, q_grid, np.asarray(energy)

    def energy_profile_kBT(
        self,
        x_nm: np.ndarray,
        q: float,
        opposing_force_pN: float | None = None,
    ) -> np.ndarray:
        """Evaluate a one-dimensional energy profile at fixed q.

        Args:
            x_nm: Positions in nanometers.
            q: Fixed conformational coordinate in [0, 1].
            opposing_force_pN: Optional opposing load in pN.

        Returns:
            Energy profile in k_B T.
        """
        return np.asarray(self.energy_kBT(x_nm, q, opposing_force_pN))
