# Task 1B — tune the altitude PID (Swift Pico, Z axis)

Source: KD portal → Task 1 → Task 1B Instruction and Submission, pasted by Saurabh on 2026-09-16.
The three ball-and-beam screenshots are **e-Yantra's own demo** from that page; they are not
Saurabh's runs. **The portal is the authority.** Deadline: unknown.

## What the task really is [VERIFIED 2026-09-16]
**You do not write PID code in 1B.** `task_1b_controller` is a **pre-compiled binary** (ELF) that
e-Yantra supplies, as are `task_1c_controller` and `mujoco_bridge`. The job is to **tune three
numbers**, Kp, Ki and Kd, for the throttle (Z) axis, then record proof.
- Controller I/O: subscribes `/whycode_node/markers` (position from the camera) and `/throttle_pid`
  (`controller_msg/PIDTune`: `kp ki kd`); publishes `/drone_command` and `/pos_error`
  (`error_msg/Error`: `roll_error pitch_error throttle_error yaw_error`).
- On start it prints "Would you like to tune the PID gains now? (Y/N)". Y means use the GUI; N
  means "enter the gains manually" (it prompts for Kp, Ki, Kd). It **arms immediately**.
- **Target [DOC]:** `throttle_error` within **±0.4** within **5 s**, then held for **10 s**.
- GUI: `ros2 launch pid_tune pid_tune_drone.launch.py`. Use the **Throttle card only**. The value
  sent is **integer × multiplier**; judge by the "= computed value". Changes apply instantly.
  **Save Values** writes `pid_values.yaml`.
  **Resolved from the GUI source:** Save Values writes `~/pico_ws/src/swift_pico/src/pid_values.yaml`.
  The repo's `controller_tuner/pid_tune/scripts/pid_values.yaml` is unused. Default multipliers are
  Kp×0.03, Ki×0.008, Kd×0.6. The GUI has a built-in live `/pos_error` graph. **It sends gains only on
  −/+ or Enter**; see the trap in `11-task1c.md`.
- Portal method: all gains 0 → raise Kp until it holds but oscillates → back off a little → add Kd
  to damp → add a small Ki to remove the leftover offset. **If the WhyCode marker leaves the
  camera view, there is no feedback and gains appear to do nothing.**
- Portal video: https://youtu.be/ef2SI6uARuA

## Setup status on the Ubuntu box [VERIFIED 2026-09-16]
- `~/pico_ws`: `git pull` says already up to date. The 16 Sep "Task1 Release" clone already
  contains 1B/1C. Built.
- **Blocker 1 — `libmujoco.so.3.9.0` not found.** e-Yantra's `mujoco_bridge` has a hard-coded
  RUNPATH of `/home/joe/.local/lib/python3.10/site-packages/mujoco`, the developer's machine.
  **FIXED:** `~/.bashrc` now prepends the KD venv's MuJoCo dir
  (`~/drone_ws/task0/drone_env/lib/python3.10/site-packages/mujoco`, which contains
  `libmujoco.so.3.9.0`) to `LD_LIBRARY_PATH`. The comment block is marked "Added by Claude
  2026-09-16". PacBot's Python MuJoCo is still 3.11.0, verified. The NEON "ROS 2" terminal profile
  sources `~/.bashrc`, so it is covered too. Backup of the old `.bashrc` in the session
  scratchpad only.
- **Blocker 2 — `libglfw.so.3` not found. FIXED 2026-09-16:** Saurabh ran `sudo apt install -y libglfw3-dev`
  (libglfw3 3.3.6-1). `ldd mujoco_bridge` in a fresh login shell now shows **no missing libraries**.
- **Full smoke test PASSED 2026-09-16 (real GLFW, no temporary copies):** sim + `task_1b_controller` (answered Y;
  it printed "Ready to fly!") + tuner GUI (`drone_pid_tuner`, button UI) all started with no errors in any log.
  Also present: `zip`; tuner imports (tkinter, yaml, matplotlib 3.5.1); rosbag2 sqlite3 storage plugin; GNOME
  Shell 42.9 for screen recording. Not yet observed: live `/pos_error` values and the gains-only-on-click trap.
  Check both in the first tuning session.
- **Earlier trial launch succeeded** with a temporary GLFW copy: nodes `mujoco_swift_pico`,
  `whycode_node`, `rotors/roll_pitch_yawrate_thrust_controller`, `rotors/rotors_swift_interface`,
  `whycode_display/image_view`. `/whycode_node/markers` runs at **30 Hz** with the marker found
  (id 2, z ≈ 15.0 in camera coordinates), and there were no errors. Camera is 1280×1280, fx=fy=1108.77.
  `/pos_error` only appears once the controller runs.
- The trial caused an Ubuntu "internal error" popup: `timeout` sent SIGTERM to `ros2 topic hz`,
  whose Python traceback was caught by apport (`/var/crash/_opt_ros_humble_bin_ros2.1000.crash`).
  Harmless. **Stop ROS CLI tools with SIGINT (`timeout -s INT`)**, never SIGTERM.

## Submission [DOC-SOURCED]
1. Note the three computed gains (Save Values → `pid_values.yaml`).
2. Launch the sim → `ros2 run swift_pico task_1b_controller` → type the gains.
3. `ros2 bag record -o task_1b /pos_error /whycode_node/markers` for **≥ 60 s**.
4. From **inside** `task_1b/`: `zip -r KD_4817_task_1b.zip task_1b_0.db3 metadata.yaml` (the
   two files, **no folder**).
5. **Gauri uploads** it (Team Leader only).
6. **YouTube:** one continuous screen recording in which the **terminal is visible before the sim
   launches** and throughout; the GUI is not needed. Upload **Unlisted**, titled
   **`KD_4817_Task_1b`**, and submit the link. Example video: https://youtu.be/xqOyre-afOE
   - *[INFERRED, verify with a test recording]* Ubuntu here runs a **Wayland** session. Kazam and
     SimpleScreenRecorder are X11 recorders and typically capture black or partial screens on
     Wayland. Use GNOME's built-in recorder (Print Screen → video) or OBS, or log in with "Ubuntu on
     Xorg". **Do a 2-minute test recording first**, in case of time limits.

## Scoring [DOC-SOURCED] — 40 marks
| Part | Marks | Rule |
|---|---|---|
| Hovering | 16 | per second inside the target box, up to 10 s |
| Finishing bonus | 8 | only for the full 10 s (9 s earns 0) |
| Speed | 16 | full if finished within 15 s, falling to 0 at 60 s |

*Open question:* when does the clock start: bag start, controller start, or first message? The
portal order is sim → controller (which arms at once) → record. Ask on the forum before the final
run.

## Learning angle
This is pure **tuning skill**: exactly roadmap M3's P/PD/PID feel, then M6. Claude handles
bring-up, plots of `throttle_error`, recording and zipping, and a **self-scorer** that reads a
practice bag and applies the scoring table above. **Saurabh chooses every gain.** Do not auto-tune
for him. The roadmap M6 text ("you write the PID terms") is outdated; update it in the next
roadmap rebuild, after the rest of the Task 1 material (KD 1C + PacBot) arrives.
