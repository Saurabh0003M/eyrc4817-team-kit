#!/usr/bin/env python3
"""
screen_record.py - record the whole screen for task videos (Ubuntu 22.04, GNOME, Wayland).

Why this exists: GNOME's own recorder stops only when the SAME program that started it asks,
and on some themes the red stop indicator in the top bar is hidden. This program starts
GNOME's recorder, keeps running, and stops it cleanly when you press Ctrl+C here
(safety stop after 20 minutes).

Usage:
    python3 screen_record.py                   # -> ~/Videos/Screencasts/eyrc_<date>_<time>.webm
    python3 screen_record.py PB_4817_Task1A    # -> ~/Videos/Screencasts/PB_4817_Task1A_<date>_<time>.webm
Stop: Ctrl+C in the same terminal. Upload the .webm to YouTube as Unlisted.
"""
import signal
import sys
import time
from pathlib import Path

from gi.repository import Gio, GLib

MAX_SECONDS = 20 * 60


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else 'eyrc'
    folder = Path.home() / 'Videos' / 'Screencasts'
    folder.mkdir(parents=True, exist_ok=True)
    video_path = folder / f"{name}_{time.strftime('%Y%m%d_%H%M%S')}.webm"

    bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
    recorder = Gio.DBusProxy.new_sync(bus, Gio.DBusProxyFlags.NONE, None, 'org.gnome.Shell.Screencast',
                                      '/org/gnome/Shell/Screencast', 'org.gnome.Shell.Screencast', None)
    started, _ = recorder.call_sync('Screencast', GLib.Variant('(sa{sv})', (str(video_path), {})),
                                    Gio.DBusCallFlags.NONE, -1, None).unpack()
    if not started:
        sys.exit('Could not start GNOME screen recording (is this a normal GNOME desktop session?)')
    print(f'RECORDING the whole screen -> {video_path}')
    print('Press Ctrl+C here to stop.', flush=True)
    start_time = time.time()
    loop = GLib.MainLoop()

    def stop():
        recorder.call_sync('StopScreencast', None, Gio.DBusCallFlags.NONE, -1, None)
        print(f'\nStopped after {time.time() - start_time:.0f} s. Video saved: {video_path}', flush=True)
        loop.quit()
        return GLib.SOURCE_REMOVE

    GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, stop)
    GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGTERM, stop)
    GLib.timeout_add_seconds(MAX_SECONDS, stop)
    loop.run()


if __name__ == '__main__':
    main()
