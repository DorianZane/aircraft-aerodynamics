"""
Aerodynamic forces: lift, drag, and thrust.

Uses:
  Lift  = ½ ρ V² S Cl
  Drag  = ½ ρ V² S Cd
  Cd    = Cd0 + Cl² / (π e AR)
  Cl    = cl_alpha * alpha (linear, small alpha)
"""

import math
from .aircraft_params import AircraftParams
from .atmosphere import air_density
from .constants import GRAVITY


def lift_coefficient(angle_of_attack_rad: float, cl_alpha: float) -> float:
    """Lift coefficient from angle of attack (linear, no stall)."""
    return cl_alpha * angle_of_attack_rad


def drag_coefficient(
    cl: float, cd0: float, aspect_ratio: float, oswald_efficiency: float
) -> float:
    """Total drag coefficient: parasitic + induced."""
    if aspect_ratio <= 0 or oswald_efficiency <= 0:
        return cd0
    induced = (cl ** 2) / (math.pi * oswald_efficiency * aspect_ratio)
    return cd0 + induced


def dynamic_pressure(rho: float, velocity: float) -> float:
    """q = ½ ρ V² (Pa)."""
    return 0.5 * rho * velocity * velocity


def compute_lift(params: AircraftParams) -> float:
    """Lift force (N) for current flight condition."""
    rho = air_density(params.altitude_m)
    alpha_rad = math.radians(params.angle_of_attack_deg)
    cl = lift_coefficient(alpha_rad, params.cl_alpha)
    q = dynamic_pressure(rho, params.airspeed_m_s)
    return q * params.wing_area_m2 * cl


def compute_drag(params: AircraftParams) -> float:
    """Drag force (N) for current flight condition."""
    rho = air_density(params.altitude_m)
    alpha_rad = math.radians(params.angle_of_attack_deg)
    cl = lift_coefficient(alpha_rad, params.cl_alpha)
    cd = drag_coefficient(
        cl, params.cd0, params.aspect_ratio, params.oswald_efficiency
    )
    q = dynamic_pressure(rho, params.airspeed_m_s)
    return q * params.wing_area_m2 * cd


def compute_thrust(params: AircraftParams) -> float:
    """Thrust (N) from throttle and max thrust."""
    return params.max_thrust_N * max(0.0, min(1.0, params.thrust_ratio))


def compute_weight(params: AircraftParams) -> float:
    """Weight (N)."""
    return params.mass_kg * GRAVITY


def compute_thrust_required(params: AircraftParams) -> float:
    """
    Thrust required for steady, level flight (T = D at L = W).
    Does not depend on max_thrust or thrust_ratio.
    """
    return compute_drag(params)
