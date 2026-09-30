#!/usr/bin/env bash
# One KD Task 1B tuning trial from a FRESH takeoff:
#   sim -> task_1b_controller (answers N, types the gains) -> bag starts at once -> wait -> stop -> score.
# The bag starts together with the controller, so the timing is the worst case
# (in a real run you start the bag a few seconds later, when the drone is already climbing).
#
# Usage:  kd1b_trial.sh KP KI KD [SECONDS=35]
# Output: ~/kd1b_trials/kp<KP>_ki<KI>_kd<KD>/  (bag) + .sim/.ctl/.bag logs next to it
# Everything is stopped with SIGINT (Ctrl+C), never SIGTERM (SIGTERM makes ros2 CLI crash-report).
source /opt/ros/humble/setup.bash       # (ROS setup files break under set -u, so source first)
source ~/pico_ws/install/setup.bash
# mujoco_bridge needs libmujoco.so.3.9.0: reuse the LD_LIBRARY_PATH line(s) that setup.sh
# (or a manual fix) put in ~/.bashrc, since scripts don't read ~/.bashrc themselves.
eval "$(grep -E '^export LD_LIBRARY_PATH=' ~/.bashrc)"
set -u
set -m   # each background job gets its own process group, and SIGINT is not ignored in it
KP=$1 KI=$2 KD=$3 SECS=${4:-35}
TOOLS="$(cd "$(dirname "$0")" && pwd)"

OUT=~/kd1b_trials
NAME="kp${KP}_ki${KI}_kd${KD}"
mkdir -p "$OUT"
rm -rf "${OUT:?}/$NAME"
cd "$OUT"

stop() {  # SIGINT a whole process group, wait up to 10 s
  local pgid=$1
  kill -INT -- -"$pgid" 2>/dev/null
  for _ in $(seq 20); do kill -0 -- -"$pgid" 2>/dev/null || return 0; sleep 0.5; done
  echo "warning: process group $pgid still running"
}

ros2 launch swift_pico swift_pico_simulation.launch.py > "$NAME.sim.log" 2>&1 &
SIM=$!
sleep 8   # MuJoCo bridge + WhyCode camera need a few seconds

printf 'N\n%s\n%s\n%s\n' "$KP" "$KI" "$KD" | ros2 run swift_pico task_1b_controller > "$NAME.ctl.log" 2>&1 &
CTL=$(ps -o pgid= -p $! | tr -d ' ')   # the pipeline's process group
ros2 bag record -o "$NAME" /pos_error /whycode_node/markers > "$NAME.bag.log" 2>&1 &
BAG=$!

sleep "$SECS"
stop "$BAG"; stop "$CTL"; stop "$SIM"

echo "== $NAME  (bag starts with the controller = worst case)"
python3 "$TOOLS/bag_score.py" 1b "$NAME" 2>&1 | grep -vE '^\[INFO\]' | sed -n '2,$p'
python3 "$TOOLS/kd1b_timeline.py" "$NAME" 2>&1 | grep -vE '^\[INFO\]'
