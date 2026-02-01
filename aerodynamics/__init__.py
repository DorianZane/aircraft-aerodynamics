"""
Aircraft Aerodynamics Simulation Model

Simulates lift, drag, thrust, and weight with configurable parameters.
"""

from .aircraft_params import AircraftParams
from .atmosphere import air_density
from .forces import compute_lift, compute_drag, compute_thrust_required
from .simulation import SimulationState, AerodynamicsSimulator

__all__ = [
    "AircraftParams",
    "air_density",
    "compute_lift",
    "compute_drag",
    "compute_thrust_required",
    "SimulationState",
    "AerodynamicsSimulator",
]
