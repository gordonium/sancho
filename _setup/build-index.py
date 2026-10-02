#!/usr/bin/env python3
"""
name: build-index
type: command
description: Regenerate every INDEX.md in the tree (one line per child from frontmatter), each lobe's PROJECTS.md, the ICE views, the people index with completeness, and the skill index. Never hand-edited outputs.
why: Navigation is a cascade of indexes (architecture §4); they only work if a script writes them from the files themselves, every time, so they cannot drift.
reads: every .md under the tree except SKIP_DIRS; FOCUS.md; git log for updated dates; personal/nomad/_geocache.json (never the network)
writes: INDEX.md in every folder; work/PROJECTS.md, personal/PROJECTS.md; work/ice/ICE.md, personal/ice/ICE.md; people/INDEX.md (with completeness); people/_geo.json (location.city placed through the geocache, with want_to_see_by and last_seen; uncached cities `pending`); skills/INDEX.md; _setup/index-manifest.json (hashes of generated files, for the lint)
schedule: after every commit batch and nightly (via the watcher); on demand as command `index.build`
test: _setup/tests/build-index/
"""
from __future__ import annotations
import sys, json, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sancho_lib import tree_root, read_frontmatter, walk, git_updated, is_generated, today, city_query, SKIP_DIRS

ROOT = tree_root()
MANIFEST = ROOT / "_setup" / "index-manifest.json"
written: dict[str, str] = {}

PERSON_FIELDS = ["description", "mbti", "skills", "availability", "location", "roles", "last_seen",
                 "want_to_see_by", "contact", "voiceprint", "relationships"]
PERSON_SECTIONS = ["## How to work with them", "## Who they are", "## What we know", "## Open threads", "## History with Gordon"]


def rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


def write_generated(path: Path, text: str):
    path.write_text(text, encoding="utf-8")
    written[rel(path)] = hashlib.sha256(text.encode("utf-8")).hexdigest()


def describe(path: Path) -> tuple[str, str, str]:
    """(type, status, description) for a file; folders use their INDEX/entity/business/project file."""
    if path.is_dir():
        for cand in ("entity.md", "business.md", "project.md", "client.md", "README.md"):
            if (path / cand).exists():
                fm, _ = read_frontmatter(path / cand)
                return str(fm.get("type") or "folder"), str(fm.get("status") or ""), str(fm.get("description") or "")
        n = sum(1 for f in path.rglob("*.md") if not is_generated(f))
        return "folder", "", (f"{n} files" if n else "empty")
    fm, _ = read_frontmatter(path)
    return str(fm.get("type") or path.suffix.lstrip(".")), str(fm.get("status") or ""), str(fm.get("description") or "NO DESCRIPTION")


def build_folder_index(folder: Path):
    children = []
    for child in sorted(folder.iterdir(), key=lambda p: p.name.lower()):
        if child.name.startswith(".") or child.name in SKIP_DIRS or is_generated(child):
            continue
        if child.is_dir() and child.name.startswith("_") and child.name not in ("_params",):
            continue
        if child.is_file() and child.suffix not in (".md", ".py", ".sh", ".csv", ".vtt", ".txt"):
            continue
        t, st, d = describe(child)
        upd = git_updated(ROOT, rel(child)) if child.is_file() else ""
        name = child.name + ("/" if child.is_dir() else "")
        parts = [name, t]
        if st: parts.append(st)
        if upd: parts.append(upd)
        parts.append(d)
        children.append("- " + " · ".join(parts))
    head = f"# {rel(folder) or 'Sancho'} · INDEX\ngenerated {today()} by build-index.py · {len(children)} entries\n"
    focus_block = ""
    if rel(folder) in ("work", "personal"):
        focus_block = focus_for(rel(folder))
    write_generated(folder / "INDEX.md", head + focus_block + "\n" + "\n".join(children) + "\n")


def focus_for(lobe: str) -> str:
    f = ROOT / "FOCUS.md"
    if not f.exists():
        return ""
    lines = f.read_text(encoding="utf-8").splitlines()
    out, keep = [], False
    for ln in lines:
        if ln.startswith("## "):
            keep = True; out.append(ln)
        elif keep and ln.strip().lower().startswith(lobe + ":"):
            out.append(ln)
    return "\n## FOCUS (from FOCUS.md)\n" + "\n".join(out) + "\n" if out else ""


def build_projects(lobe: str):
    rows = []
    for dirpath, _, files in walk(ROOT, Path(lobe)):
        if "project.md" in files:
            fm, _ = read_frontmatter(dirpath / "project.md")
            na = fm.get("next_action") or {}
            na_text = na.get("text") if isinstance(na, dict) else str(na or "")
            na_set = na.get("set") if isinstance(na, dict) else ""
            waiting = fm.get("waiting") or []
            wtxt = "; ".join(f"{w.get('who','?')}: {w.get('what','?')} since {w.get('since','?')}" for w in waiting if isinstance(w, dict))
            rows.append(f"| {fm.get('name') or dirpath.name} | {fm.get('status') or ''} | {fm.get('area') or ''} | {na_text or '(none)'} | {na_set or ''} | {wtxt} | {rel(dirpath)}/ |")
    head = f"# {lobe} · PROJECTS\ngenerated {today()} by build-index.py · {len(rows)} projects\n\n| project | status | area | next action | set | waiting for | path |\n|---|---|---|---|---|---|---|\n"
    write_generated(ROOT / lobe / "PROJECTS.md", head + "\n".join(rows) + "\n")


def build_ice(lobe: str):
    folder = ROOT / lobe / "ice"
    if not folder.exists():
        return
    rows = []
    for f in sorted(folder.glob("*.md")):
        if is_generated(f):
            continue
        fm, _ = read_frontmatter(f)
        rows.append(f"| {fm.get('title') or f.stem} | {fm.get('status') or ''} | {fm.get('area') or ''} | {fm.get('project') or ''} | {fm.get('captured') or ''} | {fm.get('next_review') or ''} | {f.name} |")
    head = f"# {lobe} · ICE\ngenerated {today()} by build-index.py · {len(rows)} ideas\n\n| idea | status | area | project | captured | next review | file |\n|---|---|---|---|---|---|---|\n"
    write_generated(folder / "ICE.md", head + "\n".join(rows) + "\n")


def person_completeness(path: Path) -> tuple[int, int]:
    fm, body = read_frontmatter(path)
    filled = 0
    for k in PERSON_FIELDS:
        v = fm.get(k)
        if isinstance(v, dict):
            if any(x not in (None, "", [], {}) for x in v.values()):
                filled += 1
        elif v not in (None, "", [], {}):
            filled += 1
    for sec in PERSON_SECTIONS:
        i = body.find(sec)
        if i >= 0:
            nxt = body.find("\n## ", i + len(sec))
            content = body[i + len(sec): nxt if nxt > 0 else None].strip()
            if content:
                filled += 1
    return filled, len(PERSON_FIELDS) + len(PERSON_SECTIONS)


def build_people():
    folder = ROOT / "people"
    rows, thin = [], 0
    for f in sorted(folder.glob("*.md")):
        if is_generated(f):
            continue
        fm, _ = read_frontmatter(f)
        got, total = person_completeness(f)
        tier = "contact-only" if got <= 2 else ("thin" if got < total // 2 else "full")
        if tier != "full":
            thin += 1
        if tier == "contact-only":
            continue
        rows.append(f"- {f.stem} · {tier} {got}/{total} · {git_updated(ROOT, rel(f))} · {fm.get('description') or 'NO DESCRIPTION'}")
    head = f"# people · INDEX\ngenerated {today()} by build-index.py · {len(rows)} shown, {thin} thin or contact-only (contact-only hidden)\n\n"
    write_generated(folder / "INDEX.md", head + "\n".join(rows) + "\n")


def build_people_geo():
    """people/_geo.json: every person with a `location.city`, placed through the nomad geocache
    (personal/nomad/_geocache.json, filled by nomad-brief.py). Offline by design: a city not in the cache
    is listed `pending` and the next nomad.brief geocodes it; blank cities are skipped, non-places listed."""
    cache_p = ROOT / "personal" / "nomad" / "_geocache.json"
    try:
        cache = json.loads(cache_p.read_text(encoding="utf-8")) if cache_p.exists() else {}
    except ValueError:
        cache = {}
    people, skipped = [], []
    for f in sorted((ROOT / "people").glob("*.md")):
        if is_generated(f):
            continue
        fm, _ = read_frontmatter(f)
        loc = fm.get("location")
        city = loc.get("city") if isinstance(loc, dict) else loc
        key, name, hint = city_query(city)
        if key is None:
            if name != "blank":
                skipped.append({"slug": f.stem, "city": str(city), "why": name})
            continue
        row = {"slug": f.stem, "name": str(fm.get("name") or f.stem), "city": str(city), "query": key,
               "want_to_see_by": str(fm.get("want_to_see_by") or ""), "last_seen": str(fm.get("last_seen") or ""),
               "lat": None, "lon": None, "resolved": "", "pending": True}
        hit = cache.get(key)
        if isinstance(hit, dict) and hit.get("none"):
            skipped.append({"slug": f.stem, "city": str(city), "why": "the geocoder found no such place"}); continue
        if isinstance(hit, dict) and hit.get("lat") is not None:
            row.update(lat=hit["lat"], lon=hit["lon"], resolved=hit.get("label", ""), pending=False)
        people.append(row)
    text = json.dumps({"generated": today(), "by": "build-index.py", "geocache": "personal/nomad/_geocache.json",
                       "people": people, "skipped": skipped}, indent=1, ensure_ascii=False) + "\n"
    write_generated(ROOT / "people" / "_geo.json", text)


def build_skills():
    folder = ROOT / "skills"
    rows = []
    for d in sorted(folder.iterdir()):
        if d.is_dir() and (d / "SKILL.md").exists():
            fm, _ = read_frontmatter(d / "SKILL.md")
            trig = ", ".join(str(t) for t in (fm.get("triggers") or [])[:4])
            rows.append(f"- {d.name} · {fm.get('lobe') or '?'}{' · shared: astra' if fm.get('shared') == 'astra' else ''} · {fm.get('description') or 'NO DESCRIPTION'} · triggers: {trig}")
    head = f"# skills · INDEX\ngenerated {today()} by build-index.py · {len(rows)} skills\n\n"
    write_generated(folder / "INDEX.md", head + "\n".join(rows) + "\n")


def main():
    # folder indexes everywhere except the skip list and people/skills (special)
    for dirpath, dirnames, files in walk(ROOT):
        r = rel(dirpath)
        if r in ("people", "skills") or r.startswith(("people/", "skills/")):
            continue
        if dirpath.name.startswith("_") and dirpath != ROOT:
            continue
        build_folder_index(dirpath)
    for lobe in ("work", "personal"):
        if (ROOT / lobe).exists():
            build_projects(lobe); build_ice(lobe)
    if (ROOT / "people").exists():
        build_people()
        build_people_geo()
    if (ROOT / "skills").exists():
        build_skills()
    MANIFEST.write_text(json.dumps({"generated": today(), "files": written}, indent=1), encoding="utf-8")
    print(f"build-index: wrote {len(written)} generated files")


if __name__ == "__main__":
    main()
