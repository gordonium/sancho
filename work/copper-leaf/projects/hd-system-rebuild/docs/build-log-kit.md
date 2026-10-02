---
name: Home Directions v4 build log, kit track
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: What the kit track of the overnight build planned and did, stage by stage, with the test commands and their pass and fail numbers; the kit is the Laravel development kit at ~/Dev/clc-laravel/
sources: ["[doc:build-handoff.md]", "[doc:laravel-kit-spec.md]", "[doc:guard-check-2026-10-01.md]", "[doc:wp-kit-map.md]", "[doc:~/Dev/clc-plugins/, read only]", "[web:code.claude.com/docs/en/hooks, read 2026-10-02 through a summarising fetch tool]", "[gordon 2026-10-02]"]
status: live during the build that started 2026-10-02 00:55; each stage adds its plan first and its evidence after
---
# Build log: kit track

The kit lives at `/Users/gordonium/Dev/clc-laravel/`, kit files at the top level. Each stage below has its plan (written before any code) and then what was done, with evidence.

## Stage K1: scaffold and both guards

Started 2026-10-02 01:00 CEST. Builder: Claude, model Fable 5.1 (`claude-fable-5-1`). I cannot see my own effort level. Scope: items 2 and 3 of section 14 of `laravel-kit-spec.md`. Nothing from item 4 onward.

### Plan (written before coding)

**What will exist at the end.**

1. A git repository at `~/Dev/clc-laravel/` whose `.gitignore` ignores everything except the kit's own files. So every project folder is ignored, `hdonline-v4/` first. I never read, touch or stage anything inside `hdonline-v4/`.
2. `CLAUDE.md`: the kit's rules file. The same twelve sections and numbering as the WordPress kit. Every rule carries a short ID in a comment (`L-<section>.<number>`). A dated change list at the foot.
3. `templates/project-CLAUDE.md`: the per-project file, with the headings of spec section 12.
4. `LESSONS.md`: the ten lessons the spec names for day one, each with its incident, date, rule, the test or hook that catches it, and whether it applies to the other kit. Where the catching test is not built yet, the lesson says so.
5. `parity/ledger.md`: about 70 rows, one per capability, seeded from `wp-kit-map.md`. Five columns as the spec sets them.
6. `bin/kit-lint.py`: three checks. The per-project file has every heading, in order, and the "not reachable from this machine" sentence. Every rule ID in the rules file is in the ledger, and the ledger cites no ID that does not exist. Every lesson has all five parts.
7. The guards, on one shared core (decision D10):
   - `bin/guard_core.py`: the shared rules. It reads its host lists from `config/guard-rules.json`: staging aliases and app roots, production hosts, the two production addresses that may be read, hosts left to another guard (GitHub, SiteDistrict), and the panel addresses that are always refused. No Forge host exists yet, so the real file's staging and production lists are empty.
   - `bin/production-guard.py`: the shell guard. Lettered rules. Default is to refuse.
   - `bin/browser-guard.py`: the browser guard. Refuses the Forge panel, the DigitalOcean console, GitHub settings, Actions and branch pages, and the production app, by address.
   - `bin/guard-wrapper.sh`: the command a hook would run. It turns a crash, a missing Python or a hang into a refusal, because Claude Code lets a command through when a hook crashes or times out (checked against the hook documentation tonight).
   - `bin/guard-selftest.sh`: runs the guard tests when a guard file changes, whether the change came from an edit tool or from the shell.
   - `bin/check-registration.py`: says whether the three hooks are registered, by reading the settings file. It changes nothing.
8. `bin/install-mac.sh`: prints what Gordon must do. It writes nothing, links nothing, registers nothing.
9. `config/claude-settings-hooks.json`: the hooks block for Gordon to merge, as an example. Not registered by me.
10. `docs/HANDOFF-laravel-dev-kit.md`: the kit's handoff, with a line for each build step done.
11. `bin/test-all.sh`: one command that runs every test.

**The shell guard's rules, in short** (spec section 8.3).
- The program is seen as `ssh` or by full path, in any capitals. The same for `scp`, `rsync`, `sftp`.
- The destination must be exactly a listed staging alias. Anything else is refused, unknown hosts included. Hosts on the "left to another guard" list are not this guard's business.
- A production host named anywhere in a shell command is refused. The one exception is a plain read of one of the two listed addresses.
- A staging command starts with `cd <staging app root> &&`. After that: no `;`, no `||`, no single `&`, no line break. No `..`, no `~`, no variables in paths, no absolute paths outside the app root, no sftp, one remote command per call, no custom remote program, no bare login.
- Verbs: after the `cd`, each piece must start with a program on a short list. This is what closes case H3 of the guard check, which a path checker cannot. On top of that the spec's list is refused by name: the test runners, tinker, `db:seed`, the database shell, `migrate:fresh`, `migrate:refresh`, `migrate:reset`, `db:wipe`, and `migrate:rollback` (always, until job files exist to record Gordon's say).
- Refused everywhere: the `forge` program, `gh`, any deploy-hook address, the Forge address. Inside a kit project: a bare `git push`, `--all`, `--mirror`, `--tags`, and any push that names `main` or a tag.
- It fails closed: input it cannot read is refused.

**Order of work.**
1. `git init`, `.gitignore`, `.gitattributes`. Commit.
2. Guard core, shell guard and its first test file (the eight cases of the guard check first). Commit when green.
3. Browser guard and tests. Commit.
4. Wrapper, self-test, registration check, their tests, the example hooks block. Commit.
5. Rules file, per-project template, lessons, ledger, the lint and its tests. Commit.
6. Installer and its test (it must leave every file as it found it). Handoff document. Commit.
7. Run everything once more from a clean state; record the numbers here.

**How it is tested.**
- Python's built-in test runner only. Nothing is installed.
- Every guard test hands the guard a pretend command as text, with its own made-up rules file and its own made-up SSH config in `tests/fixtures/`. Host names are invented. Nothing contacts a server. Nothing depends on this Mac's SSH config or settings.
- The eight guard-check cases (and its three controls) are the first cases in `tests/test_shell_guard.py`.
- The real rules file has its own test: no production host may be on any allow list.
- The wrapper is tested against stand-in guards that crash, hang, print rubbish or are missing.
- The installer test runs it with a pretend home folder and proves no file changed.
- Example ssh and rsync commands live in the test files only, never on my own command line, because this Mac's live-site guard reads every command I run.

**What I will not do.** Register a hook. Edit anything under `~/.claude/`. Install anything. Push, or add a remote. Touch `~/Dev/clc-plugins/` or `hdonline-v4/`. Start the gate script, the ship script, the skills or the plan-gate hooks.

**Checked before coding** (hook documentation, read 2026-10-02 through a summarising fetch tool, one reader): a hook blocks only by an explicit deny or by exit code 2; any other exit code, and a timeout, let the command through; a matcher made only of letters, digits, `_`, `-` and `|` is an exact list, and anything else is a regular expression; the hook's input carries the working folder (`cwd`); managed settings can carry hooks. One thing for stage K3: the documentation says the hook input also carries the session's effort level. That would let the model-and-effort check be read by a hook, not only confirmed by Gordon. Unconfirmed until tried.

### What was done

**K1 is built, tested and committed. Finished 2026-10-02 01:48 CEST. 614 automatic tests, all pass. Nothing is registered, installed, pushed or switched on.**

**The test command and its result.**

```
bash /Users/gordonium/Dev/clc-laravel/bin/test-all.sh
```

Result: `Ran 614 tests in 16.542s`, `OK`, exit code 0. Failures 0, errors 0, skipped 0.

| Test file | Tests | What it covers |
|---|---|---|
| `tests/test_shell_guard.py` | 456 | the shell guard: 444 pretend commands in 13 tables, and 12 tests through the real program |
| `tests/test_browser_guard.py` | 47 | the browser guard: 43 pretend actions, and 4 through the real program |
| `tests/test_real_rules.py` | 13 | the real rules file: no production host on any allow list |
| `tests/test_guard_wrapper.py` | 19 | the wrapper, against guards that crash, hang, print rubbish or are missing |
| `tests/test_guard_selftest.py` | 7 | the self-test runs after any change, and not when nothing changed |
| `tests/test_registration_check.py` | 19 | registered, half registered and unregistered settings files |
| `tests/test_kit_lint.py` | 48 | the per-project file, the ledger and the lessons lint |
| `tests/test_installer.py` | 5 | the installer prints and changes nothing |

Three more checks, each run once by hand tonight:
- **From a clean copy.** The repository was cloned into a scratch folder and the tests run there with the home folder pointed at an empty folder. Result: 614 tests, OK. The empty home folder was still empty afterwards and the clone had no new files. So the tests do not depend on this Mac's SSH config or settings.
- **The tests notice a missing rule.** Each main rule of the guard was switched off in turn and the 487 table cases rerun. Every time, cases failed: 12 with rule N off, 21 with the production rule off, 50 with the push rule off, 98 with the remote-command rules off, 2 at the fewest. With nothing switched off, 0 fail.
- **End to end with the real rules file.** The wrapper was fed four hook-shaped inputs: `git status` passed in silence; `gh release create` was refused (rule W); `git push origin main` from inside a project was refused (rule Y); opening the Forge panel was refused (rule X).

The lint on the kit's own documents: `python3 bin/kit-lint.py all` says template ok, ledger ok (97 rows, 124 rule IDs, 35 gaps in WordPress, 2 gaps in Laravel), lessons ok (10 lessons, 7 with no test or hook yet, each naming the build step that brings one).

**What exists now**, all under `/Users/gordonium/Dev/clc-laravel/`:

| Path | What it is |
|---|---|
| `.gitignore`, `.gitattributes` | everything is ignored except the kit's own files; `hdonline-v4/` is named first |
| `CLAUDE.md` | the rules: the WordPress kit's twelve sections, 124 rules, each with an ID, a change list at the foot |
| `templates/project-CLAUDE.md` | the per-project file, nineteen fixed headings |
| `LESSONS.md` | ten lessons, five parts each |
| `parity/ledger.md` | 97 rows comparing the two kits |
| `bin/kit-lint.py` | the three lints |
| `bin/guard_core.py` | the rules of both guards, lettered, explained at the top |
| `bin/production-guard.py`, `bin/browser-guard.py` | the two guards |
| `bin/guard-wrapper.sh` | what a hook would run; turns a broken guard into a refusal |
| `bin/guard-selftest.py` | reruns the tests after any change to the kit |
| `bin/check-registration.py` | reads the settings file and says whether the three hooks are registered |
| `bin/install-mac.sh` | prints what Gordon must do; changes nothing |
| `bin/test-all.sh` | the one test command |
| `config/guard-rules.json` | the real host list: no staging alias and no production host yet |
| `config/claude-settings-hooks.json` | the hooks block for Gordon to merge; an example, not registered |
| `docs/HANDOFF-laravel-dev-kit.md` | the kit's handoff, with a line for steps 2 and 3 |
| `tests/` | the tests and their made-up fixtures |

**Commits.** 8, local only, on `main`. Last: `26a0dbc` (full: `26a0dbcaa6702a54e6a0e6e86daed592ee9df791`). No remote exists. The working tree is clean.

**The guard check of 2026-10-01.** Its three controls and eight holes are the first table in `tests/test_shell_guard.py` (14 cases). They are carried over shape for shape, with made-up names: the WordPress guard draws its line at a folder name, this guard at an exact alias and an app root. All eight holes are refused here, H3 included (an account-wide command after a valid `cd`), which the WordPress guard still allows by design.

**Where I went beyond the letter of the spec.** Each is written up in the kit handoff, section 5, for the reviewers and for Gordon.
1. After the `cd`, a remote command must start with a program on a short allowed list. A list of bad words alone cannot close H3.
2. Some hosts are left to another guard: GitHub and SiteDistrict. Without that list, the spec's "refuse any unknown destination" would stop `ssh -T git@github.com` and every WordPress staging job, because the hooks run for every session on this Mac. Checked tonight: those two are the only hosts this Mac's SSH config points at (domains counted, nothing else read out).
3. The push rule applies only inside a kit project. The WordPress kit pushes `master` and tags by design.
4. `scp` and `rsync` may only copy from staging, and only its logs. Staging holds real client data.
5. The server's `.env` is not read or copied.
6. `migrate:rollback` is always refused for now. The spec's exception needs job files, which come in stage K3.
7. A production host named in any shell command is refused, even in a commit message. Strict on purpose.
8. The text of a commit message written the usual way (a here-document handed to `cat`) is not read as commands. Inside `bash -c` or `eval` it is.

**Not done, and why.**
- Nothing is registered. That is Gordon's step; `bin/install-mac.sh` prints it.
- The real rules file has no staging alias and no production host. No Forge server exists.
- "Whether a network allow-list around the agent's shell covers SSH" (spec 8.3, last line) was not tested. It needs a change to settings, which this run may not make.
- The hook facts were read in the documentation, not tried with a live hook, because no hook is registered.
- The WordPress rules file has no rule IDs, so the ledger cites it by file and line. Adding IDs there is a proposal for Gordon.
- The hourly backup does not cover `~/Dev/clc-laravel/`. That waits for the filter, which is a change to the WordPress kit's script.
- No README. The kit handoff carries the "what is where" list.

**Refused by the app's safety check:** nothing.

**Untouched, checked at the end.** `~/.claude/settings.json` was last changed on 2026-10-01 21:23, before this run. `~/Dev/clc-plugins/` shows the same five uncommitted files as before. Nothing inside `hdonline-v4/` was read, changed or staged. Nothing else was written in the Sancho tree.

**For stage K2 and K3.**
- K2's ship script must be the only thing that pushes `main`; the guard already refuses the rest (rule Y). The script's own `git push` is not seen by the guard, because the guard reads the command Claude types, not what a script does.
- K3 should add the `migrate:rollback` exception (job file records Gordon's say), run `bin/check-registration.py` and `bin/kit-lint.py project` from the preflight, and check which user the staging alias in `~/.ssh/config` points at.
- Any new rule in `CLAUDE.md` needs a new ID and a ledger row, or `bin/test-all.sh` fails.
- Editing anything under `bin/`, `config/`, `tests/`, `templates/`, `parity/`, or `CLAUDE.md` and `LESSONS.md`: run `bash bin/test-all.sh` afterwards. The self-test would do it by itself once registered; it is not registered.

## Stage K2: the gate, the ship script and the project template

Started 2026-10-02 01:55 CEST. Builder: Claude, model Fable 5.1 (`claude-fable-5-1`). I cannot see my own effort level. Scope: items 4 and 5 of section 14 of `laravel-kit-spec.md`. Nothing from item 6 onward (no skills, no hooks, no updates calendar). K1's guard files are not changed; anything I need there is written below as a request.

### Plan (written before coding)

**What will exist at the end**, all under `~/Dev/clc-laravel/`:

1. `bin/gate.py`: the gate. It lives in the kit, so a change in an app cannot loosen it. It is handed a project folder and:
   - refuses to run unless the folder is a git repository with a clean working tree, and records the commit it ran on;
   - runs, in the spec's order: clear the cached config; Pint in check mode; Larastan; the tests (architecture tests included), counting passed, failed and skipped from the test runner's own report file; `composer audit --locked`;
   - then the migration checks of rules L-2.2 and L-2.3: no migration file that is already on `main` has changed, and every migration runs up, down and up again on a throwaway SQLite database, with nothing left behind after the down;
   - judges every step by its exit code, and checks afterwards that the tools changed no file;
   - lists "controls changed": every change in the branch to the files that control the gate (the analyser config and its baseline, the formatter config, the test config, the audit ignore list, the CI workflow, the bot config, `.gitignore`, the deploy script, and the kit's own test files in the project), and any drop in the number of tests or rise in skipped ones against the gate's record for `main`;
   - writes its record outside the tree it certifies: under the repository's `.git` folder, one file per commit. (The spec's review found that a gate which writes into the tree cannot certify the commit it ran on.)
   - Exit codes: 0 green; 1 a check failed; 2 it could not run; 3 green, but controls changed, which needs Gordon's yes before ship.
   - Which PHP it runs is chosen on the kit side (an option or an environment variable), never by a file in the app.
2. `bin/ship.py`: the release gate of decision D2. The only thing that moves `main`. In order:
   - refuses unless: the tree is clean; the branch is `feature/...` or `updates/...`; it descends from the remote's `main`; the version file holds a version higher than `main`'s; the change log has an entry for it; the tag does not exist; the job file records a passing review of a commit that differs from this one only in the version file, `CHANGELOG.md` and `.kit/jobs/`, and that commit has a passing gate record; the job file records Gordon's "ship it"; and, if controls changed, his yes to that;
   - reruns the gate on this exact commit;
   - pushes the branch and moves the `staging` pointer to it, waits until staging itself reports this commit, and takes the parity proof (staging's commit equals this one, staging says it is staging, no migration pending, the health address answers, the tree is still clean);
   - reads production's version line, then pushes `main` (a fast-forward only) and the tag together, then watches production's version line: if it moves, deploy-on-push is on, and the script stops with its own exit code and tells Gordon;
   - prints the hand-over of rule L-9.11 and stops. It never deploys. Gordon presses Deploy.
   - `--dry-run` does every check and pushes nothing.
3. `templates/laravel-new/`: the project template, as files laid out the way they sit in a project, with a manifest:
   - architecture tests (no `dd` or `dump`, no `env()` outside config, no database facade in controllers, plus Pest's own presets);
   - the three isolation measures: the stray-request switch in the base test case; a test config with the in-memory mailer, the in-process queue and dummy credentials, with a test that fails if any credential the tests can see is not a dummy; an architecture test with the list of wrapper classes, forbidding any other HTTP client;
   - lazy-loading prevention and the destructive-command switch, in one service provider, with tests;
   - the log probe: an artisan command and a web variant, both absent in production, with a test that asserts it;
   - the version line: one `VERSION` file, an address that needs no login and serves version and commit, and a command that gives staging's status in one call;
   - `deploy.sh`: the one deploy script (backup first on production and stop if it fails; install with package scripts off; build assets; refuse to migrate if the SQLite file is missing; migrate; record the commit; keep its output where it can be read);
   - the CI workflow (the gate's steps on the four branch patterns, on pull requests and nightly; never on `wip/`; no secret);
   - the bot config (Dependabot: Composer and npm grouped weekly, Actions separately; nothing merges by itself);
   - `pint.json`, `phpstan.neon`, the required `.gitignore` entries, `.gitattributes`, `CHANGELOG.md`, `.kit/project.json`, `.kit/jobs/`, and the per-project `CLAUDE.md` from K1's template.
4. `bin/laravel-new.py`: lays the template over a fresh Laravel project. By default it only lists what it would do; `--apply` does it. It never runs Composer, git or the network; it prints those steps.
5. `bin/check-project.py`: says whether a project has every piece of the template, one named line per piece. Reads only.
6. `bin/prove-template.sh`: an optional proof with real PHP: makes a real Laravel project in a temporary folder, lays the template over it, and runs the real gate on it. It needs Composer and so is not part of the everyday test run.
7. Tests, added to `bin/test-all.sh` (same runner, same folder): `tests/test_gate.py`, `tests/test_ship.py`, `tests/test_project_template.py`, `tests/test_deploy_script.py`.
8. The kit handoff, `LESSONS.md` (the "not built yet" lines that these steps bring) and the ledger rows that say "not built: step 4" or "step 5", brought up to date.

**Order of work.** Gate and its tests; commit. Ship and its tests; commit. Template files, `laravel-new`, `check-project` and their tests; commit. Deploy script tests; commit. The proof with real PHP, once; fix what it finds; commit. Documents; commit. Full run from a clean copy; numbers here.

**How it is tested.**
- Python's built-in test runner, as K1. Nothing installed.
- The gate and the ship script are tested against throwaway git repositories made inside each test, in a temporary folder, with a throwaway bare repository standing in for GitHub. PHP, Composer, the staging server and production's version address are stand-ins the tests control, so every outcome can be produced: a red formatter, a failing test, fewer tests than `main`, a changed control file, an edited old migration, a `down()` that leaves a table behind, staging that never moves, production that moves by itself.
- The template is tested by laying it over a made-up fresh project and checking each piece by name; then each piece is removed in turn and the check must name it.
- The deploy script is run for real, as a shell script, against stand-in `php`, `composer` and `npm` programs, to prove the order of its steps and that it stops where it must.
- No test touches `hdonline-v4/` or any real project. I read its `composer.json`, test config and tests layout to make the template fit.
- No ssh or rsync command appears on my own command line; staging is a stand-in program inside the tests.

**What I will not do.** Register a hook. Edit anything under `~/.claude/`. Install anything with Homebrew. Push, or add a remote to the kit. Change K1's guard files. Write, stage or run anything in `hdonline-v4/`, or read its environment files. Start the skills, the plan-gate hooks or the updates calendar.

### What was done

**K2 is built, tested and committed. Finished 2026-10-02 03:20 CEST. 894 automatic tests, all pass (K1's 614 and 280 new). On top of that, the template, the gate and the deploy script were proved once with real PHP on a real Laravel project made for the purpose: 43 checks, all pass. Nothing is registered, installed, pushed or switched on.**

**The test command and its result.**

```
bash /Users/gordonium/Dev/clc-laravel/bin/test-all.sh
```

Result at the last commit (`00c07f8`): `Ran 894 tests in 163.239s`, `OK`, exit code 0. Failures 0, errors 0, skipped 0. The run takes about two minutes forty now, not sixteen seconds, because the new tests start real programs against real git repositories.

| Test file | Tests | What it covers |
|---|---|---|
| K1's eight files | 614 | unchanged, still passing (one assertion in `tests/test_kit_lint.py` now accepts an eleventh lesson) |
| `tests/test_gate.py` | 72 | the gate against throwaway repositories: green, each red step, what stops it from starting, the migration checks, controls changed, numbers of tests against `main` |
| `tests/test_ship.py` | 84 | the ship script against a throwaway repository with a bare repository standing in for GitHub: 12 ships that must succeed, a dry run, 32 refusals before any push, staging that misbehaves, production that moves by itself |
| `tests/test_project_template.py` | 87 | the template laid over a copy of a fresh Laravel project's stock files: each piece is there; each piece taken away or hollowed out is named by the check |
| `tests/test_deploy_script.py` | 37 | the deploy script run for real against stand-in programs: the order of its steps, and every place it must stop |

No test touches a real project. PHP, Composer, npm and the staging server are played by one stand-in the tests control (`tests/fixtures/standin.py`); staging's health address and production's version line by a small web server inside the test.

**Four more checks, each run by hand tonight.**

- **From a clean copy.** The repository was cloned into a scratch folder and the tests run there with the home folder pointed at an empty folder. Result: 894 tests, OK. The empty home folder was still empty afterwards and the clone had no new files.
- **The tests notice a missing check.** In a scratch copy, 39 checks of the gate and the ship script were switched off one at a time and the tests rerun. 38 made at least one test fail. The one that did not was the ship script's own clean-tree check: the gate refuses a dirty tree too, and the test accepted either message. That test was tightened and now fails with the check off. So: 39 of 39.
- **The proof with real PHP** (`bin/prove-template.py`; PHP 8.5.10, Laravel 13.34.0, Pest 5.3.0, Larastan 3.12.2, Pint 1.32.1; run three times, the last on the committed kit): 43 checks, all pass.
  - A fresh Laravel project was made with Composer in a scratch folder, the template laid over it, `composer update` run, and Pint run once. Pint changed none of the template's own files. `check-project.py` found all 15 pieces.
  - The real gate was green on it: 44 tests, 0 failed, 0 skipped; Larastan at level 8 found nothing; `composer audit` found nothing; every migration ran up, down and up.
  - 21 deliberate changes were then made, one at a time, each on its own branch, and the real gate run on each. 19 were breakages, and the gate gave the right answer at the right step for every one: the stray-request switch taken out; the log probe let into production (command, then route); the destructive commands let through; lazy loading allowed; a `dump()` left behind; `env()` outside config; a controller using the database facade; Guzzle used directly; curl used directly; a second class using a vendor's client beside the listed wrapper; a credential in the test config that is not a dummy; unformatted code; a type error; a failing test; a migration with an empty `down()`; an edited old migration; a deleted test (exit code 3: fewer tests than `main`); a skipped test (exit code 3: more skipped). 2 were harmless and were let through.
  - The deploy script was run for real as a staging site and as a production site (real PHP, Composer and SQLite; npm a stand-in, so nothing large was downloaded). It ran to its end, recorded the commit, and `php artisan kit:status` reported that commit with 0 pending migrations. On staging the log probe's token was found in Laravel's log twice and came out of `error_log`. On production the backup ran first and the copy was sound; the log probe's command and route did not exist; `migrate:fresh` was refused; and with no database to back up the deploy stopped at step 1 and changed nothing.
- **The lint on the kit's own documents**: `python3 bin/kit-lint.py all` says template ok, ledger ok (98 rows, 124 rule IDs, 36 gaps in WordPress, 2 gaps in Laravel), lessons ok (11 lessons, 5 with no test or hook yet, each naming the build step that brings one).

**The proof found a real fault, which is fixed.** The template's architecture rule against a second HTTP client was written as "not to be used in App" over a list of names. Pest reads that as "not all of them", so the rule passed with Guzzle used in the app, and every test was green. Only breaking a real project on purpose showed it. The rule is rewritten in the form that is checked name by name, a test refuses the broken form, and it is lesson LL-11 and ledger row C-98.

**What exists now**, all under `/Users/gordonium/Dev/clc-laravel/`:

| Path | What it is |
|---|---|
| `bin/gate.py` | the gate: clear the cached config, Pint, Larastan, the tests, `composer audit --locked`, then the two migration checks. It certifies a clean commit, keeps its record under the project's `.git` folder, and lists "controls changed". Exit codes 0, 1, 2, 3 |
| `bin/ship.py` | the ship script: the one thing that moves `main`. `--dry-run` does every check and pushes nothing. Exit codes 0, 1, 2, 4 |
| `bin/laravel-new.py` | lays the template over a fresh Laravel project. Lists by default; `--apply` does it; never runs Composer, git or the network |
| `bin/check-project.py` | says whether a project has every piece of the template, T1 to T15. Reads only |
| `bin/prove-template.py` | the proof with real PHP. Needs Composer, so it is not part of `bin/test-all.sh` |
| `bin/kit_repo.py` | shared pieces for those scripts |
| `templates/laravel-new/files/` | the template: 28 files laid out as they sit in a project |
| `tests/test_gate.py`, `test_ship.py`, `test_project_template.py`, `test_deploy_script.py`, `throwaway.py`, `fixtures/standin.py`, `fixtures/fresh-laravel/` | the tests and what they stand on |
| `docs/HANDOFF-laravel-dev-kit.md` | brought up to date: what each new script does, the lines the ship script reads from a job file, 18 choices made while building (numbers 11 to 28), what is unconfirmed, a line each for steps 4 and 5 |
| `CLAUDE.md`, `LESSONS.md`, `parity/ledger.md` | L-5.5 reworded, L-6.10 and L-9.4 name the scripts; three lessons now name the tests that catch them, four say why the template could not carry theirs, one lesson added; eleven ledger rows updated, one added |

**Commits.** 7 new, local only, on `main`, after K1's `26a0dbc`. Last: `00c07f8` (full: `00c07f8e09298434a0b9800d2e4745c096f35228`). No remote exists. The working tree is clean.

**Where I went beyond the letter of the spec, or settled something it left open.** Each is written up in the kit handoff, section 5, numbers 11 to 28. The ones that matter most:

1. The gate also runs the migration checks (spec section 4 gives them to the gate; its list in 5.1 does not), and on every migration, not only the new ones.
2. More files count as "controls" than the spec lists: the base test case, the test bootstrap, the kit's own tests in a project, `.kit/project.json`, and the list of Composer plugins that may run.
3. The ship script reads the review and Gordon's "ship it" from the job file, in three fixed line shapes. The job file's format is K3's; these three lines are what K3 must write, or change in one place in `bin/ship.py`. They are the agent's words, so that part is instruction. The arithmetic on top is mechanical: nothing but `VERSION`, `CHANGELOG.md` and `.kit/jobs/` may differ from the reviewed commit.
4. `migrate:rollback` is left usable. This settles the spec's open point: Laravel's one-line switch blocks rollback too (read in the framework's source, 13.34), and the way back of a release needs it. The template switches off the four commands that destroy a database, one by one. Rule L-5.5 was reworded to match.
5. The deploy script refuses a production site with debug on, a commit it cannot identify, and a missing or relative SQLite path. Its backup is a few lines of PHP of its own, because on a fresh release the packages are not installed yet and the backup must come first. It handles SQLite only and stops the deploy for any other database.
6. A fresh Laravel 13 project ships a `CLAUDE.md` and an `AGENTS.md` written for agents, which tell an agent to install programs. `laravel-new.py` replaces the first with the per-project file and removes the second (rule L-5.12).
7. The CI workflow repeats the gate's commands, because CI may hold no secret and so cannot fetch a private kit. `check-project.py` fails when the workflow drops one.

**For Gordon to decide or know.**

- **CI needs one third-party action**, `shivammathur/setup-php`, because GitHub's machines do not carry PHP 8.5. A new dependency is his say (L-6.4). It is in the template; nothing runs it until a repository exists.
- **Herd ships a program called `forge`** in its bin folder (`~/Library/Application Support/Herd/bin/forge`, seen tonight; not run). The kit relies on `forge` being absent. K1's installer reports it absent only because that folder is not on the plain PATH; it is on the PATH in a login shell. The guard refuses running it by name once registered.
- **The ship script reads staging's health address without a login.** If the login in front of staging covers `/up`, it stops there. How staging lets that one address through is his choice.
- **The very first push of `main` of a new project is his**, when he creates the repository. The ship script refuses when the remote has no `main`.

**Not done, and why.**

- Skills, the plan-gate hooks, the preflight, the updates calendar and its script: items 6 and 7, not this stage. `laravel-new.py` prints that the calendar entry is not built yet.
- Nothing here has met a real Forge site or GitHub. The ship script was tested against a bare repository on this Mac; the deploy script against real PHP but not against Forge's own deploy box. Whether Forge hands the script the commit is unconfirmed; if the commit cannot be found the script stops and says so.
- The gate compares numbers of tests only with a commit of `main` it has run on, on this Mac. With none it says so. The ship script reruns the gate on what it ships, so the record exists from the first ship on.
- The gate's up, down, up run is on SQLite.
- The template carries no browser test (the test browser is a per-project download, granted for Home Directions only) and no webhook or integration test (a fresh project has none). Lessons LL-1, LL-2, LL-3 and LL-9 say so and name step 6.
- `check-project.py` was not run on `hdonline-v4`: this stage may not run anything there. From the files I was allowed to read, the app was built before the template and does not carry its pieces under the template's names (no `tests/Feature/Kit/`, no `.kit/`, its architecture tests are in `tests/Arch/ArchTest.php`). Laying the template over it will show conflicts to settle by hand (`pint.json`, `phpstan.neon`). That is the app track's to do.

**Requests to other stages. I changed none of these files.**

- **Guard files: no change needed by this stage.** For the fix stage's information: the ship script runs one command on staging (`cd <app root> && php artisan kit:status`) and the log probe is `php artisan kit:log-probe`; both fit the guard's rules as they are.
- **`bin/guard-selftest.py`** runs the whole of `bin/test-all.sh` after any change to the kit. That now takes two minutes forty. Once registered, limiting it to the guard's own tests when only non-guard files changed would keep it usable.
- **`bin/install-mac.sh`** still says only the skills are missing, and looks for `forge` on the plain PATH only. It should look in Herd's bin folder too.
- **K3:** write the three job-file lines the ship script reads (handoff, section 4a); run `bin/check-project.py` and the gate from the preflight and the code skill; pass `--php` and `--composer` (on this Mac: Herd's `php85`); add the `migrate:rollback` exception to the guard request list as K1 noted.
- **Paperwork track:** the host checklist should say that the site's deploy box only fetches the code and runs `bash deploy.sh`; that production's `.env` has `APP_DEBUG=false` and `DB_DATABASE` as the full path of the shared database file, which must exist before the first deploy; that `/up` and `/version` must be readable without a login; and that `.kit/project.json` is filled in (staging alias, app root, health address; production's version line; `production.live` set to true after the first deploy).

**Refused by the app's safety check:** nothing.

**Untouched, checked at the end.** `~/.claude/settings.json` was last changed on 2026-10-01 21:23, before this run. `~/Dev/clc-plugins/` shows the same five uncommitted files. None of K1's guard files changed (`git diff 26a0dbc HEAD` over them is empty). The kit has no remote. Nothing else was written in the Sancho tree.

**What I read in `hdonline-v4/`, said plainly.** Its `composer.json`, `phpunit.xml`, `pint.json`, `phpstan.neon`, `package.json`, `README.md`, `.gitignore`, `.gitattributes`, the names of the files under `tests/` and `app/`, `tests/Pest.php`, `tests/TestCase.php`, `tests/Arch/ArchTest.php`, `routes/web.php` (first 40 lines), `app/Providers/AppServiceProvider.php`, and the last five lines of its `git log`. That is a little more than the three things the brief named (its `composer.json`, test config and tests layout); all of it was read only, to make the template fit a real project. I did not read `.env` or `.env.example`, and wrote, staged and ran nothing there apart from that one `git log`.

## K1 fixes

Started 2026-10-02 03:25 CEST. Fixer: Claude, model Fable 5.1 (`claude-fable-5-1`). I cannot see my own effort level. I wrote neither the kit nor the review. Scope: the 25 findings of `reviews/kit-K1.md` and its 869 cases, on the kit at commit `00c07f8`.

### Plan (written before any change)

**First, check the review.** Done before this plan was written, with a replay script kept in a scratch folder (not in the kit yet):
- The 869 cases were handed to the guard at `00c07f8`, in-process, with the fixture rules. Result: 436 allowed, 433 refused; **226 wrongly allowed** (71 "must", 56 "gap", 41 "limit", 58 "disguise") and **53 wrongly refused**. Every one of the 869 answers equals the answer the reviewer recorded at the foot of the case file. The reviewer's numbers are true.
- Finding 4 reproduced: a wrapper that is not there exits 127 and prints nothing; a wrapper cut off before it reads its input exits 0 and prints nothing; `CLC_GUARD_PYTHON=/usr/bin/true` turns a must-refuse command into exit 0 with nothing printed; with standard input held open for 12 seconds the wrapper came back after 12.0 seconds.
- Finding 5 reproduced: the registration check says OK four times and exits 0 with ` || true` added, with the variable in front, with another rules file, with `async`, and with no timeout.
- Finding 2 reproduced: the check's own matcher function says the example matcher does not cover `Monitor`. I loaded the definition of `Monitor` in this session: its `command` field is "Shell command or script" and it "runs in the same shell environment as Bash". The terminal tool's definition has its own `cwd` field (finding 3a).
- Finding 21 reproduced: one word of 400,000 characters takes 1.7 seconds.
- Hook facts, from documentation that is on this Mac (the official plugin marketplace's hook-development pages under `~/.claude/plugins/`): exit code 0 is success, exit code 2 blocks, any other exit code is a non-blocking error; the hook input carries `cwd`; a matcher is a list of exact names or a regular expression.

**What will change, in this order. Each step ends with its tests green and a commit.**

1. **The replay of the reviewer's file as a test.** A copy of the case file goes into `tests/fixtures/`, with a second file holding the expected answer for every one of the 869 ids. One test replays them all and fails on any answer that differs. A case the guard still gets "wrong" by the reviewer's reckoning stays in the expected file with the reason beside it, so the count of what is left open is itself tested.
2. **Blocker 1: a command inside a command.** Before the text is split into words, every `$( ... )`, every backtick pair and every `<( ... )` or `>( ... )` is found in the raw text, at any depth, and judged as a command line of its own. No early return for a call that only sets a variable. A redirection's target is covered because the search runs on the raw text. Operators are split the way a shell splits them (`&&>` is `&&` then `>`). More than six levels deep is refused, not skipped. The here-document exemption is narrowed (finding 20): text handed to `cat` is only "plain text" when nothing unclosed surrounds it except `git commit`, `git tag` or `git merge`.
3. **Blocker 3: the push rule decides by the repository the push would act on.** The start is the tool's own folder when the tool has one. Every folder the command moves to (`cd`, `pushd`, `git -C`, `--git-dir`, `--work-tree`, `GIT_DIR=`, `env -C`, `find -execdir`) is worked out. A folder under the kit folder is a project, except the kit's own folders (the kit's own repository stays exempt, wherever the command starts). A folder outside is looked at on disk: it is a kit project if its repository carries the template's `.kit/project.json`, or is a git worktree of a repository under the kit folder, or was cloned from one. A folder that cannot be worked out (a variable, a wildcard) is treated as a project. The words "the kit folder's name appears in the text" stop deciding anything. `git subtree push`, `git send-pack` and `git-push` by path are read as pushes.
4. **Blocker 2: every tool that runs a shell command.** `Monitor` joins the shell matcher and the registration check's own list, so the check fails without it. The guard judges `Monitor`'s command, and its web-socket address as an address. The browser pane's `preview_start` starts a program named in `.claude/launch.json`: the guard reads that file and judges the command. The iOS simulator tool joins the browser matcher (finding 25e). The log will list every tool I could find that can start a program, and say which I could not confirm.
5. **Findings 7, 8, 9, 24: other roads.** Options that point an ssh somewhere else are refused for hosts this guard passes over too. `forge`, `gh` (and `hub`, `doctl`) are caught among another program's words, by path, and as packages by their last part; only verbs that cannot install or run (`list`, `uninstall`, `show` ...) pass. Git's own destinations (`clone`, `fetch`, `pull`, `push`, `ls-remote`, `remote add`, `remote set-url`) are judged like an ssh destination. `ssh-copy-id`, `slogin`, `lftp`, `ansible` join the refused family; `ssh://`, `sftp://`, `scp://` addresses and `--ssh=` go by the same host rule.
6. **Findings 10, 11, 14, 16: what may run on staging.** Tightened: `config:show`, a recursive search from the app root, a wildcard in a dot-name, the cached config file (10); the reading tools may print the logs and source files but not the database or stored documents (11); `sort -ro`, `uniq -`, `date --set`, `make:*`, `install:*`, `vendor:publish`, `schema:dump`, `dusk`, `model:prune` (16). Opened, each with the reason it is safe: a `|` or `&&` inside quote marks is no longer taken for a join; `php8.5` and `/usr/bin/php`; `echo`, `uptime`, `ps`, `zcat`, a `find` that cannot write or run, `sed -n` with a line range only; the app root in quote marks; `.env.example` (14).
7. **Findings 12, 15, 17, 18, 21, 25.** The deploy-hook marker becomes `/deploy/http`. A comment line, `find`, `whereis`, `hash`, `[[`, the documentation sub-domain, `brew uninstall` (15). `www.` in front of the production name; a pipe to `head`, `grep`, `jq`, `wc` and a trailing `echo` after the plain read (17). Addresses are also matched after percent codes, look-alike characters, tabs, line breaks, soft hyphens, `/./` and `/../` are resolved, and number forms of an address are read (18). A word over 100,000 characters is refused (21). `ssh -G` passes; a ref written `refs/heads/...` is a branch (25).
8. **Findings 4 and 5: the outermost layer.** The registered command checks that the wrapper is there and whole (a last-line marker) and turns every failure into exit code 2. The wrapper's body moves into a function so a cut-short file cannot run half of it. The two environment overrides are removed; the tests edit a copy. The deadline covers the read of standard input. The registration check compares each command with the exact expected text, refuses `async`, and requires the timeout.
9. **Finding 6 and the Herd `forge`.** The way out of a broken guard, in plain words for Gordon, in the wrapper's message, the registered command's message, the installer and the kit handoff. The self-test remembers a failing fingerprint and reports it at once; it runs the guard's own tests after any change and the slow gate and ship tests only when their files changed. The installer looks in Herd's folder for `forge` and says so.
10. **Findings 13, 22, 23 and the honest limit.** A table in the rules file saying what each rule that claims a mechanism rests on today, checked by the lint. The lint's content checks (22) and the ledger rows (23) if they stay small. The honest limit rewritten in the guard's header and stated in the rules file (a new rule, with its ledger row).

**Two rules I hold myself to** (from the WordPress guard's repair). Nothing is loosened to cure a false refusal unless the loosened shape can be shown safe; where it cannot, the refusal stays and the log says so. And every rule change keeps the earlier answers: all 869 cases are run against the guard before and after, and any case that was refused and is now allowed is listed by id with its reason.

**What I will not do.** Register a hook. Edit anything under `~/.claude/`. Contact a server. Type an ssh, rsync, scp, sftp or push example on my own command line (they live in files). Install anything. Push, or add a remote. Touch `~/Dev/clc-plugins/` or look inside `hdonline-v4/`. Edit the review files. Change the list of hosts the guard leaves alone, or add pages to the refused list beyond what a finding's fix needs: those are Gordon's (the real-rules test says "until Gordon decides otherwise").

**How it is tested.** As K1: Python's own test runner, made-up hosts, nothing that depends on this Mac. New: the push rule's look at the disk goes through one small reader that the tests replace with a made-up disk, plus tests against real throwaway repositories (a clone, a worktree) in a temporary folder; the registered command line itself is run by the tests against a missing wrapper and against the wrapper cut at every line.
