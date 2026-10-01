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
| **Marks (1 Oct, portal)** | **KD 1A 20/20 · KD 1B 40/40 · KD 1C 40/40 (KD = 100/100) · PB 1A 35/35.** **PB 1B recorded 1 Oct (65/65 est.)**: Gauri uploads `PB#4817.zip` + video before 5 Oct |

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
| KD 1A, PB 1A | **Marked 20/20 and 35/35** | — |
| KD 1B | **Marked 40/40** | Saurabh (tuned with Claude) |
| **KD 1C** | **Marked 40/40** (gains in `09_Team_Results_PRIVATE.md`) | Saurabh (tuned with Claude) |
| **PB 1B** | **Recorded 1 Oct, 65/65 est.** (0 collisions). **Gauri uploads** | Saurabh (with Claude) |

Only Gauri can upload. Only Gauri's laptop (HP OMEN, Ubuntu 22.04) is fully set up; the other laptops are not
recorded yet (`B3_Background_Team_Setup_Log.md` → 03-machines).

## Plan to the 5 Oct deadline (Thu 1 → Mon 5 October, 11:59 pm)

Only PB 1B is left. **Submit before the deadline**: on-time uploads earn e-Ratna (PB 1A got +11); late ones are
still marked but show "Late, not eligible".

| Day | PB 1B | Everyone |
|---|---|---|
| **Thu 1** | ✅ Recorded + zipped (`PB#4817.zip`, video `PB_4817_Task1B_20261001_124141.webm`) | |
| **Fri 2** | **Gauri uploads** in the PB Task 1B slot + the Unlisted YouTube link | Read up for Task 2 when it is released |
| **Mon 5** | Deadline, 11:59 pm (nothing should be left for this day) | |

## Open questions to ask on the e-Yantra forum (the portal doesn't answer these)

1. KD 1B/1C scoring: when does the 15-second clock start? (Answered in practice: both scored 40/40.)
2. ~~Uploads after a "soft" deadline~~ Answered by the portal: accepted and marked, but "Late, not eligible" for e-Ratna.
3. ~~PacBot 1A and 1B both use `PB#4817.zip`~~ The portal has a separate upload slot per subtask.

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
| `09_Team_Results_PRIVATE.md` | you need our own graded results (KD 1B/1C gains, the PB 1B maze note). **Never copy them outside this project** |
| `B1_Background_Khoj_o_Drone.md` · `B2_Background_PacBot.md` · `B3_Background_Team_Setup_Log.md` | you need deeper detail: the team's raw notes per theme, the machines and the dated task log. Written for another AI assistant; the numbered files above win when they disagree |

## Rules that can cost the whole team

- **Plagiarism check on every submission.** Write your own code. Use ChatGPT to learn and debug, not to generate the answer file.
- **Never open or modify** the PacBot `task_1a_launch` / `task_1b_launch` programs (tampering = disqualification).
- **Never rename** the PacBot boilerplate functions.
- **Follow the e-Yantra Coding Standard** in every submitted code file.
- Videos on YouTube must be **Unlisted** (not Private), one unbroken take.
