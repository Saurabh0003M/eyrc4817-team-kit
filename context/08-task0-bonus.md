# Task 0 (Bonus) — turtlesim circle + Swift Pico bring-up

Source: portal `theme_kd/stage_1/task_0/`, Bonus page. Saurabh pasted it into chat on 2026-09-13.
This is a distilled copy; the portal remains the authority. **Not submitted — practice only.** It
is still worth doing properly, because Part 2 creates `~/pico_mujoco_ws` (**replaced by `~/pico_ws` on 2026-09-16** per the Task 1 page), the workspace **reused
for later tasks (Task 1B)**.

| Part | Status (2026-09-13) |
|---|---|
| 1 — turtlesim circle | **DONE**, verified from logs and from pixels |
| 2 — Swift Pico MuJoCo | **UNBLOCKED 2026-09-16**: apt packages installed, fresh `~/pico_ws` builds all 17 packages. Launch not yet tried |

Portal figures and our results are in `eYRC 2026-27/Media/Task0/`: `bonus_task0.webp`,
`pico_drone.webp`, `bonus_part1_result.png`.

## Part 1 — Turtlesim circle (ROS 2)

**Requirements [DOC-SOURCED]:** a circle of **diameter 2.0** centred at **(5.0, 5.0)**, then park the
turtle at **(5.0, 5.0)**. The result should "resemble" `bonus_task0.webp`.

> **The portal contradicts itself [MEASURED 2026-09-13].** The text says diameter 2.0, but the
> figure's circle is **~8.0 across** (376 px at 47 px per unit), centred at about (4.9, 4.95). The
> node therefore takes **`radius` as a ROS 2 parameter**: default 1.0 per the text,
> `-p radius:=4.0` to match the figure. Both runs verified; see `bonus_part1_result.png`.

### e-Yantra's turtlesim is not stock turtlesim [VERIFIED from source]
The `turtle_sim` branch is a fork of `turtlesim` 1.4.2 that **overrides** `/opt/ros/humble`'s
package, so colcon warns about it. Build with `--allow-overriding turtlesim` to silence the warning.
- Turtle image `e.png` is a drone, 48×47 px. Background is navy `#122648`, the pen is `#b3b8ff`,
  width 3.
- **Spawns at (5.0, 2.0), heading 0 (east).** Not (5.544, 5.544) like stock turtlesim.
- The window is 500 px and one unit = the icon height of 47 px, so the world is ~10.6 units wide.
- The turtle stops if no `cmd_vel` arrives for 1 s. Teleporting draws a line while the pen is
  down.
- Each 16 ms frame updates heading first, then position. So constant `v`, `w = v/r` closes a
  clean circle.

### What was built
```
~/turtlesim_ws/src/
├── eYRC_26-27_Khojo-Drone/        (turtle_sim branch — e-Yantra's turtlesim fork)
└── kd_task_0/                     (ament_python)
    ├── kd_task_0/task_0_4817.py   ← the node
    ├── setup.py                   console_scripts: task_0_4817 = kd_task_0.task_0_4817:main
    └── package.xml                exec_depend: rclpy, geometry_msgs, turtlesim
```
Run it:
```bash
cd ~/turtlesim_ws && colcon build --allow-overriding turtlesim && source install/setup.bash
ros2 run turtlesim turtlesim_node                                # terminal 1
ros2 run kd_task_0 task_0_4817                                   # terminal 2 (text spec)
ros2 run kd_task_0 task_0_4817 --ros-args -p radius:=4.0         # figure size
ros2 service call /reset std_srvs/srv/Empty                      # clear + respawn between runs
```

### How the node works (study this — it is Task 1B in miniature)
- One **50 Hz timer** runs a **state machine**: pen up → drive to (5, 5−r) → face east → pen down →
  circle → pen up → drive to centre → done. The pose subscriber only *stores* the latest pose,
  and all decisions happen in the timer.
- **Driving to a point = P-controller:** `w = K·heading_error` and
  `v = K·distance·max(0, cos(heading_error))`. That is a position controller, the same idea as
  the drone PID, minus I and D.
- **Circle closed-loop:** stop when the *measured* accumulated heading reaches 2π. Open-loop
  timing (`2πr/v` seconds) is not used. The theta difference is wrapped, because theta jumps
  +π → −π once per lap.
- **Services without deadlock:** `call_async` plus checking `future.done()` on later ticks.
  Blocking inside a callback would wait forever, because the reply needs the same executor.
- **Parameter** `radius`: the same mechanism will expose PID gains in Task 1B.

### Results [MEASURED 2026-09-13]
| Run | turned | radius error mean / worst | ring radius from pixels | parked error |
|---|---|---|---|---|
| r = 1.0 | 360.09° | 0.0069 / 0.0106 | 1.001 | 0.0099 |
| r = 4.0 | 360.02° | 0.0201 / 0.0341 | 4.001 | 0.0098 |

The pen line is ~0.064 units wide, so all errors are invisible. The residual comes from arriving at
the start point within `POS_TOLERANCE = 0.01`, which offsets the whole circle.

### Try it yourself (self-improvement exercises)
1. Set `POS_TOLERANCE = 0.001` and rebuild. Does the radius error drop? How much longer does
   parking take, and why? Hint: a P-controller slows exponentially near the goal.
2. Delete the `max(0, cos(...))` factor in `drive_to`, run again, and watch the path with the pen
   left down.
3. Replace the closed-loop stop with a pure timer (`2πr/v` seconds). Compare gap or overlap across
   a few runs.
4. Make `K_ANGULAR` a parameter too, then try 1, 6 and 60. Find where it starts to oscillate. That
   is the "tuning" feeling you will need for the drone.

## Part 2 — Swift Pico MuJoCo simulation

**Setup [DOC-SOURCED]**, done 2026-09-13 except the steps marked ✗:
```bash
mkdir -p ~/pico_ws/src && cd ~/pico_ws/src
git clone -b kd_sim https://github.com/eYantra-Robotics-Competition/eYRC_26-27_Khojo-Drone.git --recursive .
cd ~/pico_ws && colcon build                                        # ✗ failed, see below
echo "source ~/pico_ws/install/setup.bash" >> ~/.bashrc           # done
ros2 launch swift_pico swift_pico_simulation.launch.py                    # ✗ not yet; Ctrl+C to stop, never Ctrl+Z
```

**Repo contents:** `swift_pico` (launch file + `mujoco_bridge`), `swift_pico_description`
(`models/swift_pico/drone.xml`), and submodules `rotors_simulator` (`swift_msgs`,
`rotors_control`, `rotors_swift_interface`), `mav_comm`, `whycode-ros2` and `controller_tuner`
(`pid_tune`). The launch starts: `mujoco_bridge` (a Python MuJoCo physics + viewer + ROS bridge),
`whycode_node`, `roll_pitch_yawrate_thrust_controller_node`, `rotors_swift_interface`, and
`image_view`.

**Why the build failed [VERIFIED]:** `rotors_control` does `find_package(actuator_msgs)`, which is
not installed. colcon then aborted `whycode`, `mav_planning_msgs` and `rotors_swift_interface`. A
dependency scan of every `package.xml` shows only **two apt packages are really needed**:
- `ros-humble-actuator-msgs`: CMake build dependency, and `mujoco_bridge` imports it at runtime
- `ros-humble-image-view`: the launch file starts an `image_view` node

The other undeclared keys are harmless:
- `dynamic_reconfigure` and `message_runtime` are ROS 1 leftovers, never `find_package`'d
- `eigen` and `opencv` are satisfied by `libeigen3-dev` and `libopencv-dev`
- `ros_gz`, `sdformat_urdf` and `joint_state_publisher_gui` are for Gazebo only
  (`rotors_swift_gazebo`). Not needed for MuJoCo, and `ros_gz` would pull in all of Gazebo, so
  skip them

**numpy clash — FIXED 2026-09-13:** `mujoco_bridge` imports `cv_bridge`, which apt builds against
numpy 1.x. PacBot's `pip install mujoco` had pulled **numpy 2.2.6** into `~/.local`, which made
`cv_bridge` fail with "numpy.core.multiarray failed to import". Fixed with
`pip3 install --user "numpy<2"` (now 1.26.4). Verified after the fix: MuJoCo 3.11.0 imports and
steps a model correctly, `cv_bridge` round-trips an image, `paho-mqtt` imports, and the KD venv is
untouched (numpy 2.2.6 + MuJoCo 3.9.0 there). Undo with `pip3 install --user numpy==2.2.6`,
which would break the sim again.

**Which MuJoCo does the sim use? [INFERRED, confirm on first launch]** `ros2 run` starts the bridge
with `/usr/bin/python3`, so it will use **MuJoCo 3.11.0 from `~/.local`**, not the KD venv's 3.9.0.
If model loading fails or behaviour looks wrong, check the version first. Do not add the venv to
`PYTHONPATH`: its numpy 2.2.6 breaks `cv_bridge`.

Expected screen: `pico_drone.webp`. Flying by hand: `07-swift-pico-interface.md`. Arm with
`rc_aux4: 2000` at throttle 1500, and **disarm only near the ground**.

## Layout — applied 2026-09-13

Real workspaces sit at the portal's paths `~/turtlesim_ws` and `~/pico_ws`.
`~/Desktop/e-yantra/turtlesim_ws` and `~/Desktop/e-yantra/pico_ws` are **symlinks** to
them. This is the reverse of `drone_ws`, on purpose. colcon and CMake write physical absolute paths
into `build/` and `install/`, and the `.bashrc` line and later tasks assume the home-level path.
Building through a symlink mixes logical and physical paths.
