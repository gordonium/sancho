---
name: Home Directions v4 review, kit round 3, the release gate, the deploy script and the project template
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: Independent second look at the Laravel kit at commit fec74fb, after the 46 fixes nobody had reviewed. The three earlier blockers tried again in throwaway repositories with real PHP; decision D2 end to end; the deploy script with every spelling of debug-on, a failed migration and the backup question; a walk of one invented job through the five skills; the test run and the proof rerun; and the brief for laying the template over the first app. 24 numbered findings, each with file and line, the evidence, the fix and a weight
sources: ["[doc:build-handoff.md]", "[doc:build-state.md]", "[doc:laravel-kit-spec.md]", "[doc:plan-v2.md sections 7 to 9]", "[doc:hosting-options.md, Decision and the production boundary]", "[doc:reviews/kit-K2-K3-fit.md]", "[doc:build-log-kit.md, K2, K3 and the K2 and K3 fixes]", "[doc:build-log-app.md, searched for the template's pieces only]", "[doc:~/Dev/clc-laravel/ at commit fec74fb: CLAUDE.md, bin/, skills/, templates/, config/, tests/]", "[doc:~/Dev/clc-laravel/hdonline-v4/: composer.json, phpunit.xml and the names of the files under tests/, nothing else]", "[reviewer test 2026-10-02: bash bin/test-all.sh in a clone of fec74fb]", "[reviewer test 2026-10-02: bin/prove-template.py with PHP 8.5.10 and Composer 2.10.2, its project kept for the experiments]", "[reviewer test 2026-10-02: 19 runs of the real deploy.sh on the proof's production site]", "[reviewer test 2026-10-02: 11 runs of the real gate with real PHP on the proof's project]", "[reviewer test 2026-10-02: 33 one-change branches judged by the real gate in a throwaway repository]", "[reviewer test 2026-10-02: 20 runs of bin/ship.py against throwaway repositories made with tests/throwaway.py]", "[reviewer test 2026-10-02: one invented job walked through the skills' own commands]", "[reviewer test 2026-10-02: bin/laravel-new.py and bin/check-project.py on a stand-in shaped like the first app]"]
status: written 2026-10-02 16:05 CEST by a reviewer that did not write the kit; 1 blocker, 13 should-fix, 10 minor; no file in the kit or in the app was changed, staged or committed; every experiment ran in a scratch folder under the session's temporary folder, which was removed afterwards; nothing else was written in the Sancho tree
---
# Review: kit round 3, the release gate, the deploy script and the project template, at commit fec74fb

Reviewer: Claude, model `claude-fable-5-1`. I cannot see my own effort level. I did not write the kit and I changed nothing in it. The guards and the plan gate have their own reviewer this round; I looked at them only where a skill or a script meets them.

**The conclusion first.** The three blockers of the last round are fixed, and each fix held when I tried it again with its cousins. A commit that sits only on the local `main` no longer ships. A rebase, an amended commit and a merge after the review are all refused. The gate will not run when the lock file and the installed packages differ. A change to the audit's ignore list in `composer.json` is listed under either key. Nothing in the kit pushes `main` but the ship script, and no hook the kit installs pushes anything. The fixers' numbers are true: 4,092 tests pass, and the proof with real PHP passes 52 of 52.

It is not sound yet in four places.

1. **The deploy script still lets debug through on production.** The fix covers the value. It does not cover how the line is written. Five ordinary spellings (`APP_DEBUG = true` among them) ran to "DEPLOY FINISHED" with Laravel reporting debug on. The rules file says the script refuses this. That is the one blocker (finding 1).
2. **The gate certifies a commit but tests a folder.** Three things on this Mac that are not in the commit changed its answer: a vendor file edited by hand, a tracked file hidden from `git status`, and Composer's own settings file outside the project. Each made a red gate green (findings 2 to 4). One more file is not counted as a control: a baseline of the analyser kept as PHP (finding 5).
3. **The ship script does not survive a bad connection.** One bad answer from production during the ten-minute watch ends it with an alarm and without the hand-over. If the remote takes the push and the answer is lost, it says "Nothing reached main" when `main` has moved. It cannot be run again after either. And the watch alone is as long as the longest command a Claude Code session may run in the foreground (findings 7 to 9).
4. **The template cannot be laid over the first app by the program.** The fix that stops it overwriting the app's test files is right and holds. The other side of it: on the first app the program now stops at four conflicts and lays nothing, and it has no way to be told "keep the project's own file". The brief for doing it by hand is the last section of this file (findings 13 and 14).

Weights: **blocker** = a way for unreviewed or untested work to reach production's branch, a destructive or half-finished deploy, or a rule the documents call enforced that is not; **should-fix**; **minor**. A point I could not show by running something says "not demonstrated".

## The numbers

| What I ran | Result |
|---|---|
| `bash bin/test-all.sh`, in a clean clone of fec74fb | Ran 4,092 tests in 443.4 s, OK, exit 0. Failures 0, errors 0, skipped 0. The clone had no new file afterwards. The run left no folder in the Mac's temporary folder (the 26 old `clc-gate-report-test-` folders there are all from before 14:36) |
| `bin/prove-template.py` with Herd's `php85` | 52 of 52 checks, in 2 min 14 s. PHP 8.5.10, Composer 2.10.2, Laravel 13.34.0, Pest 5.3.0, Larastan 3.12.2, Pint 1.32.1. The real gate was green on 47 tests |
| The real `deploy.sh`, 19 spellings of the debug line on the proof's production site | 7 let through with debug on (finding 1) |
| The real `deploy.sh`, a release whose second migration fails | It said the step, that the migrations were running, where the backup is, and that `RELEASE` was not written. Correct |
| The real gate with real PHP, 11 runs | findings 2, 3, 4, 5, 18. A test turned into a todo was listed ("skipped tests rose from 0 to 1"). Correct |
| The real gate, 33 one-change branches in a throwaway repository | 21 listed as controls, 12 not (table under finding 21) |
| `bin/ship.py`, 20 runs | findings 7 to 10, 15 to 17. What held is listed under question 1 |
| The project's pre-push hook, 10 pushes | It refused `main`, a deletion of `main` and a tag in every plain form. The three ways past it that its header names worked as it says; one more is finding 23 |
| One invented job through the skills' commands | It ran from the plan to "closed" and on into the next job. Where it sticks: findings 8, 19, 22, 24 |

## The six questions, in short

1. **The three blockers.**
   - (a) *A commit only on the local `main`.* Refused, both when the review counted from the local `main` and when the Review line named the remote's `main` (the script refuses while the local `main` is ahead). Also refused: the reviewed commit amended after the review; the branch squashed by a rebase with one more file in it; another branch merged in after the review ("These changed after the review ... app/Other.php"). A merge made before the review is in the review's own difference. Allowed, and rightly: an amend of the version commit alone. A tag: finding 16.
   - (b) *Packages that are not the lock file's.* The proof changes the lock alone and the gate will not run (check 9.18). npm's lock is not the gate's business: the gate builds no assets, and a lock that does not fit fails `npm ci` on staging, which stops the ship. What is left: findings 2, 3 and 18.
   - (c) *A control changed unnoticed.* `config.audit`, `config.policy`, `config.allow-plugins` and `config.platform` are all listed now, and so are the CI workflow, a second workflow, the test config, the formatter config, a `.neon` baseline in any folder, the deploy script, the hook and `.kit/project.json`. What is left: findings 4, 5, 6, 14 and 21.
2. **Decision D2.** Nothing reaches `main` unattended by a program: the only push of `main` is line 627 of `bin/ship.py`; the six Claude Code hooks in the example block judge, stamp or test and push nothing; the pre-push hook only refuses; the CI workflow has read-only rights; the bot config merges nothing. What stands between an agent and `main` is the three lines of the job file, which Claude writes. The documents call that instruction, and it is. When the watch fails or the connection drops: findings 7, 8 and 9.
3. **The deploy script.** Debug: finding 1. A migration edited after staging ran it: refused when the job file has the `Staging:` line, missed when it has not (finding 10). A deploy that fails after or during the migrations: it now says what a person needs (shown with a real failing migration). The queue workers: finding 11. The backup: finding 12.
4. **The template over the first app.** Findings 13 and 14, and the brief at the end.
5. **The skills.** They agree with the scripts: the three fixed lines, the three kinds of stamp and the closing lines all went through `job-file.py` and `ship.py` as the skills write them. Where a job sticks: findings 8, 19, 22 and 24.
6. **The reruns.** In the table above.

## Findings

### Blocker

**1. The deploy script lets a production site with debug on through, when the line is written in any of five ordinary ways.**
- Where: `templates/laravel-new/files/deploy.sh` line 114 (`grep -E "^$1=" .env`), used by line 202. Rule L-9.15 in the kit's `CLAUDE.md` ("It refuses a production site unless debug is plainly switched off there"), the script's own header, the kit handoff (choice 22) and the fixer's log ("Seven spellings tried with real PHP: none let through").
- What is wrong: the script finds the setting only when the line begins exactly `APP_DEBUG=`. Laravel's reader is more forgiving: it accepts spaces or a tab before the name, the word `export` in front, and spaces round the equals sign. When the script does not find the line it reads "not set", which it counts as off.
- Evidence: on the proof's production site (`APP_ENV=production`), real PHP, the real script, then Laravel asked afresh (`php artisan about --only=environment --json`, field `debug_mode`):

| The line in `.env` | deploy | Laravel says debug is |
|---|---|---|
| `APP_DEBUG=true`, `True`, `1`, `on`, `"true"`, `true # for one day`, a variable that holds true, Windows line ends | stopped at step 0 | on |
| ` APP_DEBUG=true` (a space in front) | DEPLOY FINISHED | **on** |
| a tab in front | DEPLOY FINISHED | **on** |
| `export APP_DEBUG=true` | DEPLOY FINISHED | **on** |
| `APP_DEBUG =true` | DEPLOY FINISHED | **on** |
| `APP_DEBUG = true` | DEPLOY FINISHED | **on** |
| `APP_DEBUG=false`, then a later line ` APP_DEBUG=true` or `export APP_DEBUG=true` | DEPLOY FINISHED | **on** |
| `APP_DEBUG=false`, `false # normal`, the line taken out | DEPLOY FINISHED | off |

- How likely: the plain spellings are refused, so this needs a hand-typed line with a space in it. That is an ordinary slip in a host's settings box. The same blind spot applies to `APP_ENV`, `DB_CONNECTION` and `DB_DATABASE`, where it errs on the safe side (the script stops).
- Fix: do not read the file; ask Laravel. After step 2 (the packages are installed) and before step 5 (the migrations), run `php artisan about --only=environment --json` and stop unless `debug_mode` is false and the environment it reports is the one the script found. That also covers a debug default changed in `config/app.php` and a value set outside `.env`. Keep the early text check as a first, cheap stop. Add the five spellings to `bin/prove-template.py`, which runs real PHP.
- Weight: **blocker** (a rule the documents call enforced that is not).

### Should-fix

**2. A vendor file edited by hand makes the gate green on code the servers will not have.**
- Where: `bin/gate.py` lines 297 to 340 (`locked_and_installed` compares names, versions and commit references, not contents). Rule L-6.10 says the gate "certifies a clean commit".
- Evidence: on the proof's project I added one method to `vendor/laravel/framework/src/Illuminate/Support/Str.php`, and committed a class in `app/` that calls it with a test. `git status` was empty (`vendor/` is ignored). The real gate: all eight steps PASS, "Controls changed: none", exit 0. With the vendor file put back, the same test fails ("Method Illuminate\Support\Str::r3Marker does not exist").
- What softens it: CI installs from the lock on a clean machine and would be red. `main` has moved by then.
- Fix: `composer status` saw a one-byte edit of a vendor file in five seconds on this Mac. It also reports Pest's own folder, which Pest writes into, so the gate must leave that one out. Or the root fix for findings 2, 3 and 18 together: the gate tests a clean copy of the commit (a `git worktree` in a temporary folder, `composer install` from the lock out of Composer's cache), not the working folder.
- Weight: **should-fix**. It needs a deliberate edit under `vendor/`, which is why it is not a blocker.

**3. A tracked file that git has been told to overlook is tested as it is on disk, not as it is in the commit.**
- Where: `bin/gate.py` lines 445 to 450 (the clean-tree check is `git status`).
- Evidence: on the proof's project, a commit whose class returns 41 and whose test wants 42. On disk I changed the class to 42 and ran `git update-index --skip-worktree` on it. `git status --porcelain` printed nothing. The real gate: "Tests: 48 ran, 48 passed", GATE: PASS on that commit, exit 0. The commit's own test fails. The ship script reruns the same gate in the same folder, and staging runs no tests, so this commit would ship.
- Fix: one line. Refuse to run when `git ls-files -v` marks any file with `S` or a small letter (`skip-worktree`, `assume-unchanged`). It printed `S app/Support/Answer.php` here. The clean copy of finding 2 closes it too.
- Weight: **should-fix**. It needs a git command nobody types by accident; some people do use it to keep a local change out of their commits.

**4. Composer's own settings file, outside every project, silences the audit and the gate does not see it.**
- Where: `bin/gate.py` lines 286 to 294 (`clean_environment` takes the app's settings out of the steps' environment and leaves Composer's) and step 5 (line 115).
- Evidence: the proof's lock file with Laravel set to v13.0.0 (made up for the experiment; I set the same version in the scratch project's `vendor/composer/installed.json` so the gate would start). The gate as this Mac is: step 5 FAIL, four advisories, exit 1. Then with a `config.json` in Composer's home folder that lists those four IDs under `config.policy.advisories.ignore-id`, and nothing changed in the project: step 5 PASS, "Controls changed: none", GATE: PASS, exit 0. The older key, `config.audit.ignore`, did the same when I ran `composer audit --locked` directly.
- Why it matters: one `composer config --global ...` made for one project silences that advisory for every project on this Mac, and it is in no repository, so no review sees it.
- Fix: run step 5 with `COMPOSER_HOME` pointed at an empty scratch folder (keep the cache with `COMPOSER_CACHE_DIR`). Then only the project's own `composer.json` decides, and that is a listed control.
- Weight: **should-fix**.

**5. A baseline of the analyser kept as a PHP file is not a control.**
- Where: `bin/gate.py` line 137 (`CONTROL_PATTERNS = ("*.neon", "*.neon.dist")`). PHPStan writes a baseline in either form; `--generate-baseline=phpstan-baseline.php` gives PHP.
- Evidence: on the proof's project, with `phpstan.neon` on `main` already including `phpstan-baseline.php`. A branch with a type error: gate FAIL at step 3. Then PHPStan itself wrote the error into the PHP baseline. The branch now differs from `main` in `app/Support/Wrong.php` and `phpstan-baseline.php`. The gate: all steps PASS, "Controls changed: none", exit 0.
- What softens it: the first time, the `includes:` line in the `.neon` is itself a listed change. After Gordon has approved that once, every later entry in the PHP baseline is silent.
- Fix: read the `includes:` of every `.neon` file and count each included file of the project's own as a control; or have `check-project.py` refuse a baseline that is not `.neon`.
- Weight: **should-fix**.

**6. A change to the gate's own file leaves one word in a record nobody reads.**
- Where: `bin/kit_repo.py` lines 269 to 281; `bin/gate.py` line 583; `bin/ship.py` lines 336 to 340 and 527 to 529 (it reads `result` and `commit` from the record and nothing else).
- Evidence: in a second clone of the kit I changed one line of `gate.py` so that every step passes. On a throwaway project whose tests and audit were both red: GATE: PASS, exit 0. The printed output does not mention the change. The record says `kit_commit: fec74fb...+uncommitted changes`. With the unchanged kit the same project gives exit 1. A committed change to the kit leaves only a different commit ID, compared with nothing.
- What the documents say: spec 8.1 calls changes to the guard "instruction". For the gate, rule L-6.10 says it "cannot be loosened in the change that needs it green". That is true of a change in the app. The plan gate never refuses the kit's own files, so the same session can edit both.
- Fix: the gate prints a loud line and returns exit 3 ("controls changed: the kit itself has uncommitted changes") when the kit is not clean. The ship script refuses unless the kit is clean, and prints in the hand-over which kit commit judged the reviewed commit and which judged the shipped one.
- Weight: **should-fix**.

**7. One bad answer from production during the watch ends the ship with an alarm and without the hand-over.**
- Where: `bin/ship.py` lines 669 to 676 (a single unreadable answer raises the alarm at once) and 486 to 487.
- Evidence: a throwaway repository, an eight-second watch, production's version line answering 503 once, three seconds in, then fine again. Exit 4: "main is pushed, and production's version line can no longer be read (503)". The block "SHIPPED TO main. AWAITING GORDON'S DEPLOY" was not printed: no commit, no migrations, no names to set, no way back, no lines for the job file. The ship record says "ALARM". Run again: "SHIP: REFUSED. Nothing reached main. This commit is already main. There is nothing to ship." (That sentence contradicts itself: `main` is this commit.)
- Why it matters: the real watch is forty reads over ten minutes. This Mac lost its connection twice today. One timeout in forty gives Gordon an alarm that says deploy-on-push may be on, and leaves Claude without the hand-over the skill tells it to pass on.
- Fix: an answer that cannot be read is retried (say five times, a few seconds apart) and the watch goes on; only a CHANGED line is the alarm. If production still cannot be read at the end, say "could not be watched for N of M seconds" and print the hand-over all the same. Let a second run on a commit that is already `main` and has a ship record print the hand-over again and resume the watch.
- Weight: **should-fix**.

**8. The ship script cannot finish inside one command of a Claude Code session, and stopped half way it leaves `main` moved with nobody watching.**
- Where: `bin/ship.py` line 146 (the watch is 600 seconds at least); `skills/laravel-ship/SKILL.md` lines 56 to 61 (a plain command, "Let it finish: do not stop it early", nothing about how).
- What is wrong: the tool that runs commands in a session stops a foreground command after ten minutes at most, two by default (this session's own tool says so). The gate, the wait for staging and then a ten-minute watch are always longer than that.
- Evidence: a throwaway repository, the script stopped two seconds into its watch. Exit -15. The remote's `main` and the tag `v0.2.0` were at the commit. No hand-over was printed. The ship record says "awaiting Gordon's deploy". I then made the stand-in production show the new commit, as a site with deploy-on-push would. Run again: "This commit is already main. There is nothing to ship." Nothing noticed that production had moved.
- Not demonstrated: what the tool does at its limit in a live session. I showed the state the script leaves when it is stopped there.
- Fix: the skill says to run the ship script in the background with a time limit of thirty minutes or more, and to read its output when it ends. The script prints the hand-over BEFORE the watch (it has everything it needs once `main` is pushed) and the watch's verdict after. And the resume of finding 7.
- Weight: **should-fix**.

**9. When the remote takes the push and the answer is lost, the script says "Nothing reached main".**
- Where: `bin/ship.py` lines 627 to 630.
- Evidence: a throwaway repository whose stand-in for GitHub accepts the push of `main` and the tag and then cuts the pushing side off (a `post-receive` hook that ends the client, standing for a connection that drops after the server has answered). The script: exit 1, "SHIP: REFUSED. Nothing reached main. main and the tag could not be pushed. Nothing reached main, and the tag was removed again". On the remote, `main` and the tag were at the commit. The local tag was gone and no ship record was written. Run again: "already main". Production was never watched.
- Fix: when the push reports a failure, fetch and look. If the remote's `main` is the commit, say so, keep the tag, write the record and go on to the watch. If the fetch fails too, say "it is not known whether main moved" and stop with exit 4, not 1.
- Weight: **should-fix**.

**10. A migration edited after staging ran it is caught only when Claude wrote the `Staging:` line for the earlier commit.**
- Where: `bin/ship.py` lines 344 to 358. The mechanisms table says so honestly (row L-2.2: "from the job file's `Staging:` lines, which Claude writes").
- Evidence: a new migration at commit 1, pushed to staging by hand as laravel-code step 4 says. The file edited in commit 2, staging moved there. The job file holds a `Staging:` line for commit 2 only. `ship.py`: exit 0, `main` moved. (With a line for commit 1 it is refused, as the fixer says.) The clone knew better all along: `git reflog show origin/staging` listed commit 1.
- Fix: take the commits staging has stood at from git's own record of the pointer (the reflog of `refs/remotes/origin/staging`) as well as from the job file. That needs no line from Claude.
- Weight: **should-fix**.

**11. The deploy script tells the queue workers to restart before the site has switched to the new release.**
- Where: `deploy.sh` lines 257 to 258 (step 7, inside the script); `.kit/deploy-box.txt` lines 18 to 27 (take the host's own queue restart out; the switch comes after `bash deploy.sh`).
- What is wrong: the script requires releases in new folders, with the switch after it ends. A worker that is idle when step 7 runs stops at once and is started again from the folder that is still live, which is the old release. It then runs the old code against the new database until the next deploy. This app sends its mail from the queue.
- Not demonstrated: it needs a real site with workers. It follows from how `queue:restart` works (workers stop themselves; the host starts them again from the site's current folder) and from the order the deploy box is told to keep.
- Fix: the restart belongs after the switch. In the deploy box, keep the host's own queue-restart line as the last line, after the switch; take step 7 out of `deploy.sh` or leave it as a second, harmless one. Add it to the list "to confirm on the first staging deploy": after a deploy, the worker's process must have started after the switch.
- Weight: **should-fix**.

**12. The backup before a deploy: the plan says one thing and the template does another. Both are needed.**
- Where: `deploy.sh` lines 141 to 188; `plan-v2.md` section 9, first line; `hosting-options.md`, the backup schedule, second row.
- What each protects against:
  - *The template's copy* (a checked copy of the database beside it, on the same disk, ten kept): a migration or a release that damages the data. It is taken in seconds, needs no network and no installed package, and so can run first and stop the deploy every time. It does not survive losing the machine, and it does not hold the stored PDFs.
  - *The plan's archive* (database and PDFs, encrypted, to two other companies): losing the machine, the provider or the account, at the moment the database is about to change. It needs the app's packages and two outside services to answer.
- Which is right for the plan: the plan's words ask for the archive, so the template alone does not meet it. Make the deploy do both, in this order: the local checked copy first, as now, as the hard stop; then, after step 2 and before the migrations, the app's own backup command when the release has new migrations. Gordon decides one thing: whether a deploy stops when the off-site copy fails. My pick: stop when both places fail, warn and go on when one does. Otherwise an outage at Google would block a security fix.
- Weight: **should-fix** (a decision for Gordon; it is question 5 in the paperwork log and question 12 in the fixer's list).

**13. `laravel-new.py` lays nothing over the first app, and has no way to be told "keep the project's own file".**
- Where: `bin/laravel-new.py` lines 249 to 259 and 385 to 387.
- What holds: the fixer's change. A test file that was worked on is a CONFLICT and nothing is overwritten.
- Evidence: a stand-in project in the scratch folder with the first app's real `composer.json` and `phpunit.xml` and its tests layout (the files I may not read were stand-ins). The list: 27 files to create, 2 edits, 2 kept, and four CONFLICTs: `phpunit.xml`, `tests/Pest.php`, `tests/TestCase.php`, `phpstan.neon`. "RESULT: 4 conflict(s). Nothing was changed", with or without `--apply`. The only way to clear a conflict is to make the file equal to the template's, which for `phpunit.xml` would throw away the app's own settings.
- Fix: an option that lays every piece that does not conflict and lists the conflicts as "kept, merge by hand". Until then the stage that owns this works by hand, from the brief below.
- Weight: **should-fix**.

**14. The first app's own safety files are not controls to the gate.**
- Where: `bin/gate.py` lines 124 to 139. The list is fixed in the kit: the kit's own tests (`tests/Arch/Kit*`, `tests/Feature/Kit/`), `tests/Pest.php`, `tests/TestCase.php`.
- Evidence: in a throwaway repository, a branch that emptied `tests/RefusesRealServices.php` and one that weakened a test under `tests/Feature/Safety/` with the number of tests unchanged: "Controls changed: none", exit 0, both times. Those are the names of the first app's own second lock and its safety tests (from its tests layout and its `phpunit.xml`).
- Fix: let `.kit/project.json` name more control files for its project. The list can only add, and the file is itself a control. The stage that lays the template names the app's safety files there.
- Weight: **should-fix**.

### Minor

**15. A dry run says "every check before the first push passed" and the real run then refuses.** `bin/ship.py` lines 536 to 552: the check for a migration edited after staging sits after the dry run's exit. Shown: the same job, dry run exit 0, real run refused. Fix: move the check above line 536.

**16. The ship script can carry a tag it did not make.** With git's `push.followTags` set and a full tag `sneak-tag` on the reviewed commit, the stand-in for GitHub held `sneak-tag` and `v0.2.0` after the ship. A tag deploys nothing on this host. Fix: `--no-follow-tags` on the three pushes.

**17. The program that reaches staging is still found through the PATH.** The fix took the named variable away (`SSH_PROGRAM = "ssh"`, line 142). With a three-line program of that name first on the PATH, and the stand-in staging set to refuse every connection, the real, unedited `ship.py` gave exit 0 and moved `main`; no call reached the stand-in. Same kind as the last review's finding 16. Fix: `/usr/bin/ssh`.

**18. The gate clears the cached config and leaves the cached routes and events.** With `php artisan route:cache` run on `main`, and a branch that takes the `/version` route away, the test that asks for `/version` passed (it read the old cache). The gate was red all the same, because the kit's log-probe test noticed the cached routes. So a template project is covered by luck. Fix: clear all four (`config:clear`, `route:clear`, `event:clear`, `view:clear`).

**19. Two commands of the review skill can hand the reviewers the wrong material.** (a) `skills/laravel-review/SKILL.md` line 46: `php artisan migrate --pretend` runs against the local database. On the proof's project, which had already migrated, it printed "Nothing to migrate", so the reviewers would get an empty file. The gate's record already holds the text from an empty database (`migrate_pretend`); hand them that. (b) Line 35: for a merge whose result equals the other branch, the command names the other branch's last commit, not the merge. The ship script then refuses for want of a gate record, so it is safe, and the job sticks. Add `--full-history`.

**20. The copies before a deploy are kept by number, not by age.** `deploy.sh` line 184. After my 19 debug runs and one more deploy the folder held ten copies, all made within six minutes; the copies the proof itself had made two minutes earlier were gone. Ten retries of a bad deploy push out the last good copy. Fix: keep ten, and never delete a copy younger than, say, fourteen days.

**21. What else the gate does not list.** From the 33 one-change branches:

| Listed as "controls changed" | Not listed |
|---|---|
| the CI workflow, and a second workflow; `.github/dependabot.yml`; `phpunit.xml` and `phpunit.xml.dist`; `tests/Pest.php`; `tests/TestCase.php`; a kit test; `phpstan.neon`, a `.neon` baseline, a `.neon` in a subfolder; `pint.json`; `.gitignore`; `deploy.sh`; `.kit/deploy-box.txt`; `.kit/project.json`; the pre-push hook; `composer.json`: `config.audit`, `config.policy`, `config.allow-plugins`, `config.platform` | a PHP baseline (finding 5); the project's own safety files (finding 14); `.github/actions/` (a workflow can call it); `.github/dependabot.yaml` (whether GitHub reads that spelling: not checked); a `.gitignore` in a subfolder (it can make a database file trackable again); `.gitattributes`; `composer.json`: `repositories` (where packages come from) and `scripts`; `package.json` (what `npm run build` runs on the server); `bootstrap/app.php`; `config.sort-packages` (harmless, as the fixer says) |

The ones worth adding: a nested `.gitignore`, `composer.json`'s `repositories`, and `.github/actions/`.

**22. The skill's row for exit code 4 says more than the script knows.** `skills/laravel-ship/SKILL.md` line 70: "Deploy-on-push is on for the production site". Exit 4 also means the line could not be read (finding 7). And it gives no next step: the hand-over was not printed, so step 4 has nothing to pass on.

**23. One more way past the pre-push hook than its header names.** `git -c core.hooksPath=/dev/null push origin HEAD:main` moved `main` on the stand-in. The header names `--no-verify`, a clone without the hook, and the variable. Whether the guard refuses this text is the other reviewer's ground; I did not check.

**24. Registering the plan gate in the middle of a job shuts that job.** With nothing registered every job file gets the stamp "agent". The gate, once registered with the kit's setting as it is, refuses that kind: the walk showed "PLAN GATE (rule PG-1) ... its stamp is of the kind agent, which the gate does not accept", before and after the model and effort line. This is by design and the check says so. For Gordon's list: register the three plan-gate hooks between jobs, not during one.

## One job, walked through the skills

An invented job ("add a note to the thing") in a throwaway project, with the kit's real programs and nothing registered.

- **laravel-plan.** The preflight ran and reported what is true of a made-up project. No stamp is written without the hook.
- **laravel-write-plan.** `job-file.py write` refused ("no unused stamp record") and named the next command. With `--agent-stamp --plan-file` it wrote the job file; the stamp line says "agent". `check`: in shape.
- **laravel-code.** `job-file.py status` named the open job. The model and effort line went in. Gate green; `line gate PASS <commit>`; the branch and the staging pointer pushed by hand; `line staging <commit>`.
- **laravel-review.** The skill's own commands named the base (the remote's `main`) and the commit under review, and it was the gated commit. `line review PASS-WITH-NOTES <base> <commit>` gave the line the ship script reads.
- **laravel-ship.** `line ship-it`; version and change log committed with the job file; `check --job`: in shape; dry run exit 0; ship exit 0, `main` at the commit, the two lines for the job file printed in the shape `job-file.py` writes. Then `staging`, `shipped`, `deployed`, `closed`: all accepted, state "closed".
- **The next job.** `main` pulled, the records brought forward from the old branch (one file, four lines), a second job file written beside the closed one.

It sticks in four places: the ship script's length (finding 8), an alarm with no hand-over (findings 7 and 22), the reviewers' migration file (finding 19), and the stamp kind on the day the hooks are registered (finding 24).

## The brief: laying the template over the first app

**What I could see.** The app's `composer.json`, its `phpunit.xml` and the names of its test files, and nothing else: that was my limit. What I say about its other files comes from the earlier review, the app's build log and the stand-in run of finding 13, and is marked "check".

**The rule.** Do not run `laravel-new.py --apply` on `hdonline-v4`. Use it without `--apply` as a list. Lay the pieces by hand, on the app's branch, one piece to a commit, with the app's own test, lint and analysis commands after each. No other agent may be writing in the app while this runs.

**Never laid over. Keep the app's own file.**
- `phpunit.xml`. It already has both lines for every setting (`<env force="true">` and `<server>`), so the fixer's question 1 is answered: the app is protected. One thing is missing: a dummy `APP_KEY` pair. Add it by hand (step 4).
- `tests/Pest.php` and `tests/TestCase.php`. The earlier review found the kit's piece T4 present. Check that `check-project.py` still says so.
- `phpstan.neon`. It differs from the template's and passes the kit's check (T2). Keep it.
- `pint.json`. The earlier list showed it equal to the template's. Check. If it is not, keep the app's: the template's adds `declare(strict_types=1)` to every file, which changes behaviour.
- `composer.json`. I ran the program's own edit on the app's file: no change needed.

**The order.**

| Step | What | Risk |
|---|---|---|
| 1 | New files that nothing loads: `.kit/` (`README.md`, `deploy-box.txt`, `jobs/.gitkeep`, `hooks/pre-push` with its run bit, `project.json` with the name filled in and `production.live` false, `template.json`); `VERSION` and `CHANGELOG.md` with a heading for that version; `.github/workflows/gate.yml` and `.github/dependabot.yml`; `deploy.sh` with its run bit; `CLAUDE.md` from `templates/project-CLAUDE.md`, filled in as far as is known | none to the running app. Do not switch the pre-push hook on: that is Gordon's, after his first push |
| 2 | `.gitignore`: add the required block (`.env.*`, `!.env.example`, `*.sqlite*`, `*.db`, `*.sql*`, `*.dump`, `*.csv`, `/RELEASE`). `.gitattributes`: the line-endings line if it is missing. Then run `git ls-files -ci --exclude-standard`: it must print nothing | a test fixture kept as a `.sqlite`, `.sql` or `.csv` file becomes ignored: a new one is silently left out of the commit, and a tracked one fails the kit's check (decision 6) |
| 3 | The kit's PHP: `app/Support/Kit/`, the two `Kit...Command` files, `app/Http/Controllers/Kit/`, `routes/kit.php`, `app/Providers/KitServiceProvider.php`, and one line in `bootstrap/providers.php`. Then Pint, the analyser, the tests. Check by a test that `/version` answers without a login and that `/up` is there | the app already has its own lazy-loading and destructive-command switches. Setting them twice is harmless. See decision 2 |
| 4 | `phpunit.xml`, by hand: add the dummy `APP_KEY` pair, and a dummy pair for each name the kit's isolation test then reports | it is a control: the gate will list it, rightly |
| 5 | The kit's tests, one file at a time, each seen green before the next: `VersionLineTest`, `LogProbeTest`, `SafetySwitchesTest`, `IsolationTest`, `KitOutsideServicesTest`, and `KitRulesTest` LAST | `SafetySwitchesTest` runs `migrate:fresh` and `db:wipe` for real in a second process. The app's `phpunit.xml` pins that process to a database in memory, by the same two lines. Before its first run, take the rehearsal database's path out of the app's `.env`. `KitRulesTest` runs three of Pest's presets over all of `app/`: expect failures (decision 4) |
| 6 | `python3 bin/check-project.py <app>` must show T1 to T15, with only to-do lines (FILL IN, the hook not switched on). Then the gate | the gate compares with `main`, and the app's `main` holds only the installer's first commit (decision 7) |

**Decisions the stage will need, each with my pick.**
1. **The backup before a deploy** (finding 12). Pick: both.
2. **`migrate:rollback` on production.** If the app switches destructive commands off with Laravel's one line, that also refuses rollback, and the kit's test "leaves migrate:rollback usable" will fail. Pick: the kit's four named commands, so the written way back works. (Check: I could not read the app's provider.)
3. **The app's own safety files as controls** (finding 14). Pick: name them in `.kit/project.json` once the gate reads that list.
4. **The kit's architecture rules against the app's code.** Pest's security preset refuses `unserialize`, `md5`, `sha1`, `uniqid` and `rand` anywhere in `app/`; its Laravel preset wants mail classes queued and controllers with only the seven standard public methods. The importer reads WordPress's serialized values. Each failure is either a change to the app or a preset left out for this project (a listed control, Gordon's yes). Pick: keep the security preset and give the importer's one class a named exception.
5. **The browser tests.** The gate and CI run every suite in `phpunit.xml`, and CI installs no browser. Pick: a suite of their own that the gate does not run, named in the hand tests.
6. **Fixtures for the importer.** Pick: build them in code at test time, never as `.sqlite`, `.sql` or `.csv` files.
7. **The first `main` and the starting version.** The work is on `feature/v4-build`; the gate's "controls changed" will list everything against the first commit until `main` is the app. This is question 1 in the paperwork log. Pick: `0.1.0`, and Gordon's first push makes `main` the app as it stands after this stage.
8. **Where the queue restart goes** (finding 11), and the two already asked: the third-party CI action and setting Boost up.

## Not done, and not demonstrated

- Nothing here met a real Forge site or GitHub. Findings 8 (what the tool does at its limit) and 11 (the workers) say which parts rest on that.
- I did not look inside `hdonline-v4` beyond the three things my brief allowed, and ran nothing there. The brief above says where that leaves a "check".
- I did not attack the guards or the plan gate; they have their own reviewer this round. Finding 23 is the one thing I tripped over on that side.
- For finding 4 I edited `vendor/composer/installed.json` in the scratch project so the gate would start on the made-up lock file. That is a forgery made for the experiment, in a throwaway.
- I did not rerun the fixers' "each test fails on the old kit" comparison.
- The scratch folder (two clones of the kit, the proof's project and sites, the experiment scripts) was removed when this file was written.
