# Task log — eYRC 2026-27, team eYRC#4817

**Living file. Update it whenever a task's status changes, then update the `e-yantra` block in the
brain's `STATE.md` with your agent name and the date.** Newest entry first.

## Status board

| Task | Window | Status | Owner | Notes |
|---|---|---|---|---|
| Registration | 1–25 Aug 2026 | **DONE** | Gauri (Captain) | Paid, roster 4/4 active |
| Theme selection | Sep 2026 | **DONE** | team | KD primary, PB secondary |
| **Task 0 — Setup & Installation** | ~3 wk, Sep 2026 | **IN PROGRESS — 1 of 4 machines done** | all four | Ubuntu box: KD evaluator all green; PB sealed submission generated (2026-09-12). Portal upload status **unknown**. Other three machines not started or unknown |
| **Task 0 — Bonus task** | end of Task 0 | **Part 1 DONE · Part 2 UNBLOCKED (sim builds; launch not tried)** | Saurabh + claude-code | Practice only. (1) turtlesim circle: node `task_0_4817` verified; portal text says d=2.0 but its figure shows ~8.0, so `radius` is a parameter. (2) apt packages installed; fresh `~/pico_ws` builds all 17 packages. Details: `08-task0-bonus.md` |
| **Task 1A — find survivors (OpenCV)** | released 2026-09-16, **deadline 23 Sep** | **NOT STARTED — next** | proposed: Mahesh | 20 marks. Spec + traps: `09-task1-overview-and-1a.md`. Study file `chatgpt-project/01_…` |
| **Task 1B — tune altitude PID** | same | **READY TO TUNE** (sim libraries all found; not yet launched with the controller) | proposed: Gauri | 40 marks. Controller is a pre-built binary: **tune gains, record bag + YouTube**. `10-task1b.md` |
| **Task 1C — tune pitch + roll** | same | not started (needs 1B throttle gains first) | proposed: Gauri | 40 marks. Tuning, not coding; bag + YouTube. `11-task1c.md` |
| **PacBot Task 1A — maze path planning** | released, **deadline 23 Sep** | **SETUP DONE, not started** | proposed: Parth | 35 marks. `15-pacbot-task1.md` |
| **PacBot Task 1B — wall following (MuJoCo)** | same | **SETUP DONE, not started**; submission page received | proposed: Saurabh | 65 marks. `15-pacbot-task1.md` |
| Task 2 — Learn & Explore II | ~4 wk | not started | — | commit to one theme |
| Tasks 3–6 | Nov 26 – Feb 27 | Stage 2 only | — | needs Stage 1 selection |

## Open actions

0. **Task 1 (all five subtasks), deadline Wed 23 Sep.** Plan + proposed owners: `chatgpt-project/00_START_HERE.md`
   (work final Tue 22; Gauri uploads early on the 23rd). Forum questions (results-file line 2, deadline time, …)
   are listed there. Everyone studies via the team ChatGPT Project and writes their own code; Claude supplies tools (`learning/tools/`) and checks. **Gauri
   must upload**, because only the Team Leader can.
1. **Confirm the Task 0 uploads.** Check whether `pacbot_ws/task0/4817_task0.zip` and
   `drone_ws/task0/result-2026-KD-0-20260912.json` have been submitted on the portal.
   The PB file is an encrypted sealed box (`eyrc-2026-PB-task0-sealedbox-v1`, team 4817), so it
   cannot be inspected, only uploaded.
2. **Identify the Ubuntu box's owner** (AMD Ryzen 7 7840HS — see `03-machines.md`). It does not
   match Saurabh's recorded HP Pavilion. If Task 0 has to be completed per member, the other
   members still need their own runs.
3. **Collect machine specs** for Gauri, Parth and Mahesh → `03-machines.md`. Blocks setup planning.
4. ~~Re-copy `F:\e-yantra` in full.~~ **Done 2026-09-13**, from T9 volume 2. See the entry below.
5. **Small setup gaps on the Ubuntu box:** set a unique `ROS_DOMAIN_ID` in `~/.bashrc`; set git
   `user.name`/`user.email`; plan for the 48.8 GB root partition before Task 1B.
6. **Agree the role split** in `CLAUDE.md` with the team — currently an unagreed proposal.
7. *(superseded?)* **Saurabh's HP dual-boot** plan in `03-machines.md` — only if the HP laptop is
   still meant to run Linux.
8. *(optional)* **RoboReady** — free, voluntary 5-hour collaborative-problem-solving course from
   IIT Bombay. Register by emailing the captain's address to `suprabhaj@iitb.ac.in`. Stage 4 needs a
   Firebird V robot and can be skipped. Worth it only if all four can sit together for 5 hours.

## Entries

### 2026-09-17 · claude-code — deadline 23 Sep; ChatGPT Project replaces the roadmap PDF

- Saurabh: **Task 1 deadline = 23 Sep 2026**. The portal's *ROS 2 Books* page leads to a paid book (skip). **Teammate info
  may stay public.** He **didn't like the roadmap PDF**, and the new plan is **a ChatGPT Project** (instructions + files)
  shared with all teammates for questions and learning.
- Built **`chatgpt-project/`**: `PROJECT_INSTRUCTIONS.md` (~3.9k chars: tutor role, plain words, **no complete graded
  solutions (plagiarism check, shared project)**, environment facts, common wrong advice) + 9 files: 00 start (team,
  subtask table, **proposed owners** Gauri KD 1B/1C, Mahesh KD 1A, Parth PB 1A, Saurabh PB 1B, **6-day plan**, forum
  questions), 01–04 one per subtask, 05 setup/run/submit/coding standard/troubleshooting, 06 concepts, 07 all links +
  watch-first list, 08 portal-learnings summary + portal mistakes. Plus `HOW_TO_CREATE_THE_PROJECT.md`.
- **New findings from the PacBot boilerplates** (see `15`): the 1B sensor-name contradiction (portal vs boilerplate);
  1A north = row+1; manual `mosquitto` conflicts with the service.
- Repo: the roadmap PDF + source + builder removed from git (moved to `~/Desktop/e-yantra-old-roadmap/`); README and
  RESOURCES re-tagged by subtask instead of roadmap modules; `check_links.py` retries 5xx and covers
  `chatgpt-project/`.

### 2026-09-16 (late) · claude-code — teammate-readiness pass

- **Audit:** the repo had only 48 links vs ~180 in the portal material (no docs.ros.org at all), and
  `CLAUDE.md` pointed at 21 local-only paths.
- Added **`RESOURCES.md`** (every portal link + roadmap extras, mapped to modules) and
  **`learning/tools/check_links.py`** (YouTube via oEmbed, Colab via GitHub). Result: 182 links OK, portal
  links skipped, one transient 500 re-checked OK.
- **`setup.sh` v2:** preflight, inventory, install-only-missing, verification, "where things are", log file,
  `ROS_LOCALHOST_ONLY=1`, and it disables stale `pico_mujoco_ws` bashrc lines. Fixed 3 bugs found by `--check`
  (VM detection, MuJoCo search depth, perpetual to-dos). The bashrc editing was tested on a fake HOME and is
  idempotent. **Install mode is untested on a fresh machine.**
- **README v2:** teammate-first (first day, setup table, laptop layout, run commands, tools, troubleshooting,
  forum questions, rules).
- Still open: Linux + ROS 2 Books portal pages never shared; login-only PDFs; live checks (tuner
  click-trap, PB LEFT = ±90°, scoring clock); public-repo personal data/IP decision; deadline, split, machines.

### 2026-09-16 (night) · claude-code — all material in, roadmap v3

- Saurabh: "all learning material provided" (KD + PacBot), plus the PB Task 1B submission page →
  `15-pacbot-task1.md` (result.json; marks = C × max(0, 65 − 10·collisions)).
- PacBot Task 1 setup done and smoke-tested (see `15`). `~/pacbot_ws` symlink; `task_1a.py` /
  `task_1b.py` copied from the boilerplates.
- **Roadmap v3 rebuilt**: 19 pages, both themes, a module per Task 1 subtask, and portal material slotted
  into video ladders. Includes the portal-bug exercises (I-term formula; translational EOM missing
  thrust) and a team-split *proposal*. Open: the team split, deadline, laptop owner, other machines,
  Task 0 upload status.
- **Team git repo (local)** at `~/Desktop/e-yantra`: whitelist `.gitignore`, `README.md`, `setup/setup.sh`
  (`--check` passes on this laptop), first commit `89ff48c` (24 files, 568 K). Git identity set: Saurabh Tomke
  <saurabh.tomke@gmail.com>. Saurabh chose **public GitHub**; not pushed yet, because it waits for his explicit yes
  after the IP/privacy warning and his own `gh auth login`. The file isn't committed yet, so it lands with the next commit.

### 2026-09-16 (evening) · claude-code — Task 1C brief, yt-dlp

- Saurabh approved and **`yt-dlp` 2026.08.19 was installed** (`pip3 install --user`, 3.2 MB, no
  dependencies; numpy, MuJoCo and cv2 unchanged). It warns that Python 3.10 support is deprecated,
  which is harmless for now.
- The three portal videos are **silent, uncaptioned screen recordings**. Captions are useless, so
  frames would need the video (≈ 11.5 MB); asked Saurabh before downloading.
- Task 1C brief → `11-task1c.md`. From the tuner GUI source: the save path, the default
  multipliers, the built-in `/pos_error` graph, and the **gains-only-sent-on-click trap**.
- PacBot Task 1 material not received yet. The roadmap rebuild is still pending until it arrives.

### 2026-09-16 (later) · claude-code — Task 1B brief + sim bring-up

- Task 1B brief saved → `10-task1b.md`. **Key correction:** 1B is **tuning** a pre-built controller
  binary (Kp/Ki/Kd for throttle), not writing PID code. The submission is a ros2 bag
  (`/pos_error`, `/whycode_node/markers`, ≥ 60 s) plus an unlisted YouTube recording.
- **Found and fixed:** `mujoco_bridge` looks for `libmujoco.so.3.9.0` under `/home/joe/...`.
  `~/.bashrc` now adds the KD venv's MuJoCo dir to `LD_LIBRARY_PATH`. **Still needed:** Saurabh
  runs `sudo apt install -y libglfw3-dev`. **Done the same day; no missing libraries remain.**
  Also found: an RTX 4050 dGPU, and **only 6.5 GB free on `/`** (8 GB swapfile + snapd). See `03-machines.md`.
- Trial launch with a temporary GLFW worked: 5 nodes, WhyCode markers at 30 Hz, no errors.
  Stopped cleanly with SIGINT.
- Caused an Ubuntu "internal error" popup by stopping `ros2 topic hz` with SIGTERM (`timeout`). It
  is harmless; use `timeout -s INT` from now on.
- Saurabh is sending **all Task 1 material for KD and PacBot**, including YouTube links. He
  suggested installing a tool to read them. Ask permission before installing anything (e.g.
  `yt-dlp`, which can fetch captions/transcripts only). Rebuild the roadmap **once** after
  everything arrives.

### 2026-09-16 · claude-code — Task 1 released

- Saurabh pasted the Task 1 overview and the Task 1A instruction and submission pages →
  `09-task1-overview-and-1a.md`. Task 1 = 1A OpenCV survivors (20) + 1B altitude PID (40) + 1C
  3-axis PID (40). This corrects the earlier assumption that 1B was a full position controller.
- Per the portal: `~/pico_mujoco_ws` → Trash, fresh **`~/pico_ws`** (commit `3318915`, "Task1
  Release"), **all 17 packages build**; Saurabh had installed the two apt packages. Updated
  `~/.bashrc`, the Desktop symlink, and the NEON "ROS 2" terminal profile
  (`~/.local/share/neon-hud/ros2/ros2-env.sh` + `ros2-bashrc` comment).
- **Verified:** apt OpenCV **4.5.4**, so the **old ArUco API** applies (no `ArucoDetector`). There
  is no pip OpenCV. `image_1.jpg` is 800 × 800.
- **Flagged:** the results file is 4 lines (blank line 2) on one page and "exactly three lines" on
  the other; the example marker IDs differ between pages.
- Saurabh said (2026-09-13) he knows only Linux, C++, breadboards and intro Python, and wants to
  learn by doing, talking, teaching and video ladders. The roadmap was restructured to put Task 1A
  (image processing) first and split PID into 1B/1C modules; it is rebuilt as a PDF.

### 2026-09-13/14 (learning roadmap) · claude-code

Saurabh said plainly that ROS 2, Humble, MuJoCo, MQTT and PID are all **new to him**. He already
knows Linux, C++, breadboards and intro Python. He asked why the bonus task was a circle, why the
radius was fixed, and how big the drone is. He wants a roadmap that skips what AI can do and fits
how he learns: talking, doing, teaching, and chained video ladders.

- Built **`LEARNING-ROADMAP.pdf`**, 14 pages: dictionary, modules M0–M6, PacBot track, 53
  clickable checkboxes, fillable learning and tuning logs, 52 links. Every video link was checked
  by web search. At his request it is a PDF, not Markdown and not an Artifact.
- **Simulated Swift Pico facts, from `drone.xml`:** 1.5 kg, 47×47×11 cm collision box, motors
  ±0.19 m, 5.47 N max per motor (hover ≈ 67%), WhyCode marker 0.313 m, top camera 20 m up at 60°
  FOV, 0.005 s RK4 timestep. The **real kit's size is unknown**: the model claims 1:1 scale, but
  the theme says "nano".
- The bridge has **no keyboard flight control** (its keyboard handling only quits), so roadmap
  1C needs a small teleop tool written by Claude. e-Yantra's `controller_tuner/pid_tune` provides
  a Tk slider GUI (Kp 0–5000, Ki 0–1000, Kd 0–5000) publishing `controller_msg/PIDTune`.
- Still pending from Saurabh: `sudo apt install ros-humble-actuator-msgs ros-humble-image-view`
  (it blocks M1-1C), and the e-Yantra learning material, to fill the "[e-Yantra — slot in when
  shared]" rungs.

### 2026-09-13 (bonus task) · claude-code

Saurabh chose to have claude-code set up both workspaces and write the node. **His stated goal is
self-improvement**, so the node is heavily commented and `08-task0-bonus.md` includes a study
section and exercises.

- **Part 1 done.** Built `~/turtlesim_ws`: e-Yantra's turtlesim fork plus the `kd_task_0`
  package with node `task_0_4817.py`. The node is a 50 Hz state machine with P-controllers,
  closes the circle on measured heading, and calls services asynchronously. Verified from logs and
  from pixel measurements of a window capture. r=1.0 gives a ring of 1.001 and parks 0.0099 from
  (5,5). **Found a portal inconsistency:** the text says d=2.0 while the figure shows ~8.0, so the
  radius became a ROS parameter. r=4.0 was verified to match the figure.
- **Part 2 blocked.** `~/pico_mujoco_ws` cloned (`kd_sim`, with submodules); the build failed on
  missing `actuator_msgs`. A dependency scan narrowed the need to 2 apt packages; there is no
  passwordless sudo, so Saurabh has to install them. `.bashrc` source line added.
- **Fixed a hidden numpy clash:** `~/.local` numpy 2.2.6 broke `cv_bridge`, which would have
  crashed `mujoco_bridge`. Downgraded to 1.26.4 and re-verified PB MuJoCo 3.11.0, `cv_bridge` and
  `paho-mqtt`. The KD venv is untouched.
- Symlinks `~/Desktop/e-yantra/{turtlesim_ws,pico_mujoco_ws}` → the real home-level workspaces.
- Corrected an earlier note: this turtlesim fork spawns at (5.0, 2.0), not (5.544, 5.544).

### 2026-09-13 (rearrangement) · claude-code

**All paths in older entries below are pre-move.** Rearranged the Ubuntu box so that everything
eYRC lives under one root, at Saurabh's request. Moves, all on the same filesystem:

| From | To |
|---|---|
| `~/Downloads/e-yantra/` | **`~/Desktop/e-yantra/`** |
| `~/Desktop/drone_ws/` | `~/Desktop/e-yantra/drone_ws/` |
| `~/Desktop/pacbot_ws/` | `~/Desktop/e-yantra/pacbot_ws/` |
| `~/Downloads/bonus_task0.DvemL89h_Z2tLDp8.webp` | `eYRC 2026-27/Media/Task0/bonus_task0.webp` |
| `~/Downloads/pico_drone.D2sM9csf_Z2v87V1.webp` | `eYRC 2026-27/Media/Task0/pico_drone.webp` |

- **`drone_env` venv fixed** with `~/drone_ws → ~/Desktop/e-yantra/drone_ws`. Verified: MuJoCo
  3.9.0 inside, `pip` and `eyantra-autoeval` run, and the system is still 3.11.0 outside.
- `pacbot_ws` git state unchanged: clean apart from the two untracked `4817_task0.*` files.
- Workspaces are deliberately **not** inside `eYRC 2026-27/`, because the space in that name breaks
  colcon/CMake. Layout diagram: `CLAUDE.md` → "Layout on the Ubuntu box".
- `~/Desktop` now holds only `e-yantra/`, and `~/Downloads` is empty of eYRC material.
- **Bonus task brief received** (pasted from the portal) → `08-task0-bonus.md`. This **corrects
  the low-confidence guess below**: `bonus_task0.webp` is the **turtlesim** circle target, drawn
  with the `turtle_sim` branch's drone-shaped turtle. It is not a drone flight.

### 2026-09-13 (later) · claude-code

- Both truncated `e-yantra.zip` files (`~/Downloads`, T9 volume 1) were **moved to Trash** with
  `gio trash`, at Saurabh's request. They are recoverable until the Trash is emptied; the T9 one
  sits in `.Trash-1000` on that volume.
- **Per-theme MuJoCo split confirmed**, and it is intentional: each theme's Task 0 demands its own
  version. KD uses **3.9.0** in the `drone_env` venv; the evaluator hard-requires exactly 3.9.0. PB
  uses **3.11.0** in the system user site, alongside `paho-mqtt` 2.1.0. This corrects my earlier
  guess that it had been "upgraded afterwards".
- **Found that `drone_env` was relocated** from `~/drone_ws` to `~/Desktop/drone_ws`, so its
  `activate`/`pip`/`eyantra-autoeval` still point at the old path. Activating it silently gives
  MuJoCo 3.11.0. Documented in `03-machines.md` with fix options; **not fixed yet**.
- **Bonus task at the end of Task 0 is pending, with nothing done**, and it is not described
  anywhere in this folder. Portal images in `~/Downloads`: `bonus_task0.*.webp` shows a top-down
  view of a quadcopter at the centre of a white circle. *[INFERRED, low confidence: possibly a
  circle-flying or hover-inside-a-boundary exercise — do not plan from this; get the text.]*
  `pico_drone.*.webp` shows the Swift Pico model in the MuJoCo viewer.

### 2026-09-13 · claude-code (first session on Ubuntu)

The folder arrived on the Ubuntu box as `~/Downloads/e-yantra.zip`, but the zip was **truncated**:
there was data only up to 98 MiB of 129.6 MiB, the rest was zero-filled, and there was no central
directory. A local-header walk recovered `CLAUDE.md`, all of `context/`, `eYRC 2025-26/Backups/`
and the RL workspace, every file CRC-verified. Lost: `CropDrop bot.docx` (cut off mid-file) and
whatever followed it in the archive, which includes `eYRC 2026-27/` and `_extracted/`.

**Resolved the same day.** The T9 volume 1 copy of `e-yantra.zip` turned out to be a separately
built zip that is even more truncated (data only to 56 MiB). Both zips end in zero-filled space at
an exact MiB boundary. *[INFERRED]* That is the signature of a write that never finished flushing,
such as unplugging the drive without ejecting. Saurabh then put the **unzipped folder on T9
volume 2**. All 87 files verified: every docx/zip CRC-clean, image and PDF end markers intact, and
byte-identical to the salvaged files wherever the two overlap. Merged into `~/Downloads/e-yantra`
with `rsync --ignore-existing`, which kept this session's edits to `CLAUDE.md`, `03-machines.md`
and this file. `eYRC 2026-27/` is a git repo with **no commits**; everything in it is untracked.

**[DOC-SOURCED from evaluator output] Task 0 has been run on this machine for both themes,
2026-09-12:**
- **KD** — `~/Desktop/drone_ws/task0/result-2026-KD-0-20260912.json`: Ubuntu 22.04.5 x86_64, not
  virtualised or dockerised, `ros_humble_desktop_installed: true`, ROS `humble`, MuJoCo `3.9.0`,
  Python `3.10.12`, `generate: true`. A `drone_env` venv sits next to it.
- **PB** — `~/Desktop/pacbot_ws` is a clone of `eYantra-Robotics-Competition/eYRC_26-27_PacBot`
  (upstream commit "Task 0 Evaluator Added"). Running `task0/task0_eval` produced
  `4817_task0.json` (libsodium sealed box, team 4817) and `4817_task0.zip`. Both are untracked in
  git, which is correct: **do not commit or push them** to the e-Yantra repo. The payload is
  encrypted, so **pass/fail cannot be read from the file**. Since the same machine's KD checks are
  all green, a pass is likely *[INFERRED]*. I did not re-run the evaluator; it is interactive and
  asks for a team ID.

**Unknown, so ask:** whether either file was uploaded to the portal; whose machine this is (AMD
Ryzen 7 7840HS, not the HP Pavilion on record for Saurabh); whether Task 0 must be run per member.
Machine measured once and recorded in `03-machines.md`, which also covers the 48.8 GB root
partition risk. The brain's `STATE.md` is not reachable from this machine, so it was **not**
updated. Do that at the next Windows/Obsidian checkpoint.

### 2026-09-12 (third drop) · claude-code

Turtlesim, MuJoCo, Quadcopters and the **Swift Pico** pages handed over. **The Swift Pico tutorial
names Task 1B outright** — it is a PID position controller in MuJoCo: subscribe `/rotors/odometry`,
publish `/drone_command` (`swift_msgs/msg/SwiftMsgs`, RC 1000–2000 centred on 1500, `rc_aux4: 2000`
arms). Written up as `07-swift-pico-interface.md`; MuJoCo and quadcopter triage folded into
`06-prelearnings.md`. The earlier WhyCon inference is now superseded for Stage 1 — right about
*what*, wrong about the mechanism (odometry in sim, WhyCon on hardware later).

Also noted: the portal says "complete the **Installations part of Task 1B**" as a prerequisite, so
Task 1 material exists on the portal and has not been handed over yet. The MuJoCo tutorials include
an **LQR control Colab**, matching the theme spec's "PID / LQR" — the natural after-PID step.

### 2026-09-12 (later) · claude-code

Saurabh handed over the portal's **ROS 2 prelearnings** section. Triaged into
`06-prelearnings.md`. Three decision-changing findings: **(a)** the distro is **ROS 2 Humble**, which
hard-locks **Ubuntu 22.04** — installing 24.04 would break everything; **(b)** the section is titled
"ROS 2 & MuJoCo", so MuJoCo not Gazebo looks like the simulator, which defuses the Arc iGPU concern;
**(c)** `ROS_DOMAIN_ID` collisions will bite a 4-person team on one Wi-Fi unless each member sets a
unique ID. **Still awaiting: the Linux section, the MuJoCo page, and the actual Task 0 instructions.**

### 2026-09-12 · claude-code

Read the whole folder and the brain's e-yantra notes cold — 11 tool calls, roughly 13k tokens,
because the folder had no entry point. Built `CLAUDE.md` plus this `context/` tier so the next
session is a zero-call read. Recorded Saurabh's machine specs and the dual-boot plan. Flagged the
WhyCon-to-PID inference as the highest-value prep signal.

**Found a contradiction in the brain's `STATE.md`:** line 684 says payment CONFIRMED, line 687 still
says `blocked: **payment**`, and the `deep:` link points at a note titled "…payment pending". Needs
fixing at checkpoint.

### 2026-08-29 · antigravity

Verified the team portal. Payment confirmed, roster 4/4 active (Gauri logged in, Mahesh accepted the
invite). Moved all e-Yantra files into `F:\e-yantra` and structured them year-wise. Wrote the theme
comparison matrix into the brain.

### 2026-08-25 · claude-code

Phone audit found the portal dashboard screenshot that corrected a three-week-stale brain entry —
the real state was a registered team with money owed, not the two unread docx files STATE claimed.
