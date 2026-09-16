#!/usr/bin/env python3
"""
Submission checker — roadmap M1-i/M1-k, M6-g, M7-d, P2-g, P3-e.

It never looks at *whether your answer is right*. It checks what gets submissions rejected:
file names, e-Yantra's coding-standard comment blocks, forbidden GUI/input calls, the KD 1A
results-file format, unchanged PacBot boilerplate functions, and zip structure.

    python3 submission_check.py kd1a  --file KD_4817_task1a.py [--image image_1.jpg] [--zip KD_4817.zip]
    python3 submission_check.py pb1a  --file task_1a.py [--zip 'PB#4817.zip']
    python3 submission_check.py pb1b  --file task_1b.py [--zip 'PB#4817.zip']
    python3 submission_check.py kd1b  --zip KD_4817_task_1b.zip
    python3 submission_check.py kd1c  --zip KD_4817_task_1c.zip
"""
import argparse
import ast
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

TEAM_ID = '4817'
PB_BOILERPLATE = {'pb1a': '~/pacbot_ws/task1a/task_1a_boilerplate.py',
                  'pb1b': '~/pacbot_ws/task1b/task_1b_boilerplate.py'}
EXPECTED_ZIP = {'kd1a': (f'KD_{TEAM_ID}.zip', {f'KD_{TEAM_ID}_task1a.py'}),
                'kd1b': (f'KD_{TEAM_ID}_task_1b.zip', {'task_1b_0.db3', 'metadata.yaml'}),
                'kd1c': (f'KD_{TEAM_ID}_task_1c.zip', {'task_1c_0.db3', 'metadata.yaml'}),
                'pb1a': (f'PB#{TEAM_ID}.zip', {'result.yaml', 'task_1a.py'}),
                'pb1b': (f'PB#{TEAM_ID}.zip', {'result.json', 'task_1b.py'})}
HEADER_FIELDS = ['Team ID:', 'Theme:', 'Author List:', 'Filename:', 'Functions:', 'Global variables:']
DOC_FIELDS = ['Purpose:', 'Input Arguments:', 'Returns:', 'Example call:']
FORBIDDEN_CALLS = [r'cv2\.imshow', r'cv2\.waitKey', r'cv2\.namedWindow', r'\binput\s*\(', r'plt\.show']
LABEL = r'[A-K](?:1[01]|[1-9])'

results = []


def report(ok, message):
    results.append(ok)
    print(('  [ok] ' if ok else '  [!!] ') + message)


def check_coding_standard(path, source, tree):
    print('\n== e-Yantra coding standard')
    head = source[:1500]
    missing = [f for f in HEADER_FIELDS if f not in head]
    report(not missing, 'file header block' + (f' is missing: {", ".join(missing)}' if missing else ''))
    if f'Team ID:' in head:
        report(TEAM_ID in head.split('Team ID:')[1].splitlines()[0], f'header Team ID is {TEAM_ID}')
    functions = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    bad_docs = [f.name for f in functions if not all(k in (ast.get_docstring(f) or '') for k in DOC_FIELDS)]
    report(not bad_docs, f'{len(functions)} function(s) have Purpose / Input Arguments / Returns / Example call'
           + (f'; missing or incomplete in: {", ".join(bad_docs)}' if bad_docs else ''))
    short = set()
    for node in ast.walk(tree):
        names = []
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            names.append(node.id)
        elif isinstance(node, ast.arg):
            names.append(node.arg)
        short.update(n for n in names if (len(n) == 1 and n not in 'ijk_') or n.lower() in ('temp', 'tmp'))
    report(not short, 'descriptive variable names' + (f'; rename: {", ".join(sorted(short))}' if short else ''))


def check_forbidden(source):
    print('\n== blocking / GUI calls (a script that waits is marked failed)')
    code_lines = [l for l in source.splitlines() if not l.strip().startswith('#')]
    labels = ['cv2.imshow', 'cv2.waitKey', 'cv2.namedWindow', 'input()', 'plt.show']
    hits = [label for pattern, label in zip(FORBIDDEN_CALLS, labels) if any(re.search(pattern, l) for l in code_lines)]
    report(not hits, 'no imshow / waitKey / namedWindow / input() / plt.show' + (f'; found: {", ".join(hits)}' if hits else ''))


def check_kd1a_run(path, image):
    print('\n== KD 1A: run on a copy of the image, then check the results file format')
    work = tempfile.mkdtemp(prefix='kd1a_check_')
    image_copy = os.path.join(work, os.path.basename(image))
    shutil.copy(image, image_copy)
    try:
        proc = subprocess.run([sys.executable, path, '--image', image_copy], cwd=work, capture_output=True,
                              text=True, timeout=60)
    except subprocess.TimeoutExpired:
        report(False, 'script finished within 60 s (it may be waiting on a window or keypress)')
        return
    report(proc.returncode == 0, f'script exited normally (code {proc.returncode})')
    results_path = os.path.splitext(image_copy)[0] + '_results.txt'
    if not os.path.isfile(results_path):
        report(False, f'wrote {os.path.basename(results_path)} next to the image')
        return
    report(True, f'wrote {os.path.basename(results_path)} next to the image')
    lines = open(results_path, encoding='utf-8').read().split('\n')
    while lines and lines[-1] == '':
        lines.pop()
    content = [l for l in lines if l != '']
    report(len(lines) in (3, 4), f'{len(lines)} lines ({"blank line 2, per the instruction page" if len(lines) == 4 else "no blank line, per the submission page"}; the portal pages disagree)')
    patterns = [r'^Detected marker IDs: \[(\d+(, \d+)*)?\]$',
                rf'^Critical Survivors: ({LABEL}(, {LABEL})*)?$',
                rf'^Stable Survivors: ({LABEL}(, {LABEL})*)?$']
    for pattern, line, name in zip(patterns, content + [''] * 3, ['marker IDs', 'Critical', 'Stable']):
        report(bool(re.match(pattern, line)), f'{name} line format: {line!r}')
    shutil.rmtree(work, ignore_errors=True)


def signatures(tree):
    found = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            found[node.name] = [a.arg for a in node.args.args]
    return found


def check_boilerplate(task, tree):
    print('\n== PacBot: boilerplate functions unchanged (the evaluator looks for them)')
    path = os.path.expanduser(PB_BOILERPLATE[task])
    if not os.path.isfile(path):
        report(False, f'boilerplate found at {path}')
        return
    original = signatures(ast.parse(open(path, encoding='utf-8').read()))
    mine = signatures(tree)
    for name, args in original.items():
        if name not in mine:
            report(False, f'function {name}() still exists')
        else:
            report(mine[name] == args, f'{name}({", ".join(args)}) has the same arguments')


def check_zip(task, zip_path):
    print('\n== zip structure')
    expected_name, expected_files = EXPECTED_ZIP[task]
    report(os.path.basename(zip_path) == expected_name, f'zip named {expected_name}')
    with zipfile.ZipFile(zip_path) as archive:
        names = set(n for n in archive.namelist() if not n.endswith('/'))
    report(names == expected_files, f'contains exactly {sorted(expected_files)} at the top level (found {sorted(names)})')


def main():
    parser = argparse.ArgumentParser(description='Check a submission before handing it to the Team Leader.')
    parser.add_argument('task', choices=['kd1a', 'kd1b', 'kd1c', 'pb1a', 'pb1b'])
    parser.add_argument('--file', help='your submission .py file')
    parser.add_argument('--image', default=os.path.expanduser('~/pico_ws/src/swift_pico/scripts/image_1.jpg'))
    parser.add_argument('--zip', help='the zip you are about to upload')
    args = parser.parse_args()

    if args.file:
        path = os.path.abspath(args.file)
        source = open(path, encoding='utf-8').read()
        tree = ast.parse(source)
        print(f'Checking {path}')
        if args.task == 'kd1a':
            report(os.path.basename(path) == f'KD_{TEAM_ID}_task1a.py', f'file named KD_{TEAM_ID}_task1a.py')
            report("'--image'" in source or '"--image"' in source, 'uses an --image command-line argument')
        check_coding_standard(path, source, tree)
        check_forbidden(source)
        if args.task in PB_BOILERPLATE:
            check_boilerplate(args.task, tree)
        if args.task == 'kd1a':
            check_kd1a_run(path, args.image)
    if args.zip:
        check_zip(args.task, args.zip)
    if not args.file and not args.zip:
        parser.error('give --file and/or --zip')
    failed = results.count(False)
    print(f'\n{len(results) - failed}/{len(results)} checks passed' + ('' if not failed else ' — fix the [!!] lines'))
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
