# 02 — Khoj-o-Drone Task 1B (40 marks) + Task 1C (40 marks): PID tuning

Source: e-Yantra portal, KD → Stage 1 → Task 1 → Task 1B/1C Instruction + Submission. The portal is the final authority.

## In one sentence

**No coding.** e-Yantra gives a ready-made controller program. You choose the **PID gains** (Kp, Ki, Kd) so the simulated Swift Pico drone holds still: **1B = height only**, **1C = height + forward/back + left/right**.

## The pieces (three programs at once, each in its own terminal)

| Terminal | Command | What it is |
|---|---|---|
| 1 | `ros2 launch swift_pico swift_pico_simulation.launch.py` | MuJoCo physics simulator + a top-down camera that tracks the WhyCode marker on the drone (that gives the drone's position) |
| 2 | `ros2 run swift_pico task_1b_controller` (1C: `task_1c_controller`) | The PID controller you're tuning. It **arms (starts the motors) immediately**. It asks "Would you like to tune the PID gains now? (Y/N)": **Y** = use the tuner GUI; **N** = type gains by hand |
| 3 | `ros2 launch pid_tune pid_tune_drone.launch.py` | Tuner GUI with 3 cards: Throttle, Pitch, Roll. Each has Kp, Ki, Kd rows and a live error graph |

Order for tuning and KD 1B recording: terminal 1 → 2 → 3. Order in the portal's **1C submission** steps: sim → **tuner** → controller.

If the launch file errors out: `sudo apt install -y libglfw3-dev` (our setup script already does this).

## Axes and topics

| Axis | Movement | Tuner card / topic | Error to watch (on `/pos_error`) | Task |
|---|---|---|---|---|
| Z | up/down (**throttle**) | Throttle → `/throttle_pid` | `throttle_error` | 1B (and keep it working in 1C) |
| X | forward/back (**pitch**) | Pitch → `/pitch_pid` | `pitch_error` | 1C |
| Y | left/right (**roll**) | Roll → `/roll_pid` | `roll_error` | 1C |

Messages: gains are `controller_msg/PIDTune` (kp, ki, kd); errors are `error_msg/Error` (roll_error, pitch_error, throttle_error, yaw_error). The controller reads the drone position from `/whycode_node/markers` and sends `/drone_command`.

## Target

- **1B:** `throttle_error` inside **±0.4** within **5 seconds**, then stays inside for **10 seconds** straight.
- **1C:** throttle, pitch **and** roll errors **all** inside ±0.4 within 5 s, and held together for 10 s.

## Tuner facts (read from the tuner's source code)

- Each row has −/+ buttons and a number. **The value sent = number × scale**. Default scales: **Kp × 0.03, Ki × 0.008, Kd × 0.6**. Judge by the "= computed value" label, not the raw number.
- **Gains are sent only when you press −/+ or Enter.** Launching the tuner does *not* send the saved values by itself. After (re)starting the controller, press Enter in each row, or answer **N** at the controller and type the gains.
- **Save Values** writes the computed gains to `~/pico_ws/src/swift_pico/src/pid_values.yaml`, which the tuner reloads next time. (Another `pid_values.yaml` inside `controller_tuner/` is not used.)
- If gains seem to do nothing: the drone's marker may be **out of the camera's view**. No marker = no feedback.

## How to tune (portal method, one axis at a time)

1. All gains 0. Confirm the drone behaves predictably.
2. Raise **Kp** until the drone holds position but starts to **oscillate** (swing back and forth).
3. Lower Kp a little, then add **Kd** to **damp** (calm) the oscillation.
4. Add a **small Ki** to remove the leftover offset (the drone settling slightly off target).
5. Watch the error graph the whole time. Change **one number at a time** and write down what happened.

**What each gain does (feel):** Kp = how hard it pushes toward the target (too big → overshoot and swinging). Kd = brakes when it's moving fast toward the target (too big → jittery). Ki = slowly adds push if it stays off target (too big → slow big swings, "windup").

**1C specifics:**
- Keep the 1B throttle gains; confirm height hold first.
- **Pitch and roll are symmetric on this drone: tune them together with the same values.**
- Tilting to move sideways steals some upward thrust, so throttle may need a small touch-up.
- Why x/y is harder: the drone can't push sideways. It must **tilt**, and the tilt splits thrust into up + sideways. Sideways acceleration ≈ g × tilt angle (radians).

## Submission — KD 1B

1. Tune, press **Save Values**, open `pid_values.yaml` and note the three throttle numbers.
2. **Start the screen recording** (terminal visible before you launch anything, for the whole run).
3. Launch the sim. In a second terminal: `ros2 run swift_pico task_1b_controller`, answer the prompt, type your gains.
4. Third terminal, record **at least 60 seconds**: `ros2 bag record -o task_1b /pos_error /whycode_node/markers`
5. From **inside** the `task_1b` folder: `zip -r KD_4817_task_1b.zip task_1b_0.db3 metadata.yaml` (the two files, **no folder**).
6. **Gauri uploads** in the Task 1B slot.
7. Upload the video to YouTube as **Unlisted**, titled **`KD_4817_Task_1b`**, and submit the link. (The tuner GUI need not appear in the video.)

## Submission — KD 1C

1. Tune pitch + roll on top of 1B throttle; press **Save Values**.
2. Screen recording on. Launch: sim → tuner → `ros2 run swift_pico task_1c_controller` (watch the gains-sent-only-on-click trap above).
3. `ros2 bag record -o task_1c /pos_error /whycode_node/markers` for ≥ 60 s.
4. Inside `task_1c`: `zip -r KD_4817_task_1c.zip task_1c_0.db3 metadata.yaml`
5. Gauri uploads in the Task 1C slot; YouTube **Unlisted**, titled **`KD_4817_Task_1c`**.

## Scoring (same for 1B and 1C, 40 marks each)

| Part | Marks | Rule |
|---|---|---|
| Hovering | 16 | For each second inside the target box, up to 10 s |
| Finishing bonus | 8 | Only for the full 10 s (9 s = 0) |
| Speed | 16 | Full if finished within 15 s, dropping to 0 at 60 s |

Unclear (ask on the forum): when the clock starts, and whether hover seconds must be continuous. The repo tool `learning/tools/bag_score.py 1b task_1b` estimates the score from a practice bag (its assumptions are written in the file).

## The drone (simulated Swift Pico, from its model file)

1.5 kg (weight 14.7 N) · body 47 × 47 × 11 cm · each motor max 5.47 N (all four 21.9 N) → hovering needs ~67% power · loses height past ~48° tilt even at full power · overhead camera 20 m up, 60° view · physics step 0.005 s.

Manual flying (to feel it, optional): arm with `ros2 topic pub /drone_command swift_msgs/msg/SwiftMsgs "{rc_roll: 1500, rc_pitch: 1500, rc_yaw: 1500, rc_throttle: 1500, rc_aux1: 0, rc_aux2: 0, rc_aux3: 0, rc_aux4: 2000, drone_index: 0}"`. 1500 = neutral/hover, above = climb, `rc_aux4` other than 2000 = motors cut (the drone falls). Press Ctrl+C before sending the next command.

## Learning path (about 1 day, before tuning)

1. *PID Control — A brief introduction* (Brian Douglas, 8 min).
2. *What Is PID Control?* (MATLAB Part 1) → *A PID Tuning Guide* (Part 4, the most useful).
3. Portal *PID Controller* page: "P, PD & PID for Drones" + the ball-and-beam demo (press Start, try P, then PD, then PID).
4. *Drone flight physics in under 2 minutes* (Dronology) for 1C.
5. Optional: *Introduction to Quadcopters* (e-Yantra talk), minutes ~12–26 and ~42–48.

Links: `07_Learning_Resources.md`.
