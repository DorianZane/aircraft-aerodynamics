"""
Time-stepping simulation: state and forces over time.

State: altitude, airspeed, angle of attack (simplified 2D longitudinal).
You can change AircraftParams at any step to simulate parameter changes.
"""

import math
from dataclasses import dataclass

from .aircraft_params import AircraftParams
from .atmosphere import air_density
from .constants import GRAVITY
from .forces import (
    compute_lift,
    compute_drag,
    compute_thrust,
    compute_weight,
)


@dataclass
class SimulationState:
    """Current state of the aircraft in the simulation."""

    altitude_m: float = 0.0
    airspeed_m_s: float = 50.0
    angle_of_attack_deg: float = 3.0
    time_s: float = 0.0

    # Cached forces (N) from last step
    lift_N: float = 0.0
    drag_N: float = 0.0
    thrust_N: float = 0.0
    weight_N: float = 0.0

    # Net acceleration (m/s²) from last step
    acceleration_m_s2: float = 0.0


class AerodynamicsSimulator:
    """
    Simulates aircraft motion by integrating forces over time.

    Parameters can be changed between steps (e.g. throttle, angle of attack)
    to simulate pilot inputs or configuration changes.
    """

    def __init__(self, params: AircraftParams, dt_s: float = 0.1):
        self.params = params
        self.dt_s = dt_s
        self.state = SimulationState(
            altitude_m=params.altitude_m,
            airspeed_m_s=params.airspeed_m_s,
            angle_of_attack_deg=params.angle_of_attack_deg,
        )

    def sync_params_from_state(self) -> None:
        """Update params from current state (altitude, speed, alpha)."""
        self.params.altitude_m = self.state.altitude_m
        self.params.airspeed_m_s = self.state.airspeed_m_s
        self.params.angle_of_attack_deg = self.state.angle_of_attack_deg

    def step(self) -> SimulationState:
        """
        Advance one time step using current params.
        Uses simplified longitudinal dynamics: thrust–drag along flight path,
        lift–weight perpendicular. Angle of attack is set by params (no pitch
        dynamics in this simplified model).
        """
        self.sync_params_from_state()
        L = compute_lift(self.params)
        D = compute_drag(self.params)
        T = compute_thrust(self.params)
        W = compute_weight(self.params)

        alpha_rad = math.radians(self.params.angle_of_attack_deg)
        # Along flight path: T - D - W*sin(gamma). Assume small gamma ≈ 0.
        # So axial acceleration ≈ (T - D) / m (simplified).
        axial = (T - D) / self.params.mass_kg
        # Perpendicular: L - W*cos(gamma) ≈ L - W. If L != W, we'd change
        # flight path; here we only update speed from axial.
        self.state.lift_N = L
        self.state.drag_N = D
        self.state.thrust_N = T
        self.state.weight_N = W
        self.state.acceleration_m_s2 = axial

        # Euler integration for speed
        v = self.state.airspeed_m_s
        self.state.airspeed_m_s = max(5.0, v + axial * self.dt_s)

        # Simple climb/descent: sin(gamma) ≈ (T - D) / W for small gamma
        if W > 0:
            sin_gamma = max(-0.5, min(0.5, (T - D) / W))
            climb_rate = self.state.airspeed_m_s * sin_gamma
            self.state.altitude_m = max(
                0.0, self.state.altitude_m + climb_rate * self.dt_s
            )

        self.state.time_s += self.dt_s
        return self.state

    def set_params(self, **kwargs) -> None:
        """Update simulation parameters (e.g. thrust_ratio, angle_of_attack_deg)."""
        for k, v in kwargs.items():
            if hasattr(self.params, k):
                setattr(self.params, k, v)
