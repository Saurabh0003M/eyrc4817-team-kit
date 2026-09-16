# Swift Pico in MuJoCo — operational reference

The drone model used in simulation. The portal tutorial says explicitly: **"In this tutorial you will
learn how to use the Swift Pico drone model for Task 1B."** This is the single most important
operational page — keep it open while writing the controller.

Source: `portal.e-yantra.org/courses/theme_kd/learnings/quadcopter/` (Swift Pico tutorial).
Prerequisite stated by the portal: **complete the Installations part of Task 1B first.**

## Bring-up

```bash
cd ~/pico_ws
ros2 launch swift_pico swift_pico_simulation.launch.py
```

This starts the MuJoCo physics engine and viewer **plus two nodes that turn a `/drone_command`
message into motor speeds**. In every new terminal:

```bash
source install/setup.bash
```

**Kill with `Ctrl+C`, never `Ctrl+Z`.** The portal flags this and it matters: `Ctrl+Z` only
*suspends* the process — it keeps holding the ROS graph and the MuJoCo window, so your next launch
fails in a confusing way. `Ctrl+C` is slow here; wait for it.

## Topic map

| Topic | Role |
|---|---|
| **`/drone_command`** | **you publish here** — roll, pitch, yaw, throttle |
| **`/rotors/odometry`** | **you subscribe here** — the drone's position and orientation |
| `/image_raw`, `/camera_info` | onboard camera — the survivor-detection pipeline later |
| `/rotors/command/roll_pitch_yawrate_thrust` | internal, produced by the swift_pico nodes |
| `/rotors/command/motor_speed` | internal — you never write motor speeds directly |
| `/clock` | simulation time |

The pipeline is: **your node → `/drone_command` → swift_pico nodes → motor speeds → MuJoCo.** You
command intent, not motors.

## Message: `swift_msgs/msg/SwiftMsgs`

```bash
ros2 topic info /drone_command
ros2 interface show swift_msgs/msg/SwiftMsgs
```

Fields: `rc_roll`, `rc_pitch`, `rc_yaw`, `rc_throttle`, `rc_aux1`–`rc_aux4`, `drone_index`.
All fields are **`int64`** (portal screenshot of `ros2 interface show`, 2026-09-16).

**The 1000–2000 convention, centered on 1500.** This is not arbitrary: it is the RC servo/ESC pulse
width in microseconds, the same convention real flight controllers and receivers use. Consequence
worth understanding early — **the simulator speaks the same language as the Stage 2 hardware**, so
control code written now largely transfers to the real drone.

- `rc_throttle: 1500` — commands exactly the thrust needed to counter the drone's own weight, so it
  roughly holds height
- `> 1500` climbs, `< 1500` descends
- `rc_roll` / `rc_pitch` / `rc_yaw` — 1500 is neutral in each axis
- `rc_aux1`–`rc_aux3` — unused by this simulator
- **`rc_aux4`** — the arming channel

## Arming and disarming

| Action | Condition | Behaviour |
|---|---|---|
| **Arm** | `rc_aux4: 2000` | props spin; arm at a neutral `rc_throttle: 1500` first |
| **Disarm** | any other `rc_aux4` value | **motors cut instantly — the drone falls, it does not descend** |

Only disarm close to the ground. Harmless in simulation; on the Stage 2 hardware the same reflex
breaks propellers. Build the habit now.

Recovery tip from the portal: if the drone climbs into the camera and gets stuck, disarm to drop it.

**When publishing by hand, press `Ctrl+C` before entering the next command.** `ros2 topic pub`
repeats its message continuously and holds the terminal; without the interrupt your old command
fights the new one.

## What Task 1B almost certainly is

*[HIGH confidence as of 2026-09-12 — the portal names Task 1B directly and hands you exactly the two
topics a position controller needs.]*

Subscribe to `/rotors/odometry`, compare position against a target setpoint, and publish corrections
to `/drone_command`. **That is a PID position controller**, and it is the whole shape of the task.

Axis mapping, which is where the physics bites:

| Want to move | Command | Why |
|---|---|---|
| up / down (Z) | `rc_throttle` | direct — more or less thrust |
| forward / back (X) | `rc_pitch` | **indirect** — tilt redirects part of the thrust vector sideways |
| left / right (Y) | `rc_roll` | **indirect** — same mechanism |
| heading | `rc_yaw` | torque difference between CW and CCW props |

**X and Y control is indirect, and that is the crux of the theme.** You cannot command "move right";
you command a *tilt*, and the tilt splits the thrust vector into a vertical component (holding
altitude) and a horizontal one (producing motion). Tilting therefore costs you lift — which is why
altitude and lateral control interact, why hovering is only possible while level, and why tuning
these PIDs is finicky rather than four independent problems.

Practical tuning order: **get altitude (throttle) holding steady first**, alone, before touching
pitch and roll. A team that tunes all three at once cannot tell which gain caused which wobble.
