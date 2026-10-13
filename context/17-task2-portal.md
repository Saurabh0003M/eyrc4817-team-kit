# Task 2 — what the portal says (read 2026-10-13, both themes)

Read through the team's portal login. This supersedes the guesses in `16-task2-from-repos.md` where they
differ. Summarised in our own words; the portal pages are the authority.

## Deadlines (from each theme's announcements page)

| Subtask | What | Marks | Deadline |
|---|---|---|---|
| **KD 2A** | write your own position controller (PID or LQR) and hold a setpoint | 20 | **12 Oct 2026 (PASSED)** |
| **KD 2B** | ROS 2 action + service waypoint navigation, 4 fixed waypoints | 40 | **19 Oct 2026** |
| **KD 2C** | waypoints come from the camera: detect critical survivors, plan a route | 40 | **26 Oct 2026** |
| **PB 2A** | maze traversal: random spawn, one pellet, exit; no time limit | 30 | **15 Oct 2026** |
| **PB 2B** | fixed spawn, 3 random pellets, a ghost guards one, exit; time counts | 70 | **26 Oct 2026** |

Each KD subtask builds on the previous one (2B drives the 2A controller; 2C drives the 2B pipeline).
**Late policy: not stated on any Task 2 page.** In Task 1, late uploads were still marked (e-Ratna lost). Ask on
the forum before assuming the same for KD 2A.
**Theme commitment:** no Task 2 page asks the team to pick one theme; both courses carry Task 2.

## KD 2A — position controller (20)
- Boilerplate: `~/pico_ws/src/swift_pico/src/pico_controller_PID.py` or `_LQR.py` (or `.cpp`). Pick one language, one controller.
- Position comes from WhyCode (`/whycode_node/markers`), in raw marker units, not metres. Boilerplate reads X; do Y and Z the same way.
- Set the setpoint to **(1.5, −1.5, 13)**. Publish the error on `/pos_error` every cycle; send `SwiftMsgs` on `/drone_command`; run on a timer (`self.sample_time`).
- PID: build P, then D, then I (guard against integral windup); tune live with `ros2 launch pid_tune pid_tune_drone.launch.py` (1C gains load as a start). LQR: model, solve K, tune Q/R not K.
- **Rebuild (`colcon build`) after every edit**: `ros2 run` runs the built copy.
- **Hardcode the final gains** in the submitted script (no GUI at evaluation).
- Record: launch sim → `ros2 bag record -o task_2a /pos_error /whycode_node/markers /controller_heartbeat` *before* starting the controller (a late bag scores 0) → run controller ≥ 60 s.
- Zip `KD_4817_task_2a.zip` = `KD_4817_task_2a.py` + `task_2a_0.db3` + `metadata.yaml` (no folder). YouTube unlisted, title `KD_4817_Task_2a`, one continuous take.
- Score /20: hold 8 (per second of longest hold, up to 10 s, all axes within ±0.4) + finishing bonus 4 (only with the full 10 s) + speed 8 (full if the hold ends by 15 s, −0.18/s after, 0 at 60 s).

## KD 2B — waypoint navigation (40)
- New package `waypoint_navigation` (`ros2 pkg create --build-type ament_cmake`), with exactly:
  - `action/NavToWaypoint.action`: `geometry_msgs/Pose waypoint`, `bool hover` / `---` / `int32 hov_time` / `---` / `geometry_msgs/PoseStamped current_waypoint`
  - `srv/GetWaypoints.srv`: `bool get_waypoints` / `---` / `geometry_msgs/PoseArray waypoints`, `string[] marker_ids`
- Nodes in `swift_pico/src/`: `waypoint_service` (returns the waypoints), `pico_client` (asks the service, sends goals one by one on action `waypoint_navigation`, waits for each result), `pico_server` (flies each goal with the 2A controller, streams feedback = current pose, returns settle time).
- Waypoints, in this order: wp1 (−2.41, −2.41, 13), wp2 (2.41, 1.20, 13), wp3 (1.20, −2.41, 13), wp4 (−1.20, 1.20, 13).
- Yaw now matters: add a P or PD yaw hold using the boilerplate's yaw variable and setpoint.
- Fill `swift_pico/CMakeLists.txt` + `package.xml` (install the scripts, depend on `waypoint_navigation`). C++ nodes need different names (`pico_server_cpp`).
- Run order: sim → service → client → **bag** (`ros2 bag record -o task_2b /whycode_node/markers /controller_heartbeat`) → server last (it starts the flight).
- Zip `KD_4817_task_2b.zip` = `KD_4817_waypoint_service.py`, `KD_4817_pico_client.py`, `KD_4817_pico_server.py`, `task_2b_0.db3`, `metadata.yaml`. Same language for all three. YouTube `KD_4817_Task_2b`.
- Score /40: per waypoint reach 2 + hold 3 s 6; speed 8 only if all four held (full by 40 s, −0.13/s, 0 at 100 s cap). In order; a skipped waypoint can't score.

## KD 2C — perception-driven waypoints (40)
- Only `waypoint_service` changes: subscribe once to `/image_raw` (one latched frame; QoS reliable + transient local), run the Task 1A detector, keep the 4 **critical** survivors, map intersections to (X, Y) via `scripts/grid_whycode_coordinates.csv` (Z = 13), plan a route from the start **F6**, store it, destroy the subscription, answer `GetWaypoints` only once the route exists.
- Hover 3 s only at survivors; intermediate intersections are fly-through. Never hardcode waypoints.
- **Not in the repo yet (2026-10-13):** the CSV (repo has `src/grid_whycode_coordinates.json`) and the latched `/image_raw` frame. Expect another `git pull`.
- Zip `KD_4817_task_2c.zip` (same 5-file shape, `task_2c_0.db3`). Score /40: per survivor reach 2 + hold 6; speed 8 (full by 60 s, −0.2/s, 0 at 100 s). Any order.

## PB 2A — maze traversal (30)
- Topics: `pacbot/sensors` (100 Hz: `fl`/`fr` look SIDEWAYS, `sl`/`sr` look FORWARD; ToF max 2.0 m; `gyro[2]` turn rate; encoder totals, 360 ticks/turn), `pacbot/poses` (once: spawn `[row,col]`, `dir` 0 E 1 N 2 W 3 S), `pacbot/pellets` (once: `{"pellet": [r,c]}`), `pacbot/wheel_vel` (rad/s, ±30, **exact format as the boilerplate builds it**), `pacbot/result`.
- No live position: dead-reckon from gyro + encoders. Wheel radius 0.017 m, half track 0.039 m, axle 0.033 m behind centre. Cell (r,c) centre = (0.22·c, 0.22·(14−r)). Exit: south side of (14,14).
- Keep the boilerplate's function names and structure.
- Submit: screen-record → `./task_2a_launch --evaluate` → wait for "PacBot Task2A started" → run code → MAZE SOLVED → zip `PB#4817.zip` = `result.json` + `task_2a_boilerplate.py` (never open result.json). YouTube unlisted.
- Score: max(0, 20·exited + 10·pellet − 5·collisions). No time limit: drive cleanly.

## PB 2B — pellet collection (70)
- Same topics minus `pacbot/poses` (spawn fixed at (−0.15, 0), facing east), plus `pacbot/ghost` (100 Hz `{"row","col","x","y"}`). `pacbot/pellets` = `{"pellets": [[r,c],...]}` at start and after each collection; `[]` = all done. Collected within 0.06 m of a cell centre.
- Ghost: fixed loop around one pellet, never chases, slower than the bot. **Touching it ends the run (score 0).** Watch it, wait for it to pass.
- **Headings run counter-clockwise here** (`(h+1)%4` = left), the opposite of Task 1B.
- Run ends when the chassis crosses x = 3.19 (east border). Clock starts at first movement, so planning first is free. Suggested: shortest paths between spawn, pellets, exit; try all 6 pellet orders.
- Submit like 2A with `./task_2b_launch --evaluate`; zip `PB#4817.zip` = `result.json` + `task_2b_boilerplate.py`.
- Score (only if it exits; ghost catch or no exit = 0): max(0, 5·P + T − 1.5·NC), T = max(10, 55 − 0.085·t) only when all 3 pellets, else 0.
