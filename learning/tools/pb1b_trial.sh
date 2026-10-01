#!/usr/bin/env bash
# One PacBot Task 1B trial in EVALUATE mode (the only mode that reports collisions):
#   ./task_1b_launch --evaluate -> python3 task_1b.py -> wait for "wrote result" or the time limit
#   -> stop both -> print collisions, the controller's turns, and result.json.
# The launcher is only RUN, never inspected (e-Yantra tamper rule).
#
# Usage:  pb1b_trial.sh [MAX_SECONDS=300] [LABEL]
# Output: ~/pb1b_trials/<time>_<LABEL>/  launcher.log, controller.log, result.json (copy), task_1b.py (copy)
set -u
set -m   # each background job gets its own process group, and SIGINT is not ignored in it
MAX=${1:-300}
LABEL=${2:-run}
TASK=~/pacbot_ws/task1b
OUT=~/pb1b_trials/$(date +%H%M%S)_$LABEL
mkdir -p "$OUT"
cp "$TASK/task_1b.py" "$OUT/"          # remember exactly which code this trial ran

stop() {  # SIGINT the process group; the GUI launcher may ignore it, so fall back to SIGTERM
  local pgid=$1
  kill -INT -- -"$pgid" 2>/dev/null
  for _ in $(seq 10); do kill -0 -- -"$pgid" 2>/dev/null || return 0; sleep 0.5; done
  kill -TERM -- -"$pgid" 2>/dev/null
  for _ in $(seq 10); do kill -0 -- -"$pgid" 2>/dev/null || return 0; sleep 0.5; done
  echo "warning: process group $pgid still running"
}

cd "$TASK"
rm -f result.json
# `script` gives the launcher a pseudo-terminal, so it prints line by line: redirected straight to a file it
# buffers its output, and the collision lines were lost when it was stopped (trial 1, 1 Oct).
script -qfec "./task_1b_launch --evaluate" "$OUT/launcher.log" > /dev/null 2>&1 &
SIM=$!
for _ in $(seq 30); do grep -qsi 'evaluat' "$OUT/launcher.log" && break; sleep 0.5; done
sleep 2   # let the simulator publish its first sensor readings

python3 -u task_1b.py > "$OUT/controller.log" 2>&1 &
CTL=$!

START=$SECONDS
SOLVED_AT=""
while (( SECONDS - START < MAX )); do
  [ -z "$SOLVED_AT" ] && grep -qsi 'maze solved' "$OUT/launcher.log" && SOLVED_AT=$((SECONDS - START))
  grep -qsiE 'wrote.*result' "$OUT/launcher.log" && break     # the launcher says "wrote sealed result"
  kill -0 "$SIM" 2>/dev/null || break
  sleep 1
done
ELAPSED=$((SECONDS - START))
sleep 1
stop "$CTL"; stop "$SIM"
# the launcher runs in its own session under `script`; make sure it is gone (-x matches the process name only)
pkill -INT -x task_1b_launch 2>/dev/null; sleep 2; pkill -TERM -x task_1b_launch 2>/dev/null
[ -f result.json ] && cp result.json "$OUT/"

echo "== PB 1B trial $LABEL: ${ELAPSED}s (limit ${MAX}s), MAZE SOLVED at ${SOLVED_AT:-never}s after the controller started -> $OUT"
echo "   collision lines printed by the launcher: $(grep -ci 'collision' "$OUT/launcher.log")"
echo "-- launcher (collisions / solved / result):"
grep -iE 'collision|solved|wrote|evaluat|error|exit|clear' "$OUT/launcher.log" | tail -15
echo "-- controller turns and exit:"
grep -E 'turn|clear of the maze|stopped' "$OUT/controller.log" | tail -25
echo "-- last status line:"
grep -E '^t=' "$OUT/controller.log" | tail -1
[ -f "$OUT/result.json" ] && { echo "-- result.json:"; head -c 600 "$OUT/result.json"; echo; }
python3 "$(dirname "$0")/pb1b_path.py" "$OUT/controller.log" 2>&1 | tail -1
