#!/usr/bin/env python3
"""
Practice-score estimator for KD Task 1B / 1C bag recordings.

Reads /pos_error from a ros2 bag and applies the portal's scoring table:
  Hovering 16  — per second inside the ±0.4 box, up to 10 s
  Finishing 8  — only if a full 10 s hover is completed
  Speed 16     — full if finished within 15 s, falling to 0 at 60 s

ASSUMPTIONS (the portal does not define these; ask on the forum before trusting the number):
  * the clock starts at the bag's first /pos_error message;
  * "hovering seconds" means the longest continuous stretch inside the box (the cumulative total
    is printed too);
  * "finish" = the moment the first 10 s continuous hover completes; speed falls linearly 15 → 60 s.

    source ~/pico_ws/install/setup.bash
    python3 bag_score.py 1b task_1b        # the folder ros2 bag record -o task_1b created
    python3 bag_score.py 1c task_1c
"""
import argparse
import sys

try:
    import rosbag2_py
    from rclpy.serialization import deserialize_message
    from rosidl_runtime_py.utilities import get_message
except ImportError:
    sys.exit('Source ROS 2 and the workspace first:  source ~/pico_ws/install/setup.bash')

BOX = 0.4
FIELDS = {'1b': ['throttle_error'], '1c': ['throttle_error', 'pitch_error', 'roll_error']}


def read_errors(bag_dir):
    reader = rosbag2_py.SequentialReader()
    reader.open(rosbag2_py.StorageOptions(uri=bag_dir, storage_id='sqlite3'),
                rosbag2_py.ConverterOptions(input_serialization_format='cdr', output_serialization_format='cdr'))
    types = {t.name: t.type for t in reader.get_all_topics_and_types()}
    if '/pos_error' not in types:
        sys.exit(f'/pos_error is not in this bag (topics: {", ".join(types)})')
    message_type = get_message(types['/pos_error'])
    samples = []
    while reader.has_next():
        topic, data, stamp_ns = reader.read_next()
        if topic == '/pos_error':
            samples.append((stamp_ns / 1e9, deserialize_message(data, message_type)))
    return samples


def main():
    parser = argparse.ArgumentParser(description='Estimate KD Task 1B/1C marks from a practice bag.')
    parser.add_argument('task', choices=['1b', '1c'])
    parser.add_argument('bag', help='bag folder (contains metadata.yaml and *_0.db3)')
    args = parser.parse_args()

    samples = read_errors(args.bag)
    if len(samples) < 2:
        sys.exit('Fewer than 2 /pos_error messages: was the controller running while recording?')
    fields = FIELDS[args.task]
    t0 = samples[0][0]
    duration = samples[-1][0] - t0

    cumulative, streak_start, longest, finish_time = 0.0, None, 0.0, None
    for (t, msg), (t_next, _) in zip(samples, samples[1:] + [samples[-1]]):
        inside = all(abs(getattr(msg, f)) <= BOX for f in fields)
        if inside:
            cumulative += t_next - t
            streak_start = t if streak_start is None else streak_start
            streak = t_next - streak_start
            longest = max(longest, streak)
            if finish_time is None and streak >= 10.0:
                finish_time = streak_start + 10.0 - t0
        else:
            streak_start = None

    hover = 16 * min(longest, 10.0) / 10.0
    bonus = 8 if finish_time is not None else 0
    if finish_time is None:
        speed = 0.0
    else:
        speed = 16.0 if finish_time <= 15 else max(0.0, 16.0 * (60 - finish_time) / 45)
    worst = {f: max(abs(getattr(m, f)) for _, m in samples) for f in fields}

    print(f'Bag: {args.bag}  ·  {len(samples)} /pos_error messages over {duration:.1f} s  ·  axes: {", ".join(fields)}')
    print(f'Largest |error| seen: ' + ', '.join(f'{f} {v:.2f}' for f, v in worst.items()))
    print(f'Inside ±{BOX}: longest continuous {longest:.1f} s, cumulative {cumulative:.1f} s')
    print(f'10 s hover completed at: {"t = %.1f s" % finish_time if finish_time is not None else "never"}')
    print(f'\nEstimated marks (see ASSUMPTIONS in this file):')
    print(f'  Hovering  {hover:5.1f} / 16')
    print(f'  Finishing {bonus:5.1f} / 8')
    print(f'  Speed     {speed:5.1f} / 16')
    print(f'  Total     {hover + bonus + speed:5.1f} / 40')
    if duration < 60:
        print(f'\nNote: the submission needs a recording of at least 60 s (this one is {duration:.0f} s).')


if __name__ == '__main__':
    main()
