#!/usr/bin/env python3
"""
name: sancho-watcher
type: script
description: One tick of the host execution bridge. Runs every allowlisted request in _queue/requests/, writes one result per request to _queue/results/, then rewrites _queue/HEALTH.md. Exits; launchd calls it again on any change to requests/ and every 60 s.
why: A Cowork session can't run anything on the Mac; the queue is the one audited path for every Mac-side run (architecture §1). HEALTH.md is how a session knows the runner is alive instead of pretending a run happened.
reads: _setup/commands.md (the allowlist); the lint's verdict on the tree (every tick); _queue/requests/*.md; ~/.config/sancho/env; _queue/leases/, _queue/sessions/; _setup/GIT-EXCLUDED.md; pmset -g log
writes: _queue/results/<request name>; _queue/deferred/ (heavy requests while metered); _queue/log/<date>.log; _queue/HEALTH.md; state in ~/.local/state/sancho/ (lock, tick times, last status per command)
schedule: launchd com.sancho.watcher (WatchPaths on _queue/requests/, StartInterval 60, RunAtLoad)
test: _setup/tests/watcher/
"""
from __future__ import annotations
import os, re, sys, json, time, fcntl, signal, shutil, datetime, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sancho_lib import tree_root, read_frontmatter

ROOT = tree_root()
Q = ROOT / "_queue"
REQ, RES, LOG, RUNNING, DEFERRED = Q / "requests", Q / "results", Q / "log", Q / "running", Q / "deferred"
STATE = Path(os.environ.get("SANCHO_STATE", Path.home() / ".local/state/sancho"))
ENV_FILE = Path(os.environ.get("SANCHO_SECRETS_PLAIN", Path.home() / ".config/sancho/env"))
AGE_FILE = Path(os.environ.get("SANCHO_SECRETS_AGE", Path.home() / "Sync/Sancho-Secrets/sancho.env.age"))
TAIL_LINES, RESULT_KEEP_DAYS, LEASE_STALE_H = 40, 90, 2


def now() -> datetime.datetime:
    return datetime.datetime.now().astimezone().replace(microsecond=0)


def iso(t: datetime.datetime) -> str:
    return t.isoformat()


def load_commands() -> dict:
    """commands.md table → {name: {script, timeout, schedule, terminal_only}}."""
    out = {}
    p = ROOT / "_setup" / "commands.md"
    for ln in p.read_text(encoding="utf-8").splitlines():
        cells = [c.strip().strip("`") for c in ln.strip().strip("|").split("|")]
        if len(cells) < 5 or cells[0] in ("command", "") or set(cells[0]) <= set("-: "):
            continue
        try:
            timeout = int(cells[2])
        except ValueError:
            timeout = 120
        out[cells[0]] = {"script": cells[1], "timeout": timeout, "schedule": cells[3],
                         "terminal_only": "terminal only" in cells[3].lower(),
                         "heavy": "[heavy]" in (cells[3] + " " + cells[4]).lower()}
    return out


def load_env() -> dict:
    env = dict(os.environ)
    env["PATH"] = "/opt/homebrew/bin:/usr/local/bin:" + env.get("PATH", "/usr/bin:/bin")
    if ENV_FILE.exists():
        for ln in ENV_FILE.read_text(encoding="utf-8").splitlines():
            ln = ln.strip()
            if ln and not ln.startswith("#") and "=" in ln:
                k, v = ln.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    env["SANCHO_ROOT"] = str(ROOT)
    return env


def argv_for(script: Path, args) -> list:
    base = ["bash", str(script)] if script.suffix == ".sh" else ["python3", str(script)] if script.suffix == ".py" else [str(script)]
    if isinstance(args, list):
        return base + [str(a) for a in args if a is not None]
    if isinstance(args, dict):
        return base + [f"--{k}={v}" for k, v in args.items()]
    if args not in (None, ""):
        return base + [str(args)]
    return base


def write_result(name: str, fm: dict, body: str):
    RES.mkdir(parents=True, exist_ok=True)
    lines = ["---"] + [f"{k}: {v}" for k, v in fm.items()] + ["---", body]
    tmp = RES / f".{name}.tmp"
    tmp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.replace(tmp, RES / name)


def log_line(text: str):
    LOG.mkdir(parents=True, exist_ok=True)
    with open(LOG / f"{datetime.date.today().isoformat()}.log", "a", encoding="utf-8") as f:
        f.write(text.rstrip("\n") + "\n")


def run_one(req: Path, commands: dict, env: dict) -> str:
    """Claim a request by atomic rename, run it, write its result. Returns the status."""
    RUNNING.mkdir(parents=True, exist_ok=True)
    claimed = RUNNING / req.name
    try:
        os.rename(req, claimed)
    except FileNotFoundError:
        return "gone"  # another tick took it
    fm, _ = read_frontmatter(claimed)
    cmd = str(fm.get("command") or "")
    rid = req.stem
    started = now()
    rel_log = f"_queue/log/{started.date().isoformat()}.log"
    c = commands.get(cmd)
    if c is not None and c["heavy"] and NET.get("metered"):
        DEFERRED.mkdir(parents=True, exist_ok=True)
        os.replace(claimed, DEFERRED / req.name)
        write_result(req.name, {"command": cmd, "status": "deferred", "started_at": iso(started), "finished_at": iso(now()),
                                "exit_code": "", "log": rel_log},
                     f"deferred: metered network ({NET.get('label')}); runs on its own when the Mac is on an unmetered network")
        log_line(f"{iso(started)} {rid} {cmd} deferred (metered: {NET.get('label')})")
        return "deferred"
    if c is None or c["terminal_only"]:
        why = "not in _setup/commands.md" if c is None else "runs only in Terminal (it asks for a passphrase)"
        write_result(req.name, {"command": cmd or "(none)", "status": "refused", "started_at": iso(started),
                                "finished_at": iso(now()), "exit_code": "", "log": rel_log}, f"refused: `{cmd}` {why}")
        log_line(f"{iso(started)} {rid} {cmd} refused ({why})")
        claimed.unlink()
        return "refused"
    script = ROOT / c["script"]
    env = dict(env, SANCHO_REQUEST_ID=rid, SANCHO_REQUESTED_BY=str(fm.get("requested_by") or ""))
    status, code, out = "ok", 0, ""
    try:
        p = subprocess.Popen(argv_for(script, fm.get("args")), cwd=ROOT, env=env, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, text=True, start_new_session=True)
        try:
            out, _ = p.communicate(timeout=c["timeout"])
            code = p.returncode
            status = "ok" if code == 0 else "failed"
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, signal.SIGKILL)
            out, _ = p.communicate()
            status, code = "timeout", -9
            out = (out or "") + f"\n(killed after {c['timeout']} s)"
    except Exception as e:  # script missing, not executable, ...
        status, code, out = "failed", -1, f"watcher could not start {c['script']}: {e}"
    finished = now()
    lines = (out or "").rstrip().splitlines()
    summary = lines[-1] if lines else "(no output)"
    body = f"{summary}\n\n```\n" + "\n".join(lines[-TAIL_LINES:]) + "\n```"
    write_result(req.name, {"command": cmd, "status": status, "started_at": iso(started), "finished_at": iso(finished),
                            "exit_code": code, "log": rel_log, "requested_by": fm.get("requested_by") or "",
                            "job": fm.get("job") or ""}, body)
    log_line(f"{iso(started)} {rid} {cmd} {status} exit={code} {(finished - started).seconds}s\n" +
             "".join(f"    {l}\n" for l in lines))
    claimed.unlink()
    notify_on_change(cmd, status, summary, env)
    return status


def notify_on_change(cmd: str, status: str, summary: str, env: dict):
    """Push a failure, and a recovery after a failure; never a routine success."""
    f = STATE / "last-status.json"
    try:
        last = json.loads(f.read_text())
    except Exception:
        last = {}
    prev = last.get(cmd)
    last[cmd] = status
    f.write_text(json.dumps(last, indent=1))
    if status != "ok" or (prev and prev != "ok"):
        if not env.get("PUSHOVER_TOKEN") or not env.get("PUSHOVER_USER"):
            return
        level = "warn"  # info never reaches Gordon (silent, in-app only); recoveries must be heard
        msg = f"{cmd} recovered" if status == "ok" else f"{cmd} {status}: {summary[:200]}"
        subprocess.run(["python3", str(ROOT / "_setup" / "notify.py"), level, msg, f"--key=cmd:{cmd}"],
                       env=env, capture_output=True, timeout=30)


def recover_orphans():
    """A request left in running/ means a tick died mid-run (sleep, crash). Say so in a result."""
    if not RUNNING.exists():
        return
    for p in RUNNING.glob("*.md"):
        if time.time() - p.stat().st_mtime > 3600 * 6:
            fm, _ = read_frontmatter(p)
            write_result(p.name, {"command": fm.get("command") or "", "status": "failed", "started_at": "",
                                  "finished_at": iso(now()), "exit_code": "", "log": ""},
                         "the watcher stopped mid-run (Mac slept or crashed); resubmit if still wanted")
            p.unlink()


def prune_results():
    cutoff = time.time() - RESULT_KEEP_DAYS * 86400
    for p in RES.glob("*.md") if RES.exists() else []:
        if p.stat().st_mtime < cutoff:
            p.unlink()


# ---------- HEALTH.md ----------

PMSET_RE = re.compile(r"^(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) [+-]\d{4} (Sleep|Wake|DarkWake)\s+\t(\S+)", re.M)


def parse_sleep(text: str) -> dict:
    """Last real sleep window from `pmset -g log`. A full wake is a `Wake` line reading `Wake from …`;
    `Wake Requests` (scheduling) and `DarkWake` (maintenance) are not wakes. The window runs from the first
    Sleep after the previous full wake to the last full wake (ERRORS.md #3)."""
    ev = [(d, k) for d, k, first in PMSET_RE.findall(text) if k != "Wake" or first == "Wake"]
    fulls = [i for i, (_, k) in enumerate(ev) if k == "Wake"]
    if not fulls:
        return {}
    last = fulls[-1]
    prev = fulls[-2] if len(fulls) > 1 else -1
    sleeps = [i for i in range(prev + 1, last) if ev[i][1] == "Sleep"]
    if not sleeps:
        return {"wake": ev[last][0]}
    return {"sleep": ev[sleeps[0]][0], "wake": ev[last][0], "dark_wakes": sum(1 for i in range(sleeps[0], last) if ev[i][1] == "DarkWake")}


def mac_sleep_line(t: datetime.datetime) -> str:
    """Last real sleep window from pmset (slow, so cached 15 min)."""
    cache = STATE / "pmset.json"
    data = {}
    try:
        data = json.loads(cache.read_text())
    except Exception:
        pass
    if time.time() - data.get("at", 0) > 900 and shutil.which("pmset"):
        try:
            out = subprocess.run(["pmset", "-g", "log"], capture_output=True, text=True, timeout=20).stdout
            data = {"at": time.time(), **parse_sleep(out)}
            cache.write_text(json.dumps(data))
        except Exception:
            pass
    if data.get("sleep") and data.get("wake"):
        return f"last asleep {data['sleep'][5:16]} → {data['wake'][11:16]} ({data.get('dark_wakes', 0)} maintenance wakes)"
    if data.get("wake"):
        return f"last full wake {data['wake'][5:16]}"
    return "sleep history unavailable"


def ticks_line(tk: dict, t: datetime.datetime) -> str:
    """Ticks per hour for the last 12 hours: an awake witness independent of pmset (0 = the Mac was not running)."""
    hours = tk.get("hours", {})
    cells = []
    for h in range(11, -1, -1):
        key = (t - datetime.timedelta(hours=h)).strftime("%Y-%m-%dT%H")
        cells.append(f"{key[11:]}h:{hours.get(key, 0)}")
    return " ".join(cells)


def health(commands: dict, ran: list, t: datetime.datetime):
    ticks = STATE / "ticks.json"
    try:
        tk = json.loads(ticks.read_text())
    except Exception:
        tk = {}
    prev = tk.get("last")
    gap = f"; previous tick {int((t.timestamp() - prev) / 60)} min ago (Mac was asleep or off)" if prev and t.timestamp() - prev > 300 else ""
    tk["last"] = t.timestamp()
    hk = t.strftime("%Y-%m-%dT%H")
    tk["hours"] = {k: v for k, v in tk.get("hours", {}).items() if k >= (t - datetime.timedelta(hours=24)).strftime("%Y-%m-%dT%H")}
    tk["hours"][hk] = tk["hours"].get(hk, 0) + 1
    ticks.write_text(json.dumps(tk))

    today = t.date().isoformat()
    runs, fails = [], []
    for p in sorted(RES.glob("*.md")) if RES.exists() else []:
        fm, body = read_frontmatter(p)
        if str(fm.get("finished_at") or "").startswith(today):
            runs.append(fm)
            if fm.get("status") not in ("ok",):
                fails.append(f"{fm.get('command')} {fm.get('status')} at {str(fm.get('finished_at'))[11:16]}: {body.strip().splitlines()[0][:100] if body.strip() else ''}")
    pending = [p.name for p in REQ.glob("*.md")] if REQ.exists() else []

    leases, stale_leases = [], []
    for p in sorted((Q / "leases").glob("*.md")) if (Q / "leases").exists() else []:
        age_h = (time.time() - p.stat().st_mtime) / 3600
        (stale_leases if age_h > LEASE_STALE_H else leases).append(f"{p.stem} ({age_h:.1f} h since last write)")
    lease_names = {p.stem for p in (Q / "leases").glob("*.md")} if (Q / "leases").exists() else set()
    stale_notes = [p.stem for p in (Q / "sessions").glob("*.md")] if (Q / "sessions").exists() else []
    stale_notes = [s for s in stale_notes if s not in lease_names]

    excl = ROOT / "_setup" / "GIT-EXCLUDED.md"
    n_excl = len([l for l in excl.read_text().splitlines() if l.startswith("| ") and not l.startswith(("| path", "| (none)"))]) if excl.exists() else 0
    try:
        unpushed = subprocess.run(["git", "rev-list", "--count", "@{u}..HEAD"], cwd=ROOT, capture_output=True, text=True, timeout=10).stdout.strip() or "?"
    except Exception:
        unpushed = "?"

    if not AGE_FILE.exists():
        secrets = "not set up (no sancho.env.age)"
    elif not ENV_FILE.exists():
        secrets = "locked (run sancho.unlock in Terminal)"
    elif ENV_FILE.stat().st_mtime > AGE_FILE.stat().st_mtime + 1:
        secrets = "unlocked, PLAINTEXT NEWER than sancho.env.age (run sancho.lock-secrets)"
    else:
        secrets = "unlocked"

    awake_state = STATE / "stay-awake"
    awake = awake_state.read_text().strip() if awake_state.exists() else "off"

    lint_problems = []
    try:
        lr = subprocess.run(["python3", str(ROOT / "_setup" / "lint-layers.py")], cwd=ROOT, capture_output=True, text=True, timeout=60,
                            env={**os.environ, "SANCHO_ROOT": str(ROOT), "SANCHO_LINT_NO_WRITE": "1"})
        lint_problems = [l[len("PROBLEM: "):] for l in lr.stdout.splitlines() if l.startswith("PROBLEM: ")]
    except Exception as e:
        lint_problems = [f"lint did not run: {e}"]
    problems = []
    if lint_problems:
        problems.append(f"lint: {len(lint_problems)} problem(s) in the tree")
    if fails:
        problems.append(f"{len(fails)} failed run(s) today")
    if n_excl:
        problems.append(f"{n_excl} file(s) excluded from git (see _setup/GIT-EXCLUDED.md)")
    if unpushed not in ("0", "?") and int(unpushed) > 3:
        problems.append(f"{unpushed} commits not pushed to GitHub")
    if stale_leases:
        problems.append(f"{len(stale_leases)} stale lease(s)")
    if "NEWER" in secrets:
        problems.append("secrets plaintext newer than the encrypted copy")

    out = [
        "# HEALTH",
        f"generated {t.strftime('%Y-%m-%d %H:%M %Z')} by sancho-watcher.py · regenerated every tick (≤ 60 s while the Mac is awake)",
        "",
        f"**{'OK' if not problems else 'ATTENTION: ' + '; '.join(problems)}**",
        "",
        f"- watcher last seen: {t.strftime('%Y-%m-%d %H:%M:%S %Z')}{gap}",
        f"- Mac: awake now; {mac_sleep_line(t)}; stay-awake {awake}",
        f"- watcher ticks per hour (last 12 h): {ticks_line(tk, t)}",
        f"- runs today: {len(runs)} ({len(fails)} failed); this tick ran {len(ran)}; waiting in requests/: {len(pending)}",
        f"- git: {unpushed} commit(s) not pushed; {n_excl} file(s) excluded",
        f"- network: {NET.get('label', '?')}, {'METERED: heavy commands deferred (' + str(len(list(DEFERRED.glob('*.md'))) if DEFERRED.exists() else 0) + ' waiting)' if NET.get('metered') else 'unmetered'}",
        f"- secrets: {secrets}",
        f"- commands on the allowlist: {len(commands)}",
        f"- leases live: {', '.join(leases) or 'none'}",
        f"- leases stale (> {LEASE_STALE_H} h): {', '.join(stale_leases) or 'none'}",
        f"- session notes with no lease: {', '.join(stale_notes) or 'none'}",
    ]
    if lint_problems:
        out += ["", "## Lint (this tick)"] + [f"- {p}" for p in lint_problems[:20]] + ([f"- … and {len(lint_problems) - 20} more"] if len(lint_problems) > 20 else [])
    if fails:
        out += ["", "## Failures today"] + [f"- {f}" for f in fails]
    tmp = Q / ".HEALTH.md.tmp"
    tmp.write_text("\n".join(out) + "\n", encoding="utf-8")
    os.replace(tmp, Q / "HEALTH.md")


NET: dict = {}


def check_network() -> dict:
    """netstate.py decides metered/unmetered; on unmetered, deferred heavy requests go back into requests/."""
    try:
        sys.path.insert(0, str(ROOT / "_setup"))
        import netstate
        st = netstate.current()
    except Exception as e:
        st = {"label": f"unknown (netstate failed: {e})", "metered": False}
    if not st.get("metered") and DEFERRED.exists():
        for p in DEFERRED.glob("*.md"):
            os.replace(p, REQ / p.name)
            log_line(f"{iso(now())} {p.stem} released from deferred (network {st.get('label')})")
    return st


def main():
    STATE.mkdir(parents=True, exist_ok=True)
    lock = open(STATE / "watcher.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("another watcher tick is running; exiting")
        return 0
    commands = load_commands()
    env = load_env()
    recover_orphans()
    NET.update(check_network())
    ran = []
    for req in sorted(REQ.glob("*.md")) if REQ.exists() else []:
        if req.name.startswith("."):
            continue
        st = run_one(req, commands, env)
        if st != "gone":
            ran.append((req.name, st))
    prune_results()
    health(commands, ran, now())
    for name, st in ran:
        print(f"{st}: {name}")
    print(f"sancho-watcher: tick done, {len(ran)} run(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
