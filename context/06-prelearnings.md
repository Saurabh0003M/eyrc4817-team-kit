# Prelearnings (portal) — triaged study plan

Portal root: `portal.e-yantra.org/courses/theme_kd` · Learnings tree: `learnings/{linux, ros}`

This file is the **triage**, not a copy of the portal. The portal dumps ~45 links; this says what to
do, in what order, and what to skip. Source pages stay on the portal.

| Section | Portal path | Status here |
|---|---|---|
| Linux | `learnings/linux/linux/` | **AWAITING — not yet handed over** |
| ROS 2 | `learnings/ros/ros/` | captured below; **re-sent 2026-09-16** with sub-pages Concepts, Tutorials, **Turtlesim Resources**, Books → see "Portal re-send 2026-09-16" |
| MuJoCo | `learnings/mujoco/mujoco/` | captured below |
| Quadcopters | `learnings/quadcopter/quadcopters/` | captured below |
| Swift Pico model | `learnings/quadcopter/` | → **`07-swift-pico-interface.md`** |
| Task 1A / 1B / 1C instructions | — | captured → `09-task1-overview-and-1a.md`, `10-task1b.md`, `11-task1c.md` |
| Control Systems (Intro, Modelling, Stability, Pendulum, PID, LQR) | `learnings/control_system/` | **analysed 2026-09-16 → `12-learnings-control-systems.md`** |
| Image Processing · OpenCV Python · ROS 2–OpenCV · Quadcopter Control · Coding Standard | `learnings/image_processing/`, `learnings/quadcopter/` | **analysed 2026-09-16 → `13-learnings-quad-control-imgproc-coding.md`** |

## Portal re-send 2026-09-16 — what is new, and where it goes in the roadmap

Saurabh pasted the "ROS 2 & MuJoCo" learnings again, alongside the Task 1 pages. Most of it matches the
triage below. **New or changed items:**

| Portal item | What it gives you | Roadmap slot |
|---|---|---|
| **"What Is ROS2? – Framework Overview"** (YouTube `7TVWlADXwRw`, Raymond Andrade, 8:22, 2021, English captions) | Beginner overview using an example 4-wheel robot with camera/GPS/IMU: nodes talk over DDS; **publish/subscribe** (compared to YouTube channels and subscribers); **services** (request → response); **actions** (goal → feedback → result); **parameters** (e.g. wheel radius without recompiling); **bag files** (record topics, replay later); packages; cross-platform. *Summary written from its captions; not copied.* | **M4 rung ①** (before Articulated Robotics). Also mention it in **M6**: the Task 1B/1C submission *is* a bag file |
| **Turtlesim Resources page** | Hands-on CLI practice: `turtlesim_node` + `turtle_teleop_key`; `ros2 topic list/echo`; services `/clear` `/kill` `/reset` `/spawn` `/turtle1/set_pen` `/turtle1/teleport_absolute` (e.g. `ros2 service call /spawn turtlesim/srv/Spawn "{x: 5, y: 5, theta: 0}"`); action `ros2 action send_goal /turtle1/rotate_absolute ... --feedback`; draw a line and a circle with `ros2 topic pub /turtle1/cmd_vel ...` (circle: linear.x 2.0, angular.z 1.8); **remapping** a second teleop with `--ros-args --remap turtle1/cmd_vel:=turtle2/cmd_vel` | **M4 DO experiments**: Saurabh types these himself. They are the portal's own practice, and short enough to do by hand. It says the turtle spawns at (5, 2), which matches e-Yantra's turtlesim fork |
| ROS 2 Concepts page | Links to the official Humble concept pages (Basic: nodes, discovery, interfaces, topics, services, actions, parameters, CLI introspection, launch, client libraries; Intermediate: `ROS_DOMAIN_ID`, QoS, executors, RQt, security, tf2 …) | M4 rung ③. Unchanged from the triage below |
| ROS 2 Tutorials page | The official Humble tutorial sequence: CLI tools → client libraries → intermediate → advanced | M4 rung ③. The Tier 1/2/3 triage below still applies |
| **ROS 2 CLI Cheat Sheet (PDF)** | `portal.e-yantra.org/.../media/cli_cheats_sheet.pdf` sits **behind the portal login**, so Claude cannot fetch it | Ask Saurabh to download it into `eYRC 2026-27/Media/Learnings/`, then print or keep it open during M4/M6 |
| MuJoCo, MuJoCo Concepts, MuJoCo Tutorials | Same as the earlier capture: MJCF model vs `mjData` state; official docs; Colabs (intro, mjSpec, rollout, **LQR**, least squares); MJX/Unity marked advanced; Menagerie. The two figures are from the official Overview page (a body made of overlapping capsule/box/sphere geoms; the falling-box "hello world") | M5 rungs ①–②. The LQR Colab comes later, after PID works |

### Quadcopters + Swift Pico pages, cheat sheet, Menagerie (re-sent 2026-09-16, all read)

| Item | Key content | Roadmap slot |
|---|---|---|
| Video `iQAPkN7OWus` "Drone flight physics in under 2 minutes" (Dronology, 1:38) | Mode-2 sticks: throttle (all motors), yaw (one diagonal pair faster → torque turns the drone), pitch (rear pair faster → nose down → forward), roll (right pair faster → left) | **M2 rung ①**, replacing the unvetted "How Drones Fly!" |
| Portal Quadcopters page + Coursera figure | Quad/tri/hexa; F1–F4 thrust, M1–M4 reaction torques, ω1–ω4, r1–r4, world axes a vs body axes b (the page says a4/b4, which don't exist: portal typo); 4 DOF; **roll = rotation about X → motion along Y; pitch = rotation about Y → motion along X**; tilting splits thrust, so it can **only hover when level**; sensors (accelerometer, gyro, magnetometer, barometer, GNSS, rangefinder, optical flow); flight controllers; PX4/ArduPilot guides (further reading, not our stack, not opened) | **M2 rung ②** |
| Video `Gp80qN7kvfs` "Introduction to Quadcopters" (e-Yantra tech talk, 2025, 1:01:50) | ≈12–26 min: dynamics (motions, diagonal motors spin the same way to cancel torque, lift from Newton's 3rd law). ≈26–42 min: build parts (frames, props, brushed/brushless motors, ESC, FC, RC, GNSS/RTK, LiPo, firmware PX4/Betaflight/ArduPilot/iNav). **≈42–48 min: control cascade**: user gives *position* → position controller → *angle* → orientation controller with IMU feedback → RPM/PWM → ESC → motors. ≈49–52 min: planning (Mission Planner/QGC; A*, Dijkstra, RRT; Bug algorithms). Then applications + Q&A. It still says Stage 1 uses Gazebo (2025), which is now MuJoCo. *Summary from auto-captions; timestamps approximate.* | **M2 rung ③**: watch 12–26 and 42–48 min; the rest is optional. **The 42–48 min cascade = Task 1B/1C**: the tuned PID is the *position* layer, `/drone_command` feeds `rotors_swift_interface` → `roll_pitch_yawrate_thrust_controller` (orientation layer) → motor speeds |
| Portal Swift Pico page | Workspace now `~/pico_ws`; topics; `SwiftMsgs` fields are **int64**; arm with `rc_aux4: 2000` at throttle 1500; 1500 ≈ hover, 1600 climbs; disarm = motors cut, drone falls; Ctrl+C between `ros2 topic pub` commands. Its screenshots are outdated (they show `/drone/rc_command` and `~/pico_mujoco_ws`); the text and our 2026-09-16 trial confirm `/drone_command` | **M2-c / M5-a** (Saurabh types the pub commands himself) |
| Portal motor diagram | Numbering 4 = front-left, 2 = front-right, 3 = rear-left, 1 = rear-right (Betaflight-style). `drone.xml` numbers motors differently (m1 at +x−y, m2 −x+y, m3 +x+y, m4 −x−y). *[INFERRED] Don't mix the two numberings; this matters for Stage 2 Betaflight* | M2 "notice" item |
| **ROS 2 CLI cheat sheet PDF** | Now at `eYRC 2026-27/Media/Learnings/ros2_cli_cheat_sheet.pdf`. Canonical, **2019** (older than Humble). **Outdated bits [VERIFIED 2026-09-16]:** `ros2 msg` / `ros2 srv` don't exist in Humble (use `ros2 interface show`); its bag examples drop the word `bag` (use `ros2 bag info/play/record`); underscores are lost in rendering (`std msgs` = `std_msgs`) | M4 + M6 (bag commands) |
| MuJoCo Menagerie | Curated models loaded via `scene.xml`; min MuJoCo version per model README. **Quadrotors: `bitcraze_crazyflie_2`, `skydio_x2`** | Optional M5 extra: compare a real-world quadrotor model with the Swift Pico. Ask before cloning |

**Relevance check after Task 1 [INFERRED]:** Tasks 1B and 1C are *tuning*, not ROS coding. For
Task 1 itself Saurabh needs only enough ROS 2 to run three terminals, understand topics
(`/pos_error`, `/throttle_pid` …) and record a bag. The deeper ROS 2 tutorials (writing nodes,
services, actions) matter from Task 2 on. **The roadmap rebuild is still pending.** Do it once
Saurabh says all material (including PacBot Task 1 and the Image Processing / Control Systems / PID
for Drones pages) has been sent.

## Confirmed facts (these settle open questions)

**[DOC-SOURCED] ROS 2 distro is Humble.** Every documentation link on the portal points at
`docs.ros.org/en/humble/`. Humble Hawksbill is the LTS that targets **Ubuntu 22.04 Jammy**.

> **Hard lock — do not install Ubuntu 24.04.** Newer is wrong here. 24.04 ships ROS 2 Jazzy, and
> every command, package name and doc link the portal gives you would be for a different distro.
> The requirement is **Ubuntu 22.04 LTS + ROS 2 Humble**, full stop. See `03-machines.md`.

**[CONFIRMED 2026-09-12] MuJoCo is the simulator, not Gazebo.** The learnings tree has a dedicated
`learnings/mujoco/` section with its own concepts and tutorials pages; Gazebo appears nowhere.
MuJoCo is far lighter than Gazebo and runs fine on integrated graphics — this **defuses the Intel
Arc iGPU concern** in `03-machines.md`.

**[CONFIRMED 2026-09-12] Task 1B is a PID position controller on the Swift Pico drone in MuJoCo.**
The portal's Swift Pico tutorial names Task 1B outright and hands over exactly the two topics a
position controller needs — `/rotors/odometry` in, `/drone_command` out. This supersedes the earlier
WhyCon-lineage guess: the guess was right about *what* Task 1 is, and wrong only about the mechanism
in Stage 1 (odometry in simulation now; WhyCon marker tracking on real hardware in Stage 2).
**Operational detail: `07-swift-pico-interface.md`.**

**[DOC-SOURCED] ROS 1 material is a trap.** The portal warns explicitly: concepts carry over but the
CLI and APIs differ. Any tutorial you find must say ROS 2. Check before you follow it.

## What ROS 2 actually is (the one-paragraph version to teach the team)

ROS 2 is not an operating system — it's **middleware**. It is a strongly-typed, anonymous
publish/subscribe system that lets separate processes exchange messages. The whole robot is a
**graph**: independent programs (**nodes**) that publish and subscribe to named channels
(**topics**). Nothing else in the list below matters until that clicks.

For the drone: a PID controller is a node that *subscribes* to a position topic and *publishes* a
command topic. That is the entire shape of Task 1. Learn pub/sub properly and most of the rest is
detail you can pick up on demand.

## Tier 1 — the critical path. Everyone does these, in this order.

Eight tutorials. This is the real foundation; do not let anyone loose in the full link list first.

1. **Configuring environment** — sourcing `setup.bash`. The single most common beginner failure: you
   open a new terminal, nothing works, because you didn't source. Understand it once.
2. **Using turtlesim, ros2 and rqt** — see the graph move before reading theory about it.
3. **Understanding nodes**
4. **Understanding topics** ← the important one
5. **Using colcon to build packages**
6. **Creating a workspace**
7. **Creating a package**
8. **Writing a simple publisher and subscriber (Python)**

**Method:** interleave, don't stack. The Concepts pages and the Tutorials cover the same ground from
different angles — read the *Concepts* page for nodes, then do the *nodes* tutorial, then move on.
Reading all ten concept pages before touching a terminal is how people bounce off ROS 2.

**Language:** do **Python first**. The theme allows Python or C++; every tutorial has both variants.
Skip the C++ ones for now — you can come back when something needs the performance.

## Tier 2 — needed for Task 1/2, not for Task 0

- **Using parameters in a class (Python)** — this is how you expose **PID gains** for tuning without
  re-editing code. Standard practice, and you will want it the first time you tune.
- Understanding services · parameters · actions
- Creating custom msg/srv files, implementing custom interfaces
- **Launch files** — starting a dozen nodes with one command
- **Recording and playing back data (`ros2 bag`)** — replay a flight to debug a controller instead of
  re-flying it. Genuinely valuable on a drone theme.
- **`tf2`** — coordinate frame transforms. Camera frame → world frame is exactly the survivor
  localisation problem. Fundamental from Task 2; worth an early skim.
- **QoS settings** — becomes real the moment a position topic starts dropping messages.

## Tier 3 — skip for now

C++ variants of everything · composition and composable nodes · executors · plugins (pluginlib) ·
cross-compilation · topic statistics · different middleware vendors · testing · URDF and RViz
(useful later for modelling/visualising the drone, not now) · Advanced/Simulators (until MuJoCo).

## Two flags that don't fit the tiers

**`ROS_DOMAIN_ID` — read this early despite being filed under Intermediate.** ROS 2 nodes
auto-discover each other over the network. Four teammates running ROS 2 on the same college Wi-Fi
will silently discover each other's nodes and interfere — a genuinely confusing failure mode.
**Each member sets a unique `ROS_DOMAIN_ID`.** Agree the numbers before the first joint session.

**ROS 2 Security** (SROS2 / DDS security) is in the Intermediate concepts list. Three of the four
team members are Cyber Security branch — this is the natural bridge between the coursework and the
robot, and a real research direction. **Not urgent. Do not let it displace Tier 1.**

## Recommended external resources, ranked

1. **Articulated Robotics — "Getting Ready for ROS Part 4: ROS Overview (10 concepts you need to
   know)"** — best *why-before-how* explainer. Watch/read before the tutorial grind.
2. **"What Is ROS2? – Framework Overview"** (YouTube) — short framing video, good for the two
   members with no robotics background.
3. **The Robotics Back-End** (`roboticsbackend.com/category/ros2`) — Python-first ROS 2, good when an
   official tutorial is too terse.
4. **ROS 2 CLI Cheat Sheet** (PDF on the portal) — print it. Keeps you out of the docs for syntax.
5. *ROS 2 for ROS developers* (`fmrico/ros_to_ros2_talk_examples`) — only useful if you already know
   ROS 1. Nobody on this team does. **Skip.**
6. *The Construct* — good courses, largely paid. Skip while the free official path is unfinished.

## MuJoCo — triage

**What it is:** *Multi-Joint dynamics with Contact*, a physics engine from Google DeepMind for
articulated systems. Unlike a game engine's rigid-body solver it computes contacts through a soft,
convex-optimisation model, which is why robotics research uses it — accurate and differentiable
contact dynamics.

**The one concept to hold on to:** a simulation splits into a **model** (`mjModel`, the immutable
description of bodies, joints, geoms, actuators — authored in **MJCF**, MuJoCo's XML format) and
**data** (`mjData`, the mutable state that evolves each step). Everything below the Python bindings
assumes you understand that split.

**MJCF vs URDF** — coming from ROS you would expect URDF. MuJoCo loads URDF directly, but MJCF is
more expressive: contact tuning, sensors, and a CSS-like default-settings mechanism that keeps large
models compact.

**Do now:** Overview (the "hello world" falling box) · `pip install mujoco` · the **introductory
Colab tutorial**. That is enough to follow Task 1B.

**Do later, deliberately:** the **LQR control Colab** — the theme spec says "PID / **LQR**", and this
is the direct on-ramp. Only after your PID works. Model Gallery and **MuJoCo Menagerie** (curated
robot models) when you need reference models.

**Skip:** MJX (GPU/TPU MuJoCo in JAX), differentiable physics, parallel rollouts, the Unity plug-in,
the C API code samples, `mjSpec` model editing, engine extensions. These are research-scale tools;
nothing in Stage 1 needs them.

## Quadcopters — the physics that actually matters

This page is theory, and unusually it is worth reading properly rather than skimming — it explains
*why* the controller is shaped the way it is.

**The core idea:** adjacent rotors spin in opposite directions, which cancels net torque and lets the
craft lift without spinning. Four degrees of freedom — **throttle, roll, pitch, yaw** — all produced
by varying the four motors' relative speeds.

**The insight that makes Task 1B make sense:** X/Y motion is not commanded directly. To move
forward you *pitch*, and the tilt splits the thrust vector into a vertical component (holding
altitude) and a horizontal one (producing motion). So tilting costs lift, altitude and lateral
control interact, and **hovering is only possible while level**. Four PIDs, but not four independent
problems. Full mapping in `07-swift-pico-interface.md`.

**Sensors, and what each is actually for:** accelerometer (linear acceleration → tilt relative to
gravity) · gyroscope (rotation rates → roll/pitch/yaw correction) · magnetometer (heading) ·
barometer (altitude from air pressure) · GNSS/GPS (absolute 3D position) · rangefinders (obstacle
avoidance, landing, terrain following) · **optical flow** (downward camera + rangefinder for position
lock and hover stability where GPS is weak — relevant to an indoor disaster-zone arena).

**Flight controllers** are the autopilot hardware that firmware is flashed onto; it reads the sensors
and issues motor commands. The page names Pixhawk 6C and Cube Orange as common examples — note these
are **not** our Stage 2 kit, which pairs a smaller FC with Betaflight and an ELRS radio.

**PX4 and ArduPilot guides** are linked as further reading. Useful background on how real autopilots
are structured; **not** our stack. Read for concepts, do not follow their setup instructions.

## Suggested split for a ~3 week Task 0 window

Tier 1 is maybe 6–10 hours of real work per person. Everyone does all eight — this is shared
vocabulary, not something to divide up. Divide *after* Tier 1:

- **Gauri** → PID and control theory (her coursework), then `parameters in a class` for gain tuning
- **Saurabh** → workspace/package/colcon plumbing, and the MuJoCo bring-up when that page lands
- **Parth** → `ros2 bag`, launch files, `rqt_console` — the debugging and tooling surface
- **Mahesh** → `tf2` and coordinate frames, feeding into survivor localisation

Proposed 2026-09-12, not agreed with the team.
