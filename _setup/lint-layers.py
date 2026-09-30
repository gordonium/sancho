#!/usr/bin/env python3
"""
name: lint-layers
type: command
description: Enforce the layering rule (architecture §2), the focus caps, the header rule, generated-file integrity, project next-action and waiting-for freshness, and dangling references. Exit 1 on any violation so the map build fails.
why: v2's rules lived in prose and grew to 1,341 lines; v3's 'few rules' grew 6→16 with no mechanism. Rules that a script can check are the only ones that hold.
reads: ~/.config/sancho/env and ~/Sync/Sancho-Secrets/sancho.env.age (mtimes only), CLAUDE.md, FOCUS.md, every .md/.py under the tree except SKIP_DIRS, _setup/index-manifest.json, _setup/commands.md, people/ names
writes: _setup/LINT.md (last result, generated); stdout
schedule: first step of every map build; nightly
test: _setup/tests/lint-layers/ (fixture tree of deliberately bad files; every bad file must be caught, every good file must pass)
"""
from __future__ import annotations
import sys, re, json, hashlib, datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sancho_lib import tree_root, read_frontmatter, walk, is_generated, today, GENERATED_NAMES

ROOT = tree_root()
problems: list[str] = []
warnings: list[str] = []

FOCUS_CAP = 3
CLAUDE_MAX_LINES = 100
BRIEF_MAX, WATCH_MAX = 60, 40
NEXT_ACTION_STALE_DAYS, WAITING_STALE_DAYS = 7, 14
IMPERATIVE_RE = re.compile(r"\b(you must|you should always|you must never|always do|never do|do not ever)\b", re.I)
STEP_SEQ_RE = re.compile(r"(?:^|\n)\s*(?:\d+\.|-)\s+\S.*(?:\n\s*(?:\d+\.|-)\s+\S.*){3,}")


def rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


def problem(msg): problems.append(msg)
def warn(msg): warnings.append(msg)


def check_claude_md():
    p = ROOT / "CLAUDE.md"
    if not p.exists():
        problem("CLAUDE.md missing"); return
    text = p.read_text(encoding="utf-8")
    n = len(text.splitlines())
    if n > CLAUDE_MAX_LINES:
        problem(f"CLAUDE.md is {n} lines (cap {CLAUDE_MAX_LINES}); move procedure to a skill or facts to data")
    people = {f.stem for f in (ROOT / "people").glob("*.md") if not is_generated(f)}
    for slug in people - {"gordon"}:  # the principal is named in the kernel by design
        name = slug.replace("-", " ")
        if len(name) > 5 and re.search(r"\b" + re.escape(name) + r"\b", text, re.I):
            problem(f"CLAUDE.md names a person from people/ ({slug}); names belong in personal/me/brief.md")


def check_capped(path: Path, cap: int):
    if path.exists():
        n = len(path.read_text(encoding="utf-8").splitlines())
        if n > cap:
            problem(f"{rel(path)} is {n} lines (cap {cap})")


def check_focus():
    f = ROOT / "FOCUS.md"
    if not f.exists():
        warn("FOCUS.md missing (fine before scaffold completes)"); return
    horizon = None
    for ln in f.read_text(encoding="utf-8").splitlines():
        if ln.startswith("## "):
            horizon = ln[3:].strip()
        m = re.match(r"\s*(work|personal)\s*:\s*(.*)$", ln, re.I)
        if m and horizon:
            items = [x.strip() for x in m.group(2).split("·") if x.strip() and not x.strip().startswith("(")]
            if len(items) > FOCUS_CAP:
                problem(f"FOCUS.md {horizon} {m.group(1)}: {len(items)} items (cap {FOCUS_CAP})")


def check_headers_and_layers():
    for dirpath, _, files in walk(ROOT):
        for fn in files:
            p = dirpath / fn
            r = rel(p)
            if p.suffix == ".md":
                if is_generated(p) or r in ("CLAUDE.md", "FOCUS.md", "README.md") or r.startswith("_setup/templates/"):
                    continue
                fm, body = read_frontmatter(p)
                if not fm:
                    problem(f"{r}: no frontmatter (every data file needs name/type/description/lobe)"); continue
                for k in ("name", "type", "description"):
                    if not fm.get(k):
                        problem(f"{r}: frontmatter missing `{k}`")
                if not fm.get("lobe") and not r.startswith(("skills/", "_setup/")):
                    problem(f"{r}: frontmatter missing `lobe`")
                t = str(fm.get("type") or "")
                if t in ("client", "partner", "stakeholder", "guidelines", "knowledge", "summary", "person", "business", "doc"):
                    for m in IMPERATIVE_RE.finditer(body):
                        problem(f"{r}: data file contains an instruction to Claude ('{m.group(0)}'); describe the preference instead"); break
                if t == "person" and not r.startswith("people/"):
                    problem(f"{r}: type: person outside people/ (one identity per person)")
                if t == "skill":
                    check_skill(p, fm, body)
                if t in ("idea",) and not fm.get("next_review"):
                    problem(f"{r}: idea without next_review")
                if t == "project":
                    check_project(p, fm)
                if r.startswith("_queue/") or t in ("job", "idea", "lease", "note"):
                    pass  # state files: lifecycle checked by the watcher
            elif p.suffix == ".py" and r.startswith("_setup/") and not r.startswith("_setup/tests/"):
                fm, _ = read_frontmatter(p)
                for k in ("name", "type", "description", "why", "reads", "writes", "test"):
                    if k not in fm:
                        problem(f"{r}: script header missing `{k}`")


def check_skill(p: Path, fm: dict, body: str):
    r = rel(p)
    for k in ("triggers", "must_not_trigger", "reads", "writes", "test", "why"):
        if fm.get(k) in (None, "", [], {}):
            problem(f"{r}: skill header missing `{k}`")
    if fm.get("test") and not (ROOT / str(fm["test"])).exists():
        problem(f"{r}: test folder {fm['test']} does not exist")
    if not re.search(r"(?im)^\s*\d+\.\s*write\b", body) and "Receipt" not in body:
        problem(f"{r}: skill has no write step / receipt as its last step")
    if fm.get("shared") == "astra":
        if re.search(r"personal/", body):
            problem(f"{r}: shared skill reads from personal/")
    if re.search(r"routines/[\w-]+\.md", body):
        problem(f"{r}: skill reads an external guidance file; the procedure must live inside the skill")


def check_project(p: Path, fm: dict):
    r = rel(p)
    if fm.get("status") != "active":
        return
    na = fm.get("next_action") or {}
    text = na.get("text") if isinstance(na, dict) else None
    if not text:
        warn(f"{r}: active project with no next action")
    else:
        d = _date(na.get("set"))
        if d and (datetime.date.today() - d).days > NEXT_ACTION_STALE_DAYS:
            warn(f"{r}: next action unchanged for {(datetime.date.today() - d).days} days")
    for w in fm.get("waiting") or []:
        if isinstance(w, dict):
            d = _date(w.get("since"))
            if d and (datetime.date.today() - d).days > WAITING_STALE_DAYS:
                warn(f"{r}: waiting on {w.get('who')} for {(datetime.date.today() - d).days} days")


def _date(v):
    try:
        return datetime.date.fromisoformat(str(v)[:10]) if v else None
    except Exception:
        return None


def check_generated_integrity():
    mf = ROOT / "_setup" / "index-manifest.json"
    if not mf.exists():
        warn("no index manifest yet; run build-index first"); return
    files = json.loads(mf.read_text(encoding="utf-8")).get("files", {})
    for r, h in files.items():
        p = ROOT / r
        if not p.exists():
            continue
        cur = hashlib.sha256(p.read_bytes()).hexdigest()
        if cur != h:
            problem(f"{r}: generated file edited by hand since last generation (regenerate; never edit)")


def check_commands_registry():
    cmd = ROOT / "_setup" / "commands.md"
    if not cmd.exists():
        warn("_setup/commands.md missing"); return
    listed = set()
    for ln in cmd.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*`?([\w.\-]+)`?\s*\|\s*`?([^|`]+?)`?\s*\|", ln)
        if m and m.group(1) not in ("command", "---"):
            listed.add(m.group(1))
            script = m.group(2).strip()
            if script and not script.startswith("-") and not (ROOT / script).exists():
                problem(f"commands.md: {m.group(1)} points at {script}, which does not exist")
    for p in (ROOT / "_setup").glob("*.py"):
        fm, _ = read_frontmatter(p)
        if fm.get("type") == "command" and not any(r for r in listed):
            warn(f"{rel(p)} is type: command but commands.md has no rows yet")


def check_conflict_copies():
    for dirpath, _, files in walk(ROOT):
        for fn in files:
            if "-CONFLICT-" in fn or "conflicted copy" in fn.lower():
                problem(f"{rel(dirpath / fn)}: sync conflict copy present (a second writer got in)")


def check_secrets():
    """Architecture §6.5: the Sync copy must be current. Runs only where the plaintext exists (the Mac)."""
    import os
    plain = Path(os.environ.get("SANCHO_SECRETS_PLAIN", Path.home() / ".config/sancho/env"))
    enc = Path(os.environ.get("SANCHO_SECRETS_AGE", Path.home() / "Sync/Sancho-Secrets/sancho.env.age"))
    if not plain.exists():
        return
    if not enc.exists():
        problem(f"secrets plaintext {plain} exists but {enc} does not; run sancho.lock-secrets")
    elif plain.stat().st_mtime > enc.stat().st_mtime + 1:
        problem(f"secrets plaintext {plain} is newer than {enc.name}; run sancho.lock-secrets in Terminal")


GORDON_CITE_RE = re.compile(r"\[gordon(?::[a-z]+)?\s+\d{4}-\d{2}-\d{2}[^\]]*\]")
QUOTE_RE = re.compile(r"[\"“”'‘’][^\"“”'‘’]{3,}[\"“”'‘’]|\bsaid\b|\bsays\b|\bdictated\b|\bverbatim\b")
INFER_WORDS_RE = re.compile(r"\b(probably|likely|presumably|I assume|must be|should be|inferred)\b", re.I)
WORLD_STATE_FIELDS = ("timezone", "city", "location", "rv_location", "address", "phone", "email", "birthday", "mbti", "revenue", "budget", "stake")


def check_stated_not_inferred():
    """Error 2026-09-30 (ERRORS.md #1): a session wrote inferred values under a [gordon date] cite.
    Mechanical form of the rule: a value carrying a [gordon …] cite on a world-state field must show
    Gordon's words (a quoted segment or 'said/dictated'), or be marked [inferred], or be `unknown`.
    Inference words next to a [gordon] cite are flagged outright."""
    for dirpath, _, files in walk(ROOT):
        for fn in files:
            p = dirpath / fn
            if p.suffix != ".md" or is_generated(p) or rel(p).startswith(("_setup/", "_design/", "skills/")):
                continue
            try:
                lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
            except Exception:
                continue
            for i, ln in enumerate(lines, 1):
                if not GORDON_CITE_RE.search(ln):
                    continue
                if INFER_WORDS_RE.search(ln) and "[inferred]" not in ln:
                    problem(f"{rel(p)}:{i}: inference words under a [gordon] cite; mark [inferred] or write `unknown`")
                    continue
                key = ln.split(":", 1)[0].strip().lower() if ":" in ln else ""
                if key in WORLD_STATE_FIELDS:
                    val = ln.split(":", 1)[1]
                    if "unknown" in val.lower() or "[inferred]" in val:
                        continue
                    if not QUOTE_RE.search(val):
                        problem(f"{rel(p)}:{i}: `{key}` cites [gordon] without his words; quote what he said, mark [inferred], or write `unknown`")


def check_errors_have_mechanisms():
    """Every entry in _setup/ERRORS.md must name a mechanism (a lint check or a test) and its test.
    'Won't do it again' is not an entry."""
    f = ROOT / "_setup" / "ERRORS.md"
    if not f.exists():
        return
    entries = [b for b in f.read_text(encoding="utf-8").split("\n## ")[1:]]
    for b in entries:
        head = b.splitlines()[0]
        if "mechanism:" not in b:
            problem(f"_setup/ERRORS.md '{head[:50]}': no `mechanism:` line; an error without a mechanism is prose")
        if "test:" not in b:
            problem(f"_setup/ERRORS.md '{head[:50]}': no `test:` line")
        else:
            m = re.search(r"test:\s*(\S+)", b)
            if m and not (ROOT / m.group(1).rstrip("/")).exists():
                problem(f"_setup/ERRORS.md '{head[:50]}': test path {m.group(1)} does not exist")


def main():
    check_claude_md()
    check_capped(ROOT / "personal" / "me" / "brief.md", BRIEF_MAX)
    check_capped(ROOT / "personal" / "me" / "watch.md", WATCH_MAX)
    check_focus()
    check_headers_and_layers()
    check_generated_integrity()
    check_commands_registry()
    check_conflict_copies()
    check_stated_not_inferred()
    check_errors_have_mechanisms()
    check_secrets()
    out = [f"# LINT\ngenerated {today()} by lint-layers.py\n", f"**{len(problems)} problems, {len(warnings)} warnings**\n"]
    out += ["## Problems (block the build)"] + [f"- {p}" for p in problems] + ["", "## Warnings"] + [f"- {w}" for w in warnings]
    (ROOT / "_setup" / "LINT.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    for p in problems: print("PROBLEM:", p)
    for w in warnings: print("warning:", w)
    print(f"lint-layers: {len(problems)} problems, {len(warnings)} warnings")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
