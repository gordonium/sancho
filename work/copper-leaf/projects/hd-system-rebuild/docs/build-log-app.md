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
