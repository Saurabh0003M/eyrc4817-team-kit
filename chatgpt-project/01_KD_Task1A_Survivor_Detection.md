# 01 — Khoj-o-Drone Task 1A: Find survivors in a photo (20 marks)

Source: e-Yantra portal, KD → Stage 1 → Task 1 → Task 1A Instruction + Submission. The portal is the final authority.

## In one sentence

Write **one Python script** that reads a photo of the arena and writes a small text file listing which **grid intersections** have a **red triangle (critical survivor)** or a **yellow circle (stable survivor)**.

## The arena (what's in the photo)

- **4 ArUco markers** (square black-and-white codes, like tiny QR codes) sit at the four corners, **outside** the playing field. Dictionary **4x4 (250)**, marker **IDs 80, 85, 90, 95**.
- The field has **white grid lines**: **12 × 12 equal cells**, so **11 × 11 = 121 inner intersections**.
- Survivors stand **on intersections**, not inside cells. 🔴 red triangle = Critical, 🟡 yellow circle = Stable.
- Distractors: black cuboids (obstacles), green foliage, blue terrain. They are **not** survivors.
- The photo may be taken **at an angle**, so the arena looks like a tilted, squashed square.
- Starter files: `~/pico_ws/src/swift_pico/scripts/task1a.py` (almost empty) and `image_1.jpg` (800 × 800).

## Intersection names (graded exactly)

- Column letter **A–K**, left → right; row number **1–11**, top → bottom.
- Top-left is **A1**, bottom-right is **K11**.
- No padding, no space, no separator: `C2` ✔. `c2`, `C02`, `C-2` ✘.

## The 7-step pipeline (the portal's steps)

**The rule that saves hours:** after every step, **draw or print the result and look at it** before moving on.

| Step | Goal | Concepts to learn | Checkpoint |
|---|---|---|---|
| 1. Find markers | Detect the 4 ArUco markers: ID + 4 corner points each. **If any of 80/85/90/95 is missing, print a message and stop** | ArUco detection with the **old OpenCV 4.5.4 API** | Print the IDs; draw the detections once |
| 2. Straighten the arena | Perspective transform so the **playing field only** fills exactly **900 × 900** px (no markers, no title) | Perspective transform: 4 source points → 4 destination points. Which 4 of the 16 marker corners bound the field? What happens if two points are swapped? | Grid lines run perfectly horizontal/vertical; field edges touch the image edges |
| 3. Grid as numbers | Compute (or detect) where the 11 inner lines are | 900 px / 12 cells = ? px per cell | Draw your grid in green: it must sit on the painted lines within 1–2 px. If it drifts, fix step 2 |
| 4. Name intersections | Map every intersection to a name A1…K11 | Loops, string building | Print names on the image: A1 top-left, K11 bottom-right |
| 5. Find survivors | Two colour masks (red, yellow), then contours (outlines) | BGR → **HSV**, `cv2.inRange`, `cv2.findContours`; **red needs two hue ranges** (it wraps around 0/180) | Number of outlines = number of survivors you can see |
| 6. One point per survivor | The centre of each outline; must work for triangles and circles, and **must not crash on zero area** | Image moments / centroid | One dot inside each survivor |
| 7. Nearest intersection | Name each centre by its **nearest** intersection (not the cell it's in); handle centres near the edge without crashing | Distance / rounding | Keep a **composite debug image**: arena + grid + outlines + dots + names |

## Traps we found

1. **OpenCV 4.5.4 = old ArUco API.** `cv2.aruco.ArucoDetector` does not exist on our laptops; most online code uses it and crashes. Use `cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)` (or `Dictionary_get`), `cv2.aruco.DetectorParameters_create()`, `cv2.aruco.detectMarkers(...)`.
2. **Never `pip install opencv-python`**: it breaks ROS 2. OpenCV comes from apt.
3. **OpenCV stores colours as BGR, not RGB**, and **OpenCV hue runs 0–179** (half of 0–359).
4. **Red wraps around**: it sits near hue 0 *and* near 180, so combine two masks.
5. **Portal pages disagree** on the results file: the instruction page shows an empty line 2 (4 lines); the submission page says "exactly these three lines". Ask on the forum; until then follow the instruction page.
6. The submission page's example shows marker IDs `[10, 15, 20, 25]`, the instructions say 80/85/90/95. Don't hard-code IDs into the output; print what you detect.
7. Tune on `image_1.jpg`, but **the evaluator uses 2 different hidden images**: nothing may be specific to `image_1.jpg`.

## How the program must run

```bash
python3 task1a.py --image image_1.jpg
```

- The image path comes from **`--image`**, read with Python's **argparse**. No hard-coded file name.
- If the image can't be loaded: print a clear error naming the path, then exit.
- **No GUI in the submitted file**: no `cv2.imshow`, `cv2.waitKey`, `input()`, or plots. A script that waits for a key is marked failed. Use them while developing, then remove them.
- Must run start to finish on any arena image without edits.

## Output file (exact format)

Name: input file name without extension + `_results.txt`, **in the same folder as the image** (`image_1.jpg` → `image_1_results.txt`; `images/arena_test.png` → `images/arena_test_results.txt`). Overwrite if it exists.

```
Detected marker IDs: [80, 85, 90, 95]

Critical Survivors: F2, C6, D9
Stable Survivors: D2, G6, E8
```

- Line 1: `Detected marker IDs: ` + a Python-style list (square brackets, comma + space).
- Line 2: empty (see trap 5).
- `Critical Survivors: ` and `Stable Survivors: ` lines. Labels separated by comma + one space.
- If a category has none, keep the line with nothing after `: `.
- Nothing else in the file; debug prints go to the terminal. Order inside a line doesn't matter (compared as sets).
- (The labels above are only an example.)

## Scoring (20 marks)

2 hidden test images × 10 marks each. Per image: marker IDs line **4**, Critical line **3**, Stable line **3**. **Each line is all-or-nothing** (2 of 3 survivors right = 0 for that line). **SUCCESS status needs at least one image fully correct.**

## Submission

1. Rename the script to **`KD_4817_task1a.py`**.
2. Add the **e-Yantra Coding Standard** comments (see `05_Setup_Run_Submit.md`).
3. Zip **the file itself**, not a folder: `zip KD_4817.zip KD_4817_task1a.py`.
4. **Gauri uploads** it in the Task 1A slot. One language only (Python *or* C++, not both).

The C++ route also exists: `g++ -std=c++17 task1a.cpp -o task1a $(pkg-config --cflags --libs opencv4)` then `./task1a image_1.jpg`.

## Learning path (about 2 days)

1. Watch: *Digital Images — Computerphile* (image = grid of numbers).
2. Read: portal *Image Processing Basics* (BGR, HSV, hue 0–179).
3. Watch (only these chapters): freeCodeCamp *OpenCV Course*: reading images, drawing, colour spaces, thresholding, contours.
4. Watch: *Warp Perspective / Bird View* (short).
5. Read: PyImageSearch *Detecting ArUco markers with OpenCV and Python* (old API = matches our OpenCV).
6. Keep open: OpenCV tutorials *Changing Colorspaces*, *Geometric Transformations*, *Morphological Transformations*, *Contours*.

Links for all of these: `07_Learning_Resources.md`.

## Helper tools in the team repo (`learning/tools/`)

- `pixel_detective.py`: click the photo to see BGR and HSV values.
- `hsv_tuner.py`: sliders to find HSV ranges that keep only red or only yellow.
- `kd1a_testbench.py --script <your file>`: runs your script on tilted, rotated, darker, blurred versions of the arena; your answers should stay the same.
- `submission_check.py kd1a --file KD_4817_task1a.py`: checks name, coding standard, no GUI calls, results format.
