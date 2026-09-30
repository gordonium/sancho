#!/usr/bin/env python3
"""
name: build-map
type: command
description: Regenerate MAP.md, the living map, in three zoom levels: Level 0 the system (one Mermaid diagram, ≤8 boxes), Level 1 components per box, Level 2 wiring tables (reads/writes/triggers/tests/commands/retired). Built only from frontmatter, commands.md and git; no hand-kept registry. Fails if a component has no parsable header or a reads/writes/chain target does not exist.
why: If Gordon can't see it, he loses track of it (post-mortem). A component not on the map is not done; a map nobody regenerates is v2's dashboard.
reads: every .md/.py under the tree (frontmatter only), _setup/commands.md, FOCUS.md, _setup/LINT.md, _setup/TESTS.md, _setup/retired/, git log
writes: MAP.md at the tree root
schedule: last step of every map build (after lint and build-index); nightly
test: _setup/tests/build-map/
"""
from __future__ import annotations
import sys, re, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sancho_lib import tree_root, read_frontmatter, walk, today, is_generated

ROOT = tree_root()
errors: list[str] = []


def rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


def collect():
    skills, commands, scripts, entities, projects = [], [], [], [], []
    for dirpath, _, files in walk(ROOT):
        for fn in files:
            p = dirpath / fn
            if p.suffix == ".md" and not is_generated(p) and not rel(p).startswith("_setup/templates/"):
                fm, _ = read_frontmatter(p)
                t = fm.get("type")
                if t == "skill":
                    skills.append((rel(p), fm))
                elif t in ("client", "partner", "stakeholder", "business"):
                    entities.append((rel(p), fm))
                elif t == "project":
                    projects.append((rel(p), fm))
            elif p.suffix == ".py" and rel(p).startswith("_setup/") and not rel(p).startswith("_setup/tests/"):
                fm, _ = read_frontmatter(p)
                if not fm.get("name"):
                    errors.append(f"{rel(p)}: no parsable header; not on the map, so not done")
                (commands if fm.get("type") == "command" else scripts).append((rel(p), fm))
    return skills, commands, scripts, entities, projects


def read_commands_table():
    rows = []
    f = ROOT / "_setup" / "commands.md"
    if f.exists():
        for ln in f.read_text(encoding="utf-8").splitlines():
            if ln.startswith("|") and not ln.startswith("|---") and "command" not in ln.split("|")[1].lower():
                rows.append(ln)
    return rows


def check_targets(items):
    for r, fm in items:
        for key in ("reads", "writes"):
            for tgt in fm.get(key) or []:
                t = str(tgt).split(" ")[0].strip("`")
                if t.startswith(("work/", "personal/", "people/", "skills/", "recordings/", "_setup/", "_queue/")) and "<" not in t and "*" not in t:
                    if not (ROOT / t.rstrip("/")).exists() and not (ROOT / t).parent.exists():
                        errors.append(f"{r}: {key} target {t} does not exist")


def level0() -> str:
    return """```mermaid
flowchart LR
  CAP[Capture: Plaud · Zoom · calendar · dictation]
  PIPE[Pipeline on the Mac: fetch → transcribe → diarize → voiceprint]
  LAND[Landing zone: recordings/inbox]
  ING[Ingest: a session, 7 GTD buckets]
  TREE[(The tree: spine · work · personal)]
  SES[Sessions: Cowork · Claude Code · phone via Dispatch]
  Q[Queue + Mac: commands · schedules · watcher]
  OUT[Outputs: indexes · MAP · STATUS · Pushover]
  CAP --> PIPE --> LAND --> ING --> TREE
  SES <--> TREE
  SES --> Q --> PIPE
  Q --> OUT
  TREE --> OUT
```"""


def level1(skills, commands, entities, projects) -> str:
    out = []
    # tree
    out.append("### The tree\n```mermaid\nflowchart TB\n  S[spine: CLAUDE.md · people · skills · recordings · _queue · _setup]\n  W[work]\n  P[personal]\n  S --> W\n  S --> P")
    for b in sorted({e[0].split("/")[1] for e in entities if e[0].startswith("work/")} | {d.name for d in (ROOT / "work").iterdir() if d.is_dir() and not d.name.startswith(("_", ".")) and d.name not in ("ice", "reviews")}):
        out.append(f"  W --> W_{b.replace('-', '_')}[{b}]")
    for a in sorted(d.name for d in (ROOT / "personal").iterdir() if d.is_dir() and not d.name.startswith(("_", ".")) and d.name not in ("ice", "reviews")):
        out.append(f"  P --> P_{a.replace('-', '_')}[{a}]")
    out.append("```")
    # skills by family
    fam = {}
    for r, fm in skills:
        name = Path(r).parent.name
        f = "thinking" if name in ("think-first", "critical-thinking", "triz", "punnett-square", "brief-me", "fact-check-anyone") else \
            "gtd" if name in ("weekly-review", "ice-review", "open", "work-morning", "personal-morning") else \
            "ingest" if name in ("earballs-ingest", "attribution-correction", "write-it-down", "zoom-filing") else "other"
        fam.setdefault(f, []).append((name, fm))
    out.append("### Skills by family\n```mermaid\nflowchart LR")
    for f, items in sorted(fam.items()):
        out.append(f"  subgraph {f}")
        for name, fm in items:
            out.append(f"    {name.replace('-', '_')}[{name}]")
        out.append("  end")
    for r, fm in skills:
        ch = fm.get("chain") or {}
        if isinstance(ch, dict):
            nxt = ch.get("next")
            if nxt:
                out.append(f"  {Path(r).parent.name.replace('-', '_')} --> {str(nxt).split(' ')[0].replace('-', '_')}")
    out.append("```")
    # pipeline
    out.append("### Pipeline stages\n```mermaid\nflowchart LR\n  A[1 Plaud fetch 5-min] --> B[2 download + ledger] --> D[4 Groq transcribe] --> E[5 diarize + embed] --> F[6 voiceprint match] --> G[7 transcript + speakers.md] --> H[8 STATUS.md]\n  C[5b calendar feed] --> E\n  Z[Zoom poll] --> G\n  H --> I[9 ingest skill]\n  W[10 watchdog] -.-> H\n```")
    # projects
    if projects:
        out.append("### Active projects\n")
        for r, fm in projects:
            if fm.get("status") == "active":
                na = fm.get("next_action") or {}
                out.append(f"- **{fm.get('name')}** ({fm.get('lobe')}/{fm.get('area')}) · next: {na.get('text') if isinstance(na, dict) else na}")
    return "\n".join(out)


def level2(skills, commands, scripts) -> str:
    out = ["<details><summary>Skills: triggers, reads, writes, tests</summary>\n", "| skill | lobe | triggers | must not | reads | writes | test |", "|---|---|---|---|---|---|---|"]
    for r, fm in skills:
        out.append(f"| {Path(r).parent.name} | {fm.get('lobe')} | {', '.join(map(str, fm.get('triggers') or []))} | {', '.join(map(str, fm.get('must_not_trigger') or []))} | {', '.join(map(str, fm.get('reads') or []))} | {', '.join(map(str, fm.get('writes') or []))} | {fm.get('test')} |")
    out += ["\n</details>\n", "<details><summary>Commands and schedules (from _setup/commands.md)</summary>\n"]
    out += read_commands_table() or ["(none registered yet)"]
    out += ["\n</details>\n", "<details><summary>Scripts</summary>\n"]
    for r, fm in scripts + commands:
        out.append(f"- `{r}` · {fm.get('description')}")
    out += ["\n</details>\n"]
    for name in ("LINT.md", "TESTS.md"):
        f = ROOT / "_setup" / name
        if f.exists():
            out.append(f"<details><summary>{name}</summary>\n\n" + f.read_text(encoding="utf-8") + "\n</details>\n")
    retired = sorted(d.name for d in (ROOT / "_setup" / "retired").iterdir()) if (ROOT / "_setup" / "retired").exists() else []
    out.append("<details><summary>Retired (90 days)</summary>\n\n" + ("\n".join(f"- {r}" for r in retired) or "(none)") + "\n</details>")
    return "\n".join(out)


def changed_this_week() -> str:
    try:
        out = subprocess.run(["git", "log", "--since=7.days", "--name-only", "--format="], cwd=ROOT, capture_output=True, text=True, timeout=10).stdout
        files = sorted({l for l in out.splitlines() if l.strip()})
        return "\n".join(f"- {f}" for f in files[:60]) + (f"\n- … +{len(files)-60} more" if len(files) > 60 else "") or "- (no commits in the last 7 days)"
    except Exception:
        return "- (git unavailable)"


def main():
    skills, commands, scripts, entities, projects = collect()
    check_targets(skills)
    focus = (ROOT / "FOCUS.md").read_text(encoding="utf-8") if (ROOT / "FOCUS.md").exists() else "(no FOCUS.md yet)"
    doc = [f"# Sancho · MAP\ngenerated {today()} by build-map.py. Three zoom levels; Level 0 is the picture to remember.\n",
           "## FOCUS\n", focus.strip(), "\n## Level 0 · the system\n", level0(),
           "\n## Level 1 · components\n", level1(skills, commands, entities, projects),
           "\n## Changed this week\n", changed_this_week(),
           "\n## Level 2 · wiring\n", level2(skills, commands, scripts)]
    if errors:
        doc.append("\n## BUILD ERRORS\n" + "\n".join(f"- {e}" for e in errors))
    (ROOT / "MAP.md").write_text("\n".join(doc) + "\n", encoding="utf-8")
    for e in errors: print("ERROR:", e)
    print(f"build-map: MAP.md written; {len(skills)} skills, {len(commands)} commands, {len(errors)} errors")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
