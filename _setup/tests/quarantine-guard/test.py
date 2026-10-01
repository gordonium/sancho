#!/usr/bin/env python3
"""
name: test-quarantine-guard
type: script
description: quarantine-guard.py against a temp home with fake legacy folders. A main-thread Read, Grep, Glob of a fenced path is refused; a subagent Read is allowed and logged; CLAUDE.md, tools/, _dmz/, .env and credential names are refused for both; so is every instruction file by nature (a renamed CLAUDE-SAFE-DO-NOT-USE.md and any name containing CLAUDE in any case, SKILL.md, *.skill, hooks/, skills/, settings*.json, *.prompt.md), by Read, Glob, Grep and the env gate, while look-alike names (skillful.md, webhooks.md, prompt.md, settings-notes.md) still reach a subagent; a Bash cat is refused for both (agent_id mode); a search that starts above a fenced folder is refused; a same-named mount elsewhere and a symlink count; paths outside the list and the bare word in a grep are untouched; the env fallback admits only a marked, plain Bash read; the real quarantine-paths.md lists the four seed folders; a missing list falls back to the seed; --install adds the hook once, keeps the other hooks and leaves a backup; the watcher's HEALTH section counts the day and lists main-thread refusals by time.
why: ERRORS.md #9: a main thread read gordon-os-v2 directly; the fence has to be proven, not promised.
reads: _setup/quarantine-guard.py, _setup/quarantine-paths.md, _setup/sancho-watcher.py, hook-input-documented.json (documented shape, not yet a capture)
writes: temp files only
test: (this is the test)
"""
import copy, datetime, importlib.util, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent.parent
GUARD = SRC / "quarantine-guard.py"
T = Path(tempfile.mkdtemp())
if not T.is_dir():
    print("test-quarantine-guard: FAIL: no temp dir"); sys.exit(1)
T = T.resolve()


def fail(msg):
    print("test-quarantine-guard: FAIL: " + msg)
    shutil.rmtree(T, ignore_errors=True)
    sys.exit(1)


# a fake home: two fenced folders, a mount of the same name elsewhere, a link into v2, and a normal folder
V2 = T / "home" / "Sync" / "Gordonium Enterprises Sync" / "gordon-os-v2"
V3 = T / "home" / "Php" / "jarvis-v3"
for d in (V2 / "people", V2 / "tools", V2 / "_dmz", V2 / "sub", V3, T / "mnt" / "gordon-os-v2", T / "sancho", T / "log"):
    d.mkdir(parents=True)
for f in (V2 / "people" / "peter.md", V2 / "CLAUDE.md", V2 / "sub" / "CLAUDE.md", V2 / "tools" / "spawn.sh", V2 / "_dmz" / "x.md",
          V2 / ".env", V2 / ".env.local", V2 / "sub" / "api_key.txt", V2 / "sub" / "server.pem", V3 / "notes.md",
          T / "mnt" / "gordon-os-v2" / "a.md", T / "sancho" / "ok.md"):
    f.write_text("x\n")
os.symlink(V2 / "people", T / "sancho" / "link")
PATHS = T / "paths.md"


def write_paths(discriminator):
    PATHS.write_text("## Paths\n- `%s`\n- `%s`\n\n## Discriminator\ndiscriminator: `%s`\n" % (V2, V3, discriminator))


FIX = json.loads((HERE / "hook-input-documented.json").read_text())
ENV = {**os.environ, "SANCHO_QUARANTINE_PATHS": str(PATHS), "SANCHO_QUARANTINE_LOG_DIR": str(T / "log"), "HOME": str(T / "home")}
ENV.pop("SANCHO_QUARANTINE_READER", None)


def run(who, tool, tool_input, cwd=None, env=None):
    """Returns 'refused' or 'passed'."""
    hook = copy.deepcopy(FIX[who])
    hook["tool_name"], hook["tool_input"], hook["cwd"] = tool, tool_input, str(cwd or T / "sancho")
    r = subprocess.run([sys.executable, str(GUARD)], input=json.dumps(hook), capture_output=True, text=True, env=env or ENV, timeout=20)
    if r.returncode != 0:
        fail("guard exited %s on %s %s: %s" % (r.returncode, tool, tool_input, r.stderr[-300:]))
    if not r.stdout.strip():
        return "passed"
    out = json.loads(r.stdout)["hookSpecificOutput"]
    if out["permissionDecision"] != "deny" or "QUARANTINE GUARD" not in out["permissionDecisionReason"]:
        fail("odd answer: " + r.stdout)
    return "refused"


def expect(want, who, tool, tool_input, label, **kw):
    got = run(who, tool, tool_input, **kw)
    if got != want:
        fail("%s: wanted %s, got %s" % (label, want, got))


log = T / "log" / "quarantine-access.log"
write_paths("agent_id")
f = str(V2 / "people" / "peter.md")

# --- the two cases the fence exists for
expect("refused", "main", "Read", {"file_path": f}, "main-thread Read of a v2 file")
expect("passed", "subagent", "Read", {"file_path": f}, "subagent Read of the same file")
lines = log.read_text().splitlines()
if len(lines) != 2 or "\trefused\tmain\tRead\t" not in lines[0] or "\tallowed\tsubagent\tRead\t" not in lines[1] or f not in lines[0]:
    fail("access log after one refusal and one allowed read: %r" % lines)
probe = [json.loads(l) for l in (T / "log" / "quarantine-probe.log").read_text().splitlines()]
if len(probe) != 2 or "agent_id" in probe[0]["keys"] or probe[1]["agent_id"] != FIX["subagent"]["agent_id"] or "tool_input" in probe[1]:
    fail("probe log: %r" % probe)

# --- never read by anyone
for who in ("main", "subagent"):
    for p in (V2 / "CLAUDE.md", V2 / "sub" / "CLAUDE.md", V2 / "sub" / "claude.md", V2 / "tools" / "spawn.sh", V2 / "_dmz" / "x.md",
              V2 / ".env", V2 / ".env.local", V2 / "sub" / "api_key.txt", V2 / "sub" / "server.pem", V2 / "sub" / "id_rsa"):
        expect("refused", who, "Read", {"file_path": str(p)}, "%s Read of %s" % (who, p.relative_to(V2)))
    expect("refused", who, "Glob", {"pattern": "**/CLAUDE.md", "path": str(V2)}, who + " Glob for CLAUDE.md")
    expect("refused", who, "Grep", {"pattern": "x", "path": str(V2 / "tools")}, who + " Grep of tools/")
    # Bash is no way in for anyone while subagents are recognised by agent_id
    expect("refused", who, "Bash", {"command": "cat '%s'" % f}, who + " Bash cat of a v2 file")

# --- instruction files by nature: refused for everyone, renamed or not [gordon 2026-10-01]
INSTRUCTION_FILES = ("CLAUDE-SAFE-DO-NOT-USE.md", "sub/claude-safe-do-not-use.md", "sub/old-Claude.txt", "sub/NOTCLAUDE", ".claude/commands/go.md",
                     "SKILL.md", "sub/skill.md", "sub/ingest.skill", "sub/INGEST.SKILL", "hooks/pre.sh", "sub/hooks/notes.md", "sub/Hooks/notes.md",
                     "skills/open/readme.md", "sub/skills/x.md", "settings.json", "sub/settings.local.json", "sub/settings-old.json",
                     "sub/Settings.JSON", "sub/open.prompt.md", "sub/OPEN.PROMPT.MD")
for name in INSTRUCTION_FILES:
    (V2 / name).parent.mkdir(parents=True, exist_ok=True)
    if not (V2 / name).exists():  # the Mac's disk folds capitals: sub/Hooks is sub/hooks
        (V2 / name).write_text("x\n")
for who in ("main", "subagent"):
    for name in INSTRUCTION_FILES:
        expect("refused", who, "Read", {"file_path": str(V2 / name)}, "%s Read of %s" % (who, name))
    expect("refused", who, "Read", {"file_path": str(T / "mnt" / "gordon-os-v2" / "CLAUDE-SAFE-DO-NOT-USE.md")}, who + " Read of a renamed CLAUDE file in a same-named mount")
    expect("refused", who, "Read", {"file_path": str(V3 / "skills" / "x" / "SKILL.md")}, who + " Read of a v3 skill")
    for pattern in ("**/*CLAUDE*", "**/claude-safe*.md", "**/SKILL.md", "**/*.skill", "hooks/**", "skills/**/*.md", "**/settings*.json", "**/*.prompt.md"):
        expect("refused", who, "Glob", {"pattern": pattern, "path": str(V2)}, "%s Glob for %s" % (who, pattern))
    expect("refused", who, "Glob", {"pattern": str(V2) + "/**/CLAUDE-SAFE-DO-NOT-USE.md"}, who + " Glob with the folder and the renamed file in the pattern")
    for folder in ("hooks", "skills", ".claude"):
        expect("refused", who, "Grep", {"pattern": "x", "path": str(V2 / folder)}, "%s Grep of %s/" % (who, folder))
    expect("refused", who, "Grep", {"pattern": "x", "path": str(V2), "glob": "*.prompt.md"}, who + " Grep narrowed to prompt files")
    expect("refused", who, "Grep", {"pattern": "x", "path": str(V2 / "CLAUDE-SAFE-DO-NOT-USE.md"), "output_mode": "content"}, who + " Grep of the renamed CLAUDE file")
last = log.read_text().splitlines()[-1].split("\t")
if last[1:4] != ["refused", "subagent", "Grep"] or "CLAUDE in its name" not in last[5]:
    fail("a refused instruction file must be logged with its reason: %r" % last)
# names that only look alike are ordinary files: a subagent still reads them, a main thread still does not
for name in ("sub/skillful.md", "sub/webhooks.md", "sub/prompt.md", "sub/settings-notes.md", "sub/skill-list.md"):
    (V2 / name).write_text("x\n")
    expect("passed", "subagent", "Read", {"file_path": str(V2 / name)}, "subagent Read of %s" % name)
    expect("refused", "main", "Read", {"file_path": str(V2 / name)}, "main Read of %s" % name)

# --- main thread: every other door
expect("refused", "main", "Read", {"file_path": str(V3 / "notes.md")}, "main Read of v3")
expect("refused", "main", "Grep", {"pattern": "peter", "path": str(V2)}, "main Grep of v2")
expect("refused", "main", "Glob", {"pattern": "**/*.md", "path": str(V2)}, "main Glob of v2")
expect("refused", "main", "Glob", {"pattern": str(V2) + "/**/*.md"}, "main Glob with the folder in the pattern")
expect("refused", "main", "Grep", {"pattern": "peter", "path": str(V2.parent)}, "main Grep starting above v2")
expect("refused", "main", "Read", {"file_path": str(T / "mnt" / "gordon-os-v2" / "a.md")}, "main Read of a same-named mount")
expect("refused", "main", "Read", {"file_path": str(T / "sancho" / "link" / "peter.md")}, "main Read through a symlink into v2")
expect("refused", "main", "Read", {"file_path": "../home/Sync/Gordonium Enterprises Sync/gordon-os-v2/people/peter.md"}, "main Read by relative path")
expect("refused", "main", "Read", {"file_path": "~/Sync/Gordonium Enterprises Sync/GORDON-OS-V2/people/peter.md"}, "main Read with ~ and capitals")
expect("refused", "main", "Read", {"file_path": "people/peter.md"}, "main Read of a plain name while standing in v2", cwd=V2)
for c in ("cat %s" % f.replace(" ", "\\ "), 'head -5 "$HOME/Sync/Gordonium Enterprises Sync/gordon-os-v2/people/peter.md"',
          "ls ~/Sync/Gordonium\\ Enterprises\\ Sync/gordon-os-v2", "cd /somewhere && grep -rn peter gordon-os-v2/people",
          "ls /sessions/abc/mnt/jarvis-v3"):
    expect("refused", "main", "Bash", {"command": c}, "main Bash: " + c)
expect("refused", "main", "Bash", {"command": "ls"}, "main Bash while standing in v2", cwd=V2 / "people")

# --- subagent: what is and is not allowed
expect("passed", "subagent", "Glob", {"pattern": "**/*.md", "path": str(V2)}, "subagent Glob of v2")
expect("passed", "subagent", "Grep", {"pattern": "peter", "path": str(V2)}, "subagent Grep of v2 for file names")
expect("passed", "subagent", "Grep", {"pattern": "peter", "path": f, "output_mode": "content"}, "subagent Grep of one file for lines")
expect("refused", "subagent", "Grep", {"pattern": "peter", "path": str(V2), "output_mode": "content"}, "subagent Grep of the folder for lines")
expect("refused", "subagent", "Grep", {"pattern": "peter", "path": str(V2.parent)}, "subagent Grep starting above v2")

# --- not our business: nothing said, nothing logged
before = len(log.read_text().splitlines())
expect("passed", "main", "Read", {"file_path": str(T / "sancho" / "ok.md")}, "Read outside the list")
expect("passed", "main", "Grep", {"pattern": "gordon-os-v2", "path": str(T / "sancho" / "ok.md")}, "Grep for the word in a Sancho file")
expect("passed", "main", "Glob", {"pattern": "*.md", "path": str(T / "log")}, "Glob in another folder")
expect("passed", "main", "Bash", {"command": 'grep -rn "gordon-os-v2" _setup skills'}, "Bash grep for the bare word")
expect("passed", "main", "Bash", {"command": "ls ~/Sync/Sancho && git status", "description": "not about gordon-os-v2/ at all"}, "Bash elsewhere (description is not checked)")
expect("passed", "main", "Write", {"file_path": str(T / "sancho" / "new.md"), "content": "v2 said: see gordon-os-v2/people"}, "Write of a note that mentions the folder")
if len(log.read_text().splitlines()) != before:
    fail("calls outside the list were logged")
r = subprocess.run([sys.executable, str(GUARD)], input="not json", capture_output=True, text=True, env=ENV)
if r.returncode != 0 or r.stdout.strip():
    fail("unreadable input must pass silently")

# --- the env fallback: Read/Grep/Glob shut for all; only a marked, plain Bash read gets in, logged with its first 80 chars
write_paths("env")
expect("refused", "subagent", "Read", {"file_path": f}, "env mode: subagent Read")
expect("refused", "main", "Bash", {"command": "cat '%s'" % f}, "env mode: unmarked Bash")
marked = "SANCHO_QUARANTINE_READER=1 cat '%s'" % f
expect("passed", "subagent", "Bash", {"command": marked}, "env mode: marked Bash cat")
last = log.read_text().splitlines()[-1].split("\t")
if last[1:4] != ["allowed", "env-gate", "Bash"] or last[4] != marked[:80]:
    fail("env-gate log line: %r" % last)
for name in INSTRUCTION_FILES:
    expect("refused", "subagent", "Bash", {"command": "SANCHO_QUARANTINE_READER=1 cat '%s'" % (V2 / name)}, "env mode: marked cat of " + name)
    expect("refused", "subagent", "Read", {"file_path": str(V2 / name)}, "env mode: subagent Read of " + name)
expect("refused", "subagent", "Bash", {"command": "SANCHO_QUARANTINE_READER=1 ls '%s/hooks'" % V2}, "env mode: marked ls of hooks/")
# the way TO the fenced folder is not judged by name: a parent folder that is itself called "claude" does not shut the gate
CV2 = T / "claude" / "gordon-os-v2"
(CV2 / "people").mkdir(parents=True); (CV2 / "people" / "peter.md").write_text("x\n"); (CV2 / "CLAUDE-SAFE-DO-NOT-USE.md").write_text("x\n")
PATHS.write_text("## Paths\n- `%s`\n\n## Discriminator\ndiscriminator: `env`\n" % CV2)
expect("passed", "subagent", "Bash", {"command": "SANCHO_QUARANTINE_READER=1 cat '%s'" % (CV2 / "people" / "peter.md")}, "env mode: marked cat under a parent folder named claude")
expect("refused", "subagent", "Bash", {"command": "SANCHO_QUARANTINE_READER=1 cat '%s'" % (CV2 / "CLAUDE-SAFE-DO-NOT-USE.md")}, "env mode: renamed CLAUDE file under a parent folder named claude")
PATHS.write_text("## Paths\n- `%s`\n\n## Discriminator\ndiscriminator: `agent_id`\n" % CV2)
expect("passed", "subagent", "Read", {"file_path": str(CV2 / "people" / "peter.md")}, "subagent Read under a parent folder named claude")
expect("refused", "subagent", "Read", {"file_path": str(CV2 / "CLAUDE-SAFE-DO-NOT-USE.md")}, "renamed CLAUDE file under a parent folder named claude")
write_paths("env")
for c in ("cat '%s/CLAUDE.md'" % V2, "cat '%s'/people/*" % V2, "grep -rn peter '%s'" % V2, "cat '%s/tools/spawn.sh'" % V2, "cat '%s/.env'" % V2):
    expect("refused", "subagent", "Bash", {"command": "SANCHO_QUARANTINE_READER=1 " + c}, "env mode: marked " + c)

# --- the real list names the four seed folders; a missing list falls back to them
spec = importlib.util.spec_from_file_location("qg", GUARD); qg = importlib.util.module_from_spec(spec)
os.environ.pop("SANCHO_QUARANTINE_PATHS", None); spec.loader.exec_module(qg)
qg.PATHS_FILE = str(SRC / "quarantine-paths.md")
roots, disc = qg.load_config()
want = [os.path.normpath(os.path.expanduser(p)) for p in qg.SEED_PATHS]
if roots != want or disc not in ("agent_id", "env"):
    fail("real quarantine-paths.md: %r %r" % (roots, disc))
qg.PATHS_FILE = str(T / "missing.md")
if qg.load_config() != (want, "agent_id"):
    fail("a missing list must fall back to the seed paths")

# --- --install: once, beside the hooks already there, with a backup
S = T / "settings.json"
S.write_text(json.dumps({"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "live-site-guard"}]}]}, "theme": "dark"}))
IENV = {**ENV, "SANCHO_CLAUDE_SETTINGS": str(S)}
if subprocess.run([sys.executable, str(GUARD), "--check"], capture_output=True, env=IENV).returncode != 1:
    fail("--check says registered before install")
for _ in range(2):
    if subprocess.run([sys.executable, str(GUARD), "--install"], capture_output=True, env=IENV).returncode != 0:
        fail("--install failed")
s = json.loads(S.read_text()); pre = s["hooks"]["PreToolUse"]
if len(pre) != 2 or pre[0]["hooks"][0]["command"] != "live-site-guard" or s["theme"] != "dark" or "quarantine-guard.py" not in pre[1]["hooks"][0]["command"] \
        or not all(t in pre[1]["matcher"].split("|") for t in ("Read", "Grep", "Glob", "Bash")):
    fail("settings after install: %r" % s)
if len(list(T.glob("settings.json.bak-*"))) != 1:
    fail("install must leave exactly one backup")
if subprocess.run([sys.executable, str(GUARD), "--check"], capture_output=True, env=IENV).returncode != 0:
    fail("--check says not registered after install")

# --- HEALTH.md: the day's count, main-thread refusals by time, and whether the hook is registered
tree = T / "tree"; (tree / "_setup").mkdir(parents=True); (tree / "_queue" / "log").mkdir(parents=True); (tree / "CLAUDE.md").write_text("")
os.environ["SANCHO_ROOT"], os.environ["SANCHO_STATE"] = str(tree), str(T / "state")
spec = importlib.util.spec_from_file_location("w", SRC / "sancho-watcher.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
now = datetime.datetime.now().astimezone().replace(microsecond=0)
yesterday = now - datetime.timedelta(days=1)
(tree / "_queue" / "log" / "quarantine-access.log").write_text("".join("\t".join(r) + "\n" for r in [
    [yesterday.isoformat(), "refused", "main", "Read", "/old/gordon-os-v2/y.md", "a main thread never reads a legacy folder"],
    [now.isoformat(), "refused", "main", "Read", "/x/gordon-os-v2/people/peter.md", "a main thread never reads a legacy folder"],
    [now.isoformat(), "allowed", "subagent", "Read", "/x/gordon-os-v2/people/peter.md", "subagent read"],
    [now.isoformat(), "allowed", "subagent", "Grep", "/x/gordon-os-v2", "subagent read"],
    [now.isoformat(), "refused", "subagent", "Read", "/x/gordon-os-v2/CLAUDE.md", "never"],
]))
os.environ["SANCHO_CLAUDE_SETTINGS"] = str(T / "nosettings.json")
problems, section = w.quarantine_section(now)
text = "\n".join(section)
if "## Quarantine reads" not in text or "today: 2 allowed, 2 refused" not in text or "1 from a main thread" not in text:
    fail("HEALTH section counts: " + text)
if "- refused, main thread, %s: Read /x/gordon-os-v2/people/peter.md" % now.strftime("%H:%M") not in text or "/old/" in text:
    fail("HEALTH section must list today's main-thread refusal by time, and only today's: " + text)
if problems:
    fail("no guard script in the temp tree, so no registration problem expected: %r" % problems)
shutil.copy(GUARD, tree / "_setup" / "quarantine-guard.py")
problems, section = w.quarantine_section(now)
if not any("not registered" in p for p in problems) or "NOT registered" not in "\n".join(section):
    fail("an unregistered guard must be a HEALTH problem: %r" % problems)
os.environ["SANCHO_CLAUDE_SETTINGS"] = str(S)
problems, section = w.quarantine_section(now)
if problems or "guard registered" not in "\n".join(section):
    fail("a registered guard must not be a problem: %r %r" % (problems, section))

shutil.rmtree(T, ignore_errors=True)
print("test-quarantine-guard: PASS")
