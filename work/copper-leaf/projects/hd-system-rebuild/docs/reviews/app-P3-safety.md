---
name: Home Directions v4 review, app stage P3, safety lens
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: Independent review of Calendly, search, change history, delete and restore, Settings and Connections (stage P3, steps F and G) asking one question, is it safe to put on a server and safe with people's data: 13 numbered findings, each with the file and line, what is wrong, the request or test that was actually run and its result, the fix and a weight; then what was checked and holds, question by question, whether the P1 and P2 fixes still hold, the new dependencies, and the real numbers from the three checks
sources: ["[repo:/Users/gordonium/Dev/clc-laravel/hdonline-v4, branch feature/v4-build, commit 840e5e4; P3 is 9a61adf..840e5e4]", "[doc:build-handoff.md]", "[doc:build-state.md]", "[doc:plan-v2.md sections 2, 5, 8, 9, 10]", "[doc:laravel-kit-spec.md section 8]", "[doc:build-log-app.md, P3]", "[doc:reviews/app-P1-safety.md]", "[doc:reviews/app-P2-safety.md]", "[web:developer.calendly.com/api-docs/overview/webhooks/webhook-signatures.md, read 2026-10-02]", "[run: herd composer test (three times), lint, analyse, audit in the app folder, 2026-10-02 19:48 to 19:50 CEST]", "[run: 50 scratch probe tests in 10 files, about 420 HTTP requests to a scratch copy served in production mode on 127.0.0.1, 7 parallel runs of hd:calendly-check on a scratch file database, the suite under a hostile shell, 200 isolated runs of one test, 2026-10-02 19:51 to 20:16 CEST; the scratch copy and its data were outside the repository and are removed]"]
status: written 2026-10-02 20:30 CEST by a reviewer that did not write the code; 1 blocker, 2 should-fix, 10 minor; no code was changed, nothing was staged or committed, no scratch file is left; no password, key or client detail appears in this file
---
# Review: app stage P3 (Calendly, search, history, delete and restore, Settings), safety lens

Reviewer: Claude, model `claude-opus-5-5` (Opus 5.5). I cannot see my own effort level. I did not write the code and I changed none of it. I reviewed `840e5e4` on `feature/v4-build`. While I worked, another agent committed `783e9db` at 20:05 (the P4 import's test pinning: `.env.example`, `config/database.php`, `config/hd.php`, `phpunit.xml`, three test files) and left untracked import files from 20:12. None of them touches a file named below; my three checks ran from 19:48 to 19:50 on the clean `840e5e4` tree.

**The conclusion first.** The door from the outside is well built. The receiving address `POST /hooks/calendly` turns away anything not signed with the server's key, checks the signature the way Calendly's own manual describes, compares it in constant time, refuses old and future timestamps, and is safe to receive twice: I replayed a booking's notices over HTTP and in tests, in both orders, and nothing more happened. The real Calendly class sends its token to Calendly's address and nowhere else; no token reached a row, the log, a page or a mail in any failure of the kinds Calendly documents; the day-long alarm mailed three times in three days of outage, not 288. Overlapping checks did not make a single duplicate file in 450 bookings. Search builds no SQL from what is typed and answered in under 50 ms over ten thousand files. Every new route asks for a login, the form token and the gate. One thing is a real hole, and it is in the letters, not in the door: a Doc a person has written in goes to Drive's trash when the client cancels, if any correction was written into the Doc after the person wrote. The file then says nobody wrote in it, and Drive empties its trash after thirty days (as the code itself says). That is the blocker. Two things should be fixed: any one of the three logins can quietly take over another login, and one press can switch the whole Calendly intake off with nothing on the Dashboard to say so. Ten are small.

Weights: **blocker** is a way for an outsider to create, change or read records, to make the system act on a forged booking, or to lose data; **should-fix**; **minor**.

How the evidence was made. The app at `840e5e4` was copied with `git archive` (plus `vendor` and the built assets) into a scratch folder under the session's temp directory. The bad cases were run there as Pest tests with the app's own runner and helpers, on in-memory databases, with Calendly, Google and Brevo as the stand-ins or faked with the framework's HTTP fake. Where the question was what a server does, the copy was served in production mode on `127.0.0.1` from a scratch SQLite file (ten thousand invented files, three invented logins whose random passwords were made inside a script and never printed), and asked with `curl` and a small Python client that signed notices with a scratch key. Concurrency was tested with real processes on one scratch database. Nothing was sent to Calendly, Google or Brevo; the mailer was the log mailer or the test array. The client data folder and Downloads were not opened. All scratch files are removed.

---

## Blocker

### 1. A Doc a person has written in goes to the trash on a cancellation, if a correction was written into it afterwards; the file then says nobody wrote in it

**Where.** `app/Actions/PrepareLetter.php` lines 82 to 83 (after every write the system makes into the Doc, it records the Doc's latest revision as its own); `app/Jobs/PutAwayUntouchedLetter.php` line 63 (a Doc is "untouched" when its revision equals the one last recorded) and line 74 (trash); dispatched from `app/Actions/HearBooking.php` line 170; `resources/views/files/show.blade.php` line 432 ("the booking was cancelled and nobody had written in it").

**What is wrong.** Gordon's rule is "an untouched Doc goes to Drive's trash, an edited one stays" [doc:plan-v2.md section 2], under "nothing is destroyed" [section 4]. The code does not ask "has anybody but the system ever written in this Doc?"; it asks "has anybody written since the system last wrote?". Every system write moves the mark forward: a corrected name or address ("fix it once"), a stamp that follows a corrected state, the "bring the letter up to date" button when it has something to write (read in the code; the corrected name was run, below). So a person's writing is absorbed into the system's own revision by the next correction, and a later cancellation, by the client in Calendly or by the firm there, puts that Doc in the trash. The code's own comment says Drive empties its trash by itself after thirty days (`PrepareLetter::takeOutOfTheTrash`); I did not check that against Google. Until then the Doc can be taken out, but the file screen tells the reader that nobody had written in it, so nobody has a reason to look.

**Evidence.** With the stand-in Doc store, a booking through Calendly's notice, then words typed into the Doc as Peter would, then the client's notice of cancellation:
- No correction in between: revisions made 2, after the person 3, recorded by the system 2; on cancellation the Doc stayed (the builder's own test covers this case).
- One correction in between (the client's surname changed through `PATCH /files/{file}/client`, as Maria Pia would): revisions made 2, after the person 3, recorded by the system **5**, Doc now 5. On cancellation the Doc went to the trash with the person's words still in it, `letter_trashed_at` was set, and the file screen shows the "nobody had written in it" line.
With Google the same follows by construction: the fill is a write, and the revision read after it is the newest one, which comes after the person's.

**The fix.** Remember that a person has written, once and for good: before each system write in `PrepareLetter`, read the Doc's revision; if it differs from `letter_revision`, mark the file (for example `letter_touched_at`) before writing. `PutAwayUntouchedLetter` refuses when the mark is set. With Google, the revision list can also say who made each revision (`lastModifyingUser`), which answers "anybody but the app's own account" directly. A test: write, correct, cancel; the Doc stays. While there: `takeOutOfTheTrash` treats any 404 as "the Doc is gone" and forgets its identifier (`PrepareLetter.php` lines 113 to 120); Drive also answers 404 when the app's account has lost access to a file, so a change of sharing would detach a Doc from its file (read in the code, not demonstrated; the old identifier survives in the change history).

---

## Should-fix

### 2. Any one of the three logins can take over another, add logins and raise its own role, and nobody is told

**Where.** `app/Providers/AppServiceProvider.php` line 127 (`manage-settings` is true for everyone, on purpose); `app/Http/Controllers/SettingsUserController.php` lines 23 to 40 (add a login; change any login's name, address and role); `app/Http/Requests/SaveUserRequest.php` line 32 (any role, one's own included); `app/Http/Controllers/SettingsUserPasswordLinkController.php` lines 19 to 25; `app/Models/User.php` line 49 with `app/Http/Controllers/Auth/PasswordController.php` line 39 (setting a password leaves no line in the change history).

**What is wrong.** The openness is intended, not accidental: the builder's decision 17 and question 6 for Gordon say so, and the plan sets no limits per person. What is missing is any notice. One login, or anybody holding one login's browser session, can change another login's address to their own, mail that login a set-your-password link, set the password and sign in as that person; or add a login of their own that outlives a password change; or switch the others off. The only trace is one history line on the Settings screen.

**Evidence.** In a test, signed in as a second login: Peter's login address changed to another address (accepted), "send a password link" pressed (the link went to the new address), signed out, the password set through the link, then signed in: the session was Peter's. History for Peter's login: "created" and "email changed by user 2"; nothing for the password; 0 messages to Peter's old address. A login raised its own role to `admin` (accepted; roles decide nothing today, so no gain yet). Twenty-five new logins added in a row: 25 messages mailed to 25 addresses, no limit.

**The fix.** Mail the person at the old and the new address when a login's address changes, and all three people when a login is added or switched off; write "password set" (no value) into the change history; nobody changes their own role. Whether only Gordon should manage logins is Gordon's question 6.

### 3. One press switches the whole Calendly intake off, and nothing on the Dashboard or by mail says so

**Where.** `app/Actions/StopTakingBookings.php` lines 25 to 42; `app/Actions/CheckCalendly.php` line 55 (with bookings off the check does nothing, quietly); `app/Http/Controllers/DashboardController.php` lines 41 to 42 and `resources/views/dashboard.blade.php` lines 9 to 21 (the Dashboard shows raised trouble and waiting bookings only).

**What is wrong.** The plan's answer to "Calendly stops notifying" is the 15-minute check plus an alarm after a day [doc:plan-v2.md section 10]. "Switch bookings off" turns off both, silently, for any of the three logins, by mistake or otherwise. Clients go on booking in Calendly and are told they are booked; no file opens. When bookings are switched on again, those bookings wait as "earlier" for a person's word, and appointments that took place while bookings were off are never fetched, because the check looks back one day only (both read in the code, `HearBooking.php` line 83 and `CheckCalendly.php` line 65).

**Evidence.** In a test: bookings on, one booking through a notice (one file); then `DELETE settings/calendly/bookings` as a signed-in user; a second client books and Calendly's notice arrives; 288 checks over three days. Result: 1 file, 1 booking row (the second booking left no row at all), 0 checks did anything, 0 messages, and the Dashboard, after the one-time note of the press itself, did not mention Calendly.

**The fix.** Once bookings have been on, show "Bookings from Calendly are off since ..., by ..." on the Dashboard to everybody, and raise it through `RaiseTrouble` when it has lasted a day, like any other trouble. With a test.

---

## Minor

### 4. Every booking on the Calendly account is fetched and kept for good, appointment types the firm does not offer included

**Where.** `app/Calendly/CalendlyApi.php` lines 71 to 96 (every scheduled event of the user, then each one's invitees); `app/Models/CalendlyBooking.php` lines 51 to 65 (the booking as told is kept in `details`); `app/Actions/HearBooking.php` lines 87 to 90 (an unmatched type waits); `resources/views/settings/edit.blade.php` lines 270, 294 and 307 (names, and for shared appointments the email, shown to all three).

**Evidence.** A booking of an invented type "Dentist reminder": kept as a waiting row with the person's name, email, phone and every answer (`details` keys: name, first and last name, email, phone, answers, place, cancel reason and the rest); the name is on the Settings page and the Dashboard says a booking is waiting. Rows are never destroyed. This matters only if the firm's Calendly account holds other appointment types (the plan names two; unconfirmed).

**The fix.** Skip events whose type is not mapped before asking for their invitees, and keep nothing of them; or keep only the type's name and the time.

### 5. The receiving address accepts a signature for 25 hours; Calendly's own manual uses three minutes; the key's strength is not checked

**Where.** `app/Calendly/Signature.php` line 26 (`25 * 3600`) and line 33 (any non-blank key); `app/Actions/StartTakingBookings.php` lines 45 to 51; `routes/web.php` line 48 (`throttle:240,1`, by connecting address).

**What is wrong.** Calendly's manual gives the same scheme the app uses (header `t=...,v1=...`, HMAC-SHA256 of the timestamp, a dot and the body) and a replay tolerance of "3 minutes" [web:developer.calendly.com webhook-signatures, read 2026-10-02]. The app's 25 hours rest on retries carrying their first timestamp, which the manual does not say. Replays are harmless today (below), so this is defence in depth. A one-character `CALENDLY_SIGNING_KEY` would be accepted and handed to Calendly.

**Evidence.** In tests: 25 h less 5 s accepted, 25 h plus 5 s refused, 295 s in the future accepted, 305 s refused. Over HTTP: one signed notice sent seven times: 204 each, one file, the booking row's count of hearings went up each time; a cancellation, then the first notice again 20 hours later in a test: no new file, the status a person had set back stayed, no new history line. Rate limit over HTTP: of 260 junk requests from one address, the first 226 were answered 403 and the rest 429 (my earlier probes had used the rest of that minute's 240); a genuinely signed notice from the same address straight after got 429. That only matters if Calendly's notices and junk share an address (a proxy in front without trusted proxies; not demonstrated, no proxy exists).

**The fix.** A tolerance of minutes, not hours (the 15-minute check covers a late retry); refuse a signing key shorter than 32 characters when bookings are switched on; decide trusted proxies when Cloudflare is decided (P1 finding 10).

### 6. A new signing key on the server never reaches Calendly; its notices are refused until Calendly gives up

**Where.** `app/Calendly/CalendlyApi.php` lines 106 to 112 (`listen` keeps a subscription that is on, whatever key it was made with).

**Evidence.** Calendly faked: bookings switched on with key one (one subscription made, key one given); the server's key changed to key two; "Set the notifications up again" pressed: no new subscription, no key given. A notice signed with key one, as Calendly would go on signing: 403. Bookings still arrive by the check, and after about a day the alarm says the notifications are off.

**The fix.** Remember a hash of the key the subscription was made with (in `connections.facts`); when it differs, replace the subscription. Until then the runbook says: after changing the key, switch bookings off and on.

### 7. Two people switching each other off at the same moment can leave no login switched on

**Where.** `app/Http/Controllers/SettingsUserLoginController.php` lines 33 to 43 (the "not your own" check reads the session's user, not the database at the moment of writing); `app/Http/Middleware/LoginIsOn.php` line 24 (checked at the start of a request).

**Evidence.** Served copy with four workers, three logins, C switched off by A; then A switches B off and B switches A off in two requests sent together: in 7 of 10 rounds all three logins were off. Nobody can then log in; the way back is `hd:user` on the server, which can make a new login but does not switch one on (it never touches `disabled_at`).

**The fix.** In one transaction (writes are `IMMEDIATE` already), read the acting login afresh and refuse if it is off, and refuse to switch off the last login that is on.

### 8. The from address may be any address, outside the firm's domain included

**Where.** `app/Http/Requests/UpdateSettingsRequest.php` line 43; `app/Mailing/FromAddress.php` line 25.

**Evidence.** Posing as staging with Brevo faked: the from address set to an address at another domain (accepted), an invoice sent: Brevo was handed that address as `sender`. Whether Brevo refuses a sender it does not know is not demonstrated (no account).

**The fix.** Accept only addresses at the domain of `MAIL_FROM_ADDRESS`.

### 9. The test buttons, the booking switch and new logins have no limit

**Where.** `routes/web.php` lines 115 to 128.

**Evidence.** "Test Calendly" pressed 60 times as one login: 60 answers, 120 requests to (faked) Calendly. A script holding one login could use up whatever request allowance Calendly gives the account, and the 15-minute check with it (the allowance's size is not known here; not demonstrated). Twenty-five new logins mailed 25 messages (finding 2).

**The fix.** `throttle:10,1` on these routes.

### 10. Some search addresses answer with a server error

**Where.** `app/Http/Controllers/DashboardController.php` lines 32 and 37 (`->string()` on a value that may be an array); `app/Search/FileSearch.php` line 71 (`Str::squish` gives null for bytes that are not UTF-8, and line 173 then refuses null).

**Evidence.** Signed in, production mode: `/?q[]=a`, `/?q=%C3%28` and `/?cursor[]=x` each answered 500 (the plain 6,592-byte page, no trace); in a test the errors were "Array to string conversion" and a `TypeError` in `FileSearch::period()`. Only a logged-in person can reach them.

**The fix.** Read `q` and `cursor` only when they are strings, and drop invalid bytes before searching; a test with these three addresses.

### 11. A booking that fails to be written puts the client's details into the log, once per retry

**Where.** `bootstrap/app.php` line 25 (nothing removes a failed query's values before it is logged).

**Evidence.** Served copy: a database trigger made the property insert fail; one signed notice, then Calendly's retry: 500 twice, and the log gained two lines holding the failed statement with its values, the invented street, town and zip among them. A failure on the client insert would log the name and email the same way. This is the framework's habit everywhere; P3 makes it reachable from outside, and Calendly retries for a day.

**The fix.** In `withExceptions`, report a `QueryException` with its SQL and without its values; a test that a failed booking logs no name, address or email.

### 12. The first check after bookings are switched on asks once per appointment, with no overall limit

**Where.** `app/Actions/CheckCalendly.php` lines 64 to 77; `routes/console.php` line 14 (`withoutOverlapping(30)`, in the foreground).

**Evidence.** Calendly faked: 40 appointments, first check 42 requests, next check 1; 250 appointments, first check 254 requests, next 3. Each request may take 30 seconds, and nothing bounds the whole, so a slow Calendly can keep one check running past the 30-minute lock, and the next one starts beside it; a hand-run `hd:calendly-check` is never locked out (both read in the code; the lock's 30 minutes read from the schedule in a test). Overlap itself is safe: three checks run side by side on one file database over 300 new bookings made 300 files; four over 150 more and 20 cancellations made 450 files and 20 cancellations, no duplicate. (In my very first parallel run two of three checks stopped on a unique constraint of `connections`, because I had switched bookings on by writing the setting directly; switching on through Settings writes that row first.)

**The fix.** A time budget for the check (stop at about ten minutes, carry on next time), and `withoutOverlapping` held for the check's real length.

### 13. A test from P1 fails by chance once in a hundred runs

**Where.** `tests/Feature/Matching/ClientMatcherTest.php` lines 58 to 63; `database/factories/ClientFactory.php` line 25 (phones drawn from 100 values).

**Evidence.** My first whole run: 1,262 tests, 1 failed ("Same name and phone number" suggested); the next two passed. The one test run alone 200 times: 2 failed. Not a safety matter, but the rule is that the gate passes before work is called done.

**The fix.** Fixed, different phones in that test, as the builder did for three others in `840e5e4`.

---

## What was checked and holds

**1. The receiving address.** Unsigned and wrongly signed notices were refused (403 over HTTP and in tests); with no key on the server it is shut (the builder's test, passing in the suite). The scheme matches Calendly's manual; `hash_equals` compares in constant time; the timestamp is checked both ways. Upper-case hex, a junk second `v1`, `v0`, no `t` and a fractional `t` were refused; `GET`, `PUT`, `PATCH`, `DELETE` answered 405. It sits outside the browser middleware, so it keeps no session and needs no form token (`routes/web.php` line 48). A signed notice while bookings are off: 204 and nothing kept. A signed notice that cannot be read: 204, and the failure written to the Connections panel names nobody. A public booking mails nobody. Markdown typed on the booking form came out as text in the client's invoice (0 links, 0 images from it): the P2 fix holds on the Calendly road. Script and attribute-breaking text from a booking (name, address, answers, type name, cancel reason) came back escaped on the File screen, the Dashboard, search results, Settings and the stand-in page (0 raw). Size: an unsigned 1.9 MB body was refused in 148 ms; a signed 1.9 MB notice was accepted and its 1,946,271 bytes kept in `details`, which needs the key; over PHP's `post_max_size` (2 MB on this Mac) the body never reaches the app (on Forge, nginx and PHP-FPM decide; not checked). What a forged notice could do needs the key: open files, move a file to another appointment (and so aim a later "also cancel in Calendly" at another appointment of the same account), cancel files (read in the code). Without it, nothing reached the database but the rate counter.

**"Also cancel in Calendly".** Only `DeleteFile` calls Calendly's cancel, behind the login, the form token and the policy. Ticked for a file typed by hand and for an appointment already past: ignored, Calendly untouched. With Calendly out of reach: nothing deleted. With Calendly cancelling and the write here failing: the file was left booked and visible, and Calendly's own notice of the cancellation later marked it cancelled, so nothing is lost.

**What is kept of a notice.** Not the raw body: the booking as read (names, email, phone, every answer, place, cancel reason, Calendly's addresses), per booking, for good, shown on the File screen and in Settings' waiting lists, and in the database the nightly archive copies. Not in the log, except as in finding 11.

**2. The 15-minute check.** Overlapping checks made no duplicate (finding 12). Calendly unreachable for three days, 288 checks: 3 alert mails, all to the alert address; with a mailer that cannot send, 3 attempts and the trouble still raised. The alert address comes only from the environment: a Settings save carrying `hd[mail][live]`, `mail[trap]`, `calendly[listening_since]` or a key and value changed nothing, and line breaks in the from address and the type name were refused. The token: with Calendly unreachable, answering 401, or answering 502 with HTML, 0 occurrences of a marker token in the connections row, the history, the log, Settings, the Dashboard and the alert mail. Only if Calendly's own error text contained the token would it be kept, logged, shown and mailed as it came (a made-up answer did exactly that); Calendly's documented errors do not. The token went only to `https://api.calendly.com/`: five crafted next-page addresses (another host, `api.calendly.com.evil...`, a user-info `@` trick, plain `http`, a scheme-relative address) were refused, 0 requests elsewhere.

**3. Search.** Column names are constants; every pattern is bound; `%`, `_` and `\` are looked for as typed; `' OR 1=1 --` and a `union` found nothing; the matching keys drop pattern characters. Ten thousand files on a file database in production mode, over HTTP: eight one-letter words 47 ms, one letter 18 ms, "May 2022" 7 ms, eight words and a month 35 ms, all deleted files 6 ms. Input is cut to 200 characters and 8 words. Deleted files appear only with `deleted=1`, which every logged-in person may ask for (by design, so a file can be restored).

**4. Settings and users.** Nobody can switch off their own login (refused with a message); no login can be deleted (the model refuses). Extra fields on the login forms (`id`, `disabled_at`, `password`, `remember_token`, `created_at`) were ignored. After a login was made, its link used, and the login switched off and on, the history held no hash, password, link token or remember token, and neither did the Settings page. Stamp uploads judged by their bytes (real files, not the framework's fakes, which judge by name): SVG, PHP and HTML under image names were refused, and so was a real PNG named `.php`; a PNG with PHP and HTML appended, and a GIF carrying script, were kept as `.png` and `.gif` and served as `image/png` and `image/gif` with `nosniff`; a name with `../` was ignored. Stamps live on the `records` disk outside `public/`, served behind the login or by a 30-minute signed address. A template link is cut to the Doc's identifier (P2, unchanged). The app fetches no address a person types: the HTTP client is used only in the three wrappers, against fixed hosts; the booking page link is shown, never fetched.

**5. Connections.** No key appears on the panel (above). Each test button needs the form token (419 without) and the gate.

**6. Delete and restore.** Deleting and restoring each wrote a history line naming the person who did it. A hidden file opens (200) and every one of 11 routes that change it or act on it answered 404. Force-deleting a file, deleting a client, a booking row, a connection row and a login were all refused by the models; updating or deleting history rows was refused by the triggers. A grep of `app/` for quiet or bulk writes found none (the architecture test agrees).

**7. Routes, input, output.** With the gate made to say no, all 21 routes P3 added or changed answered 403 and no table changed. As a visitor, 21 of 21 answered 302 to the login; as a switched-off login, 21 of 21 answered 302 and logged it out. Over HTTP in production mode, 15 changing routes without a form token answered 419, with and without a cross-site `Origin`, and nothing changed. The stand-in Calendly page and its check answered 404 where the real Calendly answers. Settings carries `Cache-Control: no-store`, `X-Frame-Options: DENY`, `frame-ancestors 'none'`, `nosniff` and `same-origin`. P3 adds no `{!! !!}`; the four in the repository predate it (two escape their value first, two are the framework's own mail layout).

**8. The P1 and P2 fixes still hold.**
- `.env.example`: production, debugging off, an `.invalid` address, secure cookie, log level `info`, no password; the new lines (`CALENDLY_TOKEN`, `CALENDLY_SIGNING_KEY`, `HD_ALERT_ADDRESS`) are empty.
- The live-mail switch: `off`, `no`, `1`, `yes`, `on` leave mail not live; `true` (any capitals) with the site named and production makes it live; `true` with no site named, or on staging, does not. Debugging stays off with `APP_ENV=local` on a real address.
- The tests on their own database: the whole suite under a hostile shell (`DB_DATABASE` at a scratch file holding a marker row, `APP_ENV=production`, `MAIL_MAILER=smtp`, mail live with a trap and a host, `HD_CALENDLY_DRIVER=calendly`, made-up Calendly token and signing key, an alert address, the Google driver and made-up Google and Brevo values): 1,262 passed; the marker row untouched, no table added, nothing logged.
- The mail trap now logs counts, not addresses; Google's access token is kept encrypted (read in the code).

---

## New dependencies

None. `composer.json` and `composer.lock` are unchanged from `9a61adf` to `840e5e4`, and so are `package.json` and `package-lock.json`. `herd composer audit`: no advisories.

---

## The checks, run by me on 2026-10-02, PHP 8.5.10 through Herd, in the app folder at `840e5e4`

| Command | Result |
|---|---|
| `herd composer test` (19:48) | 1,262 tests, 1,261 passed, **1 failed** by chance (finding 13), 4,976 assertions, 17.6 s |
| `herd composer test` (19:49, run twice more) | 1,262 passed, 4,976 assertions, 17.6 s each |
| `herd composer lint` | passed |
| `herd composer analyse` (Larastan level 8) | passed: 0 errors |
| `herd composer audit` | no advisories |
| the suite under a hostile shell, in the scratch copy | 1,262 passed; marker row untouched |

The passing numbers match the builder's report in `build-log-app.md`. My own probes: 50 scratch tests in 10 files, all run to completion; about 420 requests to the served copy; 7 parallel check processes; 200 isolated runs of the chance-failing test.

## For whoever fixes this, and the stages that follow

- Finding 1 before a real Doc exists; it needs a mark and a test.
- Findings 2 and 3 before cutover; both are small.
- P4 imports ten thousand clients through the same models: finding 11 decides whether a failed import row puts a real name in the log.
- Still there from P2, not mine and left alone: a second working tree registered from an earlier agent (`git worktree list`: one under the session's scratch folder, branch `p2-build` at `9706e8d`).
