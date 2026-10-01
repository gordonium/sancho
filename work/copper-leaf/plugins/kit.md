---
name: Copper Leaf plugin dev kit
type: doc
business: copper-leaf
lobe: work
status: active
description: The rules, three skills and safety scripts every Copper Leaf plugin job runs through; repo at ~/Dev/clc-plugins
sources: ["[doc:~/Dev/clc-plugins/README.md]", "[doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md]", "[doc:~/Dev/clc-plugins/CLAUDE.md]"]
---
# Copper Leaf plugin dev kit

Registry entry built 2026-10-02 (batch B4). Sancho orchestrates the kit and never absorbs it; plugin work happens in Claude Code [doc:~/Sync/Sancho/CLAUDE.md]. Read-only summary; the kit's files win.

## What it is
- "The rules, skills and safety scripts that every Copper Leaf WordPress plugin job runs through"; the same folder is the parent for plugin clones, each its own git repo, ignored by the kit repo [doc:~/Dev/clc-plugins/README.md:3]
- Repo: `git@github.com:CopperLeafCreative/clc-plugin-dev-kit.git`, private, branch `main`, on GitHub since 2026-09-22 [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md:247]
- Must stay at `~/Dev/clc-plugins/`: the hooks, the LaunchAgent, the skill symlinks and CLAUDE.md auto-loading all depend on that path [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md:322]
- `CLAUDE.md` is the Copper Leaf WordPress Development Rules (plan, approval, memory, implement; migrations; Readability Rule; security; safety; release flow; staging; review chain; lessons) [doc:~/Dev/clc-plugins/README.md:7] [doc:~/Dev/clc-plugins/CLAUDE.md:19-184]
- `docs/HANDOFF-plugin-dev-workflows.md` (written 2026-09-21 for Sancho): the workflows, tooling, safety mechanisms, decisions and known gaps [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md:3-5]
- Two deliberate choices: no `gh` CLI, so nothing on the machine can create a Release by accident; clones live outside any file-sync folder [doc:~/Dev/clc-plugins/README.md:26-29]

## Release flow (five lines)
1. Sites update through Plugin Update Checker plus the Copper Leaf Updates Handler, which watches GitHub Releases on private `CopperLeafCreative` repos; pushing commits or tags does not ship [doc:~/Dev/clc-plugins/CLAUDE.md:136]
2. Quick fixes commit on `master`; multi-day or might-be-abandoned work uses `feature/<short-name>` and merges before release [doc:~/Dev/clc-plugins/CLAUDE.md:139]
3. Bump every version location, write the `release-notes.txt` entry newest on top, tag `vX.Y.Z`, push branch then tag [doc:~/Dev/clc-plugins/CLAUDE.md:141-149]
4. Claude never creates, drafts or publishes the Release; it hands Gordon the tag and the release-notes text, and Gordon publishes on github.com [doc:~/Dev/clc-plugins/CLAUDE.md:150]
5. After publishing: confirm a site sees the update, smoke test, check the error log; rollback is re-releasing the previous tag [doc:~/Dev/clc-plugins/CLAUDE.md:151]

## Skills (run in this order)
- `plugin-edit`: "Start and carry out work on a Copper Leaf WordPress plugin or theme the safe, repeatable way - preflight the git repo, connect to the SiteDistrict staging site over SSH, investigate, plan, implement, deploy to staging and test." [doc:~/Dev/clc-plugins/skills/plugin-edit/SKILL.md:3]
- `plugin-review`: "The pre-ship review chain for Copper Leaf WordPress plugins - three independent reviews (backward compatibility, security, performance) run in parallel on the uncommitted or unmerged change, then fixes, retest and re-review until they pass." [doc:~/Dev/clc-plugins/skills/plugin-review/SKILL.md:3]
- `plugin-ship`: "Ship a finished, tested and reviewed Copper Leaf WordPress plugin change - version bump, release-notes.txt entry, final staging parity check, commit, tag, push, hand Gordon the GitHub Release text, post-release checks, rollback guidance, the "competent human developer" time estimate, and memory cleanup." [doc:~/Dev/clc-plugins/skills/plugin-ship/SKILL.md:3]

## bin tools
- `install-mac.sh`: "set up the Copper Leaf plugin dev kit on a Mac" (links the skills, checks the hooks, installs the hourly backup) [doc:~/Dev/clc-plugins/bin/install-mac.sh:3]
- `sitedistrict-live-site-guard.py`: "a safety gate that Claude cannot skip" (PreToolUse hook) [doc:~/Dev/clc-plugins/bin/sitedistrict-live-site-guard.py:3]
- `sitedistrict-live-site-guard-tests.py`: "Tests for sitedistrict-live-site-guard.py"; a second hook runs them whenever the guard is edited [doc:~/Dev/clc-plugins/bin/sitedistrict-live-site-guard-tests.py:3] [doc:~/Dev/clc-plugins/README.md:12]
- `wip-backup.sh`: "protect unfinished plugin work from hardware failure" (hourly snapshots to `wip/<machine>/<branch>`; never touches master, tags or Releases) [doc:~/Dev/clc-plugins/bin/wip-backup.sh:3]

## config (examples only, no secrets)
- `claude-settings-hooks.json` (the hooks block), `com.copperleaf.wip-backup.plist.example` (the LaunchAgent), `ssh-config.example` (the `~/.ssh/config` pattern), `staging-error-log-probe.php` (temporary probe that proves where PHP errors land on a staging site) [doc:~/Dev/clc-plugins/README.md:16] [doc:~/Dev/clc-plugins/config/staging-error-log-probe.php:2-4] [doc:~/Dev/clc-plugins/CLAUDE.md:162]

## Live-site guard (two lines)
- On SiteDistrict hosts only `~/sites` folders whose name ends with `.sitedistrict.com` are staging; every other folder is a live client site, and a PreToolUse hook refuses any ssh/rsync/scp command that could touch one, default block [doc:~/Dev/clc-plugins/CLAUDE.md:158] [doc:~/Dev/clc-plugins/bin/sitedistrict-live-site-guard.py:8-15]
- Commands must open with `cd ~/sites/<staging-folder>/... &&` and chain with `&&` only (rule added 2026-10-01; 86 tests); if it blocks, stop and tell Gordon, never rephrase around it [doc:~/Dev/clc-plugins/CLAUDE.md:158] [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md:125]

## Staging aliases named in the kit (names only)
- `copperleaf-dev`, `filmadelphia-dev` (host-5), `artspeak-staging`, `wizardacademy-dev` (host-2), `govartshow-dev` (host-12), as of 2026-09-21 [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md:63]

## Open threads (from the handoff)
- Leah's Windows machine has no guard, backup job or skills yet; a Claude Code plugin bundling the skills and hooks is the suggested delivery [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md:251]
- The guard covers only SiteDistrict; any other host needs its own boundary rule [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md:252]
- Skills untested beyond the pilot; descriptions not trigger-optimised [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md:253]
- Per-plugin CLAUDE.md coverage is thin (most of ~50 have none) [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md:255]
- Tag hygiene audit (header vs tag vs Release) suggested across repos [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md:256]
- Rules section 1 step 3 still says "save to memory"; the decision is that plans live in Markdown files, and the rule is to be repointed [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md:247] [doc:~/Dev/clc-plugins/CLAUDE.md:25]
