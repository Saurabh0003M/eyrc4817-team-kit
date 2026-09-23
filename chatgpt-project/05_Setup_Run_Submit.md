# 05 — Setup, running, submitting, coding standard, troubleshooting

## Requirements (from e-Yantra)

Ubuntu **22.04** LTS on **bare metal** (dual-boot is fine; **not** WSL, not a virtual machine, **not 24.04**) · x86_64 processor with more than 4 cores · 8 GB+ RAM · 100 GB+ disk recommended · **ROS 2 Humble** desktop (installed in Task 0).

Why 22.04 exactly: every portal command is for ROS 2 **Humble**, which only supports Ubuntu 22.04. Ubuntu 24.04 comes with a different ROS 2 version (Jazzy), and the portal's commands won't match it.

## One-command setup (team repo)

```bash
git clone https://github.com/Saurabh0003M/eyrc4817-team-kit.git ~/eyrc4817
cd ~/eyrc4817
bash setup/setup.sh --check     # look only: shows what's installed and what setup would change
bash setup/setup.sh             # do it: installs only what's missing (asks for the password once)
```

Then **open a new terminal** and run `--check` again: it should say everything is set up. Log file: `~/eyrc4817-setup.log`.

**What it checks first:** Ubuntu 22.04, x86_64, not WSL, not a VM, RAM, free disk (≥ 4 GB), ROS 2 Humble, internet. If a hard requirement fails, it stops before changing anything.

**What it installs or sets up (only if missing):**
- apt packages: `git zip curl python3-pip python3-venv python3-opencv python3-numpy python3-tk python3-yaml python3-matplotlib python3-reportlab libglfw3-dev ros-humble-actuator-msgs ros-humble-image-view ros-humble-rosbag2-storage-default-plugins python3-colcon-common-extensions mosquitto mosquitto-clients`
- pip (user): `numpy<2` (ROS 2's cv_bridge breaks on numpy 2), `paho-mqtt>=2`
- **MuJoCo 3.9.0 library** in `~/.local/share/eyrc4817/mujoco-3.9.0`. e-Yantra's drone simulator was built to look for `libmujoco.so.3.9.0` in a folder that only exists on the developer's own computer, so we point it to our copy.
- **`~/pico_ws`**: clones e-Yantra's Khoj-o-Drone repo (branch `kd_sim`, with submodules) and builds it with `colcon build`.
- **`~/pacbot_ws`**: clones e-Yantra's PacBot repo; creates `task1a/task_1a.py` and `task1b/task_1b.py` from the boilerplates.
- A marked block in `~/.bashrc` (backup saved as `~/.bashrc.eyrc4817-backup`): sources ROS 2 + `~/pico_ws`, adds the MuJoCo 3.9.0 path, and sets **`ROS_LOCALHOST_ONLY=1`** so teammates' simulators on the same Wi-Fi don't interfere.
- Enables the **mosquitto** MQTT broker as a service (localhost only).

**Two MuJoCo versions on purpose:** PacBot Task 0 installed MuJoCo **3.11.0** for Python; the KD simulator needs the **3.9.0** library. Setup never changes your Python MuJoCo.

**Manual setup (what the portal says), if not using the script:**
```bash
# Khoj-o-Drone (Task 1 page: delete any old ~/pico_mujoco_ws and use a fresh ~/pico_ws)
mkdir -p ~/pico_ws/src && cd ~/pico_ws/src
git clone -b kd_sim https://github.com/eYantra-Robotics-Competition/eYRC_26-27_Khojo-Drone.git --recursive .
cd ~/pico_ws && colcon build
echo "source ~/pico_ws/install/setup.bash" >> ~/.bashrc && source ~/.bashrc
sudo apt install python3-opencv python3-numpy libglfw3-dev
# PacBot
git clone https://github.com/eYantra-Robotics-Competition/eYRC_26-27_PacBot.git ~/pacbot_ws
sudo apt install mosquitto mosquitto-clients && pip install paho-mqtt
```
Manual setup still needs the MuJoCo 3.9.0 library fix above, or the drone simulator fails with `libmujoco.so.3.9.0: cannot open shared object file`.

## Where things are on the laptop (and why)

```
~/eyrc4817/     the team kit (GitHub repo): notes, these study files, tools, setup script
~/pico_ws/      KD workshop = a ROS 2 workspace
   src/         "source" = the code, the ONLY folder people edit. Holds packages (a folder + package.xml "ID card"):
      swift_pico/scripts/   task1a.py (KD 1A starter), image_1.jpg        ← KD 1A: write code here
      swift_pico/src/       task_1b_controller, task_1c_controller; pid_values.yaml (tuner "Save Values")
      swift_pico/launch/    start-up recipes (one command starts several programs)
      controller_tuner/ (package pid_tune: the tuning window) · whycode-ros2/ (marker tracker → drone position)
      rotors_simulator/ (simulator machinery, attitude controller) · mav_comm/ (message formats) · swift_pico_description/ (3D model)
   build/       colcon's workbench – ignore
   install/     the runnable result; `source ~/pico_ws/install/setup.bash` (in ~/.bashrc) lets `ros2 run/launch` find it
   log/         build diaries – read them when `colcon build` fails
~/pacbot_ws/    PB workshop = e-Yantra's download (not a ROS workspace), one folder per task:
   task1a/      task_1a_launch (the game: encrypted, only run it) · task_1a_boilerplate.py (template) · task_1a.py (your code) · result.yaml (--evaluate)
   task1b/      same pattern: task_1b_launch · task_1b_boilerplate.py · task_1b.py (+ lib/, meshes/ – don't touch)
```
- **Why the workshops aren't inside the kit:** e-Yantra's commands use exactly `~/pico_ws` and `~/pacbot_ws`, and colcon writes the workspace's full path into what it builds, so moving/renaming `~/pico_ws` (or a space in a folder name) breaks it.
- After editing a program you start with `ros2 run` / `ros2 launch`, run `colcon build` in `~/pico_ws`. Files started directly with `python3 …` need no rebuild.
- Find anything fast: in Files or any upload window press **Ctrl+L** and type the path.
- The portal writes `task_1a` / `task_1b`, but e-Yantra's repo folders are **`task1a` / `task1b`**.

## Running each task (one terminal per line, in order; stop with Ctrl+C)

| Task | Commands |
|---|---|
| KD 1A | `cd ~/pico_ws/src/swift_pico/scripts && python3 task1a.py --image image_1.jpg` |
| KD 1B | `ros2 launch swift_pico swift_pico_simulation.launch.py` → `ros2 run swift_pico task_1b_controller` → `ros2 launch pid_tune pid_tune_drone.launch.py` |
| KD 1C | same, with `task_1c_controller` |
| PB 1A | `cd ~/pacbot_ws/task1a && ./task_1a_launch` → `cd ~/pacbot_ws/task1a && python3 task_1a.py` |
| PB 1B | `cd ~/pacbot_ws/task1b && ./task_1b_launch` → `cd ~/pacbot_ws/task1b && python3 task_1b.py` |

If `./task_1a_launch` says "Permission denied": `chmod +x ./task_1a_launch`.

## Submission summary (Gauri uploads; videos Unlisted on YouTube)

| Task | Zip name | Zip contents (files at top level, **no folder**) | Video |
|---|---|---|---|
| KD 1A | `KD_4817.zip` | `KD_4817_task1a.py` | none |
| KD 1B | `KD_4817_task_1b.zip` | `task_1b_0.db3`, `metadata.yaml` (bag ≥ 60 s of `/pos_error` `/whycode_node/markers`) | `KD_4817_Task_1b` |
| KD 1C | `KD_4817_task_1c.zip` | `task_1c_0.db3`, `metadata.yaml` | `KD_4817_Task_1c` |
| PB 1A | `PB#4817.zip` | `result.yaml`, `task_1a.py` (from `./task_1a_launch --evaluate`) | link on portal |
| PB 1B | `PB#4817.zip` | `result.json`, `task_1b.py` (from `./task_1b_launch --evaluate`) | link on portal |

**Screen recording:** Ubuntu 22.04 uses Wayland; Kazam / SimpleScreenRecorder record a black screen. Use the team tool: `python3 ~/eyrc4817/learning/tools/screen_record.py PB_4817_Task1A` in its own terminal; **Ctrl+C there stops it**; the video lands in `~/Videos/Screencasts/`. (GNOME's Print Screen recorder also works, but on some themes its stop button is hidden and nothing else can stop it.) **Do a short test first.** Record one unbroken take with the terminal visible from the start. Keep videos online until results are published.

**Checker tool:** `python3 ~/eyrc4817/learning/tools/submission_check.py <kd1a|kd1b|kd1c|pb1a|pb1b> --file <your file> --zip <your zip>` checks names, coding standard, no GUI/input calls, results format, unchanged PacBot functions, and zip layout.

## e-Yantra Coding Standard (all submitted code)

**1. File header** at the top of the file:
```python
'''
# Team ID:          4817
# Theme:            Khoj-o-Drone          (or PacBot)
# Author List:      <names of team members who worked on this file>
# Filename:         <file name>
# Functions:        <comma-separated list of functions in this file>
# Global variables: <list of global variables, or None>
'''
```

**2. Every function** gets this block right after its `def` line:
```python
def example_function(image_path):
    '''
    Purpose:
    ---
    <what this function does>

    Input Arguments:
    ---
    `image_path` :  [ str ]
        <one-line description>

    Returns:
    ---
    `result` :  [ <type> ]
        <one-line description>

    Example call:
    ---
    example_function('image_1.jpg')
    '''
```

**3. Variable names** must describe the value (`table1_kp_val` ✔; `a`, `b`, `temp` ✘). If a name isn't self-explanatory, add `# name: what it holds` above it.

**4. Comments** on tricky or important parts: `# <what the code below does>`.

For PacBot, add these comments **without renaming or restructuring** the boilerplate's functions.

## Troubleshooting

| Problem | Cause → fix |
|---|---|
| `libmujoco.so.3.9.0: cannot open shared object file` | Old terminal or setup not run → open a new terminal; run `setup.sh --check` |
| `libglfw.so.3` not found / KD launch errors | `sudo apt install -y libglfw3-dev` |
| `numpy.core.multiarray failed to import` | numpy 2 installed → `python3 -m pip install --user "numpy<2"` |
| `cv2.aruco has no attribute ArucoDetector` | Code written for newer OpenCV → old API: `getPredefinedDictionary`, `DetectorParameters_create`, `detectMarkers` |
| Someone suggests `pip install opencv-python` | Don't: it breaks ROS 2's OpenCV (apt 4.5.4) |
| `ros2: command not found` | ROS not sourced → `source /opt/ros/humble/setup.bash` (setup adds it to `~/.bashrc`) |
| `Package 'swift_pico' not found` | Workspace not built or sourced → `cd ~/pico_ws && colcon build`, then `source install/setup.bash` |
| KD drone ignores new gains | Marker out of the camera view, or you didn't press Enter / −/+ in the tuner |
| `pico_mujoco_ws/install/setup.bash: No such file` in every terminal | Old line in `~/.bashrc` → re-run setup (it comments it out) or delete that line |
| PacBot: nothing moves | Start the simulator first · `systemctl status mosquitto` · topic name typo |
| `mosquitto`: address already in use | The broker already runs as a service. Don't start it again |
| PacBot misbehaves after a crash | A hard kill left a stale MQTT session → stop both programs with Ctrl+C and restart |
| Ubuntu "internal error" popup after stopping a ROS command | Harmless crash report → "Don't send"; stop programs with Ctrl+C |
| Screen recording is black / can't be stopped | Wayland → `learning/tools/screen_record.py` (Ctrl+C stops it) |
| Someone else's nodes in `ros2 node list` | Set `export ROS_LOCALHOST_ONLY=1` (setup adds it) or give each laptop a different `ROS_DOMAIN_ID` |
| Low disk space | Clear `~/.cache`, `sudo apt clean`; bag files and videos can be moved to another drive |
