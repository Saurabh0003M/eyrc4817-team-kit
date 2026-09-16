# Task 1C — tune Pitch (X) and Roll (Y), on top of the 1B throttle hold

Source: KD portal → Task 1 → Task 1C Instruction + Submission, pasted by Saurabh on 2026-09-16.
**The portal is the authority.** Deadline: unknown. Read `10-task1b.md` first; everything there
about the sim, libraries, tuner GUI and scoring applies here too.

## What it is [DOC-SOURCED + VERIFIED]
- Again **tuning, not coding**: `task_1c_controller` is a pre-built binary with the same prompts
  as 1B ("tune now? Y/N" → GUI, or enter gains manually). It prompts for three sections: Throttle
  (z), Pitch (x), Roll (y). It subscribes `/throttle_pid`, `/pitch_pid`, `/roll_pid` and publishes
  `/pos_error`.
| Axis | Moves | Tuner topic | Error field |
|---|---|---|---|
| Z | up/down | `/throttle_pid` | `throttle_error` — keep the 1B gains; small retune allowed |
| X | forward/back (**pitch**) | `/pitch_pid` | `pitch_error` |
| Y | left/right (**roll**) | `/roll_pid` | `roll_error` |
- **Target:** **all three** errors within **±0.4** within **5 s**, then held for **10 s** together.
- Method: confirm altitude holds with the 1B throttle gains → **Pitch and Roll are symmetric on this
  frame, so tune them together** (same gains) → raise Kp until it holds but oscillates → back off
  → add Kd → small Ki for leftover offset. Tilting to move costs vertical thrust, so throttle may
  need a small touch-up (the roadmap M2 "phone on palm" idea).
- Scoring is identical to 1B: hover 16 + finishing bonus 8 + speed 16 = 40.

## Submission [DOC-SOURCED]
1. Tune, then press **Save Values**.
2. Three terminals, **in this order (different from 1B!)**: sim → **tuner GUI** → `ros2 run
   swift_pico task_1c_controller`.
3. `ros2 bag record -o task_1c /pos_error /whycode_node/markers`, **≥ 60 s**.
4. From inside `task_1c/`: `zip -r KD_4817_task_1c.zip task_1c_0.db3 metadata.yaml` (two files,
   no folder). **Gauri uploads.**
5. YouTube: one continuous take, terminal visible before the sim launches. **Unlisted**, titled
   **`KD_4817_Task_1c`**. Submit the link. Example video: https://youtu.be/Ut5wKqhMFdM

## Tuner GUI facts, read from its source 2026-09-16 [VERIFIED from code]
(`~/pico_ws/src/controller_tuner/pid_tune/scripts/pid_tune_drone_button_ui.py`, commit `8267a97`
"Add Plotter and GUI integrated")
- **Save Values writes `~/pico_ws/src/swift_pico/src/pid_values.yaml`**, which the GUI reloads on
  start. The file `controller_tuner/pid_tune/scripts/pid_values.yaml` in the repo is **not** used.
  This resolves the path question in `10-task1b.md`.
- Default multipliers: **Kp × 0.03, Ki × 0.008, Kd × 0.6**. Sent value = integer × multiplier.
  Each row also has a **step** field (default 1) for the +/− buttons.
- It has a **built-in live graph of `/pos_error`** with a series picker, play/pause and a window
  control. Use it to watch `throttle_error`, `pitch_error` and `roll_error`; no separate plotting
  tool is needed.
- **TRAP [INFERRED from code, verify on first run]:** the GUI publishes a card's gains **only**
  when you press −/+ or Enter in a field. There is no periodic resend, and the default volatile
  QoS means a controller started *after* the GUI does not receive the loaded values. So in the
  1C submission order (GUI before controller), the drone may fly with zero gains until you press
  Enter in each card. The other safe route: answer **N** at the controller prompt and type all
  nine gains straight from `pid_values.yaml`.

## Portal videos (fetched 2026-09-16 with yt-dlp)
All three are on channel "roganjo", uploaded 2026-09-12, **silent screen recordings with no
captions and no description**: `ef2SI6uARuA` "Tuner and Plotter demo" (2:21), `xqOyre-afOE`
"task 1b submission demo" (0:59), `Ut5wKqhMFdM` "task 1c submission" (0:42). Understanding them
needs frames from the video itself (≈ 11.5 MB at 720p total). **Ask Saurabh before downloading.**
