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
