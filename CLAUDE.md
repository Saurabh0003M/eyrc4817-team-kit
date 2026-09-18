# e-Yantra / eYRC 2026-27 — agent entry point

**This file is auto-loaded at session start. For ~90% of questions it is all you need — answer from
it with zero tool calls.** Open a `context/` file only when the question actually needs that file.
Never bulk-read `_extracted/`, `eYRC 2025-26/`, or the `.docx` / `.pdf` / `.png` originals — those
are storage, not context.

`Verified: 2026-09-17 · claude-code (on the Ubuntu box)`

## State in one paragraph

Team **`eYRC#4817`** (G.H. Raisoni College of Engineering & Management, Pune — portal tag `e-LSI`)
is **registered, payment confirmed, roster 4/4 active**. Themes chosen: **Khoj-o-Drone primary,
PacBot secondary**. The team is inside the **Task 0 — Setup & Installation** window (~3 weeks,
Sep 2026). **Task 0 has been run on one bare-metal Ubuntu 22.04.5 machine for both themes
(2026-09-12)**: the KD evaluator is all green, and the PB evaluator produced `4817_task0.zip`.
Portal upload status and machine owner are unknown → `context/04-task-log.md`.

**NOW (2026-09-16): Task 1 is released.** It has three parts: **1A** image processing, find
survivors in a photo (20 marks); **1B** PID for altitude hold (40); **1C** PID for all 3 axes (40).
Brief and traps: `context/09-task1-overview-and-1a.md`. The workspace is now **`~/pico_ws`** (it
replaced `pico_mujoco_ws`) and builds cleanly. **Task 1 deadline: 23 Sep 2026** (confirm the exact time).

**Saurabh is a beginner in ROS 2, PID, MuJoCo and OpenCV** (he knows Linux, C++, breadboards and
basic Python). His goal is **learning**. **The PDF roadmap was dropped (2026-09-17: he didn't like it); the team now learns through a shared ChatGPT Project** built from `chatgpt-project/`. Claude does setup and
plumbing; **Saurabh writes the "brain" code**. Explain every term, ask him to predict before each
experiment, and never hand him a finished graded solution (submissions are plagiarism-checked).

> **MuJoCo is split by theme on purpose:** KD = **3.9.0** in the `drone_env` venv, PB = **3.11.0**
> in system `python3`. Activate `drone_env` for KD work and deactivate it for PB work.
> `~/drone_ws` is a **symlink to `drone_ws/` in this folder**. Keep it: the venv's scripts
> hard-code that path. Details in `context/03-machines.md`.

## Team

| Member | Portal role | Branch / year | Proposed ownership |
|---|---|---|---|
| Gauri S Nanaware | **Captain** | Electrical, 3rd yr | Flight controller, power/ESC, **PID tuning** — control theory is her coursework; career target is F1 / renewable energy |
| Saurabh Tomke | Member | Cyber Security, 3rd yr | Drives this repo. Wants hardware / robotics / hardware-security; treats AI as tool, not replacement. **Knows Linux, C++, breadboards, intro Python. New to ROS 2 / PID / MuJoCo / MQTT.** Studies with the team ChatGPT Project (`chatgpt-project/`) |
| Parth S Hingankar | Member | Cyber Security, 3rd yr | Linux, ground-station comms |
| Mahesh B Ugale | Member | Cyber Security, 3rd yr | Linux, git discipline, CV pipeline |

Ownership column is a **proposal from 2026-09-12, not yet agreed by the team.** Roster is **frozen**
by the rules — no additions, removals or replacements. Each member must sign in with their exact
registered email or activation fails.

## Themes

Rules force **two themes through Task 1**, then commitment to **exactly one from Task 2/3 onward**.

- **Primary — Theme 2, Khoj-o-Drone (KD).** Autonomous quadcopter search-and-rescue: explore a
  disaster zone, detect survivors, estimate coordinates, prioritise critical ones, report to a
  ground station. Recommended for 3rd/4th yr. → `context/01-theme-khoj-o-drone.md`
- **Secondary — Theme 7, PacBot (PB).** Micromouse-style maze bot collecting points while evading
  patrolling ghost bots. All years. → `context/02-theme-pacbot.md`

### Task 1 — CONFIRMED from the portal (2026-09-16)

| Part | What | Marks |
|---|---|---|
| 1A | OpenCV: ArUco corners → 900×900 top-down view → 12×12 grid → red/yellow survivors → nearest intersection names (A1–K11) → `<image>_results.txt` | 20 |
| 1B | **Tune** e-Yantra's pre-built controller (Kp/Ki/Kd, throttle only): error within ±0.4 in 5 s, held 10 s; submit a ros2 bag + unlisted YouTube video | 40 |
| 1C | **Tune** pitch (X) + roll (Y) gains on top of the 1B throttle; all 3 errors within ±0.4 in 5 s, held 10 s; bag + YouTube | 40 |

For 1B/1C, subscribe to `/rotors/odometry` and publish `/drone_command`
(`swift_msgs/msg/SwiftMsgs`, RC values 1000–2000 centred on 1500). Launch with
`swift_pico_simulation.launch.py` in `~/pico_ws`. Reference: `context/07-swift-pico-interface.md`.
*Superseded:* the earlier note that "1B = full position controller" was wrong; 1B is altitude only,
and x/y come in 1C.

## Stack (KD)

**Ubuntu 22.04 LTS + ROS 2 Humble** · MuJoCo · Betaflight Configurator · Git · Python / C++
Skills unlocked: image processing · control systems (PID / LQR) · path planning & trajectory generation

> **Hard lock: Ubuntu 22.04 + ROS 2 Humble. Do not install Ubuntu 24.04.** Every doc link on the
> portal points at `docs.ros.org/en/humble/`; Humble is the LTS for 22.04 Jammy. 24.04 would give
> you Jazzy and invalidate every command the portal hands you. *(Confirmed 2026-09-12 from the
> portal prelearnings.)*

The theme doc said "Gazebo / MuJoCo" but the portal section is titled **"ROS 2 & MuJoCo"** — MuJoCo
looks like the real simulator, which is much lighter than Gazebo and defuses the Intel Arc iGPU
concern. *[INFERRED — confirm when the MuJoCo page arrives.]*

Portal: `portal.e-yantra.org/courses/theme_kd` · learnings tree `learnings/{linux, ros}`.
Triaged study plan — what to do, in what order, what to skip: `context/06-prelearnings.md`.

Stage-2 kit, free to teams that clear Stage 1: flight controller, motors, RadioMaster Ranger Nano
2.4 GHz ELRS module, battery + charger, clear props, 3D-printed parts, frame, camera, WhyCon sticker.

## Timeline

| When | What |
|---|---|
| Sep 2026 | Task 0 — Setup & Installation (~3 weeks) |
| **16 → 23 Sep 2026** | **Task 1 (KD 1A/1B/1C + PB 1A/1B). ← CURRENT. Deadline 23 Sep** |
| Oct–Nov 2026 | Task 2 Learn & Explore II (~4 wk) |
| Nov 2026 | Stage 1 ends. Top teams selected for Stage 2 + free hardware kit |
| Nov 2026 – Feb 2027 | Tasks 3–6 (hardware) |
| Mar 2027 | National Finale, IIT Bombay |

Prize pool ₹10,00,000 · 5–6 finale teams · paid 6–8 week summer internship at IIT Bombay for
individually strong performers. Advancement to Stage 2 is **purely on Stage 1 task performance**.

## Machines — the live gate

Requirement: Ubuntu 22.04 LTS · >4 cores x86_64 · 8 GB+ RAM · 100 GB+ storage · no dedicated GPU needed.

**Ubuntu box, Task 0 done (measured 2026-09-13, owner unconfirmed):** AMD Ryzen 7 7840HS
(8C/16T), Radeon 780M iGPU, 14 GiB RAM, 954 GB NVMe dual-boot. Ubuntu 22.04.5 bare metal, kernel
6.8. **Its root partition is only 48.8 GB (26 GB free), below the 100 GB requirement.** That is
fine for Task 0 but will get tight once MuJoCo workspaces, colcon builds and `ros2 bag` recordings
pile up.

**Saurabh's HP Pavilion Plus 14** as recorded 2026-09-12: Core Ultra 5 125H, Intel Arc, 477 GB
NVMe, Windows only with no Linux partition. It is unclear whether this has been superseded by the
Ubuntu box above.

**Gauri's, Parth's and Mahesh's machines are UNKNOWN — ask the team, do not probe.** Full inventory,
the install risks, and the dual-boot plan: `context/03-machines.md`.

## Where things are

| Path | Contents | Read when |
|---|---|---|
| `CLAUDE.md` | this file | always — auto-loaded, free |
| `README.md` | **Teammate entry point** (public repo): first day, what setup checks, laptop layout, per-task run commands, tools, troubleshooting, open forum questions, team rules | teammate questions |
| `RESOURCES.md` | **Every portal learning link (~180, all verified 2026-09-16 with `check_links.py`)**, grouped like the portal, tagged by subtask (KD 1A … PB 1B) | finding any video/doc link |
| `setup/setup.sh` | v2: preflight (OS/arch/WSL/VM/RAM/disk/ROS/internet) → inventory → installs only what's missing → verify. `--check` = no changes. bashrc block adds `ROS_LOCALHOST_ONLY=1`. Install mode not yet run on a fresh laptop | teammate setup |
| `learning/tools/` | `pixel_detective.py` + `hsv_tuner.py` (KD 1A), `toy_drone.py` (PID practice; controller left blank for Saurabh), `kd1a_testbench.py` (KD 1A; consistency across 10 variants, no answer key), `submission_check.py` (kd1a/kd1b/kd1c/pb1a/pb1b: coding standard, GUI calls, results format, PB signatures, zip), `bag_score.py` (KD 1B/1C; scoring assumptions in the file), `check_links.py` (every link in README/RESOURCES/chatgpt-project; retries 5xx). All tested 2026-09-16 with dummy inputs, and none contains a solution | learning sessions, pre-submission checks |
| `chatgpt-project/` | **The team's ChatGPT Project kit (2026-09-17):** `PROJECT_INSTRUCTIONS.md` (paste into the project instructions), 9 upload files `00_START_HERE` … `08_Portal_Learnings_Summary`, `HOW_TO_CREATE_THE_PROJECT.md`. **Keep these in sync when task facts change**, then tell Saurabh which file to re-upload | any change to task facts, team plan, setup |
| `context/01-theme-khoj-o-drone.md` | KD objectives, build targets, win condition, kit | planning KD work |
| `context/02-theme-pacbot.md` | PB equivalent | only if PB comes back into play |
| `context/03-machines.md` | laptop inventory, dual-boot plan, install risks | any setup / Task 0 work |
| `context/04-task-log.md` | **living status per task — update this** | every session |
| `context/05-competition-reference.md` | rules, full schedule, FAQ answers, learning resources | rare, lookup only |
| `context/06-prelearnings.md` | **triaged study path** (ROS 2, MuJoCo, quadcopter physics), tiers, gotchas, per-member split | teaching or planning study |
| `context/07-swift-pico-interface.md` | **Swift Pico sim: topics, message, arming, axis mapping** | writing any controller code |
| `context/08-task0-bonus.md` | **Task 0 bonus:** turtlesim circle (d=2.0 at 5,5) + Swift Pico bring-up, approach notes, MuJoCo-version watch-out | bonus task / sim bring-up |
| `context/15-pacbot-task1.md` | **PacBot Task 1:** 1A grid maze over MQTT (35), 1B MuJoCo wall following (65); topics, scoring, submission (`PB#4817.zip`), **tamper rule for the launch binaries**, repo-vs-portal name differences, setup verified | working on PacBot Task 1 |
| `context/14-learnings-pacbot-mqtt-pathplanning.md` | **PacBot learnings:** MQTT (QoS, wildcards, retained/LWT; **local mosquitto + paho 2.1.0 verified**), path planning (BFS/DFS/Dijkstra/Greedy/A*; **PB Task 1A = grid maze planning + pellet choice**) | PacBot work; updating `chatgpt-project/` |
| `context/13-learnings-quad-control-imgproc-coding.md` | Quadcopter Control (6 DOF, **Stage-2 laptop→RC→attitude-controller architecture = the sim's structure**, translational-EOM exercise trap), Image Processing/OpenCV/ROS 2–OpenCV (red hue wraps; sim `image_sink` defaults to shm so no `/image_raw`), **e-Yantra Coding Standard** for submissions | updating `chatgpt-project/`; Task 1A/2 coding |
| `context/12-learnings-control-systems.md` | **Portal Control Systems learnings analysed**: PID/stability/modelling/LQR video ladders (metadata-ordered), portal formula bugs, **"LQR/LQI will be implemented" signal**, PDFs behind login | updating `chatgpt-project/`; PID/LQR learning |
| `context/11-task1c.md` | **Task 1C:** tune pitch/roll on top of 1B, submission order, **tuner GUI facts from its source** (save path, multipliers, gains-sent-only-on-click trap) | working on Task 1C / using the tuner |
| `context/10-task1b.md` | **Task 1B:** tune the pre-built throttle PID, GUI, scoring, bag + YouTube submission, **MuJoCo/GLFW library fixes** | working on Task 1B / launching the sim |
| `context/09-task1-overview-and-1a.md` | **Task 1 structure + full Task 1A spec**, output format, scoring, traps (OpenCV 4.5.4 old ArUco API, 3-vs-4-line contradiction) | working on Task 1A |
| `eYRC 2026-27/` | becomes the working repo — Task code lives here (git init'd, no commits) | writing code |
| `eYRC 2025-26/` | last season's archive (CropDrop Bot, KrishiCobot, Q-learning + CoppeliaSim) | historical reference |
| `_extracted/` | verbatim `.docx` text dumps — greppable fallback if `context/` looks wrong | verifying a quote |
| `eYRC 2026-27/Media/Task0/` | portal images: `bonus_task0.webp` (bonus task figure), `pico_drone.webp` (Swift Pico in MuJoCo) | bonus task |
| `drone_ws/task0/` | KD Task 0: `drone_env` venv (MuJoCo 3.9.0, `eyantra-autoeval`) + evaluator output `result-2026-KD-0-20260912.json`. Also reachable as `~/drone_ws` (symlink — **do not delete**) | KD setup / submission |
| `pacbot_ws/` | clone of `eYantra-Robotics-Competition/eYRC_26-27_PacBot`; `task0/task0_eval` + sealed submission `4817_task0.zip`; uses system MuJoCo 3.11.0 + paho-mqtt. **Never commit the `4817_task0.*` files** | PB setup / submission |

### Layout on the Ubuntu box (rearranged 2026-09-13)

```
~/Desktop/e-yantra/              ← everything eYRC lives here (this file)
├── CLAUDE.md  README.md  RESOURCES.md  context/  setup/  _extracted/
├── eYRC 2025-26/                  last season's archive
├── eYRC 2026-27/                  docs, media (git, no commits)
│   └── Media/Task0/               bonus_task0.webp, pico_drone.webp
├── drone_ws/task0/                KD — drone_env venv (MuJoCo 3.9.0) + result JSON
├── pacbot_ws/                     PB — e-Yantra git clone (task0, task1a, task1b); also ~/pacbot_ws (symlink)
├── turtlesim_ws    → ~/turtlesim_ws      (symlink) bonus Part 1, node kd_task_0/task_0_4817.py
├── pico_ws         → ~/pico_ws           (symlink) Swift Pico sim + Task 1 scripts (src/swift_pico/scripts/)
├── chatgpt-project/               team ChatGPT Project: instructions + 9 upload files
└── learning/tools/                learning + submission-check tools
~/Desktop/e-yantra-old-roadmap/  dropped roadmap PDF + source (outside the repo, reference only)
~/drone_ws  →  ~/Desktop/e-yantra/drone_ws     (symlink; the venv needs this path)
```

**Never put a workspace inside `eYRC 2026-27/`.** The space in that folder name breaks
colcon/CMake. **ROS 2 (colcon) workspaces live at the portal's home-level path**, e.g.
`~/turtlesim_ws` and `~/pico_ws`, with a symlink *into* this folder for browsing. That is
the reverse of `drone_ws`, because colcon writes physical paths into `install/`. Plain venvs can
live here with a home symlink. Reasoning: `context/08-task0-bonus.md`.

> **Backups and provenance:** the full unzipped folder, as it was before this session's edits, is
> on **T9 volume 2** (`/media/ubantu/Samsung T9 volume 2/e-yantra`), verified 2026-09-13: 87
> files, CRC-clean. Both truncated `e-yantra.zip` copies were moved to Trash. `F:\e-yantra` on
> Windows is the original.

## Working rules for agents

1. **Answer from this file first.** If you find yourself running `find` or `ls` to orient, this file
   failed — fix it at the end of the session rather than leaving the next agent to re-explore.
2. **Folder vs brain split.** This folder holds *artifacts and current technical state*. The Obsidian
   brain (`brain/e-yantra/e-yantra-index`) holds *decisions and why*. Do not duplicate across them;
   link instead.
3. **Update `context/04-task-log.md`** whenever a task's status changes, then update the `e-yantra`
   block in the brain's `STATE.md` with your agent name and the date.
4. **Write every file as UTF-8.** A single cp1252 byte corrupted the brain's STATE.md in Sep 2026.
5. **Mark confidence.** Distinguish what a source document says from what you inferred. The WhyCon
   inference above is the template.
6. **State gaps explicitly** so the next agent asks instead of re-probing. See the UNKNOWN machines.
