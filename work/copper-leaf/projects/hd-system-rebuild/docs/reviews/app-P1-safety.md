---
name: Home Directions v4 review, app stage P1, safety lens
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: Independent review of the app skeleton (stage P1, step C) asking one question, is it safe to put on a server and safe with people's data: 17 numbered findings, each with the file and line, what is wrong, the request or test that was actually run and its result, the fix and a weight; then what was checked and holds, the kit spec's section 5 items as present, absent or not yet due, and the real numbers from the three checks
sources: ["[repo:/Users/gordonium/Dev/clc-laravel/hdonline-v4, branch feature/v4-build, commit 7eb7d60]", "[doc:build-handoff.md]", "[doc:plan-v2.md]", "[doc:laravel-kit-spec.md]", "[doc:hosting-options.md]", "[doc:build-log-app.md]", "[doc:build-state.md]", "[doc:runbook-accounts.md]", "[web:laravel.com/forge/docs/sites/environment-variables.md, read 2026-10-02]", "[run: herd composer test, lint, analyse, audit, 2026-10-02 01:36 CEST]", "[run: 16 scratch probe tests and about 60 local HTTP requests against two scratch servers on 127.0.0.1, 2026-10-02 01:36 to 01:47 CEST; scratch files kept outside the repository and removed]"]
status: written 2026-10-02 01:50 CEST by a reviewer that did not write the code; 1 blocker, 6 should-fix, 10 minor; no code was changed, nothing was committed, no scratch file is left in the app folder; no password appears in this file
---
# Review: app stage P1 (the skeleton), safety lens

Reviewer: Claude, model `claude-fable-5-1`. I cannot see my own effort level. I did not write the code and I changed none of it. The repository was at `7eb7d60` with a clean working tree before and after.

**The conclusion first.** The login itself is sound: I could not get past it, fix a session on it, or forge a request to it. Input is validated, output is escaped, nothing builds SQL by hand, and a visitor who is not logged in reaches a login page, a health check and nothing else. The trouble is in what happens when this repository meets a server. The one file Forge copies onto a new site is written for this Mac: it says "local", it turns debugging on, and it carries the three known passwords. Every protection the builder added for a server (the seeder's refusal, the destructive-command switch, debug off) is switched by that same line. That is the blocker. Six more things should be fixed before a server exists; ten are small.

Weights: **blocker** is a real hole or a way to lose or leak data; **should-fix**; **minor**.

How the evidence was made. The three checks were run as the builder runs them. The bad cases were run as tests kept outside the repository (in the session's scratch folder, run with the app's own test runner), against scratch SQLite files, never the app's local database. Where the question was what a browser meets (cookies, the forgery check, error pages), the app was served twice on `127.0.0.1` from scratch databases, once with the environment exactly as `.env.example` gives it and once as production, and asked with `curl`. I did not type the seeded passwords into anything; the login flow was exercised with a throwaway user and a random password made inside the test. The client data folder and Downloads were not opened.

---

## Blocker

### 1. The file Forge copies onto a server says "local", turns debugging on and carries the three known passwords; the seeder's refusal and the destructive-command switch both hang on that one line

**Where.** `.env.example` lines 2 (`APP_ENV=local`), 4 (`APP_DEBUG=true`), 5 (`APP_URL=http://hdonline-v4.test`), 21 (`LOG_LEVEL=debug`), 74 to 76 (the three `SEED_PASSWORD_` lines, added in commit `1e56e71`). `database/seeders/UserSeeder.php` lines 20 to 24. `app/Providers/AppServiceProvider.php` lines 28 and 31. `README.md` lines 19 and 25. `composer.json` lines 43 and 71.

**What is wrong.** Forge copies a project's `.env.example` into a new site's environment and changes only some database settings. [web:laravel.com/forge/docs/sites/environment-variables.md, read 2026-10-02] Whether it also rewrites the mode line is not confirmed anywhere. [doc:runbook-accounts.md 4.3 item 5] So a new site starts as a copy of this Mac's settings. The builder's guard is "refuse unless the environment is local or testing", and the copied file says local. The passwords and the permission to use them travel together. The same line also switches off the destructive-command switch and leaves the debug page on for anyone. The app's local `.env` on this Mac differs from `.env.example` only in the app key (checked by name, values not printed), so running the app from `.env` here is exactly the site Forge would create.

**Evidence, each run on a scratch database.**
- Environment as `.env.example` plus a key, `php artisan migrate --seed --force`: the seeder ran, 3 users were created (owner, treasurer, admin), and each stored hash verifies against the value committed in `.env.example` (three times `true`). The app reported `env=local debug=true`.
- Same environment, `migrate:rollback --force` and `migrate:fresh --force`: both ran. `migrate:fresh` without `--force` also ran, with no question asked. The users table was emptied.
- Same environment over HTTP, as a visitor with no login: `PUT /login` returned a debug page of 855,619 bytes naming the exception, 68 framework file paths, the PHP version and the Laravel version. A malformed `_method` and a malformed `Host` also returned debug pages with framework paths (919,670 and 864,773 bytes). The same three requests in production mode returned 997 to 1,011 bytes and nothing of the kind. The debug page did not show the app key or the seed passwords (counted: 0 occurrences of each).
- Same environment, with the development packages installed: `POST /_boost/browser-logs` with no login and no token returned 200 and wrote my line into a log file. In production mode the route does not exist (404).
- For contrast, with `APP_ENV=production` and with `APP_ENV=staging`: `db:seed --force` stopped with "never seeded on a server" and left 0 users; `migrate:fresh`, `migrate:refresh`, `migrate:reset`, `migrate:rollback` and `db:wipe`, each with `--force`, were all refused ("prohibited from running in this environment") and all 21 tables were still there. So the guards work when the mode line is right. They are only as good as that line.

**The fix.**
1. Make `.env.example` the file a server should start from: `APP_ENV=production`, `APP_DEBUG=false`, no `APP_URL` pointing at this Mac, `LOG_LEVEL` no lower than `info`, `SESSION_SECURE_COOKIE=true`, and no `SEED_PASSWORD_` lines. What a developer's machine needs differently is set by the local setup step, not by the file a server receives.
2. Take the known passwords out of the repository. The seeder can make three random ones the first time it runs on this Mac and write them into the untracked `.env` (the handoff asks only that Gordon can find them in the app's own config). The three values now in history at `1e56e71` are burned: never reuse them. The repository has no remote yet, so this is the cheap moment.
3. The seeder's refusal must not rest on the mode line alone. Also refuse unless the app's own address is a local one (`localhost`, `127.0.0.1`, or a name ending in `.test`), with a test for each case.
4. Something that fails loudly when a server is running as a developer's machine: the deploy script (which the kit says lives in this repository) stops unless the mode is `staging` or `production` and debug is off; and a test asserts it.
5. Correct `README.md` lines 19 and 25 to match.

---

## Should-fix

### 2. There is no way to give a server its three users, or to change or reset a password, except the seeder

**Where.** `database/seeders/UserSeeder.php` lines 11 to 15 ("a server gets its users another way"); `routes/console.php` (one command, `inspire`); there is no `app/Console`; `routes/web.php` has no password route.

**What is wrong.** The "other way" does not exist. On a server the only ways to make a login are `tinker`, which the kit forbids on staging [doc:laravel-kit-spec.md section 6 item 5], or running the seeder with the mode set to local, which is finding 1. Step C's gate is "usable by hand on staging" [doc:plan-v2.md section 7]; nobody can log in on staging without one of those two. Nor can a password be changed once set, by its owner or by Gordon: there is no "forgot password" (the builder says so: none until mail exists), no change-password screen, and no command.

**Evidence.** The route list in production mode has 18 routes: 13 behind the login, `GET` and `POST /login`, `/up`, and the framework's two signed storage routes. None sets a password. `git ls-files` shows no console command. The seeder under `production` and `staging` creates 0 users (finding 1).

**The fix.** One command, for example `hd:user`, that creates a user or sets a new password. It asks for the password without showing it, or makes one and shows it once; it never takes the password as an argument (arguments land in the shell's history); it works in every environment; it has tests. Gordon runs it on the server, since the agent holds nothing that reaches production. That command is also the password reset until mail exists. Say in the per-project file that this is how a server gets its users.

### 3. Wrong passwords are counted only per email-and-address pair, and nothing is written down

**Where.** `app/Http/Requests/LoginRequest.php` lines 16, 38 to 48 and 70 to 73. No listener anywhere for the framework's `Failed`, `Lockout` or `Login` events.

**What is wrong.** The limit is five wrong tries a minute for one email from one address. A guesser who changes address every five tries is never slowed, and one address may try any number of different emails. Nothing is logged, so a night of guessing leaves no trace and nobody is told. This app holds ten thousand clients' details behind three passwords and nothing else.

**Evidence.**
- 100 wrong passwords for one account from 20 addresses inside one minute: 0 refused.
- 40 tries from one address against 40 different emails: 0 refused.
- 5 wrong tries and a lockout wrote 0 bytes to the application log. Listeners registered for `Failed`, `Lockout`, `Login`: none.
- What holds: after 5 wrong tries the 6th is refused even with the right password, across separate requests, with the database cache; a forged `X-Forwarded-For` header on the 6th did not slip the limit; the lock lasts 60 seconds; the same account with the right password from another address still gets in during the lock.

**The fix.** Two more limits beside the present one: one on the email alone whatever the address (for example 20 wrong tries an hour), and one on the address alone whatever the email. Log every failed try and every lockout with the email and the address, never the password; when mail exists, tell Gordon about a lockout. A limit on the email alone lets a stranger lock Peter out for a while by guessing; set it high enough that it is not hit by accident, and that is the better side of the trade. For Gordon to decide, because the plan does not ask for it: a second factor, or putting the login behind a gate such as Cloudflare Access.

### 4. SQLite as configured will fail with "database is locked" the moment two things write at once

**Where.** `config/database.php` lines 43 to 46: `busy_timeout`, `journal_mode` and `synchronous` are left unset, and `transaction_mode` is `DEFERRED`. `.env.example` has no `DB_DATABASE` line.

**What is wrong.** On a server the web requests, the queue worker and the scheduler all write to the one file (sessions, the cache and the queue are in the database too). With the default journal a writer blocks every reader; and a transaction that reads before it writes, which is what `MergeDuplicate` and `KeepApart` do, fails at once when another writer is active, without waiting. The wait that does apply is PHP's default of 60 seconds, long enough to hang a request.

**Evidence.** Pragmas read through the app's own connection on a file database, in production mode: `journal_mode=delete`, `busy_timeout=60000`, `foreign_keys=1`, `synchronous=2`. Then two connections with the app's settings: A begins a transaction and reads; B begins and writes; A's write failed after 0 ms with "database is locked", in spite of the 60-second wait. Both were rolled back.

**The fix.** In `config/database.php`: `journal_mode` `wal`, `busy_timeout` `5000`, `synchronous` `normal`, `transaction_mode` `IMMEDIATE`; and a test that opens a file database and reads the four back. Foreign keys are already on. Two consequences for later stages: with that journal the nightly backup must take its copy with SQLite's own backup, never by copying the file; and `DB_DATABASE` must name the shared path on the server (the default, `database/database.sqlite`, sits inside the release folder, so each new release would start from an empty or stale file). The second is not demonstrated here; it belongs to the deploy script and is not yet due.

### 5. The history can be bypassed, and hiding a file leaves no entry in it

**Where.** `app/Models/Concerns/RecordsHistory.php` lines 21 to 32 (it listens to `created` and `updated` only); `app/Models/File.php` lines 44 to 46 (soft delete on `hidden_at`); `app/Models/HistoryEntry.php` (an ordinary model); `database/migrations/2026_10_02_000008_create_history_table.php`.

**What is wrong.** The plan says the history lists "delete and restore" and that a merge is "reversible through the history". [doc:plan-v2.md sections 5 and 10] Today a file that is hidden gets no history entry, because the framework's soft delete writes straight to the table without the `updated` event. Any change made by a query rather than through a model is not recorded, nor is one saved "quietly". And the history's own rows can be rewritten or deleted like any others. No screen does any of this yet; stage P3 adds the delete button and will walk into the first one.

**Evidence.** In a test, signed in: hiding a file wrote 0 history rows (and `hidden_at` was set); restoring it wrote 1; a query-builder update of a client's email wrote 0; `saveQuietly` wrote 0; a history row was rewritten and read back changed; one query deleted all 4 history rows.

**The fix.** Record hide and restore explicitly (listen to `deleted` and `restored`, or write the entry in the P3 action), with a test that fails without it. Make the `history` table append-only in the database itself: two SQLite triggers, in a migration, that refuse an update or a delete of a history row. Add a line to the gate that greps `app/` for `saveQuietly`, `withoutEvents` and query updates on the recorded models, since the architecture tests cannot see method calls. [doc:laravel-kit-spec.md 5.5]

### 6. The test suite's isolation gives way to the shell's environment; the app's own tests emptied a database named there

**Where.** `phpunit.xml` lines 24 to 37: none of the `<env>` lines has `force="true"`. `tests/Pest.php` lines 9 to 11 (`RefreshDatabase` on every feature test). `tests/TestCase.php`.

**What is wrong.** A value already present in the shell wins over the test configuration. If `DB_DATABASE` is set in the shell when the tests run, the feature tests run `migrate:fresh` on that file. Values in `.env` do not have this effect, only variables in the shell or on the command line. Stage P4 brings a rehearsal database of the real history onto this Mac and agents that set database paths; one `export` followed by `composer test` empties it. The same goes for `MAIL_MAILER`: a shell that sets it gives the tests a real mailer.

**Evidence.** A scratch database with one marker row; the app's own `tests/Feature/Auth/LoginTest.php` run with `DB_DATABASE` pointing at it: 10 tests passed, marker rows afterwards 0. A one-test probe run with `MAIL_MAILER=smtp DB_DATABASE=<file>` reported `mail=smtp` and that file as its database; without them it reported `mail=array`, `db=:memory:`. `grep -c 'force=' phpunit.xml`: 0. On a server this cannot happen in production mode: the test runner is not installed there and `migrate:fresh` is refused.

**The fix.** `force="true"` on every `<env>` line of `phpunit.xml`. In `tests/TestCase.php`, refuse to start unless the environment is `testing` and the default database is `:memory:`. When P4 adds the old-system connection, pin that one in `phpunit.xml` too, so no test can open the real `legacy.sqlite`.

### 7. The version line and the log probe are absent

**Where.** `routes/web.php` (no version route); no probe command anywhere (`git ls-files` has no console command); no version file; no `CHANGELOG.md`.

**What is wrong.** The kit asks every app for a version line (version and commit) on an address that needs no login, and for a log probe that refuses to exist in production with a test asserting it. [doc:laravel-kit-spec.md sections 4, 5 and 7 "laravel-new"] The ship script reads the version line to prove what production runs; without it there is no parity proof. Neither is needed to use the skeleton locally. Both are needed before the first deploy.

**Evidence.** `GET /version` is not a route (the production route list has 18 routes, listed in finding 2). `grep -ri probe app routes` finds nothing.

**The fix.** Add both from the kit's template when the kit track delivers it, before step B. The version line must give the version and the commit and nothing else. The probe's two forms must both refuse in production, with the test the spec asks for.

---

## Minor

### 8. "Nothing is destroyed" is a habit of the screens, not a property of the models

**Where.** `app/Models/Client.php`, `app/Models/Property.php` (no soft delete); `app/Models/File.php` line 44.

**What is wrong.** No route deletes anything, and a file's "delete" is a mark. But the models will destroy a row if asked. **Evidence:** in a test, `File::delete()` kept the row; `Client::delete()` on a client with no file removed the row; `File::forceDelete()` removed the row; `Client::delete()` on a client with a file was refused by the foreign key. No migration cascades a delete (`grep -i cascade database/migrations`: nothing). **The fix,** before P3 adds the delete button: the models refuse (a `deleting` listener that throws on `Client`, `Property`, `Invoice`, `Send`, `Source`, `HistoryEntry`; `forceDeleting` that throws on `File`), each with a test.

### 9. "Keep me logged in on this computer" lasts 400 days

**Where.** `app/Http/Requests/LoginRequest.php` line 40; `resources/views/auth/login.blade.php` lines 11 to 14; nothing sets the duration, so the framework's default applies.

**Evidence.** The cookie set by a login with the box ticked expires in 400 days; it is `HttpOnly`, `SameSite=lax`; with only that cookie and no session, `GET /` answered 200. What holds: after a logout the same cookie was refused (302 to `/login`), because logging out renews the stored token, which ends every remembered computer for that person. **The fix:** a shorter life, for example 30 days, set in the guard's configuration. For Gordon to choose the number.

### 10. The app believes whatever host name the request carries

**Where.** `bootstrap/app.php` lines 16 to 18 (no trusted hosts, no trusted proxies).

**Evidence.** `GET /` with `Host: evil.example` answered `Location: http://evil.example/login`. I could not turn this into a redirect a stranger controls: a browser cannot be made to send a forged host to the real server, and Forge's web server answers only for the site's own name unless the site is the server's default. Not demonstrated as a hole. **The fix:** `trustHosts` with the site's own name, and decide `trustProxies` when it is known whether Cloudflare sits in front (if it does, the address the login limit sees is Cloudflare's, and the session cookie's secure flag depends on it).

### 11. No protective headers, pages with client data may be kept by the browser, and robots are invited in

**Where.** `bootstrap/app.php` (no middleware); `public/robots.txt` (an empty `Disallow:`); `resources/views/components/layout.blade.php`.

**Evidence.** `GET /login` in production mode returns no `X-Frame-Options`, `Content-Security-Policy`, `X-Content-Type-Options`, `Referrer-Policy` or `Strict-Transport-Security`, and does return `X-Powered-By: PHP/8.5.10`. The dashboard answers `Cache-Control: no-cache, private`, not `no-store`. The login page has no `noindex`. Forge's web server adds some of these itself; that is not confirmed here. **The fix:** one small middleware for the headers and `no-store` on every page behind the login; `Disallow: /` in `robots.txt`.

### 12. A forged page cursor is a server error

**Where.** `app/Http/Controllers/DashboardController.php` line 17; `app/Http/Controllers/FileController.php` line 35.

**Evidence.** Signed in, `GET /?cursor=<valid base64 of a JSON object without the expected keys>` threw `UnexpectedValueException: Unable to find parameter [scheduled_at] in pagination item`. A cursor that is not base64 at all answered 200. Only a logged-in user can reach it; with debugging on it becomes a debug page. **The fix:** catch it and show the first page, with a test.

### 13. The login treats capitals in the email address as a different address

**Where.** `app/Http/Requests/LoginRequest.php` lines 23 to 27 and 40.

**Evidence.** A user stored as `ada.probe@example.test`; a login with the right password and `Ada.Probe@Example.test` was not authenticated. Clients' emails are lowercased on save (`app/Models/Client.php` line 134); users' are not, and the login does not lowercase what is typed. Not a hole (the limit's key is already lowercased), but it will lock a person out on a phone that capitalises. **The fix:** lowercase the email before validation in `LoginRequest`, and on save in `User`.

### 14. Tinker is installed on servers

**Where.** `composer.json` line 13 (`laravel/tinker` under `require`, not `require-dev`).

**What is wrong.** The kit's rule is no tinker on staging, and its guard refuses the word. [doc:laravel-kit-spec.md sections 6 and 8.3] The package is still shipped to every server, where anyone with a shell can run it. **Evidence:** `php artisan tinker --execute=...` ran in production mode in this review (it is how the pragmas in finding 4 were read). **The fix:** move it to `require-dev`, once finding 2's command exists so nobody needs it.

### 15. The three roles are stored and decide nothing

**Where.** `app/Policies/FilePolicy.php` lines 17 to 38 (every answer is `true`); `app/Enums/UserRole.php`.

**What is wrong.** Not a hole: the builder says so in the policy, and the plan sets no limits per person. But a reader of `users.role` would think the treasurer is limited to payments. **Evidence:** the builder's own test "lets each of the three people work on every file" passes for all three roles in the suite I ran. **For Gordon:** say whether any of the three should be unable to do something (change a price, answer a duplicate prompt, and later delete or change Settings). If not, leave it and say so in the per-project file.

### 16. Three real names are in the repository

**Where.** `config/hd.php` lines 29, 70, 76, 82; `.env.example` line 69; `database/factories/FileFactory.php` line 38; four test files.

**What is there.** The names of the three people who use the system (the inspector's name is also the default printed on a file). Their email addresses in the repository are invented ones at `hdonline-v4.test`. I found no client's name, address, email or letter in any tracked file or in the history of the eight commits, no key or token, and no database, dump or export (`git log --all` searched for secret-shaped strings and for data files; the only hits are the three seed passwords of finding 1 and framework text). **For Gordon:** these names in a private repository are probably what he wants; said here so it is a decision and not an accident.

### 17. Whether a wrong password answers more slowly for a real account than for an unknown one (not demonstrated)

**Where.** `app/Http/Requests/LoginRequest.php` line 40.

**What was measured.** In production mode on this Mac, hashing at cost 12: four wrong tries on a known account took 0.213 to 0.216 seconds; four on addresses nobody has took 0.214 to 0.218. No difference: the framework holds every answer to at least 0.2 seconds. On a slower server the hash may take longer than that floor, and a known account would then answer measurably later. Not demonstrated; it cannot be without the server. **The fix,** if it shows on staging: raise the floor (the guard's timebox) above the hash time. Three accounts with guessable addresses make this a small matter.

---

## What was checked and holds

**The login (hand-written, checked hard).**
- **Hashing.** Passwords are stored as bcrypt at cost 12 outside the tests (`$2y$12$` on all three seeded rows; the tests use cost 4 by design). The `password` column is cast `hashed` and hidden from serialisation (`app/Models/User.php` lines 16 and 29).
- **Session renewed at login.** Each request run in a new application with only the cookies handed to it, database sessions: the session id changed at login; the visitor's old session row was gone from the table; the pre-login cookie afterwards opened nothing (302 to `/login`); the new one opened the dashboard (200).
- **Logout.** The session id changed again, the logged-in row was gone, and replaying the cookie that had been valid a moment before was refused (302 to `/login`). The remember cookie was cleared and its replay refused.
- **Forgery check.** Over HTTP in production mode: `POST /login` with no token 419; with a session cookie and a wrong token 419; with `Sec-Fetch-Site: cross-site` and no token 419; `POST /logout` with no token 419; `PATCH /files/1` with no token 419. Every form that changes anything carries `@csrf` (9 POST forms, 9 `@csrf`; the one GET form is the search box).
- **Cookies.** Session cookie `HttpOnly`, `SameSite=lax`, 120 minutes. The secure flag follows the request (absent over plain HTTP here, as expected); finding 1's fix sets it outright.
- **Hostile input to the login.** A 200,000-character password, arrays in place of strings, a malformed-byte email, a garbage session cookie: 302 or 422 each time, never a server error.
- **What a visitor who is not logged in can reach.** In production mode, of 18 routes: `/login` (GET 200, POST), `/up` (200, says only that the app is up), and the framework's two storage routes, which need a signed address (`GET /storage/x` 404, `PUT /storage/x` 404, nothing written). Every other route answered 302 to `/login`, or 401 for a JSON request, and a guest's attempts at seven changing routes (new file, the three corrections, both answers to a client match, logout) left every table's row count unchanged; the builder's own test covers all thirteen. `/.env`, `/../.env`, `/composer.json` and `/telescope` answered 404.
- **What a logged-in user can do that they should not.** Nothing found beyond finding 15. A hidden file answers 404 to view and to every change. The duplicate routes answer only for a pair the matcher is suggesting (the builder's tests, which pass).

**Input and output.**
- **Mass assignment.** Extra fields sent with each form were ignored: on a file `client_id`, `property_id`, `hidden_at`, `letter_doc_id`, `calendly_event_uri`, `id`; on a client and a property `merged_into`, `name_key`, `place_key`, `id`; on a new file `status`, `inspector`, `client_id`, `hidden_at`, `client[merged_into]`, `property[place_key]`. None was stored. Every model names its fillable columns; every controller passes only validated data.
- **Validation.** Every form that takes input has a form request (login, new file, file, client, property). Prices of 1000000.01, -1, 1e3, a 20-digit number and 12.345 were each refused; `$1,250.00` was accepted and stored as 125000 cents.
- **Escaping.** No `{!! !!}` in any view (grep: none). A script tag and an attribute-breaking string put into every text field of a client, property, file and user name came back escaped on the file screen (45 escaped occurrences, 0 raw), the second file's screen with its duplicate prompts (27, 0), the dashboard (11, 0), the dashboard with a search term (13, 0), the scrolled-rows fragment (10, 0) and the refused new-file form (4, 0).
- **SQL by hand, files, redirects.** No raw SQL anywhere in `app`, `database` or `routes` (grep: none). No upload, download or path handling exists yet. Every redirect goes to a named route; the only "intended" redirect returns to the address the visitor first asked for, on this site.

**The database.**
- Foreign keys are on (`foreign_keys=1` read at run time). No cascade anywhere.
- All 14 migrations only create tables; none can lose data going up. Each `down()` drops what its `up()` made.
- In `production` and in `staging` the five destructive commands, `migrate:rollback` among them, were refused with `--force`. The builder's note stands: the kit must settle how a rollback is run on a server.

**The repository.** `.env` is not tracked; the required ignore entries of kit spec 8.5 are present (`.gitignore` lines 29 to 37); `composer audit` reports no advisories.

---

## Kit spec section 5, item by item

| Item | State at P1 |
|---|---|
| Isolation 1: stray HTTP requests refused in the base test case | **Present**, verified: a request to an unfaked address threw `StrayRequestException` (`tests/TestCase.php` line 17) |
| Isolation 2: test config with the in-memory mailer, the in-process queue and dummy credentials for every integration | **Present** for mail (`array`) and queue (`sync`), verified at run time; dummy credentials **not yet due** (no integration exists until P2). Weakened by finding 6 |
| Isolation 3: one wrapper class per outside service, a fake, and an architecture test forbidding the vendor client elsewhere | **Not yet due** (no outside service at P1). One rule is already there: controllers may not use the HTTP client |
| Architecture tests: no `dd`/`dump`, no `env()` outside config, controllers without the database facade | **Present**, and passing inside the 302. I did not break the code to see them fail |
| Lazy loading prevented outside production | **Present** (`AppServiceProvider.php` line 28) |
| Destructive-command switch | **Present** (`AppServiceProvider.php` line 31), verified in `production` and `staging`; undone by finding 1 |
| Log probe | **Absent** (finding 7); due before the first deploy |
| Version line | **Absent** (finding 7); due before the first deploy |
| Required `.gitignore` entries and `.gitattributes` | **Present** |
| Deploy script, version file, `CHANGELOG.md`, per-project rules file, job file | **Absent**; not yet due at P1 (the kit's template and step B). The deploy script is where findings 1 and 4 need their checks |

---

## The three checks, run by me on 2026-10-02 at 01:36 CEST, PHP 8.5.10 through Herd

| Command | Result |
|---|---|
| `herd composer test` | passed: 302 tests, 302 passed, 935 assertions, 0 failed, 3.15 seconds |
| `herd composer lint` (`pint --test`) | passed, exit 0 |
| `herd composer analyse` (Larastan, level 8) | passed: 0 errors, exit 0 |
| `herd composer audit` (not asked for; the kit's gate includes it) | no security advisories, exit 0 |

These match the builder's report in `build-log-app.md`.

My own probes: 16 scratch tests in three files (12 on input, output, history and the limiter; 3 on the session flow with a new application per request; 1 on isolation), all run to completion, and about 60 `curl` requests to two scratch servers on `127.0.0.1`. One note for the builder's Herd finding: `herd php` hung when run from the `public/` folder (the Herd app still does not answer), so the scratch servers were started with Herd's `php85` binary directly; I stopped both.

## For the stages that follow

- P2 onward stores PDFs. The framework's storage route hands a private file to whoever holds a signed address, with no login. That is how a temporary link works; decide on purpose whether invoices and letters are ever served that way.
- P3: findings 5 and 8 before the delete button.
- P4: finding 6 before the rehearsal database exists, and pin the old-system connection in the test configuration.
- Before step B: findings 1, 2, 4 and 7, and the server's environment written out line by line in the runbook from the corrected `.env.example`.
