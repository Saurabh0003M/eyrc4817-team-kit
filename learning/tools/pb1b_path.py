#!/usr/bin/env python3
"""Draw the PacBot's estimated path from a PB 1B controller log (the `t=… x=… y=…` status lines
and the `turn` lines), coloured by time, so loops and dead ends are visible at a glance.

    python3 pb1b_path.py ~/pb1b_trials/<trial>/controller.log     -> path.png next to the log
"""
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

log = Path(sys.argv[1])
t, x, y, turns = [], [], [], []
for line in log.read_text().splitlines():
    status = re.match(r"t=\s*([\d.]+)s \w+\s.*x=([+-][\d.]+) y=([+-][\d.]+)", line)
    if status:
        t.append(float(status[1])); x.append(float(status[2])); y.append(float(status[3]))
    turn = re.search(r"t=\s*([\d.]+)s turn\s+([+-]\d+)", line)
    if turn:
        turns.append((float(turn[1]), turn[2]))
if not t:
    sys.exit("no status lines in the log")

fig, ax = plt.subplots(figsize=(7, 7))
dots = ax.scatter(x, y, c=t, cmap="viridis", s=6)
ax.plot(x[0], y[0], "go", ms=10, label="start")
ax.plot(x[-1], y[-1], "rx", ms=12, mew=3, label="end")
for when, angle in turns:
    i = min(range(len(t)), key=lambda k: abs(t[k] - when))
    ax.annotate(angle, (x[i], y[i]), fontsize=6, color="red")
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
ax.legend()
plt.colorbar(dots, label="sim time (s)")
ax.set_title(f"PB 1B path (odometry, m): {log.parent.name}")
out = log.parent / "path.png"
fig.savefig(out, dpi=110, bbox_inches="tight")
print(f"path plot: {out}")
