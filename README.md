# eYRC 2026-27 · Team 4817 · Khoj-o-Drone + PacBot

Everything the team needs to **set up**, **learn** and **check submissions** for e-Yantra Robotics
Competition 2026-27, Stage 1. Written for teammates who are new to ROS 2, PID, MuJoCo, OpenCV and MQTT.

> This repo contains **no e-Yantra competition files** (task PDFs, launch binaries, boilerplates) and
> **no graded solutions**. You get those from the portal and e-Yantra's own GitHub repos, and
> `setup.sh` fetches the GitHub ones for you.

---

## Contents

1. [First day (30 minutes)](#1-first-day-30-minutes)
2. [Setup: what the script does](#2-setup-what-the-script-does)
3. [Where everything lives on your laptop](#3-where-everything-lives-on-your-laptop)
4. [Task 1 at a glance](#4-task-1-at-a-glance)
5. [How to run each task](#5-how-to-run-each-task)
6. [Learning: where to start](#6-learning-where-to-start)
7. [Tools in this repo](#7-tools-in-this-repo)
8. [Troubleshooting](#8-troubleshooting)
9. [Open questions to ask e-Yantra](#9-open-questions-to-ask-e-yantra)
10. [Team rules](#10-team-rules)
11. [What's in this repo](#11-whats-in-this-repo)

---

## 1. First day (30 minutes)

You need **Ubuntu 22.04 on bare metal** (not WSL, not 24.04) with **ROS 2 Humble**, i.e. e-Yantra **Task 0 done**.

```bash
git clone https://github.com/Saurabh0003M/eyrc4817-team-kit.git ~/eyrc4817
cd ~/eyrc4817
bash setup/setup.sh --check     # 1) look only: shows what you have and what setup would change
bash setup/setup.sh             # 2) do it (asks for your password once; takes ~5–10 min)
```

Then:

1. **Close the terminal and open a new one** so the settings load.
2. Run `bash ~/eyrc4817/setup/setup.sh --check` again. It should say *Everything is set up*.
3. Open **`LEARNING-ROADMAP.pdf`** and read sections 1–3 (about 10 minutes).
4. Agree with the team **who owns which Task 1 subtask** (section 4 below).
5. Try one simulator from [section 5](#5-how-to-run-each-task), just to see it open.

If anything fails, send the team `~/eyrc4817-setup.log`.

---

## 2. Setup: what the script does

**It checks before it changes anything.** `--check` changes nothing. A normal run installs **only
what's missing**, never deletes your files, and backs up `~/.bashrc` first. Safe to run again anytime,
e.g. after `git pull`.

| Stage | What it checks or does |
|---|---|
| **1. Your computer** | Ubuntu 22.04 · x86_64 · not WSL · not a virtual machine · RAM · ≥ 4 GB free disk · ROS 2 Humble desktop · GitHub reachable. **Stops before changing anything** if a hard requirement fails |
| **2. What's installed** | Each apt package · numpy (must be < 2) · paho-mqtt (≥ 2) · OpenCV · your MuJoCo Python version (never changed) · MuJoCo 3.9.0 library · workspaces · old `~/pico_mujoco_ws` · `~/.bashrc` · MQTT broker. Prints `[ok]`, `[todo]` or `[!!]` for each |
| **3. Install** (not in `--check`) | `apt` installs only the missing packages · `numpy<2` / `paho-mqtt>=2` only if needed · MuJoCo **3.9.0** library in a private folder (`~/.local/share/eyrc4817/`) only if not found · clones or updates **`~/pico_ws`** (branch `kd_sim`) + `colcon build` · clones or updates **`~/pacbot_ws`** + creates `task_1a.py` / `task_1b.py` from the boilerplates if missing · `~/.bashrc` block · enables the `mosquitto` broker |
| **4. Verify** | OpenCV 4.5.x with the old ArUco API · numpy < 2 · `cv_bridge` · paho-mqtt · the KD simulator finds all its libraries · KD controllers + PID tuner · PacBot launchers + task files · broker running |

**The `~/.bashrc` block** (between `# >>> eyrc4817 >>>` and `# <<< eyrc4817 <<<`):

- sources ROS 2 Humble and `~/pico_ws` in every terminal;
- adds the MuJoCo 3.9.0 library path (e-Yantra's KD simulator was built to look in a folder that only
  exists on their own computer);
- sets **`ROS_LOCALHOST_ONLY=1`**, so ROS 2 stays on your laptop and teammates' simulators on the same
  Wi-Fi don't interfere with yours;
- comments out any old line that sources the deleted `~/pico_mujoco_ws` (the Task 1 page says to
  replace it with `~/pico_ws`).

**Two MuJoCo versions on purpose:** PacBot's Task 0 uses MuJoCo **3.11.0** (Python), while the Khoj-o-Drone
simulator needs the **3.9.0** library. Setup keeps both, and they don't clash.

---

## 3. Where everything lives on your laptop

```
~/eyrc4817/          ← this repo (docs, roadmap, tools). Clone it anywhere; ~/eyrc4817 is just the suggestion
~/pico_ws/           ← Khoj-o-Drone workspace. Path fixed by e-Yantra; don't rename it
   src/swift_pico/scripts/   task1a.py + image_1.jpg   (KD Task 1A)
   src/swift_pico/src/       pid_values.yaml           (saved by the PID tuner)
~/pacbot_ws/         ← PacBot workspace. Path fixed by e-Yantra
   task1a/   task_1a_launch · task_1a_boilerplate.py · task_1a.py   (PB Task 1A)
   task1b/   task_1b_launch · task_1b_boilerplate.py · task_1b.py   (PB Task 1B)
~/.local/share/eyrc4817/mujoco-3.9.0/   ← library for the KD simulator (created by setup if needed)
~/eyrc4817-setup.log                    ← setup log
```

> ⚠ The portal says `task_1a` / `task_1b`, but e-Yantra's repo actually uses **`task1a` / `task1b`**. Use the real folders.
> Some notes in `CLAUDE.md` and `context/` describe Saurabh's laptop (paths like `~/Desktop/e-yantra`,
> `drone_ws`, `_extracted/`). Those are not in this repo and you don't need them.

---

## 4. Task 1 at a glance

Both themes are carried until Task 2/3. Deadline: **ask the portal/forum** (not yet known).

| Theme | Part | What | Code or tune? | Marks | Roadmap | Brief |
|---|---|---|---|---|---|---|
| Khoj-o-Drone | 1A | Find survivors in a photo → grid names like `D2` | write Python + OpenCV | 20 | M1 | [`context/09`](context/09-task1-overview-and-1a.md) |
| Khoj-o-Drone | 1B | Drone holds a fixed height | tune 3 gains | 40 | M6 | [`context/10`](context/10-task1b.md) |
| Khoj-o-Drone | 1C | Drone holds x and y too | tune pitch + roll gains | 40 | M7 | [`context/11`](context/11-task1c.md) |
| PacBot | 1A | Grid maze: 2 pellets, then an exit, over MQTT | write Python (search + turn logic) | 35 | P2 | [`context/15`](context/15-pacbot-task1.md) |
| PacBot | 1B | 3D maze wall following, 0 collisions | write Python + PID | 65 | P3 | [`context/15`](context/15-pacbot-task1.md) |

Submissions are uploaded by the **Team Leader (Gauri)** plus an **unlisted YouTube** screen recording for
KD 1B/1C and PB 1A/1B. **Test your screen recorder first**: Ubuntu 22.04 runs Wayland, where Kazam and
SimpleScreenRecorder often record a black screen. Use the built-in recorder (Print Screen → video) or OBS.

---

## 5. How to run each task

Open a **separate terminal for each command**, in the order shown. Stop everything with **Ctrl+C**
(never Ctrl+Z, never close the window, never `kill -9`).

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
Tuner facts: value sent = number × scale (default Kp×0.03, Ki×0.008, Kd×0.6). **Gains are sent only when
you press −/+ or Enter.** "Save Values" writes `~/pico_ws/src/swift_pico/src/pid_values.yaml`.
If gains seem to do nothing, the drone's marker may be out of the camera view.

**PB 1A** (two terminals; the broker is already running as a service):
```bash
cd ~/pacbot_ws/task1a && ./task_1a_launch                   # 1: maze window
cd ~/pacbot_ws/task1a && python3 task_1a.py                 # 2: your code
mosquitto_sub -h localhost -t 'robot/pose' -t 'pellets/pose' -t 'bot/cmd' -v   # optional: watch the messages
```

**PB 1B** (two terminals):
```bash
cd ~/pacbot_ws/task1b && ./task_1b_launch                   # 1: MuJoCo maze
cd ~/pacbot_ws/task1b && python3 task_1b.py                 # 2: your code
```

Submission runs add `--evaluate` to the PacBot launchers, and `ros2 bag record` for KD 1B/1C. See the briefs in section 4.

---

## 6. Learning: where to start

| You want to… | Open |
|---|---|
| Know **what to learn, in what order, with experiments** | **`LEARNING-ROADMAP.pdf`**: one module per Task 1 subtask; click boxes to tick, Ctrl+S saves |
| Find **any link** the portal gave (videos, docs, playlists) | **[`RESOURCES.md`](RESOURCES.md)**: every portal link, grouped like the portal, mapped to roadmap modules |
| Look up a **word** (PID, topic, broker, HSV…) | Roadmap §4, the plain-words dictionary |
| Read the **exact task rules**, traps and scoring | `context/09`–`11` (KD), `context/15` (PacBot) |
| See what the **learning pages say** + portal mistakes we found | `context/12` (control), `13` (quad control, OpenCV, coding standard), `14` (MQTT, path planning), `06` (ROS 2, MuJoCo, quadcopters) |

**Suggested first modules:** M0 (big picture) → M1 if you own KD 1A · P1 → P2 if you own PB 1A · M3 (PID)
for **everyone** (4 of the 5 subtasks use PID).

**The roadmap was written with an AI assistant ("Claude") in mind.** No assistant? Here is who does the
"Claude does" parts: setup → `setup.sh`; checking your work → the tools in section 7; everything else →
ask a teammate. **The learning parts (predict, try, explain, teach) are yours either way.**

---

## 7. Tools in this repo

All in `learning/tools/`. None of them solves a task; they measure and check.

| Tool | Use it for | Example |
|---|---|---|
| `pixel_detective.py` | Click the photo → see BGR and HSV numbers (M1-b) | `python3 learning/tools/pixel_detective.py` |
| `hsv_tuner.py` | Sliders → see which pixels a colour range keeps (M1-f) | `python3 learning/tools/hsv_tuner.py` |
| `kd1a_testbench.py` | Runs **your** KD 1A script on 10 harder versions of the arena; answers must stay the same (M1-j) | `python3 learning/tools/kd1a_testbench.py --script ~/pico_ws/src/swift_pico/scripts/task1a.py` |
| `submission_check.py` | Before Gauri uploads: file names, **coding standard**, no `imshow`/`input()`, results format, PacBot functions unchanged, zip layout | `python3 learning/tools/submission_check.py pb1a --file ~/pacbot_ws/task1a/task_1a.py` |
| `bag_score.py` | Estimates KD 1B/1C marks from a practice bag (assumptions in the file) | `python3 learning/tools/bag_score.py 1b task_1b` |
| `toy_drone.py` | Plain-Python PID playground; you write the controller (M3-f) | `python3 learning/tools/toy_drone.py --kp 20` |
| `check_links.py` | Checks every link in the docs still works | `python3 learning/tools/check_links.py` |

---

## 8. Troubleshooting

| You see | Cause → fix |
|---|---|
| `libmujoco.so.3.9.0: cannot open shared object file` | Old terminal, or setup not run → open a **new terminal**; run `setup.sh --check` |
| `numpy.core.multiarray failed to import` (from `cv_bridge`) | numpy 2 installed → `python3 -m pip install --user "numpy<2"` |
| `module 'cv2.aruco' has no attribute 'ArucoDetector'` | Tutorial written for newer OpenCV → use the old API: `cv2.aruco.getPredefinedDictionary`, `DetectorParameters_create`, `detectMarkers` |
| Never `pip install opencv-python` | It breaks ROS 2's OpenCV. OpenCV comes from `apt` (4.5.4) |
| KD drone ignores your gains | Marker outside the camera view, or you didn't press Enter / −/+ in the tuner |
| PacBot: nothing moves | Start the launcher **before** your code · `systemctl status mosquitto` · topic name typo |
| PacBot behaves oddly after a crash | A process was hard-killed and left a stale MQTT session → restart both with Ctrl+C |
| `~/pico_mujoco_ws/install/setup.bash: No such file` in every terminal | Old bonus-task line in `~/.bashrc` → re-run `setup.sh` (it comments that line out) |
| Ubuntu "internal error" popup after stopping a ROS tool | Harmless crash report from a `ros2` command stopped with a kill signal → click Don't send; stop tools with Ctrl+C |
| Screen recording is black | Wayland → Ubuntu's built-in recorder (Print Screen → video), OBS, or log in with "Ubuntu on Xorg" |
| Someone else's ROS nodes show up in `ros2 node list` | `ROS_LOCALHOST_ONLY` not set → re-run setup, open a new terminal |

---

## 9. Open questions to ask e-Yantra

Post these on the e-Yantra forum; the portal pages don't answer them or contradict each other:

1. **Task 1 deadline** for both themes.
2. **KD 1A results file:** 3 lines or 4? The instruction page shows a blank line 2; the submission page says "exactly three lines".
3. **KD 1A marker IDs:** always 80, 85, 90, 95 in the hidden test images? The submission page's example shows 10, 15, 20, 25.
4. **KD 1B/1C scoring:** when does the clock start (bag start, controller start)? Are "hover seconds" continuous or cumulative?
5. **Theme commitment:** from Task 2 or Task 3? Two e-Yantra documents disagree.
6. **PacBot:** 1A and 1B both use the zip name `PB#<team_id>.zip`. Confirm they go in separate slots.

---

## 10. Team rules

- **This repo is public. Never commit graded solution code** (`task1a.py`, `task_1a.py`, `task_1b.py`,
  `KD_4817_*`, results/zips). Other teams could copy it, and **our** submission would then fail the
  plagiarism check. `.gitignore` blocks the usual names; still run `git status` before every commit.
- **Never commit e-Yantra's files** (their IP): theme docs, portal PDFs, launch binaries, boilerplates.
- **Never open, decompile or modify** the PacBot `task_1*_launch` binaries (tamper rule = disqualification).
- **Follow the e-Yantra coding standard** in every submitted file (header block + Purpose/Input/Returns/Example
  under each function). `submission_check.py` checks it.
- **PacBot:** never rename or restructure the boilerplate's functions.
- Want push access? Ask Saurabh to add you as a collaborator (GitHub → Settings → Collaborators).

---

## 11. What's in this repo

| Path | What |
|---|---|
| `README.md` | This page |
| `RESOURCES.md` | Every learning link from the portal, mapped to roadmap modules |
| `LEARNING-ROADMAP.pdf` | The learning roadmap (source: `learning/source/roadmap.md`, built with `build_roadmap_pdf.py`) |
| `setup/setup.sh` | Laptop setup + checker |
| `learning/tools/` | The tools in section 7 |
| `CLAUDE.md` | Index of the team notes (written for the AI assistant, but readable) |
| `context/` | Task briefs, setup findings, learning-material analysis, task log |
