# 07 — Learning resources: every link from the portal

## Watch-first list for the 23 September deadline (≈ 1 day of learning per subtask)

| Subtask | In this order |
|---|---|
| **Everyone** | [PID Control — A brief introduction](https://www.youtube.com/watch?v=UR0hOmjaHp0) (8 min) → [What Is PID Control? Part 1](https://www.youtube.com/watch?v=wkfEZmsQqiA) (MATLAB) → portal *PID Controller* page + ball-and-beam demo |
| **KD 1A** | [Digital Images — Computerphile](https://www.youtube.com/watch?v=06OHflWNCOE) → portal *Image Processing Basics* → [OpenCV Course (freeCodeCamp)](https://www.youtube.com/watch?v=oXlwWbU8l2o): reading images, drawing, colour spaces, thresholding, contours only → [Warp Perspective / Bird View](https://www.youtube.com/watch?v=Tm_7fGolVGE) → [Detecting ArUco markers (PyImageSearch, old API)](https://pyimagesearch.com/2020/12/21/detecting-aruco-markers-with-opencv-and-python/) |
| **KD 1B/1C** | [A PID Tuning Guide — Part 4](https://www.youtube.com/watch?v=sFOEsA0Irjs) → [Tuner and Plotter demo](https://youtu.be/ef2SI6uARuA) → [Drone flight physics in under 2 minutes](https://www.youtube.com/watch?v=iQAPkN7OWus) → [task 1b submission demo](https://youtu.be/xqOyre-afOE) / [task 1c submission](https://youtu.be/Ut5wKqhMFdM) |
| **PB 1A** | portal *Path Planning* page → [Dijkstra — Computerphile](https://www.youtube.com/watch?v=GazC3A4OQTE) → [A* — Computerphile](https://www.youtube.com/watch?v=ySN5Wnu88nE) → portal *MQTT* + *MQTT Concepts* → [expected output video](https://youtu.be/95Kb59pPsXU) |
| **PB 1B** | [A PID Tuning Guide — Part 4](https://www.youtube.com/watch?v=sFOEsA0Irjs) → portal *MQTT* page → portal *MuJoCo* overview → [expected output video](https://youtu.be/Ac7dU4j0nVs) |

Everything else below is for going deeper or for later tasks.


Collected from the Khoj-o-Drone (KD) and PacBot (PB) portal pages shared on 2026-09-16, organised the
same way as the portal. **Use for** tells you which Task 1 subtask it helps (KD = Khoj-o-Drone, PB = PacBot).

- 🔒 = on the portal; you must be logged in (these files are e-Yantra's and are **not** in this repo).
- ⭐ = do this first; the rest is reference.
- Links are checked with `python3 learning/tools/check_links.py`.

**Contents:** [1 Portal pages](#1-portal-pages-login) · [2 Task videos](#2-task-videos) ·
[3 ROS 2](#3-ros-2) · [4 MuJoCo](#4-mujoco) · [5 Quadcopters](#5-quadcopters) ·
[6 Control systems & PID](#6-control-systems--pid) · [7 Image processing & OpenCV](#7-image-processing--opencv) ·
[8 MQTT (PacBot)](#8-mqtt-pacbot) · [9 Path planning](#9-path-planning) · [10 Extras (not on the portal)](#10-extras-not-on-the-portal)

---

## 1. Portal pages (login)

| Page | Use for |
|---|---|
| 🔒 [Khoj-o-Drone course](https://portal.e-yantra.org/courses/theme_kd): Stage 1 → Task 1 (1A, 1B, 1C), Learnings, Coding Standard | all KD |
| 🔒 [PacBot course](https://portal.e-yantra.org/courses/theme_pb): Stage 1 → Task 1 (1A, 1B), Learnings | all PB |
| 🔒 KD learnings: [Linux](https://portal.e-yantra.org/courses/theme_kd/learnings/linux/linux/) · [ROS 2](https://portal.e-yantra.org/courses/theme_kd/learnings/ros/ros/) · [ROS 2 Concepts](https://portal.e-yantra.org/courses/theme_kd/learnings/ros/ros2_concepts/) · [ROS 2 Tutorials](https://portal.e-yantra.org/courses/theme_kd/learnings/ros/ros2_tutorials/) · [Turtlesim](https://portal.e-yantra.org/courses/theme_kd/learnings/ros/turtlesim_tutorials/) · ROS 2 Books (links to a paid book — skip) · [MuJoCo](https://portal.e-yantra.org/courses/theme_kd/learnings/mujoco/mujoco/) · [MuJoCo Concepts](https://portal.e-yantra.org/courses/theme_kd/learnings/mujoco/mujoco_concepts/) · [MuJoCo Tutorials](https://portal.e-yantra.org/courses/theme_kd/learnings/mujoco/mujoco_tutorials/) · [Quadcopters](https://portal.e-yantra.org/courses/theme_kd/learnings/quadcopter/quadcopters/) · [Swift Pico model](https://portal.e-yantra.org/courses/theme_kd/learnings/quadcopter/swift_model/) · [Control Systems](https://portal.e-yantra.org/courses/theme_kd/learnings/control_system/control_systems/) · [System Modelling](https://portal.e-yantra.org/courses/theme_kd/learnings/control_system/maths_model/) · [Image Processing](https://portal.e-yantra.org/courses/theme_kd/learnings/image_processing/image_processing/) · [OpenCV Python](https://portal.e-yantra.org/courses/theme_kd/learnings/image_processing/opencv_py/) | all KD |
| 🔒 KD Task pages: [Stage 1 intro](https://portal.e-yantra.org/courses/theme_kd/stage_1/introduction/) · [Task 0 overview](https://portal.e-yantra.org/courses/theme_kd/stage_1/task_0/overview/) · [Task 0 installation](https://portal.e-yantra.org/courses/theme_kd/stage_1/task_0/instruction/) (Task 1 pages: via the course menu) | setup, setup, KD 1A/1B/1C |
| 🔒 PB learnings: [Linux](https://portal.e-yantra.org/courses/theme_pb/learnings/linux/linux/) · [MQTT](https://portal.e-yantra.org/courses/theme_pb/learnings/mqtt/mqtt/) · [MQTT Concepts](https://portal.e-yantra.org/courses/theme_pb/learnings/mqtt/mqtt_concepts/) · [MQTT Tutorials](https://portal.e-yantra.org/courses/theme_pb/learnings/mqtt/mqtt_tutorials/) · Path Planning (via the course menu) | all PB |
| 🔒 [ROS 2 CLI cheat sheet PDF](https://portal.e-yantra.org/courses/theme_kd/learnings/ros/media/cli_cheats_sheet.pdf). **2019 edition:** in Humble `ros2 msg`/`ros2 srv` are gone (use `ros2 interface show`), and its bag examples are missing the word `bag` | KD 1B/1C |
| 🔒 [*Fundamentals of Control Theory* book](https://portal.e-yantra.org/courses/theme_kd/learnings/control_system/pdf/fundamentals_of_control_r1_6.pdf). Focus: PID and LQR chapters | PID (KD 1B/1C, PB 1B), after Task 1 |
| 🔒 [`StateSpace.pdf`](https://portal.e-yantra.org/courses/theme_kd/learnings/control_system/pdf/StateSpace.pdf) (State-space representation of LTI systems) | after Task 1 |
| 🔒 [`lqr.pdf`](https://portal.e-yantra.org/courses/theme_kd/learnings/control_system/pdf/lqr.pdf) (R. M. Murray, Lecture 2 – LQR Control) | after Task 1 |
| e-Yantra GitHub: [eYRC_26-27_Khojo-Drone](https://github.com/eYantra-Robotics-Competition/eYRC_26-27_Khojo-Drone) (branches `kd_sim`, `turtle_sim`) · [eYRC_26-27_PacBot](https://github.com/eYantra-Robotics-Competition/eYRC_26-27_PacBot) | setup |

## 2. Task videos

| Video | What it shows | Use for |
|---|---|---|
| [Tuner and Plotter demo](https://youtu.be/ef2SI6uARuA) (2:21, silent) | KD 1B/1C PID tuner GUI walkthrough | KD 1B, KD 1C |
| [task 1b submission demo](https://youtu.be/xqOyre-afOE) (0:59, silent) | Framing of the KD 1B video submission | KD 1B |
| [task 1c submission](https://youtu.be/Ut5wKqhMFdM) (0:42, silent) | Framing of the KD 1C video submission | KD 1C |
| [PacBot Task 1A expected output](https://youtu.be/95Kb59pPsXU) | What a successful PB 1A run looks like | PB 1A |
| [PacBot Task 1B expected output](https://youtu.be/Ac7dU4j0nVs) | What a successful PB 1B run looks like | PB 1B |

## 3. ROS 2

**Start here:** ⭐ [What Is ROS2? – Framework Overview](https://youtu.be/7TVWlADXwRw) (8:22) ·
⭐ [Getting Ready for ROS Part 4: ROS Overview](https://articulatedrobotics.xyz/ready-for-ros-4-ros-overview/) · the portal's **Turtlesim Resources** page (commands you type yourself). Use for **KD 1B/1C**.

**Concepts — Basic** ([docs.ros.org](https://docs.ros.org/en/humble/)):
[Nodes](https://docs.ros.org/en/humble/Concepts/Basic/About-Nodes.html) ·
[Discovery](https://docs.ros.org/en/humble/Concepts/Basic/About-Discovery.html) ·
[Interfaces](https://docs.ros.org/en/humble/Concepts/Basic/About-Interfaces.html) ·
⭐ [Topics](https://docs.ros.org/en/humble/Concepts/Basic/About-Topics.html) ·
[Services](https://docs.ros.org/en/humble/Concepts/Basic/About-Services.html) ·
[Actions](https://docs.ros.org/en/humble/Concepts/Basic/About-Actions.html) ·
[Parameters](https://docs.ros.org/en/humble/Concepts/Basic/About-Parameters.html) ·
[Command line tools](https://docs.ros.org/en/humble/Concepts/Basic/About-Command-Line-Tools.html) ·
[Launch](https://docs.ros.org/en/humble/Concepts/Basic/About-Launch.html) ·
[Client libraries](https://docs.ros.org/en/humble/Concepts/Basic/About-Client-Libraries.html)

**Concepts — Intermediate:**
⭐ [ROS_DOMAIN_ID](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Domain-ID.html) (why teammates' robots can interfere on one Wi-Fi) ·
[Middleware vendors](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Different-Middleware-Vendors.html) ·
[Logging](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Logging.html) ·
[Quality of Service](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Quality-of-Service-Settings.html) ·
[Executors](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Executors.html) ·
[Topic statistics](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Topic-Statistics.html) ·
[RQt](https://docs.ros.org/en/humble/Concepts/Intermediate/About-RQt.html) ·
[Composition](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Composition.html) ·
[Cross-compilation](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Cross-Compilation.html) ·
[Security](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Security.html) · tf2

**Tutorials — do them in order** (the portal says they build on each other; [How-to Guides](https://docs.ros.org/en/humble/How-To-Guides.html) for specific questions):

| # | Beginner: CLI tools | For Task 1? |
|---|---|---|
| 1 | ⭐ [Configuring environment](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html) | yes |
| 2 | ⭐ [Using turtlesim, ros2 and rqt](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html) | yes |
| 3 | ⭐ [Understanding nodes](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html) | yes |
| 4 | ⭐ [Understanding topics](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html) | yes |
| 5 | [Understanding services](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html) | later |
| 6 | [Understanding parameters](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html) | later |
| 7 | [Understanding actions](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html) | later |
| 8 | [Using rqt_console to view logs](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/Using-Rqt-Console.html) | later |
| 9 | [Launching nodes](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes.html) | yes (you use launch files) |
| 10 | ⭐ [Recording and playing back data](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html) | **yes — KD 1B/1C submissions are bag files** |

| # | Beginner: client libraries | For Task 1? |
|---|---|---|
| 1 | [Using colcon to build packages](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html) | good to know |
| 2 | [Creating a workspace](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html) | good to know |
| 3 | [Creating a package](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html) | Task 2 |
| 4 | [Simple publisher and subscriber (C++)](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Publisher-And-Subscriber.html) | Task 2 |
| 5 | [Simple publisher and subscriber (Python)](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html) | Task 2 |
| 6 | [Simple service and client (C++)](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Service-And-Client.html) | later |
| 7 | [Simple service and client (Python)](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client.html) | later |
| 8 | [Custom msg and srv files](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html) | later |
| 9 | [Implementing custom interfaces](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Single-Package-Define-And-Use-Interface.html) | later |
| 10 | [Parameters in a class (C++)](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-CPP.html) | later |
| 11 | [Parameters in a class (Python)](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.html) | later (PID gains as parameters) |
| 12 | [Using ros2doctor](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Getting-Started-With-Ros2doctor.html) | when something is broken |
| 13 | [Plugins (C++)](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Pluginlib.html) | skip |

**Intermediate / advanced:**
[rosdep](https://docs.ros.org/en/humble/Tutorials/Intermediate/Rosdep.html) ·
[Creating an action](https://docs.ros.org/en/humble/Tutorials/Intermediate/Creating-an-Action.html) ·
[Action server/client (C++)](https://docs.ros.org/en/humble/Tutorials/Intermediate/Writing-an-Action-Server-Client/Cpp.html) ·
[Action server/client (Python)](https://docs.ros.org/en/humble/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html) ·
[Composable node](https://docs.ros.org/en/humble/Tutorials/Intermediate/Writing-a-Composable-Node.html) ·
[Composition](https://docs.ros.org/en/humble/Tutorials/Intermediate/Composition.html) ·
[Monitoring parameter changes (C++)](https://docs.ros.org/en/humble/Tutorials/Intermediate/Monitoring-For-Parameter-Changes-CPP.html) ·
[Launch](https://docs.ros.org/en/humble/Tutorials/Intermediate/Launch/Launch-Main.html) · tf2 ·
[Testing](https://docs.ros.org/en/humble/Tutorials/Intermediate/Testing/Testing-Main.html) ·
[URDF](https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/URDF-Main.html) ·
[RViz](https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-Main.html) ·
[Simulators](https://docs.ros.org/en/humble/Tutorials/Advanced/Simulators/Simulation-Main.html)

**More on ROS 2 (portal list):** [The Robotics Back-End](https://roboticsbackend.com/category/ros2) (Python-first) ·
[ROS 2 for ROS developers](https://github.com/fmrico/ros_to_ros2_talk_examples) (only if you know ROS 1) ·
[The Construct](https://www.theconstructsim.com/) (mostly paid)

## 4. MuJoCo

**Start here (KD 1B/1C, PB 1B):** ⭐ [Overview](https://mujoco.readthedocs.io/en/stable/overview.html) (model vs data, "hello world") ·
⭐ [Introductory tutorial (Colab)](https://colab.research.google.com/github/google-deepmind/mujoco/blob/main/python/tutorial.ipynb) ·
[Installing the Python bindings](https://mujoco.readthedocs.io/en/stable/python.html#installation)

**Concepts:** [Modeling (MJCF)](https://mujoco.readthedocs.io/en/stable/modeling.html) ·
[XML reference](https://mujoco.readthedocs.io/en/stable/XMLreference.html) ·
[Model gallery](https://mujoco.readthedocs.io/en/stable/models.html) ·
[Computation](https://mujoco.readthedocs.io/en/stable/computation/index.html) ·
[Fluid forces](https://mujoco.readthedocs.io/en/stable/computation/fluid.html) ·
[Simulation (mjModel, mjData, stepping)](https://mujoco.readthedocs.io/en/stable/programming/simulation.html) ·
[Visualization](https://mujoco.readthedocs.io/en/stable/programming/visualization.html) ·
[User interface](https://mujoco.readthedocs.io/en/stable/programming/ui.html) ·
[Model editing (mjSpec)](https://mujoco.readthedocs.io/en/stable/programming/modeledit.html) ·
[Extensions](https://mujoco.readthedocs.io/en/stable/programming/extension.html) ·
[API reference](https://mujoco.readthedocs.io/en/stable/APIreference/index.html)

**Tutorials:** [Python bindings](https://mujoco.readthedocs.io/en/stable/python.html) ·
[C code samples](https://mujoco.readthedocs.io/en/stable/programming/samples.html) ·
[Releases + simulate viewer](https://github.com/google-deepmind/mujoco/releases) ·
Colabs: [mjSpec model editing](https://colab.research.google.com/github/google-deepmind/mujoco/blob/main/python/mjspec.ipynb) ·
[Parallel rollouts](https://colab.research.google.com/github/google-deepmind/mujoco/blob/main/python/rollout.ipynb) ·
⭐ [LQR control](https://colab.research.google.com/github/google-deepmind/mujoco/blob/main/python/LQR.ipynb) (after Task 1, once PID works) ·
[Least-squares solver](https://colab.research.google.com/github/google-deepmind/mujoco/blob/main/python/least_squares.ipynb)

**Advanced (skip for Stage 1):** [MJX (Colab)](https://colab.research.google.com/github/google-deepmind/mujoco/blob/main/mjx/tutorial.ipynb) ·
[Differentiable physics with MJX](https://colab.research.google.com/github/google-deepmind/mujoco/blob/main/mjx/training_apg.ipynb) ·
[Unity plug-in](https://mujoco.readthedocs.io/en/stable/unity.html)

**Models:** [MuJoCo on GitHub](https://github.com/google-deepmind/mujoco) ·
[MuJoCo Menagerie](https://github.com/google-deepmind/mujoco_menagerie) (has `bitcraze_crazyflie_2` and `skydio_x2` quadrotors)

## 5. Quadcopters

| Resource | Notes | Use for |
|---|---|---|
| ⭐ [Drone flight physics in under 2 minutes](https://www.youtube.com/watch?v=iQAPkN7OWus) (Dronology, 1:38) | Throttle, yaw, pitch, roll with the sticks | KD 1B/1C |
| ⭐ [Introduction to Quadcopters](https://www.youtube.com/watch?v=Gp80qN7kvfs) (e-Yantra tech talk, 1:01:50) | **Watch ~12–26 min** (dynamics) and **~42–48 min** (control cascade = your Task 1B/1C setup). The rest is optional (parts list, planning, Q&A) | KD 1B/1C |
| 🔒 Portal pages: Quadcopters · Swift Pico model · Quadcopter Control | Forces/torques figure (Coursera *Robotics: Aerial Robotics*), sensors, arming commands, hardware architecture | KD 1B/1C, KD 1B/1C, PB 1B, all |
| [PX4 Guide](https://docs.px4.io/main/en/) · [ArduPilot Copter](https://ardupilot.org/copter/index.html) | Further reading only; not our stack | — |

## 6. Control systems & PID

| Resource | Length | Use for |
|---|---|---|
| ⭐ [Everything You Need to Know About Control Theory](https://youtu.be/lBC1nEq0_nk) (MATLAB) | 16:07 | PID (KD 1B/1C, PB 1B) (big picture) |
| [A real control system — how to start designing](https://youtu.be/Mbx5IMICS_Y) (Brian Douglas) | 26:58 | optional |
| [Classical Control Theory playlist](https://www.youtube.com/playlist?list=PLUMWjy5jgHK1NC52DXXrriwihVrYZKqjk) (Brian Douglas) | 46 videos, ~10 h | reference only |
| ⭐ [PID Control — A brief introduction](https://www.youtube.com/watch?v=UR0hOmjaHp0) (Brian Douglas) | 7:44 | PID (KD 1B/1C, PB 1B) |
| ⭐ [Simple Examples of PID Control](https://www.youtube.com/watch?v=XfAt6hNV8XM) | 13:10 | PID (KD 1B/1C, PB 1B) |
| ⭐ [What Is PID Control? — Part 1](https://www.youtube.com/watch?v=wkfEZmsQqiA) (MATLAB) | ~11 min | PID (KD 1B/1C, PB 1B) |
| [Anti-windup — Part 2](https://www.youtube.com/watch?v=NVLXCwc8HzM) | ~10 min | PID (KD 1B/1C, PB 1B) |
| [Noise filtering — Part 3](https://www.youtube.com/watch?v=7dUVdrs1e18) | ~10 min | PID (KD 1B/1C, PB 1B) |
| ⭐ [A PID Tuning Guide — Part 4](https://www.youtube.com/watch?v=sFOEsA0Irjs) | 12:05 | PID (KD 1B/1C, PB 1B) (**watch before tuning**) |
| [3 Ways to Build a Model — Part 5](https://www.youtube.com/watch?v=qhIjIu-Zk10) | 13:45 | after Task 1 |
| [Manual and Automatic Tuning — Part 6](https://www.youtube.com/watch?v=qj8vTO1eIHo) | 13:31 | PID (KD 1B/1C, PB 1B) |
| [Important PID Concepts — Part 7](https://www.youtube.com/watch?v=tbgV6caAVcs) | 12:29 | PID (KD 1B/1C, PB 1B) |
| [Introduction to State-Space Equations](https://www.youtube.com/watch?v=hpeKrMG-WP0) (MATLAB) | 14:12 | after Task 1 |
| [Introduction to System Stability and Control](https://www.youtube.com/watch?v=uqjKG32AkC4) | 11:32 | after Task 1 |
| [Stability of Closed Loop Control Systems](https://www.youtube.com/watch?v=yf09OrHa520) | 11:36 | after Task 1 |
| [What Is LQR Optimal Control?](https://www.youtube.com/watch?v=E_RDCFOlJx4) (MATLAB) | 17:24 | after Task 1 |
| [Why the Riccati Equation Is Important for LQR](https://www.youtube.com/watch?v=ZktL3YjTbB4) (MATLAB) | 14:30 | after Task 1 |
| [Jacobian (Wolfram MathWorld)](http://mathworld.wolfram.com/Jacobian.html) | reading | after Task 1 |

**Portal pages 🔒:** The Map of Control Theory · Introduction to Control Systems · System Modelling · Model Examples ·
Stability · Simple Pendulum · **PID Controller (incl. "P, PD & PID for Drones" + ball-and-beam demo)** · LQR Controller.
**Known portal mistakes:** the PID page's I-term `Iterm = (Iterm + error)·Ki` should be `Iterm = Iterm + Ki·error`;
the Quadcopter Control "To Do" leaves out thrust; one eigenvalue is printed −2.824 instead of −2.828.

## 7. Image processing & OpenCV

**Start here (KD 1A):** 🔒 portal *Image Processing Basics* (BGR vs RGB, HSV, **OpenCV hue is 0–179**) ·
⭐ [OpenCV Course — Full Tutorial with Python](https://www.youtube.com/watch?v=oXlwWbU8l2o) (freeCodeCamp, 4 h, the portal's pick; watch: reading images, drawing, colour spaces, thresholding, contours) ·
[Python argparse docs](https://docs.python.org/3/library/argparse.html) (KD 1A's `--image`)

**Official OpenCV-Python tutorials (portal's order)** — ⚠ your apt OpenCV is **4.5.4**; these pages are for newer 4.x, mostly identical except **ArUco** (use the *old* API, see §10):
[Tutorial index](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) ·
[Introduction](https://docs.opencv.org/4.x/da/df6/tutorial_py_table_of_contents_setup.html) ·
[Images](https://docs.opencv.org/4.x/db/deb/tutorial_display_image.html) ·
[Videos](https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html) ·
[Drawing](https://docs.opencv.org/4.x/dc/da5/tutorial_py_drawing_functions.html) ·
[Trackbar](https://docs.opencv.org/4.x/d9/dc8/tutorial_py_trackbar.html) ·
[Basic operations](https://docs.opencv.org/4.x/d3/df2/tutorial_py_basic_ops.html) ·
[Arithmetic](https://docs.opencv.org/4.x/d0/d86/tutorial_py_image_arithmetics.html) ·
⭐ [Changing colorspaces](https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html) ·
⭐ [Geometric transformations (warpPerspective)](https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html) ·
[Thresholding](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html) ·
[Smoothing](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html) ·
⭐ [Morphological transformations](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html) ·
[Gradients](https://docs.opencv.org/4.x/d5/d0f/tutorial_py_gradients.html) ·
[Canny edges](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html) ·
⭐ [Contours](https://docs.opencv.org/4.x/d3/d05/tutorial_py_table_of_contents_contours.html) ·
[Histograms](https://docs.opencv.org/4.x/de/db2/tutorial_py_table_of_contents_histograms.html) ·
[Template matching](https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html) ·
[Hough lines](https://docs.opencv.org/4.x/d6/d10/tutorial_py_houghlines.html) ·
[Hough circles](https://docs.opencv.org/4.x/da/d53/tutorial_py_houghcircles.html)
*(docs.opencv.org blocks automated link checks; open them in a browser.)*

**ROS 2 + OpenCV (Task 2 prep):** [OpenCV in a ROS 2 C++ node (The Construct)](https://www.theconstruct.ai/how-to-integrate-opencv-with-a-ros2-c-node/) ·
[Getting started with OpenCV in ROS 2 (Python)](https://automaticaddison.com/getting-started-with-opencv-in-ros-2-foxy-fitzroy-python/) ·
[Integrating OpenCV with ROS 2 (Medium)](https://ibrahimmansur4.medium.com/integrating-opencv-with-ros2-a-comprehensive-guide-to-computer-vision-in-robotics-66b97fa2de92) ·
[Object Detection with OpenCV for ROS 2](https://www.youtube.com/watch?v=pK_SvyOm8pg) (1:05) ·
[Line Following with OpenCV for ROS 2](https://www.youtube.com/watch?v=88y_1ovno8g) (1:12).
Note: the KD simulator publishes `/image_raw` only when launched with `image_sink:=both`.

## 8. MQTT (PacBot)

**Start here (PB 1A/1B):** 🔒 portal *MQTT* → *MQTT Concepts* → *MQTT Tutorials* ·
⭐ [MQTT Essentials (HiveMQ)](https://www.hivemq.com/mqtt-essentials/)

| Concept | HiveMQ chapter |
|---|---|
| Connection | [Part 3: client, broker, connection](https://www.hivemq.com/blog/mqtt-essentials-part-3-client-broker-connection-establishment/) |
| ⭐ Topics & wildcards | [Part 5: topics & best practices](https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/) |
| ⭐ QoS 0/1/2 | [Part 6: quality of service](https://www.hivemq.com/blog/mqtt-essentials-part-6-mqtt-quality-of-service-levels/) |
| Sessions | [Part 7: persistent session & queuing](https://www.hivemq.com/blog/mqtt-essentials-part-7-persistent-session-queuing-messages/) |
| ⭐ Retained messages (PB 1A uses them) | [Part 8: retained messages](https://www.hivemq.com/blog/mqtt-essentials-part-8-retained-messages/) |
| Last Will | [Part 9: last will and testament](https://www.hivemq.com/blog/mqtt-essentials-part-9-last-will-and-testament/) |
| Keep-alive | [Part 10: keep alive & client take-over](https://www.hivemq.com/blog/mqtt-essentials-part-10-alive-client-take-over/) |

**Getting started:** [mqtt.org getting started](https://mqtt.org/getting-started/) ·
[Steve's Internet Guide: introduction](http://www.steves-internet-guide.com/mqtt/) ·
[Steve's: how MQTT works](http://www.steves-internet-guide.com/mqtt-works/)

**Broker & libraries:** [Eclipse Mosquitto](https://mosquitto.org/) (installed by `setup.sh`) ·
[test.mosquitto.org](https://test.mosquitto.org/) (public, **anyone can read it**, never for real data) ·
[Eclipse Paho](https://eclipse.dev/paho/) · [paho-mqtt on PyPI](https://pypi.org/project/paho-mqtt/) ·
[paho.mqtt.python](https://github.com/eclipse-paho/paho.mqtt.python) · C++: [paho.mqtt.cpp](https://github.com/eclipse-paho/paho.mqtt.cpp)
([examples](https://github.com/eclipse-paho/paho.mqtt.cpp/tree/master/examples)) · [paho.mqtt.c](https://github.com/eclipse-paho/paho.mqtt.c)

**Specification (reference):** [mqtt.org](https://mqtt.org/) · [specification page](https://mqtt.org/mqtt-specification/) ·
[MQTT 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html) · [MQTT 3.1.1](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)

## 9. Path planning

🔒 Portal *Path Planning* page (PacBot → Learnings): BFS, DFS, Dijkstra, Greedy best-first, A\*, with animations
on the same map. No external links; it's the main reading for **PB 1A**. Pair it with the Computerphile videos in §10.

## 10. Extras (not on the portal)

Not on the portal. Chosen so each topic goes short → longer → deeper.

| Resource | Why | Use for |
|---|---|---|
| [eYRC 2026-27 Official Launch](https://www.youtube.com/watch?v=G8m9-6jlzaE) | Big picture | all |
| [Digital Images — Computerphile](https://www.youtube.com/watch?v=06OHflWNCOE) | "An image is numbers" before OpenCV | KD 1A |
| [Warp Perspective / Bird View](https://www.youtube.com/watch?v=Tm_7fGolVGE) | Short perspective-transform demo | KD 1A |
| [Computing Homography (Shree Nayar)](https://www.youtube.com/watch?v=l_qjO4cM74o) | The maths behind it | KD 1A |
| ⭐ [Detecting ArUco markers with OpenCV and Python](https://pyimagesearch.com/2020/12/21/detecting-aruco-markers-with-opencv-and-python/) | Uses the **old ArUco API that matches OpenCV 4.5.4** | KD 1A |
| [Drone Simulation and Control playlist (MATLAB)](https://www.youtube.com/playlist?list=PLn8PRpmsu08oOLBVYYIwwN_nvuyUqEjrj) | Optional drone-control series | KD 1B/1C |
| [Understanding PID Control playlist (MATLAB)](https://www.youtube.com/playlist?list=PLn8PRpmsu08pQBgjxYFXSsODEF3Jqmm-y) | The Part 1–7 series above as one playlist | PID (KD 1B/1C, PB 1B) |
| [Dijkstra's Algorithm — Computerphile](https://www.youtube.com/watch?v=GazC3A4OQTE) → [A* Search — Computerphile](https://www.youtube.com/watch?v=ySN5Wnu88nE) | The second builds on the first | PB 1A |
