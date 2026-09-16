# Theme 7 — PacBot (PB) · SECONDARY

Source: `_extracted/Themes__Chosen__eYRC_Theme_7_PacBot.txt`. Carried only **through Task 1**; the
team commits to one theme from Task 2/3. Year recommendation: **all years**. Tags: Simulator +
Hardware, Maze Solving, Pathfinding, Grid Navigation.

## Mission

A Pac-Man-inspired bot in a known maze must collect scattered pallets and reach the exit while a
pre-programmed Ghost bot patrols the corridors. The layout is known; surviving it is the problem.
Every pallet costs time; every second lets the Ghost close in.

## The 5 objectives

1. Find a path collecting maximum points while avoiding all Ghosts
2. Decide how aggressively to collect before heading for the exit
3. Reach the exit before escape routes are cut off
4. Reroute in real time as Ghost positions change every second
5. Balance points against survival

## Build targets

- Real-time Ghost tracking that dynamically reroutes the moment a threat appears
- A decision engine choosing between collecting and exiting
- A sensor layer detecting walls, corridors and Ghost positions
- A tuned motor control system for precise movement without collision or drift

## Toolkit

MQTT · MuJoCo · Linux · Arduino IDE · Git. Skills: embedded systems, path planning, Embedded C,
Python, realtime decision algorithms, PID control.

## Stage 2 kit

ESP WROOM-32 MCU · TB6612FNG motor driver · N20 motor (3V, 500 RPM) with encoder · N20 wheel ·
VL53L1X ToF sensor · MPU6050 IMU · LiPo 3.7V 850mAh 1S · charger.

## System requirements

Ubuntu 22.04 LTS · >4 cores x86_64 · 100 GB+ · 8 GB+ RAM · dedicated GPU **preferable**.

## Analysis

*(claude-code, 2026-09-12)*

**[OPINION]** PB is the strictly easier theme and a sane hedge: ESP32 + Arduino IDE is a far shorter
runway than ROS 2 + Gazebo, and the maze problem is classical graph search. If Task 0/1 shows the
team drowning in the Linux/ROS 2 setup, PB is the honest fallback rather than a failed KD run.

**[OPINION]** Shared prep between the two themes: Linux, Git, PID control, path planning. Those four
carry over whichever theme survives, so **front-load them** — no prep is wasted.
