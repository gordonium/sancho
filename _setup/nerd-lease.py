#!/usr/bin/env python3
"""
name: nerd-lease
type: script
description: Leases for Nerd sessions in _queue/leases/, so a cold hop or job.run sees "a Nerd is active" mechanically. `run -- <cmd…>` wraps an interactive Claude Code session (the `sancho nerd` shell phrase): takes `nerd-interactive-<stamp>.md` carrying its pid, touches it every 5 min, removes it when the session ends. `take`/`release` for hooks; `status` lists live Nerd leases (exit 1 if any).
why: Must-never 5 (one writer at a time). Cold hops had to infer "interactive Nerd active" from file timestamps (STATUS.md, check-backs 2026-10-01); a lease with a pid and a heartbeat is a fact, not an inference.
reads: _queue/leases/
writes: _queue/leases/nerd-interactive-<stamp>.md (while the session runs)
schedule:
test: _setup/tests/nerd-lease/
"""
from __future__ import annotations
import os, sys, time, signal, argparse, datetime, threading, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sancho_lib import tree_root, live_leases, write_lease

ROOT = tree_root()
HEARTBEAT_S = int(os.environ.get("SANCHO_LEASE_HEARTBEAT", "300"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["run", "take", "release", "status"])
    ap.add_argument("--name", help="lease name (default nerd-interactive-<stamp>)")
    ap.add_argument("--session", default=os.environ.get("SANCHO_SESSION", "interactive"))
    ap.add_argument("--pid", type=int, help="pid the lease follows (take; default the parent shell)")
    argv = sys.argv[1:]
    cut = argv.index("--") if "--" in argv else len(argv)
    a = ap.parse_args(argv[:cut])
    a.cmd = argv[cut + 1:]
    if a.action == "status":
        live = live_leases(ROOT)
        for p, fm in live:
            print(f"{p.stem}: {fm.get('kind', '?')} · {fm.get('session', '?')} · since {fm.get('started', '?')}")
        print(f"nerd-lease: {len(live)} live Nerd lease(s)")
        return 1 if live else 0
    name = a.name or "nerd-interactive-" + datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    if a.action == "take":
        p = write_lease(ROOT, name, "interactive", a.session, a.pid or os.getppid())
        print(f"nerd-lease: took {p.name}")
        return 0
    if a.action == "release":
        (ROOT / "_queue" / "leases" / f"{name}.md").unlink(missing_ok=True)
        print(f"nerd-lease: released {name}")
        return 0
    cmd = a.cmd
    if not cmd:
        raise SystemExit("nerd-lease: run needs a command after --")
    lease = write_lease(ROOT, name, "interactive", a.session, os.getpid(), " ".join(cmd))
    stop = threading.Event()

    def beat():
        while not stop.wait(HEARTBEAT_S):
            try:
                os.utime(lease)
            except OSError:
                pass
    threading.Thread(target=beat, daemon=True).start()
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))
    signal.signal(signal.SIGHUP, lambda *_: sys.exit(129))
    signal.signal(signal.SIGINT, signal.SIG_IGN)  # Ctrl-C belongs to the session, not the wrapper
    try:
        return subprocess.Popen(cmd, preexec_fn=lambda: signal.signal(signal.SIGINT, signal.SIG_DFL)).wait()
    finally:
        stop.set()
        lease.unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit(main())
