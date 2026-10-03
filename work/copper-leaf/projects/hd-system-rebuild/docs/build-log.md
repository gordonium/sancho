---
name: Home Directions v4 build log, summary
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: The one-minute summary of the build for Gordon: what works now, how to see it on this Mac, what it is not yet, what it cost, and what comes next; the detail is in build-log-app.md, build-log-kit.md, build-log-paperwork.md, build-state.md and the reviews folder
sources: ["[doc:build-state.md]", "[doc:build-log-app.md]", "[doc:build-log-kit.md]", "[doc:build-log-paperwork.md]", "[doc:reviews/app-W3-walkthrough.md]"]
status: written 2026-10-03 02:15 by the orchestrating thread, after the morning version was finished
---
# Build summary: read this first

**A working version is on your Mac, with your real history in it.** It works when used as it should be: every everyday path was run in a real browser, and every one of the 10,206 imported jobs opens without an error.

## See it
1. Open **http://hdonline-v4.test** in a browser on this Mac.
2. Log in as `peter@hdonline-v4.test`, `mariapia@hdonline-v4.test` or `gordon@hdonline-v4.test`. The passwords are in the app folder: `/Users/gordonium/Dev/clc-laravel/hdonline-v4/storage/app/private/local-logins.txt`.
3. Try what Peter does: find a client by name, a street, or a month ("May 2022"); open a job; New File; write the invoice description; make the letter; send the invoice; mark paid; open the change history at the foot of a file.

If the address gives no answer, Herd's web server is down: open Herd and restart its services.

## What works, checked
- **Your history:** 10,206 jobs, 8,693 clients, 9,112 properties, 10,206 invoices (9,559 paid), imported from the dev clone's database. Jobs by year match the census in 38 of 44 years; the other six are off by one or two, explained in the log. Three test records and six others in the trash or dated in the future were skipped, listed by ID.
- **Every screen on the real data:** an Opus checker made about 11,000 requests: every imported job's screen, the whole Dashboard scroll, 199 searches. No crashes, no errors from the app's code, nothing slower than 40 ms.
- **Every everyday path** in a real browser (21 browser tests), and 1,387 tests in all, passing; formatting and static analysis clean.
- **Peter's CT and NY stamps** are loaded from the old plugin, so letters carry the right stamp.

## What it is not yet
- **On this Mac only.** No server exists yet.
- **No real outside services:** letters go to a stand-in instead of Google Docs, mail is logged instead of sent, Calendly is a stand-in. Connecting them is your account checklist: `docs/runbook-accounts.md`.
- **Old letters are not converted yet** into Google Docs.
- **Known gaps before go-live:** four serious findings from the reviews, all edge cases (a booking rescheduled twice opens a second file; a Doc Peter wrote in can go to the trash after a cancellation; at cutover nothing ties a Calendly booking to its imported job; any login can quietly take over another). Details: `reviews/app-P3-plan-fit.md`, `reviews/app-P3-safety.md`.

## What it cost
- **Last night, the morning version (00:49 to 02:10):** $21.26 of usage credits, Fable at high effort with a cap on every stage: the real history $5.74, the browser paths $8.03, the fixes $5.72, test calls $1.77. The walkthrough ran on Opus inside your plan.
- **The evening before (18:42 to 20:27):** $98.48, Fable at max effort, three stages at once.
- This month so far: $172.92 of the $300 limit.
- So high effort with per-stage caps cost about $6 to $8 a stage, against about $30 an hour at max. Sancho's estimate for the rest of the local build (the four review blockers, the old-letter conversion, backups, laying the kit over the app): six to eight such stages, roughly $40 to $70. An estimate, not a quote.

## What Sancho needs from you, in order
1. **Look at it**, and say what is wrong or missing.
2. **Your note to Anthropic** is drafted, not sent: `docs/draft-note-to-anthropic-2026-10-03.md`.
3. **Say go on the rest** (the list above), or wait for the weekly Fable reset (Sunday 01:00) to run it inside your plan.
4. **The questions** that shape Peter's screens: `docs/questions-for-gordon.md` (from the build's agents) and the fifteen earlier ones in `docs/build-state.md`.
5. **The account checklist** when you are ready for a server: `docs/runbook-accounts.md`.

Do not switch on the kit's hooks yet: once on, they refuse changes to a project without an approved plan, and the build still has work to do in the app.

## Where the detail is
- `build-log-app.md`: every app stage, P1 to W4. `build-log-kit.md`: the kit. `build-log-paperwork.md`: the runbooks.
- `build-state.md`: what ran when, every usage reading, every decision of yours with your words.
- `reviews/`: every review, with its findings and what was fixed.
