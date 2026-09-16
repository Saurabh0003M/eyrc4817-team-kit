#!/usr/bin/env bash
# Team ID:          4817
# Theme:            Khoj-o-Drone + PacBot (eYRC 2026-27)
# Filename:         setup.sh
# Purpose:          Set up a teammate's laptop for Task 1 of both themes, safely and repeatably.
#
#   bash setup/setup.sh --check    look only: what's installed, what's missing, what setup WOULD change
#   bash setup/setup.sh            do it: install only what's missing, then verify everything
#   bash setup/setup.sh --help
#
# Safe to re-run at any time: every step checks first and skips work already done.
# It never deletes your files. It backs up ~/.bashrc before its first edit.
# A full log is written to ~/eyrc4817-setup.log (send it to the team if something fails).
set -o pipefail   # no "set -u": ROS's setup.bash reads unset variables

# ------------------------------------------------------------------ settings
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
KD_REPO="https://github.com/eYantra-Robotics-Competition/eYRC_26-27_Khojo-Drone.git"
PB_REPO="https://github.com/eYantra-Robotics-Competition/eYRC_26-27_PacBot.git"
KD_WS="$HOME/pico_ws"            # path fixed by the e-Yantra portal instructions
PB_WS="$HOME/pacbot_ws"          # path fixed by the e-Yantra portal instructions
OLD_KD_WS="$HOME/pico_mujoco_ws" # Task 0 bonus workspace; the Task 1 page says to replace it
MUJOCO39_VENV="$HOME/.local/share/eyrc4817/mujoco-3.9.0"
BASHRC="$HOME/.bashrc"
BLOCK_START="# >>> eyrc4817 >>>"
BLOCK_END="# <<< eyrc4817 <<<"
APT_PACKAGES="git zip curl python3-pip python3-venv python3-opencv python3-numpy libglfw3-dev \
ros-humble-actuator-msgs ros-humble-image-view ros-humble-rosbag2-storage-default-plugins \
python3-colcon-common-extensions mosquitto mosquitto-clients"
MIN_FREE_GB=4

failures=0
warnings=0
planned=()

# ------------------------------------------------------------------ output helpers
say()  { printf '\n\033[1;36m== %s\033[0m\n' "$*"; }
ok()   { printf '  \033[32m[ok]\033[0m   %s\n' "$*"; }
warn() { printf '  \033[33m[warn]\033[0m %s\n' "$*"; warnings=$((warnings + 1)); }
bad()  { printf '  \033[31m[!!]\033[0m   %s\n' "$*"; failures=$((failures + 1)); }
todo() { printf '  \033[35m[todo]\033[0m %s\n' "$*"; planned+=("$*"); }
info() { printf '         %s\n' "$*"; }

usage() {
    sed -n '2,15p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

apt_installed() { dpkg-query -W -f='${Status}' "$1" 2>/dev/null | grep -q "install ok installed"; }

python_version_of() {  # prints a package's version, or nothing if not importable
    python3 - "$1" 2>/dev/null <<'PY'
import importlib, sys
try:
    module = importlib.import_module(sys.argv[1])
    print(getattr(module, "__version__", "?"))
except Exception:
    pass
PY
}

find_mujoco39_dir() {  # our private venv first, then any existing copy (e.g. a Task 0 venv)
    local candidate="$MUJOCO39_VENV/lib/python3.10/site-packages/mujoco"
    if [ -f "$candidate/libmujoco.so.3.9.0" ]; then echo "$candidate"; return; fi
    local found
    found=$(find "$HOME" -maxdepth 12 \( -path "$HOME/.cache" -o -path "$HOME/snap" -o -path "$KD_WS" \) -prune \
            -o -name 'libmujoco.so.3.9.0' -print 2>/dev/null | head -1)
    [ -n "$found" ] && dirname "$found"
}

# ------------------------------------------------------------------ 1. preflight
preflight() {
    say "1. Your computer"
    . /etc/os-release
    if [ "$VERSION_ID" = "22.04" ] && [ "$ID" = "ubuntu" ]; then ok "Ubuntu $VERSION_ID"
    else bad "found $PRETTY_NAME — e-Yantra requires Ubuntu 22.04"; fi
    [ "$(uname -m)" = "x86_64" ] && ok "x86_64 processor" || bad "processor is $(uname -m); e-Yantra requires x86_64"
    if grep -qi microsoft /proc/version; then warn "running inside WSL — e-Yantra's evaluators reject WSL; use bare-metal Ubuntu"
    else ok "not WSL"; fi
    virt="$(systemd-detect-virt 2>/dev/null | head -1)"; [ -z "$virt" ] && virt=none
    [ "$virt" = "none" ] && ok "bare metal (not a virtual machine)" || warn "virtual machine detected ($virt) — simulators may be slow, and the Task 0 evaluator notes VMs"
    ram_gb=$(awk '/MemTotal/ {printf "%d", $2/1024/1024}' /proc/meminfo)
    [ "$ram_gb" -ge 7 ] && ok "RAM ${ram_gb} GB" || warn "RAM ${ram_gb} GB (8 GB+ recommended)"
    free_gb=$(df -BG --output=avail "$HOME" | tail -1 | tr -dc '0-9')
    [ "$free_gb" -ge "$MIN_FREE_GB" ] && ok "free disk ${free_gb} GB in $HOME" || bad "only ${free_gb} GB free in $HOME (setup needs about ${MIN_FREE_GB} GB)"
    if [ -f /opt/ros/humble/setup.bash ]; then
        apt_installed ros-humble-desktop && ok "ROS 2 Humble (desktop)" || warn "ROS 2 Humble found but not ros-humble-desktop (Task 0 installs desktop)"
    else
        bad "ROS 2 Humble not installed — finish e-Yantra Task 0 first"
    fi
    if timeout 15 git ls-remote --heads "$PB_REPO" >/dev/null 2>&1; then ok "internet: GitHub reachable"
    else bad "cannot reach GitHub (check internet/proxy)"; fi
}

# ------------------------------------------------------------------ 2. inventory (read-only)
inventory() {
    say "2. What's already installed"
    missing_apt=()
    for package in $APT_PACKAGES; do
        apt_installed "$package" || missing_apt+=("$package")
    done
    if [ ${#missing_apt[@]} -eq 0 ]; then ok "all $(echo $APT_PACKAGES | wc -w) apt packages installed"
    else todo "apt install: ${missing_apt[*]}"; fi

    numpy_version="$(python_version_of numpy)"
    if [ -z "$numpy_version" ]; then todo "pip install --user 'numpy<2'"
    elif [ "${numpy_version%%.*}" -ge 2 ]; then todo "pip install --user 'numpy<2'  (you have $numpy_version; ROS 2 cv_bridge breaks on numpy 2)"
    else ok "numpy $numpy_version"; fi
    paho_version="$(python3 -c 'import importlib.metadata as m; print(m.version("paho-mqtt"))' 2>/dev/null)"
    if [ -z "$paho_version" ] || [ "${paho_version%%.*}" -lt 2 ]; then todo "pip install --user 'paho-mqtt>=2'  (found: ${paho_version:-none})"
    else ok "paho-mqtt $paho_version"; fi
    cv_version="$(python_version_of cv2)"
    [ -n "$cv_version" ] && info "OpenCV (python3): $cv_version" || info "OpenCV (python3): not importable yet"
    mujoco_py="$(python_version_of mujoco)"
    info "MuJoCo Python package (PacBot Task 0 uses 3.11.0): ${mujoco_py:-not installed}  — setup never changes it"

    mujoco39_dir="$(find_mujoco39_dir)"
    if [ -n "$mujoco39_dir" ]; then ok "libmujoco.so.3.9.0 (needed by the KD simulator): $mujoco39_dir"
    else todo "create $MUJOCO39_VENV with mujoco==3.9.0 (for libmujoco.so.3.9.0)"; fi

    if [ -d "$KD_WS/src/.git" ]; then
        branch="$(git -C "$KD_WS/src" rev-parse --abbrev-ref HEAD)"
        [ "$branch" = "kd_sim" ] && ok "$KD_WS (branch kd_sim)" || warn "$KD_WS is on branch '$branch', expected kd_sim — setup will not switch branches"
        info "setup will also git pull + rebuild $KD_WS (quick if nothing changed)"
    elif [ -e "$KD_WS" ]; then
        bad "$KD_WS exists but src/ is not the e-Yantra git clone — move it aside, then re-run"
    else
        todo "clone Khoj-o-Drone (kd_sim) into $KD_WS and colcon build"
    fi
    [ -d "$OLD_KD_WS" ] && warn "$OLD_KD_WS still exists — the Task 1 page says delete it and use $KD_WS (setup won't delete it for you)"

    if [ -d "$PB_WS/.git" ]; then ok "$PB_WS (git clone)"; info "setup will also git pull $PB_WS and create missing task_1*.py copies"
    elif [ -e "$PB_WS" ]; then bad "$PB_WS exists but is not the PacBot git clone — move it aside, then re-run"
    else todo "clone PacBot into $PB_WS"; fi

    grep -q "^$BLOCK_START" "$BASHRC" 2>/dev/null && ok "~/.bashrc has the eyrc4817 block" || todo "add the eyrc4817 block to ~/.bashrc (backup first)"
    if grep -nE '^[^#]*source .*pico_mujoco_ws/install/setup\.bash' "$BASHRC" >/dev/null 2>&1 && [ ! -f "$OLD_KD_WS/install/setup.bash" ]; then
        todo "comment out the ~/.bashrc line that sources the missing pico_mujoco_ws (it prints an error in every terminal)"
    fi
    systemctl is-enabled --quiet mosquitto 2>/dev/null && systemctl is-active --quiet mosquitto 2>/dev/null \
        && ok "mosquitto broker enabled and running" || todo "enable and start the mosquitto broker"
}

# ------------------------------------------------------------------ 3. install (only in install mode)
update_bashrc() {  # $1 = directory holding libmujoco.so.3.9.0
    local mujoco_dir="$1"
    [ -f "$BASHRC" ] || touch "$BASHRC"
    [ -f "$BASHRC.eyrc4817-backup" ] || cp "$BASHRC" "$BASHRC.eyrc4817-backup"
    if [ ! -f "$OLD_KD_WS/install/setup.bash" ]; then
        sed -i -E 's|^([^#]*source .*pico_mujoco_ws/install/setup\.bash.*)$|# [eyrc4817: disabled, workspace no longer exists] \1|' "$BASHRC"
    fi
    sed -i "/^$BLOCK_START\$/,/^$BLOCK_END\$/d" "$BASHRC"
    cat >> "$BASHRC" <<EOF
$BLOCK_START
# Added by eyrc4817 setup.sh — safe to edit; re-running setup rewrites only this block.
source /opt/ros/humble/setup.bash
[ -f "\$HOME/pico_ws/install/setup.bash" ] && source "\$HOME/pico_ws/install/setup.bash"
# The Khoj-o-Drone simulator needs libmujoco.so.3.9.0 (e-Yantra's build looks in a path from their own machine)
export LD_LIBRARY_PATH="$mujoco_dir\${LD_LIBRARY_PATH:+:\$LD_LIBRARY_PATH}"
# Keep ROS 2 traffic on this laptop, so teammates' simulators on the same Wi-Fi don't interfere.
# Remove this line only if you really need ROS 2 across machines.
export ROS_LOCALHOST_ONLY=1
$BLOCK_END
EOF
}

install_everything() {
    say "3. Installing what's missing (you may be asked for your password once)"
    sudo -v || { bad "sudo is needed for apt and the broker"; return; }

    if [ ${#missing_apt[@]} -gt 0 ]; then
        info "apt: ${missing_apt[*]}"
        sudo apt-get update -qq && sudo apt-get install -y "${missing_apt[@]}" || bad "apt install failed"
    fi

    numpy_version="$(python_version_of numpy)"
    if [ -z "$numpy_version" ] || [ "${numpy_version%%.*}" -ge 2 ]; then python3 -m pip install --user -q "numpy<2" || bad "pip numpy<2 failed"; fi
    paho_version="$(python3 -c 'import importlib.metadata as m; print(m.version("paho-mqtt"))' 2>/dev/null)"
    if [ -z "$paho_version" ] || [ "${paho_version%%.*}" -lt 2 ]; then python3 -m pip install --user -q "paho-mqtt>=2" || bad "pip paho-mqtt failed"; fi

    if [ -z "$(find_mujoco39_dir)" ]; then
        info "creating $MUJOCO39_VENV (mujoco 3.9.0, ~60 MB)"
        python3 -m venv "$MUJOCO39_VENV" && "$MUJOCO39_VENV/bin/pip" install -q "mujoco==3.9.0" || bad "MuJoCo 3.9.0 venv failed"
    fi

    source /opt/ros/humble/setup.bash
    if [ -d "$KD_WS/src/.git" ]; then
        git -C "$KD_WS/src" pull --ff-only && git -C "$KD_WS/src" submodule update --init --recursive || warn "could not update $KD_WS (local changes?) — building what's there"
    elif [ ! -e "$KD_WS" ]; then
        mkdir -p "$KD_WS/src" && git clone -b kd_sim --recursive "$KD_REPO" "$KD_WS/src" || bad "clone of Khoj-o-Drone failed"
    fi
    if [ -d "$KD_WS/src/.git" ]; then
        info "colcon build in $KD_WS (a few minutes the first time)"
        (cd "$KD_WS" && colcon build 2>&1 | tail -3) || bad "colcon build failed — see ~/eyrc4817-setup.log"
    fi

    if [ -d "$PB_WS/.git" ]; then
        git -C "$PB_WS" pull --ff-only || warn "could not update $PB_WS (local changes?)"
    elif [ ! -e "$PB_WS" ]; then
        git clone "$PB_REPO" "$PB_WS" || bad "clone of PacBot failed"
    fi
    for task_dir in "$PB_WS"/task1a "$PB_WS"/task1b; do
        [ -d "$task_dir" ] || continue
        for boilerplate in "$task_dir"/task_1*_boilerplate.py; do
            [ -f "$boilerplate" ] || continue
            working_copy="${boilerplate%_boilerplate.py}.py"
            [ -f "$working_copy" ] || { cp "$boilerplate" "$working_copy"; info "created $(basename "$working_copy") from the boilerplate"; }
        done
        chmod +x "$task_dir"/task_1*_launch 2>/dev/null
    done

    mujoco39_dir="$(find_mujoco39_dir)"
    update_bashrc "$mujoco39_dir"
    info "~/.bashrc updated (backup: ~/.bashrc.eyrc4817-backup)"
    sudo systemctl enable --now mosquitto >/dev/null 2>&1 || bad "could not enable mosquitto"
}

# ------------------------------------------------------------------ 4. verification
verify() {
    say "4. Verification"
    source /opt/ros/humble/setup.bash 2>/dev/null
    [ -f "$KD_WS/install/setup.bash" ] && source "$KD_WS/install/setup.bash"
    local mujoco_dir; mujoco_dir="$(find_mujoco39_dir)"
    [ -n "$mujoco_dir" ] && export LD_LIBRARY_PATH="$mujoco_dir:${LD_LIBRARY_PATH:-}"

    python3 - <<'PY' && ok "Python: OpenCV 4.5.x + old ArUco API, numpy < 2, cv_bridge, paho-mqtt >= 2" || bad "Python packages (see line above)"
import sys, importlib.metadata as md
problems = []
try:
    import cv2
    if not cv2.__version__.startswith("4.5."): problems.append(f"cv2 {cv2.__version__} (expected apt 4.5.x; never pip-install opencv-python)")
    if not hasattr(cv2, "aruco") or not hasattr(cv2.aruco, "detectMarkers"): problems.append("cv2.aruco.detectMarkers missing")
except ImportError: problems.append("cv2 not importable")
try:
    import numpy
    if int(numpy.__version__.split(".")[0]) >= 2: problems.append(f"numpy {numpy.__version__} (needs < 2)")
except ImportError: problems.append("numpy not importable")
try:
    from cv_bridge import CvBridge
except Exception as error: problems.append(f"cv_bridge: {error}")
try:
    if int(md.version("paho-mqtt").split(".")[0]) < 2: problems.append("paho-mqtt < 2")
except md.PackageNotFoundError: problems.append("paho-mqtt missing")
if problems:
    print("           " + "; ".join(problems)); sys.exit(1)
PY
    [ -n "$mujoco_dir" ] && ok "libmujoco.so.3.9.0 found" || bad "libmujoco.so.3.9.0 not found"
    local bridge; bridge="$(ros2 pkg prefix swift_pico 2>/dev/null)/lib/swift_pico/mujoco_bridge"
    if [ -x "$bridge" ]; then
        local missing; missing="$(ldd "$bridge" | grep 'not found')"
        [ -z "$missing" ] && ok "KD simulator: all libraries found" || bad "KD simulator is missing: $missing"
    else
        bad "KD workspace not built ($KD_WS)"
    fi
    ros2 pkg executables swift_pico 2>/dev/null | grep -q task_1c_controller && ok "KD task_1b / task_1c controllers" || bad "KD controllers not found"
    ros2 pkg executables pid_tune 2>/dev/null | grep -q button_ui && ok "KD PID tuner GUI" || bad "KD PID tuner not found"
    [ -x "$PB_WS/task1a/task_1a_launch" ] && [ -f "$PB_WS/task1a/task_1a.py" ] && ok "PacBot Task 1A: launcher + task_1a.py" || bad "PacBot Task 1A files missing"
    [ -x "$PB_WS/task1b/task_1b_launch" ] && [ -f "$PB_WS/task1b/task_1b.py" ] && ok "PacBot Task 1B: launcher + task_1b.py" || bad "PacBot Task 1B files missing"
    systemctl is-active --quiet mosquitto && ok "mosquitto broker running" || bad "mosquitto not running"
}

summary() {
    say "Where everything is"
    info "Team repo (docs, roadmap, tools) : $REPO_DIR"
    info "Khoj-o-Drone workspace           : $KD_WS    (Task 1A script + image in src/swift_pico/scripts/)"
    info "PacBot workspace                 : $PB_WS    (task1a/, task1b/)"
    info "Setup log                        : ~/eyrc4817-setup.log"
    say "Result"
    if [ "$MODE" = "check" ]; then
        if [ ${#planned[@]} -eq 0 ] && [ "$failures" -eq 0 ]; then echo "  Everything is set up. Nothing to do."
        else echo "  ${#planned[@]} thing(s) to do, $failures problem(s). Run without --check to set up:  bash setup/setup.sh"; fi
    else
        [ "$failures" -eq 0 ] && echo "  All checks passed. Open a NEW terminal, then start with README.md → 'First day'." \
                               || echo "  $failures problem(s) — see [!!] lines above and ~/eyrc4817-setup.log"
    fi
    [ "$warnings" -gt 0 ] && echo "  $warnings warning(s) — read the [warn] lines."
}

main() {
    case "${1:-}" in
        --check|--dry-run) MODE=check ;;
        "") MODE=install ;;
        -h|--help) usage; exit 0 ;;
        *) usage; exit 2 ;;
    esac
    exec > >(tee -a "$HOME/eyrc4817-setup.log") 2>&1
    echo "---- eyrc4817 setup ($MODE) $(date) ----"
    preflight
    if [ "$failures" -gt 0 ] && [ "$MODE" = "install" ]; then
        say "Stopping: fix the [!!] items above first (nothing was changed)."
        exit 1
    fi
    inventory
    [ "$MODE" = "install" ] && install_everything
    verify
    summary
    exit "$failures"
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    main "$@"
fi
