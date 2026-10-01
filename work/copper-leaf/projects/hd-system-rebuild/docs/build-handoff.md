---
name: Home Directions v4 build handoff
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: What the build thread starts from: the inputs to read, the scope Gordon authorised for the first unattended run, the rules that bind it, the facts about this Mac it needs, what it must not touch, when it must stop, and what it leaves for Gordon in the morning
sources: ["[gordon 2026-10-01]", "[doc:plan-v2.md]", "[doc:laravel-kit-spec.md]", "[doc:requirements.md]", "[doc:phase0-brief.md]", "[doc:hosting-options.md]"]
status: written by the planning thread on 2026-10-01 night; takes effect only once Gordon has approved plan-v2.md and said to start
---
# Build handoff: from the planning thread to the build thread

Gordon: "please warn me before you start writing any real code ... we'll want to ... start a new 'actually write it' thread separate from this planning thread." And: "let our limits rest for 5 hours, then cut loose on a clean slate to do the build." [gordon 2026-10-01]

You are that clean slate. You have no memory of the planning conversation. Everything decided is on disk; read it before doing anything.

## 1. Read first, in this order
All under `/Users/gordonium/Sync/Sancho/work/copper-leaf/projects/hd-system-rebuild/`:
1. `docs/plan-v2.md`: what is being built, every decision, the build order (steps A to J).
2. `docs/laravel-kit-spec.md`: the kit. Sections 2 (decisions; D1, D3, D5, D8 were changed by Gordon after draft 2, and the text says how), 5, 7, 8 and 14.
3. `docs/requirements.md`: R1 to R9.
4. `docs/phase0-brief.md`, the Decisions section and "Plan questions 4 onward": Gordon's exact words.
5. `docs/hosting-options.md`, the Decision section: one server, the backup schedule.
6. `docs/census-2026-10-01.md` and `docs/census-part2-2026-10-01.md`: what the data is, for the data model and the import.
7. `/Users/gordonium/Sync/Sancho/CLAUDE.md`: who Gordon is and the must-nevers. `handoff.md` in the project folder: this project's rules.
The WordPress kit at `/Users/gordonium/Dev/clc-plugins/` (its `CLAUDE.md`, `skills/`, `bin/`, `docs/HANDOFF-plugin-dev-workflows.md`) is the model the Laravel kit is built to match. Read it; do not change it.

## 2. What this run is authorised to do
Steps A and C of `plan-v2.md` section 7, and, if those are finished and green, steps D, E and F **against fakes only**.

- **A. The kit's first slice**, in a new local git repository at `/Users/gordonium/Dev/clc-laravel/` (kit files at the top level, as the WordPress kit is laid out): the rules file; the shell guard for the Forge host with its tests; the plan-gate and model-and-effort hooks as scripts with tests; the gate script; the ship script; the project template; the skills `laravel-plan`, `laravel-write-plan`, `laravel-code`, `laravel-review`, `laravel-ship`; the per-project file template and its lint; the lessons file seeded per the spec; the parity ledger seeded from `docs/wp-kit-map.md`; an installer that prints what Gordon must do and changes nothing by itself.
- **C. The app skeleton**, in a new local git repository at `/Users/gordonium/Dev/clc-laravel/hdonline-v4/`: Laravel at the versions in the spec; the tables in `plan-v2.md` section 4; logins for three people; Dashboard and File with entry by hand and the duplicate prompts; tests.
- **D, E, F against fakes:** letters, invoices and mail, Calendly, each behind one wrapper class with a fake, fully tested without the network. No real Google, Brevo or Calendly account exists for this app yet; do not look for credentials.

The plan Gordon approved is the plan for this run. Before each step, write that step's own short plan into the job file (what you will build, in what order, how it is tested), then code, then review. Gordon is asleep; he approved the scope, not each line. Anything outside the scope above waits for him.

## 3. Rules that bind this run
- **Idiomatic, elegant Laravel.** The WordPress Readability Rule does not apply. [gordon 2026-10-01]
- **Tests are automatic and must pass before a step is called done.** Never claim "tested" without a test that ran. [Sancho must-never 9]
- **Model and effort:** Gordon wants real code written at the top setting. This prompt carries his keyword for multi-agent work. State at the start of your first message which model you are; you cannot see your effort level, so say that too.
- **Independent review before a step is called done:** the kit spec's five review questions, by agents that did not write the code, with fixes and a rerun.
- **Local only.** No server exists. No pushes: there are no remotes, and creating GitHub repositories is Gordon's. Commit locally, small commits, clear messages.
- **Do not register hooks.** Do not edit `/Users/gordonium/.claude/settings.json` or anything under `/Users/gordonium/.claude/`. Build the hook scripts and their tests; registration is Gordon's step, from the installer's printed instructions. A broken hook would block every session on this Mac.
- **Do not touch** `/Users/gordonium/Dev/clc-plugins/` (it has uncommitted guard fixes awaiting Gordon), any SiteDistrict server, the dev clone, v2, or anything under `~/Sync/` except writing this project's own notes (below). No legacy data work: that is Phase 2.
- **No client data in any repository.** The census numbers are in the docs; real rows are not to be copied anywhere.
- **Install nothing new** beyond what Composer and npm pull in for the project itself. If a tool is missing, write down what is needed and stop that step.
- **Cite and record.** Write what you did, with evidence, into `/Users/gordonium/Sync/Sancho/work/copper-leaf/projects/hd-system-rebuild/docs/build-log.md` as you go (create it with the same frontmatter shape as the other docs). Add one dated line to `project.md` Notes at the end. Touch nothing else in the Sancho tree: another thread owns `_setup/`, `_queue/`, `_design/`, `skills/`.

## 4. This Mac
- PHP: Laravel Herd is installed. As of 2026-10-01 23:42 its setup was unfinished: only `"/Users/gordonium/Library/Application Support/Herd/bin/php84"` (PHP 8.4.25) existed there, with no Composer and nothing on the PATH. Check that folder first. The plan calls for PHP 8.5; if only 8.4 is present, build on 8.4 with the code written to run on 8.5, and say so in the log.
- **If Composer is not available, step C cannot start.** Do step A's parts that need no PHP (the guard, the hooks, the scripts, the rules, the skills, the ledger), write down exactly what Gordon needs to do in Herd, and stop.
- Node 26 and npm 11 are installed. SQLite 3.51 is installed. Homebrew is at `/opt/homebrew/bin/brew` (use it for nothing without Gordon).
- The live-site guard hook is active on this Mac and reads every shell command. A command that mentions ssh and a SiteDistrict server will be refused; you have no reason to write one.
- Gordon is travelling on a metered connection. Composer and npm installs are fine; no large downloads beyond them.

## 5. Stop when
- a step's tests cannot be made to pass after an honest attempt: write what fails and stop that step;
- something needs an account, a password, a key, or a decision not in the documents;
- you would have to go outside section 2 to continue;
- steps A and C (and D to F if reached) are done.
Do not start step B, G, H, I or J.

## 6. Leave for Gordon
At the top of `docs/build-log.md`, a short summary he can read in a minute: what is built and passing, what is not, what you need from him (in order), and the exact commands to see it running locally. Then the detail.

Things already known to be waiting on him, which you should not try to do: finish Herd's setup and add PHP 8.5; create the two private repositories in the Copper Leaf organisation; create the Forge and DigitalOcean accounts and the server; Cloudflare storage for backups; the Brevo key; the Calendly connection; the Google credential and the letters folder; put the letterhead and signature images into the letter template; register the kit's hooks; decide whether to commit the WordPress guard fix.
