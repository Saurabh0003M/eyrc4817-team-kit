# 00 — START HERE: Team 4817 · eYRC 2026-27 · Task 1

**Read this first.** It says what Task 1 is, who does what now, the plan to the 5 Oct deadline, and which file to open next.

## Team

| | |
|---|---|
| Team ID | **4817** (appears in every submission file name) |
| College | G.H. Raisoni College of Engineering & Management, Pune |
| Members | **Gauri S Nanaware**: Team Leader, Electrical, 3rd year. **Only she can upload submissions** on the portal · **Saurabh Tomke** · **Parth S Hingankar** · **Mahesh B Ugale**: all Cyber Security, 3rd year |
| Themes | **Khoj-o-Drone (KD)**, primary: a drone searches a disaster zone for survivors · **PacBot (PB)**, secondary: a Pac-Man-style robot in a maze. The team must do both until Task 2/3, then e-Yantra lets us keep one |
| Portal | https://portal.e-yantra.org/courses/theme_kd and https://portal.e-yantra.org/courses/theme_pb (login needed) |
| Team repo | https://github.com/Saurabh0003M/eyrc4817-team-kit (setup script + checker tools) |
| **Task 1 deadlines** (portal "All deadlines", soft, 11:59 pm) | KD 1A **21 Sep** (submitted) · PB 1A **23 Sep** (submitted) · KD 1B **28 Sep** · KD 1C **5 Oct** · PB 1B **5 Oct** |
| **Status (1 Oct)** | **KD 1B recorded: 40/40 estimated** (gains in `09_Team_Results_PRIVATE.md`; upload pending — past 28 Sep, check the slot). Next: **KD 1C** and **PB 1B** by 5 Oct |

## Task 1 = five subtasks, 200 marks

| # | Subtask | What you do | Code or tune? | Marks | Difficulty for beginners | File |
|---|---|---|---|---|---|---|
| 1 | **KD 1A** Find survivors | Python + OpenCV reads one photo of the arena and writes which grid points (like `D2`) have red (critical) and yellow (stable) survivors | write code | 20 | medium | `01_KD_Task1A_Survivor_Detection.md` |
| 2 | **KD 1B** Hold height | Tune 3 PID numbers so the simulated drone holds a fixed altitude | tune only | 40 | easy–medium | `02_KD_Task1B_1C_PID_Tuning.md` |
| 3 | **KD 1C** Hold position | Tune pitch and roll PID numbers so the drone also holds x and y | tune only | 40 | medium | `02_KD_Task1B_1C_PID_Tuning.md` |
| 4 | **PB 1A** Maze path planning | Python sends one move at a time over MQTT to eat 2 pellets and exit a grid maze | write code | 35 | medium | `03_PB_Task1A_Maze_Path_Planning.md` |
| 5 | **PB 1B** Wall following | Python + PID drives a robot through a 3D MuJoCo maze without touching walls | write code | 65 | hard | `04_PB_Task1B_Wall_Following.md` |

KD Task 1 total = 100 (20 + 40 + 40). PB Task 1 total = 100 (35 + 65).

## Who does what now (1 Oct)

| Subtask | Status | Owner (agreed 24 Sep; the team can change it) |
|---|---|---|
| KD 1A, PB 1A | Submitted | — |
| KD 1B | Recorded, 40/40 estimated. **Gauri uploads** | Saurabh tuned it on Gauri's laptop |
| **KD 1C** | Not started | Saurabh tunes; anyone can learn along with `02_KD_Task1B_1C_PID_Tuning.md` |
| **PB 1B** | A first draft runs on Gauri's laptop (13 clean turns in practice, no exit yet) | Saurabh |

Only Gauri can upload. Only Gauri's laptop (HP OMEN, Ubuntu 22.04) is fully set up; the other laptops are not
recorded yet (`B3_Background_Team_Setup_Log.md` → 03-machines).

## Plan to the 5 Oct deadline (Thu 1 → Mon 5 October, 11:59 pm)

| Day | KD 1C | PB 1B | Everyone |
|---|---|---|---|
| **Thu 1** | Launch sim + `task_1c_controller` with the 1B throttle gains (`09_Team_Results_PRIVATE.md`); confirm height hold | Run the draft with `--evaluate`; note exactly where it fails | Gauri uploads the KD 1B zip + YouTube link |
| **Fri 2** | Tune pitch = roll together, testing from a **fresh takeoff** each time | Fix the failure found on Thu (corners / exit) | |
| **Sat 3** | Score practice bags (`bag_score.py 1c task_1c`); aim for 40/40 est. with margin | Full `--evaluate` runs: zero collisions, reaches the exit | Test the screen recording |
| **Sun 4** | **Record** the 1C bag + video; score before zipping; zip | **Record** the evaluate run + video; coding standard; zip; checker tool | **Everything final tonight** |
| **Mon 5** | | | **Gauri uploads both early in the day** |

## Open questions to ask on the e-Yantra forum (the portal doesn't answer these)

1. Uploads after a "soft" deadline (KD 1B's was 28 Sep): still accepted, and with what penalty?
2. KD 1B/1C scoring: when does the 15-second clock start? (Our 1B tests reach the box ~2.5 s after takeoff, so for a well-tuned drone it hardly matters.)
3. PacBot 1A and 1B both use the zip name `PB#4817.zip`: separate upload slots, correct?

## Files in this project

| File | Open it when |
|---|---|
| `00_START_HERE.md` | first |
| `01_KD_Task1A_Survivor_Detection.md` | working on KD 1A |
| `02_KD_Task1B_1C_PID_Tuning.md` | working on KD 1B or 1C |
| `03_PB_Task1A_Maze_Path_Planning.md` | working on PB 1A |
| `04_PB_Task1B_Wall_Following.md` | working on PB 1B |
| `05_Setup_Run_Submit.md` | setting up a laptop, running anything, submitting, troubleshooting, coding standard |
| `06_Concepts_Explained.md` | any word or idea is unclear (PID, ROS 2, MQTT, HSV, BFS…) |
| `07_Learning_Resources.md` | looking for a video, doc or portal link |
| `08_Portal_Learnings_Summary.md` | what e-Yantra's learning pages say, and the mistakes we found in them |
| `09_Team_Results_PRIVATE.md` | you need our own graded numbers (KD 1B gains). **Never copy them outside this project** |
| `B1_Background_Khoj_o_Drone.md` · `B2_Background_PacBot.md` · `B3_Background_Team_Setup_Log.md` | you need deeper detail: the team's raw notes per theme, the machines and the dated task log. Written for another AI assistant; the numbered files above win when they disagree |

## Rules that can cost the whole team

- **Plagiarism check on every submission.** Write your own code. Use ChatGPT to learn and debug, not to generate the answer file.
- **Never open or modify** the PacBot `task_1a_launch` / `task_1b_launch` programs (tampering = disqualification).
- **Never rename** the PacBot boilerplate functions.
- **Follow the e-Yantra Coding Standard** in every submitted code file.
- Videos on YouTube must be **Unlisted** (not Private), one unbroken take.
