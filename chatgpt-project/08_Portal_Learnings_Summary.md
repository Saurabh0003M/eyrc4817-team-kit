# 08 — What e-Yantra's learning pages say (summary) + mistakes we found

Summaries of the portal's Learnings pages as shared on 16 September 2026. The portal pages are e-Yantra's, so log in for the full text. Links are in `07_Learning_Resources.md`.

## Khoj-o-Drone learnings

### ROS 2 (portal: ROS 2, Concepts, Tutorials, Turtlesim, Books)
- ROS 2 is middleware, not an OS. Make sure any tutorial is for **ROS 2**, not ROS 1 (commands differ).
- **Concepts page:** links to the official Humble concept docs (nodes, discovery, interfaces, topics, services, actions, parameters, command-line tools, launch, client libraries; intermediate: ROS_DOMAIN_ID, middleware, logging, QoS, executors, topic statistics, RQt, composition, cross-compilation, security, tf2).
- **Tutorials page:** the official Humble tutorials, meant to be done **in order** (CLI tools → client libraries → intermediate → advanced).
- **Turtlesim page:** hands-on commands: `ros2 run turtlesim turtlesim_node`, `turtle_teleop_key`, `ros2 topic list/echo`, services (`/clear`, `/kill`, `/reset`, `/spawn`, `/turtle1/set_pen`, `/turtle1/teleport_absolute`), action `ros2 action send_goal /turtle1/rotate_absolute turtlesim/action/RotateAbsolute "{theta: 1.57}" --feedback`, drawing a line/circle with `ros2 topic pub /turtle1/cmd_vel …`, remapping teleop to a second turtle.
- **Books page:** leads to a paid book. Skip.
- **More links:** The Robotics Back-End, ROS 2 for ROS developers, The Construct, the ROS 2 CLI cheat sheet PDF, Articulated Robotics "ROS Overview", video "What Is ROS2? – Framework Overview".
- **Cheat sheet caution:** it's from 2019. `ros2 msg` / `ros2 srv` don't exist in Humble (use `ros2 interface show`), and its bag examples leave out the word `bag` (`ros2 bag record`, `ros2 bag play`, `ros2 bag info`).
- **Task 1 needs only:** running launch files and nodes in separate terminals, sourcing, `ros2 topic list/echo`, and `ros2 bag record`. Writing your own nodes matters from Task 2.

### MuJoCo (portal: MuJoCo, Concepts, Tutorials)
- MuJoCo (Multi-Joint dynamics with Contact), by Google DeepMind: a physics engine for robots, with accurate soft contact modelling.
- A simulation = **model** (`mjModel`, fixed description written in **MJCF** XML: bodies, joints, geoms, actuators, sensors) + **data** (`mjData`, the state that changes every step). MJCF is more expressive than ROS's URDF; MuJoCo can load URDF too.
- Tutorials: Overview ("hello world" falling box) → `pip install mujoco` → introductory Colab → later mjSpec, rollouts, **LQR Colab**, least squares. MJX/Unity are advanced. **MuJoCo Menagerie** has ready robot models, including Crazyflie 2 and Skydio X2 quadrotors.
- For Task 1 you don't write MuJoCo code; the simulators are provided.

### Quadcopters + Swift Pico (portal)
- Multirotors: tri/quad/hexa; adjacent motors spin opposite ways.
- Coursera "Aerial Robotics" figure: thrust forces F1–F4, motor torques M1–M4, rotor speeds ω1–ω4, arm vectors r1–r4, world axes (a) vs body axes (b). *(The page mentions a4 and b4 axes, which don't exist; it's a typo.)*
- 4 controls: throttle (all motors), pitch (rear vs front motors → forward/back), roll (one side vs the other → left/right), yaw (clockwise vs counter-clockwise pairs → spin). Moving in x/y **requires tilting**; hover only when level.
- Sensors: accelerometer, gyroscope, magnetometer, barometer, GNSS/GPS, rangefinders, optical flow. Flight controllers (Pixhawk 6C, Cube Orange). PX4 and ArduPilot guides are further reading.
- Videos: "Drone flight physics in under 2 minutes" (Dronology); **e-Yantra "Introduction to Quadcopters" talk (1 h)**: ~12–26 min = dynamics; ~26–42 min = parts (frames, props, brushless motors, ESCs, flight controller, RC, GNSS, LiPo, firmware PX4/Betaflight/ArduPilot/iNav); **~42–48 min = control cascade** (position controller → angle controller with IMU feedback → motor speeds); ~49–52 min = planning (Mission Planner/QGC, A*, Dijkstra, RRT).
- **Swift Pico page:** `cd ~/pico_ws`, `ros2 launch swift_pico swift_pico_simulation.launch.py`; topics `/drone_command`, `/rotors/odometry`, `/clock`, `/image_raw`, `/camera_info`, `/rotors/command/roll_pitch_yawrate_thrust`, `/rotors/command/motor_speed`; message `swift_msgs/msg/SwiftMsgs` (all int64: rc_roll, rc_pitch, rc_yaw, rc_throttle, rc_aux1–4, drone_index); RC 1000–2000 centred on 1500; arm with `rc_aux4: 2000` at throttle 1500; throttle 1600 climbs; disarm = motors cut (the drone falls); Ctrl+C between `ros2 topic pub` commands. *(Its screenshots show old names `/drone/rc_command` and `~/pico_mujoco_ws`; the text is current.)*
- **Motor numbering:** the portal's diagram numbers motors 4 (front-left), 2 (front-right), 3 (rear-left), 1 (rear-right), which differs from the simulator's model file. Don't mix them up (matters for Stage 2 hardware).

### Quadcopter Control (portal)
- 6 degrees of freedom: x, y, z + roll φ (about x), pitch θ (about y), yaw ψ (about z). Inertial (earth) frame vs body frame (the IMU measures in the body frame).
- **"To Do" exercise:** derive translational equations of motion with Euler–Lagrange, linearize, and build the state space. **Missing piece:** with only potential energy (mgz) and translational kinetic energy, you get free fall. The **rotor thrust must be added as an external force**, tilted by the attitude. About hover (small angles, thrust ≈ mg): ẍ ≈ g·θ, ÿ ≈ −g·φ, z̈ ≈ ΔT/m (signs depend on convention).
- **Hardware architecture (Stage 2):** overhead WhyCon camera → laptop running the PID/LQR position loop → RC transmitter connected to the laptop → drone's RC receiver → RC map → onboard **attitude controller** (outer angle loop P + feed-forward; inner rate loop PID; "square-root controller") → motors. The competition uses the laptop-controlled path. The simulator mirrors this structure.

### Control Systems (portal: Map, Intro, Modelling, Examples, Stability, Pendulum, PID, LQR)
- **Map of Control Theory** poster (Brian Douglas): orientation only. For Stage 1, PID, state space, linearization, stability and LQR matter.
- **Portal's focus statement:** "focus on classical **PID** control and modern **LQR/LQI** control, as these are the ones you'll actually be implementing on the drone" (a later task, probably).
- **Intro:** control system = controller + actuator; open loop (traffic light, washing machine) vs closed loop (AC, autonomous car, drone flight controller). Book: *Fundamentals of Control Theory* (portal PDF). Playlist: Brian Douglas *Classical Control Theory* (46 videos, ~10 h; use as reference).
- **Modelling:** F = ma with correct units; **Euler–Lagrange** (L = KE − PE; d/dt(∂L/∂ẋ) − ∂L/∂x = 0), worked on a falling mass (ÿ = −g); **state space** ẋ = Ax + Bu, y = Cx + Du; **linearization**: equilibrium points → Jacobian → A at each point → eigenvalues (positive real part = unstable).
- **Examples:** point mass, spring–mass–damper, 2D projectile (gravity as a constant disturbance), rotation about one axis.
- **Stability:** a coupled system with equilibria (0,0), (1,−1), (−1,1); eigenvalues −1 ± i (stable) and 2 ± 2√2 (unstable). Continuous systems: stable if all eigenvalues have negative real parts; discrete systems: eigenvalues inside the unit circle.
- **Pendulum:** ml²θ̈ + mgl·sin θ = τ; hanging (0,0) → eigenvalues ±i√(g/l) (marginally stable, keeps swinging); upright (π,0) → ±√(g/l) (unstable).
- **PID page:** P reduces but never removes steady-state error and can oscillate; PD damps oscillation; PID removes steady-state error. u(t) = Kp·e + Ki·∫e dt + Kd·de/dt. **Drone example with real graphs (Pluto drone):** P oscillated and overshot; PD gave damped oscillation with steady-state error; PID had no overshoot and no steady-state error. MATLAB "Understanding PID Control" Parts 1–7.
- **LQR page:** u = −Kx; closed loop ẋ = (A − BK)x; choose K by minimising J = ∫(xᵀQx + uᵀRu)dt; bigger Q weight = that state matters more; R = 1 for a single input; K comes from the Riccati equation (Octave's `lqr` command); Murray's LQR lecture notes; MATLAB State Space Part 4 + Riccati video.

**Mistakes found in the control pages:**
1. **PID integral formula**: written as `Iterm = (Iterm + error) · Ki`. That multiplies the whole running total by Ki every step (with Ki = 0.5 it creeps toward a limit; with Ki = 2 it explodes). Correct: `Iterm = Iterm + Ki · error` (× dt).
2. Linearization example: an eigenvalue −2√2 is printed as −2.824 (it's −2.828).
3. The Quadcopter Control "To Do" leaves out thrust (see above).

### Image Processing, OpenCV Python, ROS 2–OpenCV (portal)
- Digital image processing pipeline: **acquire → preprocess → segment → extract features → decide**. This is exactly KD 1A's steps.
- Image = function F(x, y) sampled on a grid; binary / grayscale (0–255) / colour (3 channels, ~16.7 million colours).
- **OpenCV loads BGR**, not RGB (convert before showing with matplotlib).
- HSV table (hue in degrees: red 0–60, yellow 60–120, green 120–180, cyan 180–240, blue 240–300, magenta 300–360). **OpenCV halves hue: 0–179.** *(Simplification in the table: red also wraps around near 330–360°, i.e. near 165–179 in OpenCV.)*
- OpenCV Python page: a first script `imread → cvtColor(BGR2HSV) → inRange → mask` then `findContours`; the official 4.x tutorial list (colour spaces, geometric transformations, thresholding, smoothing, morphology, gradients, Canny, contours, histograms, template matching, Hough lines/circles). **No ArUco tutorial is listed**, and 4.x docs use the new ArUco API; our OpenCV 4.5.4 needs the old one. freeCodeCamp OpenCV course video.
- ROS 2–OpenCV page: camera frames arrive as `sensor_msgs/msg/Image`; `cv_bridge.CvBridge().imgmsg_to_cv2(msg, desired_encoding='bgr8')` converts to an OpenCV image (and `cv2_to_imgmsg` back). Install: `sudo apt install ros-humble-cv-bridge`. Two long The Construct videos (object detection, line following). **Note:** the drone simulator only publishes `/image_raw` when launched with `image_sink:=both` (default is shared memory for the WhyCode node). This is for Task 2, not Task 1.

### Coding Standard (portal)
File header (Team ID, Theme, Author List, Filename, Functions, Global variables), a Purpose / Input Arguments / Returns / Example call block under every function, descriptive variable names (no `a`, `b`, `temp`), comments on tricky parts. Full template: `05_Setup_Run_Submit.md`.

## PacBot learnings

### MQTT (portal: MQTT, Concepts, Tutorials)
- Publish/subscribe protocol (IBM, 1999, built for slow unreliable links, so it's tiny). Clients never talk directly; **every message goes through a broker**. Topics are slash strings created by publishing. Publishers and subscribers are decoupled in space, time and sync.
- **Wildcards:** `+` one level (`home/+/temperature`), `#` everything below, last character only (`home/#`).
- **QoS:** 0 at most once (no acknowledgement); 1 at least once (PUBACK; duplicates possible); 2 exactly once (PUBLISH → PUBREC → PUBREL → PUBCOMP).
- **Sessions:** CONNECT carries client ID, credentials, keep-alive, clean-session flag; persistent sessions keep subscriptions and queue QoS 1/2 messages while offline.
- **Retained message:** the last known value, handed to new subscribers immediately. **Last Will and Testament:** published by the broker if a client disconnects ungracefully.
- Each concept is paired with a HiveMQ "MQTT Essentials" chapter; OASIS specs for v5.0 and v3.1.1.
- **Tutorials:** install `mosquitto mosquitto-clients`; try `mosquitto_sub -h test.mosquitto.org -t "pacbot/test"` and `mosquitto_pub … -m "hello mqtt"`; Python paho-mqtt subscriber/publisher using `CallbackAPIVersion.VERSION2`; C++ `paho.mqtt.cpp` built from source.
- **Security caution:** `test.mosquitto.org` is public, unencrypted and unauthenticated; anyone can read or publish. Use the local broker for real work.

### Path Planning (portal)
- Path planning answers "where am I, where must I go, which way?". Used in warehouses, self-driving cars, vacuum robots, drones, rovers, robot arms, games, navigation apps.
- Maze → graph (open cell = node; neighbours without a wall = edge). Every algorithm keeps a **frontier** and differs only in **which frontier cell it expands next**.
- **BFS** (oldest; rings; shortest on equal costs; undirected) · **DFS** (newest; one long thread; finds a path, not a good one) · **Dijkstra** (cheapest so far; handles costs; BFS = Dijkstra with unit costs) · **Greedy best-first** (smallest heuristic; fast; not guaranteed shortest; commits into dead ends) · **A\*** (cost so far + estimate; cheapest if the heuristic never overestimates; h = 0 → Dijkstra; ignoring cost so far → Greedy).
- The page's final hint for Task 1A: the grid is fully visible from the start, you need a *good* route, and what to do about the pellets is your decision.
