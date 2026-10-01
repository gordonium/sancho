"""
name: sancho_lib
type: script
description: Shared helpers for Sancho's build scripts: find the tree, read YAML-ish frontmatter without PyYAML, walk files, ask git for last-updated dates; write requests; write and read Nerd leases.
why: The lint, the index builder and the map builder must agree on what a file's frontmatter says; one reader, one answer.
reads: any Markdown file in the tree; git log (read-only)
writes: nothing itself; enqueue() and write_lease() write for their callers (_queue/requests/, _queue/leases/)
schedule:
test: _setup/tests/sancho_lib/
"""
from __future__ import annotations
import os, re, subprocess, datetime
from pathlib import Path

# Folders never walked for indexes or the map (state, references, design, git internals).
SKIP_DIRS = {".git", "_reference", "_design", "_queue", "node_modules", ".venv", "__pycache__", "_killed", "_archive", "fixture"}
GENERATED_NAMES = {"INDEX.md", "MAP.md", "PROJECTS.md", "STATUS.md", "HEALTH.md", "TESTS.md", "LINT.md", "CONTACTS.csv", "_registry.md", "GIT-EXCLUDED.md", "ICE.md", "index-manifest.json"}


def tree_root(start: Path | None = None) -> Path:
    """The Sancho tree: $SANCHO_ROOT if set (tests point it at a fixture), else the nearest
    ancestor of the current directory, else of this file, that contains CLAUDE.md and _setup/."""
    env = os.environ.get("SANCHO_ROOT")
    if env:
        return Path(env).resolve()
    for origin in ([start] if start else []) + [Path.cwd(), Path(__file__)]:
        p = origin.resolve()
        for cand in [p] + list(p.parents):
            if (cand / "CLAUDE.md").exists() and (cand / "_setup").is_dir():
                return cand
    raise SystemExit("not inside a Sancho tree (no CLAUDE.md + _setup/ above here)")


_FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.S)


def _parse_scalar(v: str):
    v = v.strip()
    if v == "" or v == "~":
        return None
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(x) for x in _split_top(inner)]
    if v.startswith("{") and v.endswith("}"):
        inner = v[1:-1].strip()
        out = {}
        if inner:
            for part in _split_top(inner):
                if ":" in part:
                    k, val = part.split(":", 1)
                    out[k.strip()] = _parse_scalar(val)
        return out
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    if v.lower() in ("true", "yes"):
        return True
    if v.lower() in ("false", "no"):
        return False
    return v


def _split_top(s: str):
    """Split on commas not inside brackets/braces/quotes."""
    out, depth, cur, q = [], 0, "", None
    for ch in s:
        if q:
            cur += ch
            if ch == q:
                q = None
            continue
        if ch in "\"'":
            q = ch; cur += ch; continue
        if ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur); cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur)
    return [x.strip() for x in out]


def read_frontmatter(path: Path) -> tuple[dict, str]:
    """Return (frontmatter dict, body). Handles simple YAML: key: value, inline lists/maps,
    and block lists of scalars or inline maps. Nested block maps are kept as raw strings."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {}, ""
    m = _FM_RE.match(text)
    if not m:
        # Python scripts carry the header in a docstring.
        if path.suffix == ".py":
            dm = re.match(r'\A(?:#![^\n]*\n)?\s*(?:"""|\'\'\')\s*\n(.*?)(?:"""|\'\'\')', text, re.S)
            if dm:
                return _parse_block(dm.group(1)), text
        return {}, text
    return _parse_block(m.group(1)), text[m.end():]


def _parse_block(block: str) -> dict:
    fm, cur_key = {}, None
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.strip().startswith("-") or any(ch in raw for ch in "\"'{}[]"):
            line = raw.rstrip()
        else:
            line = raw.split(" #", 1)[0].rstrip()
        if raw.startswith((" ", "\t")) and cur_key is not None:
            item = line.strip()
            if item.startswith("- "):
                val = fm.get(cur_key)
                if not isinstance(val, list):
                    fm[cur_key] = []
                fm[cur_key].append(_parse_scalar(item[2:]))
            else:
                # nested map line: keep as raw text under the key
                val = fm.get(cur_key)
                if not isinstance(val, dict):
                    fm[cur_key] = {}
                if ":" in item:
                    k, v = item.split(":", 1)
                    fm[cur_key][k.strip()] = _parse_scalar(v)
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            cur_key = k.strip()
            fm[cur_key] = _parse_scalar(v) if v.strip() else None
    return fm


def walk(root: Path, sub: Path | None = None):
    """Yield (dirpath, dirnames, filenames) skipping SKIP_DIRS, sorted."""
    base = root / sub if sub else root
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        yield Path(dirpath), dirnames, sorted(f for f in filenames if not f.startswith("."))


def git_updated(root: Path, rel: str) -> str:
    """Last commit date (YYYY-MM-DD) touching rel; falls back to file mtime."""
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel], cwd=root,
                             capture_output=True, text=True, timeout=5).stdout.strip()
        if out:
            return out
    except Exception:
        pass
    try:
        ts = (root / rel).stat().st_mtime
        return datetime.date.fromtimestamp(ts).isoformat()
    except Exception:
        return ""


def is_generated(path: Path) -> bool:
    return path.name in GENERATED_NAMES


def today() -> str:
    return datetime.date.today().isoformat()


# ---------- leases (must-never 5: one writer at a time) ----------
LEASE_STALE_H = 2


def pid_alive(pid) -> bool:
    try:
        os.kill(int(pid), 0)
        return True
    except PermissionError:  # exists, just not ours to signal
        return True
    except (OSError, ValueError, TypeError):
        return False


def live_leases(root: Path, prefix: str = "nerd-") -> list[tuple[Path, dict]]:
    """Leases in _queue/leases/ named <prefix>*.md that are live: the `pid:` they carry is running, or, with
    no pid (a lease written off the Mac), the file was touched within LEASE_STALE_H hours."""
    import time
    d = root / "_queue" / "leases"
    out = []
    for p in sorted(d.glob(f"{prefix}*.md")) if d.exists() else []:
        fm, _ = read_frontmatter(p)
        alive = pid_alive(fm["pid"]) if fm.get("pid") not in (None, "") else time.time() - p.stat().st_mtime < LEASE_STALE_H * 3600
        if alive:
            out.append((p, fm))
    return out


def enqueue(root: Path, command: str, args: list, by: str, session: str, job: str = "", body: str = "") -> Path:
    """Write one request to _queue/requests/ (atomic; the shape sancho-enqueue.py writes)."""
    import secrets
    q = root / "_queue" / "requests"
    q.mkdir(parents=True, exist_ok=True)
    t = datetime.datetime.now(datetime.timezone.utc)
    name = f"{t.strftime('%Y%m%dT%H%M%SZ')}_{command}_{secrets.token_hex(3)}.md"
    fm = [f"command: {command}", f"args: [{', '.join(str(x) for x in args)}]", f"requested_by: {by}", f"session: {session}",
          f"requested_at: {t.replace(microsecond=0).isoformat()}"] + ([f"job: {job}"] if job else [])
    tmp = q / f".{name}.tmp"
    tmp.write_text("---\n" + "\n".join(fm) + "\n---\n" + (body.rstrip() + "\n" if body else ""), encoding="utf-8")
    os.replace(tmp, q / name)  # the watcher never sees a half-written request
    return q / name


def advance_pending(state: Path, job: str | None = None, why: str = "", drop: bool = False) -> dict:
    """Jobs job.run could not advance because a Nerd held the tree; the watcher re-queues them when the leases clear.
    With job: add it (or drop it); always returns the current {job: {since, why}}."""
    import json, time
    f = state / "advance-pending.json"
    try:
        d = json.loads(f.read_text())
    except Exception:
        d = {}
    if job:
        if drop:
            d.pop(job, None)
        else:
            d.setdefault(job, {"since": time.time(), "why": why})
        state.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(d, indent=1))
    return d


def write_lease(root: Path, name: str, kind: str, session: str, pid: int, note: str = "") -> Path:
    """One lease file: who holds the tree (kind, session, pid, since). Cowork reads it as text; the Mac also checks the pid."""
    d = root / "_queue" / "leases"
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{name}.md"
    stamp = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    tmp = d / f".{name}.tmp"
    tmp.write_text(f"---\nname: {name}\ntype: lease\nlobe: both\ndescription: {kind} Nerd session holds the tree ({session})\n"
                   f"kind: {kind}\nsession: {session}\npid: {pid}\nstarted: {stamp}\n---\n{note[:500]}\n", encoding="utf-8")
    os.replace(tmp, p)
    return p
