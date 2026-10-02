---
name: Home Directions v4 build log, app track
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: What the app track of the overnight build did, stage by stage: each stage's plan written before its code, then what was built, the commands run and their numbers, the decisions the documents did not settle, and what was left undone or refused
sources: ["[doc:build-handoff.md]", "[doc:plan-v2.md]", "[doc:laravel-kit-spec.md]", "[doc:requirements.md]", "[doc:phase0-brief.md]", "[doc:census-part2-2026-10-01.md]", "[gordon 2026-10-02]"]
status: live during the build that started 2026-10-02 00:55; one section per stage, newest last
---
# Build log: app track

The app lives at `/Users/gordonium/Dev/clc-laravel/hdonline-v4/` in its own git repository. This log holds no password, no client name and no real data.

## Stage P1: the skeleton (step C of plan-v2 section 7)

Builder: Claude, model `claude-fable-5-1` (Fable 5.1). I cannot see my own effort level; Gordon said he would raise it before the run [doc:phase0-brief.md, "I'll up you to Ultra before I go"]. Started 2026-10-02 00:55 CEST.

### Plan (written before any code)

**What.** A new Laravel app with the eleven tables of plan-v2 section 4, three seeded logins, the Dashboard, the File screen with entry by hand, and the duplicate prompts for client and property. Nothing of letters, invoices, mail, Calendly or the import beyond their empty tables.

**Order.**
1. Install: `laravel new` with SQLite and Pest, resolved on PHP 8.5 (a `php` shim that points at `php85`, so Composer resolves for 8.5); `herd isolate 8.5`; PHP requirement `^8.5`; Larastan 3, Pint (ships with Laravel), Laravel Boost as a development dependency (spec D8). `git init` inside the app folder only. The untouched installer output is the first commit.
2. Ground rules in code (kit spec sections 4 and 5): strict models with lazy loading refused outside production, the destructive-command switch outside local and testing, immutable dates, an enforced morph map, stray HTTP requests refused in tests, the required `.gitignore` entries and `.gitattributes`.
3. Tables, models, factories: `users` (with a role), `clients`, `properties`, `files`, `file_contacts`, `invoices`, `sends`, `settings`, `history`, `sources`, `old_links`. Every migration has a real `down()`. Enums for role, service, mode, status, stamp, contact role, send kind, source system. Money is whole cents.
4. Logins: a plain email and password login, rate limited, with log out. Three users seeded (owner, treasurer, admin) with generated passwords that live only in the app's `.env.example` and the local `.env`; the seeder refuses to run outside local and testing.
5. New File by hand: one form for the client (with a second person), the property, the job facts and the invoice description; one action class that creates the three rows in a transaction and fills the defaults (standard invoice text and price for the service, stamp by the property's state, inspector).
6. File screen: client and property shown and corrected on the same page, job facts, invoice description and price, "been here before", and the duplicate prompts.
7. Duplicate prompts: a matcher for clients (email first; otherwise the same name with a matching phone or mailing address) and for properties (the geocoded key when both have one; otherwise the normalised address). A match is only ever shown. One click links (the newer record is marked as merged into the older and its files are moved; no row is removed) or keeps apart (remembered, so it is not asked again).
8. Dashboard: New File, a search box (present, not yet working: search is stage P3), the recent files newest first, each with client, address, status and the next thing to do, loading further pages as the list is scrolled, with an ordinary "more" link when scripts are off.
9. Change history is recorded from the first day (who, what, from, to, when) because merges must be reversible through it (plan-v2 section 10); showing it is stage P3.
10. Confirm the site answers at `http://hdonline-v4.test`; run the full suite, Pint and Larastan; commit.

**How it is tested.** Pest, written with the code:
- feature tests for every screen and rule: login, log out, the rate limit, every app route refusing a guest, the seeder, the Dashboard (order, hidden files, paging, the fragment the scroll loads), New File (defaults by service, stamp by state, validation, time zone), the File screen (each correction saved and recorded in history), every duplicate rule in both directions (matches and non-matches), link and keep apart, and that linking a record the matcher did not suggest is refused;
- unit tests for the address normaliser, the money helper, the name and phone keys, the stamp rule;
- a schema test that every table of section 4 exists, that every model's factory makes a valid row, and that the migrations roll back and run again cleanly;
- architecture tests: strict types everywhere, no `dd`/`dump`, no `env()` outside config, controllers do not touch the database facade, naming and base classes of controllers, requests, models and enums.
List tests seed at least two parent rows, so a lazy-loaded relation fails the suite (kit spec section 4, performance).

Done means the suite, `pint --test` and Larastan all pass, with the commands and numbers recorded below.

### What was done (finished 2026-10-02 01:27 CEST)

**State: built, tested, committed. One thing is not right and needs Gordon: the Herd address answers with an error until Herd's web server is restarted (below).**

**What exists.** `/Users/gordonium/Dev/clc-laravel/hdonline-v4/`, its own git repository, no remote. Laravel 13.34.0, PHP requirement `^8.5`, SQLite, Pest 5.3.0, Larastan 3.12.2 at level 8, Pint 1.32.1, Laravel Boost 2.10.1 as a development dependency. 51 PHP files under `app/`, 14 migrations, 26 test files.
- Tables, each with a model, a factory and a real `down()`: `users` (with `role`), `clients`, `properties`, `files`, `file_contacts`, `invoices`, `sends`, `settings`, `history`, `sources`, `old_links`, plus `kept_apart` (see decisions).
- Logins: `/login`, `/logout`; five wrong tries then a pause; three local users seeded (owner, treasurer, admin) at invented `@hdonline-v4.test` addresses. The generated passwords are in the app's `.env.example` (committed) and `.env` (not tracked), nowhere else.
- Dashboard (`/`): New File, the search box (shows "Search is not built yet" when used), recent files newest first, 25 at a time, more rows fetched from `/files?cursor=...` as the list is scrolled; with scripts off the same item is a link.
- New File (`/files/create`): client with second person, property, job, invoice description and price on one form. Blanks start from the service's standard price and text (Settings first, then `config/hd.php`); the stamp follows the property's state unless one is chosen.
- File (`/files/{id}`): client and property corrected in place (one record each, so right on every file), job facts, invoice description and price, "been here before", and the duplicate prompts with one-click "same" and "different".
- Change history is written for clients, properties, files and invoices on every create and every changed field, with the user. Nothing shows it yet (stage P3).

**Evidence.** Run in the app folder on 2026-10-02, through Herd's PHP 8.5:

| Command | Result |
|---|---|
| `herd composer test` (which runs `php artisan test`) | passed: 302 tests, 935 assertions, 0 failed, about 3.2 s |
| `herd composer lint` (`pint --test`) | passed |
| `herd composer analyse` (`phpstan analyse`, Larastan level 8) | passed: 0 errors |
| `herd php artisan migrate:fresh --seed` on the local database | 14 migrations ran; 3 users: owner, treasurer, admin |
| `git log --oneline` | 8 commits; last `7eb7d60`; working tree clean; no remote |

The architecture tests are part of the 302: Pest's `php`, `security` and `laravel` presets, strict types everywhere, no debugging calls, `env()` only in config, controllers without the database facade or the HTTP client, final stand-alone actions and matchers. A test (`AccessTest`) fails if a route is added without being covered by the guest test and the policy test.

**The Herd address.** `curl http://hdonline-v4.test/up`:
- 01:01, before the PHP requirement was raised: HTTP 200, served by PHP 8.4.25.
- After `^8.5` was set and `herd isolate 8.5` was run: HTTP 500, still served by PHP 8.4.25, with Composer's message that the app needs PHP 8.5.
- Why: `herd isolate 8.5` wrote the site's own config (it points at the 8.5 socket) and reported "The site [hdonline-v4.test] is now using 8.5", but each request it made to the Herd app (is 8.5 installed, restart PHP, restart Nginx) timed out after two minutes; `osascript` to Herd returns "AppleEvent timed out (-1712)". Herd's Nginx has been running unreloaded since 23:58, before PHP 8.5 was installed at 00:32. So the config is right and the running server has not read it. Most likely a macOS prompt is waiting on screen for the Herd app; I did not try to get round it.
- What Gordon does: in the Herd menu, stop and start the services (or quit and reopen Herd), then `curl -I http://hdonline-v4.test/up` should say 200 and `X-Powered-By: PHP/8.5.x`. Later stages should re-run that check.
- What was confirmed instead: the app served for a minute by `php artisan serve` on PHP 8.5.10 at `127.0.0.1:8085` (then stopped): `/up` 200; `/login` 200 with the title "Log in · Home Directions", the form fields and the built stylesheet (200); `/`, `/files`, `/files/create` each 302 to `/login`.

**Not done, and why.**
- The Herd address does not answer 200 (above).
- Nobody has looked at the screens in a browser. The built-in browser was refused the local preview address, and logging in by hand needs Gordon's own say. The screens are covered by feature tests on their HTML; the look itself is unchecked. The browser tests of stage P4 will be the first real look.
- No demonstration data: the local database has the three logins and no files (stage P4 makes the demonstration set).
- `boost:install` was not run (see decisions).

**Refused or blocked.**
- The built-in browser would not open `http://127.0.0.1:8099` (a static preview of the screens with invented data). Not retried.
- The Herd app did not answer requests from the command line (above). Not worked around.
- Nothing was refused by the app's safety check.

**The installer's agent files.** `laravel new` put a `CLAUDE.md` and an `AGENTS.md` in the app that tell an agent to install PHP with a script from the web and to run `boost:install`. They are a vendor's text, not instructions (kit spec 5.9); I did not act on them and removed both in the second commit. They remain in the first commit for the record. The per-project rules file is the kit's to supply.

### Decisions the documents did not settle

1. **Front end: server-rendered Blade, Tailwind (as the skeleton ships it), one small plain script for the scrolling list. No Livewire, no Alpine.** Why: three screens of forms; every extra package is one more upgrade clock (kit spec 9.1); the superseded draft plan had also picked plain Blade.
2. **Login written by hand (one request class, one controller), no starter kit, no Fortify.** Why: three fixed users, no sign-up; the starter kits bring React, Vue or Livewire with them.
3. **The build is on branch `feature/v4-build`; `main` is the untouched installer output.** Why: kit decision D2 says `main` moves only at ship, and a review can read `main...feature/v4-build`. Later stages continue on this branch.
4. **One extra table, `kept_apart`.** Why: "keep apart" has to be remembered or the prompt comes back on every visit; the history table is a record, not a place to look things up.
5. **The duplicate prompt is asked on the newer record only, and "same" always keeps the older record.** Why: one question, in one place, with one meaning; the newer record's files move to the older and the newer is marked `merged_into`. Only a pair the matcher is suggesting can be answered (anything else is a 404).
6. **The address key is street, unit and city; state and zip are left out, and two records with different states are not a match.** Why: zip is missing on most old rows and state on some (census part 2); a key that needed them would hide the matches it exists to find.
7. **No geocoder yet.** `place_key` exists and the matcher uses it when both records have one; nothing fills it. Why: a geocoder is an outside account.
8. **`file_contacts` holds the person's own name, email and phone, not a link to `clients`.** Why: brokers and attorneys are not clients, and the plan describes them as people on a job.
9. **One invoice per file** (`invoices.file_id` is unique). Why: the plan speaks of "the invoice" of a file throughout. Stage P2 can lift it with a migration if a revised invoice needs its own row.
10. **`sources` has a `collection` column beside system and identifier.** Why: v2's jobs and contacts number separately, so an identifier alone is ambiguous.
11. **`files.mode`, `files.price` and `files.invoice_description` are nullable; client names are nullable.** Why: the old records do not always have them, and an invented value would be a false fact. Files opened in the app always have them (validated).
12. **`files.scheduled_at` is required, for hourly design work too** (the day the job is opened). Why: the recent-files list sorts on it.
13. **Dates are stored in UTC and typed and shown in `America/New_York`** (`HD_TIMEZONE`). Why: the server's clock should not decide what day a visit was.
14. **Deleting a file will be Laravel's soft delete on `hidden_at`.** Why: it is the framework's own "hidden and recoverable". The column and the behaviour exist; the button is stage P3.
15. **History is recorded now, shown later.** Why: a merge must be reversible through the history from the first merge on.
16. **Money is whole cents.** Standard prices and the three invoice texts are defaults in `config/hd.php`; a text saved in `settings` wins. Why: a fresh database must work before anyone opens Settings (kit lesson: nothing set up by hand outside a migration).
17. **The seeded logins use invented addresses and the seeder refuses to run outside local and testing.** Why: known passwords must never reach a server; real addresses do not belong in a repository.
18. **Boost is required as a development dependency (spec D8) but `boost:install` was not run.** Why: it writes agent configuration (`CLAUDE.md`, `AGENTS.md`, `.mcp.json`, skills), which belongs to the kit's project template and to Gordon, and D8 says its rule store stays off.
19. **Larastan level 8**, analysing `app`, `database`, `routes`, `bootstrap/app.php` and `config/hd.php` (not the framework's stock config files). Why: the research suggested 6 rising to 8; a new codebase can start at 8.
20. **The status can be set by hand on the File screen.** Why: until letters and invoices exist, nothing else moves it.

### For the stages that follow

- Work on branch `feature/v4-build`. Run everything as `herd php ...` or `herd composer ...` in the app folder; the Mac's plain `php` is 8.4 and the app refuses it.
- The service list is opinion, design, hourly, as the plan writes it. The import (P4) will meet inspections and consultations; `files.service` is a plain string column, so only the `Service` enum grows.
- The architecture tests' `security` preset forbids `unserialize`; the importer needs it for WordPress's serialized links and will have to say so in that test, in the open.
- A corrected state on a property does not change the stamp of its files; the stamp is set when the file is opened and by hand after. Stage P2 (letters) should decide whether an open file's stamp follows a corrected state.
- The destructive-command switch is on outside local and testing. In Laravel 13 it also blocks `migrate:rollback` (kit spec section 4); the kit has still to settle how a rollback is run on a server.
- `password_reset_tokens` is the skeleton's table and is unused: there is no "forgot password" until mail exists.
- The local logins' passwords are the three `SEED_PASSWORD_` lines of `.env.example`.

## P1 fixes

Fixer: Claude, model `claude-fable-5-1` (Fable 5.1). I cannot see my own effort level. I wrote neither the code nor the two reviews (`reviews/app-P1-plan-fit.md`, 24 findings; `reviews/app-P1-safety.md`, 17 findings). Started 2026-10-02 02:00 CEST from commit `7eb7d60`, 302 passing tests (rerun by me before touching anything: 302 tests, 935 assertions).

### Plan (written before any change)

Each finding is checked against the code first. Every fix has a test written to fail before it. Small commits, in this order, safety first because a later stage points the app at real data.

1. **The tests can never touch a real database** (safety 6). `force="true"` on every line of `phpunit.xml`; the base test case refuses to start unless the environment is `testing` and every SQLite connection is in memory (or a file under the test's own temporary folders). Proof: a test that starts the suite's own runner in a child process with `DB_DATABASE`, `APP_ENV` and `MAIL_MAILER` set to hostile values and a marker row in the named file, and finds the marker still there.
2. **SQLite fit for a server** (safety 4, plan-fit 24c): write-ahead journal, busy timeout, foreign keys, immediate transactions, read back from a file database in a test.
3. **Nothing dangerous reaches a server** (safety 1). `.env.example` becomes the file a server may start from (production, debug off, no local address, no password); a test reads it and fails on any of those. One rule for "this is a developer's machine" (environment local or testing, and a local address), used by the seeder's refusal and the destructive-command switch; debugging is forced off wherever the address is not local. The three local logins get passwords generated at seed time into a file git ignores; the three values that sat in `.env.example` are burned and are taken out of this Mac's `.env` and database.
4. **A proper way to give a server its logins** (safety 2, plan-fit 12): one command that creates the person and either mails a set-your-password link or takes the password at a hidden prompt; never an argument, never a file, never the log. Tinker moves to the development packages (safety 14).
5. **The login** (safety 3, 9, 13): limits on the email alone and the address alone beside the present pair; every failure, lockout and login logged without the password; emails compared in lower case; "keep me logged in" shortened.
6. **Small hardening** (safety 10, 11, 12): trusted host, protective headers and no-store behind the login, robots kept out, a forged page cursor shows the first page.
7. **History that cannot be bypassed** (safety 5, 8; plan-fit 3, 4, 14, 22): hide and restore are events; every act's rows share a batch identifier; the history table refuses updates and deletes in the database itself; models refuse to be destroyed; a test fails if app code uses the quiet or bulk ways round the models.
8. **Tables that can hold the old data** (plan-fit 5, 6, 7, 8, 23, 24b): service, stamp, the street, the invoice number and amounts become nullable; inspections and consultations become services that are not offered for new files; sources become unique and carry what has no column here; link columns indexed; `merged_into` renamed. The rules for rows made by hand are not weakened: a model refuses an incomplete row unless it is created through the one import entry point, which writes its source in the same step.
9. **Forms that assert nothing by themselves** (plan-fit 9, 18): no preselected state or mode; a correction validates what was changed and does not demand blanks an old row never had.
10. **The working list** leaves out cancelled files (plan-fit 10).
11. **Matching** (plan-fit 2, 15, 16, 24a): suggestions in both directions; one base matcher and one controller; the second person and seven-digit phones; the address key's holes.
12. **"Same" keeps what was typed** (plan-fit 1, 3, 17): the record kept is the one with the earliest job; per field, the details from the more recent job win where they are filled, blanks never overwrite, names stay as on the record kept, notes are joined; every change is a history row in the merge's batch; a merge can be undone and a "keep separate" asked again, both from the file and both recorded.
13. **The other people on a job** (plan-fit 11): a panel to add, correct, copy and take off, with history.
14. Whatever tests plan-fit 14 lists that the above did not already add.

Not planned as code here, with the reason given per finding below: the version line and the log probe (the kit's template, stage K2, is building them), the status design and the `sends` columns (the reviewer hands both to P2), one invoice per file and the roles (Gordon's to say).

### What was done (finished 2026-10-02 03:05 CEST)

**State: fixed, tested, committed.** 14 new commits on `feature/v4-build`, `900781f` to `c5e734f`; working tree clean; no remote, nothing pushed. Of 41 findings: 34 fixed, 1 not a demonstrated problem, 4 left for Gordon, 2 not done because they belong to another stage (the kit's template; P2).

**Evidence.** Run in the app folder through Herd's PHP 8.5.10 at 03:02:

| Command | Result |
|---|---|
| `herd composer test` | passed: 597 tests, 2,007 assertions, 0 failed, about 4.4 s (was 302 tests, 935 assertions) |
| `herd composer lint` | passed |
| `herd composer analyse` (Larastan level 8) | passed: 0 errors |
| `herd composer audit` | no advisories |
| the same suite with `DB_DATABASE`, `APP_ENV=production`, `MAIL_MAILER=smtp` set in the shell, against a scratch database shaped like the app's | 597 passed; the database's two tables and its marker row untouched |
| today's tests run against the code as it stood at `7eb7d60` (a scratch worktree, removed afterwards) | 116 pass, 481 fail or error |
| `herd php artisan migrate:fresh --seed` on this Mac's local database | 14 migrations; 3 logins; journal mode `wal` |
| the app served on `127.0.0.1` for a minute, as a visitor | `/up` 200, `/login` 200 with the five protective headers, `/` and `/files/create` 302 to `/login`, `/robots.txt` 200 |
| this Mac's log after some thirty runs of the suite, searched for every password the tests use | 0 occurrences in 452 lines |

**Where Gordon finds the local passwords.** `storage/app/private/local-logins.txt` in the app folder (git ignores it; readable by its owner only). The README says so. The seeder made three new ones; the three that were committed in `1e56e71` open nothing any more: they are out of `.env.example`, out of this Mac's `.env`, and the local database was rebuilt.

**Not looked at in a browser.** As before, nobody has seen the screens; the new panels (other people on a job, linked records, "ask me again") are covered by feature tests on their HTML only. `http://hdonline-v4.test/up` still answers 500 from PHP 8.4 until Herd's services are restarted (unchanged since the build; not mine to work around).

**Nothing was refused by the app's safety check.** I did not log in to the running app: the login is covered by tests.

### Per finding: plan fit (`reviews/app-P1-plan-fit.md`)

Each was checked against the code before anything was changed. All 24 hold.

| # | Finding | Outcome |
|---|---|---|
| 1 | "Same" drops what was just typed | **Fixed** (`4f541ac`). The record kept takes the other's details field by field (table below); every change is a history line in the merge's batch. Test: the reviewer's own case through the real routes. |
| 2 | Asked in one direction only, by row number | **Fixed** (`4f541ac`). Suggested in both directions; the record kept is the one with the earliest job, then the lower number, whichever file the answer is given on. Tests for both of the reviewer's cases (a correction on the older file; a 1995 record imported later). |
| 3 | No undo; history cannot tell one merge from another | **Fixed** (`e2da000` the batch and the events, `4f541ac` the undo). A `merged` line on the duplicate, one batch per act, `UndoMerge` reads the batch backwards, `AskAgain` withdraws a "keep separate" as a mark. Both are one click on the file. Merge, undo, merge again, undo again is tested. |
| 4 | Hiding a file writes no history | **Fixed** (`e2da000`): `deleted` and `restored` events, with the user. |
| 5 | `files.service` cannot hold the old jobs | **Fixed** (`b438579`, screens in `c69adb9`). Nullable; `Inspection` and `Consultation` added and never offered for a new file. |
| 6 | A job with no address needs an invented one | **Fixed** (`b438579`): street and key nullable; "Address not recorded". |
| 7 | Old invoices have no number; the number rule has no code | **Fixed as far as P1 goes** (`b438579`): number, wording, lines and amounts nullable for imported invoices, still unique. The generator (`HD-YYMM-NNN`, retry, a month's thousand used up) is P2's, as the reviewer says. |
| 8 | A source can be recorded twice | **Fixed** (`b438579`): unique per row; empty text for no collection; `HasSources` on all five models. |
| 9 | Forms fill in Connecticut and "site visit" | **Fixed** (`c69adb9`). |
| 10 | A cancelled file stays on the working list | **Fixed** (`a277b05`). |
| 11 | Nobody can see or enter the other people on a job | **Fixed** (`78d4cd1`). |
| 12 | No way to make a login on a server | **Fixed** (`3238f78`): `hd:user`. |
| 13 | One status line for two things | **Left for Gordon**, then P2 (question 2). The reviewer's fix is P2's to build; nothing at P1 can be derived from facts that do not exist yet. |
| 14 | Important rules with no test | **Fixed** (`e2da000` models refuse deletion; `b438579` a test per constraint; `c69adb9` old-shaped rows on every screen; `4ac9a6d` two rows in each list, and a test that the lazy-loading refusal is in force). |
| 15 | Holes in the address key | **Fixed** (`4f541ac`), except a hamlet against its town, which only a geocoder can solve, as the reviewer says. |
| 16 | Client matches that are missed | **Fixed** (`4f541ac`): either person of a couple; seven-digit numbers. Also found while there: two nameless clients on one phone were suggested as "same name", because "Unnamed client" was being used as a name; no longer. |
| 17 | "Keep separate" does not follow a merge | **Fixed** (`4f541ac`), and undone with the merge. |
| 18 | Old records refuse a correction until unrelated blanks are filled | **Fixed** (`c69adb9`): a correction is held to the rules for what it changes; New File is as strict as before. |
| 19 | Two things the importer must know | **Fixed as far as P1 goes** (`b438579`): `Model::importFrom()` goes through the model, so keys and history are written, and a test says so. The display-name point is a note for P4 (below). |
| 20 | One invoice per file | **Left for Gordon** (question 1). The unique rule stays, and now has a test. |
| 21 | `sends` has one recipient and no failure | **Not done: P2's**, by the reviewer's own fix ("P2 decides"). Noted below. |
| 22 | History cannot name the source of a replacement | **Fixed** (`e2da000`): `history.source_id` and `HistoryEntry::takingFrom()`. |
| 23 | No indexes on the link columns | **Fixed** (`b438579`). |
| 24 | Three idiomatic points | **Fixed**: one controller and one base matcher (`4f541ac`); `merged_into_id` (`b438579`); SQLite (`f64748d`). |

### Per finding: safety (`reviews/app-P1-safety.md`)

| # | Finding | Outcome |
|---|---|---|
| 1 | `.env.example` says local, debug on, carries the passwords | **Fixed** (`e48a33d`). The file is written for a server and a test parses it. One rule (`DeveloperMachine`: the local environment at a local address, or the tests) now decides the seeder, the destructive commands and the debugging page, so a server left in local mode is still protected. Tests for production, staging and "local with a real address". |
| 2 | No way to give a server its users or replace a password | **Fixed** (`3238f78`). |
| 3 | Wrong passwords counted per pair only; nothing logged | **Fixed** (`d28d1bf`): 5 a minute per pair, 20 an hour per email, 30 an hour per address; every failure, lockout, login and password set logged without the password. A second factor or a gate in front of the login is question 7. |
| 4 | SQLite fails with "database is locked" | **Fixed** (`f64748d`). |
| 5 | History can be bypassed; hiding leaves no entry | **Fixed** (`e2da000`): events for hide and restore; the table refuses update and delete by trigger; a test reads the app's code for the quiet and bulk ways round the models. |
| 6 | The tests emptied a database named in the shell | **Fixed** (`900781f`). **The reviewer's fix was not enough:** `force="true"` sets `getenv()` and `$_ENV`, and Laravel reads `$_SERVER` first, so a shell variable still won. Each setting is now pinned twice (a forced `<env>` and a `<server>` twin), and the base test case refuses to start unless every SQLite connection is in memory. Proof is a test that runs the runner in a child process under a hostile shell. |
| 7 | No version line, no log probe | **Not done: the kit's.** Stage K2 is building both into the project template right now; writing a second version here would fork it. Due before the first deploy, as the reviewer says. `/version` answers 404 today. |
| 8 | "Nothing is destroyed" is a habit, not a property | **Fixed** (`e2da000`, `78d4cd1`). |
| 9 | "Keep me logged in" lasts 400 days | **Fixed** (`d28d1bf`): 30 days. The number is Gordon's (question 6). |
| 10 | The app believes any host name | **Fixed** (`c9bd072`): on a server it answers only for `APP_URL`'s name. Trusted proxies are not set: question 5. |
| 11 | No protective headers; pages may be cached; robots invited | **Fixed** (`c9bd072`). Not done: a full content security policy (only `frame-ancestors`, until the screens are final) and `X-Powered-By`, which is PHP's own setting on the server. |
| 12 | A forged page cursor is a server error | **Fixed** (`a277b05`). |
| 13 | Capitals in the email are another address | **Fixed** (`3238f78`, `d28d1bf`). |
| 14 | Tinker is installed on servers | **Fixed** (`3238f78`): a development package now; versions in the lock file unchanged. |
| 15 | The three roles decide nothing | **Left for Gordon** (question 3). |
| 16 | Three real names in the repository | **Left for Gordon** (question 8). |
| 17 | Timing of a wrong password | **Not a demonstrated problem**, in the reviewer's own words: no difference was measured here, and it cannot be measured without the server. Nothing changed. |

### What the record kept takes on "same" (the per-field decision)

The record kept is the one with the earliest job. "Fresher" is the record whose details were given more recently: typed or corrected here by a person counts from that moment; an imported record nobody has corrected counts from its last job, however recently it was imported.

| Field | Rule |
|---|---|
| Client email; mobile, home and work phone | the fresher record's when it has one, otherwise the other's |
| Client mailing address | field by field as above when both give the same street or the fresher gives none; the fresher address whole when it is another street (two addresses are never mixed) |
| Client names | as on the record kept; taken from the other only when the record kept names nobody. A different spelling stays visible on the row that was linked in |
| Client company | as on the record kept; filled when blank |
| Property state, zip, year built, place key | the fresher record's when it has one, otherwise the other's |
| Property street, unit, city | as on the record kept; filled when blank |
| Notes (both) | both, the record kept first |

A blank never overwrites anything. Every change is a history line with old and new, and the undo puts each back unless somebody has corrected it since.

### Decisions the documents did not settle

1. **The merge rules above**, including "fresher" and which record is kept.
2. **Old kinds of job are services that are never offered**, not a separate column. A type the importer does not recognise goes in as "not recorded", with the original word on the source row.
3. **The strict rules moved from the columns to the models.** A file, property, invoice or job contact made here without what it must have is refused (`IncompleteRecord`); `Model::importFrom()` is the one way round and writes the source in the same step.
4. **`sources.extra`** carries what the old system recorded and plan section 4 has no column for (question 4).
5. **The create-table migrations were edited in place**, and sources now runs before history. Nothing has run on any server and `main` is untouched, so the kit's "never edit a migration that has run" is not broken.
6. **`hd:user` works two ways:** a mailed link (good for 24 hours, once), or a hidden prompt where no mail exists yet. There is no "forgot my password" page.
7. **Debugging is forced off wherever the app's address is not local**, whatever the environment file says.
8. **`.env.example` carries a placeholder address** (`https://set-the-site-address.invalid`). Until `APP_URL` is set on a server, the app refuses every request there (400). Deliberate: a half-configured server fails loudly.
9. **The history is append-only by SQLite triggers**, which ties that protection to SQLite. The plan fixes SQLite.
10. **A row and its history are written in one transaction.**
11. **Taking a person off a job is a soft delete** (`removed_at`).
12. **The tests' log goes to the null channel, and the framework's fixed delay on password checks is off in tests only.**

### Questions for Gordon

1. **One invoice per file?** Hourly design work is billed "during [period]", which reads as several. Kept at one.
2. **One status line, or two facts?** Payment often comes before the letter; the plan's status line puts "sent" before "paid". P2 needs the answer before it builds on it.
3. **Should any of the three people be unable to do something** (change a price, link records, delete, change Settings)? Today all three can do everything.
4. **The old property facts** (square footage, water, sewage, house type, radon, water test): plan section 4 gives them no column, R7.8 says the database houses all the legacy data. They are carried unshown on the source row. Columns, or leave them there?
5. **Will anything sit in front of the app** (Cloudflare or another proxy)? If so it must be named as trusted, or the per-address login limit and the HTTPS detection go wrong.
6. **Thirty days for "keep me logged in", and the login limits** (20 wrong tries an hour locks an email for up to an hour, which a stranger could do to Peter on purpose): right?
7. **A second factor, or a gate in front of the login?** Three passwords guard ten thousand clients' details.
8. **The three real names in the repository:** intended?
9. **On "same", the newer contact details win by themselves and the names stay as on the older record.** Right, or should he choose per field on the screen?
10. **The three old local passwords are still in git history at `1e56e71`.** They open nothing. Rewrite the history before the repository gets a remote, or leave them?

### For the stages that follow

- **Any new database connection or outside service must be pinned in `phpunit.xml`, twice** (a forced `<env>` and a `<server>` twin). P4's old-system connection especially: until it is pinned to `:memory:`, every test refuses to start, with a message that says what to add. That is the point.
- **P2.** The invoice number generator (finding 7). The status design (finding 13, question 2). `sends`: one row per recipient or a `cc` column, and a failure with its reason (finding 21). An invoice made here must have a number, wording, lines, subtotal and total, or the model refuses it. `hd:user` mails its link through whatever mailer is configured and refuses the log and array mailers on a server. Who is copied is `file_contacts.is_copied`, and a copied person always has an email.
- **P3.** The history is ready to show: events `created`, `updated`, `deleted`, `restored`, `merged`, `unmerged`, `kept_apart`, `asked_again`; one `batch` per act; `HistoryEntry::subject` finds hidden files. "Undo the link" and "Ask me again" already exist under the Client and Property panels and can move into the history panel. Deleting a file is `$file->delete()`; the history line writes itself. Search must still find cancelled files.
- **P4.** Import every row with `Model::importFrom(system, collection, identifier, attributes, extra)`: it goes through the model (keys, history) and writes the source. Leave the display name empty unless the old system truly had a separate one. An unknown job type is null, with the original in `extra`. A job with no client gets a client row with no name ("Unnamed client"); a job with no address gets a property row with no street. A job with no date cannot be stored and must be listed, not guessed. The merge treats an untouched imported record as being as old as its last job, so the job dates must be right. `sources` refuses the same source twice for one row, which is what makes a second run safe.
- **The deploy script and the kit.** The version line and the log probe (finding 7). The script should stop unless the environment is staging or production and debugging is off. A server's environment must set `APP_KEY`, `APP_URL` and `DB_DATABASE` (an absolute path outside the release folder), and a real mailer before `hd:user` can mail a link. `migrate:rollback` is refused on a server along with fresh, refresh, reset and wipe. With the write-ahead journal the backup must use SQLite's own backup, never a copy of the file. `expose_php` off is a server setting.
- **Paperwork (W2).** `.env.example` holds no password any more, so the settings' names can be read from it.

## P2

Stage P2: letters, invoices and mail (steps D and E of plan-v2 section 7), against stand-ins only.

Builder: Claude, model `claude-fable-5-1` (Fable 5.1). I cannot see my own effort level. I wrote none of P1 and neither review. Started 2026-10-02 03:10 CEST from commit `c5e734f`; before touching anything I reran the suite: 597 tests, 2,007 assertions, all passing.

No Google, Brevo or Calendly account exists for this app. Nothing in this stage calls one, and no credential was looked for. What I did read from the web, once each, are the public manual pages the real implementations are written against: Google's Docs API pages on requests and named ranges, and Brevo's pages on sending a transactional message, its delivery notices and creating a notice. [web:developers.google.com/workspace/docs/api 2026-10-02] [web:developers.brevo.com 2026-10-02]

### Plan (written before any code)

**What.** Everything between "a file exists" and "the client has the invoice, the letter and a paid copy, and the system can show what was sent": the letter as a Google Doc made from a template and kept right when a name or address is corrected; the invoice with its number and a real PDF; send, mark paid, resend; mail through one wrapper with a trap; the message log and the receiving end for Brevo's delivered and opened reports; the Settings the two steps need (three invoice texts, the template for each service, the two stamp images).

**Order.** Small commits, each with its tests.

1. **Ground.** New migrations (never an edit of P1's): on `files`, the letter's name, what was last written into its tagged places, and when the letter was first sent; on `sends`, one row per recipient (who it went to, as what, who it was meant for when the trap redirected it), one identifier shared by the rows of one message, and a failure with its reason (plan-fit finding 21). A `records` disk for the PDFs that are kept. Settings for the two drivers, pinned in `phpunit.xml` twice each, and the test start-up guard taught to refuse a real Google or Brevo setting.
2. **Status from facts** (plan-fit finding 13, which P1 left to this stage and Gordon has not answered): the next step is worked out from what has happened (visit made, letter sent, invoice sent, invoice paid); "sent" and "paid" are set by the system when those things happen, in either order; a person sets only what only a person knows (booked, visited, drafting, closed, cancelled).
3. **Invoices.** The number generator (`HD-YYMM-NNN`, three random digits, never a number already used, a clear refusal when a month's thousand is gone). The invoice row is made with the file, in the same transaction, from the file's invoice description and price. A PDF renderer behind one class (dompdf, pure PHP, through Composer), with the firm's letterhead, "Bill to", what the job was, the description and price, the total, "Amount due" or "Paid", and how to pay. A preview on the file.
4. **Mail.** A Brevo transport for Laravel's own mailer, written against Brevo's documented interface with Laravel's HTTP client, so the suite's "no stray request" switch covers it; locally and in tests the framework's own log and array mailers are the stand-in. The trap, three locks deep: one rule (`live` means the production environment and an explicit switch); a listener that redirects every message to the trap address anywhere that is not live, or refuses when no trap address is set and the mailer could really send; and the Brevo transport itself refusing any recipient that is not the trap address when not live. The message log: one row per recipient, written whether the message left or failed.
5. **Send, mark paid, resend.** Send the invoice (PDF kept, the invoice marked issued); mark paid (who and when, a paid copy to the client); resend (the paid copy once paid). Each writes the change history.
6. **Delivery reports.** `POST /hooks/brevo`, closed unless the shared token matches, taking one report or a batch; delivered, opened and failed recorded on the right recipient's row; safe to receive twice; tested with made-up reports.
7. **Letters.** One interface for the Doc store. A real implementation against Google's Drive and Docs interfaces (copy, read, batch update, rename, share by link, export as PDF, revisions) with Laravel's HTTP client, exercised only against faked responses. A stand-in that keeps each Doc as a small file on the local disk and behaves the same way, with a page to look at a stand-in Doc. Both use one piece of logic for the tagged places, so the logic the tests prove on the stand-in is the logic the real one runs. The first fill turns each `{{tag}}` into a named range; later corrections replace the contents of those ranges and nothing else. A tag that can be empty and stands alone on its line (the address, the stamp) owns its line, so an empty one leaves no blank line and can still be filled later. Naming by the rule. The stamp by the property's state. A queued job creates the Doc when a file is opened and brings it up to date after a correction; a button on the file does the same at once.
8. **Sending a letter.** Share by link, PDF as it stands, revision noted, the client mailed the link and the PDF, people marked "copied" on the job copied, the PDF kept.
9. **Settings.** One screen: the three invoice texts, the template Doc for each service (a link or an identifier; one can serve all three), the two stamp images. Changes recorded in the history.
10. **File screen.** Invoice panel, letter panel, message log.
11. Architecture tests for the new rules (the HTTP client and dompdf each used in their wrapper only), the route-coverage test extended, the whole suite, Pint, Larastan; this log; commit.

**How it is tested.** Pest, with the code, on invented data. For letters: the naming rule case by case; each tag's value; the address block with and without a street; the stamp for Connecticut, New York, elsewhere and a virtual visit; a correction to a client's name with that same name typed into the body of the Doc, asserting the body is untouched while the name, the address block and the salutation change; the same for a property address; the real Google class against faked responses, asserting the exact requests it would send. For invoices: number format, uniqueness, a full month; the PDF is a real PDF with one page; the paid copy says paid. For mail: the Brevo transport against a faked Brevo (payload, key header, refusal); the trap in every environment, with and without a trap address, through the listener and through the transport alone; made-up delivery reports, including a repeat, an unknown message and a wrong token. Screens through their routes, with the history asserted for every action.

Done means `herd composer test`, `herd composer lint` and `herd composer analyse` pass, with the numbers below.

### Restart (second builder, 2026-10-02 08:50 CEST)

The first builder was cut off at about 04:00 when the connection dropped. It had made no commit and had not written its results here. I am a second agent: Claude, model `claude-fable-5-1` (Fable 5.1). I cannot see my own effort level. I wrote none of the code above.

**What I found.** 109 changed or new files on top of `c5e734f`, the plan above carried out through step 11 except this log and the commit. Before changing anything I ran the three checks on the tree as found: `herd composer test` 853 tests, 3,001 assertions, 0 failed; `herd composer lint` passed; `herd composer analyse` 0 errors. I then read every changed and new file.

**Plan for the restart (written before any change).**
1. Commit the tree as found, as one commit, so that what I keep and what I change afterwards is plain in the git log.
2. Fix what the reading turned up, each with a test written to fail first, each its own commit:
   - the tests write into this Mac's log file again whenever a test poses as staging or production (P1 had closed that);
   - a letter can be made twice (two Docs for one file) when the "Create the letter" button is pressed while the queued job is still making it;
   - filling the tagged places leans on a guess about how Google treats text put in at the very edge of a named range; make the result the same whichever way Google does it.
3. Look at a real invoice PDF and a stand-in letter with my own eyes (invented data).
4. Run the three checks, `composer audit`, and the hostile-shell proof again; write the results, the decisions and the list of what cannot be proven here; commit.

### What was done (finished 2026-10-02 09:25 CEST)

**State: built, tested, committed.** Steps D and E work end to end against the stand-ins. Nine new commits on `feature/v4-build`, `dadcc67` to `6ab6cf3`; working tree clean; no remote, nothing pushed. Nothing here has touched Google or Brevo, and no screen has been looked at in a browser.

**What exists now.**
- **Letters.** One interface (`App\Letters\LetterDocs`). The real store (`GoogleLetterDocs`) is written against Google's Drive and Docs interfaces and has only ever been run against made-up answers. The stand-in (`StandInLetterDocs`) keeps each Doc as a small file and is what this Mac and every test use. A letter is a copy of the template for the file's service, named `Home-Directions-letter_YYYYMMDD_property-address_client-name`, with the seven tags filled. Each filled place is a named range in the Doc, so a correction replaces what the range holds and nothing else, and renames the Doc. The address block closes up when the client has no street. The stamp follows the property's state (Connecticut, New York, otherwise none) for every job, virtual visits included.
- **Sending a letter.** The Doc is shared "anyone with the link can view"; a PDF is made of it as it stands and kept; the client is mailed the link and the PDF; the people marked "copied" on the job are copied; the message log notes the revision.
- **Invoices.** Made in the same act as the file, from the service's text in Settings. Number `HD-YYMM-NNN`, three random digits, unique (the table refuses a repeat too). A real PDF made here with dompdf. Send, mark paid (who and when; a paid copy goes to the client), send again.
- **Mail.** A Brevo transport for the framework's mailer; the framework's own `log` and `array` mailers stand in. From `office@homedirections.net`, with a copy to that mailbox. One line per recipient in the message log. Brevo's reports arrive at `POST /hooks/brevo`, closed without the token.
- **The trap.** Mail reaches a real client only where the environment is `production` **and** `HD_MAIL_LIVE=true`. Anywhere else every message goes to the one address in `HD_MAIL_TRAP`; with none set, a mailer that could really send refuses. Three places enforce it (the rule, a listener on every outgoing message, the Brevo transport itself).
- **Settings screen.** The three invoice texts, the template Doc for each service (one can serve all three), the two stamp images.
- **File screen.** Invoice panel, letter panel, message log. The status and the "next step" follow what has happened.
- **History.** Every action above writes it: opening, each correction, the Doc and its name, each send, the payment, each Settings change.

**Evidence.** Run in the app folder through Herd's PHP 8.5 at 09:19:

| Command | Result |
|---|---|
| `herd composer test` | passed: 868 tests, 3,054 assertions, 0 failed, about 10 s (597 before the stage; 853 on the first builder's tree) |
| `herd composer lint` | passed |
| `herd composer analyse` (Larastan level 8) | passed: 0 errors |
| `herd composer audit` | no advisories (dompdf 3.1 and what it brings are the only new packages) |
| the suite with `DB_DATABASE`, `APP_ENV=production`, `MAIL_MAILER=smtp`, `HD_MAIL_LIVE=true`, `HD_LETTERS_DRIVER=google`, a Brevo key and a Google token all set in the shell, against a scratch database with a marker row | 868 passed; the marker row and both tables untouched |
| this Mac's log file before and after a run of the suite | 11,668 lines both times (it grew by about 200 lines a run before the fix below) |
| one invented job run through the app outside the tests (local settings, a scratch database and scratch storage, nothing written into the project): open the file, type into the stand-in Doc, correct the name and the address, send the invoice, send the letter, mark paid | invoice `HD-2610-235`, $875.00; the Doc renamed and its tagged places corrected while the same misspelt name in the typed sentence stayed; six lines in the message log (invoice, letter, paid copy, each to the client and the office); three PDFs kept; status "paid", next step "Close the file" |
| the invoice PDF and the paid copy, opened and read | one page each: letterhead, number, date, "Bill to", "For", the description and price, "Amount due" (or "Paid October 2, 2026. Thank you."), how to pay |
| the letter's PDF as kept at sending in that run (the stand-in's plain rendering), opened and read | the corrected name, address block, "Re:" line and greeting; the misspelt name and the old street still standing in the typed sentence |

**What I kept of the first builder's work: nearly all of it.** I read every file. The design is sound and the tests are real: the "name in Peter's own sentences" test is there exactly as asked, on a file opened through the real routes. Its work is commit `dadcc67`, one commit, because it came as one piece and its parts lean on each other.

**What I changed, each with a test that failed first:**

| Commit | What was wrong | What it does now |
|---|---|---|
| `b92fbd4` | The tests wrote into this Mac's log again. `LOG_CHANNEL=null` reads as "no channel", and the framework only falls back to the null channel while the environment is "testing"; the mail-trap tests pose as staging and production. | The default channel names the null channel. A test poses as each environment and looks. |
| `1760146` | A file could get two Docs. On a server the letter is made by a queued job a moment after the file is opened; "Create the letter", pressed in that moment, copied the template a second time. | One at a time per file (a lock), and the second reads the file again and finds the first one's Doc. |
| `e9ded03` | Filling the places leaned on a guess. The address block's range starts exactly where the name's ends. The edits wrote the name at that edge while the address range already existed. If a Google Doc takes text at the edge into the range, the address range swallows the name, and the next address correction deletes the name from the letter. The stand-in assumed the other behaviour, so every test passed. | All our ranges are dropped first, the text is changed, and every place is named last by arithmetic. A test plays a Doc both ways and gets the same letter. |
| `b7fa134` | Every client message was headed with a link to this system's own address (the framework's default mail frame links to `APP_URL`). | The frame names the firm and links to `www.homedirections.net`. Found by reading what the log mailer wrote. |
| `c8a6eab` | Google's access token was remembered under one fixed name for 45 minutes, so a site given another Google account went on acting as the old one. | Remembered under a mark of the credential. A token Google rejects is replaced and the call made once more. |
| `7c47383` | A message Brevo refused showed as "Not delivered" with a link "The PDF as sent". | "Not sent", with the reason; no such link. |
| `c3d7124`, `6ab6cf3` | | README: what a server needs; one more test of the request Google is sent. |

**Not done, and why.**
- Nothing was sent to Google or Brevo; no account exists. The list of what that leaves unproven is below.
- Nobody has looked at the screens in a browser, as in P1. The panels are tested on their HTML. I did not log in to a running copy.
- `http://hdonline-v4.test` did not answer at all at 09:15 (it answered 500 after P1). Herd's services need Gordon's restart; not mine to work round.
- "Are you sure?" on the Send and Mark paid buttons, and an undo for a payment recorded by mistake: not in the documents; asked below.
- The from address as a Setting, the Calendly map, users and the Connections panel are stage P3's.
- This Mac's `storage/logs/laravel.log` still holds about 11,000 lines of noise from earlier test runs (invented data and stack traces, no password). I left it; it is ignored by git.

**Refused or blocked.** Nothing was refused by the app's safety check. I opened nothing under `~/Dev/hd-v4-import-data/` or Downloads and did not read `~/Dev/clc-plugins/`.

### Decisions the documents did not settle

The first builder's, as the code shows them (it left no list), then mine.

1. **The status follows the facts** (P1 plan-fit finding 13). "Sent" and "paid" are set by the system; a person sets booked, visited, drafting, closed, cancelled. Paid before the letter goes, the file stays as it is and the payment shows on the invoice. Why: payment often comes first, and Gordon has not yet answered P1's question 2.
2. **The message log has one line per recipient**, with who it was meant for when the trap sent it elsewhere, and a failure with its reason (finding 21). Why: Brevo reports per recipient.
3. **The invoice takes its wording and price from the file each time it goes out, until it is paid; then both are settled.** Why: one editable field, as the plan says; a paid invoice must not change.
4. **The invoice number's year and month are when the invoice is made**, on the firm's clock, not the job's date.
5. **The PDF library is dompdf.** Pure PHP, no browser on the server.
6. **The letterhead image and the "how to pay" lines** (check payable to the firm; Zelle to the firm's Gmail address, naming the Treasurer) are in the repository, taken by the first builder from the old system. I have not checked them against it. They are the firm's own facts, not client data.
7. **A message is sent while the person waits, not queued.** The kit says outbound work is queued. Why not here: the person who pressed Send is told at once whether it went, and the log needs the name Brevo gives the message.
8. **The office's copy is a blind copy.** The client does not see it.
9. **People marked "copied" get the letter, not the invoice or the paid copy.**
10. **Live means two things together**: the production environment and `HD_MAIL_LIVE=true`. Why: a staging site left in production mode, or a production site not yet meant to send, mails nobody. A trapped message says "[Test, meant for ...]" in its subject.
11. **Brevo's reports are let in by a bearer token.** Recorded: delivered, opened (the first), and as "not delivered" with the reason: a hard or soft bounce, a block, an invalid address, an error. Not recorded: clicks, deferrals, spam complaints, and opens by a mail program's privacy proxy (they do not mean a person read it).
12. **The app signs in to Google as one Google user, with a refresh token.** Not a service account. Why, as far as I can reconstruct it (unconfirmed): a service account cannot own files in an ordinary Drive folder on the Business Starter plan. Which user, and how narrow the permission can be made, is Gordon's (plan section 11, item 6).
13. **A tagged place is a named range in the Doc.** An address or a stamp alone on its line owns the line, so an empty one leaves no blank line and can be filled again.
14. **The date on the letter, and in its name, is the job's date.**
15. **The client part of the Doc's name is the surname** (both surnames of a couple who have two); the address part is street, unit and town.
16. **The greeting is by first name** ("Dear Ada and Ben,"); with no first name, the name on the record; with no name, "To whom it may concern:".
17. **The address block shows only when there is a street.** A town alone is not an address to write to.
18. **A corrected state moves the stamp** on files at that property whose letter has not gone and whose stamp was still the one the old state gave. A stamp chosen by hand, and the stamp on a sent letter, stay. (P1 left this to P2.)
19. **A correction reaches every letter of that client or property, sent ones included.** Only the stamp is frozen at sending. Why: R2.3 says fix it once, right everywhere. Asked below.
20. **Only a place whose value changed is rewritten.** What Peter retypes inside a place stays until the system has something new to say there.
21. **The letter is made by a queued job once the file is safely stored**, with a button to do it at once. Why: opening a file must never wait on Google.
22. **The client's link is the Doc's "preview" address**, which shows a page, not an editor (R3.6).
23. **A stamp image is given to Google by a signed address on this site, good for half an hour.** Until an image is in Settings, the place is empty and the file says so.
24. **The stand-in may be chosen on staging; production refuses it.**
25. **Settings are open to all three people**, behind one rule that can be tightened in one line (P1's question 3).
26. **Every PDF that goes out is kept by itself**, on a disk no web address reaches. A resend never overwrites.
27. **Google refuses a fill if the Doc changed since it was read** (so a letter being typed in is never edited on a stale reading); the job tries again later.
28. **A payment is recorded even when the paid copy cannot be sent** (no email address, mail down); the screen says the copy did not go.

Mine:

29. **The first builder's work is one commit.** Why: splitting it after the fact would have made commits that do not pass alone.
30. **One process at a time per letter**, waiting up to 20 seconds, the lock letting go by itself after 150. Why: the job's own time limit is 120.
31. **Every range of ours is dropped and named again on every fill**, the unchanged ones too. Why: it is the only way the result cannot depend on what Google does at a range's edge.
32. **The frame of every message names "Home Directions, inc." and links to `https://www.homedirections.net`.** The staff's set-your-password message uses the same frame.
33. **`LOG_CHANNEL=null` means "log nothing"** rather than "no channel", in every environment.

### What cannot be proven until the real Google and Brevo accounts exist

Google:
- That Google accepts each request as written: the copy into the letters folder, the batch of edits, the rename, the link sharing, the PDF export, the list of revisions.
- Which permissions the credential needs, and whether the Workspace's own rules allow "anyone with the link".
- That a refresh token keeps working. If the Google app is left in "testing" status its tokens may expire after a week (from memory; unconfirmed). The Google checklist should settle this.
- What a Doc does when Peter types at the very edge of a tagged place, deletes part of one, or cuts and pastes one. The system's own fills no longer depend on it; his typing still does.
- How the lines look after the address block closes and opens again (paragraph spacing and style).
- That Google can fetch the stamp image from the site, and how large it places it (no size is sent).
- That a letter full of photographs still exports as a PDF. Drive's export has a size limit (10 MB, from memory; unconfirmed).
- That the "revision" Drive reports is the one the PDF shows; there is a moment between the two calls.
- How often a fill is refused because somebody is typing in the Doc at that moment.
- The real template: that its tags are these seven, spelled this way, with the address and the stamp each alone on a line.
- That the "preview" link looks like a document to a client who is not signed in to Google.

Brevo:
- That Brevo accepts the message as built (sender, recipients, the PDF attached) and that the firm's sender is approved there.
- That the name Brevo returns for a message is the one its reports carry, with or without angle brackets.
- That Brevo can send its reports with a bearer token, one report per recipient, the copies included.
- That "opened" is switched on in the account, and what it reports for mail programs that hide opens.
- That a message to `office@homedirections.net` reaches the Gmail box (plan section 11, item 4).
- That real mail lands in inboxes, not in spam.

The server:
- The queue worker, the lock in the database cache, and that the kept PDFs survive a deploy.
- The trap on a real staging site: Gordon running one whole job and receiving every message himself (step E's gate).
- The screens, in a browser.

### Questions for Gordon

1. **Should a correction change letters that have already been sent?** Today a corrected name or mailing address is written into every letter that client has, old jobs included (the PDF kept at sending does not change). If a client moves, the address block of a three-year-old letter moves too.
2. **Which date belongs at the top of a letter:** the job's date (as now), or the day it is sent?
3. **Should Send and Mark paid ask "are you sure?"**, and should a payment recorded by mistake be undoable? Today each is one click, and a payment cannot be taken back.
4. **Which Google user does the app sign in as?** It must be able to read the template and own the letters.
5. **Are the "how to pay" lines and the letterhead still right?** They came from the old system. They also put the Treasurer's name and the firm's Gmail address in the repository (P1's question 8).
6. **Should anyone but the client and the office get the invoice?** Today the people "copied" on a job get the letter only.
7. **If a gate is ever put in front of the site** (P1's question 7), it must let two addresses through: Brevo's reports and Google's fetch of the stamp image.

### For the stages that follow

- **P3.** The message log is `sends`, one row per recipient, grouped on the screen by `batch`. History has a new event, `sent`, on the file (field = the kind, new value = who it went to); a failed send is in the message log only. Settings changes are in the history under subject `setting`. Still to build on the Settings screen: the from address (today `MAIL_FROM_ADDRESS`), the Calendly map, users, Connections. For Connections: `LetterDocs` and the Brevo transport have no "test me" call yet. A correction to a client or a property skips the letters of hidden files; the file screen offers "Bring the Doc up to date" once such a file is restored. A Calendly cancellation must decide "untouched Doc" from the Doc's revision: the stand-in counts revisions, and the system's own fills raise it.
- **P4.** A migrated letter needs `letter_doc_id`, `letter_name` and `letter_filled` set as `PrepareLetter` sets them. Without them the first correction renames the Doc by the rule and looks for tags the Doc may not have (it then writes nothing, which is harmless, but the name changes). An imported invoice has no number and cannot be sent from here (by design: it is a record). Pin any new connection in `phpunit.xml`, twice, and add it to `tests/RefusesRealServices.php`.
- **Paperwork (W2) and the deploy script.** New settings, all in `.env.example` with a comment each: `BREVO_KEY`, `BREVO_WEBHOOK_TOKEN`, `HD_MAIL_LIVE`, `HD_MAIL_TRAP`, `HD_LETTERS_DRIVER`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`, `GOOGLE_LETTERS_FOLDER`; optional `HD_MAIL_OFFICE_COPY`, `HD_RECORDS_PATH`. A server needs a queue worker and `MAIL_MAILER=brevo`. Staging: `HD_MAIL_LIVE=false` and `HD_MAIL_TRAP` set to Gordon's address. The nightly archive must include `storage/app/records/` (every PDF as sent, the stamp images). Brevo's notice is set up to call `https://<site>/hooks/brevo` with the token as a bearer token.

## P2 fixes

Fixer: Claude, model `claude-fable-5-1` (Fable 5.1). I cannot see my own effort level. I wrote neither the code nor the two reviews (`reviews/app-P2-plan-fit.md`, 20 findings; `reviews/app-P2-safety.md`, 12 findings and three notes). Started 2026-10-02 09:50 CEST from commit `6ab6cf3`, working tree clean. Before touching anything I reran the suite: 868 tests, 3,054 assertions, all passing.

### Plan (written before any change)

Each finding is checked against the code first. Every fix has a test written to fail before it. Small commits, in this order: what could mail a real client by mistake first, then what says "sent" when it was not, then the letter, then the invoice, then the small things.

1. **The live switch** (safety 1, the blocker). Live only when `HD_MAIL_LIVE` is the word `true`. A test reads the real `config/hd.php` with a table of words.
2. **Live is tied to the site's own name** (safety 2; plan-fit 18). A third line, `HD_MAIL_LIVE_HOST`, must name the host in `APP_URL`, so an environment file copied to staging is not enough. `.env.example` and the README say that staging sets `APP_ENV=staging` first; a test reads `.env.example`.
3. **A mailer that sends nothing is refused on a server** (plan-fit 1; safety 3). The same rule P1 wrote for `hd:user` (`DeveloperMachine`), applied to every client message, in the rule and in the listener. One test per environment.
4. **The last lock looks at what Brevo is handed** (safety 7), and the trap no longer writes addresses into the log (safety, closing note).
5. **Names cannot become links** (safety 4). One helper used by both mail views: what comes from a record is written so that markdown cannot read it as structure. **One-line fields refuse line breaks** (safety 12): one rule, used by both field lists.
6. **Written down first, sent second** (plan-fit 8; safety 5). The message-log lines are written before the mailer is called, in their own step, then completed as sent or failed. A message Brevo did not answer for is "not confirmed", never "not sent". Tests: the write after the send fails; Brevo times out.
7. **Nothing shared or kept before the app knows the mail can go** (plan-fit 9; safety 10). The address, the trap and the mailer are checked first; the Doc is shared last; a PDF is kept only when its message is about to be written into the log.
8. **Letters: a place the Doc does not have** (plan-fit 2, 19 in part). `fill` reports which tags it found. Only those are recorded as written. The file says which places the Doc lacks. A letter that still shows `{{...}}` is refused, naming the tag. Tags are read whatever their capitals. A named range Google reports in two pieces is left alone and reported.
9. **Letters: the stamp** (plan-fit 3, 7, 16). Text first, the picture in a second batch; if the picture fails, the text stays and the file says why. A Connecticut or New York letter is refused until its stamp is in the Doc. The stamp remembers which image it is, so a replaced image reaches unsent letters; a sent letter keeps the one it went with.
10. **Letters: names** (plan-fit 10, 11; safety 8). Each part of the name cut to 60 characters; `/` and `_` become hyphens; "Re:" with no service.
11. **Letters: one Doc per file even when Google's answer is lost** (safety 6). Each copy carries a mark kept on the file first; a second try looks for the mark before copying. **Google's access token is kept encrypted** (safety 11).
12. **Invoices: hourly work** (plan-fit 4). An invoice whose description still says "[period]" is refused, to send or to mark paid. The hours question goes to Gordon.
13. **Invoices: mark paid** (plan-fit 6, 14). A confirmation that names the client and the amount; "this was a mistake" takes a payment back, writes the history and sends nothing; a note when the file differs from the invoice as last sent.
14. **Invoices: an old unpaid invoice** (plan-fit 5). The safer reading: a person gives it a number from the file screen, after which it behaves like any other. The import numbers nothing by itself. Asked of Gordon.
15. **Invoices: small** (plan-fit 12, 15). A changed service offers its standard price and wording with one click; a full month is a notice, not an error page; the number is drawn inside a transaction wherever it is asked for.
16. **Delivery reports** (safety 9): a time out of range is "now"; one bad report does not stop the rest; a batch has a limit.
17. **A setting is never destroyed** (plan-fit 17).
18. **The tests plan-fit 20 lists** that the above did not already add: the letter job through a real database queue; the invoice PDF's own text; the naming rule's edge cases.

Not planned as code, with the reason given per finding below: the company on the invoice and the letter (plan-fit 13: Gordon's to say), the look of a Doc after a fill and the credential's reach (plan-fit 19: only the real Google can show them), the leftover working tree of an earlier agent (not mine to remove).

### What was done (finished 2026-10-02 10:25 CEST)

**State: fixed, tested, committed.** 14 new commits on `feature/v4-build`, `c02c9e9` to `9a61adf`; working tree clean; no remote, nothing pushed. Of 32 findings: 31 fixed (two of them to the safer reading, with the question below; one in the parts that can be shown here), 0 rejected, 1 left for Gordon. All 32 held when checked against the code.

**Evidence.** Run in the app folder through Herd's PHP 8.5 at 10:20:

| Command | Result |
|---|---|
| `herd composer test` | passed: 1,011 tests, 3,707 assertions, 0 failed, about 15 s (868 tests, 3,054 assertions before) |
| `herd composer lint` | passed |
| `herd composer analyse` (Larastan level 8) | passed: 0 errors |
| `herd composer audit` | no advisories; no package added |
| the suite with `DB_DATABASE`, `APP_ENV=production`, `MAIL_MAILER=smtp`, `HD_MAIL_LIVE=true`, `HD_MAIL_LIVE_HOST`, a trap address, `HD_LETTERS_DRIVER=google` and made-up Brevo and Google values set in the shell, against a scratch database with a marker row | 1,011 passed; the marker row, its one user and both tables untouched |
| the app's own reading of `HD_MAIL_LIVE` (`artisan config:show hd.mail`) with the word in the shell | `off`: false; `no`: false; `true`: true |
| this Mac's log file before and after a run of the mail, letter and invoice tests | 11,668 lines both times |
| one invented job run through the app outside the tests (local settings, a scratch database and scratch storage, removed afterwards): open, type in the Doc, correct the name and the address, send the invoice, send the letter, mark paid, take the payment back, mark paid again | invoice `HD-2610-008`; the Doc renamed and its places corrected while the typed sentence kept the old spelling; the stamp placed; eight lines in the message log, all "Sent"; four PDFs kept, each with its line; status "paid"; the file page answered 200 and showed "This was a mistake"; the mail as written read "Dear Ada," with no stray marks |

Every fix has a test that failed first. The tests for the letter changes could not even load before the fix (the interface they call did not exist); the others failed on the assertion.

**This Mac's local database** was migrated (`herd php artisan migrate`): one new migration adds three columns to `files`. The file page would fail on the old shape.

**Not looked at in a browser**, as before. The new notices and the two new confirmations are tested on their HTML.

**Nothing was refused by the app's safety check.** I opened nothing under `~/Dev/hd-v4-import-data/` or Downloads and did not read `~/Dev/clc-plugins/`.

### Per finding: plan fit (`reviews/app-P2-plan-fit.md`)

| # | Finding | Outcome |
|---|---|---|
| 1 | A server on the "log" mailer says "sent" | **Fixed** (`f926c49`). Anywhere but a developer's machine, a mailer that sends nothing is refused for every message, in the trap's rule and in its listener, with a notice that says what to set. Five environments tested. |
| 2 | A missing place is recorded as written; a letter can go out showing `{{...}}` | **Fixed** (`6e98ed3`). `fill` reports which tags it found. The file records only those, remembers the places the Doc lacks (new column `letter_unplaced`), and says so on the screen with a "Look again" button. A letter that still shows a tag is refused, naming it. Tags are read whatever their capitals. All three of the reviewer's cases are tests. |
| 3 | The stamp picture travels with the names | **Fixed** (`6e98ed3`). Both stores write the words first and the picture in a second batch. A picture that fails leaves the words in, the place empty, and the reason on the file; the queued job tries again. The requests are asserted against a faked Google that answers as its manual says for an image it cannot fetch. |
| 4 | An hourly invoice goes out for one hour, with "[period]" | **Fixed to the safer reading** (`66cafdd`), and asked below. An invoice whose description still says "[period]" is refused, to send and to mark paid. The file says so, and says when the price is still one hour's rate. Where the hours go is Gordon's. |
| 5 | An old unpaid invoice cannot be paid here | **Fixed to the safer reading** (`66cafdd`), and asked below. The file screen offers "Give this invoice a number" for an old invoice that is not paid; from then on it works like any other. The import numbers nothing by itself. Tested with an imported unpaid invoice, through to the paid copy. |
| 6 | "Mark paid" is one click and cannot be undone | **Fixed** (`66cafdd`). It asks first, naming the client and the amount. "This was a mistake" takes the payment back: the history keeps who recorded it and who took it back, the status steps back, nothing is sent. |
| 7 | A Connecticut or New York letter can go with no stamp | **Fixed** (`6e98ed3`). Refused until the stamp is in the Doc: no image in Settings, a picture that could not be placed, or a Doc with no place for it. "No stamp" on the file sends without one. |
| 8 | The mail leaves before anything is written down | **Fixed** (`386f889`). The lines are written first, then the PDF is kept, then the mailer is called, then the lines are completed. A message the system never heard back about is "Not confirmed" on the screen, with advice to look in the mail service's log before sending again. |
| 9 | Loose ends when a send fails halfway | **Fixed** (`386f889`). The address, the mailer and the trap are asked before anything else; the PDF and the revision are read before the Doc is shared; the Doc is shared last; a PDF is kept only once its line is in the message log; the invoice takes the file's wording in the same act that records it as sent. One case remains by its nature: if Brevo refuses after the Doc was shared, the Doc stays shared; the message log says "Not sent" with the reason. |
| 10 | A very long Doc name cannot be kept | **Fixed** (`c8ac981`). Each part cut to 60 characters; the longest name is 153. Tested through the real form at the lengths it allows. |
| 11 | Small things in the name and the text | **Fixed** (`c8ac981`): `/` and `_` become hyphens; a job with no service reads "Re: Services at ..." as its invoice does. Not changed: a name in a script with no Latin spelling still becomes `client`; the rule is letters and digits. |
| 12 | A changed service keeps the old price | **Fixed** (`66cafdd`). Nothing changes by itself; the file says the price and wording are still the other service's standard and offers the new one in one click. |
| 13 | A company is not named when a person is | **Left for Gordon** (question 3). The reviewer says to ask; old records' company fields are unchecked, so printing them is not the safer reading. |
| 14 | The paid copy can differ from the invoice sent | **Fixed** (`66cafdd`): the "mark paid" question says so, with both amounts. |
| 15 | A full month is an error page; numbers are safe only inside a transaction | **Fixed** (`66cafdd`). A notice on the form, nothing saved. `DraftInvoice` now opens its own transaction, so stage P3's Calendly intake is safe whatever it does. A test watches the number being read inside it. |
| 16 | A replaced stamp image does not reach letters already made | **Fixed** (`6e98ed3`). The file remembers which image it placed. A new image reaches the letters not yet sent; a letter that has gone keeps the one it went with (asked below). |
| 17 | A setting can be destroyed | **Fixed** (`3be2ea6`). |
| 18 | The example file gives every server `APP_ENV=production` | **Fixed** (`21202e4`): `.env.example` and the README say staging sets `APP_ENV=staging` first, and a test reads both. The code no longer rests on that line alone (safety 2). |
| 19 | The Google class: what could not be run | **Fixed where it can be shown here** (`6e98ed3`): a named range Google reports in two pieces is left alone and reported as a place the Doc lacks; tags in a header, footer or second tab now show up as places the Doc lacks; the PDF export is asked for as a PDF. **Not changed, because only the real Google can show them:** the look of a line after a fill (insert first, then delete), the credential's reach (Gordon's question 4 of P2), the refresh token's life. They stay on the list above, "What cannot be proven". |
| 20 | Important rules with no test | **Fixed** (`e0b38ff` and with each fix). Added: a server on a mailer that sends nothing; a tag sent, a place missing; Google refusing the picture; an hourly invoice as it goes out; an imported unpaid invoice; a letter with no stamp image; the write failing after the mail left; a send that fails after the PDF, at the revision, at the sharing; the letter job through the database queue, and put back on it when Google is out of reach; the invoice PDF and its paid copy read as text from the file itself; a town with no street, a first name only, a very long name. Two processes at one invoice number: the mechanism is tested (the number is read inside a transaction, and the database lets one writer in at a time); a real race is not run in the suite. No browser. |

### Per finding: safety (`reviews/app-P2-safety.md`)

| # | Finding | Outcome |
|---|---|---|
| 1 | The live switch reads "off" and "no" as on (blocker) | **Fixed** (`c02c9e9`). Live for the word `true` alone. A test reads the real `config/hd.php` with seventeen words. |
| 2 | Staging starts in production mode | **Fixed** (`21202e4`). Live now takes three lines: production, `HD_MAIL_LIVE=true`, and `HD_MAIL_LIVE_HOST` naming the host in `APP_URL`. A staging site given production's environment file still mails no client. |
| 3 | A server on the log mailer says "sent" and logs the whole message | **Fixed** (`f926c49`), with plan-fit 1. |
| 4 | Markdown in a name becomes a link | **Fixed** (`531765f`). The framework's own secured encoding for markdown mail is switched on. The reviewer's strings are the test: no link, no image, and the plain-text part reads as typed. |
| 5 | Sent first, written second; a timeout recorded as "not sent" | **Fixed** (`386f889`), with plan-fit 8. No answer from Brevo, an error of Brevo's own, or an answer without a message name is "not confirmed", never "not sent". Only a plain refusal (a 4xx answer) is "not sent". |
| 6 | A copy whose answer is lost is made again | **Fixed** (`6e98ed3`). Each copy carries a mark (Drive's `appProperties`) that is kept on the file before the copy is asked for; a second try looks for it first. Against the real Google this is written, not run. |
| 7 | The last lock looks at the envelope | **Fixed** (`0c635a4`): it judges the addresses the request is built from, and the envelope too. |
| 8 | A long name makes a letter impossible to send | **Fixed** (`c8ac981`), with plan-fit 10. |
| 9 | One odd report stops a batch; no limit | **Fixed** (`b89157f`). A report's time is believed only between the moment the message went and now; a report that goes wrong does not stop the rest; a batch over 500 is refused. |
| 10 | A letter is shared and kept before the app knows mail can go | **Fixed** (`386f889`), with plan-fit 9. |
| 11 | Google's access token in plain text in the database | **Fixed** (`6e98ed3`): kept encrypted with the app's key. |
| 12 | One-line fields accept line breaks | **Fixed** (`289381e`): one rule, on names, companies, phones, streets, towns, the people on a job and the inspector. Notes and the invoice description still take lines. An old record is not held to it for a field a correction leaves alone. |
| note | The trap writes addresses into the log | **Fixed** (`0c635a4`): how many, never which. |
| note | A leftover working tree and branch `p2-build` | **Not mine, left alone.** It is the first P2 builder's: three commits, all superseded by `dadcc67`. Question 8. |
| note | The Treasurer's name and the Gmail address in `config/hd.php`; corrections rewriting sent letters | Already asked of Gordon in P2 (questions 1 and 5 there). Unchanged. |

### Decisions the documents did not settle

1. **Live is three lines** (production, the switch, the site named). Why: a line can be mistyped and a file can be copied; a site's own address cannot be copied by accident. Gordon enters `HD_MAIL_LIVE_HOST` on production at go-live.
2. **Only the word `true` switches mail on.** "yes", "on" and "1" do not.
3. **"Not confirmed" is a third state of a message**, beside sent and not sent. A 5xx answer from Brevo and a timeout are both "may have gone".
4. **A message's PDF is kept just before it is sent, after its line is written.** So a PDF may be kept for a message that was then refused; its line says "Not sent" and the screen offers no "PDF as sent" for it.
5. **The invoice row changes only in the act that records it as sent.** Before, it was brought up to date first and stayed changed when the send failed.
6. **A place the Doc lacks is asked for again only when there is something new to say there, or when a person presses "Look again"** (or "Bring the Doc up to date", or Send).
7. **A letter that is to carry a stamp is not sent without it.** When Peter puts the stamp in by hand, the file must say "No stamp". Asked below.
8. **A sent letter keeps the stamp image it went with.** Asked below.
9. **The mark on a copy is a random identifier, not the file's number.** Why: a rebuilt database would give the same numbers to other files, and a file would adopt a stranger's Doc.
10. **A named range in two pieces is not written to.** Why: writing the value into each piece says it twice, and nothing shows that Google ever does this.
11. **An old invoice gets its number from a person, on the file.** The file takes the old invoice's price and wording where it has none, because here an invoice reads from its file.
12. **Taking a payment back sends nothing.** The paid copy that went stays in the message log.
13. **A report's time must lie between the moment the message went and now**, give or take five minutes; otherwise it is "now".
14. **Sharing a Doc writes no history line.** It is the last thing before the message, and the message log shows what became of that.

### Questions for Gordon

1. **Hourly design work: where do the hours go?** An hours box beside the rate, with the total worked out once and stored; or a price that starts empty. Today the price starts at one hour ($475), the file says so, and the invoice cannot go until "[period]" is replaced.
2. **Old invoices not yet paid at cutover: numbered by a person, one at a time (as built), or all of them by the import?** The old data may show many old invoices as unpaid that were paid long ago; that is why the import numbers none.
3. **Should the company print under the person's name** on the invoice and at the head of the letter? Today the company shows only when nobody is named.
4. **A Connecticut or New York letter is refused until its stamp is in the Doc.** Right? If Peter places the stamp by hand, he chooses "No stamp" on the file.
5. **A letter already sent keeps its stamp image when a new one is uploaded.** Right, or should old letters take the new image at their next correction?
6. **When a payment recorded by mistake is taken back, nothing is sent.** If a paid copy went to the wrong client, telling them is a person's call. Right?
7. **`HD_MAIL_LIVE_HOST` is one more line to enter on production at go-live** (the site's own name). It goes in the cutover runbook.
8. **The app repository still has a second working tree and a branch `p2-build`** from the first P2 builder (three commits, superseded). Remove both before the first push? Sancho's pick: yes.

### For the stages that follow

- **P3.** Ask `Outbox::check($file, $kind)` before doing anything for the sake of a message. A message-log line has a third state: `Send::isUnconfirmed()`. The Connections panel should show: whether the mailer is one that sends nothing; whether mail is live and, if not, which of the three lines is missing; Docs in the letters folder that carry a mark (`appProperties.hdLetter`) no file holds. A Calendly intake must validate names and addresses with `ClientFields` and `PropertyFields` (they now refuse line breaks). `DraftInvoice` is safe outside a transaction. New routes: `files.invoice.payment.destroy` (take a payment back), `files.invoice.number.store`. Taking a payment back is ordinary `updated` lines on the invoice (`paid_at` to nothing) in one batch with the status. `LetterDocs` has `find`, `placeholders`, and `fill` now returns what it placed.
- **P4.** Make each migrated Doc with the tagged places (or with the `{{tags}}` standing, and let `PrepareLetter` fill them); otherwise a correction only renames it and the file lists every place as lacking. A migrated letter whose stamp is already in its text must have `stamp` empty or `none` on the file, or it cannot be sent again from here. The stamp in `letter_filled` now reads `picture:ct@<image file name>`. Unpaid old invoices are not numbered by the import; put the old invoice's description and total on the invoice row, and they are carried to the file when a person numbers it. `files.letter_mark` is unique and may be empty.
- **Paperwork (W2) and the deploy script.** New setting `HD_MAIL_LIVE_HOST` (empty everywhere but production at go-live). Staging's list begins with `APP_ENV=staging`. A server must have `MAIL_MAILER=brevo` before any client mail: with `log` the app refuses and says so. One new migration since `6ab6cf3`.

## P3

Stage P3: Calendly (step F) and search, change history, delete and restore, Settings and Connections (step G) of plan-v2 section 7, against stand-ins only.

Builder: Claude, model `claude-fable-5-1` (Fable 5.1). I cannot see my own effort level. I wrote none of P1 or P2 and none of their reviews. Started 2026-10-02 15:45 CEST from commit `9a61adf`, working tree clean. Before touching anything I reran the suite: 1,011 tests, 3,707 assertions, all passing.

No Calendly, Google or Brevo account exists for this app. Nothing in this stage calls one and no credential was looked for. The real Calendly class is written from what I know of Calendly's public manual (version 2 of its interface: scheduled events, invitees, event types, webhook subscriptions, the signature header). I did not fetch the manual tonight; the paperwork track found two of its pages unreachable. So every detail of the real class is on the list of what cannot be proven here.

### Plan (written before any code)

**What.** Two things. F: a booking, a cancellation or a reschedule in Calendly does the right thing to a file, once, whether Calendly tells the system at once or the system finds it at its 15-minute check. G: search on the Dashboard, the change history at the foot of the File screen, delete and restore, and the rest of Settings with the Connections panel.

**Order.** Small commits, each with its tests.

1. **Ground.** New migrations, never an edit of an old one: a table of the bookings Calendly has reported (one row per booking, which is what makes "acted on once" a fact of the database); a table of the outside connections (when each last worked, what last went wrong, when trouble was last raised); on `files`, the Doc's revision as the system last left it and when the Doc was put in the trash; on `users`, a mark for a login that is switched off. Settings for Calendly and for the alert address, pinned in `phpunit.xml` twice each; the test start-up guard taught to refuse a real Calendly token.
2. **The wrapper.** One interface (`App\Calendly\Calendly`). A real class against Calendly's interface with the framework's HTTP client, run only against made-up answers. A stand-in that keeps "Calendly's side" as a small file on this machine and hands out bookings in exactly the shape Calendly sends them, so both roads go through one reader. The check of a notice's signature. A reader for the address a client types on the booking form.
3. **The intake.** One action that hears a booking by either road and acts once: opens the file with its client and property through the same door as New File (so the duplicate prompts are the same and nothing is merged by itself), or moves the date for a reschedule, or marks the file cancelled. A booking it cannot act on yet (its appointment type has no service in Settings; it was made before bookings were switched on) waits, visibly, and is taken up when that is put right. On a cancellation an untouched Doc goes to the trash and an edited one stays; the Doc store gets "put in the trash", "take out again" and the file remembers the revision the system left.
4. **The receiving address** `POST /hooks/calendly`: closed unless the signature matches and is fresh; safe to receive twice.
5. **The 15-minute check** as a scheduled command. It does nothing, quietly, while Calendly is not switched on. It also looks at whether Calendly's notices are still on, and raises it when they have stopped for a day or the check itself has failed for a day: on the screens, in the log, and by mail to an alert address when one is set.
6. **Delete and restore.** Two steps to delete (R2.6); for an upcoming Calendly booking the second step offers "also cancel it in Calendly", ticked. A deleted file can still be opened, found and restored. Both in the history.
7. **Search.** One box: words are looked for in the client's names and the property's address; a month ("May 2022", "5/2022", "2022-05") limits it to that month; both together work. Cancelled files are found; deleted ones on request. Tested on ten thousand files with a time limit.
8. **The change history** at the foot of the file, folded shut: one entry per act, newest first, with who, when, old and new, in plain words.
9. **Settings.** The from address; the Calendly type map (by the appointment type's name, so it can be set before any token exists); users (add, correct, send a set-your-password link, switch a login off and on); the Connections panel with a test button for Calendly, Google and Brevo, and the two backup stores shown as not set up yet. A page for the stand-in Calendly, so a booking can be made on this Mac by hand.
10. Architecture tests for the new rules, the route-coverage test extended, the whole suite, Pint, Larastan; this log; commit.

**How it is tested.** Pest, with the code, on invented data. Calendly: made-up notices and made-up answers in Calendly's shape; each kind of booking by each road, and by both roads in both orders, asserting one file; a reschedule and a cancellation arriving in either order; the signature with a wrong key, an old time and a changed body; the real class against faked responses, asserting the requests it would send; the check doing nothing with no token; the one-day alert by moving the clock. Search: each kind of query, and the ten-thousand-file timing. History, delete, restore and Settings through their routes, with the history asserted for every action.

Done means `herd composer test`, `herd composer lint` and `herd composer analyse` pass, with the numbers below.

### Restart (second builder, 2026-10-02 18:50 CEST)

The first P3 builder was cut off by a usage limit at about 16:10. Its unfinished work was committed by the orchestrating thread as `89c4118` on top of `9a61adf`. I am a second agent: Claude, model `claude-fable-5-1` (Fable 5.1). I cannot see my own effort level. I wrote none of the code above.

**What I found at `89c4118`** (the three checks run before anything was touched): `herd composer test` 1,015 tests, 718 passed, 261 failed; `herd composer lint` fails on two files (import order); `herd composer analyse` 14 errors. I read every one of the 93 changed and new files.

- The back end of the stage is there and sound: the Calendly wrapper (interface, real class, stand-in, the reader for Calendly's shape, the signature check, the address reader, the type map), the booking and connection tables, the intake that acts once by either road, the 15-minute check with its day-long alarm, delete and restore, the search, the two history readers, the user and Connections controllers, the scheduled command.
- **Not there:** every Blade view the new controllers render (the deletion page, the stand-in Calendly page, the history panel, the search results, the booking panel, the users and Connections panels, the from address and the type map on Settings), and every test of the stage. Two Larastan errors are those two missing views.
- **Why 218 of the 261 tests fail:** one line. `User::isSwitchedOff()` reads `disabled_at`; the user factory never sets it; the framework's `actingAs` marks the user as not newly created, so the strict model throws on the first request of nearly every feature test. The other 43 are the same fault seen from further away (a request that answered 500 wrote no message log, saved no setting), plus one architecture test (`StandInCalendlyController` has a public method the Laravel preset does not allow on a controller) and the route-coverage test, which does not yet know the eighteen new routes.

**Plan for the restart (written before any change).**
1. Green first, then commit: the factory sets `disabled_at`; Pint; the 14 Larastan errors (the two missing views made real; `SendPasswordLink` asks the mail trap first, which also stops a token being made for a link that cannot go; list types; a literal SQL string for the search's `like ... escape`; `createStrict` for a month); the check moved to its own invokable controller; the route-coverage test told the new routes; the one P1 test that asserted a deleted file answers 404, changed to the plan's rule (it opens, read-only, to be restored).
2. Then, in small green commits, each with its tests: the Dashboard search (words, month, both, deleted files, the scrolling list carrying the search), timed on ten thousand files; the File screen's change history (folded shut), its booking panel, the deleted-file banner with restore, the two-step delete with "also cancel in Calendly"; Settings (from address, Calendly type map, users, the Connections panel with its test buttons, the settings history); the Calendly tests (each kind of booking by each road and by both roads in both orders, reschedule and cancellation in either order, the signature, the receiving address, the check and its alarm with the clock moved, the real class against made-up answers, the stand-in page); README and `.env.example`; this log.

Done means `herd composer test`, `herd composer lint` and `herd composer analyse` pass, with the numbers below.

### What was done (finished 2026-10-02 19:40 CEST)

**State: built, tested, committed.** Steps F and G work end to end against the stand-ins. Seven new commits on `feature/v4-build` on top of the first builder's `89c4118`, `1fcff36` to `840e5e4`; working tree clean; no remote, nothing pushed. Nothing here has touched Calendly, Google or Brevo, and no screen has been looked at in a browser.

**What exists now.**
- **Calendly (F).** One interface (`App\Calendly\Calendly`). The real class (`CalendlyApi`) is written against Calendly's version-2 interface and has only ever been run against made-up answers. The stand-in (`StandInCalendly`) keeps Calendly's side as one small file and has a page of its own (`/stand-in/calendly`) where a person plays the client. A booking opens the file, the client and the property through the same door as New File (`OpenFile`), so the duplicate rules are the same: a likely match waits on the file for one click, nothing is merged by itself; every row a booking made is marked as from Calendly, as an imported row is. A cancellation marks the file cancelled and keeps it; a Doc nobody has written in goes to the trash, one somebody has stays, and it comes back when the file comes back to life. A reschedule moves the date (and the letter follows). Each booking is acted on once, by either road, in either order: one row per booking in `calendly_bookings`, what was done written on it in the same step. The receiving address `POST /hooks/calendly` takes only a notice signed with the server's key and not older than a day. The 15-minute check (`hd:calendly-check`, scheduled) hears what the notices did not bring, asks Calendly once per check and only about appointments whose state it does not already know, and raises a day of trouble (notifications switched off or gone; a booking that a notification should have brought with none arriving since; Calendly out of reach) on the Dashboard, in the log, and by mail to `HD_ALERT_ADDRESS`, once a day at most. Which appointment type is which service is a Setting; a booking whose type matches none waits, visibly, and is taken up when it does. Bookings are off until a person switches them on under Connections; bookings already in the calendar then wait for a person's word (bring them in, or leave them).
- **Search (G).** One box on the Dashboard: words in the client's names, company and email and in the property's address ("Road" and "Rd" alike), a month or a year on the firm's clock typed any of the ways Peter says it, both together; every word must be found; an invoice number finds its file; cancelled and closed files are found, deleted ones on request; the scrolling list carries the search.
- **Change history (G).** At the foot of the File screen, folded shut: every change to the file, its client, its property, its invoice and the people on the job, who, when, old and new, in plain words; "The system" and "Calendly" when nobody was signed in; the latest 500 lines of a long history, with a word to say so.
- **Delete and restore (G).** Two steps; the file is hidden and kept; it still opens, read-only, with the way back; for an upcoming Calendly booking the second step offers to cancel it in Calendly too, ticked; Calendly is asked first and nothing is deleted if it cannot be.
- **Settings (G).** The from address; the Calendly type map; the people who can log in (add, correct, mail a set-your-password link, switch a login off and on; never removed); the Connections panel for Calendly, Brevo, Google and the two backup stores ("not set up yet"), each with whether it works, when it last did, what it said, and a test button; bookings from Calendly switched on and off there; the bookings waiting for a person; trouble that has been raised; and the change history of Settings and the logins, folded shut, never a password.

**Evidence.** Run in the app folder through Herd's PHP 8.5 at 19:35:

| Command | Result |
|---|---|
| `herd composer test` | passed: 1,262 tests, 4,976 assertions, 0 failed, about 19 s (1,011 before the stage; 1,015 with 261 failing at `89c4118`) |
| `herd composer lint` | passed |
| `herd composer analyse` (Larastan level 8) | passed: 0 errors (14 at `89c4118`) |
| `herd composer audit` | no advisories; no package added |
| `herd php artisan schedule:list` | `*/15 * * * * php artisan hd:calendly-check` |
| `herd php artisan migrate` on this Mac's local database (invented data) | the four P3 migrations ran: `calendly_bookings`, `connections`, two columns on `files`, one on `users` |
| the whole suite run three times at the end | the first two runs each turned up one test that failed by chance (below); the third passed clean |

The suite's own locks held throughout: every new setting (`HD_CALENDLY_DRIVER`, `CALENDLY_TOKEN`, `CALENDLY_SIGNING_KEY`, `HD_ALERT_ADDRESS`) is pinned twice in `phpunit.xml`, and `tests/RefusesRealServices.php` refuses a Calendly token or a driver that is not the stand-in (the first builder did this; the hostile-shell proof covers it).

**What I kept of the first builder's work: all of its back end.** I read every file. The design is sound: one interface and two implementations as for letters; the booking row as the fact behind "once"; the intake through `OpenFile`; the two history readers; the search. It is in `89c4118` as the orchestrating thread committed it.

**What I changed of it, each with a test that failed first** (all in `1fcff36` unless said otherwise):

| What was wrong | What it does now |
|---|---|
| The user factory never set `disabled_at`; the strict model threw on the first request of 218 tests. | The factory sets it. |
| Larastan: dead catch in `SendPasswordLink`, five list types, a non-literal SQL string in the search, `CarbonImmutable::create` that may return null, two views that did not exist. | `SendPasswordLink` asks the mail trap before the password broker (so no token is made for a link that cannot go); `array_values`; the search's columns are its own constants, so the SQL is a literal; `createStrict`; the two views exist. |
| `StandInCalendlyController::check` broke the Laravel preset (a public method that is not a resource method). | `StandInCalendlyCheckController`, invokable. |
| The real Calendly class followed `next_page` by handing the HTTP client the address and an empty query; Guzzle's `query` option wipes the address's own query, so it fetched the first page for ever (`e1fa140`). | With a next-page address, no query argument. |
| A mistyped zip ("CT 0687") was read as the town (`e1fa140`). | Three to nine trailing digits that are not a zip are taken off and left empty. |
| A cut cancellation reason was 503 characters, not 500 (`e1fa140`). | Cut to 500 exactly. |
| The stand-in page threw on an unknown booking (`e1fa140`). | It says "There is no such booking." |
| Opening a file was four acts in the history (client, property, file, invoice each in their own batch), because `OpenFile` used a plain transaction (`ded9862`). | One act (`HistoryEntry::batch`, which is a transaction too). |
| Nothing was there to see: no view for the deletion page, the stand-in page, the history, the search results, the booking, the users, the Connections panel, the from address or the type map; and no test of the stage. | All written (`1fcff36`, `6b0984c`); 251 new tests in 15 new test files (`cee8bfa`, `ded9862`, `6b0984c`, `e1fa140`). |

**Three tests that failed by chance, and the mechanism** (`840e5e4`): a P1 history test relied on a made-up zip not being 06877 (one run in a thousand); two of my search tests asserted a word's absence from a page of made-up addresses. Fixed inputs, and assertions on a file's own address rather than a word. The suite then passed clean.

**Not done, and why.**
- Nothing was sent to Calendly, Google or Brevo; no account exists. The list of what that leaves unproven is below.
- Nobody has looked at the screens in a browser, as in every stage so far; the panels are tested on their HTML. The browser tests are P4's.
- `http://hdonline-v4.test` was not checked; the local database was migrated so the served site works once Herd's services are restarted (P1's note).
- The booking page link on the Connections panel appears after the first "Test Calendly" or switch-on, not before: the panel learns where clients book from Calendly's own answer (for the stand-in, its page). The README names the page.
- Search does not look in notes or in the invoice description, and not in the people on a job: R6.2 names client, address and time. One click to add if wanted.
- Deleting a client or a property is not offered: the plan speaks of deleting a file; records are linked and unlinked, never hidden.

**Refused or blocked.** Nothing was refused by the app's safety check and no model safety classifier stopped anything. I opened nothing under `~/Dev/hd-v4-import-data/` or Downloads and did not read `~/Dev/clc-plugins/`. I fetched no web page: the real Calendly class stands on the first builder's reading of Calendly's manual, which neither of us could check tonight.

### Decisions the documents did not settle

The first builder's, as the code shows them (it left no list), then mine.

1. **Bookings are off until a person switches them on** (`calendly.listening_since` in Settings). Why: the token can be entered and tested weeks before cutover without live bookings making files early (the paperwork review's blocker); the switch is the moment Calendly is pointed at v4.
2. **Bookings made in Calendly before that moment wait for a person's word.** Why: they may already be on file (from the import, or typed by hand); a second file for the same job helps nobody.
3. **One row per booking, keyed by Calendly's name for the invitee**, with what was done written on it in the same step. Why: "once" as a fact of the database, not of memory.
4. **A booking's rows are marked as from Calendly** (`sources`: system `calendly`, collection `invitees`, identifier the invitee's address), through `Model::importFrom()`. Why: what the client typed may be thinner than the form allows, and a thin row must be a marked row (P1's rule).
5. **What the client typed is held to the New File form's rules field by field; a value that does not pass is left empty**, never guessed, and the booking as typed is kept and shown on the file. Why: nobody is at the screen to be asked, and a booking must never be lost over a bad zip.
6. **The address is read from the first answer whose question mentions "address" or "property".** Why: the question's wording in Calendly is Peter's, not ours.
7. **Names from one box: the last word is the surname.**
8. **A visit unless Calendly's place is a video or phone kind** (zoom, google, teams, webex, call).
9. **The service is matched by the appointment type's name**, saved in Settings, with the two shipped names as the fallback. Why: it can be set before any account exists.
10. **A cancellation of a file whose letter has gone, or a file a person has closed, only writes the history.** Why: a late cancellation must not undo a job that was done.
11. **A reschedule of a closed or cancelled file keeps its date**, noted in the history.
12. **"Nobody has written in the Doc" means the Doc is still at the revision the system itself last left it at**; whenever that cannot be said for certain, the Doc stays. Why: a Doc is put away on evidence, never on doubt.
13. **A Doc in the trash comes out when the file is set to anything but cancelled, or when the letter is next brought up to date; one whose trash was emptied is replaced by a new copy.**
14. **Deleting a file with an upcoming Calendly booking cancels it in Calendly first, and deletes nothing if Calendly cannot; the file is then marked cancelled as well as hidden.** Why: it says the truth if restored; Calendly tells the client, the system sends nothing (Q6).
15. **A deleted file opens read-only**, with the restore button; the routes that would change it do not find it. Why: it must be read to be restored, and nothing on it may change while hidden.
16. **The change history keeps old values on the page, folded shut.** Tests that look for a corrected value's absence look outside it. Why: that is what a history is for; Gordon asked for it hidden by default, not absent.
17. **Logins are never removed, only switched off**; nobody switches off their own; a switched-off login is refused in the same words as a wrong password and logged out at its next click. Why: the history names the person.
18. **A new login is mailed a link and has a password nobody knows until then.** The password link goes through the mail trap like every message.
19. **Trouble is raised once a day at most, and clears by itself** when the next check finds nothing wrong.
20. **A notice is taken up to 25 hours old and 5 minutes into the future.** Why: Calendly retries for about a day; clocks differ.
21. **The signing key is ours to make** and entered on the server; Calendly is given it when the notifications are switched on.
22. **The check asks only about appointments whose state it does not already know** (standing and still standing, or over and still over). Why: a check that finds nothing new is one request.
23. **The Connections panel keeps only observations** (when it last worked, what it said, what went wrong) and never a key.
24. **Search: words AND month; each word must be in the client or the property; a bare year only when nothing else was typed; a month's name only with a year.**
25. **A linked (merged) record is found under its old spelling**, through `coalesce(merged_into_id, id)`.

Mine:

26. **The first builder's work stays as one commit** (`89c4118`, the orchestrating thread's). Why: splitting it after the fact would make commits that do not pass alone.
27. **The 15-minute check from the stand-in page is its own invokable controller.** Why: the Laravel preset allows no other public method on a controller, and the rule is worth keeping.
28. **`SendPasswordLink` asks the mail trap before the password broker.** Why: a token must not be made for a link that cannot go; it also made the dead catch real.
29. **Opening a file is one act.** Why: the history panel showed four.
30. **The panel learns where clients book from Calendly's answer** (`facts.booking_page`), so the stand-in's page is linked from Connections after the first test or switch-on. Why: nothing in the views names the stand-in, and the arch rule stays.
31. **The address reader takes off a mistyped zip and leaves it empty.** Why: "CT 0687" must not become the town.
32. **A cut cancellation reason is 500 characters exactly.**
33. **Tests use fixed data where a made-up value could carry the word they look for.**

### What cannot be proven until the real Calendly account exists

- That Calendly accepts each request as written: `GET /users/me`, `GET /event_types` (with `user` and `active`), `GET /scheduled_events` (with `user`, `min_start_time`, `sort`, `count`) and each event's `/invitees`, `POST .../cancellation`, `GET`/`POST`/`DELETE /webhook_subscriptions` with `scope: user`, `organization`, `user` and `signing_key`; that `pagination.next_page` is a full address; that a personal access token is enough for all of it on the firm's plan.
- The shape of a notice: `event` of `invitee.created` or `invitee.canceled`; `payload` the invitee with `scheduled_event` inside it; `questions_and_answers`, `text_reminder_number`, `rescheduled`, `old_invitee`, `new_invitee`, `cancellation.canceled_by` and `reason`; the status word `canceled`; the `Calendly-Webhook-Signature` header as `t=...,v1=...` over `"<t>.<body>"` with HMAC-SHA256. All from the first builder's reading of the manual, which neither of us could fetch.
- That a reschedule arrives as a cancellation marked `rescheduled` plus a new booking naming the old one, and in which order.
- That Calendly switches a subscription off after about a day of failures, and what `state` it then reports.
- The wording of the firm's booking-form question for the address (the reader looks for "address" or "property"), and the exact names of the two appointment types (the fallback is "Professional Opinion" and "Structural Design").
- How Calendly reports the place of a video appointment for the firm's own setup.
- That `Str::limit` to 500 is within what Calendly takes for a cancellation reason.
- Which plan tier the firm has and whether it includes webhooks (plan section 11, item 7); without them, bookings arrive by the check alone, which the code allows for.
- The server: the scheduler running every minute; the queue worker for the letter work a cancellation sets off; the alert mail reaching Gordon.
- The screens, in a browser.

### Questions for Gordon

1. **Should a late cancellation of a file whose letter has already gone change the file?** Today it only writes the history (the job was done).
2. **A deleted file with an upcoming booking: cancel in Calendly first, and delete nothing if Calendly cannot be reached?** Today that is the rule; the alternative is to delete here and let a person cancel in Calendly by hand.
3. **Who gets the alert mail** (`HD_ALERT_ADDRESS`): Gordon alone, or the office too?
4. **Should Search look in the invoice description and the notes as well?** Today it looks in names, addresses, email, company, month and invoice number, as R6.2 says.
5. **The Calendly booking form's address question: is its wording "Property address"?** The reader takes the first answer whose question mentions "address" or "property".
6. **Should the three people all be able to add logins and switch them off?** Today Settings is open to all three (P1's question 3).

### For the stages that follow

- **P4 (import).** `CalendlyBooking::settled()` and the intake rest on `files.calendly_event_uri` being unique; the import must leave it empty. A migrated file is not a booking: no `calendly_bookings` row. The search looks in `clients.name_key`, `second_name_key` and `properties.address_key`, so the import must go through the models (it does, by `importFrom()`), or the keys are empty and old jobs are found by their typed spelling only. The ten-thousand-file timing test builds its rows with the query builder; the real import's rows will carry the keys.
- **Browser tests (P4).** The main paths now exist: new file by hand, duplicate prompt, invoice, mark paid, search, delete and restore, and the stand-in Calendly page.
- **Backups (later).** `OutsideService::BackupCloudflare` and `BackupDrive` are listed on the Connections panel as "not set up yet"; `OutsideService::isBuilt()` and `TestConnection` are where they are switched on, with a `check()` each.
- **Paperwork (W2) and the deploy script.** New settings, all in `.env.example` with a comment each: `CALENDLY_TOKEN`, `CALENDLY_SIGNING_KEY`, `HD_ALERT_ADDRESS`; optional `HD_CALENDLY_DRIVER`. A server needs the scheduler (`php artisan schedule:run` every minute) beside the queue worker. A third open address: `POST /hooks/calendly`. The cutover runbook's Calendly step is: enter the token and the signing key on production; "Test Calendly"; set the two appointment type names if they differ; "Switch bookings on" at the moment Calendly is pointed at v4; then say what becomes of the bookings already in the calendar. Staging may run `HD_CALENDLY_DRIVER=stand-in`; production refuses it.

## P4a: the import and the letter conversion, then the rehearsal on the real history (plan-v2 section 6, steps 1 and 2)

Builder: Fable (claude-fable-5-1; the effort level is not visible to me). Started 2026-10-02 19:50 CEST from 840e5e4 (1,262 tests green, 17.6 s). Two Opus reviews of P3 read fixed copies at the same commit; P3's code is not reshaped here beyond what the import needs.

### Plan (written before any code)

**What, in order, each committed when green:**

1. **Test safety.** A `legacy` database connection is added to `config/database.php` (SQLite, named only by `HD_LEGACY_DATABASE` in `.env`, opened with SQLite's read-only flag so that nothing in the app can write to the old system, and no journal pragma, which a read-only file refuses). It is pinned in `phpunit.xml` twice (`<env force>` and `<server>`) to `:memory:`, as the P1 fixes asked. Tests: (a) the subprocess test that runs part of the suite under a hostile shell now also names a real-looking old-system file in `HD_LEGACY_DATABASE`, and both real-looking files are made unreadable for the run, so the suite passing proves neither was opened; (b) the environment file cannot override a pinned setting, proven on the loader the app really uses (an immutable repository: a hostile env file loaded into it leaves `DB_DATABASE` and `HD_LEGACY_DATABASE` at `:memory:`); (c) through its own connection the old system cannot be written to (an insert is refused as "readonly"); (d) no tracked file names this Mac's data folder. The tests' old system is an invented SQLite file written by a fixture builder (`tests/Fixtures/OldSystem.php`) with the same twelve tables as the staged copy, pointed at through the same read-only connection.
2. **The importer.** `php artisan hd:import` (`--dry-run`, `--from=legacy`, `--chunk=`), reading WordPress and v2's `REPORTS` and `CONTACTS` through the read-only connection and writing clients (with the second person), properties, files, who was copied, invoices with their totals (the old template's arithmetic, in cents) and paid state, and a `sources` row for every row (`wordpress` with the WordPress ID; a second `v2` source where the job came from v2, carrying the v2 row's own identifiers and fields in `extra`). History lines of imported rows carry a new event, `imported`, in nobody's name; the Timeline shows "The import". Idempotent: a WordPress ID already recorded in `sources` is skipped, so a second run creates nothing. One transaction per job (client, property, file, contacts, invoice and their sources together or not at all). Skipped: future-dated records, records whose client name, property address or any title holds the whole word "test", and records in WordPress's trash; each counted and listed by WordPress ID and reason. The command ends with the reconciliation tables (by year and by type) and writes the same counts to `storage/app/private/import/` (git-ignored). Tests on the invented fixture: every shape the census describes, including a plain-ID relation, a serialized one, a job with no client, no property, no type, no fee, no address, a two-person client, a v2 job and a v3 job, a broker copied and one not, a test record, a future date, an 8888 date, a trashed record, the invoice arithmetic case by case, no mail, no Docs, the history event, and running twice.
3. **The letter conversion.** `php artisan hd:convert-letters` (`--dry-run`, `--since=2022-06-21`, `--uploads-listing=`): for each imported file whose WordPress report is a published letter (not a compiled report) since the date, parse the Gutenberg blocks into a `LetterBody` (paragraphs with their bold runs, bold headings, pictures with captions, bulleted and numbered lists; empty tables dropped; a table with text kept as paragraphs and the letter listed by ID for a person; anything else is a failure with its reason), make the Doc the way a new file's letter is made (`PrepareLetter`: template copy, tagged places filled, named by the rule), then write the body after the greeting through a new `LetterDocs::writeBody()` on both stores, record the old public addresses of the letter and its invoice in `old_links` pointing at the file, and note the letter as sent on the day the old system published it. Photos: the app keeps the photo files itself on the `records` disk (`old-photos/YYYY/MM/file`), loaded from an unpacked copy of the old uploads folder by `hd:import-photos`, and hands Google a signed address good for half an hour (`GET /photos/...`, as the stamp already works); a photo the store does not hold leaves its caption and a counted gap. The dry run makes no Doc and counts: clean, with photos (and how many photos the uploads listing holds), tables with text, lists, unhandled, failures by reason. Tests on invented letters through the stand-in, and the real Google class against made-up answers asserting the exact requests.
4. **The rehearsal.** `.env` only: `HD_LEGACY_DATABASE` at the staged copy, `DB_DATABASE` at the rehearsal database. Migrate, run the import, reconcile against both census documents, run it again and compare a dump of the database before and after, then the letters' dry run. The suite is run again with `.env` naming the real files, as the proof of step 1 on this Mac.
5. **This log**, then the final message.

**Decisions taken for the plan** (each also listed under "decisions the documents did not settle" below, with its reason): old jobs come in `closed`, except the v3 invoices WordPress marks unpaid, whose files come in `sent` with the invoice issued on its record's date; `paid_at` for a paid old invoice is the invoice record's last edit in WordPress, the nearest witness; a v3 client whose only name is one field keeps it as the display name, first and last names left empty rather than guessed; a job's time of day missing in the old data is midnight on the firm's clock.

## W1: the real history in the app

Builder: Fable (claude-fable-5-1, started at effort high per the brief; the level is not visible to me). 2026-10-03, about 00:30 to 01:10 CEST, from 783e9db on `feature/v4-build`. Scope: finish the importer left uncommitted by P4a, run it on the real history into the rehearsal database, reconcile, leave the local site showing it. The letter conversion, browser tests and the P3 findings were not touched.

### What was kept and what changed of P4a's work

Kept, all of it: the 13 uncommitted files (ImportCommand, `app/Import/` with its twelve classes, the `imported` history event and its wording in FileHistory and Timeline, the fixture builder's v2 pointer, the three unit tests and the feature test on the invented old system). The design stands as P4a planned it: WordPress is the truth for which client and property a job has; v2's REPORTS and CONTACTS rows are read for the two names on a client and cross-checked; one transaction per job; a `sources` row for every row, unverified; the history says "The import".

Changed, three things, each because a test said so, and one for the analyser:
1. A further source note on a row (v2's note beside WordPress's) was written with the polymorphic columns in a mass-assignment list, which `Source` does not allow. It now goes through the row's own `sources()` relation. This was the error behind 15 of the 17 failing tests.
2. v2's note on a property now goes only with the property v2 agrees on (its `wp_property_id` is empty or is the one WordPress links), or where WordPress links none. Before, a job whose v2 row named another property still pinned that row to WordPress's property.
3. The paid date of an old invoice is read from WordPress's `post_modified_gmt` as UTC (`OldDate::recordedGmt`), not as a time on the firm's clock, which put it five hours out.
4. One line in `Serialized` the analyser called always-true, simplified.

One commit: 03b5972. Checks on it: `herd composer test` 1,334 tests, 5,266 assertions, 0 failed; `herd composer lint` clean; `herd composer analyse` 0 errors. Tests still cannot open the real data: `phpunit.xml` pins both databases to `:memory:` twice, and 783e9db's proof stands.

### The rehearsal on the real history

Set through `.env` only (never committed): `DB_DATABASE` at the rehearsal file and `HD_LEGACY_DATABASE` at the read-only copy, both in `~/Dev/hd-v4-import-data/`. `migrate --seed` made the tables and the three local logins (their passwords stayed in the git-ignored `storage/app/private/local-logins.txt`, which already existed; nothing new was written there). Then `hd:import --dry-run` (1.5 s), `hd:import` (25 s), `hd:import` again (0.8 s, "already imported 10,206", every table the same size before and after, highest `sources` ID 70,299 both times). The command writes its counts and the skipped IDs to `storage/app/private/import/` (git-ignored; counts and WordPress IDs only).

Reconciliation, counts only:

| What | Census (2026-10-01) | Imported | Note |
|---|---|---|---|
| Appointment records read | 10,212 + 3 in the trash | 10,215 | all statuses |
| Skipped | 9 future-dated records (3 appointments, 3 invoices, 3 properties) | 9 appointments | 3 dated in the future (one of them 8888), 3 in the trash, 3 published test records; two are both. Listed by WordPress ID in the command's output and file |
| Files | 10,209 published | 10,206 | the 3 published test records |
| Inspections / consultations / no type | terms: 7,247 / 2,839 | 7,244 / 2,839 / 123 | the 3 skipped inspections |
| From v2 / made in v3 | 9,441 carry a v2 ID / 771 | 9,435 / 771 | the 6 v2 jobs skipped are all among the 9 (see below) |
| Clients | 8,697 contact records with the client term | 8,693 rows | 8,681 from WordPress contact records, 12 stand-in rows for jobs that link no client record (11 no link, 1 link to a missing record) |
| Clients with a second person named | about 6,182 by name (part 1) | 6,138 | from v2's name columns |
| Properties | 9,030 published | 9,112 rows | 9,027 from WordPress (3 skipped), 82 from v2's rows where WordPress links no property, 3 stand-in rows where neither has one |
| Invoices | 10,208 published | 10,206 | one per file |
| Invoices paid / unpaid / no mark | 9,434 + 131 paid, 216 unpaid, about 430 no value | 9,559 paid, 216 unpaid, 431 no mark | 48 carry no amount at all |
| People on jobs | | 1,992 | brokers 1,860 (561 copied), attorneys 132 (82 copied) |
| History lines | | 40,209 "imported" | plus 3 "created": the local logins |
| Jobs by year | part 1's table (by record date) | the command's table (by job date) | 38 of 44 years equal. Differences of 1 or 2 in 1983, 2000, 2016, 2017, 2020, 2021 and 2022: 3 appointments whose job date is in another year than their record (checked in the copy: 3 rows), and the census's year filter working on the record's date at year boundaries. Totals 10,206 here against 10,205 placed plus 7 unplaced there |

For a person to look at later (IDs in the file): the fee differs between v2 and WordPress on 344 jobs (WordPress stands); 8 v2 jobs have no client row in v2; 1 v2 row points at no appointment.

### How the local site is set up

`http://hdonline-v4.test`, served by Herd on PHP 8.5, reads the rehearsal database through `.env`. Plain local checks: `/up` 200, `/login` 200. Through the HTTP kernel, signed in as the local `peter@` login (no browser, no password typed): the dashboard 200 listing 25 files, the search "2024-05" and "May 2024" each 200 listing 12 files, which is the number of files dated May 2024 in the database; a search for "2007" 200 with 25 listed; the newest and the oldest file's pages 200; Settings 200. The invoice PDF preview of an imported file answers 404 by the app's own rule (an imported invoice has no number, so there is nothing "as it would go out"); the file page shows the invoice's wording, total and paid state instead.

Mail: `MAIL_MAILER=log`; `HD_MAIL_LIVE` unset, so the trap. Letters and Calendly: their driver names unset, so the stand-ins. No Google, Brevo or Calendly value is in `.env`. Nothing outside this Mac was called. Nothing holding real rows sits in a tracked path: `.env`, the rehearsal file, `storage/app/private/` and `database/*.sqlite` are all ignored (checked with `git check-ignore`).

### Decisions the documents did not settle

- Every old job comes in `closed`, including the 647 whose invoice is unpaid or unmarked: P4a's plan had those come in `sent` with an issued invoice, but an imported invoice has no number and cannot be sent, so a closed file with the invoice's paid state on record is the honest shape; marking an old invoice paid in v4 is a follow-up to check.
- The paid date of a paid old invoice is the invoice record's last edit in WordPress (UTC): the old system kept no payment date, and this is the nearest witness; the source note says so.
- A v3 client whose name is one field keeps it as the display name; first and last names are not guessed.
- A job with no time of day is at midnight on the firm's clock.
- v2's note goes with a property only where v2 agrees it is that property: otherwise the note would pin v2's facts about one house to another.
- v2's whole row goes into the source note's `extra` (inside the rehearsal database only), so nothing v2 recorded is lost even where this app has no column for it.
- The stamp choice on the old letter is carried onto the file (CT, NY, none, or unknown where there was no box); the letters themselves are not converted here.
- The nine "future" records of the handoff are three appointments with their invoice and property each; the importer skips by appointment and the invoice goes with it, which is what Gordon asked.

## W2: the everyday paths in a browser

Builder: Fable (claude-fable-5-1, started at effort high per the brief; the level is not visible to me). 2026-10-03, from 03b5972 on `feature/v4-build`. Scope: browser tests of the everyday paths on invented data, fix whatever breaks normal use, check the local site by plain requests. The P3 review findings, the letter conversion and the kit were not touched.

### Which tool, and why

Pest's browser plugin (`pestphp/pest-plugin-browser` 5.1, a development dependency) driving Chromium through Playwright 1.63.0 (an npm development dependency; the browser itself, about 360 MB, went into the user's cache folder `~/Library/Caches/ms-playwright`, the one download Gordon granted). Not Laravel Dusk. The reason is the real-data rule: the plugin answers the browser from the test process itself (an Amp HTTP server handing each request to the app's own HTTP kernel), so the browser tests run on the same in-memory SQLite database, emptied each test, and the same stand-ins and array mailer as every other test, under the same `phpunit.xml` pins and the same refusal in `tests/RefusesRealServices.php`. Dusk starts a separate server that reads `.env`, which on this Mac points at the rehearsal database with real client records; it would have needed its own environment file and a second lock. Pest 5 also has no Dusk fit without a starter kit.

How it is wired: a `Browser` suite in `phpunit.xml` (`tests/Browser/`), extended in `tests/Pest.php` with the base test case and `RefreshDatabase`; `herd composer test` runs it with the rest, and `herd composer test:browser` runs it alone. The screenshots the plugin takes of a failure (`tests/Browser/Screenshots/`) are ignored by git. The README says what a machine needs once (`npm install`, `npx playwright install chromium`).

### The paths, each as a short test (21 tests, 8 files)

| Path | Test file | Result |
|---|---|---|
| Log in and out; a wrong password turned away | `LoginTest` | passed |
| Dashboard: recent files newest first; search by client name, by property address, by month, and "Clear" | `DashboardTest` | passed |
| New File by hand: client, property, job on one form; the file opened with the standard price and the stamp by state | `NewFileTest` | passed |
| The second file for a known client at a known property: "may already be on file" for both, one click each links them, and "Been here before" lists the other files | `NewFileTest` | passed |
| File screen: correct the client in place; correct the property in place; the job's facts; the invoice description and price | `FileScreenTest` | passed |
| The folded change history opened and showing the correction just made (old and new value) | `FileScreenTest` | passed |
| The letter: made when the file opened, named as the plan says, opened as a Doc (the stand-in's page); sent, logged in Messages with "The PDF as sent", the Doc shared by link | `LetterTest` | passed |
| The invoice: sent; marked paid from the "Mark paid and send a paid copy" fold (the question names the client and the amount); the paid copy sent again; three lines in Messages | `InvoiceTest` | passed |
| Delete (two steps) and restore: gone from the Dashboard, found under "Deleted files", opened read-only, restored, back on the Dashboard | `DeleteRestoreTest` | passed |
| Settings: an invoice text saved and a new file starting from it; the letter template link for a service; a person added who can log in (the link mailed); the Connections panel with "Test Google" and bookings from Calendly switched on | `SettingsTest` | passed |

Every path passed against the app as W1 left it. Nothing in the app's code had to change for normal use.

### What I changed

- **One test-isolation fix, in `tests/TestCase.php`** (the only change outside new test files and the wiring): every test now starts with no trusted hosts. Symfony keeps the trusted-host list on the request class itself, not on the app, so a feature test that poses as a server (the mail-trap tests) left the list behind, and when the browser suite ran after the rest, every page on `127.0.0.1` was refused ("Untrusted Host"). Run alone, the browser suite passed; run inside `composer test`, all 21 failed. The feature tests never noticed because they all use the same host. Found by the full run; fixed with one line.
- The tests themselves, `tests/Browser/*.php`; the suite wiring in `phpunit.xml`, `tests/Pest.php`, `composer.json`; `.gitignore` for the screenshots; the README's Checks section.

Things learned about the plugin, so the next person does not lose the hour I did: a text with a comma, a colon, brackets or an equals sign is read as a CSS selector, not as text, so a button such as "Yes, delete this file" is pressed as `text=Yes, delete this file`; a nested field name such as `client[email]` cannot be used even quoted (the plugin's CSS parser refuses the inner brackets), so the field's id is used (`default-client-email`, as the field component builds it); `assertSeeIn` is strict, so the text must occur once inside the selector; a folded `<details>` is opened with `click('#history summary')` before what is inside is asserted on, because `assertSee` wants the text visible.

### Evidence

Run in the app folder through Herd's PHP 8.5 on 2026-10-03:

| Command | Result |
|---|---|
| `herd composer test` | passed: 1,355 tests, 5,376 assertions, 0 failed, about 25 s (1,334 before the stage) |
| `herd composer test:browser` | passed: 21 tests |
| `herd composer lint` | passed |
| `herd composer analyse` (Larastan level 8) | passed: 0 errors |
| `curl` on the Herd address | `/up` 200, `/login` 200 (PHP 8.5.10), `/files/1` and `/settings` 302 to `/login`; the built stylesheet loads (a Playwright screenshot of the login page, styled) |
| `git log` | 3 new commits, db9b0e0, b071044, 1063e6c; tree clean; no remote |

The browser tests ran on the suite's in-memory database only: `.env` was not changed, nothing under `~/Dev/hd-v4-import-data/` was opened, and the one request to the Herd site was the login page, which shows no data.

### Not done, and why

- The look of the screens is not asserted: the base test case renders pages without the built assets (`withoutVite`), so the browser tests see the unstyled forms. The behaviour is what was asked; the styled login page was checked by one screenshot of the local site.
- "Open the Doc", "Look at the PDF" and "The PDF as sent" open in a new tab, which the tests do not follow; the stand-in Doc page is visited by its address instead, and the PDFs are covered by the feature tests.
- Calendly's own booking path (the stand-in's page) and the other people on a job are not browser-tested: not in the list of everyday paths given.
- The P3 review findings (`docs/reviews/app-P3-*.md`) are untouched: none stops an everyday path.

**Refused or blocked.** Nothing was refused by the app's safety check and no model safety classifier stopped anything. Nothing was installed with Homebrew; no hook was registered; nothing was pushed.
