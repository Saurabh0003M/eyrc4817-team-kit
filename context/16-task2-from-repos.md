# Task 2 — what the official repos show (read 2026-10-12)

**Source of truth for task code:** e-Yantra publishes every task's launchers and boilerplate in two
GitHub repos, and both are already cloned on the Ubuntu box. Marks, deadlines, rules and the
submission format are **only on the portal**; the repos never state them.

| Theme | Repo | Local clone | Branch | Update with |
|---|---|---|---|---|
| KD | `eYantra-Robotics-Competition/eYRC_26-27_Khojo-Drone` | `~/pico_ws/src` | `kd_sim` (also `turtle_sim`, `main`) | `git -C ~/pico_ws/src stash && git -C ~/pico_ws/src pull && git -C ~/pico_ws/src stash pop`, then `cd ~/pico_ws && colcon build` (plain, never `--symlink-install`). Stash is needed: we edited 6 tracked files (Task 2 nodes, CMakeLists.txt, package.xml) |
| PB | `eYantra-Robotics-Competition/eYRC_26-27_PacBot` | `~/pacbot_ws` | `main` | `git -C ~/pacbot_ws stash && git -C ~/pacbot_ws pull && git -C ~/pacbot_ws stash pop` (repo README's own method; Task 2 is written into the tracked boilerplates) |

Pulled 2026-10-12: KD `3318915 → af3b062`, PB `2c1343c → a5fad58`. Fresh `colcon build` of
`~/pico_ws`: 17/17 packages. All team files (untracked) survived both pulls.

## KD Task 2 (repo commits "Task 2 released" 2026-10-05, boilerplate fix 2026-10-07)

**From the repo:**
- New boilerplate in `swift_pico/src/`, each in `.py` and `.cpp`: `pico_controller_PID`,
  `pico_controller_LQR`, `pico_server` (action server `waypoint_server`), `pico_client`,
  `waypoint_service`. The server comment says "use either PID or LQR".
- Position now comes from **WhyCon** (`/whycode_node/markers`), not `/rotors/odometry`. The PID
  boilerplate's hold point is `[1.0, -1.0, 13.0]`.
- The server holds yaw (`desired_yaw = -0.5` degrees, from the WhyCon marker rotation) and tracks
  **time spent inside a sphere** around each waypoint.
- Action `NavToWaypoint`, action name `waypoint_navigation`; service `GetWaypoints`, service name
  `waypoints`.
- `grid_whycode_coordinates.json` maps grid names A1–K11 to WhyCon x/y (links Task 1A's grid to flight).
- Arena: the three black obstacles and the yellow circles were removed; red triangles only.
- `task_1b_controller` / `task_1c_controller` binaries were **deleted** upstream (Task 1 is over).

**Inferred, not stated:** the `waypoint_navigation` interface package (the `.action` and `.srv`
files) is not in the repo, and `package.xml` has its dependency commented out, so the team
probably has to create it. Confirm on the portal.

**Dependency `tf_transformations` (the server imports it).** Installed on the Ubuntu box 2026-10-12:
`sudo apt install ros-humble-tf-transformations`, then `pip3 install --user --upgrade transforms3d`.
Trap: apt's `python3-transforms3d` 0.3.1 uses `np.float`, which numpy ≥1.24 removed, so the import
crashes with `module 'numpy' has no attribute 'float'`. The pip upgrade puts a newer transforms3d in
`~/.local`, which wins; numpy stays 1.26.4 (must stay below 2). The LQR library import is left
blank in the boilerplate.

## PB Task 2 (repo commit "Task 2 Added" 2026-10-05)

New folders `task2a/` and `task2b/`, each with `task_2x_launch` (sealed binary, same tamper rule
as Task 1), `lib/`, `meshes/`, boilerplate. Keep each folder together: the launcher finds `lib/`
and `meshes/` beside itself. Both are MQTT + MuJoCo, 15×15 maze, 0.22 m cells.

| | 2A | 2B |
|---|---|---|
| Maze | fixed, embedded in the boilerplate | fixed "official" maze in `maze_2b.py` |
| Start | random cell, random open heading | west entrance, row 14, heading east |
| Goal | pass the pellet cell, exit −y side of (14, 14) | collect **3 pellets** (random every run), exit east at row 7 |
| Score in repo | 20 solve + 10 pellet − 5 per wall collision | not stated ("no score, no time" in result) |
| Your part | BFS over walls, dead-reckon pose from encoders + gyro, drive the action list | one TODO in `decide()` (+ optional planning hook) |

Topics: in `pacbot/poses`, `pacbot/pellets` (retained, once), `pacbot/sensors` (every 10 ms: ToF,
gyro, accelerometer, encoder ticks), `pacbot/result`; out `pacbot/wheel_vel` (rad/s).

## PB Task 2 smoke test on Gauri's OMEN (2026-10-12, verified)
- Both launchers start with the bundled libs; mosquitto active; paho-mqtt 2.1.0. Stock boilerplates connect,
  receive the start messages and stream `pacbot/wheel_vel`.
- **2B ghost:** `pacbot/ghost` `{"row","col","x","y"}` every sensor frame (x/y in the maze's metre frame). Example run:
  pellets (3,3) (4,12) (12,10); "ghost guarding the pellet at (12,10), a path of 7 cells". The boilerplate already
  subscribes (`controller.ghost`).
- **2B modes:** `./task_2b_launch` = practice (nothing written); `./task_2b_launch --evaluate` = scored run that writes
  the sealed `result.json`, zipped as `PB#4817.zip`. Maze, pellet rules and **time limit are built in**.
- 2A launcher has no `--help` (it treats the argument as a model file). Run it with no arguments. Never probe the binaries further (tamper rule).
- **Trap: retained MQTT messages survive between tasks.** The 2B run also received 2A's retained `pacbot/poses`
  and the old `pacbot/pellets {"pellet": ...}`. Parse by the key you expect (`"pellets"` in 2B), or clear stale
  retained topics before a scored run: `mosquitto_pub -t pacbot/poses -r -n` (same for `pacbot/pellets`).

## Dates and marks (from the brain note "eYRC Task 2 — released 2026-10-05, both themes", 2026-10-08)
Source: the public PacBot task site https://themes.e-yantra.org/Pacbot_2627/ . The competition runs one
schedule, but **verify the KD dates on the portal**.

| Task | Window |
|---|---|
| **Task 2** | **6 Oct – 26 Oct 2026** |
| Task 3 | 27 Oct – 16 Nov 2026 (end of Stage 1) |

- PacBot Task 2 = 100: **2A Maze Traversal 30** (no time limit), **2B Pellet Collection 70**: a **ghost
  patrols one of the three pellets**, and **every second costs marks**. The 2B boilerplate does not
  mention the ghost, so read the task site for its topic and behaviour.
- KD Task 2 marks: not public; portal only.

## Still UNKNOWN — portal
KD Task 2 marks and submission files; whether both themes still need Task 2 or the team commits to
one now; whether KD rewards LQR over PID.
