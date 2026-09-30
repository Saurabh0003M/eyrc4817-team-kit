#!/usr/bin/env python3
"""Print how throttle_error moved during a KD 1B bag: first entry into ±0.4, overshoot, and a
1-second timeline of the first 20 s. Companion to bag_score.py (which gives the marks).

    source ~/pico_ws/install/setup.bash
    python3 kd1b_timeline.py task_1b
"""
import sys

import rosbag2_py
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message

BOX = 0.4

reader = rosbag2_py.SequentialReader()
reader.open(rosbag2_py.StorageOptions(uri=sys.argv[1], storage_id="sqlite3"),
            rosbag2_py.ConverterOptions("cdr", "cdr"))
types = {t.name: t.type for t in reader.get_all_topics_and_types()}
err = []
while reader.has_next():
    topic, data, stamp = reader.read_next()
    if topic == "/pos_error":
        err.append((stamp, deserialize_message(data, get_message(types[topic])).throttle_error))
if not err:
    sys.exit("no /pos_error messages in the bag")

t0 = err[0][0]
pts = [((t - t0) / 1e9, v) for t, v in err]
first_in = next((s for s, v in pts if abs(v) < BOX), None)
print(f"first inside ±{BOX}: {'never' if first_in is None else f'{first_in:.1f} s'}"
      f"   |   lowest error {min(v for _, v in pts):+.2f} (negative = went ABOVE target)"
      f"   |   last 5 s range {min(v for s, v in pts if s > pts[-1][0] - 5):+.2f}"
      f" .. {max(v for s, v in pts if s > pts[-1][0] - 5):+.2f}")
row, last = [], -1.0
for s, v in pts:
    if s > 20:
        break
    if s - last >= 1:
        row.append(f"{s:3.0f}s {v:+.2f}")
        last = s
for i in range(0, len(row), 7):
    print("   " + "   ".join(row[i:i + 7]))
