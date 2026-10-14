#!/usr/bin/env python3
"""
Practice-score estimator for KD Task 2B / 2C bag recordings.

Reads the drone's position from /whycode_node/markers in a ros2 bag and the waypoints from the
pico_client log ("Waypoints: [x, y, z]" lines), then applies the portal's scoring table:
  2B (in order):  per waypoint reach 2 + hold 3 s 6;  speed 8 only if all four held:
                  full by 40 s, -0.13 per second after, 0 at 100 s
  2C (any order): per survivor reach 2 + hold 3 s 6;  speed 8: full by 60 s, -0.2 per second after

ASSUMPTIONS (the portal does not define these; treat the number as a practice estimate):
  * "reached" / "held" = all three axes within +-0.4 of the waypoint (the Task 2A box); with --sphere, within
    0.4 straight-line distance (the server boilerplate measures "time inside a sphere"; the radius is not published);
  * the clock starts at the bag's first marker message; the finish is the end of the last hold.

    source ~/pico_ws/install/setup.bash
    python3 kd2_bag_score.py 2b ~/kd_rehearsal/task_2b ~/kd_rehearsal/client.log
"""
import argparse
import re
import sys

try:
    import rosbag2_py
    from rclpy.serialization import deserialize_message
    from rosidl_runtime_py.utilities import get_message
except ImportError:
    sys.exit('Source ROS 2 and the workspace first:  source ~/pico_ws/install/setup.bash')

BOX = 0.4
HOLD = 3.0
SPHERE = False      # --sphere: count "inside" as within 0.4 straight-line distance instead of per-axis


def read_track(bag_dir):
    reader = rosbag2_py.SequentialReader()
    reader.open(rosbag2_py.StorageOptions(uri=bag_dir, storage_id='sqlite3'),
                rosbag2_py.ConverterOptions(input_serialization_format='cdr', output_serialization_format='cdr'))
    types = {t.name: t.type for t in reader.get_all_topics_and_types()}
    topic = '/whycode_node/markers'
    if topic not in types:
        sys.exit(f'{topic} is not in this bag (topics: {", ".join(types)})')
    msg_type = get_message(types[topic])
    track = []
    while reader.has_next():
        name, data, stamp = reader.read_next()
        if name != topic:
            continue
        msg = deserialize_message(data, msg_type)
        if msg.markers:
            p = msg.markers[0].position.position
            track.append((stamp * 1e-9, p.x, p.y, p.z))
    if not track:
        sys.exit('no marker positions in the bag')
    t0 = track[0][0]
    return [(t - t0, x, y, z) for t, x, y, z in track]


def read_waypoints(client_log):
    points = []
    for line in open(client_log, errors='replace'):
        m = re.search(r'Waypoints: \[([-\d.e]+), ([-\d.e]+), ([-\d.e]+)\]', line)
        if m:
            points.append(tuple(float(v) for v in m.groups()))
    if not points:
        sys.exit(f'no "Waypoints: [x, y, z]" lines in {client_log}')
    return points


def first_hold(track, wp, after):
    """(reach time, hold end time) of the first full HOLD inside the box after `after`, else partials."""
    reach, start = None, None
    for t, x, y, z in track:
        if t < after:
            continue
        if SPHERE:
            inside = ((x - wp[0]) ** 2 + (y - wp[1]) ** 2 + (z - wp[2]) ** 2) ** 0.5 <= BOX
        else:
            inside = abs(x - wp[0]) <= BOX and abs(y - wp[1]) <= BOX and abs(z - wp[2]) <= BOX
        if inside:
            reach = t if reach is None else reach
            start = t if start is None else start
            if t - start >= HOLD:
                return reach, t
        else:
            start = None
    return reach, None


def main():
    parser = argparse.ArgumentParser(description='Estimate KD Task 2B/2C marks from a practice bag.')
    parser.add_argument('task', choices=['2b', '2c'])
    parser.add_argument('bag', help='bag folder (contains metadata.yaml and *_0.db3)')
    parser.add_argument('client_log', help='pico_client output (has the "Waypoints: [...]" lines)')
    parser.add_argument('--sphere', action='store_true',
                        help='stricter reading: within 0.4 straight-line distance (the boilerplate talks of a sphere)')
    args = parser.parse_args()
    global SPHERE
    SPHERE = args.sphere
    track = read_track(args.bag)
    waypoints = read_waypoints(args.client_log)
    print(f'{len(track)} positions over {track[-1][0]:.1f} s; {len(waypoints)} waypoints')
    total, after, held_all, finish = 0.0, 0.0, True, 0.0
    for i, wp in enumerate(waypoints, 1):
        reach, hold_end = first_hold(track, wp, after if args.task == '2b' else 0.0)
        marks = (2 if reach is not None else 0) + (6 if hold_end is not None else 0)
        total += marks
        state = 'not reached' if reach is None else (f'reached {reach:5.1f} s, ' +
                ('held to ' + f'{hold_end:5.1f} s' if hold_end is not None else 'never held 3 s'))
        print(f'  wp{i} ({wp[0]:+.2f}, {wp[1]:+.2f}, {wp[2]:.1f}): {state}  -> {marks}/8')
        if hold_end is None:
            held_all = False
            if args.task == '2b':
                break           # in order: a skipped waypoint stops the rest from counting
        else:
            finish = max(finish, hold_end)
            after = hold_end
    full_by, slope = (40.0, 0.13) if args.task == '2b' else (60.0, 0.2)
    speed = max(0.0, 8.0 - slope * max(0.0, finish - full_by)) if held_all else 0.0
    total += speed
    print(f'  speed: finished {finish:.1f} s -> {speed:.1f}/8' if held_all else '  speed: 0 (not all held)')
    print(f'ESTIMATE {args.task.upper()}: {total:.1f} / {8 * len(waypoints) + 8}')


if __name__ == '__main__':
    main()
