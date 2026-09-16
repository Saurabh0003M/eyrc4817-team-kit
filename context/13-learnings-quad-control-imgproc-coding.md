# Portal learnings — Quadcopter Control, Image Processing, OpenCV, ROS 2–OpenCV, Coding Standard

Pasted by Saurabh on 2026-09-16; analysed from page text and figures plus video metadata only.

## 1. Quadcopter Control page
- **6 DOF**: x (forward/back), y (left/right), z (altitude); roll φ about x, pitch θ about y, yaw ψ
  about z. Inertial (earth) frame vs body-fixed frame; the IMU measures in the body frame.
- **"To Do" exercise** (learning, not graded as far as stated): derive the **translational**
  equations of motion with Euler–Lagrange (PE = mgz, KE = ½mv²), linearize, build the state
  space. **Trap in the page as written [checked]:** with only PE and translational KE, and no
  generalized force, Euler–Lagrange gives free fall (ẍ = ÿ = 0, z̈ = −g). The **rotor thrust has to
  enter as an external/generalized force**, rotated by the attitude. That is the missing piece.
  Expected linear result about hover (φ = θ = 0, thrust = mg), up to sign convention:
  ẍ ≈ g·θ, ÿ ≈ −g·φ, z̈ ≈ ΔT/m, state [x ẋ y ẏ z ż]. **This is exactly why Task 1C pitch and roll
  move x and y.** A good Gauri + Saurabh paper exercise (roadmap M2/M3 or the LQR module).
- **The Stage-2 hardware architecture [DOC-SOURCED]:** an **overhead WhyCon camera** measures the
  drone's (x, y, z) → a **laptop runs the PID/LQR position loop** → sends roll, pitch, yaw, thrust
  through an **RC transmitter plugged into the laptop** → the drone's RC receiver → RC map →
  onboard **attitude controller** (outer angle P + feed-forward, inner rate PID, square-root
  controller; "just for reading") → motors. The competition uses the laptop path, not a hand-held
  transmitter.
  **→ The simulator mirrors this exactly:** WhyCode node = overhead camera; `task_1b/1c_controller`
  = the laptop position loop; `/drone_command` = RC channels; `rotors_control` = the attitude
  controller.
- *[INFERRED, verify at Stage 2]* The diagrams use **ArduPilot** vocabulary ("RCx_Option", RC Map,
  square-root controller, accel limit), while the theme doc names **Betaflight Configurator**.
  Firmware choice unclear; don't prepare for either yet.

## 2. Image Processing Basics / OpenCV Python / ROS 2–OpenCV
- DIP pipeline: **acquire → preprocess → segment → extract features → decide**. It maps 1:1
  onto the Task 1A steps (load → warp → colour mask → contours/centres → nearest intersection).
- Image = F(x, y) array; binary / grayscale (0–255) / colour (3 channels). **OpenCV is BGR**
  (convert before matplotlib).
- HSV: Hue = colour angle, S = vividness, V = brightness. **OpenCV hue is 0–179 (halved)**. *Portal
  table simplification:* it lists red as 0–60°, but **red wraps around 0/360** (≈ 330–360° as
  well), so red usually needs **two `inRange` masks OR-ed**. That matters for the red triangles
  in Task 1A (roadmap M1 TALK already asks this).
- OpenCV Python page: a minimal `imread → cvtColor(HSV) → inRange → findContours` script, plus an
  ordered list of official **4.x** tutorials. Most relevant to Task 1A: Changing Colorspaces,
  **Geometric Transformations (includes warpPerspective)**, Thresholding, **Morphological
  Transformations** (clean speckles from masks), **Contours**, Trackbar (what `hsv_tuner.py`
  does). **The list has no ArUco tutorial**, and the 4.x docs show the *new* ArUco API that doesn't
  exist in our OpenCV 4.5.4; the roadmap's PyImageSearch (old API) link covers that gap.
  Video: `oXlwWbU8l2o`, freeCodeCamp, 4 h (already roadmap M1 rung ③).
- ROS 2–OpenCV page: `sensor_msgs/Image` → `cv_bridge.imgmsg_to_cv2(msg, 'bgr8')` subscriber
  example (topic name is a placeholder; check `ros2 topic list`). **Setup is ready:** `cv_bridge`
  works on this box (verified 2026-09-13 after the numpy < 2 fix).
  **[VERIFIED from the launch file 2026-09-16]** The Swift Pico sim's `image_sink` launch arg
  defaults to **`shm`** (shared memory for WhyCode) with options `dds|both`. So **`/image_raw` is
  NOT published by default**; any ROS camera node (a likely Task 2 need) must launch with
  `image_sink:=both` or `dds`.
  Videos (The Construct live classes, **optional, long**): `pK_SvyOm8pg` *Object Detection with
  OpenCV for ROS 2* (1:04:47), `88y_1ovno8g` *Line Following…* (1:11:49). → Task 2 prep, not
  Task 1.

## 3. Coding Standard (applies to submitted code, e.g. Task 1A `KD_4817_task1a.py`)
- **File header** in a `'''` block: `# Team ID: 4817`, `# Theme: Khoj-o-Drone`, `# Author List:`,
  `# Filename:`, `# Functions:` (comma list), `# Global variables:` (or None).
- **Each function** gets a `'''` block right after `def`: `Purpose:` / `---` / text;
  `Input Arguments:` / `---` / `` `name` :  [ type ] `` + description; `Returns:` / `---` / same
  format; `Example call:` / `---` / example.
- **Variables:** descriptive names (e.g. `table1_kp_val`). **No `a`, `b`, `temp`.** Add a one-line
  `# name: description` comment when the name isn't self-explanatory.
- **Implementation comments** `# …` on tricky or important parts.
- Setup/tooling implications: Claude's **Task 1A submission checker (roadmap M1-k)** should also
  check that the header fields exist, every `def` has a Purpose/Input/Returns/Example block, and
  there are no single-letter or `temp` variable names. Saurabh writes the comments; it's also good
  "explain it" practice.
