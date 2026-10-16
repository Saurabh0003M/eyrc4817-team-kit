# 10 — Task 2 (both themes): what is asked, what to learn, how to submit

Task 2 ran from 6 to 26 October 2026. Source: the portal pages, read 2026-10-13 (full notes in
`B4_Background_Task2.md`). Code status and who wrote it: the table below. **This file holds no solution:**
the team's graded code lives on Gauri's laptop only, never in a public place.

## The five subtasks

| Subtask | What it asks | Marks | Soft deadline | Our score (portal, 17 Oct) |
|---|---|---|---|---|
| **KD 2A** | Your own position controller (PID or LQR): hold the drone at (1.5, −1.5, 13) | 20 | 12 Oct | **20**: uploaded late on 16 Oct (the forum had said "closed"); accepted |
| **KD 2B** | ROS 2 **service** gives 4 waypoints; ROS 2 **action** flies to each in order and holds 3 s | 40 | 19 Oct | **40** (all 4 held, finished 37 s) |
| **KD 2C** | Same, but the waypoints come from the **camera**: detect the 4 critical survivors, plan a route from F6 | 40 | 26 Oct | **40** (finished 41 s) |
| **PB 2A** | Real robot physics: random spawn, collect one pellet, leave by the exit, no wall touches | 30 | 15 Oct | **30** (0 collisions, 205 s) |
| **PB 2B** | Fixed spawn, 3 random pellets, a ghost patrols near one of them, time counts | 70 | 26 Oct | **63.60** (3/3, 0 collisions, 75.28 s) |

**Totals: Khoj-o-Drone 100/100, PacBot 93.60/100.** PB 2B is scored 5 × pellets + (55 − 0.085 × seconds) − 1.5 ×
collisions, so 70 would need a 0-second run; the portal's numbers matched this formula exactly.

"Soft" deadline = last day for e-Ratna. Late submissions are still marked until an unpublished hard deadline.
The code for these was written by Claude at Saurabh's request (logged in the team's task log), so every
teammate should be able to explain it: ask this project to quiz you, using `11_Task2_How_It_Works_PRIVATE.md`.

## What each subtask teaches (learn these, in this order)

**KD 2A → 2B → 2C build on each other.**
1. **Position PID on three axes** (2A): the same P, I, D as Task 1, but now you write the loop yourself.
   New ideas: *integral windup* (the I term keeps growing during a long flight and overshoots on arrival)
   and *output limits* (cap how hard the drone may tilt).
2. **ROS 2 service vs action** (2B): a service is one request → one reply. An action is a long job with a
   goal, a stream of feedback while it runs, and a result at the end. Learn to define `.srv` and `.action`
   files in a package, and to call them from Python.
3. **Executors and callback groups** (2B): if one callback runs a long loop, other callbacks (like the
   position updates) must still run. Look up `MultiThreadedExecutor` and `ReentrantCallbackGroup`.
4. **Latched topics and QoS** (2C): a topic published once, with *transient local* durability, still
   reaches a subscriber that joins later. A normal subscription can miss it completely.
5. **Perception → planning** (2C): reuse Task 1A's detector, turn grid names into coordinates, and choose
   the visiting order (with 4 stops, trying every order is cheap).

**PacBot 2A → 2B.**
1. **Dead reckoning** (2A): no position is given. Heading from the gyro, distance from the wheel
   encoders, and both drift. Measure how much (drive a known distance, compare).
2. **Map-based correction** (2A): the maze is known, so you can predict what each distance sensor should
   read and correct your position estimate when it reads something else. Learn why you must ignore
   readings that look past the end of a wall.
3. **Planning with turn costs** (2B): turning is slow, so "fewest cells" is not "fastest". Search over
   (cell, heading) states, for example with Dijkstra. Try every pellet order (3 pellets = 6 orders).
4. **Moving obstacles** (2B): the ghost repeats a fixed circuit. Watch one lap before moving (the clock
   starts only at your first movement), then predict where it will be and only enter its area when
   you can get through.
5. **Measure before tuning**: log how long each action really takes before trusting any timing model.
   This is how PB 2B went from 151 s to 75 s: two-thirds of the time was pivots and starts/stops (most runs
   are one cell long), not driving. The fix was removing the slow *tails* at the end of each pivot and each run.
6. **Know where the limit is**: faster pivots looked fine for 9 runs, then one fast U-turn made the wheels slip,
   the position estimate never recovered, and the robot got stuck (that run would score 0). A 26-run stress
   test, not 4 runs, is what told us which settings were safe.

## Traps found so far

- KD: **rebuild after every edit** (`colcon build`, then source again); `ros2 run` runs the built copy.
- KD: start the **bag before the server**; a bag started late scores 0.
- KD: hard-code the final gains in the submitted file; there is no GUI during evaluation.
- KD: WhyCode z grows as the drone goes **down**, so throttle works the opposite way to x and y.
- PB: the topics `pacbot/poses` and `pacbot/pellets` are **retained**. A stale message from an earlier
  run confuses the next one: clear them with `mosquitto_pub -t <topic> -r -n`.
- PB 2B: headings run **counter-clockwise** (`(h + 1) % 4` is a left turn), the opposite of Task 1B.
- PB 2B: the evaluator ends the run if the robot has not moved within 60 s.
- PB: never open or modify the `task_2a_launch` / `task_2b_launch` programs, and never rename the
  boilerplate's functions.
- MuJoCo windows freeze while the screen is locked; keep the screen unlocked while recording.
- **Test the recorder the way it will really run.** `ros2 bag record` reads the keyboard; started as a
  background job from a real terminal it was frozen by the shell (no bag at all). All the rehearsals had
  run without a terminal, so only the first real recording showed it. Fixed in `kd_record.sh` (16 Oct).
- PB 2B: when the ghost guards the way to the exit, the robot may find no safe gap and take a long detour
  (~1 run in 10, ~40 s lost). Not a bug; record again and keep the fastest clean run.
- PacBot: every zip is `PB#4817.zip`. A 2A zip uploaded in the 2B slot scores 0: upload from the right folder.
- A "closed" answer on the forum was not final: the late KD 2A upload was accepted. If a late upload costs
  little, try it.

## How to record and submit (one command each)

Run on Gauri's laptop from a normal terminal (Ctrl+Alt+T), with the screen unlocked, the charger in and other apps closed:

| Subtask | Command | What you get |
|---|---|---|
| PB 2A / 2B | `python3 ~/Desktop/e-yantra/learning/tools/pb_record.py --task 2a` (or `2b`) | video + `PB#4817.zip` in `~/pacbot_ws/task2a/` (or `task2b/`) |
| KD 2A / 2B / 2C | `~/Desktop/e-yantra/learning/tools/kd_record.sh 2a` (or `2b`, `2c`) | video + `~/kd_upload_2a/KD_4817_task_2a.zip` (or `2b`, `2c`) |

Then: check the zip with `python3 ~/Desktop/e-yantra/learning/tools/submission_check.py <pb2a|pb2b|kd2b|kd2c> --zip <zip>`,
upload the video to YouTube as **Unlisted** (title `KD_4817_Task_2b` style for KD), and Gauri uploads the
zip + link in that subtask's slot. Step-by-step manual version: `B4_Background_Task2.md` (runbook section).
