#!/usr/bin/env python3
"""
Run the aircraft aerodynamics simulation with configurable parameters.

Examples:
  python run_simulation.py                    # default params, steady flight
  python run_simulation.py --altitude 5000    # high altitude (thinner air)
  python run_simulation.py --alpha 5 --speed 60
  python run_simulation.py --throttle 0.7     # reduce thrust
"""

import argparse

from aerodynamics import (
    AircraftParams,
    AerodynamicsSimulator,
    air_density,
    compute_lift,
    compute_drag,
    compute_thrust_required,
)


def main():
    parser = argparse.ArgumentParser(
        description="Simulate aircraft aerodynamics with adjustable parameters."
    )
    parser.add_argument(
        "--mass", type=float, default=1000, help="Aircraft mass (kg)"
    )
    parser.add_argument(
        "--wing-area", type=float, default=20, help="Wing area (m²)"
    )
    parser.add_argument(
        "--aspect-ratio", type=float, default=8, help="Wing aspect ratio"
    )
    parser.add_argument(
        "--cd0", type=float, default=0.025, help="Zero-lift drag coefficient"
    )
    parser.add_argument(
        "--altitude", type=float, default=0, help="Altitude (m)"
    )
    parser.add_argument(
        "--speed", type=float, default=50, help="True airspeed (m/s)"
    )
    parser.add_argument(
        "--alpha", type=float, default=3, help="Angle of attack (degrees)"
    )
    parser.add_argument(
        "--max-thrust", type=float, default=5000, help="Max thrust (N)"
    )
    parser.add_argument(
        "--throttle", type=float, default=1.0, help="Throttle 0–1"
    )
    parser.add_argument(
        "--steps", type=int, default=50, help="Number of time steps to run"
    )
    parser.add_argument(
        "--dt", type=float, default=0.1, help="Time step (s)"
    )
    args = parser.parse_args()

    params = AircraftParams(
        mass_kg=args.mass,
        wing_area_m2=args.wing_area,
        aspect_ratio=args.aspect_ratio,
        cd0=args.cd0,
        altitude_m=args.altitude,
        airspeed_m_s=args.speed,
        angle_of_attack_deg=args.alpha,
        max_thrust_N=args.max_thrust,
        thrust_ratio=args.throttle,
    )

    # Steady-state summary (no time stepping)
    rho = air_density(params.altitude_m)
    lift = compute_lift(params)
    drag = compute_drag(params)
    weight = params.mass_kg * 9.81
    thrust_req = compute_thrust_required(params)

    print("=== Steady-state aerodynamics (current parameters) ===\n")
    print(f"  Altitude:        {params.altitude_m:.0f} m")
    print(f"  Air density:     {rho:.4f} kg/m³")
    print(f"  Airspeed:        {params.airspeed_m_s:.1f} m/s")
    print(f"  Angle of attack: {params.angle_of_attack_deg:.1f}°")
    print(f"  Mass:            {params.mass_kg:.0f} kg")
    print(f"  Wing area:       {params.wing_area_m2:.1f} m²")
    print(f"  Aspect ratio:    {params.aspect_ratio:.1f}")
    print()
    print(f"  Lift:            {lift:.1f} N")
    print(f"  Weight:          {weight:.1f} N")
    print(f"  Drag:            {drag:.1f} N")
    print(f"  Thrust required: {thrust_req:.1f} N (for level flight)")
    print(f"  Thrust (current): {params.max_thrust_N * params.thrust_ratio:.1f} N")
    print()

    if abs(lift - weight) > weight * 0.1:
        print("  → Lift ≠ Weight: aircraft would climb or descend.")
    if abs(args.throttle * params.max_thrust_N - thrust_req) > thrust_req * 0.1:
        print("  → Thrust ≠ Thrust required: speed will change over time.")
    print()

    # Time stepping
    sim = AerodynamicsSimulator(params, dt_s=args.dt)
    print(f"=== Time evolution ({args.steps} steps × {args.dt} s) ===\n")
    print(f"  {'Time(s)':>8} {'Alt(m)':>8} {'Speed(m/s)':>10} {'Lift(N)':>10} {'Drag(N)':>10} {'T(N)':>8} {'a(m/s²)':>8}")
    print("  " + "-" * 64)

    for _ in range(args.steps):
        state = sim.step()
        print(
            f"  {state.time_s:8.1f} {state.altitude_m:8.1f} {state.airspeed_m_s:10.1f} "
            f"{state.lift_N:10.1f} {state.drag_N:10.1f} {state.thrust_N:8.1f} {state.acceleration_m_s2:8.2f}"
        )

    print()
    print("Done. Change parameters via command-line flags to explore the model.")


if __name__ == "__main__":
    main()
