# eYRC 2026-27 · Team 4817 · Khoj-o-Drone + PacBot

**Repo:** https://github.com/Saurabh0003M/eyrc4817-team-kit ·
**Portal:** [Khoj-o-Drone](https://portal.e-yantra.org/courses/theme_kd) · [PacBot](https://portal.e-yantra.org/courses/theme_pb) (login) ·
**Links:** [RESOURCES.md](RESOURCES.md) · **Study with ChatGPT:** [chatgpt-project/](chatgpt-project) · **⏰ Task 1 deadline: 23 September 2026**

```bash
git clone https://github.com/Saurabh0003M/eyrc4817-team-kit.git ~/eyrc4817
```

Everything the team needs to **set up**, **learn** (through our shared ChatGPT Project) and **check submissions** for e-Yantra Robotics
Competition 2026-27, Stage 1. Written for teammates who are new to ROS 2, PID, MuJoCo, OpenCV and MQTT.

> This repo contains **no e-Yantra competition files** (task PDFs, launch binaries, boilerplates) and
> **no graded solutions**. Those come from the portal and e-Yantra's GitHub repos, which `setup.sh`
> clones for you.

| Team | |
|---|---|
| Team ID | **4817** (used in every submission file name) |
| Themes | Khoj-o-Drone (primary) · PacBot (secondary). Both are carried until Task 2/3, then we pick one |
| Team Leader | **Gauri**: the only person who can upload submissions on the portal |
| Who owns which subtask | **Not decided yet**: agree it in the team chat, then note it in [`context/04-task-log.md`](context/04-task-log.md) |

---

## Contents

1. [First day (30 minutes)](#1-first-day-30-minutes)
2. [Setup: what the script checks and does](#2-setup-what-the-script-checks-and-does)
3. [Where everything lives on your laptop](#3-where-everything-lives-on-your-laptop)
4. [Task 1 at a glance](#4-task-1-at-a-glance)
5. [How to run each task](#5-how-to-run-each-task)
6. [Submission cheat sheet](#6-submission-cheat-sheet)
7. [Learning: where to start](#7-learning-where-to-start)
8. [Tools in this repo](#8-tools-in-this-repo)
9. [Troubleshooting](#9-troubleshooting)
10. [FAQ](#10-faq)
11. [Open questions to ask e-Yantra](#11-open-questions-to-ask-e-yantra)
12. [Updating, undoing, contributing](#12-updating-undoing-contributing)
13. [Team rules](#13-team-rules)
14. [What's in this repo](#14-whats-in-this-repo)

---

## 1. First day (30 minutes)

You need **Ubuntu 22.04 on bare metal** (not WSL, not 24.04) with **ROS 2 Humble**, i.e. e-Yantra **Task 0 done**.

```bash
git clone https://github.com/Saurabh0003M/eyrc4817-team-kit.git ~/eyrc4817
cd ~/eyrc4817
bash setup/setup.sh --check     # 1) look only: what you have, and what setup would change
bash setup/setup.sh             # 2) do it (asks for your password once; ~5–10 min the first time)
```

Then:

1. **Close the terminal and open a new one** so the new settings load.
2. Run `bash ~/eyrc4817/setup/setup.sh --check` again. It should end with *Everything is set up*.
3. Open the team's **ChatGPT Project** (Saurabh shares the link) and ask: *"I'm <name>. What's my subtask and what do I do today?"*. The same files are in [`chatgpt-project/`](chatgpt-project); start with `00_START_HERE.md`.
4. Agree with the team **who owns which Task 1 subtask** ([section 4](#4-task-1-at-a-glance)).
5. Open one simulator from [section 5](#5-how-to-run-each-task), just to see it start. Stop it with Ctrl+C.

If anything fails, send the team `~/eyrc4817-setup.log`.

---

## 2. Setup: what the script checks and does

**It checks before it changes anything.** `--check` changes nothing. A normal run installs **only what's
missing**, never deletes your files, and backs up `~/.bashrc` first. Safe to run again anytime.

| Stage | What it checks or does |
|---|---|
| **1. Your computer** | Ubuntu 22.04 · x86_64 · not WSL · not a virtual machine · RAM · ≥ 4 GB free disk · ROS 2 Humble desktop · GitHub reachable. **Stops before changing anything** if a hard requirement fails |
| **2. What's installed** | Each apt package · numpy (must be < 2) · paho-mqtt (≥ 2) · OpenCV · your MuJoCo Python version (never changed) · MuJoCo 3.9.0 library · both workspaces · leftover `~/pico_mujoco_ws` · `~/.bashrc` · MQTT broker. Each gets `[ok]`, `[todo]`, `[warn]` or `[!!]` |
| **3. Install** (skipped by `--check`) | apt: only the missing packages from `git zip curl python3-pip python3-venv python3-opencv python3-numpy python3-tk python3-yaml python3-matplotlib python3-reportlab libglfw3-dev ros-humble-actuator-msgs ros-humble-image-view ros-humble-rosbag2-storage-default-plugins python3-colcon-common-extensions mosquitto mosquitto-clients` · pip: `numpy<2`, `paho-mqtt>=2` only if needed · MuJoCo **3.9.0** library in `~/.local/share/eyrc4817/` only if not found · clones or updates **`~/pico_ws`** (branch `kd_sim`) and runs `colcon build` · clones or updates **`~/pacbot_ws`** and creates `task_1a.py` / `task_1b.py` from the boilerplates if missing · the `~/.bashrc` block · enables the `mosquitto` broker |
| **4. Verify** | OpenCV 4.5.x with the old ArUco API · numpy < 2 · `cv_bridge` · paho-mqtt · tkinter/yaml/matplotlib · the KD simulator finds all its libraries · KD controllers + PID tuner · PacBot launchers + task files · broker running |

**The `~/.bashrc` block** (between `# >>> eyrc4817 >>>` and `# <<< eyrc4817 <<<`) does four things:
- sources ROS 2 Humble and `~/pico_ws` in every terminal;
- adds the MuJoCo 3.9.0 library path (e-Yantra's KD simulator was built to look in a folder that only
  exists on their own computer);
- sets **`ROS_LOCALHOST_ONLY=1`**, so ROS 2 stays on your laptop and teammates' simulators on the same
  Wi-Fi don't interfere;
- comments out any old line that sources the deleted `~/pico_mujoco_ws`.

**Two MuJoCo versions on purpose:** PacBot's Task 0 uses MuJoCo **3.11.0** (Python); the Khoj-o-Drone
simulator needs the **3.9.0** library. Setup keeps both, and they don't clash.

---

## 3. Where everything lives on your laptop

```
~/eyrc4817/          ← this repo (docs, ChatGPT files, tools). Any folder works; ~/eyrc4817 is the suggestion
~/pico_ws/           ← Khoj-o-Drone workspace. Path fixed by e-Yantra; don't rename it
   src/swift_pico/scripts/   task1a.py + image_1.jpg   (KD Task 1A: write your code in task1a.py)
   src/swift_pico/src/       pid_values.yaml           (written by the PID tuner's "Save Values")
~/pacbot_ws/         ← PacBot workspace. Path fixed by e-Yantra
   task1a/   task_1a_launch · task_1a_boilerplate.py · task_1a.py   (PB Task 1A: edit task_1a.py)
   task1b/   task_1b_launch · task_1b_boilerplate.py · task_1b.py   (PB Task 1B: edit task_1b.py)
~/.local/share/eyrc4817/mujoco-3.9.0/   ← library for the KD simulator (made by setup if needed)
~/eyrc4817-setup.log                    ← setup log
~/.bashrc.eyrc4817-backup               ← your .bashrc before setup first touched it
```

> ⚠ The portal says `task_1a` / `task_1b`, but e-Yantra's repo uses **`task1a` / `task1b`**. Use the real folders.
> Some notes in `CLAUDE.md` and `context/` describe Saurabh's laptop (paths like `~/Desktop/e-yantra`,
> `drone_ws`, `_extracted/`). Those are not in this repo and you don't need them.

---

## 4. Task 1 at a glance

**Deadline: 23 September 2026** (confirm the exact time on the portal). Suggested owners and a day-by-day plan: [`chatgpt-project/00_START_HERE.md`](chatgpt-project/00_START_HERE.md).

| Theme | Part | What | Code or tune? | Marks | Study file | Full brief |
|---|---|---|---|---|---|---|
| Khoj-o-Drone | 1A | Find survivors in a photo → grid names like `D2` | write Python + OpenCV | 20 | [01](chatgpt-project/01_KD_Task1A_Survivor_Detection.md) | [context/09](context/09-task1-overview-and-1a.md) |
| Khoj-o-Drone | 1B | Drone holds a fixed height | tune 3 gains | 40 | [02](chatgpt-project/02_KD_Task1B_1C_PID_Tuning.md) | [context/10](context/10-task1b.md) |
| Khoj-o-Drone | 1C | Drone holds x and y too | tune pitch + roll gains | 40 | [02](chatgpt-project/02_KD_Task1B_1C_PID_Tuning.md) | [context/11](context/11-task1c.md) |
| PacBot | 1A | Grid maze: 2 pellets, then an exit, over MQTT | write Python (search + turn logic) | 35 | [03](chatgpt-project/03_PB_Task1A_Maze_Path_Planning.md) | [context/15](context/15-pacbot-task1.md) |
| PacBot | 1B | 3D maze wall following, 0 collisions | write Python + PID | 65 | [04](chatgpt-project/04_PB_Task1B_Wall_Following.md) | [context/15](context/15-pacbot-task1.md) |

Four of the five parts use **PID**, so everyone should watch the PID videos (list in `chatgpt-project/07_Learning_Resources.md`).

---

## 5. How to run each task

One **terminal per command**, in the order shown. Stop everything with **Ctrl+C** (never Ctrl+Z, never
close the window, never `kill -9`).

**KD 1A** (no simulator):
```bash
cd ~/pico_ws/src/swift_pico/scripts && python3 task1a.py --image image_1.jpg
```

**KD 1B / 1C** (three terminals):
```bash
ros2 launch swift_pico swift_pico_simulation.launch.py     # 1: simulator + camera view
ros2 run swift_pico task_1b_controller                      # 2: controller (task_1c_controller for 1C); answer Y to tune with the GUI
ros2 launch pid_tune pid_tune_drone.launch.py               # 3: tuner (Throttle card for 1B; Pitch + Roll for 1C)
```
Tuner facts:
- The value sent is number × scale (defaults Kp×0.03, Ki×0.008, Kd×0.6).
- **Gains are sent only when you press −/+ or Enter.**
- "Save Values" writes `~/pico_ws/src/swift_pico/src/pid_values.yaml`.
- If gains seem to do nothing, the drone's marker may be outside the camera view.

**PB 1A** (two terminals; the broker already runs as a service):
```bash
cd ~/pacbot_ws/task1a && ./task_1a_launch                   # 1: maze window
cd ~/pacbot_ws/task1a && python3 task_1a.py                 # 2: your code
mosquitto_sub -h localhost -t 'robot/pose' -t 'pellets/pose' -t 'bot/cmd' -v   # optional: watch messages
mosquitto_pub -h localhost -t robot/cmd_vel -m FRONT        # optional: drive one step by hand
```

**PB 1B** (two terminals):
```bash
cd ~/pacbot_ws/task1b && ./task_1b_launch                   # 1: MuJoCo maze
cd ~/pacbot_ws/task1b && python3 task_1b.py                 # 2: your code
```

---

## 6. Submission cheat sheet

Always run `learning/tools/submission_check.py` first. Only **Gauri** can upload. Videos go on YouTube as **Unlisted** (not Private), recorded in **one unbroken take** with the terminal visible from the start.

| Part | Run it for real | Upload (zip = files at top level, **no folder**) | Video title |
|---|---|---|---|
| KD 1A | rename your script to `KD_4817_task1a.py`; no `imshow` / `waitKey` / `input()` | `KD_4817.zip` → `KD_4817_task1a.py` | none |
| KD 1B | sim → `task_1b_controller` (answer **N**, type your gains) → `ros2 bag record -o task_1b /pos_error /whycode_node/markers` for ≥ 60 s | `KD_4817_task_1b.zip` → `task_1b_0.db3`, `metadata.yaml` | `KD_4817_Task_1b` |
| KD 1C | sim → tuner → `task_1c_controller` → `ros2 bag record -o task_1c /pos_error /whycode_node/markers` for ≥ 60 s | `KD_4817_task_1c.zip` → `task_1c_0.db3`, `metadata.yaml` | `KD_4817_Task_1c` |
| PB 1A | recording on → `./task_1a_launch --evaluate` → `python3 task_1a.py` | `PB#4817.zip` → `result.yaml`, `task_1a.py` | unlisted link on portal |
| PB 1B | recording on → `./task_1b_launch --evaluate` → `python3 task_1b.py` | `PB#4817.zip` → `result.json`, `task_1b.py` | unlisted link on portal |

Zip the files, not the folder. Example: `cd task_1b && zip -r KD_4817_task_1b.zip task_1b_0.db3 metadata.yaml`.

---

## 7. Learning: where to start

| You want to… | Open |
|---|---|
| **Ask questions, learn, get unstuck** | The team **ChatGPT Project** (it has all the files below as context) |
| Read **your subtask in plain words** | [`chatgpt-project/`](chatgpt-project): `00_START_HERE` (team, plan) · `01` KD 1A · `02` KD 1B/1C · `03` PB 1A · `04` PB 1B · `05` setup/run/submit · `06` concepts · `07` links · `08` portal learnings |
| Find **any link** the portal gave (videos, docs, playlists) | **[`RESOURCES.md`](RESOURCES.md)**: grouped like the portal, tagged by subtask, ⭐ = start here |
| Look up a **word** (PID, topic, broker, HSV…) | [`chatgpt-project/06_Concepts_Explained.md`](chatgpt-project/06_Concepts_Explained.md) |
| Read the **exact task rules**, traps and scoring | [context/09](context/09-task1-overview-and-1a.md)–[11](context/11-task1c.md) (KD), [context/15](context/15-pacbot-task1.md) (PacBot) |
| See what the **learning pages say** + portal mistakes we found | [context/12](context/12-learnings-control-systems.md) control · [13](context/13-learnings-quad-control-imgproc-coding.md) quad control, OpenCV, coding standard · [14](context/14-learnings-pacbot-mqtt-pathplanning.md) MQTT, path planning · [06](context/06-prelearnings.md) ROS 2, MuJoCo, quadcopters |

**Using ChatGPT for graded tasks:** it's set up to teach, review and debug, **not** to write the whole answer file, because e-Yantra plagiarism-checks every submission and all four of us use the same project.

---

## 8. Tools in this repo

All in `learning/tools/`, run from the repo folder. None of them solves a task; they measure and check.

| Tool | Use it for | Example |
|---|---|---|
| `pixel_detective.py` | Click the photo → see BGR and HSV numbers (KD 1A) | `python3 learning/tools/pixel_detective.py` |
| `hsv_tuner.py` | Sliders → see which pixels a colour range keeps (KD 1A) | `python3 learning/tools/hsv_tuner.py` |
| `kd1a_testbench.py` | Runs **your** KD 1A script on 10 harder arena versions; answers must stay the same (KD 1A) | `python3 learning/tools/kd1a_testbench.py --script ~/pico_ws/src/swift_pico/scripts/task1a.py` |
| `submission_check.py` | Before upload: names, **coding standard**, blocking calls, results format, PacBot functions unchanged, zip layout | `python3 learning/tools/submission_check.py pb1a --file ~/pacbot_ws/task1a/task_1a.py` |
| `bag_score.py` | Estimate KD 1B/1C marks from a practice bag (assumptions in the file) | `python3 learning/tools/bag_score.py 1b task_1b` |
| `toy_drone.py` | Plain-Python PID playground; you write the controller (PID practice) | `python3 learning/tools/toy_drone.py --kp 20` |
| `check_links.py` | Check every link in these docs still works | `python3 learning/tools/check_links.py` |

---

## 9. Troubleshooting

| You see | Cause → fix |
|---|---|
| `libmujoco.so.3.9.0: cannot open shared object file` | Old terminal, or setup not run → open a **new terminal**; run `setup.sh --check` |
| `numpy.core.multiarray failed to import` (from `cv_bridge`) | numpy 2 → `python3 -m pip install --user "numpy<2"` |
| `module 'cv2.aruco' has no attribute 'ArucoDetector'` | Tutorial for newer OpenCV → old API: `cv2.aruco.getPredefinedDictionary`, `DetectorParameters_create`, `detectMarkers` |
| Tempted to `pip install opencv-python` | **Don't.** It breaks ROS 2's OpenCV. OpenCV comes from `apt` (4.5.4) |
| KD drone ignores your gains | Marker outside the camera view, or you didn't press Enter / −/+ in the tuner |
| PacBot: nothing moves | Start the launcher **before** your code · `systemctl status mosquitto` · topic name typo |
| PacBot acts strangely after a crash | A hard-killed process left a stale MQTT session → restart both with Ctrl+C |
| `pico_mujoco_ws/install/setup.bash: No such file` in every terminal | Old bonus-task line in `~/.bashrc` → re-run `setup.sh` (it comments that line out) |
| Ubuntu "internal error" popup after stopping a ROS tool | Harmless crash report → click Don't send; stop tools with Ctrl+C |
| Screen recording is black | Wayland → Ubuntu's built-in recorder (Print Screen → video), OBS, or log in with "Ubuntu on Xorg". **Test a 2-minute recording first** |
| Someone else's ROS nodes in `ros2 node list` | `ROS_LOCALHOST_ONLY` not set → re-run setup, open a new terminal |
| `setup.sh` says `[!!] ... exists but is not the git clone` | You made that folder by hand → rename it (e.g. `mv ~/pico_ws ~/pico_ws.old`) and re-run |

---

## 10. FAQ

**I'm on Windows / WSL / a VM.** e-Yantra requires bare-metal Ubuntu 22.04; its evaluators reject WSL.
Dual-boot is the way (see e-Yantra Task 0).

**I already did Task 0 and the bonus task my own way. Will setup break it?** No. It never deletes or
renames your folders, never changes your MuJoCo Python version, and only adds a marked block to
`~/.bashrc` (after a backup). If an existing `~/pico_ws` or `~/pacbot_ws` isn't the e-Yantra git clone,
it stops and tells you.

**Do I need both themes?** Yes, until the team commits to one (from Task 2/3). Everyone learns both;
each person owns specific subtasks.

**Where do I write my code?** KD 1A: `~/pico_ws/src/swift_pico/scripts/task1a.py`. PB 1A/1B:
`~/pacbot_ws/task1a/task_1a.py`, `~/pacbot_ws/task1b/task_1b.py`. KD 1B/1C: no code, only gains.
**Never** put solution code in this repo.

**Who made these notes?** Saurabh, with an AI assistant (Claude); the `CLAUDE.md` file is its index. Teammates use the ChatGPT Project.

---

## 11. Open questions to ask e-Yantra

Post these on the e-Yantra forum; the portal doesn't answer them, or contradicts itself:

1. **Exact deadline time** on 23 September (both themes).
2. **KD 1A results file:** 3 lines or 4? The instruction page shows a blank line 2; the submission page says "exactly three lines".
3. **KD 1A marker IDs:** always 80, 85, 90, 95 in the hidden test images? The submission example shows 10, 15, 20, 25.
4. **KD 1B/1C scoring:** when does the clock start? Are "hover seconds" continuous or cumulative?
5. **Theme commitment:** from Task 2 or Task 3? Two e-Yantra documents disagree.
6. **PacBot:** 1A and 1B both use `PB#<team_id>.zip`. Confirm they go in separate slots.

---

## 12. Updating, undoing, contributing

**Get the latest docs, tools and e-Yantra updates:**
```bash
cd ~/eyrc4817 && git pull && bash setup/setup.sh
```
(`setup.sh` also runs `git pull` on `~/pico_ws` and `~/pacbot_ws` and rebuilds.)

**Undo setup** (nothing else on your system is touched):
```bash
cp ~/.bashrc.eyrc4817-backup ~/.bashrc          # restore your old .bashrc (or delete just the eyrc4817 block)
rm -rf ~/.local/share/eyrc4817                  # remove the MuJoCo 3.9.0 library folder
sudo systemctl disable --now mosquitto          # stop the MQTT broker from auto-starting
```
The workspaces `~/pico_ws` and `~/pacbot_ws` are e-Yantra's normal task folders; keep them.

**Contribute:** ask Saurabh to add you as a collaborator (GitHub → Settings → Collaborators). Then:
`git pull` → edit → `git status` (**check no solution files**) → `git add <files>` → `git commit -m "…"` → `git push`.

---

## 13. Team rules

- **This repo is public. Never commit graded solution code** (`task1a.py`, `task_1a.py`, `task_1b.py`,
  `KD_4817_*`, results, zips). Other teams could copy it, and **our** submission would then fail the
  plagiarism check. `.gitignore` blocks the usual names; still run `git status` before every commit.
- **Never commit e-Yantra's files** (their IP): theme docs, portal PDFs, launch binaries, boilerplates.
- **Never open, decompile or modify** the PacBot `task_1*_launch` binaries (tamper rule = disqualification).
- **Follow the e-Yantra coding standard** in every submitted file (header block + Purpose / Input Arguments /
  Returns / Example call under each function). `submission_check.py` checks it.
- **PacBot:** never rename or restructure the boilerplate's functions.

---

## 14. What's in this repo

| Path | What |
|---|---|
| [`README.md`](README.md) | This page |
| [`RESOURCES.md`](RESOURCES.md) | Every learning link from the portal, tagged by subtask |
| [`chatgpt-project/`](chatgpt-project) | The files + instructions for the team's ChatGPT Project (see `HOW_TO_CREATE_THE_PROJECT.md`) |
| [`setup/setup.sh`](setup/setup.sh) | Laptop setup + checker |
| [`learning/tools/`](learning/tools) | The tools in [section 8](#8-tools-in-this-repo) |
| [`CLAUDE.md`](CLAUDE.md) | Index of the team notes (written for the AI assistant, but readable) |
| [`context/`](context) | Task briefs, setup findings, learning-material analysis, task log |
