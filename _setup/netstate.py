#!/usr/bin/env python3
"""
name: netstate
type: script
description: Which network the Mac is on and whether it is metered. Fingerprint = the default gateway's MAC (macOS hides the Wi-Fi name without Location permission). Policy from _setup/metered-networks.md; unknown networks are metered while the policy date runs. `mark <label> metered|unmetered` records the current network.
why: Gordon roams on a capped cell plan (30 GB through 2026-10-06); heavy work must wait for unmetered Wi-Fi automatically instead of by memory (Cowork request, 2026-09-30).
reads: route/arp (default gateway); _setup/metered-networks.md
writes: ~/.local/state/sancho/network.json; _setup/metered-networks.md (only on `mark`)
schedule: every watcher tick
test: _setup/tests/netstate/
"""
from __future__ import annotations
import os, re, sys, json, datetime, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sancho_lib import tree_root

ROOT = tree_root()
POLICY = ROOT / "_setup" / "metered-networks.md"
STATE = Path(os.environ.get("SANCHO_STATE", Path.home() / ".local/state/sancho")) / "network.json"


def fingerprint() -> tuple[str, str]:
    """(gateway MAC, interface) or ('', '') when offline. SANCHO_NET_FINGERPRINT overrides (tests)."""
    fake = os.environ.get("SANCHO_NET_FINGERPRINT")
    if fake is not None:
        return fake, "test"
    try:
        r = subprocess.run(["route", "-n", "get", "default"], capture_output=True, text=True, timeout=5).stdout
        gw = re.search(r"gateway:\s*(\S+)", r)
        iface = re.search(r"interface:\s*(\S+)", r)
        if not gw:
            return "", ""
        a = subprocess.run(["arp", "-n", gw.group(1)], capture_output=True, text=True, timeout=5).stdout
        mac = re.search(r" at ([0-9a-f:]+) ", a)
        norm = ":".join(f"{int(x, 16):02x}" for x in mac.group(1).split(":")) if mac else f"gw-{gw.group(1)}"
        return norm, iface.group(1) if iface else ""
    except Exception:
        return "", ""


def policy() -> tuple[str | None, dict]:
    """(unknown-networks-metered-until date, {fingerprint: (label, metered bool)})."""
    until, nets = None, {}
    if not POLICY.exists():
        return until, nets
    for ln in POLICY.read_text().splitlines():
        m = re.match(r"\s*unknown networks:\s*metered until (\d{4}-\d\d-\d\d)", ln, re.I)
        if m:
            until = m.group(1)
        cells = [c.strip().strip("`") for c in ln.strip().strip("|").split("|")]
        if len(cells) >= 3 and re.match(r"^[0-9a-f]{2}(:[0-9a-f]{2}){5}$|^gw-", cells[0]):
            nets[cells[0]] = (cells[1], cells[2].lower().startswith("metered"))
    return until, nets


def current() -> dict:
    fp, iface = fingerprint()
    until, nets = policy()
    today = datetime.date.today().isoformat()
    if not fp:
        st = {"fingerprint": "", "label": "offline", "metered": False, "why": "no network"}
    elif fp in nets:
        label, met = nets[fp]
        st = {"fingerprint": fp, "label": label, "metered": met, "why": "listed in metered-networks.md"}
    else:
        met = bool(until and today <= until)
        # a locally administered MAC (second hex digit 2/6/a/e) is what phone hotspots use
        hint = "looks like a phone hotspot" if int(fp[1], 16) & 2 and not fp.startswith("gw-") else "unlisted"
        st = {"fingerprint": fp, "label": f"unknown ({hint})", "metered": met,
              "why": f"unknown networks metered until {until}" if met else "unknown network, no metered policy in force"}
    st.update(interface=iface, checked_at=datetime.datetime.now().astimezone().replace(microsecond=0).isoformat())
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st))
    return st


def mark(label: str, kind: str) -> str:
    fp, _ = fingerprint()
    if not fp:
        return "netstate: offline; nothing to mark"
    kind = "metered" if kind.startswith("met") else "unmetered"
    text = POLICY.read_text()
    lines = [l for l in text.splitlines() if not l.strip().startswith(f"| {fp} ")]
    lines.append(f"| {fp} | {label} | {kind} | {datetime.date.today().isoformat()} |")
    POLICY.write_text("\n".join(lines) + "\n")
    current()
    return f"netstate: {fp} marked {kind} as '{label}'"


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "mark":
        print(mark(sys.argv[2], sys.argv[3]))
    else:
        s = current()
        print(f"netstate: {s['label']} ({s['fingerprint'] or '-'}): {'METERED' if s['metered'] else 'unmetered'} · {s['why']}")
