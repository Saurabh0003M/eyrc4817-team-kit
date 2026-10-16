# eYRC 2026-27 · Team 4817 · Khoj-o-Drone + PacBot

**Repo:** https://github.com/Saurabh0003M/eyrc4817-team-kit ·
**Portal:** [Khoj-o-Drone](https://portal.e-yantra.org/courses/theme_kd) · [PacBot](https://portal.e-yantra.org/courses/theme_pb) (login) ·
**e-Yantra's GitHub repos:** [Khoj-o-Drone](https://github.com/eYantra-Robotics-Competition/eYRC_26-27_Khojo-Drone) · [PacBot](https://github.com/eYantra-Robotics-Competition/eYRC_26-27_PacBot) ([section 4](#4-e-yantras-github-repos)) ·
**Links:** [RESOURCES.md](RESOURCES.md) · **Study with ChatGPT:** [chatgpt-project/](chatgpt-project) · **✅ Task 2 done: KD 100/100 · PB 93.60/100** · **⏰ Task 3: 27 Oct – 16 Nov 2026** (ends Stage 1)

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
3. [Where everything lives on your laptop](#3-where-everything-lives-on-your-laptop-and-why)
4. [e-Yantra's GitHub repos](#4-e-yantras-github-repos)
5. [Tasks at a glance (Task 1, Task 2, results)](#5-tasks-at-a-glance)
6. [How to run each task](#6-how-to-run-each-task)
7. [Submission cheat sheet](#7-submission-cheat-sheet)
8. [Learning: where to start](#8-learning-where-to-start)
9. [Tools in this repo](#9-tools-in-this-repo)
10. [Troubleshooting](#10-troubleshooting)
11. [FAQ](#11-faq)
12. [Open questions to ask e-Yantra](#12-open-questions-to-ask-e-yantra)
13. [Updating, undoing, contributing](#13-updating-undoing-contributing)
14. [Team rules](#14-team-rules)
15. [What's in this repo](#15-whats-in-this-repo)

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
4. Agree with the team **who owns which Task 1 subtask** ([section 5](#5-tasks-at-a-glance)).
5. Open one simulator from [section 6](#6-how-to-run-each-task), just to see it start. Stop it with Ctrl+C.

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

## 3. Where everything lives on your laptop (and why)

Three places, three jobs (`~` = your home folder):

```
~/eyrc4817/     the KIT = this repo: notes, study files, tools, setup script (any folder works; ~/eyrc4817 is the suggestion)
~/pico_ws/      the Khoj-o-Drone WORKSHOP: a ROS 2 workspace (drone simulator + your KD code). Path fixed by e-Yantra
~/pacbot_ws/    the PacBot WORKSHOP: e-Yantra's PacBot download (games + your PB code). Path fixed by e-Yantra
```

**Why the workshops are separate from the kit:** e-Yantra's commands (and every teammate's laptop) use exactly
`~/pico_ws` and `~/pacbot_ws`, so commands can be copy-pasted. And ROS 2's build tool **colcon** writes the workspace's
full path into what it builds: move or rename `~/pico_ws` and it breaks, and a space in a folder name breaks the build.
Leave both where setup puts them.

### The kit: `~/eyrc4817/`

```
README.md          this page
RESOURCES.md       every portal learning link, tagged by subtask
CLAUDE.md          briefing for AI assistants: an index of everything (describes Saurabh's laptop)
chatgpt-project/   instructions + files for the team's ChatGPT project
context/           detailed notes, one file per topic; 04-task-log.md is the team diary
learning/tools/    helper programs: submission checker, KD 1A testbench, screen recorder, …
setup/setup.sh     the one-command installer (section 2)
.gitignore         decides what may be shared here (never solution files)
```

### The KD workshop: `~/pico_ws/` (a ROS 2 workspace)

Every ROS 2 workspace has the same four folders:

```
~/pico_ws/
├── src/       "source" = the code. The ONLY folder people edit
├── build/     colcon's workbench while building – ignore it
├── install/   the finished, runnable result. `source ~/pico_ws/install/setup.bash` (setup puts it in ~/.bashrc)
│              tells ROS 2 to look here – that's why `ros2 launch swift_pico …` works from any folder
└── log/       build diaries – read them when `colcon build` fails
```

**`src` is short for "source code".** It holds **packages**: one folder each, with a `package.xml` "ID card" (name + what it needs):

```
src/
├── swift_pico/               ← the one you work in
│   ├── scripts/              Python programs + task files: task1a.py (KD 1A starter), image_1.jpg
│   ├── src/                  the package's own "src": e-Yantra's ready-made task_1b_controller and
│   │                         task_1c_controller; the tuner's "Save Values" writes pid_values.yaml here
│   ├── launch/               start-up recipes: one command starts several programs
│   ├── config/               settings files
│   ├── package.xml           ID card
│   └── CMakeLists.txt        build instructions for colcon
├── swift_pico_description/   the drone's 3D model
├── rotors_simulator/         simulator machinery, incl. e-Yantra's attitude controller
├── mav_comm/                 message formats for drone commands
├── controller_tuner/         the tuning window (its package is called pid_tune)
└── whycode-ros2/             tracks the marker on the drone → gives its position
```

Rule of thumb: programs started with `ros2 run` / `ros2 launch` are taken from `install/`, so after editing one in
`src/`, run `colcon build` in `~/pico_ws`. Files you start directly (`python3 task1a.py …`) need no rebuild.

### The PacBot workshop: `~/pacbot_ws/` (e-Yantra's download, not a ROS workspace)

Every task folder follows one pattern:

```
~/pacbot_ws/
├── task1a/   task_1a_launch          the maze game – e-Yantra's, encrypted: only run it, never open or edit it
│             task_1a_boilerplate.py  the empty template
│             task_1a.py              YOUR code (the bot's brain); starts as a copy of the template
│             result.yaml             written by the game in --evaluate mode (goes into the zip)
├── task1b/   task_1b_launch · task_1b_boilerplate.py · task_1b.py   (+ lib/, meshes/ the game needs – don't touch)
├── task2a/   task_2a_launch · task_2a_boilerplate.py   (Task 2: you write INTO the boilerplate file; it is the submitted file)
└── task2b/   task_2b_launch · task_2b_boilerplate.py · maze_2b.py (the maze the boilerplate imports – don't edit)
```

Submission zips are made inside the task folder, next to the files they contain.

### Other files setup creates

```
~/.local/share/eyrc4817/mujoco-3.9.0/   library for the KD simulator (made by setup if needed)
~/eyrc4817-setup.log                    setup log
~/.bashrc.eyrc4817-backup               your .bashrc before setup first touched it
```

**Finding things fast:** in the Files app or any upload/attach window, press **Ctrl+L**, type a path
(e.g. `~/pacbot_ws/task1a/`) and press Enter.

> ⚠ The portal says `task_1a` / `task_1b`, but e-Yantra's repo uses **`task1a` / `task1b`**. Use the real folders.
> On Saurabh's laptop the kit folder is `~/Desktop/e-yantra`; it also holds private portal downloads and
> shortcuts (symlinks) to the workspaces, and notes in `CLAUDE.md` / `context/` use those paths. Same idea, different place.

---

## 4. e-Yantra's GitHub repos

e-Yantra publishes every task's **simulator, launchers and boilerplate code** in two public GitHub repos. Marks, deadlines,
rules and the submission format are **only on the portal**: the repos never state them. `setup.sh` clones both for you.

| Theme | Repo | On your laptop | Branch | What's in it |
|---|---|---|---|---|
| **Khoj-o-Drone** | [eYantra-Robotics-Competition/eYRC_26-27_Khojo-Drone](https://github.com/eYantra-Robotics-Competition/eYRC_26-27_Khojo-Drone) | `~/pico_ws/src` | **`kd_sim`** (also `turtle_sim` = Task 0 bonus, `main`) | the Swift Pico drone simulator (MuJoCo), WhyCon marker tracking, PID tuner, and each task's boilerplate in `swift_pico/src/` (Task 2: `pico_controller_PID/LQR`, `waypoint_service`, `pico_client`, `pico_server`) |
| **PacBot** | [eYantra-Robotics-Competition/eYRC_26-27_PacBot](https://github.com/eYantra-Robotics-Competition/eYRC_26-27_PacBot) | `~/pacbot_ws` | `main` | one folder per task (`task0`, `task1a`, `task1b`, `task2a`, `task2b`): an encrypted launcher (**run only**, never open it), the boilerplate, and the files it needs |

Also public, no login: e-Yantra's [theme site](https://themes.e-yantra.org/) (task pages and timelines; PacBot had its own pages there).
The organisation page lists every e-Yantra repo: [github.com/eYantra-Robotics-Competition](https://github.com/eYantra-Robotics-Competition).

**New tasks arrive through these repos** (Task 3 opens 27 Oct). To get them:
```bash
git -C ~/pico_ws/src pull --ff-only && cd ~/pico_ws && colcon build     # Khoj-o-Drone (plain build, no --symlink-install)
git -C ~/pacbot_ws pull --ff-only                                       # PacBot
```
If `git pull` refuses because you edited one of e-Yantra's files, save your work first: `git stash`, pull, `git stash pop`.
Our own files in those folders are untracked, so a pull never touches them. Last checked 2026-10-17: nothing new after
Task 2 (KD `af3b062`, PB `a5fad58`).

---

## 5. Tasks at a glance

**Results so far (portal):** Task 1 full marks on both themes · **Task 2: Khoj-o-Drone 100.00/100 · PacBot 93.60/100**.

### Task 1 (16 Sep → 5 Oct, done)

| Theme | Part | What | Code or tune? | Marks | Study file | Full brief |
|---|---|---|---|---|---|---|
| Khoj-o-Drone | 1A | Find survivors in a photo → grid names like `D2` | write Python + OpenCV | 20 | [01](chatgpt-project/01_KD_Task1A_Survivor_Detection.md) | [context/09](context/09-task1-overview-and-1a.md) |
| Khoj-o-Drone | 1B | Drone holds a fixed height | tune 3 gains | 40 | [02](chatgpt-project/02_KD_Task1B_1C_PID_Tuning.md) | [context/10](context/10-task1b.md) |
| Khoj-o-Drone | 1C | Drone holds x and y too | tune pitch + roll gains | 40 | [02](chatgpt-project/02_KD_Task1B_1C_PID_Tuning.md) | [context/11](context/11-task1c.md) |
| PacBot | 1A | Grid maze: 2 pellets, then an exit, over MQTT | write Python (search + turn logic) | 35 | [03](chatgpt-project/03_PB_Task1A_Maze_Path_Planning.md) | [context/15](context/15-pacbot-task1.md) |
| PacBot | 1B | 3D maze wall following, 0 collisions | write Python + PID | 65 | [04](chatgpt-project/04_PB_Task1B_Wall_Following.md) | [context/15](context/15-pacbot-task1.md) |

Four of the five parts use **PID**, so everyone should watch the PID videos (list in `chatgpt-project/07_Learning_Resources.md`).

### Task 2 (6 → 26 Oct, done)

| Theme | Part | What | Marks | Our score | Full brief |
|---|---|---|---|---|---|
| Khoj-o-Drone | 2A | Write your own position controller (PID): hold the drone at (1.5, −1.5, 13) | 20 | **20** (uploaded late, accepted) | [context/17](context/17-task2-portal.md) |
| Khoj-o-Drone | 2B | ROS 2 **service + action**: fly 4 fixed waypoints in order, hold each 3 s | 40 | **40** | [context/17](context/17-task2-portal.md) |
| Khoj-o-Drone | 2C | Waypoints from the **camera**: detect the critical survivors (Task 1A detector), plan a route, fly it | 40 | **40** | [context/17](context/17-task2-portal.md) |
| PacBot | 2A | MuJoCo maze: random spawn, one pellet, exit, **no live position** (dead reckoning from gyro + encoders) | 30 | **30** | [context/17](context/17-task2-portal.md) |
| PacBot | 2B | 3 pellets + a **ghost** that patrols one of them (touching it = 0); **time counts** | 70 | **63.60** | [context/17](context/17-task2-portal.md) |

**Why PB 2B can't reach 70:** its score is 5 × pellets + (55 − 0.085 × seconds), so every second costs 0.085 marks and
the full 70 would need a 0-second run. Ours: 3/3 pellets, 0 collisions, **75.28 s**. Each PacBot run draws new random
pellets, so we recorded several runs and uploaded the fastest clean one.

How the recordings were made, one command each: [context/18-task2-submission-runbook.md](context/18-task2-submission-runbook.md).
Day-by-day story of what worked and what didn't: [`context/04-task-log.md`](context/04-task-log.md).

---

## 6. How to run each task

One **terminal per command**, in the order shown. Stop everything with **Ctrl+C** (never Ctrl+Z, never
close the window, never `kill -9`). **Exception: the PacBot game windows ignore Ctrl+C: press `q` in the maze window**
(if it still won't close: `pkill -x task_1a_launch`).

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
cd ~/pacbot_ws/task1a && ./task_1a_launch                   # 1: maze window (add --evaluate for the recorded run)
cd ~/pacbot_ws/task1a && python3 task_1a.py                 # 2: your code - the bot moves ONLY while this runs
mosquitto_sub -h localhost -t 'robot/pose' -t 'pellets/pose' -t 'bot/cmd' -v   # optional: watch messages
mosquitto_pub -h localhost -t robot/cmd_vel -m FRONT        # optional: drive one step by hand
```

PacBot lessons from our 1A run:
- Start the launcher **from a terminal, never by double-clicking it** in Files: it then runs without `--evaluate`,
  without a terminal, and with nothing driving the bot.
- **One maze at a time.** Two mazes (or two `task_1a.py`) share the same MQTT names and fight: the bot freezes.
  Close old ones with `q` before starting again.
- With `--evaluate` the maze terminal prints `evaluation ended → result.yaml (N commands, M rejected)` when the run is
  over. `result.yaml` is written once at the start (small) and again at the end (full): **zip only after the end**.

**PB 1B** (two terminals):
```bash
cd ~/pacbot_ws/task1b && ./task_1b_launch                   # 1: MuJoCo maze
cd ~/pacbot_ws/task1b && python3 task_1b.py                 # 2: your code
```

**Task 2, practice runs** (nothing is written; one terminal per line):
```bash
# PacBot 2A / 2B
cd ~/pacbot_ws/task2a && ./task_2a_launch                   # 1: MuJoCo maze (task2b: ./task_2b_launch)
cd ~/pacbot_ws/task2a && python3 task_2a_boilerplate.py     # 2: your code (task2b: task_2b_boilerplate.py)

# Khoj-o-Drone 2B / 2C (order matters: the server starts the flight)
ros2 launch swift_pico swift_pico_simulation.launch.py      # 1: simulator
ros2 run swift_pico waypoint_service                        # 2: hands out the waypoints
ros2 run swift_pico pico_client                             # 3: asks for them, sends them one by one
ros2 run swift_pico pico_server                             # 4: flies each one
```
KD 2A is one node instead: `ros2 run swift_pico pico_controller_PID.py` after the simulator.
**After editing anything in `~/pico_ws/src`, run `colcon build`**: `ros2 run` uses the built copy.

**Task 2, recorded runs: one command does it all** (screen recording, the runs in the right order, a practice score,
and the upload zip). Run them from a normal terminal (**Ctrl+Alt+T**), not from an editor's built-in terminal:
```bash
python3 ~/eyrc4817/learning/tools/pb_record.py --task 2b    # PacBot (or --task 2a)
~/eyrc4817/learning/tools/kd_record.sh 2c                   # Khoj-o-Drone (or 2a, 2b)
```

---

## 7. Submission cheat sheet

Always run `learning/tools/submission_check.py` first. Only **Gauri** can upload. Videos go on YouTube as **Unlisted** (not Private), recorded in **one unbroken take** with the terminal visible from the start. Record with `learning/tools/screen_record.py` (section 9). PacBot's pages give no video title; we used `PB_4817_Task_1a` (no `#`: YouTube turns it into a hashtag).

| Part | Run it for real | Upload (zip = files at top level, **no folder**) | Video title |
|---|---|---|---|
| KD 1A | rename your script to `KD_4817_task1a.py`; no `imshow` / `waitKey` / `input()` | `KD_4817.zip` → `KD_4817_task1a.py` | none |
| KD 1B | sim → `task_1b_controller` (answer **N**, type your gains) → `ros2 bag record -o task_1b /pos_error /whycode_node/markers` for ≥ 60 s | `KD_4817_task_1b.zip` → `task_1b_0.db3`, `metadata.yaml` | `KD_4817_Task_1b` |
| KD 1C | sim → tuner → `task_1c_controller` → `ros2 bag record -o task_1c /pos_error /whycode_node/markers` for ≥ 60 s | `KD_4817_task_1c.zip` → `task_1c_0.db3`, `metadata.yaml` | `KD_4817_Task_1c` |
| PB 1A | recording on → `./task_1a_launch --evaluate` → `python3 task_1a.py` | `PB#4817.zip` → `result.yaml`, `task_1a.py` | unlisted link on portal |
| PB 1B | recording on → `./task_1b_launch --evaluate` → `python3 task_1b.py` | `PB#4817.zip` → `result.json`, `task_1b.py` | unlisted link on portal |
| KD 2A | `kd_record.sh 2a` (sim → bag with `/pos_error` → controller, 75 s) | `KD_4817_task_2a.zip` → `KD_4817_task_2a.py`, `task_2a_0.db3`, `metadata.yaml` | `KD_4817_Task_2a` |
| KD 2B | `kd_record.sh 2b` (sim → service → client → bag → server) | `KD_4817_task_2b.zip` → `KD_4817_waypoint_service.py`, `KD_4817_pico_client.py`, `KD_4817_pico_server.py`, `task_2b_0.db3`, `metadata.yaml` | `KD_4817_Task_2b` |
| KD 2C | `kd_record.sh 2c` (same order as 2B) | `KD_4817_task_2c.zip` → same 5 files, `task_2c_0.db3` | `KD_4817_Task_2c` |
| PB 2A | `pb_record.py --task 2a` (`./task_2a_launch --evaluate` → your code) | `PB#4817.zip` → `result.json`, `task_2a_boilerplate.py` | unlisted link on portal |
| PB 2B | `pb_record.py --task 2b`; **re-run until "0 collisions · OK to submit"**, keep the fastest | `PB#4817.zip` → `result.json`, `task_2b_boilerplate.py` | unlisted link on portal |

Zip the files, not the folder. Example: `cd task_1b && zip -r KD_4817_task_1b.zip task_1b_0.db3 metadata.yaml`.

**Every PacBot zip is called `PB#4817.zip`.** Upload from the right task folder (`task2a` vs `task2b`): a 2A zip in the 2B
slot scores 0. `pb_record.py` moves the previous zip out to `~/pb2b_trials/` (`~/pb2a_trials/`) so the task folder only
ever holds the newest one, and its last line names the matching video. **Never open or edit `result.json`** (it is sealed).
Re-uploading replaces the earlier upload, so only upload a run that is better.

---

## 8. Learning: where to start

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

## 9. Tools in this repo

All in `learning/tools/`, run from the repo folder. None of them solves a task; they measure and check.

| Tool | Use it for | Example |
|---|---|---|
| `pixel_detective.py` | Click the photo → see BGR and HSV numbers (KD 1A) | `python3 learning/tools/pixel_detective.py` |
| `hsv_tuner.py` | Sliders → see which pixels a colour range keeps (KD 1A) | `python3 learning/tools/hsv_tuner.py` |
| `kd1a_testbench.py` | Runs **your** KD 1A script on 10 harder arena versions; answers must stay the same (KD 1A) | `python3 learning/tools/kd1a_testbench.py --script ~/pico_ws/src/swift_pico/scripts/task1a.py` |
| `submission_check.py` | Before upload: names, **coding standard**, blocking calls, results format, PacBot functions unchanged, zip layout | `python3 learning/tools/submission_check.py pb1a --file ~/pacbot_ws/task1a/task_1a.py` |
| `bag_score.py` | Estimate KD 1B/1C/2A marks from a practice bag (assumptions in the file) | `python3 learning/tools/bag_score.py 2a task_2a` |
| `kd2_bag_score.py` | Estimate KD 2B/2C marks from a bag: each waypoint's reach + 3 s hold, and speed | `python3 learning/tools/kd2_bag_score.py 2b task_2b client.log` |
| `kd_record.sh` | **KD 2A/2B/2C recorded run in one command**: recording → sim → nodes in order → bag → stop on success → score → upload zip in `~/kd_upload_<task>/` (`--no-video` = rehearsal) | `learning/tools/kd_record.sh 2b` |
| `pb_record.py` | **PacBot 1B/2A/2B recorded run in one command**: two terminals, recording, `--evaluate`, verdict ("0 collisions · OK to submit" or "do NOT submit"), zip made on camera | `python3 learning/tools/pb_record.py --task 2b` |
| `toy_drone.py` | Plain-Python PID playground; you write the controller (PID practice) | `python3 learning/tools/toy_drone.py --kp 20` |
| `check_links.py` | Check every link in these docs still works | `python3 learning/tools/check_links.py` |
| `screen_record.py` | Record the whole screen for task videos (works on Wayland). **Ctrl+C in its terminal stops it**; video → `~/Videos/Screencasts/` | `python3 learning/tools/screen_record.py PB_4817_Task1A` |

---

## 10. Troubleshooting

| You see | Cause → fix |
|---|---|
| `libmujoco.so.3.9.0: cannot open shared object file` | Old terminal, or setup not run → open a **new terminal**; run `setup.sh --check` |
| `numpy.core.multiarray failed to import` (from `cv_bridge`) | numpy 2 → `python3 -m pip install --user "numpy<2"` |
| `module 'cv2.aruco' has no attribute 'ArucoDetector'` | Tutorial for newer OpenCV → old API: `cv2.aruco.getPredefinedDictionary`, `DetectorParameters_create`, `detectMarkers` |
| Tempted to `pip install opencv-python` | **Don't.** It breaks ROS 2's OpenCV. OpenCV comes from `apt` (4.5.4) |
| KD drone ignores your gains | Marker outside the camera view, or you didn't press Enter / −/+ in the tuner |
| PacBot: bot doesn't move | Your `task_1a.py` isn't running (the maze never moves the bot by itself) · launcher double-clicked instead of started in a terminal · **two mazes open** (they fight: close all with `q`, start one) · `systemctl status mosquitto` |
| PacBot maze window won't close | It ignores Ctrl+C → press `q` in the window, or `pkill -x task_1a_launch` |
| PacBot acts strangely after a crash | A hard-killed process left a stale MQTT session → restart both with Ctrl+C |
| `pico_mujoco_ws/install/setup.bash: No such file` in every terminal | Old bonus-task line in `~/.bashrc` → re-run `setup.sh` (it comments that line out) |
| Ubuntu "internal error" popup after stopping a ROS tool | Harmless crash report → click Don't send; stop tools with Ctrl+C |
| Screen recording is black, or the recorder has no stop button | Wayland → `learning/tools/screen_record.py` (Ctrl+C stops it). Kazam / SimpleScreenRecorder record black on Wayland. **Test a short recording first** |
| Someone else's ROS nodes in `ros2 node list` | `ROS_LOCALHOST_ONLY` not set → re-run setup, open a new terminal |
| KD recorder made **no bag** / "bag still running" | Fixed 16 Oct (`ros2 bag record` reads the keyboard, so as a background job in a real terminal it was frozen). `git pull` the kit |
| PB 2B: after the last pellet the bot takes a very long way round | The ghost guards the way to the exit and the safety check found no gap in a whole lap, so it detoured (~1 run in 10, ~40 s lost). Not a bug: just record again |
| `ImportError: tf_transformations` or `module 'numpy' has no attribute 'float'` (KD 2B server) | `sudo apt install ros-humble-tf-transformations` then `pip3 install --user --upgrade transforms3d` |
| `setup.sh` says `[!!] ... exists but is not the git clone` | You made that folder by hand → rename it (e.g. `mv ~/pico_ws ~/pico_ws.old`) and re-run |

---

## 11. FAQ

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
Task 2: KD in `~/pico_ws/src/swift_pico/src/` (`pico_controller_PID.py`, `waypoint_service.py`, `pico_client.py`,
`pico_server.py`, then `colcon build`); PacBot directly in `~/pacbot_ws/task2a/task_2a_boilerplate.py` and
`task2b/task_2b_boilerplate.py`. **Never** put solution code in this repo.

**Do we have to pick one theme now?** Both themes ran through Task 2. The rules say the team commits to one from
Task 2/3; no portal page has asked yet. Watch for it when Task 3 opens.

**Who made these notes?** Saurabh, with an AI assistant (Claude); the `CLAUDE.md` file is its index. Teammates use the ChatGPT Project.

---

## 12. Open questions to ask e-Yantra

Still open (post on the e-Yantra forum):

1. **Theme commitment:** from Task 3, or later? Two e-Yantra documents disagree, and no portal page has asked yet.
2. **KD hold rule (2B/2C):** "inside" a waypoint = a ±0.4 box per axis, or a 0.4 sphere? Our code holds by straight-line
   distance, slightly inside 0.4, which counts under both readings.
3. **Hard deadlines:** posted dates are *soft* (the e-Ratna bonus needs them); the hard cutoffs are not published.

Answered: deadline time (posted dates are soft, 11:59 pm) · KD 1B/1C clock and hover counting · both PacBot tasks use
`PB#4817.zip`, in separate slots · late KD 2A was accepted after the forum had said it was closed.

---

## 13. Updating, undoing, contributing

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

## 14. Team rules

- **This repo is public. Never commit graded solution code** (`task1a.py`, `task_1a.py`, `task_1b.py`,
  `task_2*_boilerplate.py`, `pico_*.py`, `waypoint_service.py`, `KD_4817_*`, bags `*.db3`, results, zips). Other teams could copy it, and **our** submission would then fail the
  plagiarism check. `.gitignore` blocks the usual names; still run `git status` before every commit.
- **Never commit e-Yantra's files** (their IP): theme docs, portal PDFs, launch binaries, boilerplates.
- **Never open, decompile or modify** the PacBot `task_*_launch` binaries (tamper rule = disqualification).
- **Follow the e-Yantra coding standard** in every submitted file (header block + Purpose / Input Arguments /
  Returns / Example call under each function). `submission_check.py` checks it.
- **PacBot:** never rename or restructure the boilerplate's functions.

---

## 15. What's in this repo

| Path | What |
|---|---|
| [`README.md`](README.md) | This page |
| [`RESOURCES.md`](RESOURCES.md) | Every learning link from the portal, tagged by subtask |
| [`chatgpt-project/`](chatgpt-project) | The files + instructions for the team's ChatGPT Project (see `HOW_TO_CREATE_THE_PROJECT.md`) |
| [`setup/setup.sh`](setup/setup.sh) | Laptop setup + checker |
| [`learning/tools/`](learning/tools) | The tools in [section 9](#9-tools-in-this-repo) |
| [`CLAUDE.md`](CLAUDE.md) | Index of the team notes (written for the AI assistant, but readable) |
| [`context/`](context) | Task briefs, setup findings, learning-material analysis, task log |
