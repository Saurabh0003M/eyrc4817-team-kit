# Task 1 — overview, and Task 1A (find survivors in a photo)

Source: KD portal, Stage 1 → Task 1 (Overview, Task 1A Instruction, Task 1A Submission). Saurabh
pasted it on 2026-09-16, with the five figures. This is a distilled copy; **the portal is the
authority**. **Deadline: UNKNOWN — ask.** *[INFERRED]* The schedule gives Task 1 about 4 weeks,
which means roughly mid-October.

## Task 1 structure [DOC-SOURCED]

| Subtask | What | Marks |
|---|---|---|
| **1A** | Image processing: find survivors in one photo and classify them as critical or stable | 20 |
| **1B** | PID: hold the drone at a **fixed altitude** | 40 |
| **1C** | PID: stabilise the drone in **all three axes** | 40 |

Attempt them in order. This **supersedes earlier notes** that described "Task 1B" as a full
position controller: 1B is altitude only, and the x/y part is 1C. **80 of the 100 marks are
PID.**

## Setup changes [DOC-SOURCED, done 2026-09-16]
- The portal says: delete `~/pico_mujoco_ws` and use a **fresh `~/pico_ws`** ("we've fixed some bugs").
  Done: the old one is in Trash, `~/pico_ws` is cloned at commit `3318915` ("Task1 Release"), and
  **all 17 packages build**. `~/.bashrc` now sources `~/pico_ws/install/setup.bash`, the
  Desktop symlink `e-yantra/pico_ws` was added, and the NEON "ROS 2" terminal profile
  (`~/.local/share/neon-hud/ros2/ros2-env.sh`) was switched to `pico_ws`.
- Saurabh installed `ros-humble-actuator-msgs` and `ros-humble-image-view`, which unblocks the bonus
  Part 2 sim.
- **Only OpenCV + NumPy are allowed**, installed via apt: `python3-opencv 4.5.4`. **Never
  `pip install opencv-python`**, because it breaks ROS 2. Verified: there is no pip OpenCV on the
  box. The NumPy in use is 1.26.4 from `~/.local`, see `08-task0-bonus.md`.
- Starter files: `~/pico_ws/src/swift_pico/scripts/task1a.py` (just a comment) and
  `image_1.jpg` (**800 × 800**).

## Task 1A spec [DOC-SOURCED]

**Arena:** 4 ArUco corner markers (dictionary **4x4_250**, IDs **80, 85, 90, 95**) sit *outside*
the playing field. The field has painted white grid lines making **12 × 12 equal cells**, which
gives **11 × 11 = 121 interior intersections**. Survivors stand **on intersections**. 🔴 Red
triangle = **Critical**, 🟡 yellow circle = **Stable**. Black cuboids, green foliage and blue
terrain are distractors.

**The 7-step pipeline.** At every step, *display the result and check it* before moving on:
1. Detect the markers: get IDs and 4 corners each. If any of the 4 is missing, **say so and stop**.
2. Perspective-transform the field (field only, no markers) to exactly **900 × 900**. *Portal
   prompt:* of the 16 marker corners, which 4 bound the field? What happens if you swap the order
   of two points?
3. Grid: detect it or compute it. Draw it on the image; it must sit on the paint within 1–2 px. If
   it drifts, the problem is step 2.
4. Names: column letter **A–K left→right**, row **1–11 top→bottom**. A1 top-left, K11 bottom-right.
   No padding or separator: `C2`, never `c2`, `C02` or `C-2`.
5. Colour masks, red and yellow separately, then contours. The contour count must equal the
   survivors you can see.
6. One centre per survivor. It must work for a circle **and** a triangle, and **not crash on zero
   area**.
7. **Nearest** intersection, not the containing cell. Guard centres near the edge: no crash and no
   nonsense label. **Keep one composite debug image:** grid + outlines + dots + labels.

**Output file:** `<image stem>_results.txt` in the **same folder as the input image**, overwritten
if it exists:
```
Detected marker IDs: [80, 85, 90, 95]

Critical Survivors: F2, C6, D9
Stable Survivors: D2, G6, E8
```
Separator is `, `. An empty category keeps its line (`Critical Survivors: ` with nothing after).
Nothing else goes in the file; debug output goes to the terminal. Order doesn't matter, because
the evaluator compares sets.

**Running:** `python3 task1a.py --image image_1.jpg` via **argparse**. Fail loudly if the image
doesn't load. **No `imshow`, `waitKey`, `input()` or GUI in the submission**; a blocking script is
marked failed. No hard-coded image name; it must work on any arena image.

**Submission:** rename to `KD_4817_task1a.py` and zip **the file itself**, not a folder, as
`KD_4817.zip`. One language only. **Only the Team Leader (Gauri) can upload.** The code is checked
by plagiarism software.

**Scoring:** 2 hidden test images × 10 marks. Per image: marker IDs line 4, Critical line 3,
Stable line 3, and **each line is all-or-nothing**. **Pass (SUCCESS) needs at least one image
fully correct.**

## Traps and contradictions found [VERIFIED / FLAGGED 2026-09-16]
1. **OpenCV 4.5.4 uses the OLD ArUco API [VERIFIED on this machine].** `cv2.aruco.ArucoDetector`
   does not exist (it arrived in 4.7). What exists: `cv2.aruco.detectMarkers`,
   `cv2.aruco.getPredefinedDictionary` / `Dictionary_get`, `DetectorParameters_create`. Most
   code online uses the new API and will crash. Read the **4.5.4** docs.
2. **3 lines or 4?** The instruction page shows line 2 as *empty* (4 lines). The submission page
   says "exactly these three lines" and shows no blank line. **Ask on the e-Yantra forum.**
   Until answered, follow the instruction page, which is the detailed spec.
3. **Marker IDs:** the instruction says 80/85/90/95; the submission page example shows
   `[10, 15, 20, 25]`, labelled "example". *Design question for Saurabh:* tie each corner to a
   marker ID, or to the marker's *position* in the photo? Think about what breaks in each case.
4. `image_1.jpg` is 800 × 800, but the rectified canvas must be 900 × 900.
5. The portal's figure 5 caption asks for the **nearest intersection**, not the cell, so rounding
   beats flooring.

## Learning plan
Roadmap module **M1 — How a computer sees (Task 1A)** in `LEARNING-ROADMAP.pdf`. Saurabh writes
steps 1–7 and the results-file writer. Claude provides the tools (pixel detective, HSV tuner, test
bench, format checker), reviews, and runs checks. **Do not hand Saurabh a finished solution:** his
goal is learning, and submissions are plagiarism-checked.
