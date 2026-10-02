---
name: Home Directions v4 review, kit stages K2 and K3, fit to the specification
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: Independent review of stages K2 and K3 of the Laravel kit at commit d47f4ea (the gate, the ship script, the project template, the seven skills, the updates calendar, the installer) against laravel-kit-spec.md and plan-v2.md; the release gate attacked in throwaway repositories, the template and the deploy script tried with real PHP, the test run and the proof rerun; 27 numbered findings, each with the file and line, the evidence, the fix and a weight, and a verdict on each thing the builders did beyond the spec
sources: ["[doc:build-handoff.md]", "[doc:build-state.md]", "[doc:laravel-kit-spec.md]", "[doc:laravel-tooling-research.md]", "[doc:plan-v2.md sections 7 to 9]", "[doc:hosting-options.md, Decision and the production boundary]", "[doc:build-log-kit.md, K2 and K3]", "[doc:runbook-accounts.md lines 179 to 199]", "[doc:~/Dev/clc-laravel/ at commit d47f4ea: CLAUDE.md, docs/HANDOFF-laravel-dev-kit.md, bin/, skills/, templates/, config/, tests/]", "[reviewer test 2026-10-02: bash bin/test-all.sh in a clone of d47f4ea]", "[reviewer test 2026-10-02: bin/prove-template.py with PHP 8.5.10, kept in a scratch folder for the experiments below]", "[reviewer test 2026-10-02: eleven runs of bin/ship.py against throwaway repositories made with tests/throwaway.py]", "[reviewer test 2026-10-02: the real gate and the real deploy script on the proof's made-up project and sites]", "[reviewer test 2026-10-02: bin/whats-due.py at nine made-up dates]", "[reviewer test 2026-10-02: bin/install-mac.sh with a pretend home folder, files fingerprinted before and after]", "[reviewer test 2026-10-02: bin/check-project.py and bin/laravel-new.py (list only) on hdonline-v4, reading only]"]
status: written 2026-10-02 12:35 CEST by a reviewer that did not write the kit; 3 blockers, 12 should-fix, 12 minor; no file in the kit or in the app was changed, staged or committed; the scratch folder was removed afterwards (one small folder the kit's own test leaves in the temporary folder was not, see finding 27); nothing else was written in the Sancho tree
---
# Review: kit stages K2 and K3, fit to the specification, at commit d47f4ea

Reviewer: Claude, model `claude-fable-5-1`. I cannot see my own effort level. I did not write the kit and I changed nothing in it. The tests ran in a clone in a scratch folder. The experiments ran on throwaway repositories and on the made-up project that `bin/prove-template.py` builds. No server was contacted. No real client data was opened. The plan gate and the guards have their own reviewer; I looked at them only where a skill's step meets them.

**The conclusion first.** The builders' numbers are true: 2,720 tests pass, and the proof with real PHP passes 43 of 43. The ship script does what decision D2 asks in every case the builders tested: it refuses a red gate, a wrong branch, a code change after the review, and a missing "ship it"; it raises the alarm when production moves by itself. The installer only prints. Nothing is registered, linked or pushed, and nothing needs a credential.

The first real project does not stand on it yet, for three reasons that let unreviewed or untested work reach `main`, and one that is simply not done:

1. **A commit made on the local `main` ships with no reviewer pointed at it.** The review reads `main...<branch>` with the local `main`. The ship script moves the remote's `main`. A commit that sits on local `main` and was never pushed is in neither the review's list nor its difference, and the ship script pushes it. Shown in a throwaway repository (finding 1). So the spec review's "ship would carry unreviewed commits" is closed for commits made after the review, and still open for this road.
2. **The gate is green on packages that are not the ones the lock file names.** It tests whatever is in `vendor/`. After a lock file changes and nobody runs `composer install`, the gate passes on the old packages and the server installs the new ones (finding 2).
3. **The gate does not list a change to the audit's ignore list as "controls changed"** when it is written where Composer 2.10 keeps it. A branch silenced four real Laravel advisories and the gate said "Controls changed: none" (finding 3).
4. **The first app carries 3 of the template's 15 pieces, and no stage owns laying it over.** Laying it over as the program stands would replace the app's hardened test config with the template's weaker one (findings 6 and 7).

Weights: **blocker** = a way for unreviewed or untested work to reach production's branch, a destructive deploy step, or a rule the documents call enforced that is not; **should-fix**; **minor**. A point I could not show by running something says "not demonstrated".

## The numbers

| What I ran | Result |
|---|---|
| `bash bin/test-all.sh`, in a clone of d47f4ea | Ran 2,720 tests in 287.4 s, OK, exit 0. Failures 0, errors 0, skipped 0. The clone had no new file afterwards |
| `bin/prove-template.py` with Herd's `php85` | 43 of 43 checks passed, in 1 min 52 s. PHP 8.5.10, Laravel 13.34.0, Pest 5.3.0, Larastan 3.12.2, Pint 1.32.1. The real gate was green on 44 tests; the 21 deliberate changes each got the answer the builder lists |
| `bin/kit-lint.py all` | ok: 105 ledger rows, 129 rule IDs, 14 lessons, 39 mechanism rows |
| `bin/install-mac.sh` with a pretend home folder | It printed 123 lines. 840 files fingerprinted before and after: identical. The pretend home was still empty. (It ran 2,133 guard tests in 32 s.) |
| `bin/check-registration.py` on this Mac | six hooks missing, none registered. `~/.claude/settings.json` was last changed 2026-10-01 21:23 and does not name `clc-laravel`. No Laravel skill or agent is linked. The kit has no remote and no `.kit-state` folder |
| `bin/ship.py`, eleven experiments | findings 1, 11, 16, 17; the controls all held (list under question 1) |
| The real gate, six experiments on the proof's project | findings 2, 3, 5, 12, 18 |
| The real `deploy.sh`, on the proof's two sites | findings 4, 8, 9, 10 |
| `bin/whats-due.py`, nine dates | the date rules match section 9.3; finding 14 |
| `bin/check-project.py` on `hdonline-v4` (reads only) | 3 pieces there, 12 missing |

Not rerun: the builders' "each check switched off once" runs (39 and 157 pieces).

## The eight questions, in short

1. **The release gate (D2).** Held in these runs: an ordinary job ships (exit 0); a code change after the review is refused; a red gate is refused; shipping from `main`, `staging` or `hotfix/x` is refused; a dry run pushes nothing (no branch, no `staging`, no `main` on the stand-in for GitHub); production moving by itself gives exit 4; `production.live` switched to false on the branch needs "Controls approved"; a review of a commit with no gate record is refused. Not held: findings 1, 11, 16, 17.
2. **The gate.** It runs what the spec lists, in the spec's order, then the two migration checks. A missing PHP, Composer or tool gives exit 2 with a plain message (tried: no PHP, no Composer, `vendor/bin/phpstan` moved away, a plain PATH). What it lets through: findings 2, 3, 5, 18.
3. **The template.** Architecture tests, the three isolation measures, log probe, version line, CI workflow and bot config are there and behave as the proof says. The deploy script does nothing destructive: it deletes only its own safety copies beyond the newest ten. On a failed step it stops; what it leaves and says is finding 9. Others: 4, 8, 10, 12, 21.
4. **The skills.** Each step of section 7 has its place. Three steps do not fit the kit's own programs (findings 13, 19, 20). Write steps: write-plan, code, review, ship and kit-parity each end with a write; laravel-plan and laravel-update do not (finding 24). Triggers: finding 15. Claims of enforcement: the tables in the skills are honest about what is a hook and what is instruction; the over-claims are findings 3, 4 and 12.
5. **The calendar and "what is due".** Every date matches section 9.1 and the research; every row has a source and a read date; the assumed dates are marked. The rules match 9.3: the hard line for leaving Laravel 13 is 2027-12-18; with a made-up release of Laravel 14 on 2027-03-16 the upgrade is due from 2027-04-15 and overdue from 2027-06-15; PHP 8.6 may be adopted from 2027-02-17; Node 26 from 2026-12-27. No wrong date found. Findings 14 and 26.
6. **The installer.** It only prints. Nothing in the kit registers a hook or writes under `~/.claude/`. The only pushes are the three in `bin/ship.py`, to the project's own remote. Nothing needs a password, key or token.
7. **Beyond the spec.** A verdict on each is in the table near the end.
8. **The test run.** 2,720 tests, all pass.

## Findings

### Blockers

**1. A commit on the local `main` reaches the remote's `main` with no reviewer pointed at it.**
- Where: `skills/laravel-review/SKILL.md` lines 33 and 34 (`git diff main...HEAD`, `git log main..HEAD`); `CLAUDE.md` rule L-11.1; `bin/ship.py` lines 386 to 393 (it compares with `refs/remotes/origin/main`) and 261 to 290 (the review check).
- What is wrong: the review's range starts at the local `main`. The ship script's range starts at the remote's `main`. Nothing checks that the two are the same commit. The Review line names only the last commit, not where the review began.
- Evidence: throwaway repository with a bare repository as the remote. One commit made on local `main` (`app/Sneak.php`), not pushed. Branch `feature/thing` cut from it, one change to `app/Thing.php`. The review skill's own two commands showed one file (`app/Thing.php`) and one commit. Job file with a passing review of that commit and "Ship it". `ship.py` gave exit 0, and the remote's `main` then held `app/Sneak.php` as well.
- How it happens by mistake: any commit on local `main`. The WordPress kit's habit is exactly that ("quick-turn fixes commit directly on master"), and nothing mechanical stops a commit on local `main` here.
- Fix: (a) the Review line names the range, base and end (`Review: PASS <base>..<commit> <date>`), and the ship script refuses unless the base is the remote's `main` as just fetched; (b) the review skill fetches and uses `origin/main...HEAD`; (c) the ship script and the preflight (P9) refuse when local `main` is not the same commit as the remote's `main`. A test for each.
- Weight: **blocker**.

**2. The gate passes on installed packages that are not the ones the lock file names.**
- Where: `bin/gate.py`, `check_before_start` (lines 359 to 387) and the steps (line 433). The gate checks that `vendor/bin/...` exist. It never compares `vendor/` with `composer.lock`. `vendor/` is ignored by git, so the clean-tree check does not see it either.
- What is wrong: the gate "certifies a commit" (L-6.10), but the tests run on whatever is installed. The servers install from the lock file. For an `updates/<date>` branch this is the main road: the lock changes, and if `composer install` is not run before the gate, the old packages are tested and the new ones ship. The ship script reruns the same gate on the same `vendor/`.
- Evidence: on the proof's project, `composer update fakerphp/faker --prefer-lowest --no-install` changed only `composer.lock`. Committed. The real gate: all eight steps PASS, "Controls changed: none". `composer install --dry-run` then said "Downgrading fakerphp/faker (v1.24.1 => v1.23.0)".
- What softens it: CI installs from the lock on a clean machine, so its result for that commit would differ. The ship hand-over prints the address of those checks. `main` has already moved by then.
- Fix: before step 1, compare every package and version in `composer.lock` with `vendor/composer/installed.json` (plain Python, no network). Any difference is exit 2: "run composer install first". The laravel-code and laravel-update skills say to install after any change to a lock file.
- Weight: **blocker**.

**3. A change to the audit's ignore list is not listed as "controls changed".**
- Where: `bin/gate.py` line 126: `COMPOSER_CONTROLS = (("config", "audit"), ("config", "allow-plugins"))`. Its own header and the spec (section 5, item 1) say the audit ignore list is a control.
- What is wrong: the Composer on this Mac is 2.10.2. Its own schema marks `config.audit` as deprecated and keeps the ignore list under `config.policy` (`policy.advisories.ignore-id`, `ignore`, `ignore-severity`). The gate does not look there.
- Evidence: on the proof's project I set the lock's Laravel to v13.0.0. `composer audit --locked` listed four advisories (one high) and gave exit 1; the gate failed at step 5, as it should. I then added the four IDs under `config.policy.advisories.ignore-id` in `composer.json`. `composer audit --locked`: exit 0. The gate: all eight steps PASS, "Controls changed: none", exit 0.
- Fix: add `("config", "policy")` to the list; better, list any change to `composer.json`'s `config` block except a short list of harmless keys. Add this case to `bin/prove-template.py`, which runs the real Composer. Also: a baseline or include file of the analyser in a subfolder is not a control (lines 123 and 124 look in the top folder only; by reading).
- Weight: **blocker** (the documents call this listed, and for the installed Composer's own key it is not).

### Should-fix

**4. The deploy script's debug check refuses only the exact word `true`.**
- Where: `templates/laravel-new/files/deploy.sh` line 132. The script's header, the kit handoff (choice 22) and the build log say it "refuses a production site whose `.env` has debug switched on".
- Evidence: on the proof's production site, with `APP_ENV=production`: `APP_DEBUG=true` stopped the deploy. `True`, `TRUE`, `1`, `(true)`, `yes` and `true # for one day` each ran to "DEPLOY FINISHED", and Laravel then reported debug on for all six.
- Fix: refuse unless the value is one of `false`, `(false)`, `0`, empty or absent, compared without regard to capitals, after cutting a trailing comment. Or ask Laravel itself after the caches are built and stop before the commit is recorded. A test for each spelling.
- Weight: **should-fix**. It borders on a blocker by the brief's third clause; I weigh it lower because the spelling most likely to be typed is the one refused.

**5. The template's test config does not force its settings, so a database named in the shell is emptied by the gate.**
- Where: `templates/laravel-new/files/phpunit.xml` lines 32 to 47 (no `force="true"`); `bin/gate.py` line 433 (the test step inherits the shell's environment; the migration step at line 294 gets a made one).
- What is wrong: this is the fault the app's P1 safety review found ("running the app's tests with `DB_DATABASE` set in the shell emptied that database"). The app fixed it. The template does not carry the fix, so every later project starts with it.
- Evidence: a scratch SQLite file with one table, `precious`, and five made-up rows. The real gate run with `DB_CONNECTION=sqlite DB_DATABASE=<that file>` in the shell: GATE: PASS. Afterwards the file held the app's ten tables and no `precious`.
- Fix: `force="true"` on every `<env>` line of the template's `phpunit.xml`; the gate removes `DB_*`, `MAIL_*`, `QUEUE_*`, `CACHE_*`, `SESSION_*` and `APP_ENV` from the environment of the test step; a mutation in `bin/prove-template.py` for it.
- Weight: **should-fix** (destructive on this Mac, not on a server).

**6. Laying the template over the first app would replace its hardened test files.**
- Where: `bin/laravel-new.py` line 73 (`REPLACED = ("phpunit.xml", "tests/TestCase.php", "tests/Pest.php")`) and line 221: any of these that differs from the template is replaced and described as "the fresh project's stock file", with no check that it is one.
- Evidence: `laravel-new.py /Users/gordonium/Dev/clc-laravel/hdonline-v4` (list only, nothing changed) printed "replace phpunit.xml (the fresh project's stock file)", the same for `tests/Pest.php` and `tests/TestCase.php`, and one CONFLICT (`phpstan.neon`). The app's `phpunit.xml` has 31 `force="true"` attributes from the P1 safety fix; the template's has none. Once the one conflict is settled, `--apply` would overwrite all three.
- Fix: replace only when the file is byte for byte the stock file (the kit already keeps the stock files in `tests/fixtures/fresh-laravel/`); anything else is a CONFLICT. Fix finding 5 first, so the template's file is not the weaker one.
- Weight: **should-fix**. Do not run `laravel-new.py --apply` on `hdonline-v4` before this is fixed.

**7. The first app does not stand on the kit, and no stage owns putting it there.**
- Where: `hdonline-v4` as it is on disk; `build-state.md` (P3, P4, W2 and Z do not name it); `build-log-kit.md` K2 and K3 both say "that is the app track's to do".
- Evidence: `bin/check-project.py` on the app: T1, T2 and T4 are there; T3 and T5 to T15 are missing. No `deploy.sh`, no `VERSION`, no `/version` address, no `kit:status` command, no CI workflow, no bot config, no `.kit/project.json`, no per-project `CLAUDE.md`. `bin/ship.py` stops at "This project has no .kit/project.json". The runbooks' deploy, version-line and backup-before-deploy steps all assume these pieces.
- Fix: give it a stage of its own, after findings 5 and 6: lay the template over the app by hand where files differ, then the gate on it, then the app's own review.
- Weight: **should-fix** (for the orchestrating thread).

**8. A new migration edited after staging ran it is not noticed; staging then proves nothing about it.**
- Where: `bin/gate.py` lines 240 to 246 (the "unchanged" check compares with `main` only); `bin/ship.py` step B10. Rule L-2.2's first sentence ("a migration that has run on staging is never edited") has no check.
- Evidence: on the proof's staging site: a new migration that creates `review_notes` with one column; `deploy.sh`, exit 0. The same file edited to add a column `body`; `deploy.sh` again, exit 0, "Nothing to migrate"; `kit:status` said "pending migrations: 0"; the table on staging had the one column `id`. The ship script's parity proof reads exactly those two facts. Production would run the edited file.
- Fix: the job file already records `Staging: <commit>`. The ship script (or the gate) refuses when a migration file that exists at any commit on a `Staging:` line, or at the remote's `staging` before it is moved, has changed since.
- Weight: **should-fix**.

**9. A deploy that fails after the migrations says nothing about where it stopped or what has already changed.**
- Where: `templates/laravel-new/files/deploy.sh` lines 204 to 212. Only the script's own `stop` calls print "DEPLOY STOPPED". A failing program ends the run through `set -e` with no closing line.
- Evidence: on the proof's production site, with a new migration and a stand-in PHP that fails at `artisan optimize`: exit 1; the output's last line was the tool's own error; the production database had the new table; `RELEASE` still held the old commit; `kit:status` reported the old commit and 0 pending. With a two-word Composer setting (finding 10) the log simply ends after the heading of step 2.
- What this means: with Forge's zero-downtime releases the old release stays live, now on a database one step ahead. On a site that deploys in place, the live folder would hold new code and old caches. The runbook sets zero-downtime on for both sites (`runbook-accounts.md` line 179). The script does not say it depends on that. The lines for Forge's deploy box are written nowhere in the kit; the runbook says "Sancho gives you the few lines".
- Fix: an `ERR` trap that prints "DEPLOY STOPPED at step N", whether the migrations had already run, and where the backup of step 1 is. Say in the script's header and in the per-project file that the site must use zero-downtime releases. Put the deploy box's lines in the template as a file.
- Weight: **should-fix**.

**10. The deploy script treats `FORGE_COMPOSER` as one word.**
- Where: `deploy.sh` lines 42 and 155 (`"$COMPOSER" install ...`).
- Evidence: with `FORGE_COMPOSER` set to two words (a PHP program and Composer's path), the production deploy took its backup and then stopped at step 2: "No such file or directory". Nothing else changed.
- Not demonstrated: that Forge hands over a two-word value. From memory, Forge's own default script uses `$FORGE_COMPOSER` unquoted and its value is a PHP program followed by Composer's path. The kit's own gate accepts a two-word program for the same reason.
- Fix: split the setting into words before use, as `bin/gate.py` does. Confirm on the first staging deploy.
- Weight: **should-fix**.

**11. The ship script watches production for 120 seconds; a deploy can take longer, and the script then says "It did not deploy by itself".**
- Where: `bin/ship.py` line 615 (`"watch": 120`) and lines 539 to 559. The same script waits up to 600 seconds for staging to run the same deploy script. The research says Forge lets a deploy run for ten minutes.
- Evidence: scaled down in a throwaway repository: the watch set to 4 seconds, a made-up production that shows the new commit 8 seconds after `main` is pushed. `ship.py`: exit 0, "Production still shows 0.1.0 ... It did not deploy by itself." Eight seconds later the version line showed the shipped commit.
- Fix: watch at least as long as staging took to report the commit in step B9, and not less than 600 seconds; print how long it watched; laravel-ship step 4 reads the version line once more just before Gordon presses Deploy.
- Weight: **should-fix** (this watch is the kit's only detector for deploy-on-push left on).

**12. The "only dummy credentials" test looks at two config groups; the documents say "any".**
- Where: `templates/laravel-new/files/tests/Feature/Kit/IsolationTest.php` lines 32 to 35 (`services` and `filesystems.disks`). `phpunit.xml`'s comment and the kit handoff (choice 20) say it fails on any key the tests can see.
- Evidence: on the proof's project, a config file of the app's own (`config/brevo.php`) reading two keys, and three made-up values in `.env` that do not start with "dummy" (two for that file, one for `MAIL_PASSWORD`). A probe test showed the tests see both values. The isolation tests passed, and the gate was green.
- For the first app the keys that matter (Brevo, Google) are in `config/services.php`, which the test does read.
- Fix: walk the whole of `config()`, not two groups.
- Weight: **should-fix**.

**13. laravel-ship tells Claude to edit the project's `CLAUDE.md` after the ship; the plan gate refuses that, and the edit would never reach `main`.**
- Where: `skills/laravel-ship/SKILL.md` line 129 (step 7); `skills/laravel-write-plan/SKILL.md` lines 37 to 45 ("Bring the records forward" copies only `.kit/jobs`).
- Evidence: in a made-up kit, with the real `plan-gate.py`: an edit to the project's `CLAUDE.md` is allowed before the `Shipped:` line and denied after it (PG-1: "every job file of the project is shipped or closed"). The job file itself can still be written.
- Fix: the facts go into the project's `CLAUDE.md` before the review (laravel-code step 6 already says so). Step 7 keeps only what goes into the job file; anything else is a follow-up for the next job.
- Weight: **should-fix**.

**14. "What is due" answers "nothing is due" while the app's Node line and server are not recorded.**
- Where: `bin/whats-due.py` lines 512 and 513: a missing Node line or operating system is a "note", and notes do not change the exit code. The script's part of the schedule is its exit code (spec 9.4).
- Evidence: `whats-due.py` today: exit 0, "RESULT: nothing is due", with two notes. The template has no `.nvmrc`, so every new project starts this way. With nothing recorded, the Ubuntu and Node end dates can never be raised.
- Fix: once production is live, a missing server or Node entry is DUE. Read the Node line from the CI workflow when there is no `.nvmrc`.
- Weight: **should-fix** (must-never 10: never fall behind silently).

**15. "Ship it" is claimed only by the WordPress skill.**
- Where: `tests/test_skills.py` lines 31 and 32 forbid the Laravel descriptions from holding "ship it", "review this", "we're done". The WordPress `plugin-ship` description lists "ship it", "push it", "tag it". The kit's own rules call Gordon's gate "ship it" and the job file's line is `Ship it: Gordon`.
- What is wrong: once both sets are linked, the one description that names the words Gordon will say in a Laravel session is the WordPress one, and that skill commits, tags and pushes by hand. With no guard registered nothing would stop it.
- Not demonstrated: it needs a live session with both sets linked.
- Fix: Gordon's decision. Either apply proposal P-9 to the WordPress descriptions before the Laravel skills are linked, or let `laravel-ship` name the words, tied to a project under `~/Dev/clc-laravel`. The `pre-push` hook the K1 fix left for this review (see the table below) would also stop it.
- Weight: **should-fix**.

### Minor

**16. An environment variable replaces the staging server.** `bin/ship.py` line 363 reads `CLC_SHIP_SSH`. With it set to a three-line script that prints the four facts, and the stand-in staging set to refuse every connection, `ship.py` gave exit 0 and moved `main`; no call reached the stand-in staging. The K1 fix removed the same kind of override from the guard's wrapper. Fix: the tests edit a copy, as they now do for the wrapper.

**17. After a review, any file under `.kit/jobs/` may change, not only job files.** `bin/ship.py` line 117. A `helper.php` added there after the review shipped (exit 0). It is inert unless something loads it. Fix: allow only `.md` files and `.gitkeep`.

**18. App code may use a development-only package.** A class in `app/` that uses Faker: the gate was green. The staging site of the proof, installed the way the deploy script installs (no dev packages), has no Faker. Fix: an architecture rule that `App` uses nothing from the dev packages' namespaces.

**19. The gate, the record and the review chase each other.** `skills/laravel-review/SKILL.md` line 24: "If the head moved since the last gate run, run the gate again and record it." Recording a gate run changes the job file; committing that moves the head. The kit's own end-to-end test avoids the loop by leaving the lines uncommitted until the version commit. Fix: say that a commit touching only `.kit/jobs/` needs no new gate run, and that the Review line names the last gated commit. laravel-ship step 1 says "the commit that is the branch's head", which is then not true either.

**20. "Command-line PHP and web PHP are the same version" has no tool.** `skills/laravel-plan/SKILL.md` line 66, rule L-10.5. `kit:status` prints the command line's version; the version line and the log probe's web answer print none. Fix: add the PHP version to the log probe's web answer.

**21. The backup before a deploy.** (a) `deploy.sh` line 92 puts the copies beside the database path as it is written in `.env`. If that path runs through the `current` link, the copies sit inside a release folder that the host prunes. By reading; not demonstrated on Forge. Fix: resolve the real path first. (b) The plan (section 9) and the hosting decision say the backup before a deploy is the encrypted archive, with the stored PDFs, in two places elsewhere. The template makes a plain copy of the database on the same disk. This is already question 5 for Gordon in the paperwork log.

**22. Records.** (a) `bin/kit_repo.py` lines 249 to 254: the gate's record names the kit's commit even when the kit has uncommitted changes, so an edited `gate.py` leaves no mark. By reading. (b) The parity proof, the previous `main` and the reviewed commit are kept only under the project's `.git` folder on this Mac; the spec (section 5, item 2) puts the parity proof in the job file.

**23. "One job on staging at a time" is instruction.** `bin/ship.py` lines 441 to 444 take the lease on `staging` from a fetch made seconds earlier, so it always matches. Another job under test on staging is moved off without a word. By reading.

**24. Two skills end without a write.** laravel-plan ends with a hand-over (by design: plan mode allows no write, and with the hooks off an approved plan leaves nothing on disk until laravel-write-plan). laravel-update ends with a report; a plain "what is due" run leaves no receipt.

**25. Laravel Boost is half of decision D8.** The package is in the template; `boost:install` has not been run (`boost:update` answers "Please set up Boost"). laravel-plan step 4 points to Boost's documentation search, which is therefore not there. The research says setting Boost up rewrites `CLAUDE.md`; `check-project.py` would flag that (T14). Not demonstrated.

**26. "What is due", two small things.** (a) It reads PHP from `composer.json`'s constraint, not from what the server runs; it errs toward a false alarm. (b) The plan (section 9) asks for a restore test once before go-live; the script starts counting the restore drill only when production is live.

**27. Every full test run leaves a folder behind in the Mac's temporary folder.** `tests/test_gate.py` line 494 (`test_the_report_is_counted_through_nested_suites`) makes `clc-gate-report-test-...` and never removes it. Each holds one 12-byte file. 21 of them were there at 12:35 today (18 in the user's temporary folder, 3 in `/private/tmp`), one from my own run; I left them, because I could not tell mine from another agent's. The builders' "the copy had no new files" is true of the copy; this is outside it. Fix: remove the folder at the end of the test.

## What the builders did beyond or differently from the spec

K2 (their list in the build log):

| # | What | Verdict |
|---|---|---|
| 1 | The gate also runs the migration checks, on every migration | Right. Spec section 4 gives them to the gate. Their limit is finding 8 |
| 2 | More files count as controls | Right, and still one short: finding 3 |
| 3 | The ship script reads three fixed lines of the job file | Right, and honestly labelled instruction. The Review line should also name where the review began: finding 1 |
| 4 | `migrate:rollback` left usable; four commands switched off one by one | Right. The proof shows it (checks 9.05 and 21) |
| 5 | The deploy script refuses debug on, an unknown commit, a missing or relative SQLite path; its own backup | Right in aim. The debug check is finding 4. The backup differs from the plan: finding 21 |
| 6 | Laravel's shipped `CLAUDE.md` and `AGENTS.md` replaced and removed | Right (rule L-5.12). See finding 25 |
| 7 | The CI workflow repeats the gate's commands | Right: CI may hold no secret, so it cannot fetch a private kit. The one third-party action is Gordon's to accept |

K3 (their list in the build log):

| # | What | Verdict |
|---|---|---|
| 1 | A preflight program | Right. It should also compare local `main` with the remote's: finding 1 |
| 2 | The job file made by a program | Right |
| 3 | Three kinds of stamp and a settings file | Right, and honestly labelled |
| 4 | The stamp lives in the kit folder | Acceptable. It is on one Mac only and in no backup |
| 5 | The plan gate fails open for shell commands and the kit's own files | A fair choice, correctly put to Gordon |
| 6 | A file git ignores is not the gate's business | Right for the plan gate. The same blind spot in the release gate is finding 2 |
| 7 | The job file's record is one list at the end | Right. It is what stops an old "ship it" counting for a new review |
| 8 | The closing lines reach `main` with the next job | Works for `.kit/jobs`. Anything else written after the ship is lost: finding 13 |
| 9 | The effort level compared by the hook | Right, labelled "not seen live" |
| 10 | The reviewers get their material as files | Right. The commands that make the files use the wrong base: finding 1 |
| 11 | Not built: the `migrate:rollback` exception | Right to leave it refused |
| 12 | Not built: a `laravel-new` skill | Matches the build handoff's list. The second project will have no written procedure; "what is due" does flag a project that is missing from the calendar |
| 13 | A calendar row for Node 26 | Right, with its source |

Left for this review by the K1 fix: **a git `pre-push` hook in the project template.** Verdict: build it. It is the one check that would work today, with no Claude hook registered: git hands it the real names being pushed, so a push of `main` or a tag from anything but the ship script is refused, the WordPress ship skill included (finding 15). Switching it on in a clone is one git setting, which is a step for Gordon's checklist.

## Not done, and not demonstrated

- Nothing here met a real Forge site or GitHub. Findings 9, 10 and 21 say which parts rest on how Forge behaves.
- Finding 15 needs a live session with both sets of skills linked.
- I did not run the gate, the preflight or the tests on `hdonline-v4`: the gate writes its record into the project's `.git` folder, and the preflight reads the names in its `.env`. I ran `check-project.py` and `laravel-new.py` without `--apply`, which only read.
- I did not rerun `bin/parity-check.py` against the WordPress kit; my brief did not ask me to read that kit beyond its three skill descriptions.
- The plan gate and the guards were not attacked here; they have their own review.
