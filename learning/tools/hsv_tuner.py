#!/usr/bin/env python3
"""
HSV tuner — for KD Task 1A (finding colour ranges).

Drag the six sliders to choose a colour range. Two views update live:
  - left:  the photo, showing ONLY the pixels inside your range
  - right: the mask (white = inside the range, black = outside)

Your goal: a range that keeps the red shapes and nothing else, then one that keeps the
yellow shapes and nothing else. Watch what sneaks in: trees, bright paint, shadows.

    python3 hsv_tuner.py                      # opens image_1.jpg
    python3 hsv_tuner.py --image other.jpg

Keys: p = print the current range, q or Esc = quit.
Reminder: OpenCV hue runs 0-179, not 0-359.
This is a LEARNING TOOL. It uses a GUI window, so nothing like it may go into
your Task 1A submission.
"""
import argparse
import os
import sys

import cv2
import numpy as np

DEFAULT_IMAGE = os.path.expanduser('~/pico_ws/src/swift_pico/scripts/image_1.jpg')
WINDOW = 'HSV tuner  (p = print range, q = quit)'
SLIDERS = [('H low', 0, 179), ('H high', 179, 179), ('S low', 0, 255), ('S high', 255, 255),
           ('V low', 0, 255), ('V high', 255, 255)]


def main():
    parser = argparse.ArgumentParser(description='Find an HSV range with live sliders.')
    parser.add_argument('--image', default=DEFAULT_IMAGE, help='path to the photo')
    args = parser.parse_args()

    image = cv2.imread(args.image)
    if image is None:
        sys.exit(f'Could not read image: {args.image}')
    # Show both views side by side at a size that fits a laptop screen.
    scale = min(1.0, 620 / max(image.shape[:2]))
    image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    cv2.namedWindow(WINDOW, cv2.WINDOW_AUTOSIZE)
    for name, start, top in SLIDERS:
        cv2.createTrackbar(name, WINDOW, start, top, lambda _value: None)

    def current_range():
        v = [cv2.getTrackbarPos(name, WINDOW) for name, _, _ in SLIDERS]
        return np.array([v[0], v[2], v[4]]), np.array([v[1], v[3], v[5]])

    was_visible = False
    while True:
        lower, upper = current_range()
        mask = cv2.inRange(hsv, lower, upper)
        kept = cv2.bitwise_and(image, image, mask=mask)
        view = np.hstack([kept, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)])
        text = f'lower {lower.tolist()}   upper {upper.tolist()}'
        cv2.putText(view, text, (10, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 4)
        cv2.putText(view, text, (10, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 1)
        cv2.imshow(WINDOW, view)

        key = cv2.waitKey(30) & 0xFF
        # Quit on q/Esc, or when the window's close button was used. The window only counts
        # as closed after it has been seen open, because it takes a moment to appear.
        visible = cv2.getWindowProperty(WINDOW, cv2.WND_PROP_VISIBLE) >= 1
        was_visible = was_visible or visible
        if key in (ord('q'), 27) or (was_visible and not visible):
            break
        if key == ord('p'):
            print(f'lower = {lower.tolist()}   upper = {upper.tolist()}')
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
