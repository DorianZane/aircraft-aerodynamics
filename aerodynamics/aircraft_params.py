"""
Configurable aircraft parameters for the aerodynamics model.

Adjust these to simulate different aircraft or flight conditions.
"""

from dataclasses import dataclass


@dataclass
class AircraftParams:
    """
    Aircraft and flight parameters. All can be changed to explore the model.

    Geometry & mass:
        mass_kg: Aircraft mass (kg)
        wing_area_m2: Wing reference area (m²)
        aspect_ratio: Wing aspect ratio (span² / area). Affects induced drag.

    Aerodynamic coefficients (simplified polar):
        cl_alpha: Lift curve slope (per radian). Cl ≈ cl_alpha * alpha.
        cd0: Zero-lift drag coefficient (parasitic drag).
        oswald_efficiency: Wing efficiency (0.7–0.9). Affects induced drag.

    Propulsion:
        max_thrust_N: Maximum thrust (N). Set to 0 for glider.
        thrust_ratio: Throttle 0–1. Actual thrust = max_thrust_N * thrust_ratio.

    Flight condition:
        altitude_m: Altitude (m). Affects air density.
        airspeed_m_s: True airspeed (m/s).
        angle_of_attack_deg: Angle of attack (degrees).
    """

    # Mass & geometry
    mass_kg: float = 1000.0
    wing_area_m2: float = 20.0
    aspect_ratio: float = 8.0

    # Lift/drag model
    cl_alpha: float = 5.5  # per radian, typical for thin airfoil ~2*pi
    cd0: float = 0.025
    oswald_efficiency: float = 0.82

    # Thrust
    max_thrust_N: float = 5000.0
    thrust_ratio: float = 1.0  # 0 = idle, 1 = full

    # Flight condition
    altitude_m: float = 0.0
    airspeed_m_s: float = 50.0
    angle_of_attack_deg: float = 3.0

    def copy_with(self, **kwargs) -> "AircraftParams":
        """Return a new instance with only the given fields updated."""
        d = {
            "mass_kg": self.mass_kg,
            "wing_area_m2": self.wing_area_m2,
            "aspect_ratio": self.aspect_ratio,
            "cl_alpha": self.cl_alpha,
            "cd0": self.cd0,
            "oswald_efficiency": self.oswald_efficiency,
            "max_thrust_N": self.max_thrust_N,
            "thrust_ratio": self.thrust_ratio,
            "altitude_m": self.altitude_m,
            "airspeed_m_s": self.airspeed_m_s,
            "angle_of_attack_deg": self.angle_of_attack_deg,
        }
        d.update(kwargs)
        return AircraftParams(**d)
