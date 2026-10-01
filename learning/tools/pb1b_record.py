#!/usr/bin/env python3
"""PB 1B recorded evaluate run, laid out so the video meets the portal rule: BOTH terminals readable and
the WHOLE maze in shot for the whole video.

One window with two real terminals (GNOME Terminal's VTE widget), one above the other:
  top    = ./task_1b_launch --evaluate   (typed in automatically; proves evaluation mode)
  bottom = python3 task_1b.py            (starts when you press Enter in it)
It also starts/stops GNOME's screen recorder, and makes PB#4817.zip on camera at the end.

What you do (4 things):
  1. Click the TOP pane and press Enter: the screen recording starts, then the launcher.
  2. When the "Micromouse sim" window opens: click it, press Super+Right (right half of the screen).
  3. Click this window's title bar, press Super+Left (left half).
  4. Click the BOTTOM pane, press Enter: the robot starts. Then don't touch anything until DONE (~4-5 min).
While it records, the screen is kept from blanking/locking (GNOME stops recording on lock). If the screen
locks anyway, the run is marked INTERRUPTED and nothing is zipped. At the end it also writes a sim-only copy
of the video (right half, the part showing the maze) next to the full one.

usage: python3 pb1b_record.py [--dry-run] [--auto]
  --dry-run  fake launcher + controller in a temp folder, no recording (to test this tool)
  --auto     start the robot by itself 3 s after the launcher is ready (no Enter needed)
"""
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Vte", "2.91")
from gi.repository import Gio, GLib, Gtk, Pango, Vte

DRY = "--dry-run" in sys.argv
AUTO = "--auto" in sys.argv
DEBUG = "--debug" in sys.argv
TASK = Path(tempfile.mkdtemp(prefix="pb1b-dry-")) if DRY else Path.home() / "pacbot_ws" / "task1b"
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
VIDEO = Path.home() / "Videos" / "Screencasts" / f"PB_4817_Task1B_{STAMP}.webm"
TRIALS = Path.home() / "pb1b_trials"
SOLVE_TIMEOUT_S = 8 * 60          # give up if the maze is not solved this long after the robot starts
START_TIMEOUT_S = 10 * 60         # give up if nobody presses Enter (robot never starts) this long
CLOSE_AFTER_DONE_S = 15           # the window closes itself this long after DONE (real runs only)
ZIP = "PB#4817.zip"

if DRY:   # fake programs that print what the real ones print, fast
    (TASK / "task_1b.py").write_text("import time\nfor i in range(400):\n    print(f't={i*0.25:6.2f}s FOLLOW (dry run)', flush=True)\n    time.sleep(0.05)\n")
    (TASK / "task_1b_launch").write_text("#!/bin/bash\necho -e '\\e[1;36mevaluate:\\e[0m recording data; result will be written to result.json'\n"
                                         "sleep 6; echo -e '\\e[1;32mMAZE SOLVED\\e[0m'; echo '{\"dry\": true}' > result.json\n"
                                         "echo -e '\\e[1;32mevaluate:\\e[0m wrote sealed result to result.json'; sleep 600\n")
    (TASK / "task_1b_launch").chmod(0o755)


class Recorder:
    """GNOME Shell's screen recorder over D-Bus (same as screen_record.py)."""
    def __init__(self):
        bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        self.proxy = Gio.DBusProxy.new_sync(bus, Gio.DBusProxyFlags.NONE, None, "org.gnome.Shell.Screencast",
                                            "/org/gnome/Shell/Screencast", "org.gnome.Shell.Screencast", None)
        self.running = False

    def start(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        ok, used = self.proxy.call_sync("Screencast", GLib.Variant("(sa{sv})", (str(path), {})),
                                        Gio.DBusCallFlags.NONE, -1, None).unpack()
        self.running = bool(ok)
        return used if ok else None

    def stop(self):
        if self.running:
            self.proxy.call_sync("StopScreencast", None, Gio.DBusCallFlags.NONE, -1, None)
            self.running = False


class Session:
    """Keep the screen from blanking/locking while recording, and tell if it locked anyway."""
    def __init__(self):
        self.bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        self.cookie = None

    def keep_awake(self):
        reply = self.bus.call_sync("org.gnome.SessionManager", "/org/gnome/SessionManager", "org.gnome.SessionManager",
                                   "Inhibit", GLib.Variant("(susu)", ("pb1b_record", 0, "recording the PB 1B run", 4 | 8)),
                                   GLib.VariantType("(u)"), Gio.DBusCallFlags.NONE, 5000, None)
        self.cookie = reply.unpack()[0]          # 4 = suspend, 8 = idle (screen blank + lock)

    def release(self):
        if self.cookie is not None:
            self.bus.call_sync("org.gnome.SessionManager", "/org/gnome/SessionManager", "org.gnome.SessionManager",
                               "Uninhibit", GLib.Variant("(u)", (self.cookie,)), None, Gio.DBusCallFlags.NONE, 5000, None)
            self.cookie = None

    def locked(self):
        try:
            reply = self.bus.call_sync("org.gnome.ScreenSaver", "/org/gnome/ScreenSaver", "org.gnome.ScreenSaver",
                                       "GetActive", None, GLib.VariantType("(b)"), Gio.DBusCallFlags.NONE, 2000, None)
            return reply.unpack()[0]
        except GLib.Error:
            return False


class RunWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="PB 1B evaluate run · team 4817")
        self.set_default_size(950, 1000)
        self.top, self.bottom = self.terminal(), self.terminal()
        panes = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
        panes.pack1(self.top, True, False)
        panes.pack2(self.bottom, True, False)
        panes.set_position(330)               # the launcher prints only a few lines
        self.add(panes)
        self.connect("destroy", self.on_close)
        self.recorder = None if DRY else Recorder()
        self.session = Session()
        self.stage, self.robot_started_at, self.stage_since = "start", None, time.time()
        GLib.timeout_add(500, self.tick)

    def terminal(self):
        term = Vte.Terminal()
        term.set_font(Pango.FontDescription("Monospace 10"))
        term.set_scrollback_lines(10000)
        env = [f"PS1=ubantu@ubantu:{'~/pacbot_ws/task1b' if not DRY else str(TASK)}$ ", f"HOME={Path.home()}",
               "TERM=xterm-256color", f"PATH={GLib.getenv('PATH')}"]
        for key in ("DISPLAY", "WAYLAND_DISPLAY", "XAUTHORITY", "DBUS_SESSION_BUS_ADDRESS", "XDG_RUNTIME_DIR"):
            if GLib.getenv(key):
                env.append(f"{key}={GLib.getenv(key)}")
        term.spawn_async(Vte.PtyFlags.DEFAULT, str(TASK), ["/bin/bash", "--norc", "--noprofile", "-i"], env,
                         GLib.SpawnFlags.DEFAULT, None, None, -1, None, None, None)
        return term

    @staticmethod
    def type_into(term, text):
        term.feed_child(text.encode())

    @staticmethod
    def screen_text(term):
        text = term.get_text(None, None)
        return text[0] if isinstance(text, tuple) else (text or "")

    def set_stage(self, stage, title=None):
        if DEBUG:
            print(f"[{time.strftime('%H:%M:%S')}] stage {self.stage} -> {stage}", flush=True)
        self.stage, self.stage_since = stage, time.time()
        if title:
            self.set_title(title)

    def tick(self):
        try:
            return self.step()
        except Exception:                      # a failure inside a GLib timer would otherwise vanish
            import traceback
            traceback.print_exc()
            self.set_stage("failed", "FAILED: see the terminal that started this tool")
            return False

    def step(self):
        now = time.time()
        top_text = self.screen_text(self.top)
        recording = self.stage in ("recording", "launching", "waiting_robot", "running", "solved", "stopping_ok", "zipping")
        if recording and not DRY and self.session.locked():
            self.type_into(self.bottom, "\x03")
            self.type_into(self.top, "\x03")
            self.set_stage("stopping_fail", "INTERRUPTED: the screen locked, so the recording stopped · run again (no zip)")
            return True
        if self.stage == "start" and now - self.stage_since > 1.5:          # shells are up
            prompt = "Press Enter here to START the screen recording and the launcher..."
            self.type_into(self.top, "clear; read -p '" + prompt + " ' _ ; clear\n" if not AUTO else "clear\n")
            self.set_stage("await_start", "Click the TOP pane and press Enter to start")
        elif self.stage == "await_start" and now - self.stage_since > 1.0 and "Press Enter here to START" not in top_text:
            if not DRY:
                self.session.keep_awake()
            if self.recorder and not self.recorder.start(VIDEO):
                self.set_stage("failed", "FAILED: GNOME did not start the screen recording")
                return True
            self.set_stage("recording", "Recording…")
        elif self.stage == "recording" and now - self.stage_since > 2.0:    # a moment of quiet terminals on video
            self.type_into(self.top, "./task_1b_launch --evaluate\n")
            self.set_stage("launching", "Arrange windows: sim → Super+Right · this window → Super+Left · Enter in the bottom pane")
        elif self.stage == "launching" and "recording data" in top_text:
            command = "python3 task_1b.py\n" if AUTO else "read -p 'Windows arranged? Press Enter to start the robot... ' _ && python3 task_1b.py\n"
            self.type_into(self.bottom, command)
            self.set_stage("waiting_robot")
        elif self.stage == "waiting_robot" and "t=" in self.screen_text(self.bottom):
            self.robot_started_at = now
            self.set_stage("running", "Robot running · don't touch anything until DONE")
        elif self.stage == "waiting_robot" and now - self.stage_since > START_TIMEOUT_S:
            self.set_stage("timeout", f"Robot not started within {START_TIMEOUT_S // 60} min · stopping (no zip)")
        elif self.stage == "running":
            if "wrote sealed result" in top_text:
                self.set_stage("solved", "MAZE SOLVED · stopping, zipping…")
            elif now - self.robot_started_at > SOLVE_TIMEOUT_S:
                self.set_stage("timeout", f"NOT SOLVED within {SOLVE_TIMEOUT_S // 60} min · stopping (no zip)")
        elif self.stage == "solved" and now - self.stage_since > 3:
            self.type_into(self.bottom, "\x03")                              # Ctrl+C: controller
            self.type_into(self.top, "\x03")                                 # Ctrl+C: launcher
            self.set_stage("stopping_ok")
        elif self.stage == "timeout":
            self.type_into(self.bottom, "\x03")
            self.type_into(self.top, "\x03")
            self.set_stage("stopping_fail")
        elif self.stage == "stopping_ok" and now - self.stage_since > 3:
            self.ensure_launcher_stopped()
            self.type_into(self.top, f"zip '{ZIP}' result.json task_1b.py && unzip -l '{ZIP}'\n")
            self.set_stage("zipping")
        elif self.stage == "stopping_fail" and now - self.stage_since > 3:
            self.ensure_launcher_stopped()
            self.finish(zip_made=False)
        elif self.stage == "zipping" and now - self.stage_since > 3:
            self.finish(zip_made=(TASK / ZIP).exists())
        return self.stage not in ("done", "failed")

    def ensure_launcher_stopped(self):
        if DRY:
            subprocess.run(["pkill", "-INT", "-f", f"{TASK}/task_1b_launch"], check=False)
            return
        if subprocess.run(["pgrep", "-x", "task_1b_launch"], capture_output=True).returncode == 0:
            subprocess.run(["pkill", "-TERM", "-x", "task_1b_launch"], check=False)   # it ignored Ctrl+C

    def finish(self, zip_made):
        if self.recorder:
            self.recorder.stop()
        self.session.release()
        if not DRY and VIDEO.exists():          # sim-only copy: the right half, below the top bar
            GLib.timeout_add_seconds(2, self.crop_copy)
        video = "dry run, no video" if DRY else str(VIDEO)
        summary = f"DONE · zip {'made' if zip_made else 'NOT made'} · video: {video}"
        self.set_stage("done", summary)
        if not DRY:
            GLib.timeout_add_seconds(CLOSE_AFTER_DONE_S, self.close)
        TRIALS.mkdir(exist_ok=True)
        (TRIALS / f"recorded_{STAMP}{'_dry' if DRY else ''}.txt").write_text(
            f"{summary}\nfolder: {TASK}\nzip: {TASK / ZIP if zip_made else '-'}\n\n--- launcher pane ---\n"
            f"{self.screen_text(self.top)}\n")
        print(summary, flush=True)

    @staticmethod
    def crop_copy():
        out = VIDEO.with_name(VIDEO.stem + "_sim_only.webm")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(VIDEO), "-vf", "crop=iw/2:ih-32:iw/2:32",
                        "-c:v", "libvpx-vp9", "-b:v", "3M", "-row-mt", "1", "-deadline", "realtime", str(out)], check=False)
        print(f"sim-only copy: {out}", flush=True)
        return False

    def on_close(self, *_):
        if self.recorder:
            self.recorder.stop()
        self.session.release()
        Gtk.main_quit()


def main():
    # get_text() on VTE 0.68 prints a deprecation warning on every call; it is harmless here
    GLib.log_set_handler("VTE", GLib.LogLevelFlags.LEVEL_WARNING, lambda *args: None, None)
    if not DRY:
        old = TASK / "result.json"
        if old.exists():      # keep the previous run's sealed result, but make sure the zip gets the new one
            TRIALS.mkdir(exist_ok=True)
            keep = TRIALS / f"previous_result_{datetime.fromtimestamp(old.stat().st_mtime):%Y%m%d_%H%M%S}.json"
            shutil.move(str(old), keep)
            print(f"moved the old result.json to {keep}", flush=True)
        if (TASK / ZIP).exists():
            (TASK / ZIP).rename(TASK / f"PB#4817_previous_{STAMP}.zip")
    window = RunWindow()
    window.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
