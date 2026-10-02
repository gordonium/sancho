"""
name: sancho_lib
type: script
description: Shared helpers for Sancho's build scripts: find the tree, read YAML-ish frontmatter without PyYAML, walk files, ask git for last-updated dates; write requests; write and read Nerd leases; read a free-text city as a geocoder query (city_query, place_matches).
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


def write_lease(root: Path, name: str, kind: str, session: str, pid: int, note: str = "", writes_only: list | None = None) -> Path:
    """One lease file: who holds the tree (kind, session, pid, since), or with `writes_only` only those paths.
    Cowork reads it as text; the Mac also checks the pid; the guard refuses other sessions' writes inside `writes_only` (ERRORS.md #12)."""
    import json
    d = root / "_queue" / "leases"
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{name}.md"
    stamp = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    tmp = d / f".{name}.tmp"
    scope = f"writes_only: {json.dumps(as_paths(writes_only))}\n" if as_paths(writes_only) else ""
    holds = "holds " + ", ".join(as_paths(writes_only)) if scope else "holds the tree"
    tmp.write_text(f"---\nname: {name}\ntype: lease\nlobe: both\ndescription: {kind} Nerd session {holds} ({session})\n"
                   f"kind: {kind}\nsession: {session}\npid: {pid}\nstarted: {stamp}\n{scope}---\n{note[:500]}\n", encoding="utf-8")
    os.replace(tmp, p)
    return p


# ---------- disjoint write sets (STATUS.md 2026-10-01 23:40: two Nerd sessions at once when their writes cannot meet) ----------
NERD_MAX_PARALLEL = 2
EX_DEFER = 75  # nerd-run.py's exit code for "cannot start now, a Nerd holds what this task writes" (sysexits EX_TEMPFAIL)


def as_paths(v) -> list[str]:
    """A `writes_only` value (list, one string, or nothing) as tidy tree-relative paths."""
    items = v if isinstance(v, list) else [v] if v not in (None, "") else []
    return [s for s in (str(x).strip().removeprefix("./").rstrip("/") for x in items) if s]


def paths_overlap(a: list[str], b: list[str]) -> str | None:
    """The first pair that can name the same file: equal, one a folder above the other, or a wildcard match either way."""
    import fnmatch
    for x in a:
        for y in b:
            if x == y or x.startswith(y + "/") or y.startswith(x + "/") or fnmatch.fnmatch(x, y) or fnmatch.fnmatch(y, x):
                return f"{x} / {y}"
    return None


def task_frontmatter(text: str) -> dict:
    """The frontmatter a task carries at its top (a task file is given to the Nerd whole), or {}."""
    m = re.match(r"\s*---\n(.*?)\n---\s*(?:\n|$)", text, re.S)
    try:
        return _parse_block(m.group(1)) if m else {}
    except Exception:
        return {}


def nerd_admit(root: Path, writes_only, me: str = "") -> tuple[bool, str]:
    """May a nerd.run session start now? Yes with no other nerd.run lease live. Beside a live one only when both sides
    declare `writes_only`, the sets cannot meet, and fewer than NERD_MAX_PARALLEL are running. A session without
    `writes_only` keeps the one-at-a-time rule (must-never 5)."""
    mine = as_paths(writes_only)
    live = [(p, fm) for p, fm in live_leases(root) if fm.get("kind") == "nerd.run" and p.stem != me]
    if not live:
        return True, ""
    if len(live) >= NERD_MAX_PARALLEL:
        return False, f"{len(live)} Nerd sessions are already running ({', '.join(p.stem for p, _ in live)})"
    if not mine:
        return False, f"this task declares no writes_only and {live[0][0].stem} is running"
    for p, fm in live:
        theirs = as_paths(fm.get("writes_only"))
        if not theirs:
            return False, f"{p.stem} holds the whole tree (no writes_only)"
        hit = paths_overlap(mine, theirs)
        if hit:
            return False, f"write sets overlap with {p.stem} ({hit})"
    return True, f"beside {', '.join(p.stem for p, _ in live)} (disjoint writes)"


# ---------- places (the nomad brief and people/_geo.json read a city the same way) ----------
US_STATES = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
             "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia",
             "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
             "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts",
             "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", "MT": "Montana",
             "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico",
             "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
             "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota",
             "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
             "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming", "PR": "Puerto Rico"}
_NOT_A_PLACE_RE = re.compile(r"\b(unknown|not stated|in the wind|tbd|n/a)\b", re.I)


def city_query(raw) -> tuple[str | None, str, str]:
    """A free-text city ("Austin, TX area", "Fort Collins CO [inferred: …]", "Tropea") as (cache key, name, hint),
    or (None, why, "") when it names no place. The hint (a state, its abbreviation or a country) must match the
    geocoder's answer; brackets, parentheses and a trailing "area" are dropped."""
    s = str(raw or "").strip()
    if not s:
        return None, "blank", ""
    if _NOT_A_PLACE_RE.search(s):
        return None, "not a place", ""
    s = re.sub(r"\s+", " ", re.sub(r"\([^)]*\)", "", re.sub(r"\[[^\]]*\]", "", s))).strip(" ,;")
    s = re.sub(r"\s+area$", "", s, flags=re.I).strip(" ,")
    if not s or not s[0].isupper() or ";" in s:
        return None, "not a place", ""
    name, hint = s, ""
    if "," in s:
        name, hint = (x.strip() for x in s.split(",", 1))
    else:
        m = re.match(r"^(.*\S)\s+([A-Z]{2})$", s)
        if m and m.group(2) in US_STATES:
            name, hint = m.groups()
    return f"{name}|{hint}".lower(), name, hint


def place_matches(hint: str, hit: dict) -> bool:
    """Does a geocoder result (Open-Meteo's shape: admin1, country, country_code) satisfy the hint?"""
    if not hint:
        return True
    h = hint.strip().lower().rstrip(".")
    full = US_STATES.get(hint.strip().upper(), "").lower()
    admin1, country, cc = (str(hit.get(k) or "").lower() for k in ("admin1", "country", "country_code"))
    if full:
        return cc == "us" and admin1 == full
    return h in (admin1, country, cc) or (h in ("usa", "us", "united states") and cc == "us")
