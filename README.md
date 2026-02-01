# Aircraft Aerodynamics Simulation Model

A configurable software model that simulates aircraft aerodynamics: **lift**, **drag**, **thrust**, and **weight** with adjustable parameters.

## Model Overview

- **Lift**: \( L = \frac{1}{2} \rho V^2 S C_L \), with \( C_L \) from angle of attack (linear lift curve).
- **Drag**: \( D = \frac{1}{2} \rho V^2 S C_D \), with \( C_D = C_{D0} + \frac{C_L^2}{\pi e \cdot AR} \) (parasitic + induced).
- **Atmosphere**: Standard atmosphere (air density vs altitude).
- **Thrust**: Configurable max thrust and throttle (0–1).

All parameters (mass, wing area, aspect ratio, coefficients, altitude, airspeed, angle of attack, thrust) can be changed to explore different aircraft and flight conditions.

## Quick Start

```bash
# Default parameters (steady-state + time evolution)
python run_simulation.py

# Change parameters from the command line
python run_simulation.py --altitude 5000 --speed 60 --alpha 5
python run_simulation.py --mass 1500 --wing-area 25 --throttle 0.8
python run_simulation.py --aspect-ratio 10 --cd0 0.02 --steps 100
```

## Changing Parameters in Code

```python
from aerodynamics import AircraftParams, compute_lift, compute_drag, air_density

# Start with defaults
params = AircraftParams()

# Steady-state forces at current condition
lift = compute_lift(params)
drag = compute_drag(params)
rho = air_density(params.altitude_m)

# Create a heavier, higher-altitude variant
params_heavy = params.copy_with(mass_kg=2000, altitude_m=3000)
lift_heavy = compute_lift(params_heavy)
drag_heavy = compute_drag(params_heavy)

# Change angle of attack and airspeed
params_fast = params.copy_with(airspeed_m_s=80, angle_of_attack_deg=2)
```

## Time-Stepping Simulation

```python
from aerodynamics import AircraftParams, AerodynamicsSimulator

params = AircraftParams(
    mass_kg=1000,
    wing_area_m2=20,
    airspeed_m_s=50,
    angle_of_attack_deg=3,
    thrust_ratio=0.9,
)
sim = AerodynamicsSimulator(params, dt_s=0.1)

# Run 100 steps; you can change params between steps
for _ in range(100):
    state = sim.step()
    print(state.altitude_m, state.airspeed_m_s, state.lift_N, state.drag_N)

# Reduce throttle mid-flight
sim.set_params(thrust_ratio=0.5)
for _ in range(50):
    state = sim.step()
```

## Configurable Parameters

| Parameter | Description | Typical range |
|-----------|-------------|---------------|
| `mass_kg` | Aircraft mass (kg) | 500–50000 |
| `wing_area_m2` | Wing reference area (m²) | 10–200 |
| `aspect_ratio` | Span²/area | 6–12 |
| `cl_alpha` | Lift curve slope (per rad) | ~5–6 |
| `cd0` | Zero-lift drag coefficient | 0.02–0.04 |
| `oswald_efficiency` | Wing efficiency | 0.7–0.9 |
| `max_thrust_N` | Max thrust (N) | 0 (glider) to 100000+ |
| `thrust_ratio` | Throttle 0–1 | 0–1 |
| `altitude_m` | Altitude (m) | 0–15000 |
| `airspeed_m_s` | True airspeed (m/s) | 20–300 |
| `angle_of_attack_deg` | Angle of attack (°) | 0–15 (linear model) |

## Project Layout

```
Math Genius/
├── aerodynamics/
│   ├── __init__.py
│   ├── aircraft_params.py   # Configurable parameters
│   ├── atmosphere.py        # Air density vs altitude
│   ├── constants.py         # Physical constants
│   ├── forces.py            # Lift, drag, thrust, weight
│   └── simulation.py        # Time-stepping simulator
├── run_simulation.py        # CLI + demo
├── requirements.txt
└── README.md
```

## Notes

- The lift model is **linear** in angle of attack (no stall).
- Drag uses a simple polar: \( C_D = C_{D0} + C_L^2/(\pi e \cdot AR) \).
- Time-stepping uses a simplified longitudinal model (thrust–drag along path, simple climb/descent from excess/deficit thrust).

You can extend the model with stall curves, different atmosphere models, or 6-DOF dynamics as needed.
# aircraft-aerodynamics
