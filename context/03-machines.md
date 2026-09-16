# Machine inventory & Task 0 setup plan

**Why this file exists:** on 2026-09-12 an agent burned four tool calls probing the OS for facts
nobody had written down. Record specs here once; never re-probe.

Requirement (both themes): **Ubuntu 22.04 LTS · >4 cores x86_64 · 8 GB+ RAM · 100 GB+ storage.**
Dedicated GPU not necessary for KD, preferable for PB.

## Inventory

| Member | Machine | CPU | RAM | Storage | OS now | Linux ready? |
|---|---|---|---|---|---|---|
| **Owner unconfirmed** ("Ubuntu box") | unknown laptop model | AMD Ryzen 7 7840HS, 8C/16T | 14 GiB | 954 GB NVMe; Ubuntu root **48.8 GB** | Ubuntu 22.04.5 bare metal (dual-boot with Windows) | **YES — KD evaluator green, PB submission generated** |
| Saurabh | HP Pavilion Plus 14-ew1xxx | Core Ultra 5 125H, 14C/18T | 15.5 GB | Samsung 512 GB NVMe (477 GB), GPT | Win 11 Home SL 26200 | **No partition yet** *(as of 2026-09-12 — may be superseded by the Ubuntu box)* |
| Gauri | **UNKNOWN** | — | — | — | — | — |
| Parth | **UNKNOWN** | — | — | — | — | — |
| Mahesh | **UNKNOWN** | — | — | — | — | — |

**Open action:** ask the three for RAM, free disk, CPU and current OS. Do not probe their machines.
All four must complete Task 0 individually; on a drone theme the weakest laptop sets the team's pace.

### Ubuntu box — measured 2026-09-13 (owner unconfirmed)

Measured by claude-code running on this machine, inside the account of the person who drives this
repo. **The hardware does not match the HP Pavilion recorded for Saurabh below.** It could be
another laptop of his or a teammate's machine, so ask rather than assume.

- **HP OMEN 16** (per the NEON//HUD session notes) · CPU **AMD Ryzen 7 7840HS** (Zen 4, 8C/16T) ·
  iGPU **Radeon 780M** (Phoenix1) **plus discrete NVIDIA GeForce RTX 4050 Laptop GPU**, driver
  580.178.04, found 2026-09-16 · RAM 14.9 GiB
- `nvme0n1` 954 GB: EFI 260 MB · MSR 16 MB · NTFS 550.9 GB · NTFS 353.3 GB · NTFS 572 MB (recovery) ·
  **ext4 48.8 GB mounted at `/`** (20 GB used, 26 GB free)
- External Samsung T9 1 TB (2 × 466 GB NTFS) mounted under `/media/ubantu/`
- Ubuntu **22.04.5**, kernel **6.8.0-138-generic** (HWE). Not virtualised and not WSL, per the KD
  evaluator
- ROS 2 **Humble** desktop at `/opt/ros/humble`, sourced from `~/.bashrc`
- Python 3.10.12. **Two MuJoCo versions on purpose, one per theme.** Each theme's Task 0 demands
  its own version; details in "Per-theme Python environments" below
- ROS 2 workspaces: `~/turtlesim_ws` (built) and `~/pico_ws` (fresh 2026-09-16, **builds OK**; replaced `pico_mujoco_ws`; needed
  `ros-humble-actuator-msgs` + `ros-humble-image-view`). `~/.bashrc` sources
  `~/pico_ws/install/setup.bash`. See `08-task0-bonus.md`
- No passwordless sudo, so apt installs must be run by the user
- **Not done yet:** `ROS_DOMAIN_ID` is not set in `~/.bashrc`, and git global
  `user.name`/`user.email` are unset

**Storage — now TIGHT [MEASURED 2026-09-16]: only 6.5 GB free on `/` (86% used)**, down from 26 GB
on 2026-09-13. Biggest items: the 8 GB `/swapfile` (added 2026-09-13 in the NEON//HUD session),
`/var/lib/snapd` 4.0 GB, `~/.cache` 1.9 GB, `/usr/lib/chatgpt` 1.4 GB, apt archives 465 MB.
Options for Saurabh to choose from; nothing has been done: shrink the swapfile, `sudo apt clean`,
clear `~/.cache`, remove old snap revisions, or grow ext4 from Windows.

**Storage risk [INFERRED]:** a 48.8 GB root partition is under half the 100 GB requirement. It is
enough for Task 0, but Task 1/2 workspaces, colcon `build/` trees and `ros2 bag` recordings will
eat into 26 GB fast. Options: keep bags on the T9, or grow the ext4 partition by shrinking one of
the NTFS partitions from Windows. **Back up before resizing.**

The Meteor-Lake and Intel-Arc risks below **do not apply** to this box. The 7840HS/780M is
well supported by the 6.8 HWE kernel and Mesa.

#### Per-theme Python environments — do not mix them

| Theme | Where | MuJoCo | Other | Evaluator |
|---|---|---|---|---|
| **KD** | venv `~/Desktop/e-yantra/drone_ws/task0/drone_env` (= `~/drone_ws/task0/drone_env` via symlink) | **3.9.0** (exact — the evaluator sets `generate=False` on anything else) | numpy 2.2.6, glfw, PyOpenGL, `eyantra-autoeval` 0.1.68 | `eyantra-autoeval evaluate --year 2026 --theme KD --task 0` |
| **PB** | system `python3`, user site `~/.local/lib/python3.10/site-packages` | **3.11.0** | `paho-mqtt` 2.1.0 · **numpy 1.26.4** (downgraded from 2.2.6 on 2026-09-13: ROS 2 Humble's apt `cv_bridge` needs numpy 1.x; PB MuJoCo re-verified OK) | `~/Desktop/e-yantra/pacbot_ws/task0/task0_eval` (static binary) |

**The `~/drone_ws` symlink is load-bearing — FIXED 2026-09-13, do not delete it.** The KD venv
was created at `~/drone_ws/task0/drone_env`, and every script inside it hard-codes that path:
`activate` sets `VIRTUAL_ENV`, and `pip` and `eyantra-autoeval` have it in their shebangs. The
folder has since moved, and is now at `~/Desktop/e-yantra/drone_ws`. The fix was
`ln -s ~/Desktop/e-yantra/drone_ws ~/drone_ws`.

Verified after the fix: activating from the real path gives `python3` → venv, MuJoCo **3.9.0**;
`pip` 22.0.2 and `eyantra-autoeval --help` both run; outside the venv, the system is still 3.11.0.

Without the symlink, `pip` and `eyantra-autoeval` fail with "bad interpreter". Worse, **`source
activate` fails silently**: `python3` falls through to `/usr/bin/python3` and imports **MuJoCo
3.11.0**, so KD code runs on PB's MuJoCo without any error. **If `drone_ws` ever moves again,
re-point the symlink**, or recreate the venv in place with `mujoco==3.9.0` plus the evaluator.

### Saurabh — measured 2026-09-12

- GPU: Intel Arc (integrated, Meteor Lake)
- Partitions on disk 0: EFI 0.3 GB · reserved · **C: 326 GB (38.8 GB free)** · **F: 150 GB (116 GB free)** · recovery 0.7 GB
- WSL2 is the default version, **feature enabled but zero distros installed**
- BitLocker + Secure Boot state **unverified** — the query needs admin

## Dual-boot plan (Saurabh)

**Take the space from F:, not C:.** C: has only 38.8 GB free, well under the 100 GB requirement.
F: has 116 GB free of 150 GB (about 34 GB used, which includes this `F:\e-yantra` folder).

Two options:

- **Shrink F: to ~60 GB** → frees ~90 GB for Linux, leaves ~26 GB on F:. Keeps F: usable.
- **Move F:'s contents elsewhere and give the whole 150 GB to Linux.** Cleaner, more work.

### Pre-checks before repartitioning — run as admin

```powershell
Get-BitLockerVolume | Select-Object MountPoint,VolumeStatus,ProtectionStatus
Confirm-SecureBootUEFI
```

Then in BIOS, confirm the NVMe controller is in **AHCI, not RST/RAID mode** — some HP laptops ship
in RST, which makes the Ubuntu installer see no disk at all. Back up before touching partitions.

## Two risks specific to this hardware

1. **Meteor Lake needs a recent kernel.** Ubuntu 22.04's stock GA kernel is 5.15, which predates
   Core Ultra — expect broken Wi-Fi and/or graphics. **Download a 22.04.5 ISO** (HWE kernel 6.8),
   not an older 22.04 image. *[INFERRED from hardware generation — verify on first boot with a live
   USB before installing.]*
2. **Intel Arc iGPU + simulator.** Rendering goes through Mesa rather than a discrete GPU. Largely
   defused as of 2026-09-12: the portal's learnings section is **"ROS 2 & MuJoCo"**, and MuJoCo is
   far lighter than Gazebo. Still worth a live-USB smoke test before committing.

### The version lock — the mistake most likely to cost a week

**Ubuntu 22.04, never 24.04.** Every documentation link on the portal points at
`docs.ros.org/en/humble/`. **ROS 2 Humble is the LTS for Ubuntu 22.04 Jammy**; Ubuntu 24.04 ships
ROS 2 Jazzy instead. Installing the newer Ubuntu would silently invalidate every command, package
name and link e-Yantra gives you, and the failure shows up days later as "the tutorial doesn't
work". Tell all four members before anyone downloads an ISO.

## WSL2 vs dual-boot vs VM

*[OPINION, claude-code 2026-09-12]* For a Gazebo/ROS 2 drone theme, **dual-boot**. A VM gives poor
3D performance under a simulator, and WSL2 adds a graphics/networking layer that turns every
e-Yantra support answer into a debugging session — the task instructions will assume native Ubuntu
22.04, and so will the evaluators. WSL2 is fine only as a stopgap for a teammate who physically
cannot repartition in time.
