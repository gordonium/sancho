#!/usr/bin/env python3
"""
name: notify
type: command
description: Send one Pushover message to Gordon. Level sets priority (info -1, warn 0, alert 1). Rule (Gordon, 2026-09-30): "Warn means WARN": warn makes his phone sound and is only for things needing his attention soon (today: the pipeline red, i.e. recordings not flowing). Everything else is info (silent, in-app) or nothing; no chatter. Deduped per key: sends when the message for a key changes, otherwise at most once a day.
why: Must-never 10: the pipeline never falls behind silently. The phone channel is Pushover (architecture §13.6, P-1); dedupe keeps it from becoming noise he learns to ignore.
reads: PUSHOVER_USER, PUSHOVER_TOKEN from the env (~/.config/sancho/env via the watcher); SANCHO_PUSHOVER_URL (tests only)
writes: one HTTPS POST; ~/.local/state/sancho/notify.json (dedupe state)
schedule:
test: _setup/tests/notify/
"""
from __future__ import annotations
import os, sys, json, time, hashlib, argparse, urllib.parse, urllib.request
from pathlib import Path

URL = os.environ.get("SANCHO_PUSHOVER_URL", "https://api.pushover.net/1/messages.json")
STATE = Path(os.environ.get("SANCHO_STATE", Path.home() / ".local/state/sancho")) / "notify.json"
PRIORITY = {"info": -1, "warn": 0, "alert": 1}
DAY = 86400


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("level", choices=sorted(PRIORITY))
    ap.add_argument("message")
    ap.add_argument("--key", help="dedupe key; default: level + message")
    ap.add_argument("--title", default="Sancho")
    a = ap.parse_args()
    user, token = os.environ.get("PUSHOVER_USER"), os.environ.get("PUSHOVER_TOKEN")
    if not user or not token:
        print("notify: PUSHOVER_USER/PUSHOVER_TOKEN not set (secrets locked or not added yet)")
        return 1
    key = a.key or f"{a.level}:{a.message}"
    digest = hashlib.sha256(f"{a.level}|{a.message}".encode()).hexdigest()[:16]
    STATE.parent.mkdir(parents=True, exist_ok=True)
    try:
        state = json.loads(STATE.read_text())
    except Exception:
        state = {}
    prev = state.get(key)
    if prev and prev.get("digest") == digest and time.time() - prev.get("sent", 0) < DAY:
        print(f"notify: skipped (same message for '{key}' already sent in the last day)")
        return 0
    data = urllib.parse.urlencode({"token": token, "user": user, "message": a.message[:1024],
                                   "title": a.title, "priority": PRIORITY[a.level]}).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(URL, data=data), timeout=20) as r:
            ok = r.status == 200
    except Exception as e:
        print(f"notify: send failed: {e}")
        return 1
    if not ok:
        print("notify: Pushover did not accept the message")
        return 1
    state[key] = {"digest": digest, "sent": time.time()}
    STATE.write_text(json.dumps(state, indent=1))
    print(f"notify: sent ({a.level})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
