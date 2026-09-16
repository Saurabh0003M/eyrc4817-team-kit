# eYRC 2026-27 · Team 4817 · Khoj-o-Drone + PacBot

Team kit for e-Yantra Robotics Competition 2026-27: setup script, learning roadmap, notes and small
learning tools. **This repo contains no e-Yantra competition files and no graded solutions.**

## Quick start (teammates)

Requirements: **Ubuntu 22.04 on bare metal** with **ROS 2 Humble** installed (Task 0 done).

```bash
git clone <THIS-REPO-URL> ~/eyrc4817
cd ~/eyrc4817
bash setup/setup.sh          # installs + configures everything; asks for your sudo password
bash setup/setup.sh --check  # later: verify only, changes nothing
```

Open a **new terminal** afterwards so the `~/.bashrc` changes load.

What `setup.sh` does:

| Step | Details |
|---|---|
| apt packages | `python3-opencv python3-numpy libglfw3-dev ros-humble-actuator-msgs ros-humble-image-view mosquitto mosquitto-clients zip git python3-venv python3-pip python3-colcon-common-extensions` |
| pip (user) | `numpy<2` (ROS 2 Humble's `cv_bridge` breaks on numpy 2), `paho-mqtt` |
| MuJoCo 3.9.0 library | a private venv in `~/.local/share/eyrc4817/mujoco-3.9.0`. The Khoj-o-Drone simulator binary needs `libmujoco.so.3.9.0` and looks for it in a path that exists only on e-Yantra's own machine. Your Python MuJoCo (PacBot's 3.11.0) is **not** touched |
| Khoj-o-Drone workspace | clones `eYRC_26-27_Khojo-Drone` (branch `kd_sim`, with submodules) into `~/pico_ws`, runs `colcon build` |
| PacBot workspace | clones `eYRC_26-27_PacBot` into `~/pacbot_ws`, copies each `task_1*_boilerplate.py` to `task_1*.py` if missing |
| `~/.bashrc` | one marked block (`# >>> eyrc4817 >>>`): sources ROS 2 + `~/pico_ws`, adds the MuJoCo 3.9.0 library path |
| MQTT broker | `mosquitto` enabled and started (localhost only) |
| Verification | OpenCV version + old ArUco API, numpy < 2, `cv_bridge`, paho-mqtt, simulator libraries, broker, task files |

## What's in here

| Path | What |
|---|---|
| `LEARNING-ROADMAP.pdf` | Learning roadmap for both themes: modules per Task 1 subtask, video ladders, experiments, dictionary (source in `learning/source/`) |
| `CLAUDE.md`, `context/` | Team notes: task briefs, setup findings, traps, learning-material analysis |
| `learning/tools/` | Learning aids and checkers, none of which solve a task: `pixel_detective.py` (click → BGR/HSV), `hsv_tuner.py` (sliders → colour mask), `toy_drone.py` (plain-Python PID playground; you write the controller), `kd1a_testbench.py` (runs your KD 1A script on tilted/darker/blurred arenas and checks the answers stay consistent), `submission_check.py` (file names, coding standard, blocking calls, results format, PacBot boilerplate signatures, zip structure), `bag_score.py` (estimates KD 1B/1C marks from a practice bag) |
| `setup/setup.sh` | The setup script above |

## Rules we follow

- **Never commit** e-Yantra's files (theme docs, launch binaries, boilerplates) or **our graded
  solutions** while this repo is public. `.gitignore` blocks the usual file names; check `git status`
  before every commit.
- **Never open, decompile or modify** the PacBot `task_1*_launch` binaries (e-Yantra tamper rule).
- Stop simulators with **Ctrl+C**, not Ctrl+Z or a hard kill.
