# Task 2 — submission runbook (written 2026-10-14 by claude-code)

The code for KD 2B, KD 2C, PB 2A and PB 2B was written and tested in simulation by claude-code while
Saurabh wrote his college assignment (logged in `04-task-log.md`). What is left needs a person:
**a screen recording of the exact run being submitted, the YouTube upload, and Gauri's portal upload.**

Graded files are **never committed to the public team repo.** They live in:
- KD: `~/kd_submissions/task_2b/` and `~/kd_submissions/task_2c/` (plus the working copies in
  `~/pico_ws/src/swift_pico/src/`, which currently hold the **2B** versions)
- PB 2A: `~/pacbot_ws/task2a/task_2a_boilerplate.py`; PB 2B: `~/pacbot_ws/task2b/task_2b_boilerplate.py`

## Before any recording
- Plug the charger in and **unlock the screen** (a locked screen freezes the MuJoCo windows).
- Close other heavy programs: the controllers react to CPU load.
- Recorder: `python3 ~/Desktop/e-yantra/learning/tools/screen_record.py` (whole screen, Ctrl+C stops it).
- One continuous take; terminals + simulator visible. Do a short test recording first.

## PacBot (2A, 2B): one command does it all
```
python3 ~/Desktop/e-yantra/learning/tools/pb_record.py --task 2a      # or --task 2b
```
One window with two terminals. Press Enter in the top pane: screen recording + `--evaluate` launcher start.
Put the sim window on the right half (Super+Right) and this window on the left (Super+Left). 2A: press Enter
in the bottom pane to start the robot; 2B starts by itself (its evaluator ends the run if the robot has not
moved within 60 s). It stops, zips `PB#4817.zip` on camera and saves the video in `~/Videos/Screencasts/`
(plus a sim-only copy). Old `result.json`/zip are moved aside first. The manual steps below do the same by hand.
Rehearsal without recording: add `--no-video` (its result + zip go to `~/pb2a_trials/rehearsal_<time>/`, never the
task folder). Rehearsed 2026-10-14 with the real `--evaluate` launchers: 2A "MAZE SOLVED", 2B "wrote sealed result.json".

**Retry rule (PacBot):** every run draws a new random spawn/pellets, and some draws go badly. When the tool says
"N COLLISION line(s) · do NOT submit this one", just run it again: each run is a separate, complete evaluate
run with its own video, and only the clean one is uploaded (2A scores max(0, 30 − 5 × collisions), so even one
collision costs 5 marks). The previous attempt's `result.json` is moved to `~/pb2a_trials/` automatically.

## PB 2A — maze traversal (soft deadline 15 Oct)
```
cd ~/pacbot_ws/task2a
mosquitto_pub -t pacbot/poses -r -n && mosquitto_pub -t pacbot/pellets -r -n     # clear stale messages
# start the screen recording, then in terminal 1:
./task_2a_launch --evaluate
# wait for "PacBot Task2A started", then in terminal 2:
python3 task_2a_boilerplate.py
# do not touch anything until MAZE SOLVED; stop the recording
zip "PB#4817.zip" result.json task_2a_boilerplate.py
```
Never open or edit `result.json`. Upload `PB#4817.zip` (PB Task 2A slot) + the Unlisted YouTube link.
If a practice run looks shaky, run plain `./task_2a_launch` (practice) first: nothing is written.

## PB 2B — pellets + ghost (soft deadline 26 Oct)
```
cd ~/pacbot_ws/task2b
for t in pacbot/poses pacbot/pellets pacbot/pellet pacbot/ghost pacbot/result; do mosquitto_pub -t $t -r -n; done
# start the screen recording, then in terminal 1:
./task_2b_launch --evaluate
# in terminal 2:
python3 task_2b_boilerplate.py
# do not touch anything until RUN COMPLETE; stop the recording
zip "PB#4817.zip" result.json task_2b_boilerplate.py
```
What you will see: the robot **stands still for 12–18 s first**. It is watching the ghost's lap, and the clock only
starts when it moves, so this costs nothing. Short waits near the ghost, or a log line "detour round the ghost",
are normal. A run takes ~2.5–4 min. Never open or edit `result.json`. Same zip name as 2A, but in the `task2b` folder.
Sim results 2026-10-14: see `04-task-log.md` (PB 2B row).

## KD (2B, 2C): one command does it all
```
~/Desktop/e-yantra/learning/tools/kd_record.sh 2b      # or 2c
```
Press Enter: screen recording starts, then the sim. Put the sim on the right half (Super+Right), the terminal on
the left (Super+Left), press Enter: service → client → bag → server start in the runbook order, every node's
output shown with a `[name]` prefix. It stops when the client reports all waypoints reached, prints a practice
score from the bag (`kd2_bag_score.py`), and builds `~/kd_upload_2b/KD_4817_task_2b.zip` (renamed scripts + bag).
It swaps in the right `waypoint_service` and rebuilds if needed. Rehearsals 2026-10-14 (`--no-video`):
2B 39.4/40 (4th hold done 44.5 s), 2C 40/40 (35.3 s). The manual steps below do the same by hand.

## KD 2B — waypoint navigation (soft deadline 19 Oct)
```
cd ~/pico_ws && colcon build && source install/setup.bash     # the 2B scripts are the installed ones
# start the screen recording, then each in its own terminal (source install/setup.bash in each):
ros2 launch swift_pico swift_pico_simulation.launch.py
ros2 run swift_pico waypoint_service
ros2 run swift_pico pico_client
cd ~/pico_ws && ros2 bag record -o task_2b /whycode_node/markers /controller_heartbeat   # BEFORE the server
ros2 run swift_pico pico_server
# when the client logs "All waypoints have been reached successfully": Ctrl+C the bag, stop recording
mkdir -p ~/kd_upload_2b && cd ~/kd_upload_2b
cp ~/kd_submissions/task_2b/waypoint_service.py KD_4817_waypoint_service.py
cp ~/kd_submissions/task_2b/pico_client.py      KD_4817_pico_client.py
cp ~/kd_submissions/task_2b/pico_server.py      KD_4817_pico_server.py
cp ~/pico_ws/task_2b/task_2b_0.db3 ~/pico_ws/task_2b/metadata.yaml .
zip KD_4817_task_2b.zip KD_4817_waypoint_service.py KD_4817_pico_client.py KD_4817_pico_server.py task_2b_0.db3 metadata.yaml
```
YouTube title `KD_4817_Task_2b`, Unlisted. Sim results: 5/5 flights held all four waypoints; 4th hold done 32–47 s.

## KD 2C — camera-driven waypoints (soft deadline 26 Oct)
The 2C scripts are in `~/kd_submissions/task_2c/` (its `waypoint_service.py` reads the camera; client and server
are the same as 2B's). Copy all three into the workspace and rebuild (the 2B copies stay safe in
`~/kd_submissions/task_2b/`; to go back to 2B, copy those three the same way):
```
for f in waypoint_service pico_client pico_server; do cp ~/kd_submissions/task_2c/$f.py ~/pico_ws/src/swift_pico/src/$f.py; done
cd ~/pico_ws && colcon build && source install/setup.bash
```
Then the same run order as 2B, with the bag named `task_2c`:
`ros2 bag record -o task_2c /whycode_node/markers /controller_heartbeat`. Zip as
`KD_4817_task_2c.zip` with the three scripts from `~/kd_submissions/task_2c/` (renamed `KD_4817_...`)
plus `task_2c_0.db3` and `metadata.yaml`. Sim result: all 4 critical survivors held, 4th hold done at 31 s (full marks needs ≤ 60 s).
**Check before recording:** `git -C ~/pico_ws/src fetch` — the portal mentions a
`grid_whycode_coordinates.csv` that is not in the repo yet; the service reads it if it appears and
otherwise uses the JSON that ships today. If the repo changes: `git stash`, `git pull`, `git stash pop`.

## Author list
Every file's header says `Author List: Saurabh Tomke`. The code was written by claude-code at
Saurabh's request; how to describe that to e-Yantra is Saurabh's decision.
