#!/usr/bin/env python3
"""
name: notify
type: command
description: Send one Pushover message to Gordon. Levels (Gordon, 2026-10-01): info -1 (silent: completions, recoveries, progress); warn 0 (sound: he must move: a job at a gate, stopped or blocked, a chain end); alert 0 for now with its own title and sound (pipeline red, watcher dead); priority 1 is reserved, so Pushover's quiet hours hold for every push. warn and alert carry `--reason=<slug>` from _setup/notify-reasons.md. The sender's session (`--session` or $SANCHO_SESSION) is echoed in the message. Deduped per key: sends when the message for a key changes, otherwise at most once a day.
why: Must-never 10: the pipeline never falls behind silently. The phone channel is Pushover (architecture §13.6, P-1); dedupe and the reasons registry keep it from becoming noise he learns to ignore.
reads: PUSHOVER_USER, PUSHOVER_TOKEN from the env (~/.config/sancho/env via the watcher); _setup/notify-reasons.md; SANCHO_SESSION; SANCHO_PUSHOVER_URL (tests only; a file:// URL appends the payload to that file instead of posting)
writes: one HTTPS POST; ~/.local/state/sancho/notify.json (dedupe state)
schedule:
test: _setup/tests/notify/
"""
from __future__ import annotations
import os, re, sys, json, time, hashlib, argparse, urllib.parse, urllib.request
from pathlib import Path

URL = os.environ.get("SANCHO_PUSHOVER_URL", "https://api.pushover.net/1/messages.json")
STATE = Path(os.environ.get("SANCHO_STATE", Path.home() / ".local/state/sancho")) / "notify.json"
# alert stays at 0 until Gordon names a reason for breaking through quiet hours (priority 1) [gordon 2026-10-01]
PRIORITY = {"info": -1, "warn": 0, "alert": 0}
TITLE = {"alert": "Sancho ALERT"}
SOUND = {"alert": "siren"}
REASONS = Path(__file__).resolve().parent / "notify-reasons.md"
DAY = 86400


def registered_reasons(path: Path = REASONS) -> dict:
    """notify-reasons.md table → {reason: level}."""
    out = {}
    for ln in path.read_text(encoding="utf-8").splitlines() if path.exists() else []:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[1] in ("warn", "alert") and re.fullmatch(r"[a-z0-9-]+", cells[0]):
            out[cells[0]] = cells[1]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("level", choices=sorted(PRIORITY))
    # Request args are split on unquoted commas (args: [warn, a, b]); rejoin so a message with a comma arrives whole.
    ap.add_argument("message", nargs="+")
    ap.add_argument("--key", help="dedupe key; default: level + message")
    ap.add_argument("--title")
    ap.add_argument("--reason", help="required for warn/alert: a row of _setup/notify-reasons.md")
    ap.add_argument("--session", default=os.environ.get("SANCHO_SESSION", ""), help="who is sending (echoed in the message)")
    a = ap.parse_intermixed_args()
    a.message = ", ".join(m.strip() for m in a.message)
    base = a.message
    if a.level != "info" and registered_reasons().get(a.reason or "") != a.level:
        # never drop a sounding push (must-never 10); tag it so the miss is visible, and the notify suite catches the sender
        print(f"notify: {a.level} reason '{a.reason or ''}' is not registered for {a.level} in _setup/notify-reasons.md; sent anyway, tagged")
        a.message += " (unregistered reason)"
    if a.session:
        a.message += f" · from {a.session}"
    user, token = os.environ.get("PUSHOVER_USER"), os.environ.get("PUSHOVER_TOKEN")
    if not user or not token:
        print("notify: PUSHOVER_USER/PUSHOVER_TOKEN not set (secrets locked or not added yet)")
        return 1
    key = a.key or f"{a.level}:{base}"
    digest = hashlib.sha256(f"{a.level}|{base}".encode()).hexdigest()[:16]  # who sent it doesn't make it news
    STATE.parent.mkdir(parents=True, exist_ok=True)
    try:
        state = json.loads(STATE.read_text())
    except Exception:
        state = {}
    prev = state.get(key)
    if prev and prev.get("digest") == digest and time.time() - prev.get("sent", 0) < DAY:
        print(f"notify: skipped (same message for '{key}' already sent in the last day)")
        return 0
    fields = {"token": token, "user": user, "message": a.message[:1024],
              "title": a.title or TITLE.get(a.level, "Sancho"), "priority": PRIORITY[a.level]}
    if a.level in SOUND:
        fields["sound"] = SOUND[a.level]
    data = urllib.parse.urlencode(fields).encode()
    try:
        if URL.startswith("file://"):  # tests: a sink file, so suites run where localhost can't be bound
            with open(URL[len("file://"):], "a") as f:
                f.write(data.decode() + "\n")
            ok = True
        else:
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
