#!/usr/bin/env python3
"""
Toy drone — roadmap experiment M3-f. A PID playground in plain Python: no ROS, no simulator.

A mass hangs in the air under gravity. Your controller chooses the thrust. That's all, and it's
enough to *see* what P, I and D do before you touch the real Swift Pico.

YOUR JOB: write the controller in `choose_thrust()` below, one term at a time:
  1. P only:  thrust = hover_guess + Kp * error          → run it. What does the height do?
  2. add D:   + Kd * (change in error per second)         → what happens to the bouncing?
  3. add I:   + Ki * (error accumulated over time)        → try --mass 2.0 first. Why is I needed?
  4. try:     --delay 0.1   (the sensor reports late)     → connect it to balancing a pen while looking away

    python3 toy_drone.py --kp 20                     # plot opens in a window
    python3 toy_drone.py --kp 20 --kd 8 --mass 2.0 --save run.png

Physics numbers come from the simulated Swift Pico: 1.5 kg, max thrust 21.9 N.
"""
import argparse
from collections import deque

import matplotlib.pyplot as plt

GRAVITY = 9.81
MAX_THRUST = 21.9       # newtons, all four motors at full power
HOVER_GUESS = 1.5 * GRAVITY  # what the controller THINKS hovering needs (it assumes 1.5 kg)


def choose_thrust(error, dt, memory, kp, ki, kd):
    """
    error  : setpoint height − measured height, in metres (positive = drone is too low)
    dt     : seconds since the previous call
    memory : a dict that survives between calls; store anything you need (previous error, sum, ...)
    returns: thrust in newtons (it gets clipped to 0 … 21.9 N, like real motors)
    """
    # ------------------------------------------------------------------------------------------
    # WRITE YOUR CONTROLLER HERE. Right now it only outputs the hover guess, so it ignores the error.
    thrust = HOVER_GUESS
    # ------------------------------------------------------------------------------------------
    return thrust


def simulate(kp, ki, kd, mass, delay, setpoint, seconds, dt=0.005):
    height, velocity, memory = 0.0, 0.0, {}
    # A queue of past heights models a sensor that reports `delay` seconds late
    sensor = deque([0.0] * max(1, int(delay / dt) + 1), maxlen=max(1, int(delay / dt) + 1))
    times, heights, thrusts = [], [], []
    for step in range(int(seconds / dt)):
        sensor.append(height)
        measured = sensor[0]
        thrust = min(max(choose_thrust(setpoint - measured, dt, memory, kp, ki, kd), 0.0), MAX_THRUST)
        acceleration = thrust / mass - GRAVITY
        velocity += acceleration * dt
        height += velocity * dt
        if height < 0:                # the ground
            height, velocity = 0.0, 0.0
        times.append(step * dt)
        heights.append(height)
        thrusts.append(thrust)
    return times, heights, thrusts


def describe(times, heights, setpoint):
    final = sum(heights[-200:]) / 200
    peak = max(heights)
    band = 0.05 * setpoint
    settled = next((t for i, t in enumerate(times) if all(abs(h - setpoint) <= band for h in heights[i:])), None)
    print(f'peak height        {peak:.2f} m   (overshoot {max(0, peak - setpoint):.2f} m)')
    print(f'final height       {final:.2f} m   (steady-state error {setpoint - final:+.2f} m)')
    print(f'settled within 5%  {"never" if settled is None else f"after {settled:.1f} s"}')


def main():
    parser = argparse.ArgumentParser(description='Toy 1-D drone for PID experiments.')
    parser.add_argument('--kp', type=float, default=0.0)
    parser.add_argument('--ki', type=float, default=0.0)
    parser.add_argument('--kd', type=float, default=0.0)
    parser.add_argument('--mass', type=float, default=1.5, help='real mass in kg (the controller still assumes 1.5)')
    parser.add_argument('--delay', type=float, default=0.0, help='sensor delay in seconds')
    parser.add_argument('--setpoint', type=float, default=2.0, help='target height in metres')
    parser.add_argument('--seconds', type=float, default=15.0)
    parser.add_argument('--save', help='save the plot to this file instead of opening a window')
    args = parser.parse_args()

    times, heights, thrusts = simulate(args.kp, args.ki, args.kd, args.mass, args.delay, args.setpoint, args.seconds)
    describe(times, heights, args.setpoint)
    figure, (top, bottom) = plt.subplots(2, 1, sharex=True, figsize=(8, 6))
    top.plot(times, heights, label='height')
    top.axhline(args.setpoint, linestyle='--', color='gray', label='setpoint')
    top.set_ylabel('height (m)')
    top.legend()
    top.set_title(f'Kp={args.kp} Ki={args.ki} Kd={args.kd}  mass={args.mass} kg  delay={args.delay} s')
    bottom.plot(times, thrusts, color='tab:orange')
    bottom.set_ylabel('thrust (N)')
    bottom.set_xlabel('time (s)')
    figure.tight_layout()
    if args.save:
        figure.savefig(args.save)
        print(f'plot saved to {args.save}')
    else:
        plt.show()


if __name__ == '__main__':
    main()
