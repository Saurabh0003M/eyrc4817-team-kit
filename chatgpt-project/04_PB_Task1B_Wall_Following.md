# 04 — PacBot Task 1B: Wall following with PID in MuJoCo (65 marks)

Source: e-Yantra portal, PB → Stage 1 → Task 1 → Task 1B Overview/Instructions/Submission, plus the boilerplate in e-Yantra's repo. The portal is the final authority.

## In one sentence

Write Python that reads the robot's distance sensors and sets its **two wheel speeds**, so it **follows the maze walls from the entry to the exit without touching them**.

## Why it's harder than 1A

It's a 3D physics simulation: the robot has mass, wheels can slip, and **sensors are noisy**. You don't get cell coordinates, only what the robot senses. Two halves to write:

1. **Behaviour:** which wall to follow, when a turn is needed, when you're out.
2. **Controller (PID):** hold a steady distance from the wall. Without it the robot zig-zags, scrapes one side, then over-corrects into the other.

## Two programs, one broker

| Program | Role |
|---|---|
| `task_1b_launch` (e-Yantra, **encrypted: never open or modify it**) | MuJoCo maze + robot, publishes sensors, applies wheel speeds, counts collisions, scores |
| `task_1b.py` (yours, copy of `task_1b_boilerplate.py`) | Reads sensors, publishes wheel speeds |
| `mosquitto` on `localhost:1883` | Passes the messages |

## Topics (QoS 0, not retained)

| Topic | Direction | Payload |
|---|---|---|
| `pacbot/sensors` | sim → you, **~500 times per second** | JSON: `fl`, `fr`, `sl`, `sr` (4 Time-of-Flight distance sensors, metres), `gyro` [3] (turn rates, rad/s; `gyro[2]` = turning about the vertical axis), `accel` [3], `dt` (seconds since the last step, 0.002) |
| `pacbot/wheel_vel` | you → sim | JSON `{"left": …, "right": …}` wheel speeds in **rad/s**. **Latest value wins**: the robot keeps going at the last speeds until you send new ones. It does not stop on its own |

Publish **one wheel command for every sensors message** (the boilerplate already does this inside `on_message`).

## ⚠ Contradiction: which sensor is which? Verify before coding

| Source | `fl`, `fr` | `sl`, `sr` |
|---|---|---|
| Portal instructions | **front**-left / **front**-right distance | **side**-left / **side**-right distance |
| Boilerplate comments | distance to the left / right **side** wall | distance **ahead**, left / right of centre |

They say opposite things. **Find out by experiment:** set a small equal forward speed on both wheels, watch the printed values, and see which pair shrinks as the robot approaches the wall ahead. The first readings in our setup test (robot parked at the entry) were `fl ≈ 0.10, fr ≈ 0.10, sl ≈ 0.26, sr ≈ 0.26`.

## Boilerplate (`~/pacbot_ws/task1b/task_1b_boilerplate.py`)

- `on_message(client, userdata, msg)` parses the sensor JSON, prints the values, and publishes `left_vel` / `right_vel`, currently `0.0` (look for the `TODO`). **Write your logic in the marked section.**
- `_mqtt_client()` and `main()` are plumbing. **Don't rename or restructure the functions.**
- The printing at 500 Hz floods the terminal and can slow things down; print less often while tuning.
- Its docstring says to run `mosquitto` first. Our broker already runs as a service, so **don't start it again** (you'd get "address already in use").

## Suggested approach (concepts, not code)

1. **Driving:** equal wheel speeds = straight; left slower than right = curve left; opposite speeds = spin on the spot.
2. **Error** for wall following = desired side distance − measured side distance.
3. **P** first: steering correction = Kp × error, applied as (base speed − correction, base speed + correction). Watch the wobble.
4. Add **D** (uses the change in error per `dt`) to calm the wobble; a small **I** only if it settles off the target line.
5. **Corners:** the front sensors see a wall close ahead → stop following and **turn using the gyro**: add up `gyro[2] × dt` until about 90° (π/2 rad), then resume following. Don't use a timer for turns; wheels slip.
6. **Dead ends and openings:** decide a rule (e.g. always keep the right wall; if no wall on the right, turn right). A consistent rule gets you through a maze.
7. **Exit:** no walls in range on any side = out of the maze (the portal's example run printed "No walls in range on any side - clear of the maze").
8. **Tune one gain at a time**, and count collisions after each change.

## Running

```bash
cd ~/pacbot_ws/task1b && ./task_1b_launch          # terminal 1 (start first; the robot waits at the entry)
cd ~/pacbot_ws/task1b && python3 task_1b.py        # terminal 2
```

- The simulator must be running before your code, or you'll miss the first readings.
- Nothing moves: simulator not started first · `systemctl status mosquitto` · topic name typo.
- Wandering, zig-zagging or stalling at corners is **usually the controller (gains)**, not the wall logic.
- Stop both with **Ctrl+C**.

## Submission

1. Coding Standard comments in `task_1b.py` (see `05_Setup_Run_Submit.md`). Don't rename functions.
2. **Start the screen recording first**: both terminals readable + the **whole maze** visible, one unbroken take. The launcher terminal proves evaluation mode, so it must be in shot from the start.
3. Terminal 1: `cd ~/pacbot_ws/task1b && ./task_1b_launch --evaluate`. Wait for the evaluation message (the portal example shows `evaluate: recording data; result will be written to result.json`).
4. Terminal 2: `cd ~/pacbot_ws/task1b && python3 task_1b.py`. Don't touch anything until it finishes (`MAZE SOLVED`, then `evaluate: wrote result to result.json`).
5. Zip the **two files**: `zip 'PB#4817.zip' result.json task_1b.py`
6. **Gauri uploads** in the Task 1B slot. YouTube **Unlisted**, link on the portal.

## Scoring (65 marks)

**Marks = C × max(0, 65 − 10 × collisions)**, where C = 1 only if the robot exits the maze.

- Clean run = 65. Each wall touch = −10. 7 or more collisions = 0.
- Doesn't exit (stuck, stalled, stopped) = **0**, however clean.
- **Collisions are printed live in the launcher terminal.** Use that count while tuning.
- Hugging the wall scrapes it; oscillating clips both sides. Tune for a steady line.

## Learning path (about 1–2 days)

1. Portal *Introduction to Control Systems* (open vs closed loop) → *PID Controller* page ("P, PD & PID for Drones" + ball-and-beam demo).
2. *PID Control — A brief introduction* (8 min) → *What Is PID Control?* (MATLAB Part 1) → *A PID Tuning Guide* (Part 4).
3. Portal *MuJoCo* overview (model vs state); portal *MQTT* pages.
4. Known portal mistake: the PID page's integral formula `Iterm = (Iterm + error) · Ki` is wrong; use `Iterm = Iterm + Ki · error` (scaled by `dt`).

Links: `07_Learning_Resources.md`. Checker: `python3 learning/tools/submission_check.py pb1b --file ~/pacbot_ws/task1b/task_1b.py`.
