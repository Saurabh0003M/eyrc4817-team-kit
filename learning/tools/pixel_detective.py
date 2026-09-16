#!/usr/bin/env python3
"""
Pixel detective — roadmap experiment M1-b.

Click anywhere on the photo to see that pixel's numbers:
  - its position (x = column from the left, y = row from the top)
  - its colour as OpenCV stores it: B, G, R  (Blue, Green, Red — in that order!)
  - the same colour as H, S, V  (Hue 0-179, Saturation 0-255, Value 0-255)

Before each click, PREDICT the numbers, then check.

    python3 pixel_detective.py                      # opens image_1.jpg
    python3 pixel_detective.py --image other.jpg

Keys: r = clear marks, q or Esc = quit.
This is a LEARNING TOOL. It uses a GUI window, so nothing like it may go into
your Task 1A submission.
"""
import argparse
import os
import sys

import cv2

DEFAULT_IMAGE = os.path.expanduser('~/pico_ws/src/swift_pico/scripts/image_1.jpg')
WINDOW = 'Pixel detective  (click = read pixel, r = clear, q = quit)'


def main():
    parser = argparse.ArgumentParser(description='Click pixels to read their BGR and HSV values.')
    parser.add_argument('--image', default=DEFAULT_IMAGE, help='path to the photo')
    args = parser.parse_args()

    image = cv2.imread(args.image)
    if image is None:
        sys.exit(f'Could not read image: {args.image}')
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    shown = image.copy()
    print(f'Opened {args.image}  —  {image.shape[1]} px wide, {image.shape[0]} px tall')
    print(f'{"x":>4} {"y":>4} |  {"B":>3} {"G":>3} {"R":>3}  |  {"H":>3} {"S":>3} {"V":>3}')

    def on_mouse(event, x, y, flags, param):
        if event != cv2.EVENT_LBUTTONDOWN:
            return
        b, g, r = (int(v) for v in image[y, x])
        h, s, v = (int(v) for v in hsv[y, x])
        print(f'{x:>4} {y:>4} |  {b:>3} {g:>3} {r:>3}  |  {h:>3} {s:>3} {v:>3}')
        cv2.drawMarker(shown, (x, y), (255, 0, 255), cv2.MARKER_CROSS, 14, 2)
        label = f'BGR {b},{g},{r}  HSV {h},{s},{v}'
        tx = min(x + 10, image.shape[1] - 230)
        ty = max(y - 10, 15)
        cv2.putText(shown, label, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 3)
        cv2.putText(shown, label, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

    cv2.namedWindow(WINDOW, cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback(WINDOW, on_mouse)
    was_visible = False
    while True:
        cv2.imshow(WINDOW, shown)
        key = cv2.waitKey(30) & 0xFF
        # Quit on q/Esc, or when the window's close button was used. The window only counts
        # as closed after it has been seen open, because it takes a moment to appear.
        visible = cv2.getWindowProperty(WINDOW, cv2.WND_PROP_VISIBLE) >= 1
        was_visible = was_visible or visible
        if key in (ord('q'), 27) or (was_visible and not visible):
            break
        if key == ord('r'):
            shown = image.copy()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
