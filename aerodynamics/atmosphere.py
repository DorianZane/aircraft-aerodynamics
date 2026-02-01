"""
Standard atmosphere model: air density and pressure vs altitude.
"""

from .constants import (
    GRAVITY,
    RHO_SEA_LEVEL,
    TEMP_SEA_LEVEL,
    LAPSE_RATE,
    GAS_CONSTANT,
    PRESSURE_SEA_LEVEL,
)


def air_density(altitude_m: float) -> float:
    """
    Air density (kg/m³) at given altitude using ISA troposphere model.
    Valid for 0 <= altitude <= 11000 m.
    """
    if altitude_m <= 0:
        return RHO_SEA_LEVEL
    if altitude_m > 11000:
        # Simple extension: use stratosphere constant temp
        T_11 = TEMP_SEA_LEVEL - LAPSE_RATE * 11000
        rho_11 = RHO_SEA_LEVEL * (T_11 / TEMP_SEA_LEVEL) ** (
            (GRAVITY * 0.0289644) / (GAS_CONSTANT * LAPSE_RATE) - 1
        )
        return rho_11 * (2.718 ** (-0.000157 * (altitude_m - 11000)))
    T = TEMP_SEA_LEVEL - LAPSE_RATE * altitude_m
    return RHO_SEA_LEVEL * (T / TEMP_SEA_LEVEL) ** (
        (GRAVITY * 0.0289644) / (GAS_CONSTANT * LAPSE_RATE) - 1
    )


def pressure(altitude_m: float) -> float:
    """Pressure (Pa) at given altitude."""
    if altitude_m <= 0:
        return PRESSURE_SEA_LEVEL
    T = TEMP_SEA_LEVEL - LAPSE_RATE * min(altitude_m, 11000)
    return PRESSURE_SEA_LEVEL * (T / TEMP_SEA_LEVEL) ** (
        -GRAVITY / (GAS_CONSTANT * LAPSE_RATE)
    )
