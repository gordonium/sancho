"""
name: sancho_lib
type: script
description: Shared helpers for Sancho's build scripts: find the tree, read YAML-ish frontmatter without PyYAML, walk files, ask git for last-updated dates.
why: The lint, the index builder and the map builder must agree on what a file's frontmatter says; one reader, one answer.
reads: any Markdown file in the tree; git log (read-only)
writes: nothing
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
