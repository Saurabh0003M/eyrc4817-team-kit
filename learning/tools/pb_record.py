#!/usr/bin/env python3
"""PacBot recorded evaluate run (Task 1B, 2A or 2B), laid out so the video meets the portal rule: BOTH
terminals readable and the WHOLE maze in shot for the whole video. Generalised from pb1b_record.py.

One window with two real terminals (GNOME Terminal's VTE widget), one above the other:
  top    = ./task_<x>_launch --evaluate   (typed in automatically; proves evaluation mode)
  bottom = python3 <solver>.py            (starts when you press Enter in it; 2B starts it by itself)
It also starts/stops GNOME's screen recorder, and makes PB#4817.zip on camera at the end.

What you do:
  1. Click the TOP pane and press Enter: the screen recording starts, then the launcher.
  2. When the simulator window opens: click it, press Super+Right (right half of the screen).
  3. Click this window's title bar, press Super+Left (left half).
  4. 1B / 2A: click the BOTTOM pane, press Enter: the robot starts.
     2B: nothing; the solver starts by itself (the 2B evaluator ends the run if the robot has not moved
     within 60 s). The robot then stands still for 12-18 s, watching the ghost: that is normal.
  Then don't touch anything until DONE (a few minutes).
While it records, the screen is kept from blanking/locking (GNOME stops recording on lock). If the screen
locks anyway, the run is marked INTERRUPTED and nothing is zipped. At the end it also writes a sim-only copy
of the video (right half, the part showing the maze) next to the full one.

usage: python3 pb_record.py --task 1b|2a|2b [--dry-run] [--auto]
  --dry-run  fake launcher + controller in a temp folder, no recording (to test this tool)
  --auto     start the robot by itself 3 s after the launcher is ready (no Enter needed)
  --no-video rehearsal with the REAL launcher but no screen recording; its result.json and zip are moved to
             ~/pb<task>_trials/rehearsal_<time>/ afterwards, so no submit-ready zip is left in the task folder
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

# Per task: folder, launcher, solver; text that shows the launcher is ready; text in the solver pane that shows
# the robot program is running; text that shows the run is over (launcher pane, or solver pane); whether the
# solver starts by itself; MQTT topics the simulator retains (cleared first, a stale one confuses a new run).
TASKS = {
    "1b": dict(folder="task1b", launcher="task_1b_launch", solver="task_1b.py", ready="recording data",
               running="t=", over_launcher="wrote sealed result", over_solver=None, auto=False, retained=()),
    "2a": dict(folder="task2a", launcher="task_2a_launch", solver="task_2a_boilerplate.py",
               ready="PacBot Task2A started", running="connected", over_launcher=None, over_solver="result:",
               auto=False, retained=("pacbot/poses", "pacbot/pellets", "pacbot/result")),
    "2b": dict(folder="task2b", launcher="task_2b_launch", solver="task_2b_boilerplate.py",
               ready="waiting for your controller", running="connected", over_launcher=None,
               over_solver="run over:", auto=True,
               retained=("pacbot/poses", "pacbot/pellets", "pacbot/pellet", "pacbot/ghost", "pacbot/result")),
}
if "--task" not in sys.argv or sys.argv[sys.argv.index("--task") + 1:][:1] == [] or \
        sys.argv[sys.argv.index("--task") + 1] not in TASKS:
    sys.exit("usage: python3 pb_record.py --task 1b|2a|2b [--dry-run] [--auto]")
NAME = sys.argv[sys.argv.index("--task") + 1]
T = TASKS[NAME]
DRY = "--dry-run" in sys.argv
AUTO = "--auto" in sys.argv or T["auto"]
DEBUG = "--debug" in sys.argv
NO_VIDEO = "--no-video" in sys.argv
TASK = Path(tempfile.mkdtemp(prefix=f"pb{NAME}-dry-")) if DRY else Path.home() / "pacbot_ws" / T["folder"]
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
VIDEO = Path.home() / "Videos" / "Screencasts" / f"PB_4817_Task{NAME.upper()}_{STAMP}.webm"
TRIALS = Path.home() / f"pb{NAME}_trials"
SOLVE_TIMEOUT_S = 8 * 60          # give up if the maze is not solved this long after the robot starts
START_TIMEOUT_S = 10 * 60         # give up if nobody presses Enter (robot never starts) this long
READY_FALLBACK_S = 15             # launcher's ready text not seen: carry on after this long anyway
RESULT_WAIT_S = 20                # run over but no new result.json yet: wait this long before giving up
CLOSE_AFTER_DONE_S = 15           # the window closes itself this long after DONE (real runs only)
ZIP = "PB#4817.zip"

if DRY:   # fake programs that print what the real ones print, fast
    over = T["over_solver"] or ""
    (TASK / T["solver"]).write_text(
        "import time\nprint('connected (dry run)', flush=True)\nfor i in range(60):\n"
        "    print(f't={i*0.25:6.2f}s FOLLOW (dry run)', flush=True)\n    time.sleep(0.05)\n"
        f"print('{over} solved=True (dry run)', flush=True)\ntime.sleep(600)\n")
    (TASK / T["launcher"]).write_text(
        f"#!/bin/bash\necho '{T['ready']} (dry run)'\n"
        "sleep 6; echo -e '\\e[1;32mRUN COMPLETE\\e[0m'; echo '{\"dry\": true}' > result.json\n"
        "echo 'wrote sealed result to result.json (dry run)'; sleep 600\n")
    (TASK / T["launcher"]).chmod(0o755)


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
                                   "Inhibit", GLib.Variant("(susu)", ("pb_record", 0, f"recording the PB {NAME} run", 4 | 8)),
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
        super().__init__(title=f"PB {NAME.upper()} evaluate run · team 4817")
        self.set_default_size(950, 1000)
        self.top, self.bottom = self.terminal(), self.terminal()
        panes = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
        panes.pack1(self.top, True, False)
        panes.pack2(self.bottom, True, False)
        panes.set_position(330)               # the launcher prints only a few lines
        self.add(panes)
        self.connect("destroy", self.on_close)
        self.recorder = None if DRY or NO_VIDEO else Recorder()
        self.session = Session()
        self.stage, self.robot_started_at, self.stage_since = "start", None, time.time()
        self.launched_at = None             # wall time the launcher was started (result.json must be newer)
        self.over_since = None              # wall time the run-over text was first seen
        GLib.timeout_add(500, self.tick)

    def terminal(self):
        term = Vte.Terminal()
        term.set_font(Pango.FontDescription("Monospace 10"))
        term.set_scrollback_lines(10000)
        env = [f"PS1=ubantu@ubantu:{'~/pacbot_ws/' + T['folder'] if not DRY else str(TASK)}$ ", f"HOME={Path.home()}",
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
    def full_text(term):
        """Everything the pane printed, scrollback included (screen_text only sees the visible rows)."""
        try:
            adjustment = term.get_vadjustment()
            text = term.get_text_range(int(adjustment.get_lower()), 0, int(adjustment.get_upper()),
                                       term.get_column_count(), None, None)
            text = text[0] if isinstance(text, tuple) else text
            if text:
                return text
        except (AttributeError, TypeError):
            pass
        return RunWindow.screen_text(term)

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
        recording = not NO_VIDEO and self.stage in ("recording", "launching", "waiting_robot", "running", "solved", "stopping_ok", "zipping")
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
            self.launched_at = time.time()
            self.type_into(self.top, f"./{T['launcher']} --evaluate\n")
            hint = "" if AUTO else " · Enter in the bottom pane"
            self.set_stage("launching", f"Arrange windows: sim → Super+Right · this window → Super+Left{hint}")
        elif self.stage == "launching" and (T["ready"] in top_text or now - self.stage_since > READY_FALLBACK_S):
            solver = f"python3 {T['solver']}"
            command = f"{solver}\n" if AUTO else f"read -p 'Windows arranged? Press Enter to start the robot... ' _ && {solver}\n"
            self.type_into(self.bottom, command)
            self.set_stage("waiting_robot")
        elif self.stage == "waiting_robot" and T["running"] in self.screen_text(self.bottom):
            self.robot_started_at = now
            self.set_stage("running", "Robot running · don't touch anything until DONE")
        elif self.stage == "waiting_robot" and now - self.stage_since > START_TIMEOUT_S:
            self.set_stage("timeout", f"Robot not started within {START_TIMEOUT_S // 60} min · stopping (no zip)")
        elif self.stage == "running":
            over = (T["over_launcher"] and T["over_launcher"] in top_text) or \
                   (T["over_solver"] and T["over_solver"] in self.screen_text(self.bottom))
            if over and self.over_since is None:
                self.over_since = now
            if over and (self.fresh_result() or now - self.over_since > RESULT_WAIT_S):
                self.set_stage("solved", "RUN OVER · stopping, zipping…")
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
            self.type_into(self.top, f"zip '{ZIP}' result.json {T['solver']} && unzip -l '{ZIP}'\n")
            self.set_stage("zipping")
        elif self.stage == "stopping_fail" and now - self.stage_since > 3:
            self.ensure_launcher_stopped()
            self.finish(zip_made=False)
        elif self.stage == "zipping" and now - self.stage_since > 3:
            self.finish(zip_made=(TASK / ZIP).exists() and self.fresh_result())
        return self.stage not in ("done", "failed")

    def fresh_result(self):
        result = TASK / "result.json"
        return result.exists() and self.launched_at is not None and result.stat().st_mtime >= self.launched_at - 1

    def ensure_launcher_stopped(self):
        if DRY:
            subprocess.run(["pkill", "-INT", "-f", f"{TASK}/{T['launcher']}"], check=False)
            return
        if subprocess.run(["pgrep", "-x", T["launcher"]], capture_output=True).returncode == 0:
            subprocess.run(["pkill", "-TERM", "-x", T["launcher"]], check=False)   # it ignored Ctrl+C

    def finish(self, zip_made):
        if self.recorder:
            self.recorder.stop()
        self.session.release()
        if NO_VIDEO and not DRY:             # rehearsal: keep its sealed result + zip out of the task folder
            keep = TRIALS / f"rehearsal_{STAMP}"
            keep.mkdir(parents=True, exist_ok=True)
            for name in ("result.json", ZIP):
                if (TASK / name).exists():
                    shutil.move(str(TASK / name), str(keep / name))
            print(f"rehearsal result + zip moved to {keep}", flush=True)
        if not DRY and not NO_VIDEO and VIDEO.exists():          # sim-only copy: the right half, below the top bar
            GLib.timeout_add_seconds(2, self.crop_copy)
        video = "dry run, no video" if DRY else ("rehearsal, no video" if NO_VIDEO else str(VIDEO))
        launcher_text = self.full_text(self.top)
        collisions = launcher_text.count("COLLISION")
        caught = "CAUGHT" in launcher_text
        if caught or collisions:
            verdict = ("CAUGHT BY THE GHOST" if caught else f"{collisions} COLLISION line(s)") + \
                      " · do NOT submit this one: run the tool again (each run is a new random draw)"
        else:
            verdict = "0 collisions · OK to submit" if zip_made else "not finished"
        summary = f"DONE · {verdict} · zip {'made' if zip_made else 'NOT made'} · video: {video}"
        self.set_stage("done", summary)
        if not DRY:
            GLib.timeout_add_seconds(CLOSE_AFTER_DONE_S, self.close)
        TRIALS.mkdir(exist_ok=True)
        zip_at = (TRIALS / f"rehearsal_{STAMP}" / ZIP) if NO_VIDEO and not DRY else TASK / ZIP
        (TRIALS / f"recorded_{STAMP}{'_dry' if DRY else ''}.txt").write_text(
            f"{summary}\nfolder: {TASK}\nzip: {zip_at if zip_made else '-'}\n\n--- launcher pane ---\n"
            f"{self.full_text(self.top)}\n\n--- solver pane ---\n{self.full_text(self.bottom)}\n")
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
        for topic in T["retained"]:     # a stale retained message from an earlier run confuses a new one
            subprocess.run(["mosquitto_pub", "-t", topic, "-r", "-n"], check=False)
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
