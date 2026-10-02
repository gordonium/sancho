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
