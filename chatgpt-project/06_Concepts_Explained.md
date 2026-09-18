# 06 — Concepts explained in plain words

Each entry: what it is, an everyday picture, and where it's used in Task 1.

## Control and PID (KD 1B, KD 1C, PB 1B)

- **Setpoint**: where you want to be. **Error** = setpoint − where you are. *Picture:* destination in Maps, and the distance left.
- **Open loop**: act without checking the result. **Closed loop / feedback**: measure → compare with the goal → correct → repeat. *Picture:* walking to a door with eyes closed vs open.
- **PID controller**: the most common feedback rule. Output = **P + I + D**:
  - **P (proportional)** = Kp × error. Push harder when far away. Too big → overshoots and swings.
  - **I (integral)** = Ki × (error added up over time). Slowly removes an error that won't go away (e.g. a heavier drone settling slightly low). Too big → slow big swings.
  - **D (derivative)** = Kd × (how fast the error is changing). Brakes when approaching the target fast, which calms swinging. Too big → jittery; amplifies sensor noise.
  - *Picture:* parking a car. Steer harder when far from the spot (P), nudge if still slightly off (I), brake as you get close (D).
- **Overshoot**: going past the target. **Oscillation**: swinging back and forth. **Steady-state error**: settling slightly off the target. **Settling time**: how long until it stays near the target.
- **Integral windup**: the I term keeps growing while the system is stuck (e.g. motors at maximum), then overshoots badly once free. Fix: limit (clamp) the I term.
- **Tuning order** (portal): Kp until it oscillates → back off a bit → add Kd → small Ki. One change at a time.
- **dt**: time between updates. In code, I uses `error × dt` and D uses `(error − previous_error) / dt`. If dt is folded into the gains, the gain numbers depend on the loop rate.
- **What e-Yantra's drone graphs show** (portal "P, PD & PID for Drones"): P alone keeps oscillating; PD damps it but leaves a steady-state error; PID settles on the target.

## Drones (KD)

- **Quadcopter**: 4 propellers. **Diagonal motors spin the same way**, neighbours the opposite way, so their twisting forces cancel and the drone doesn't spin.
- **Throttle**: all motors faster/slower → up/down. **Pitch**: tilt forward/back → moves forward/back (rotation about the y-axis, motion along x). **Roll**: tilt left/right → moves left/right (rotation about x, motion along y). **Yaw**: spin on the spot (one diagonal pair faster).
- **Why sideways control is indirect**: the drone can only push "up" relative to itself. To move sideways it tilts, which splits the thrust into an upward part and a sideways part (sideways acceleration ≈ g × tilt angle). Tilting also loses some height, which is why throttle, pitch and roll affect each other. It can only hover when level.
- **Control cascade** (e-Yantra talk): a position controller turns "go to x, y, z" into tilt angles and thrust; an attitude controller turns angles into motor speeds. **In the simulator, the gains you tune are the position controller**; e-Yantra's `rotors_control` does the attitude part.
- **RC values 1000–2000**: radio-control command numbers, 1500 = neutral. `rc_throttle` 1500 ≈ hover. **Arming** = motors on (`rc_aux4 = 2000`); any other value cuts the motors instantly.
- **WhyCon / WhyCode marker**: a black-and-white circle pattern on top of the drone. An overhead camera finds it and gives the drone's (x, y, z). No marker in view = no position = no control.
- **Stage 2 hardware** (if selected): the same structure for real. Overhead camera → laptop runs PID → RC transmitter → the drone's flight controller → motors.

## ROS 2 (KD)

- **ROS 2** (Robot Operating System 2): **not an operating system**. It's a messaging system plus tools that let separate robot programs talk. *Picture:* group chats between programs. **Humble** is just the version name.
- **Node**: one running program. **Topic**: a named channel (e.g. `/pos_error`). **Message**: one packet on a topic, with fixed fields. **Publish** = send, **subscribe** = listen.
- **Service**: a request with one reply. **Action**: a longer goal with progress updates. **Parameter**: a setting a node reads.
- **Launch file**: starts several nodes at once (`ros2 launch …`). **Workspace**: a folder of packages built with **colcon**; every new terminal must **source** `install/setup.bash` so ROS finds them.
- **Bag file** (`ros2 bag record`): a recording of topic messages. **KD 1B/1C submissions are bag files.**
- **`ROS_LOCALHOST_ONLY` / `ROS_DOMAIN_ID`**: stop ROS 2 programs on different laptops on the same Wi-Fi from seeing each other.
- Useful commands: `ros2 topic list`, `ros2 topic echo /pos_error`, `ros2 node list`, `ros2 interface show <type>`, `ros2 bag info <folder>`.

## Simulation, MuJoCo (KD 1B/1C, PB 1B)

- **Simulation**: testing on a computer model before real hardware. Crashes are free, but the model is never perfectly real (the **sim-to-real gap**).
- **MuJoCo**: the physics engine both themes use. A **model** (XML file: bodies, joints, motors, sensors; fixed) plus **data** (positions and speeds that change every step).
- **Timestep**: how much simulated time passes per step (the drone sim uses 0.005 s; PacBot 1B 0.002 s).

## Images, OpenCV (KD 1A)

- **Pixel**: one dot. A colour image is a grid of pixels, each 3 numbers from 0–255.
- **OpenCV** (`cv2`): the image-processing library. It stores colour as **BGR**, not RGB.
- **HSV**: Hue (which colour), Saturation (how vivid), Value (how bright). Better than BGR for "find everything yellow", because lighting mostly changes V. **OpenCV hue is 0–179.** Red sits at both ends (near 0 and near 179), so it needs two ranges.
- **Mask / threshold**: a black-and-white image, white where a rule is true (`cv2.inRange`). **Morphology** (erode/dilate/open/close): cleans specks out of masks.
- **Contour**: the outline of one white blob (`cv2.findContours`). **Moments / centroid**: the centre point of a shape.
- **ArUco marker**: a square code with an ID, easy to detect precisely.
- **Perspective transform (homography)**: straightens a photo taken at an angle, using 4 known points and where they should go (`cv2.getPerspectiveTransform` + `cv2.warpPerspective`). The point order must match.
- **argparse**: Python's standard way to read `--image path` from the command line.

## MQTT (PacBot)

- **MQTT**: lightweight publish/subscribe messaging for small devices. **Everything goes through a broker** (our broker is **mosquitto** on localhost:1883). *Picture:* a post office.
- **Topic**: slash-separated name (`robot/pose`); created just by publishing to it. Wildcards: `+` = one level, `#` = everything below.
- **QoS 0/1/2**: at most once / at least once (possible duplicates) / exactly once.
- **Retained message**: the broker keeps the last message and gives it to anyone who subscribes later (PB 1A's pose and pellets are retained).
- **Last Will**: a message the broker publishes if a client disconnects badly.
- **vs ROS 2:** same publish/subscribe idea, but MQTT needs a broker in the middle and its payload is plain bytes (PacBot uses JSON text).
- **paho-mqtt 2.x** (Python library): create the client with `mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)`.
- **Security note:** the public test broker `test.mosquitto.org` is unencrypted with no password; anyone can read or send. Fine for "hello", never for real data.

## Path planning (PB 1A)

- **Graph**: cells = nodes, possible moves = edges. A wall = no edge.
- **Frontier**: cells found but not yet explored. The algorithms differ only in which frontier cell they explore next:
  - **BFS** (oldest first): spreads in rings; fewest steps when every move costs the same.
  - **DFS** (newest first): one long winding path; finds *a* path, usually not a good one.
  - **Dijkstra** (cheapest so far): handles different move costs; BFS is Dijkstra with equal costs.
  - **Greedy best-first** (looks closest to the goal): fast, not guaranteed shortest.
  - **A\*** (cost so far + estimated cost to go): shortest if the estimate never overestimates; usually explores far fewer cells.
- **Heuristic**: a quick distance estimate, e.g. grid distance |Δrow| + |Δcol|.
- **Visiting several goals** (2 pellets + an exit): try the possible orders and pick the shortest total. With 2 pellets there are only 2 orders (× 2 exits).

## Wall following (PB 1B)

- **ToF (Time-of-Flight) sensor**: measures distance by timing reflected light.
- **IMU**: gyroscope (turning rate) + accelerometer. Adding up the gyro's turn rate × dt gives how far the robot has turned.
- **Differential drive**: two wheels; different speeds make it turn. Equal speeds = straight, opposite = spin on the spot.
- **Wall-following rule**: keep one hand (e.g. right) on the wall; in a simply connected maze this reaches the exit.
