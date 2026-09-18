# 03 — PacBot Task 1A: Maze path planning over MQTT (35 marks)

Source: e-Yantra portal, PB → Stage 1 → Task 1 → Task 1A Overview/Instructions/Submission, plus the boilerplate file in e-Yantra's repo. The portal is the final authority.

## In one sentence

Write the function **`choose_command()`** so the bot **eats both pellets and walks out an exit**, sending **one move at a time** over MQTT, without driving into walls.

## The game

- A 2D grid maze. **2 pellets appear on random reachable cells every run**, so you can't hard-code a route.
- The bot has a **position (cell)** and a **heading (which way it faces)**. It can only move **forward**.
- To go a different way: **turn first, then move**. One step of your route is often **two commands**. Getting this wrong is the #1 failure.
- The run ends when the bot walks out through one of the **2 exits** (win banner; no more commands accepted).
- The simulator never plans anything. It only checks and applies your one command.

## Two programs, one broker

| Program | Role |
|---|---|
| `task_1a_launch` (e-Yantra, **encrypted: never open or modify it**) | Draws the maze, owns the real position/heading, checks each command against walls, keeps the score |
| `task_1a.py` (yours, copy of `task_1a_boilerplate.py`) | Receives the state, decides **one** command, publishes it |
| `mosquitto` broker on `localhost:1883` | Passes every message between them |

**The loop:** simulator publishes pose + pellets → your code sends ONE command → simulator applies it (if legal) → publishes the new pose → repeat. **Never send two commands before the reply** (you'd be racing the simulator).

## Topics

| Topic | Direction | Payload | Retained? |
|---|---|---|---|
| `robot/pose` | sim → you | JSON `{"row": 3, "col": 7, "yaw": 90.0, "valid": true}` | yes |
| `pellets/pose` | sim → you | JSON list `[[3, 7], [9, 2]]`, empty `[]` when all eaten. **Source of truth: don't keep your own count** | yes |
| `bot/cmd` | sim → you | **plain string** `"0"` paused / `"1"` running | yes |
| `robot/cmd_vel` | you → sim | **plain string** `FRONT`, `LEFT`, `RIGHT` or `BACK` | no |

- `yaw`: **0 = East, 90 = North, 180 = West, 270 = South**. It's the real heading and decides where `FRONT` goes. Track it.
- `valid: false` (position unchanged) = command refused: wall, off-grid (not through an exit), unknown string, or paused.
- `FRONT` = one cell forward. `LEFT` / `RIGHT` = turn 90° on the spot. `BACK` = turn 180° on the spot. **Turns never fail; only FRONT can.**
- "Retained" = the broker keeps the last message, so your code gets the current state the moment it connects.

## What the boilerplate gives you (read `~/pacbot_ws/task1a/task_1a_boilerplate.py`)

- Maze size **13 × 13** (`MAZE_ROWS`, `MAZE_COLS`).
- **`WALLS`**: a 13 × 13 table. Each number is a **bitmask** (walls added together): `WALL_N = 1`, `WALL_E = 2`, `WALL_S = 4`, `WALL_W = 8`. Example: `12 = 8 + 4` → walls on the West and South sides of that cell. Check a wall with `cell_value & WALL_N`.
- **`EXIT_CELLS`**: `(0, 6, 'south')` and `(12, 6, 'north')`: row, column, and the direction to walk out.
- **`HEADING_DELTA`**: for each yaw, the row/column change of one FRONT step and the wall bit to check: `0: (0, +1, E)`, `90: (+1, 0, N)`, `180: (0, −1, W)`, `270: (−1, 0, S)`.
  ⚠ **North means row + 1** in this table, so row 0 is the **south** edge. Draw the maze on paper with this convention before coding.
- **`choose_command(pacbot_cell, pacbot_yaw, pellets_remaining)`** returns `"FRONT"`, `"LEFT"`, `"RIGHT"`, `"BACK"` or `None`. `pacbot_cell` = `(row, col)`, `pellets_remaining` = set of `(row, col)`. **This is the only function you write.**
- The rest (MQTT connection, `on_message`, `decide_and_send`, `parse_pellets`, `main`) is plumbing. **Don't rename or restructure it**: the evaluator looks for those names.

## Suggested approach (concepts, not code)

1. **Graph:** each cell is a node; two neighbour cells are connected if neither side has a wall between them.
2. **Search:** **BFS** (breadth-first search) gives the fewest-steps path on this grid. A\* also works.
3. **Plan the order:** from start → pellet → pellet → exit. Try both pellet orders and both exits; pick the shortest total.
4. **Turn logic:** compare the direction to the next cell with the current yaw: same → `FRONT`; 180° off → `BACK`; otherwise `LEFT` or `RIGHT`. **Find out by experiment** whether `LEFT` adds +90 or −90 to yaw (drive by hand below).
5. **Leaving:** at an exit cell, face the exit direction, then `FRONT`.
6. Replan from the pose you receive each time (robust if something unexpected happens).

## Try it by hand first (no code)

```bash
cd ~/pacbot_ws/task1a && ./task_1a_launch                                           # terminal 1
mosquitto_sub -h localhost -t 'robot/pose' -t 'pellets/pose' -t 'bot/cmd' -v        # terminal 2: watch
mosquitto_pub -h localhost -t robot/cmd_vel -m LEFT                                 # terminal 3: drive
mosquitto_pub -h localhost -t robot/cmd_vel -m FRONT
```

Notice: how yaw changes after LEFT; what `valid: false` looks like when you drive into a wall; how `pellets/pose` changes when you eat one.

## Running your code

```bash
cd ~/pacbot_ws/task1a && ./task_1a_launch          # terminal 1 (start first; it starts live, not paused)
cd ~/pacbot_ws/task1a && python3 task_1a.py        # terminal 2
```

- Space bar / button = pause/resume. There is no reset: restart both for new pellets.
- **Stop with Ctrl+C**. Both programs use fixed MQTT client IDs, and a hard kill can leave a stale session that breaks the next run.
- The broker already runs as a service. **Don't run `mosquitto` manually** (the boilerplate comment suggests it): it will fail with "address already in use". Check it with `systemctl status mosquitto`.
- Nothing moves? (1) simulator not started first, (2) broker not running, (3) topic name typo.
- Bot stalls? Look at `valid` in the pose: repeated `false` = you sent FRONT facing the wrong way. The bug is in the turn logic, not the search.

## Submission

1. Add the **e-Yantra Coding Standard** comments to `task_1a.py` (see `05_Setup_Run_Submit.md`). Don't rename functions.
2. **Start the screen recording first**: Maze window + terminal both fully visible, the whole run, one unbroken take.
3. Terminal 1: `cd ~/pacbot_ws/task1a && ./task_1a_launch --evaluate`. Wait for "Evaluation mode enabled".
4. Terminal 2: `cd ~/pacbot_ws/task1a && python3 task_1a.py`. Don't touch anything until it stops.
5. The evaluator writes **`result.yaml`** in the folder.
6. Zip the **two files** (not the folder): `zip 'PB#4817.zip' result.yaml task_1a.py`
7. **Gauri uploads** `PB#4817.zip` in the Task 1A slot. Upload the video to YouTube as **Unlisted** (not Private) and submit the link. Keep it up until results are out.

## Scoring (35 marks)

**Marks = pellets × 10 + exit × 15.** 0 pellets and no exit = FAILED (0). Exit only = 15. 1 pellet = 10 (25 with exit). 2 pellets = 20 (**35 with exit**).

## Learning path (about 1 day)

1. Portal *Path Planning* page (BFS, DFS, Dijkstra, Greedy, A\* with animations): the key idea is **which cell to explore next**.
2. *Dijkstra's Algorithm — Computerphile* (10 min) → *A\* Search — Computerphile* (14 min).
3. Portal *MQTT* → *MQTT Concepts* (topics, retained messages).
4. Practise BFS in plain Python on a tiny hand-made grid before the real maze.

Links: `07_Learning_Resources.md`. Checker: `python3 learning/tools/submission_check.py pb1a --file ~/pacbot_ws/task1a/task_1a.py`.
