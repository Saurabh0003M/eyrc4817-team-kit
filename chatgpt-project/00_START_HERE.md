# 00 — START HERE: Team 4817 · eYRC 2026-27 · Task 1

**Read this first.** It says what Task 1 is, who does what, the 6-day plan, and which file to open next.

## Team

| | |
|---|---|
| Team ID | **4817** (appears in every submission file name) |
| College | G.H. Raisoni College of Engineering & Management, Pune |
| Members | **Gauri S Nanaware**: Team Leader, Electrical, 3rd year. **Only she can upload submissions** on the portal · **Saurabh Tomke** · **Parth S Hingankar** · **Mahesh B Ugale**: all Cyber Security, 3rd year |
| Themes | **Khoj-o-Drone (KD)**, primary: a drone searches a disaster zone for survivors · **PacBot (PB)**, secondary: a Pac-Man-style robot in a maze. The team must do both until Task 2/3, then e-Yantra lets us keep one |
| Portal | https://portal.e-yantra.org/courses/theme_kd and https://portal.e-yantra.org/courses/theme_pb (login needed) |
| Team repo | https://github.com/Saurabh0003M/eyrc4817-team-kit (setup script + checker tools) |
| **Task 1 deadline** | **23 September 2026** (confirm the exact time on the portal) |

## Task 1 = five subtasks, 200 marks

| # | Subtask | What you do | Code or tune? | Marks | Difficulty for beginners | File |
|---|---|---|---|---|---|---|
| 1 | **KD 1A** Find survivors | Python + OpenCV reads one photo of the arena and writes which grid points (like `D2`) have red (critical) and yellow (stable) survivors | write code | 20 | medium | `01_KD_Task1A_Survivor_Detection.md` |
| 2 | **KD 1B** Hold height | Tune 3 PID numbers so the simulated drone holds a fixed altitude | tune only | 40 | easy–medium | `02_KD_Task1B_1C_PID_Tuning.md` |
| 3 | **KD 1C** Hold position | Tune pitch and roll PID numbers so the drone also holds x and y | tune only | 40 | medium | `02_KD_Task1B_1C_PID_Tuning.md` |
| 4 | **PB 1A** Maze path planning | Python sends one move at a time over MQTT to eat 2 pellets and exit a grid maze | write code | 35 | medium | `03_PB_Task1A_Maze_Path_Planning.md` |
| 5 | **PB 1B** Wall following | Python + PID drives a robot through a 3D MuJoCo maze without touching walls | write code | 65 | hard | `04_PB_Task1B_Wall_Following.md` |

KD Task 1 total = 100 (20 + 40 + 40). PB Task 1 total = 100 (35 + 65).

## Who does what (proposal, the team decides)

With 6 days, work in parallel. One owner per subtask, a helper for the hard one, and everyone understands PID.

| Owner | Subtask | Why |
|---|---|---|
| Gauri | KD 1B → KD 1C (tuning) | PID is her Electrical coursework; tuning needs no coding |
| Mahesh | KD 1A (OpenCV) | Image-processing pipeline |
| Parth | PB 1A (maze planning) | Python + search algorithm |
| Saurabh | PB 1B (wall following) + helps others | Hardest subtask, highest marks |

Everyone: set up the laptop (day 1), watch the PID videos (see `07_Learning_Resources.md`), and explain your subtask to one teammate before submitting.

## 6-day plan (Fri 18 → Wed 23 September)

Everything is **final on Tue 22**, so the deadline day is only for uploading.

| Day | Everyone | KD 1A | KD 1B/1C | PB 1A | PB 1B |
|---|---|---|---|---|---|
| **Fri 18** | Laptop setup (`05_Setup_Run_Submit.md`); **test screen recording**; read your subtask file; post the forum questions (below) | Look at `image_1.jpg`; learn pixels/HSV | Watch PID videos; launch sim + tuner | Learn BFS; watch MQTT messages | Watch PID videos; launch sim, read sensor values |
| **Sat 19** | Short team check-in | Markers + perspective transform | Tune KD 1B | Drive the bot by hand with `mosquitto_pub`; write BFS | P-controller on side distance |
| **Sun 20** | | Grid + names + colour masks | Record KD 1B bag + video; start KD 1C | Turn logic + first full run | Add D (and I); corners with the gyro |
| **Mon 21** | Short team check-in | Centres + nearest intersection + results file | Tune KD 1C | Pellet order + exit; coding standard comments | Reduce collisions; full maze runs |
| **Tue 22** | **Submission dry runs** + checker tool; **everything final tonight** | Coding standard; harder images; final file + zip | Record KD 1C bag + video; zips ready | Evaluate run + video; zip ready | Coding standard; evaluate run + video; zip ready |
| **Wed 23** | **Gauri uploads everything early in the day** | | | | |

## Open questions to ask on the e-Yantra forum (the portal doesn't answer these)

1. Exact deadline time on 23 September.
2. KD 1A results file: 3 lines or 4? The instruction page shows an empty line 2; the submission page says "exactly these three lines".
3. KD 1A: are the marker IDs always 80, 85, 90, 95? The submission page example shows 10, 15, 20, 25.
4. KD 1B/1C scoring: when does the 15-second clock start? Are hover seconds continuous or total?
5. PacBot 1A and 1B both use the zip name `PB#4817.zip`: separate upload slots, correct?

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

## Rules that can cost the whole team

- **Plagiarism check on every submission.** Write your own code. Use ChatGPT to learn and debug, not to generate the answer file.
- **Never open or modify** the PacBot `task_1a_launch` / `task_1b_launch` programs (tampering = disqualification).
- **Never rename** the PacBot boilerplate functions.
- **Follow the e-Yantra Coding Standard** in every submitted code file.
- Videos on YouTube must be **Unlisted** (not Private), one unbroken take.
