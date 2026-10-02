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
