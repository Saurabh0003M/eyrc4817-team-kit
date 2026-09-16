# Theme 2 — Khoj-o-Drone (KD) · PRIMARY

Source: `_extracted/Themes__Chosen__eYRC_Theme_2_Khoj_o_Drone.txt` (verbatim). This file is the
distilled version plus analysis. Year recommendation: **3rd, 4th**. Tags: Simulator + Hardware,
Drone Flight Control, Path Planning.

## Mission

A quadcopter searching for survivors in a disaster-stricken area. It interprets a changing
environment, adapts its flight to navigate uncertainty, and maximises search efficiency while
accurately localising people in need.

## The 7 objectives

1. Autonomously explore the disaster zone
2. Safely navigate hazardous, cluttered environments
3. Detect trapped survivors
4. Accurately estimate and record each survivor's location
5. Maintain stable flight throughout
6. Transmit survivor coordinates to the ground station
7. Prioritise critical survivors while locating all of them within mission time

## Build targets → what you actually have to write

| Build target | The real engineering problem | Where it lands |
|---|---|---|
| Efficient exploration strategy | coverage path planning, maximise area / minimise time | Task 2+ |
| Robust localisation pipeline | detect survivors, estimate world coordinates | Task 2+ |
| Safe navigation | obstacle / debris avoidance without stopping the search | Task 2+ |
| **Stable flight controllers** | **PID / LQR, waypoint tracking, smooth manoeuvring** | **Task 1 — most likely** |
| Autonomous trajectory generation | waypoint sequencing and execution | Task 2+ |

## Win condition

The drone autonomously explores the zone, identifies both critical and stable survivors, prioritises
critical ones during the search, and reliably reports every detected survivor's coordinates to the
ground station before time expires.

## Toolkit

- **Core hardware:** nano quadcopter with a **WhyCode marker on top**
- **Tools:** Gazebo / MuJoCo (drone sim), Linux, **Betaflight Configurator**, Git, ROS 2
- **Skills:** image processing, control systems (PID / LQR), ROS 2, Python / C++, planning & navigation algorithms

## Stage 2 hardware kit (free, only to teams clearing Stage 1)

Flight controller · motors · RadioMaster Ranger Nano 2.4 GHz ELRS module · battery · battery charger ·
clear propellers · 3D-printed parts · frame · camera · **WhyCon sticker**

## System requirements

Ubuntu 22.04 LTS · >4 cores x86_64 · 100 GB+ SSD · 8 GB+ RAM · dedicated GPU **not** necessary.

## Analysis — what this theme actually is

*(claude-code, 2026-09-12. Marked by confidence.)*

**[INFERRED, moderate confidence]** The WhyCon marker places KD in a direct lineage with every past
eYRC drone theme: Vitarana Drone (2020) → Sentinel Drone (2022) → Luminosity Drone (2023) →
Warehouse Drone (2024) → KrishiDrone (2025). That lineage's Stage-1 pattern has been consistent: an
overhead camera tracks a WhyCon/WhyCode marker on the drone, giving position; the team writes a
**PID position controller** to hold a setpoint, then to track waypoints. Expect Task 1 to be that.
**Verify against the real task doc before committing prep time.**

**[DOC-SOURCED]** Betaflight Configurator + a RadioMaster ELRS module in the kit means this is a real
FPV-builder stack, not a purely academic one. Stage 2 will involve flashing/configuring flight
controller firmware and binding a radio link — not just writing ROS nodes.

**[INFERRED]** "Prioritise critical survivors" is a scheduling/decision problem on top of coverage
planning, not just detection. Likely where the top teams separate from the rest in Task 2.

**[OPINION]** Relevant to Saurabh's hardware-security interest: an ELRS radio link, a
flight-controller configuration protocol over serial, and a ground station receiving coordinates is a
genuine attack surface. Worth a look **after** the competition work is solid — do not let it displace
Task 0/1.

## Prep priority, highest value first

1. **PID control** — what P, I and D each do physically, why integral windup happens, how to tune by
   hand. Gauri's EE control-systems coursework covers this; she should teach it to the other three.
2. **Linux + terminal fluency** — gates everything. Non-negotiable for all four.
3. **ROS 2 basics** — nodes, topics, publishers/subscribers, `colcon build`. Breadth over depth.
4. **Image processing / OpenCV** — marker detection, coordinate estimation.
5. **Path planning** — A*, coverage planning. Matters from Task 2, not Task 0.

## Learning resources

From `05-competition-reference.md`, filtered to what's relevant to KD:
- e-Yantra official YouTube (@eyantra): **MOOC on Getting Started with ROS 2**; **SLAM on UAVs
  (eYSIP 2025)**; **eYSIP 2024 Flight Controller Development**; **Introduction to Linux** technical
  session (Aug 2026); **Seeing Like a Robot** (image processing, Aug 2026).
- Past theme reveals for Warehouse Drone (2024) and KrishiDrone (2025) — closest analogues.
