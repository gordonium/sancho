---
name: Home Directions v4 review, app stage P3, plan fit
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: Independent review of Calendly, search, change history, delete and restore, Settings and the Connections panel (steps F and G) against the plan. Covers every booking sequence driven through the stand-in, a real two- and three-process race, search on ten thousand invented jobs, the history as a person reads it, the test buttons made to fail, the builder's 33 decisions against the import and the cutover, the real test numbers and the rules that have no test. 17 numbered findings, each with file and line, the evidence, the fix and a weight
sources: ["[doc:build-handoff.md]", "[doc:plan-v2.md sections 2, 4, 5, 6, 7, 10]", "[doc:requirements.md R1, R2, R6]", "[doc:phase0-brief.md, Plan questions 4 onward]", "[doc:build-log-app.md, P3 and its 33 decisions]", "[doc:reviews/app-P1-plan-fit.md]", "[doc:reviews/app-P2-plan-fit.md]", "[doc:runbook-cutover.md]", "[doc:current-system.md, How a job flows]", "[code:/Users/gordonium/Dev/clc-laravel/hdonline-v4, branch feature/v4-build, commit 840e5e4; P3 is 9a61adf..840e5e4; read 2026-10-02]", "[run 2026-10-02 19:43 to 20:15 CEST: composer test, lint and analyse on PHP 8.5.10 in a git-archive copy of 840e5e4; 34 probe tests on invented data; 50 rounds of a real two- and three-process race on a scratch SQLite file]"]
status: written 2026-10-02, finished about 20:30 CEST, by a reviewer that did not write the code. 3 blockers, 7 should-fix, 7 minor. No code was changed, nothing was staged or committed, and nothing was written except this file. No client data was opened. The scratch copy was removed afterwards. While this review ran, another agent committed 783e9db and left the import files untracked in the app repository. This review is of 840e5e4 only
---
# Review: app stage P3 (Calendly, search, history, delete and restore, Settings), plan fit

Reviewer: Claude, model `claude-opus-5-5` (Opus 5.5). I cannot see my own effort level. I did not write this code and I changed none of it.

**The conclusion first.** Most of P3 does what the plan says, and it is well built. One booking is acted on exactly once. That holds whichever road brings it, in either order, and in a real race of two and three processes. A cancellation that arrives before its booking opens nothing. A single reschedule moves the date in every order. A booking for a known client or property merges nothing: the match waits on the file, one click each way. Search finds names with accents, apostrophes (straight or curly), hyphens and second persons, and months the way Peter says them ("May of 22"). On ten thousand jobs it answers in 4 to 40 ms. The history panel is complete for the plan's list, starts folded shut, and reads as plain English. Settings has everything the plan lists, saved with history. A test button made to fail says so, with the reason.

Three things are wrong enough to stop on.

1. **A booking moved twice opens a second file**, and the first file stays "booked" on a date that no longer exists. This happens in 16 of the 24 orders in which the four notices can arrive. It also happens on the 15-minute check alone, so it is certain on a plan with no webhooks.
2. **A Doc Peter has written in goes to Drive's trash** if any correction or reschedule came between his writing and the cancellation. The file then says nobody had written in it, and Drive destroys the Doc after 30 days. That breaks Gordon's own rule.
3. **The cutover has no way to tie a booking already in Calendly to the job imported from v3.** "Bring them in" doubles every job in flight. "Leave them" lets the next reschedule double it, and lets a cancellation miss the imported file.

Seven further findings should be fixed and seven are small.

Weights: **blocker** means wrong behaviour Peter or a client would see (a lost or doubled booking, a wrong merge, lost writing) or a foundation the import or cutover cannot stand on. Then **should-fix** and **minor**.

## The numbers, run by me

These were run in a `git archive` copy of 840e5e4 under my session's temp folder, with the app's own `vendor` and built assets copied in. The commands were the same composer scripts `herd composer` runs, on PHP 8.5.10 (Herd's `php85`) and Composer 2.10.2. They were not run in the app folder, so that nothing was written there.

| Command | Result |
|---|---|
| `composer test` | passed: **1,262 tests, 4,976 assertions, 0 failed**, 19.4 to 19.6 s. Run four times; all four clean |
| `composer lint` | passed (Pint, check only) |
| `composer analyse` | passed: **0 errors** (Larastan level 8) |

These match the build log exactly (1,262 / 4,976 / 0).

**How the findings were checked.** Where a finding says something happens, I ran it. The probes are 34 Pest tests in 13 files, all on invented data. They ran in the scratch copy on the app's own test setup: in-memory database, the stand-ins for Calendly and Google, no network. Each finding quotes what its probe printed. The race used three small PHP scripts that boot the scratch copy against a scratch SQLite file in its configured mode (WAL, busy timeout, IMMEDIATE transactions). Nothing was written inside the app folder. During the review the app repository moved from 840e5e4 to 783e9db, with untracked `app/Import/` files from another agent. That is not mine, and not reviewed here.

## What holds (run, not read)

- **Once, under a real race.** One booking was heard by the notice and by the 15-minute check in two OS processes started on the same instant, 40 rounds. The notice was delayed at random by 0 to 60 ms in 20 of them. Every round ended with one file and one booking row. Each road won some rounds: the notice opened the file in 22, the check in 18, and the loser answered "nothing". In 10 three-way rounds (two notices and a check at once) every round also ended with one file, `times_heard=3`. No exception in 50 rounds.
- **Every single-booking order.** The same booking was heard notice then check, check then notice, and notice twice then check twice: one file each. A cancellation heard before its booking, then the booking, then the check: `files=0 state=cancelled`. A single reschedule, cancellation first, new booking first, or by the check alone: one file, date moved.
- **Known client and property.** An imported client (email in different capitals) and an imported property ("Road" against "Rd") were booked again through Calendly. Nothing was merged (`merged=0`). The file screen showed both prompts, each with a one-click "same" and "different". One click on "same" put the file on the old client.
- **Unmapped appointment type.** It waits, and the Dashboard says a booking is waiting. Saving the type map in Settings opens its file at once, without waiting for the check.
- **Midnight and time zones** (server clock UTC). 03:30 UTC on 1 November shows as "Oct 31, 2026 11:30 pm EDT". "October 2026" finds it and "November 2026" does not. Its letter is dated October 31, 2026, and its Doc name carries 20261031. 06:30 UTC on 1 November, the day the clocks go back, shows as "1:30 am EST".
- **No address at all.** The file opens (200) as "Address not recorded" with no stamp, and the booking as typed is shown on the file.
- **Search** across names, accents, apostrophes (straight and curly), hyphens and second persons: "Muller", "Müller" and "MÜLLER" all find Jürgen Müller. "OBrien", "obrien" and "O’Brien" find O'Brien. "Saint Johns" and "St. John’s" find St. John's Rd. "Shad Hill Road" finds "Rd". "Dee" finds the second person. "May 2022", "may of 22", "May '22", "5/2022", "2022-05" and "show me what I did in May of 22" all give May 2022 on the firm's clock. A cancelled file is found and labelled Cancelled. A deleted one is found only among deleted files, and the empty result offers that.
- **Search speed**: 10,000 invented jobs (clients, properties, files, invoices), through the Dashboard route on the in-memory database. Searches took between 4 and 40 ms each: "Stone" 11 ms (536 found); "12 Shad Hill Rd" 29 ms; "May 2022" 4 ms; "a e i o u" 40 ms (2,982 found). The Dashboard with no search took 4 ms.
- **History.** I ran a whole job through: Calendly booking, Calendly reschedule, one-click link, email correction, price and invoice description, status, invoice sent, payment, paid copy, delete and restore. The panel showed each as its own entry with who did it ("Calendly" for the booking and the move, the person otherwise), old and new, in words. The `<details id="history">` has no `open`, so it starts folded shut.
- **Delete and restore.** Two steps. "Also cancel in Calendly" is ticked by default and offered only for an upcoming Calendly appointment. Calendly is asked first, and nothing is deleted if it refuses. The file is hidden, marked cancelled, and opens read-only with a restore button. Only `show` and the restore route find a hidden file (`routes/web.php:72-78`), so its invoice cannot be sent or paid while hidden. Its Doc is left alone. Restore brings it back as it was.
- **Settings** carries invoice texts for opinion, design and hourly; letter templates for all three; CT and NY stamps; the from address; the Calendly type for opinion and design; logins; and Connections for Calendly, Brevo, Google and the two backup stores. The backup stores show "Not set up yet" with no test button, which matches scope. Changes read in the Settings history as, for example, "From address: the standard → peter@homedirections.net" and "Bookings from Calendly switched on".
- **The test buttons when a service fails.** The Calendly stand-in out of reach gives "Not working" plus the reason. Google's real class with a revoked refresh token gives "Not working" plus Google's own words. Calendly switching its notifications off is raised at once.
- **The real Calendly class**, read against Calendly's version-2 interface as I know it. The calls checked were `GET /users/me`, `/event_types`, `/scheduled_events` with `user`, `min_start_time`, `sort=start_time:asc` and `count`, and each event's `/invitees`. Also `POST .../cancellation` with `reason`, and `GET`, `POST` and `DELETE /webhook_subscriptions` with `organization`, `user`, `scope=user` and `signing_key`. The notice shape (`event`, a `payload` invitee with `scheduled_event` inside, `old_invitee`/`new_invitee`, `rescheduled`, `cancellation`) and the `Calendly-Webhook-Signature` `t=…,v1=…` HMAC-SHA256 over `"<t>.<body>"` were checked too, as were the location types. I found nothing that plainly cannot work. What I could not run is in finding 16.

---

## Blockers

### 1. A booking moved twice opens a second file; the first stays booked on a date that no longer exists

**Where.** `app/Actions/HearBooking.php:70-79` (a new booking looks one step back only, at the booking it names) and `:151-156` (a cancellation marked as rescheduled is set to Replaced and never takes over the file of the booking it itself replaced).

**What is wrong.** A reschedule is two bookings: the old one, cancelled and marked rescheduled, and a new one that names it. The file moves only if, when the new booking is heard, the booking it names already has the file. Take a booking moved twice, A then B then C. If B is first heard as a cancellation, or not heard before C, then B's row has no file. C then opens a new file, and A's file is left behind, "booked", on A's date. The plan says "A reschedule moves the date" and "each booking is acted on once" [plan-v2 §5]. This gives a doubled booking with one ghost. On a Calendly plan without webhooks, or after Calendly switches them off (plan §10 expects that), the check is the only road. Then any client who moves an appointment twice within 15 minutes produces it.

**Evidence.**
- Probe C5e: the check alone, both moves made between two checks. Result: `files=2`. File 1 is "Oct 14 10:00 am, status booked, on the working list: yes"; file 2 is "Oct 27 10:00 am, status booked". The booking rows read: `1 replaced → file 1`, `2 replaced → file NULL`, `3 booked → file 2`. The same happens when the second move is to an earlier date.
- Probe C5f: all 24 orders of the four notices, each followed by a check. Only 8 of 24 ended right. 16 ended with two booked files, for example `c1,c2,n1,n2 -> 2 files: Oct 14 booked + Oct 27 booked` and `n2,n1,c1,c2 -> 2 files: Oct 20 booked + Oct 27 booked`. Both cancellations arriving first is a natural order when each move's two notices race.

**The fix.** Find the file through the whole chain. When any booking that names an earlier one is heard, created or cancelled as rescheduled, walk `details.replaces` back to the first row that has a file. Then give that file to every row on the chain, and move it to the newest standing booking. Test all 24 orders plus the check alone, asserting one file on the last date and none left at an old one.

### 2. A Doc Peter has written in goes to the trash when a correction or a reschedule came between his writing and the cancellation

**Where.** `app/Actions/PrepareLetter.php:82-86` records the Doc's revision after the system's own write, whatever happened before it. `app/Jobs/PutAwayUntouchedLetter.php:63-77` trusts that number. The file then says "Letter's Doc put in the trash: the booking was cancelled and nobody had written in it" (`app/History/FileHistory.php:178`, `resources/views/files/show.blade.php:431-432`).

**What is wrong.** Gordon's rule: "an untouched Doc goes to Drive's trash, an edited one stays" [gordon 2026-10-01; plan-v2 §2]. The decision says "untouched" means the Doc is still at the revision the system last left it at. But every system write (a rename, a corrected name or address, a date moved by a reschedule) records the Doc's revision as it stands after that write. Anything Peter typed before it is swallowed into the system's own number. A later cancellation then finds the revisions equal and puts the Doc in the trash. Drive empties its trash after 30 days, and the Doc goes for good. So does Peter's text: notes from the phone call, or a draft pasted in early (R3.4). The trash rule itself fits the plan. The plan's "nothing is destroyed" is about the system's rows, and an untouched Doc is a template copy the system can make again (decision 13). The fault is only in how "untouched" is judged.

**Evidence.**
- Probe C17a: booking; Peter types a note into the Doc; Maria Pia corrects the surname; the client cancels. Revisions: "system left 2; Peter typed → 3; after the correction the file says the system left 5; Doc now at 5". Then: `status=cancelled Doc in trash=true Doc still holds the typed note=true`.
- Probe C17b: Peter types, the client reschedules, then the client cancels: `Doc in trash=true Doc holds the notes=true`.
- Probe C17c, the control: typed, then cancelled with no system write between: `Doc in trash=false`.
- After the stand-in empties its trash as Drive does, `Doc a exists=false Doc b exists=false`.
- Probe C17d: the file screen and its history both say "nobody had written in it".

**The fix.** Before any write to the Doc, compare its revision with `letter_revision`. If they differ, somebody wrote in it: set a mark on the file that never clears (for example `letter_written_in_at`), and never put such a Doc in the trash. Move `letter_revision` on only when the Doc was still at the recorded revision before the write. Consider also reading the revision from the Docs API's `documents.get` `revisionId`. Google documents an unchanged ID there as an unchanged document; I know of no such promise for Drive's `revisions.list`. That second point is not demonstrated. Tests: C17a and C17b.

### 3. The cutover cannot tie a booking already in Calendly to the job imported from v3

**Where.**
- `app/Http/Controllers/SettingsEarlierBookingsController.php:26-42` and `app/Actions/LeaveEarlierBookings.php:23-29`: all the earlier bookings are brought in, or all are left.
- `app/Actions/HearBooking.php:77-85`: a reschedule of a booking that is waiting or was left opens a new file by itself.
- `app/Http/Controllers/DashboardController.php:41`: earlier bookings are not counted on the Dashboard.
- The build log's P3 note for P4: "A migrated file is not a booking: no `calendly_bookings` row".
- `docs/runbook-cutover.md:185`: "The duplicate check is there for exactly this".

**What is wrong.** v3 takes its appointments from a form filled in by hand and holds no Calendly identifiers [current-system.md, How a job flows, 1]. So at the cut, every job booked for after the cut exists twice: as a job imported from WordPress, and as a booking in Calendly. Neither knows the other. When bookings are switched on, those bookings wait as "made before bookings were switched on", and a person has two buttons, both wrong:
- **Bring them in** opens a second file for every job in flight.
- **Leave them** marks them done, so their cancellations never reach the imported file. The next reschedule, being made after the switch, opens a new file anyway.

The duplicate check the runbook counts on compares clients and properties, not jobs: it offers to link the two client rows, never the two files. On the day Gordon chose as "one hard cut" with no trial [plan-v2 §6.5], Peter would see doubled jobs, or an imported job still "booked" for an appointment that Calendly has cancelled or moved.

**Evidence.**
- Probe C16, with an imported job on Oct 20 and the same appointment in Calendly, made before switch-on. At switch-on: `waiting_for=earlier files=1`. "Leave them", then the client moves it to Oct 27: `files=2 imported file date=Oct 20 new file opened=yes`. "Bring them in" for a second imported job: `files=3`. A left booking cancelled later: `row=cancelled (no file to mark)`, and the imported job stays booked.
- Probe C15: a booking made while bookings were switched off by mistake for half an hour waits as earlier, with `files=0` and `Dashboard banner=no`.

**The fix.** A choice per booking:
- "this is that file": link the booking to an existing file, writing its two Calendly names onto the file and setting the row to booked with that file. Suggest the file by the same email and the same appointment time.
- "open a file".
- "leave it".

Beyond the per-booking choice:
- A reschedule or cancellation of a booking still waiting stays with it and never opens a file by itself.
- One of a booking that was left is shown to a person.
- Earlier bookings are counted on the Dashboard banner.

Tests: the C16 sequences, asserting one file that follows Calendly. Then correct line 185 of the runbook.

---

## Should-fix

### 4. A client's reschedule of a file Peter cancelled by hand is swallowed

**Where.** `app/Actions/HearBooking.php:124-142`: line 131 moves the date only while the status is open. Decision 11. Separately, `app/Http/Requests/UpdateFileRequest.php:50` lets the status be set to cancelled by hand without offering to cancel in Calendly, unlike the delete dialog.

**What is wrong.** A client phones to cancel, and Peter sets the file to Cancelled, which is natural. The appointment stays standing in Calendly. The client then uses Calendly's reschedule link. The file stays cancelled on the old date, off the working list, with only a line in the folded history. The plan says "A reschedule moves the date" [plan-v2 §5]. A client who reschedules has an appointment.

**Evidence.** Probes C6 and C6b. After the hand cancellation: `status=cancelled calendly side status=active`. After the client moved it to Oct 28: `status=cancelled date=Oct 14, 2026 10:00 am new booking row=booked`. `Dashboard lists the file=no; any banner (alert/status)=no`.

**The fix.** A reschedule of a file cancelled by hand reopens it, as booked on the new date, and says so in the history. Closed files may keep decision 11. Setting a file to cancelled by hand while its Calendly appointment stands offers the same "also cancel in Calendly" box as delete. Test both.

### 5. The 15-minute check itself is not watched: stopped, failing for its own reasons, or without a token, nothing is raised

**Where.**
- `app/Actions/CheckCalendly.php:55-57`: with bookings on and no token, it returns quietly.
- `:64-77`: only `CalendlyUnavailable` is written down. Anything else leaves nothing on the Connection.
- `routes/console.php:14`.
- `app/Http/Controllers/DashboardController.php:42`: the Dashboard shows only trouble that has been raised.

**What is wrong.** The plan answers "Calendly stops notifying" with "the 15-minute check covers it; a failure lasting a day is alerted" [plan-v2 §10]. The notices are watched well. The safety net is not. These all leave notices arriving and the net silently gone:
- a server whose scheduler never runs;
- a check that throws a database error on every run;
- a token taken out of the environment while bookings are on.

**Evidence.**
- Probe C18c: no check for three days, notices on: `raised=false Dashboard alert=no Connections badge=Working last worked=2026-10-05 09:00:00` on 2026-10-08.
- Probe C18d: two days of checks (192 runs) each throwing `Illuminate\Database\QueryException`: `recorded failure=NULL trouble=NULL raised=false Dashboard alert=no`.
- The no-token case is asserted by the builder's own test "does nothing while the server holds no Calendly token".

**The fix.**
- Every check records that it finished, and any failure, in a `finally`.
- With bookings on, raise "the 15-minute check has not finished since …" when the last finished check is more than about an hour old. Show it on the Dashboard and send it to the alert address once a day.
- Bookings on with no token is trouble at once.

Tests: move the clock, and make the check throw something other than `CalendlyUnavailable`.

### 6. The Connections panel stays "Working" while letters and mail fail in use

**Where.**
- `app/Models/Connection.php:70-74`: the badge is the last success against the last failure.
- Successes in use are recorded (`app/Actions/PrepareLetter.php:85`; `app/Providers/AppServiceProvider.php:149`). Failures in use are not (`app/Jobs/KeepLetterCurrent.php:55-62`; `app/Mailing/Outbox.php:101-102`).
- `app/Mailing/MailCheck.php:32-36` and `BrevoTransport::check()` ask Brevo only whether the key is known.

**What is wrong.** The panel is meant to show "whether each is working and when it last succeeded" [plan-v2 §5, Settings]. One good test, or one good send, leaves it green for good. The next day the Google refresh token can be revoked, or Brevo can start refusing the key. Every new letter fails, every send is refused, and the panel still says Working. The from address in Settings is a sender Brevo must accept, as the form's own hint says. A typo there would stop all mail, and the Brevo test does not look at it.

**Evidence.**
- Probe E3 (Google): a good test, then sign-in refused in use. Result: `badge=Working; letter made=false; Connection failure recorded=NULL`.
- Probe E3b (Brevo): after the test said "Brevo answered: it knows this server's key, for the account \"Home Directions\"", a send was refused with 401. Result: `badge=Working; failure recorded=NULL`.
- What Brevo answers for an unknown sender is not demonstrated.

**The fix.** Record failures in use on the Connection: the letter job's catch, a refused or failed send. Have the Brevo test also check the from address against Brevo's list of senders. Tests for both.

### 7. A Connecticut or New York booking typed without its state gets no stamp, without a word, and its letter goes out unstamped

**Where.** `app/Calendly/TypedAddress.php:51` (the state is read from the words only); `app/Enums/Stamp.php:17-20` (no state means no stamp); `app/Actions/OpenFile.php:72`.

**What is wrong.** The stamp follows the property's state [plan-v2 §2; phase0 Q9], and a stamped letter is the product [R3.7]. A client who types "12 Shad Hill Rd, Ridgefield 06877" gives a Connecticut zip and no state. The file gets "No stamp", the screen says nothing, and P2's guard against an unstamped letter does not apply, because "no stamp" is a legitimate choice.

**Evidence.** Probe C11b, with both stamp images present: `state=NULL zip=06877 stamp=none; file screen warns about the missing state=no; letter sent=true; Doc has a stamp=false`.

**The fix.** With the state missing and a zip given, take the state from the zip (060–069 is Connecticut, 100–149 is New York). Otherwise leave the stamp undecided, say so on the file, and refuse to send until a person chooses. Test.

### 8. Linking a booking's client to an older one can overwrite a correction Peter made after the booking came in

**Where.** `app/Actions/MergeDuplicate.php:124-130` (an imported record's details count from its last job), together with `app/Actions/OpenFile.php:55-61` (a booking's rows are made through `importFrom`, so they count as imported; decision 4).

**What is wrong.** A booking's details are given when the client books. The merge instead dates them by the appointment, which may be weeks ahead. So a booking for six weeks out beats any correction made by hand in between. A person's correction is silently lost in a merge; the plan's rule is that merges are wrong only by a person's choice and that "nothing just typed is lost".

**Evidence.** Probe M1. An imported client. On Oct 1 a booking for Nov 15 with mobile 203-555-0199. On Oct 5 Peter corrects the old record's mobile to 203-555-0123. On Oct 6 he clicks "same". The kept record then reads `mobile phone after linking = 203-555-0199`.

**The fix.** Date a booking's details by when it was made: the booking row's `booked_at`, or its source's `imported_at`. Test M1.

### 9. An address typed or pasted with its state finds nothing

**Where.** `app/Search/FileSearch.php:51` (the property's state is not among the columns searched) and `:118-147` (every word must be found).

**What is wrong.** Peter will paste addresses from mail and booking forms, and those carry the state. R6.2 asks for search by property address.

**Evidence.** Probe S1:
- `"12 Shad Hill Rd, Ridgefield, CT 06877" => []`
- `"Shad Hill Rd Ridgefield CT" => []`
- `"Ridgefield, Connecticut" => []`
- `"7 N. Salem Rd, Cross River, NY" => []`

Meanwhile `"12 Shad Hill Rd"` finds the file, and the page says only "Nothing found. Try fewer words".

**The fix.** Look for a word in `properties.state` too. Read a state's name ("Connecticut", "Conn", "New York") as its code. Test with a pasted address.

### 10. Dates as Peter may type them: "5/22" finds nothing, "Smith 2022" finds the wrong job, a full date is read as another year

**Where.** `app/Search/FileSearch.php:173-216`. The patterns are at `:177-181`. A bare year counts only when nothing else is typed (`:209`, decision 24).

**What is wrong.** R6.2 asks for search by a time window. The month forms work, but these common ones do not, and one of them silently gives a wrong answer:
- "5/22" and "05/22" find nothing.
- "Smith 2022" treats 2022 as an address word. It finds a 2026 job at "2022 Main St" and misses Smith's May 2022 job.
- "Oct 14 2026" and "October 14, 2026" are read as October 2014, plus the word "2026". "10/14/2026" finds nothing.

**Evidence.** Probe S1:
- `"5/22" => []`
- `"Smith 2022" => ["Bea Smith-Jones"]` (her job is in 2026, at 2022 Main St; Cal Smith's May 2022 job is missed)
- `"Oct 14 2026" => words=["2026"] period=October 2014 => []`
- `"10/14/2026" => []`

**The fix.**
- Read m/yy as a month.
- In a full date, never take the day for a two-digit year.
- A four-digit year between 1980 and next year, typed with other words, limits to that year. Fall back to reading it as an address number if nothing is found.

Tests for each.

---

## Minor

### 11. A house number is found inside other numbers

**Where.** `app/Search/FileSearch.php:119`, which matches each word as a substring.

**Evidence.** Probe S4: `"12 Shad Hill Rd" finds: ["1203 Shad Hill Rd","212 Shad Hill Rd","112 Shad Hill Rd","12 Shad Hill Rd"]`.

**The fix.** Match a number as a whole word of the street.

### 12. The address reader mistakes a few shapes

**Where.** `app/Calendly/TypedAddress.php:107-130`.

**Evidence.** Probe C11:
- `"Ridgefield, CT"` gives `street='Ridgefield' city=NULL`.
- `"1 Elm St, Wilton, Conecticut 06897"` gives `line2='Wilton' city='Conecticut' state=NULL`.

The typed text is kept and shown on the file, so a person sees it.

**The fix.** A single word before a state is a town. An unknown last word before a zip, after a comma, is still the town.

### 13. "Leave them" writes no line anywhere

**Where.** `app/Actions/LeaveEarlierBookings.php:25-29`.

**What is wrong.** Deciding that some bookings will never get a file is a person's decision, and nothing records who made it or when.

**Evidence.** Probe H2: `rows left=1 history lines written=0`.

**The fix.** One Settings history line per decision, naming how many bookings and who decided.

### 14. With Calendly's notifications off, its test still shows a green "Working"

**Where.** `app/Actions/TestConnection.php:71-79`.

**Evidence.** Probe E4: `badge=Working; sentence says OFF=yes; trouble shown=no` until the next check raises it.

**The fix.** Treat notices that are off as trouble in the test as well.

### 15. The history in a few places a non-programmer will stumble on

**Where.** `app/History/FileHistory.php:166, 172, 179`.

**What is wrong.**
- A link between two records with the same name reads "Client: Ada Stone → changed to Ada Stone".
- A Calendly reschedule is told twice, once as "Date and time" and once as "Rescheduled in Calendly", with the same values.
- For P4: an imported 1995 job will read "File opened" on the day of the import.

**Evidence.** Probe H1, the panel as text.

**The fix.** Name the records ("the booking's record → the record on file since 2015"). Drop the plain date line when a Calendly line says the same. Have imported rows say "Brought in from WordPress (v3)".

### 16. Not demonstrated: what real Calendly and Google will do in two places

**Where.** `app/Actions/DeleteFile.php:39-41`; `app/Letters/GoogleLetterDocs.php:134-150`.

**What is wrong.**
- If the client cancelled in Calendly a moment before Peter deletes the file with the box ticked, the stand-in cancels again without complaint (probe C20: response 302, hidden). Real Calendly may refuse to cancel an event that is already cancelled. The delete would then say "Nothing was deleted: the appointment could not be cancelled", about a booking that is cancelled.
- "Untouched" rests on Drive's `revisions.list` (see finding 2).

Everything else in the real Calendly class matches the interface as I know it. The P3 log lists what cannot be proven until the account exists.

**The fix.** On a refusal, read the event again; if it is cancelled, go on and delete. Look at both on the first real account.

### 17. Important rules with no test

**Where.** `tests/`.

**What is wrong.** The suite is strong. P3 added 251 tests in 15 files, and they test rules both ways. These have nothing guarding them:
- a booking moved twice, in any order and by the check alone (finding 1);
- a Doc written in before a system write is never trashed (finding 2);
- bookings already in Calendly against imported jobs (finding 3);
- a reschedule of a file cancelled by hand (finding 4);
- the check not running, or throwing something other than `CalendlyUnavailable` (finding 5);
- the Connections badge after failures in use (finding 6);
- a booking with a zip and no state (finding 7);
- merge freshness of a booking's record (finding 8);
- search with a state, "5/22", a year with a name, a full date, a house number (findings 9, 10, 11);
- two processes hearing one booking. The suite proves "once" in one process only; I ran the race by hand (50 rounds, all clean);
- no P3 screen has been looked at in a browser. Those tests are P4's.

**The fix.** One test per item.

---

## The builder's decisions (33), against the import and the cutover

None of them stops the import of the 10,212 jobs:
- The two Calendly columns are unique but nullable, so imported files leave them empty.
- The search keys come from model events, which `importFrom` fires.
- Search stays fast at ten thousand jobs.
- The history writes a "created" line per imported row (finding 15).

One decision closes a door the cutover needs: decision 2 as built (finding 3).

| # | Decision | Verdict |
|---|---|---|
| 1 | Bookings off until a person switches them on | Sound; the cutover runbook needs it |
| 2 | Earlier bookings wait for a person's word | Right idea; all-or-nothing, with no "this is that file", closes the cutover door: finding 3 |
| 3 | One row per booking, keyed by the invitee | Sound; held in a real race. A chain of moves is not followed: finding 1 |
| 4 | A booking's rows marked as from Calendly, through `importFrom` | Workable. Side effect in merges: finding 8 |
| 5 | Values that fail the form's rules left empty; the typed text kept | Sound, except the state: finding 7 |
| 6 | Address from the first question naming "address" or "property" | Workable; Gordon's question 5 |
| 7 | One box: the last word is the surname | Workable ("Ada Stone Jr." gives "Jr."); Peter corrects in place |
| 8 | A visit unless Calendly's place is video or phone | Sound; matches Calendly's location types as I know them |
| 9 | Service matched by the appointment type's name | Sound; a renamed type waits visibly and is taken up on save |
| 10 | A late cancellation of a sent or closed file only noted | Sound; Gordon's question 1 |
| 11 | A reschedule of a closed or cancelled file keeps its date | Sound for closed; wrong for cancelled by hand: finding 4 |
| 12 | "Untouched" = still at the revision the system left | Sound idea, wrong bookkeeping: finding 2 |
| 13 | Doc back out of the trash when the file revives; a new copy if emptied | Sound |
| 14 | Delete asks Calendly first; nothing deleted if it cannot | Sound; one edge in finding 16 |
| 15 | A deleted file opens read-only | Sound |
| 16 | History keeps old values, folded shut | Sound |
| 17, 18 | Logins never removed; a new login mailed a link | Sound |
| 19 | Trouble raised once a day, clears by itself | Sound; the check itself unwatched: finding 5 |
| 20 | A notice taken up to 25 hours old | For the safety review |
| 21 | Our own signing key | Sound; Calendly takes a `signing_key` on the subscription |
| 22 | The check asks only about states it does not know | Sound: a quiet check is one request |
| 23 | Connections keeps observations only | Sound, but failures in use are not observed: finding 6 |
| 24 | Search: words AND month; a bare year only alone | Findings 9 and 10 |
| 25 | A linked record found under its old spelling | Sound |
| 26–33 | The second builder's (one WIP commit, invokable check controller, password link through the trap, opening a file as one act, booking page learned from Calendly, mistyped zip dropped, reason cut to 500, fixed test data) | Sound |

## Against the plan and the requirements

| Plan or requirement | Verdict |
|---|---|
| §5 "Each booking is acted on once, however many times Calendly reports it" | Met for one booking, by both roads, under a real race. Not for a booking moved twice: finding 1 |
| §5 "A booking creates the file, the client and the property (or links to existing ones, with the duplicate check)" | Met; nothing merged without a click |
| §5 "A reschedule moves the date" | Met for one move; not for two (finding 1), nor for a file cancelled by hand (finding 4) |
| §2 "an untouched Doc goes to Drive's trash, an edited one stays" | Met only when no system write came between: finding 2 |
| §2 and Q6, delete hides; "also cancel in Calendly" for an upcoming booking | Met |
| §5, the change history folded shut | Met; small readability points: finding 15 |
| §5 Settings and the Connections panel | Everything listed is present and saved with history; the badge is unreliable: finding 6 |
| §6.5, one hard cut | The bookings in flight at the cut are not handled: finding 3 |
| §10 "a failure lasting a day is alerted" | Met for the notices; not for the check itself: finding 5 |
| R1.4, a reschedule moves the date | As §5 above |
| R2.6, delete with double confirmation | Met |
| R6.2, search by client, address or time window | Met for names and Peter's month phrasing; gaps in findings 9 and 10 |
