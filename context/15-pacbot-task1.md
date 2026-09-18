# PacBot Task 1 — 1A path planning (35) + 1B wall following (65)

Source: PB portal → Stage 1 → Task 1 (Overview; 1A Overview, Instructions, Submission; 1B Overview,
Instructions, Submission), pasted by Saurabh on 2026-09-16.
Deadline unknown. **The team commits to one theme from Task 2/3**, so decide whether to do PB
Task 1 at all.

## Rules that matter
- **`task_1a_launch` / `task_1b_launch` are encrypted executables. Opening, decompiling or modifying
  them counts as tampering → disqualification.** Only run them. (Claude used `file` on them and
  nothing more; never `strings`/`readelf`/`ldd` on these.)
- The boilerplate's **function names, arguments and return values must not change**: the evaluator
  looks for them. Write code only inside `choose_command()` (1A) and the marked sections (1B).
- Plagiarism-checked. Submissions are made by the team leader (portal), plus an **unlisted
  YouTube** screen recording.
- Stop both simulator and code with **Ctrl+C** (fixed MQTT client IDs; a hard kill leaves stale
  broker sessions).

## Task 1A — grid maze over MQTT (35 marks)
- Drive to **both pellets** (random reachable cells each run, so no hard-coded route), then **out an
  exit** (the maze has two). **One command per state update**; no queueing.
- The bot has a **heading**: `FRONT` moves one cell forward; `LEFT` / `RIGHT` turn 90°; `BACK` turns
  180°. Turns never fail; only FRONT can be refused. A step is often "turn, then FRONT", and getting
  that wrong is the #1 failure.
- Topics (broker `localhost:1883`):
| Topic | Direction | Payload | Retained |
|---|---|---|---|
| `robot/pose` | sim → you | JSON `{"row","col","yaw","valid"}`, yaw 0/90/180/270 = E/N/W/S | yes |
| `pellets/pose` | sim → you | JSON list of `[row, col]`, the source of truth | yes |
| `bot/cmd` | sim → you | **plain string** "0" pause / "1" run | yes |
| `robot/cmd_vel` | you → sim | **plain string** FRONT/LEFT/RIGHT/BACK | no |
- `valid: false` = refused (wall, off-grid other than an exit, unknown string, or paused).
- Debug: `mosquitto_sub -h localhost -t 'robot/pose' -t 'pellets/pose' -t 'bot/cmd' -v`; drive by
  hand with `mosquitto_pub -h localhost -t robot/cmd_vel -m FRONT`.
- **Scoring: 10 per pellet (×2) + 15 for exiting = 35.** 0 pellets and no exit = FAILED; anything
  else = SUCCESS.
- **Submission:** start the screen recording first (Maze UI and terminal both fully visible) →
  `./task_1a_launch --evaluate`, wait for "Evaluation mode enabled" → `python3 task_1a.py` → the run
  writes `result.yaml` → zip **the two files, not the folder** as **`PB#4817.zip`** containing
  `result.yaml` + `task_1a.py` → portal upload + unlisted YouTube link. Keep the video up until
  results are out.
- *Learning angle:* BFS/A* over a grid graph (`14-learnings-pacbot-mqtt-pathplanning.md`), plus
  pellet ordering, plus **heading-aware command generation** (a small state machine: target
  direction vs yaw → LEFT/RIGHT/BACK/FRONT). Saurabh writes all of it in `choose_command()`.

## Task 1B — MuJoCo wall following over MQTT (65 marks)
- 3-D maze with mass, wheel slip and **noisy sensors**. Enter, follow walls, exit. Two halves:
  **behaviour** (which wall, when to turn) + **PID** (hold the distance to the wall without
  oscillating).
- Topics (QoS 0, not retained):
| Topic | Direction | Payload |
|---|---|---|
| `pacbot/sensors` | sim → you, **~500 Hz** | JSON `fl, fr` (front ToF), `sl, sr` (side ToF), `gyro[3]`, `accel[3]`, `dt` |
| `pacbot/wheel_vel` | you → sim | `left, right` rad/s. **Latest value wins**: it keeps driving until changed |
- Publish one wheel command per sensors message. Use `dt` for the I and D terms; use the gyro to
  make turns land (integrate the yaw rate).
- Portal hint: wandering, oscillating or stalling at corners is usually **the controller**; tune
  one gain at a time.
- 1B videos: expected output `Ac7dU4j0nVs`; 1A expected output `95Kb59pPsXU` (not fetched).

### Task 1B submission + scoring [DOC-SOURCED 2026-09-16]
- Start the screen recording first, with **both terminals readable + the whole MuJoCo maze** in
  shot the entire time. The launcher terminal proves evaluation mode.
- `./task_1b_launch --evaluate` → wait for evaluation mode (the portal text says "Evaluation mode
  enabled"; the portal's example screenshot shows `evaluate: recording data; result will be written
  to result.json`, then `MAZE SOLVED`, then `evaluate: wrote result to result.json`) → `python3
  task_1b.py` → **`result.json`** (1A writes `result.yaml`).
- Zip **`result.json` + `task_1b.py`** (no folder) as **`PB#4817.zip`**, the same zip name as 1A,
  in the 1B slot. Upload an unlisted YouTube video, one unbroken take.
- **Marks = C × max(0, 65 − 10 × collisions)**: C = 1 only if the bot exits. 7+ collisions = 0.
  Stalling = 0. **Collisions are printed live in the launcher terminal**, so use that while tuning.
  Tune for a steady line (hugging the wall scrapes; oscillating clips both sides).
- Portal folder names are `task_1b`; the repo uses `task1b`. Use the real folder.

## Boilerplate facts vs portal text [VERIFIED from the boilerplates 2026-09-17]
- **PB 1A:** the maze is 13×13; `WALLS` bitmask grid (N=1, E=2, S=4, W=8); `EXIT_CELLS` = (0,6,'south'), (12,6,'north');
  `HEADING_DELTA` yaw 0:(0,+1,E) 90:(+1,0,N) 180:(0,−1,W) 270:(−1,0,S). **North = row + 1, so row 0 is the south
  edge.** `choose_command(pacbot_cell, pacbot_yaw, pellets_remaining)` returns FRONT/LEFT/RIGHT/BACK/None. Plumbing:
  `parse_pellets`, `main`, nested `decide_and_send`, `on_message`; client_id "Controller".
- **PB 1B CONTRADICTION:** the portal says `fl, fr` = FRONT ToF and `sl, sr` = SIDE ToF. The boilerplate comments say `fl`/`fr`
  = distance to the left/right SIDE wall and `sl`/`sr` = distance AHEAD left/right of centre. **Unresolved:** verify
  by driving straight and watching which pair shrinks. The first reading at the entry was fl≈0.10, fr≈0.10, sl≈0.26, sr≈0.26.
- The 1B boilerplate docstring says to run `mosquitto` first. The broker is a systemd service here, so a manual
  `mosquitto` fails with "address already in use".
- The 1B boilerplate prints every message (500 Hz), which floods the terminal.

## Setup status [VERIFIED 2026-09-16]
- Repo `~/Desktop/e-yantra/pacbot_ws` pulled (commit `2c1343c` "feat: task1 launch files").
  **`~/pacbot_ws` → symlink** to it, so the portal paths work.
- **The repo differs from the portal text:** folders are **`task1a/`, `task1b/`** (portal says
  `task_1a`, `task_1b`), and the starters are **`task_1a_boilerplate.py` / `task_1b_boilerplate.py`**.
  Claude copied them to **`task1a/task_1a.py`** and **`task1b/task_1b.py`** (the names the
  submission expects) and left the originals untouched.
- `task1b/lib/` ships its own `libmujoco.so.3.11.0`, `libglfw.so.3`, `libmosquitto.so.1` and
  `libsodium.so.23`, plus `meshes/`, so it needs no system MuJoCo.
- Boilerplates import only `json`, `time` and `paho.mqtt.client` (paho 2.1.0 is installed).
- Mosquitto 2.0.11: service **active + enabled at boot**, localhost only.
- **Smoke test passed:**
  - **1A**: the sim published `robot/pose {"row":5,"col":1,"yaw":0.0,"valid":true}`, `pellets/pose
    [[1,10],[7,11]]`, `bot/cmd 1`. Starts live, with a Qt/Wayland warning only (harmless).
  - **1B**: `pacbot/sensors` flowing (fl≈0.10, fr≈0.10, sl≈0.26, sr≈0.26, accel z≈9.81, dt=0.002 →
    500 Hz).
  - Both stopped cleanly on SIGINT. Neither ran with `--evaluate`, and no result files were
    created. The 1A test left retained pose/pellet messages on the broker; they are overwritten
    at the next launch.
- git: `task_1a.py`, `task_1b.py`, `task0/4817_task0.*` are untracked in e-Yantra's repo. **Never
  commit or push to it.**
