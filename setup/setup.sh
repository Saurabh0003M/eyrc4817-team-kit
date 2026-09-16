#!/usr/bin/env bash
# Team ID:          4817
# Theme:            Khoj-o-Drone + PacBot (eYRC 2026-27)
# Filename:         setup.sh
# Purpose:          One-shot setup for a teammate's Ubuntu 22.04 + ROS 2 Humble laptop, so Task 1 of
#                   both themes can be run: packages, workspaces, library fixes, MQTT broker.
#
# Usage:  bash setup/setup.sh           install + configure (asks for sudo once), then verify
#         bash setup/setup.sh --check   verify only, change nothing
#
# Safe to run again: every step checks first and skips work that is already done.
set -o pipefail   # no "set -u": ROS setup.bash reads unset variables

MODE="${1:-install}"
KD_REPO="https://github.com/eYantra-Robotics-Competition/eYRC_26-27_Khojo-Drone.git"
PB_REPO="https://github.com/eYantra-Robotics-Competition/eYRC_26-27_PacBot.git"
MUJOCO39_VENV="$HOME/.local/share/eyrc4817/mujoco-3.9.0"
BASHRC_START="# >>> eyrc4817 >>>"
BASHRC_END="# <<< eyrc4817 <<<"
failures=0

say()  { printf '\n\033[1;36m== %s\033[0m\n' "$*"; }
ok()   { printf '  \033[32m[ok]\033[0m %s\n' "$*"; }
bad()  { printf '  \033[31m[!!]\033[0m %s\n' "$*"; failures=$((failures + 1)); }
info() { printf '  %s\n' "$*"; }

# ---------------------------------------------------------------------------------------------
# Preconditions: the right Ubuntu and ROS 2 Humble (Task 0) must already be there.
# ---------------------------------------------------------------------------------------------
say "Preconditions"
if grep -q 'VERSION_ID="22.04"' /etc/os-release; then ok "Ubuntu 22.04"; else bad "not Ubuntu 22.04 — e-Yantra requires 22.04"; fi
if [ -f /opt/ros/humble/setup.bash ]; then ok "ROS 2 Humble found"; else bad "ROS 2 Humble missing — finish Task 0 first"; exit 1; fi
if [ "$MODE" != "install" ] && [ "$MODE" != "--check" ]; then echo "usage: bash setup/setup.sh [--check]"; exit 2; fi

# Locate a libmujoco.so.3.9.0: our private venv first, else any existing copy (e.g. a Task 0 venv).
find_mujoco39_dir() {
    local candidate="$MUJOCO39_VENV/lib/python3.10/site-packages/mujoco"
    if [ -f "$candidate/libmujoco.so.3.9.0" ]; then echo "$candidate"; return; fi
    local found
    found=$(find "$HOME" -xdev -name 'libmujoco.so.3.9.0' -not -path '*/pico_ws/*' 2>/dev/null | head -1)
    [ -n "$found" ] && dirname "$found"
}

if [ "$MODE" = "install" ]; then
    # -----------------------------------------------------------------------------------------
    say "1/6 apt packages (sudo password needed once)"
    sudo apt-get update -qq
    sudo apt-get install -y git zip python3-pip python3-venv python3-opencv python3-numpy \
        libglfw3-dev ros-humble-actuator-msgs ros-humble-image-view mosquitto mosquitto-clients \
        python3-colcon-common-extensions

    # -----------------------------------------------------------------------------------------
    say "2/6 Python packages (user site)"
    # numpy < 2: ROS 2 Humble's apt-built cv_bridge fails to import under numpy 2.x
    python3 -m pip install --user "numpy<2" paho-mqtt

    # -----------------------------------------------------------------------------------------
    say "3/6 MuJoCo 3.9.0 library for the Khoj-o-Drone simulator"
    if [ -n "$(find_mujoco39_dir)" ]; then
        info "already present: $(find_mujoco39_dir)"
    else
        python3 -m venv "$MUJOCO39_VENV"
        "$MUJOCO39_VENV/bin/pip" install -q "mujoco==3.9.0"
    fi

    # -----------------------------------------------------------------------------------------
    say "4/6 Khoj-o-Drone workspace ~/pico_ws"
    # shellcheck disable=SC1091
    source /opt/ros/humble/setup.bash
    if [ ! -d "$HOME/pico_ws/src/.git" ]; then
        mkdir -p "$HOME/pico_ws/src"
        git clone -b kd_sim --recursive "$KD_REPO" "$HOME/pico_ws/src"
    else
        git -C "$HOME/pico_ws/src" pull --ff-only
        git -C "$HOME/pico_ws/src" submodule update --init --recursive
    fi
    (cd "$HOME/pico_ws" && colcon build)

    # -----------------------------------------------------------------------------------------
    say "5/6 PacBot workspace ~/pacbot_ws"
    if [ ! -d "$HOME/pacbot_ws/.git" ]; then
        git clone "$PB_REPO" "$HOME/pacbot_ws"
    else
        git -C "$HOME/pacbot_ws" pull --ff-only
    fi
    for task_dir in "$HOME"/pacbot_ws/task1a "$HOME"/pacbot_ws/task1b; do
        [ -d "$task_dir" ] || continue
        for boilerplate in "$task_dir"/task_1*_boilerplate.py; do
            [ -f "$boilerplate" ] || continue
            working_copy="${boilerplate%_boilerplate.py}.py"
            [ -f "$working_copy" ] || cp "$boilerplate" "$working_copy"
        done
        chmod +x "$task_dir"/task_1*_launch 2>/dev/null || true
    done

    # -----------------------------------------------------------------------------------------
    say "6/6 ~/.bashrc block + MQTT broker"
    mujoco39_dir="$(find_mujoco39_dir)"
    tmp_bashrc="$(mktemp)"
    # Remove an older copy of our block, then append a fresh one
    sed "/^$BASHRC_START\$/,/^$BASHRC_END\$/d" "$HOME/.bashrc" > "$tmp_bashrc" && cat "$tmp_bashrc" > "$HOME/.bashrc"
    rm -f "$tmp_bashrc"
    cat >> "$HOME/.bashrc" <<EOF
$BASHRC_START
# Added by eyrc4817 setup.sh — ROS 2 + Khoj-o-Drone workspace + MuJoCo 3.9.0 library path
source /opt/ros/humble/setup.bash
[ -f "\$HOME/pico_ws/install/setup.bash" ] && source "\$HOME/pico_ws/install/setup.bash"
export LD_LIBRARY_PATH="$mujoco39_dir\${LD_LIBRARY_PATH:+:\$LD_LIBRARY_PATH}"
$BASHRC_END
EOF
    sudo systemctl enable --now mosquitto
fi

# ---------------------------------------------------------------------------------------------
# Verification (runs in both modes)
# ---------------------------------------------------------------------------------------------
say "Verification"
# shellcheck disable=SC1091
source /opt/ros/humble/setup.bash
[ -f "$HOME/pico_ws/install/setup.bash" ] && source "$HOME/pico_ws/install/setup.bash"
mujoco39_dir="$(find_mujoco39_dir)"
[ -n "$mujoco39_dir" ] && export LD_LIBRARY_PATH="$mujoco39_dir:${LD_LIBRARY_PATH:-}"

python3 - <<'PY' && ok "Python: OpenCV 4.5.x with old ArUco API, numpy < 2, cv_bridge, paho-mqtt >= 2" || bad "Python packages — see message above"
import sys
import cv2, numpy
from cv_bridge import CvBridge
import importlib.metadata as md
problems = []
if not cv2.__version__.startswith("4.5."): problems.append(f"cv2 {cv2.__version__} (expected apt 4.5.x)")
if not hasattr(cv2, "aruco") or not hasattr(cv2.aruco, "detectMarkers"): problems.append("cv2.aruco.detectMarkers missing")
if int(numpy.__version__.split(".")[0]) >= 2: problems.append(f"numpy {numpy.__version__} (needs < 2)")
if int(md.version("paho-mqtt").split(".")[0]) < 2: problems.append("paho-mqtt < 2")
if problems:
    print("   ", "; ".join(problems)); sys.exit(1)
PY

if [ -n "$mujoco39_dir" ]; then ok "libmujoco.so.3.9.0 at $mujoco39_dir"; else bad "libmujoco.so.3.9.0 not found"; fi

bridge="$(ros2 pkg prefix swift_pico 2>/dev/null)/lib/swift_pico/mujoco_bridge"
if [ -x "$bridge" ]; then
    missing="$(ldd "$bridge" | grep 'not found')"
    if [ -z "$missing" ]; then ok "Khoj-o-Drone simulator: all libraries found"; else bad "simulator libraries missing: $missing"; fi
else
    bad "swift_pico not built (~/pico_ws)"
fi
ros2 pkg executables swift_pico 2>/dev/null | grep -q task_1b_controller && ok "KD task_1b / task_1c controllers installed" || bad "KD controllers not found"

[ -x "$HOME/pacbot_ws/task1a/task_1a_launch" ] && ok "PacBot task1a launcher ready" || bad "PacBot task1a launcher missing or not executable"
[ -x "$HOME/pacbot_ws/task1b/task_1b_launch" ] && ok "PacBot task1b launcher ready" || bad "PacBot task1b launcher missing or not executable"
systemctl is-active --quiet mosquitto && ok "mosquitto broker running" || bad "mosquitto not running"
grep -q "$BASHRC_START" "$HOME/.bashrc" && ok "~/.bashrc block present" || info "(no eyrc4817 block in ~/.bashrc — fine if you set these lines up by hand)"

say "Done"
if [ "$failures" -eq 0 ]; then echo "  All checks passed. Open a NEW terminal before running anything."; else echo "  $failures check(s) failed — see [!!] lines above."; fi
exit "$failures"
