#!/usr/bin/env python3
"""Print how the errors moved during a KD 1B/1C bag: first moment inside ±0.4, the extremes after
that, and a 1-second timeline of the first 20 s. Companion to bag_score.py (which gives the marks).

    source ~/pico_ws/install/setup.bash
    python3 kd1b_timeline.py task_1b          # 1B: throttle only
    python3 kd1b_timeline.py task_1c 1c       # 1C: throttle (z), pitch (x) and roll (y) together
"""
import sys

import rosbag2_py
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message

BOX = 0.4
FIELDS = {"1b": ["throttle_error"], "1c": ["throttle_error", "pitch_error", "roll_error"]}
SHORT = {"throttle_error": "z", "pitch_error": "x", "roll_error": "y"}

bag = sys.argv[1]
task = sys.argv[2] if len(sys.argv) > 2 else "1b"
fields = FIELDS[task]

reader = rosbag2_py.SequentialReader()
reader.open(rosbag2_py.StorageOptions(uri=bag, storage_id="sqlite3"),
            rosbag2_py.ConverterOptions("cdr", "cdr"))
types = {t.name: t.type for t in reader.get_all_topics_and_types()}
pts = []
while reader.has_next():
    topic, data, stamp = reader.read_next()
    if topic == "/pos_error":
        msg = deserialize_message(data, get_message(types[topic]))
        pts.append((stamp, [getattr(msg, f) for f in fields]))
if not pts:
    sys.exit("no /pos_error messages in the bag")

t0 = pts[0][0]
pts = [((t - t0) / 1e9, vals) for t, vals in pts]
first_in = next((s for s, vals in pts if all(abs(v) < BOX for v in vals)), None)
print(f"first moment all inside ±{BOX}: {'never' if first_in is None else f'{first_in:.1f} s'}")
settle = pts if first_in is None else [(s, v) for s, v in pts if s >= first_in + 1]
for i, f in enumerate(fields):
    if settle:
        vals = [v[i] for _, v in settle]
        print(f"   {f:15s} {'after entry+1 s' if first_in is not None else 'whole bag'}: "
              f"{min(vals):+.2f} .. {max(vals):+.2f}")

row, last = [], -1.0
for s, vals in pts:
    if s > 20:
        break
    if s - last >= 1:
        row.append(f"{s:3.0f}s " + " ".join(f"{SHORT[f]}{v:+.2f}" for f, v in zip(fields, vals)))
        last = s
per_line = 7 if len(fields) == 1 else 4
for i in range(0, len(row), per_line):
    print("   " + "   ".join(row[i:i + per_line]))
