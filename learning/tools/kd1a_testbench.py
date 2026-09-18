#!/usr/bin/env python3
"""
KD Task 1A stress test.

The hidden test images will not look exactly like image_1.jpg. This makes harder versions of the
arena (tilted, rotated, darker, brighter, blurred, noisy, smaller) and runs YOUR script on each one.

It has no answer key, so it cannot spoil the task. It checks **consistency**: moving the camera or
changing the light does not move the survivors on the grid, so your results on every variant must
match your results on the original. A mismatch shows exactly which kind of change breaks your
pipeline.

    python3 kd1a_testbench.py --script ~/pico_ws/src/swift_pico/scripts/task1a.py
    python3 kd1a_testbench.py --script task1a.py --keep     # keep the variant images to look at
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

import cv2
import numpy as np

DEFAULT_IMAGE = os.path.expanduser('~/pico_ws/src/swift_pico/scripts/image_1.jpg')


def perspective(img, rng, strength):
    height, width = img.shape[:2]
    pad = int(0.25 * max(height, width))
    canvas = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=(40, 40, 40))
    src = np.float32([[pad, pad], [pad + width, pad], [pad + width, pad + height], [pad, pad + height]])
    jitter = rng.uniform(-strength, strength, size=(4, 2)).astype(np.float32) * max(height, width)
    matrix = cv2.getPerspectiveTransform(src, src + jitter)
    return cv2.warpPerspective(canvas, matrix, (canvas.shape[1], canvas.shape[0]), borderValue=(40, 40, 40))


def rotate(img, angle):
    height, width = img.shape[:2]
    diagonal = int(np.hypot(height, width))
    canvas = cv2.copyMakeBorder(img, (diagonal - height) // 2 + 10, (diagonal - height) // 2 + 10,
                                (diagonal - width) // 2 + 10, (diagonal - width) // 2 + 10,
                                cv2.BORDER_CONSTANT, value=(40, 40, 40))
    center = (canvas.shape[1] / 2, canvas.shape[0] / 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(canvas, matrix, (canvas.shape[1], canvas.shape[0]), borderValue=(40, 40, 40))


def variants(img, seed):
    rng = np.random.default_rng(seed)
    noise = rng.normal(0, 12, img.shape)
    return {
        'tilt_mild': perspective(img, rng, 0.06),
        'tilt_strong': perspective(img, rng, 0.12),
        'rotate_+8deg': rotate(img, 8),
        'rotate_-15deg': rotate(img, -15),
        'darker': cv2.convertScaleAbs(img, alpha=0.65, beta=-10),
        'brighter': cv2.convertScaleAbs(img, alpha=1.2, beta=25),
        'blur': cv2.GaussianBlur(img, (7, 7), 0),
        'noise': np.clip(img.astype(np.float64) + noise, 0, 255).astype(np.uint8),
        'smaller_640px': cv2.resize(img, None, fx=0.8, fy=0.8, interpolation=cv2.INTER_AREA),
        'jpeg_quality_40': cv2.imdecode(cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 40])[1], cv2.IMREAD_COLOR),
    }


def run_script(script, image_path):
    try:
        proc = subprocess.run([sys.executable, script, '--image', image_path], capture_output=True, text=True,
                              timeout=60, cwd=os.path.dirname(image_path))
    except subprocess.TimeoutExpired:
        return None, 'timed out (waiting on a window or keypress?)'
    results_path = os.path.splitext(image_path)[0] + '_results.txt'
    if not os.path.isfile(results_path):
        return None, f'no results file (exit code {proc.returncode}): {proc.stderr.strip()[-200:]}'
    parsed = {}
    for line in open(results_path, encoding='utf-8').read().splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            parsed[key.strip()] = frozenset(v.strip() for v in value.replace('[', '').replace(']', '').split(',') if v.strip())
    return parsed, ''


def main():
    parser = argparse.ArgumentParser(description='Consistency stress test for a KD Task 1A script.')
    parser.add_argument('--script', required=True, help='your task1a script')
    parser.add_argument('--image', default=DEFAULT_IMAGE)
    parser.add_argument('--seed', type=int, default=4817, help='change it to get different random tilts')
    parser.add_argument('--keep', action='store_true', help='keep the generated images and results')
    args = parser.parse_args()

    script = os.path.abspath(os.path.expanduser(args.script))
    img = cv2.imread(os.path.expanduser(args.image))
    if img is None:
        sys.exit(f'Could not read {args.image}')
    work = tempfile.mkdtemp(prefix='kd1a_testbench_')
    original_path = os.path.join(work, 'original.jpg')
    cv2.imwrite(original_path, img)
    reference, error = run_script(script, original_path)
    if reference is None:
        sys.exit(f'Your script failed on the ORIGINAL image: {error}')
    print('Reference (your result on the original):')
    for key, value in reference.items():
        print(f'  {key}: {", ".join(sorted(value)) or "(none)"}')

    passed = 0
    all_variants = variants(img, args.seed)
    print()
    for name, variant in all_variants.items():
        path = os.path.join(work, f'{name}.jpg')
        cv2.imwrite(path, variant)
        result, error = run_script(script, path)
        if result is None:
            print(f'  [!!] {name:<16} {error}')
        elif result == reference:
            passed += 1
            print(f'  [ok] {name:<16} same as original')
        else:
            diffs = [f'{k}: got {", ".join(sorted(result.get(k, []))) or "(none)"}' for k in reference if result.get(k) != reference[k]]
            print(f'  [!!] {name:<16} ' + ' | '.join(diffs))
    print(f'\n{passed}/{len(all_variants)} variants consistent with the original.')
    if args.keep:
        print(f'Images and results kept in {work}')
    else:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    main()
