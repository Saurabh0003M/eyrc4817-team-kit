#!/usr/bin/env bash
# KD Task 2A / 2B / 2C recorded run, one command: screen recording -> sim -> waypoint_service -> pico_client ->
# ros2 bag -> pico_server (the runbook order), stops when the client reports all waypoints reached, scores the
# bag (practice estimate), and builds the upload folder with the renamed scripts + bag + zip.
# 2A: sim -> ros2 bag (with /pos_error) -> pico_controller_PID.py, held for HOLD_RUN s (the portal wants >= 60 s),
# scored with bag_score.py, zip = KD_4817_task_2a.py + bag.
#
# Usage:  kd_record.sh 2a|2b|2c [--no-video] [--yes]
#   --no-video  rehearsal: no screen recording
#   --yes       do not wait for Enter (window arranging)
# Output: ~/kd_runs/<task>_<time>/ (logs + bag), ~/kd_upload_<task>/KD_4817_task_<task>.zip,
#         video ~/Videos/Screencasts/KD_4817_Task_<task>_<time>.webm
# The graded scripts come from ~/kd_submissions/task_<task>/ (never from this public repo). If the workspace
# holds the other task's waypoint_service, it is swapped in and swift_pico is rebuilt (plain colcon build).
# Everything is stopped with SIGINT (Ctrl+C), never SIGTERM (SIGTERM makes ros2 CLI crash-report).
# Every background job reads stdin from /dev/null: `ros2 bag record` has keyboard controls, and a background job
# that reads the terminal is frozen by job control (SIGTTIN): no bag at all (found on the first real 2A run, 16 Oct).
source /opt/ros/humble/setup.bash       # (ROS setup files break under set -u, so source first)
eval "$(grep -E '^export LD_LIBRARY_PATH=' ~/.bashrc)"   # mujoco_bridge needs libmujoco.so.3.9.0
set -u
set -m   # each background job gets its own process group, and SIGINT is not ignored in it

TASK=${1:-}
[[ "$TASK" == 2a || "$TASK" == 2b || "$TASK" == 2c ]] || { echo "usage: kd_record.sh 2a|2b|2c [--no-video] [--yes]"; exit 1; }
VIDEO=1; ASK=1
for arg in "${@:2}"; do
  [[ "$arg" == --no-video ]] && VIDEO=0
  [[ "$arg" == --yes ]] && ASK=0
done
TOOLS="$(cd "$(dirname "$0")" && pwd)"
STAMP=$(date +%Y%m%d_%H%M%S)
SUB=${KD_SUB:-$HOME/kd_submissions}/task_$TASK   # KD_SUB=<folder>: rehearse a variant (never for the real run)
SRC=~/pico_ws/src/swift_pico/src
RUN=~/kd_runs/${TASK}_$STAMP
UPLOAD=~/kd_upload_$TASK     # real (recorded) runs only; a rehearsal zips inside its run folder
BAG=task_$TASK
FLIGHT_TIMEOUT=180      # s from starting the server; the full-marks finish is 40 s (2B) / 60 s (2C)
HOLD_RUN=75             # 2A: s the controller runs (the portal asks for >= 60 s of recording)
if [[ "$TASK" == 2a ]]; then
  SCRIPTS=(pico_controller_PID); EXT=.py      # installed under its own name, run as pico_controller_PID.py
else
  SCRIPTS=(waypoint_service pico_client pico_server); EXT=""
fi
mkdir -p "$RUN"
(( VIDEO )) || UPLOAD=$RUN/rehearsal_upload   # no video: never a submit-ready zip next to a real one

# 1. the right scripts in the workspace, built
changed=0
for f in "${SCRIPTS[@]}"; do
  if ! cmp -s "$SUB/$f.py" "$SRC/$f.py"; then cp "$SUB/$f.py" "$SRC/$f.py"; changed=1; fi
done
if (( changed )); then
  echo "workspace held other scripts: rebuilding swift_pico for task $TASK ..."
  (cd ~/pico_ws && colcon build --packages-select swift_pico > "$RUN/build.log" 2>&1) || { echo "BUILD FAILED: $RUN/build.log"; exit 1; }
fi
set +u; source ~/pico_ws/install/setup.bash; set -u     # ROS setup files break under set -u
for f in "${SCRIPTS[@]}"; do
  cmp -s "$SUB/$f.py" ~/pico_ws/install/swift_pico/lib/swift_pico/$f$EXT || { echo "installed $f$EXT differs from $SUB/$f.py"; exit 1; }
done

declare -A PGID
start() {   # start <name> <command...>: own process group, log file, prefixed live output
  local name=$1; shift
  ( "$@" < /dev/null 2>&1 | tee "$RUN/$name.log" | sed -u "s/^/[$name] /" ) &
  PGID[$name]=$!
}
stop() {    # SIGINT a whole process group, wait up to 10 s
  local pgid=${PGID[$1]:-}
  [[ -z "$pgid" ]] && return 0
  kill -INT -- -"$pgid" 2>/dev/null
  for _ in $(seq 20); do kill -0 -- -"$pgid" 2>/dev/null || return 0; sleep 0.5; done
  echo "warning: $1 still running"
}
cleanup() { for n in bag controller server client service sim video; do stop "$n"; done; }
trap 'echo; echo "interrupted: stopping everything"; cleanup; exit 130' INT

echo "=== KD Task ${TASK^^} run · team 4817 · $(date '+%Y-%m-%d %H:%M') ==="
if (( ASK )); then read -r -p "Close other windows (and the Claude app). Press Enter to start$( ((VIDEO)) && echo ' the screen recording')... " _; fi
if (( VIDEO )); then
  start video python3 "$TOOLS/screen_record.py" "KD_4817_Task_${TASK}"
  sleep 2
fi

# 2. sim first; window arranging while it settles
start sim env vblank_mode=0 ros2 launch swift_pico swift_pico_simulation.launch.py
sleep 10
if (( ASK )); then read -r -p "Simulator window -> Super+Right, this terminal -> Super+Left. Then press Enter... " _; fi

if [[ "$TASK" == 2a ]]; then
  # 3. bag first (a late bag scores 0), then the controller: it arms and flies to the setpoint by itself
  ( cd "$RUN" && exec ros2 bag record -o "$BAG" /pos_error /whycode_node/markers /controller_heartbeat < /dev/null ) > "$RUN/bag.log" 2>&1 &
  PGID[bag]=$!
  sleep 3
  start controller ros2 run swift_pico pico_controller_PID.py
  t0=$SECONDS
  # 4. hold for HOLD_RUN s
  while (( SECONDS - t0 < HOLD_RUN )); do sleep 1; done
  stop bag; sleep 1
  stop controller; stop sim
  (( VIDEO )) && { sleep 1; stop video; }
  # 5. score + upload folder
  echo
  echo "=== ran $((SECONDS - t0)) s ==="
  python3 "$TOOLS/bag_score.py" 2a "$RUN/$BAG" | tee "$RUN/score.txt"
  if [[ -f "$RUN/$BAG/${BAG}_0.db3" && -f "$RUN/$BAG/metadata.yaml" ]]; then
    [[ -d "$UPLOAD" ]] && mv "$UPLOAD" "${UPLOAD}_previous_$STAMP"
    mkdir -p "$UPLOAD"
    cp "$SUB/pico_controller_PID.py" "$UPLOAD/KD_4817_task_2a.py"
    cp "$RUN/$BAG/${BAG}_0.db3" "$RUN/$BAG/metadata.yaml" "$UPLOAD/"
    (cd "$UPLOAD" && zip -q KD_4817_task_2a.zip KD_4817_task_2a.py "${BAG}_0.db3" metadata.yaml && unzip -l KD_4817_task_2a.zip)
    echo "zip: $UPLOAD/KD_4817_task_2a.zip"
  else
    echo "no zip: the bag is missing (logs in $RUN)"
  fi
  (( VIDEO )) && echo "video: $(ls -t ~/Videos/Screencasts/KD_4817_Task_2a_*.webm 2>/dev/null | head -1)  (YouTube title KD_4817_Task_2a, Unlisted)"
  echo "logs: $RUN"
  exit 0
fi

# 3. service, client, bag (before the server: a late bag scores 0), server
start service ros2 run swift_pico waypoint_service
sleep 3
start client ros2 run swift_pico pico_client
sleep 2
( cd "$RUN" && exec ros2 bag record -o "$BAG" /whycode_node/markers /controller_heartbeat < /dev/null ) > "$RUN/bag.log" 2>&1 &
PGID[bag]=$!
sleep 3
start server ros2 run swift_pico pico_server
t0=$SECONDS

# 4. wait for the client's success line
result=TIMEOUT
while (( SECONDS - t0 < FLIGHT_TIMEOUT )); do
  if grep -q "All waypoints have been reached successfully" "$RUN/client.log" 2>/dev/null; then result=DONE; break; fi
  sleep 1
done
sleep 2
stop bag; sleep 1
stop server; stop client; stop service; stop sim
(( VIDEO )) && { sleep 1; stop video; }

# 5. score + upload folder
echo
echo "=== $result after $((SECONDS - t0)) s ==="
python3 "$TOOLS/kd2_bag_score.py" "$TASK" "$RUN/$BAG" "$RUN/client.log" | tee "$RUN/score.txt"
if [[ "$result" == DONE && -f "$RUN/$BAG/${BAG}_0.db3" && -f "$RUN/$BAG/metadata.yaml" ]]; then
  [[ -d "$UPLOAD" ]] && mv "$UPLOAD" "${UPLOAD}_previous_$STAMP"
  mkdir -p "$UPLOAD"
  for f in waypoint_service pico_client pico_server; do cp "$SUB/$f.py" "$UPLOAD/KD_4817_$f.py"; done
  cp "$RUN/$BAG/${BAG}_0.db3" "$RUN/$BAG/metadata.yaml" "$UPLOAD/"
  (cd "$UPLOAD" && zip -q "KD_4817_task_$TASK.zip" KD_4817_waypoint_service.py KD_4817_pico_client.py \
     KD_4817_pico_server.py "${BAG}_0.db3" metadata.yaml && unzip -l "KD_4817_task_$TASK.zip")
  echo "zip: $UPLOAD/KD_4817_task_$TASK.zip"
else
  echo "no zip: the run did not finish cleanly (logs in $RUN)"
fi
(( VIDEO )) && echo "video: $(ls -t ~/Videos/Screencasts/KD_4817_Task_${TASK}_*.webm 2>/dev/null | head -1)  (YouTube title KD_4817_Task_${TASK}, Unlisted)"
echo "logs: $RUN"
