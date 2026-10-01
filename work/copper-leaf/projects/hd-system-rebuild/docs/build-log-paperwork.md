---
name: Home Directions v4 build log, paperwork track
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: The paperwork track's own log for the overnight build of 2026-10-02: the plan for stage W1 (the four runbooks for Gordon's side), then what was written, which vendor pages were read, and every detail that had to be marked unconfirmed
sources: ["[doc:build-handoff.md]", "[doc:plan-v2.md]", "[doc:hosting-options.md]", "[doc:laravel-kit-spec.md]", "[doc:hosting-claims.md]", "[doc:phase0-brief.md]", "[doc:requirements.md]", "[doc:laravel-tooling-research.md]", "[gordon 2026-10-02]"]
status: stage W1 written 2026-10-02 00:55 to 01:08 by one agent of the paperwork track; reviewed by a second (reviews/paperwork-W1.md, 23 findings); fixed by a third, 01:25 to 01:40 (section "W1 fixes" at the foot); four runbooks on disk; 94 details marked unconfirmed after the fixes, plus two marked as Gordon's to decide; stage W2 (the how-tos) not started
---
# Build log: paperwork track

Model: Claude Fable 5.1 (`claude-fable-5-1`). The agent cannot see its own effort level. [doc:build-handoff.md section 3]

## Stage W1: plan (written before any runbook)

**What is written.** Four documents in this folder, and nothing else:
1. `runbook-accounts.md`: everything only Gordon can do before the app can go on a server, one section per service, in the order he should do them.
2. `runbook-backups.md`: how the backups are set up and how each is checked.
3. `runbook-cutover.md`: the one hard cut from v3, step by step, with the way back.
4. `runbook-dress-rehearsal.md`: every path through the system on staging, as a script with expected results.

**Read first.** `build-handoff.md` (all), `plan-v2.md` (all), `hosting-options.md` (Decision, the production boundary, what we still own), `laravel-kit-spec.md` (sections 2, 4, 5, 7, 8, 9, 13, 15), `hosting-claims.md` (the Laravel, server and Cloudflare storage claims), `phase0-brief.md` (Decisions and Plan questions 4 onward), `requirements.md`, the backup and Forge lines of `laravel-tooling-research.md`, and `/Users/gordonium/Sync/Sancho/CLAUDE.md`.

**Order of work.** Accounts first, because the other three lean on it. Then backups, cutover, dress rehearsal.

**Rules for the writing.**
- Every fact about a service, a price, a setting or a person carries its source. A document on disk, Gordon's words, or a vendor page read tonight.
- Where the documents do not settle a detail, the runbook says "unconfirmed: check on the vendor's page when you do this step". No guesses.
- A vendor documentation page may be read, text only, to confirm the current name of a setting. No sign-in, nothing created, nothing sent.
- Plain words, short sentences, numbered steps, conclusion first.
- No client data anywhere. No how-tos for Peter and Maria Pia (that is stage W2).

**How it is checked.** There is no automatic test for a runbook. The check is a read-through against the sources: each step traced to its citation, each "unconfirmed" counted and listed below, and a search of the four files for any claim with no bracket after it. The stage is then handed to a reviewer who did not write it.

**Limits.** Only these four files and this log are written. Nothing under `/Users/gordonium/Dev/` is touched. No `INDEX.md` or `MAP.md` is edited.

## Stage W1: what was written (finished 2026-10-02 01:08 CEST)

| File | What it holds | Lines marked "Unconfirmed:" |
|---|---|---|
| `runbook-accounts.md` | Nine services in order, each with what to create, the decided settings, where the key goes, and the line to tell Sancho | 38 |
| `runbook-backups.md` | The nightly archive to two places, the backup before a deploy, DigitalOcean's daily backup, the morning check, the retention, the restore test, and which copy to reach for | 16 |
| `runbook-cutover.md` | What must be true before the day, seven steps on the day with owner and check, the first four weeks, the way back | 17 |
| `runbook-dress-rehearsal.md` | Set-up, sixteen paths as do-and-expect tables, clean-up, the pass rule | 7 |
| **Total** | | **78** |

The count is of the literal marker `Unconfirmed:` in each file (`grep -o 'Unconfirmed:'`). A few say the same thing in two runbooks (going back a release in Forge; how Calendly's notices are switched on), so the number of distinct open details is about 70. Ten of the 78 carry the exact wording "check on the vendor's page when you do this step"; the rest are details that a vendor page cannot settle, because they wait on a decision of Gordon's or on a part of the app that was not built yet.

**How it was checked.** Each file was searched for lines with no source bracket, and every such line read again: what is left without a bracket is a heading, an instruction, a "Tell Sancho" line, or an "Unconfirmed" line. No em dash in any of the four (the CLC style rule). No client data: the only names are Gordon, Peter and Maria Pia, the firm's two mail addresses already in the plan, and invented test people. Section names cited from `plan.md`, `hosting-options.md`, `requirements.md` and `current-system.md` were checked against the files' own headings. No automatic test exists for a runbook; this stage is not "tested", it is read through, and it goes to a reviewer next.

**The app did not exist yet.** `/Users/gordonium/Dev/clc-laravel/` was empty when this stage read it (00:53). Nothing in the runbooks comes from the app's code. That is why no setting name for a key, no command name and no screen label is given as fact.

### Vendor pages read (text only, nothing signed in to, nothing created, nothing sent)

All on 2026-10-02, through the fetch tool. Forge's pages came back whole; the others came back as a summary by the tool's small model, so they are one reader's reading.

- laravel.com/forge/docs: `sites/deployments.md`, `ssh.md`, `sites/user-isolation.md`, `servers/the-basics.md`, `sites/the-basics.md`, `servers/types.md`, `server-providers.md`, `sites/repository-access.md`, `source-control.md`, `sites/network.md`, `sites/queues.md`, `sites/environment-variables.md`, `resources/scheduler.md`, `sites/domains.md`, `sites/commands.md`, and the index `llms.txt`.
- docs.digitalocean.com/products/backups/details/features/ and /pricing/.
- developers.cloudflare.com/r2/api/tokens/ and /r2/get-started/.
- spatie.be/docs/laravel-backup/v10/cleaning-up-old-backups/overview.
- developers.brevo.com/docs/transactional-webhooks and /docs/how-to-use-webhooks.
- calendly.com/help/webhooks-overview and developer.calendly.com/docs/authentication/how-to-authenticate-with-personal-access-tokens.md.

Could not be read: Brevo's help page on API keys (refused, HTTP 403); Brevo's developer start page (no dashboard steps on it); Calendly's developer pages on webhook signatures and retries (404 at the addresses tried). DigitalOcean's two backup pages do not state how many daily backups are kept. Each of these is an "Unconfirmed" in the runbooks.

### What the reading turned up that the planning documents do not have

These are the findings a reviewer and the orchestrating thread should look at first. Each is written into the runbook as "Unconfirmed", not resolved.

1. **Forge's Commands panel stops any command at five minutes and takes no typed input.** [web:laravel.com/forge/docs/sites/commands.md 2026-10-02] The import of the whole history and the conversion of some 438 letters must run on production, where the agent has no access. How Gordon starts them, and how the old data and the photographs reach the server, is not in any document. (`runbook-cutover.md` steps 2 to 4.)
2. **A zero-downtime site on Forge fetches the code with the GitHub connection's own token, over HTTPS, not with a deploy key**, by one passage of Forge's page; another passage says a site with a deploy key deploys with that. [web:laravel.com/forge/docs/sites/repository-access.md 2026-10-02] The kit spec's "each site gets its own read-only deploy key" may therefore not be what limits access; "Manage GitHub access" on the connection is. The spec's section 15 already lists the question. (`runbook-accounts.md` 4.2.)
3. **Cloudflare storage has no write-only key.** Its four permissions are Admin Read & Write, Admin Read only, Object Read & Write, Object Read only. [web:developers.cloudflare.com/r2/api/tokens/ 2026-10-02] The kit spec's "the backup credential on production can write to one folder and read nothing" (8.2) cannot be met as written, and thinning old archives needs list and delete anyway. (`runbook-accounts.md` step 5.)
4. **The backup tool's default deletes the oldest archives past 5,000 MB in total.** [web:spatie.be/docs/laravel-backup/v10/cleaning-up-old-backups/overview 2026-10-02] Left alone it would cut into "one a year, kept". For the app track. (`runbook-backups.md` section 5.)
5. **Calendly's instant notices need a paid plan** (Professional, Standard, Standard Plus, Teams, Teams Plus, Enterprise) **and are set up through its developer interface, not on a screen.** [web:calendly.com/help/webhooks-overview 2026-10-02] So the separate test account for staging either costs money or leaves the instant path unrehearsed; and the app itself has to create the subscription with the token. (`runbook-accounts.md` step 8; `runbook-dress-rehearsal.md` path 7.)
6. **DigitalOcean joins Forge by "Login with DigitalOcean"**, not by a pasted key. [web:laravel.com/forge/docs/server-providers.md 2026-10-02] One key fewer to handle.
7. **A password in front of staging (Forge's "security rule") covers the whole site or one path.** [web:laravel.com/forge/docs/sites/network.md 2026-10-02] On the whole site it would turn away Calendly's and Brevo's notices to staging.
8. **Two lines of the approved plan disagree with other lines.** Section 10 still says "Peter's ten-letter gate" where section 6 and the gate table say twenty letters, by Gordon. Section 7 step J has the agent reading the log after each early job in production, where section 8 and the kit spec say the agent holds nothing that reaches production. The runbooks follow section 6 on the first and mark the second for Gordon's decision.
9. **The plan lists the freeze of v3 after the import.** The import reads live once; the runbook puts the freeze first and marks the order as Sancho's reading.
10. **No document names the two web addresses.** Only the superseded draft names `app.homedirections.net`.

### Every detail marked unconfirmed, by runbook

**`runbook-accounts.md` (38).** GitHub: the app repository's name. Forge: whether an account exists; whether Hobby includes health checks and heartbeats. DigitalOcean: whether an account exists; how the form chooses no database; which New York datacenter; whether Forge's form offers the backups; whether a server password is shown. Sites: the two web addresses; which credential a zero-downtime site uses to fetch; whether `storage` is shared by default; how the repository's deploy script fits Forge's three lines; the queue worker's settings; which key of this Mac goes on staging; how staging's password and the incoming notices live together; whether the deploy hook works with push to deploy off; whether Forge's key list shows fingerprints. Cloudflare: whether the checkout asks for a card; bucket names and location; the write-only key that does not exist; account token or user token; where the archive password's second copy lives. Drive: the folder's name and owner; how the server writes to it. Brevo: where senders are listed; where keys are made; which kind of key; what staging uses; who sets up the delivered and opened notices and how they are verified. Calendly: how the app switches notices on and verifies them; whether the test account must be paid; the wording of the address question. Google: who owns the letters folder; shared drive or folder; whether link sharing is allowed; whether the built app's tags match the draft template; the kind of credential; what kind of account the test account is.

**`runbook-backups.md` (16).** The hour of the nightly run; how the server writes to Drive; whether the tool needs an extra program for SQLite; the size of one archive; what the backup command reports on failure; how many daily backups DigitalOcean keeps; what does the morning check; whether heartbeats are on the plan; how the alert reaches Gordon; how many years of yearly copies; whether both places follow one schedule; the restore steps; how the production archive and its password reach staging; how production's counts are read; where the result is written; how to go back a release in Forge.

**`runbook-cutover.md` (17).** How the two passwords are first set; the date; the order of freeze and import; whether "read-only in practice" is a switch; how the old data reaches production; how the photographs reach production; how the import is started (the five-minute limit); how the conversion is started and how long it takes; how many letters to open on the day; where each PDF is served and whether without a login; how the redirects are loaded into v3; how Calendly is switched on; whether anything else listens to the Calendly account; bookings already on the calendar; how the agent reads production's log; how to go back a release; what becomes of a job done in v3 on a bad day.

**`runbook-dress-rehearsal.md` (7).** The screens' real button and field names; what the copy to office@ does on staging; what each kind of login may do; how a booking is marked virtual or site; how an instant notice is held back for the 15-minute test; where a hidden file is restored from; how a test record is removed when delete only hides.

### Not done, and why

- **The names of the settings each key goes under in Forge.** The app was not built. The runbook says Sancho gives the names, never the values.
- **The steps for creating the Google credential.** The plan leaves the kind of credential to the build, and the build ran against a stand-in.
- **The commands that run the import, the letter conversion, the backup and the restore.** Not built when this was written.
- **How-tos for Peter and Maria Pia.** Stage W2, after the screens exist. [doc:build-handoff.md section 2 item 6]
- **Nothing was pushed, created, signed in to or sent.** No file outside this folder was written; `INDEX.md` was not touched.

### For the next stage (W2) and the reviewer

- `runbook-dress-rehearsal.md` is to be corrected against the real screens: labels, where restore lives, what each login may do.
- `runbook-accounts.md` needs the list of setting names from the app's example configuration once the app track has one.
- `runbook-cutover.md` steps 2 to 4 need the real command names and the way the old data travels, from stage P4.

## W1 fixes (2026-10-02, 01:25 to 01:40 CEST)

Fixer: Claude, model `claude-fable-5-1`. I cannot see my own effort level. I wrote neither the runbooks nor the review. [doc:build-handoff.md section 3]

**The conclusion first.** All 23 findings hold when checked against the documents. None was rejected. 21 are fixed outright. Two (7 and 11) are written to the safer reading and carry a question only Gordon can answer. Three more fixes rest on a reading Gordon may overrule (5, 8, 21). Only the four runbooks and this log were written. The review file, `plan-v2.md` and everything under `/Users/gordonium/Dev/` were left alone.

**How each finding was checked.** Each was read against the runbook lines it names and against the documents it cites, opened at the cited section. Three Forge pages, Laravel's configuration page and the standard for reserved domain names were read again for the facts the fixes lean on (list at the foot of this section). No automatic test exists for a runbook. This stage is not "tested"; it is read through, and it should go to a reviewer again.

**One thing the app's safety check refused.** I tried to read the setting names (names only, values stripped) of the app's `.env.example`, and to list the app repository's branches. The command was refused, with no reason given. By the handoff rule I did not work around it. [doc:build-handoff.md section 3, "If the app's safety check refuses a command"] What it cost: the runbook still says "Sancho gives the names" for the lines to clear and replace in each site's environment, and cites the review for what the example file holds. It also means I do not know which branch the overnight work sits on, which bears on finding 7.

### Per finding

| # | Weight | Verdict | What was done, or the question |
|---|---|---|---|
| 1 | blocker | **fixed** | The firm's Calendly token is no longer made or entered in the accounts runbook. Step 8 now says why, and sets up only the test account for staging. Production gets the token at `runbook-cutover.md` Step 7, item 1, and not before. Cutover Part 1 line 7 now requires Calendly **not** connected on production, and no file made from a booking. The step 8 "Tell Sancho" line says no token of the firm's is entered anywhere. The "way back" line takes the token out again. This is the review's option (a). Option (b), a switch in the app, is noted as put to the app track. |
| 2 | blocker | **fixed** | Accounts 4.4 item 3 now opens with the condition: both guards registered on this Mac and their tests passing, shown to Gordon by Sancho, before the key is added. [doc:plan-v2.md section 7, step A] [doc:laravel-kit-spec.md section 14, step 3] The same is in the step's "Tell Sancho" line and in "Not in this runbook". |
| 3 | should-fix | **fixed** | Checked at Forge's page: the example file is copied at site creation. [web:laravel.com/forge/docs/sites/environment-variables.md 2026-10-02] Accounts 4.2 now opens with a question to Sancho before any site is made (is the example file free of seed passwords?) and the rule in bold: no seed login password may reach a server; no plain yes, no site. 4.3 item 5 tells Gordon what to clear or replace: any seed password, the app's mode, the error display, the app key, the site's address, and the stand-in lines. Names come from Sancho, because my read of the file was refused. |
| 4 | should-fix | **fixed** | The trap is now a step with an owner (accounts 4.4 item 2). Rehearsal line S5 proves it with an address that is not Gordon's and can never receive mail (`.invalid`). [web:rfc-editor.org/rfc/rfc2606.txt 2026-10-02] It is run again as line 16.1, before any real record is opened. Whether the built app has the setting is marked unconfirmed and owed by the app track. |
| 5 | should-fix | **fixed; a choice remains with Gordon** | Accounts step 7 item 6 now states the constraint: staging's Brevo key must come from an account that cannot send as the firm, or Gordon signs an exception by name and date. Question for Gordon: a separate free Brevo account for staging (Sancho's suggestion), or a signed exception? |
| 6 | should-fix | **fixed** | Two rules, in accounts step 5 item 8, in the 4.4 rules, and in backups section 6: staging has its own archive password; production's is never entered on staging and never given to the agent. For the quarterly test Gordon opens the archive himself. The mechanism stays unconfirmed. |
| 7 | should-fix | **written to the safer reading; left for Gordon** | The citation was wrong: D2 says `main` moves only at ship. Accounts step 1 now pushes the kit, the app's working branch and `staging`, and not `main`; the "Tell Sancho" line names that. The production site is made in a new step 13, after the first ship. Question for Gordon: is the first `main` (a) nothing until the first ship, with the production site made after it, as the runbook now reads, or (b) one bare first commit pushed as a named exception, so both sites can be made in one sitting? |
| 8 | should-fix | **fixed; Sancho's reading, Gordon may overrule** | Backups section 6 now has two kinds of test. 6.1, before go-live: staging's own archive, taken after the import rehearsal, restored onto staging. 6.2, quarterly: production's archive. In the rehearsal the restore is the new Path 18, last, with the state staging is left in. Path 15 keeps only the archive line. |
| 9 | should-fix | **fixed** | The clean-up has new lines C4 to C7, each with an owner and a check: the imported history, the converted letters and the trash, the photograph files and old-data copy, and the archives of staging made while it held real history. S4 is amended. Deleting is Gordon's, or approved by him by name. |
| 10 | should-fix | **fixed; plan contradiction listed below** | Path 16 now opens a consultation from before 2022-06-21 (no Doc), and jobs from the second half of 2022, from 2023 or 2024, and from the last year (each with a Doc). The Doc line cites the 2026-10-02 decision. |
| 11 | should-fix | **part fixed; part left for Gordon** | Fixed: cutover Step 6 now has Gordon take the list out of production, by a button or command that is owed by the app track; the list holds addresses only. Question for Gordon: old invoice links of migrated jobs. (a) an invoice PDF is made at migration and the link goes to it, or (b) they are left on v3? The runbook takes (b) until he says, and never points an invoice link at a letter. |
| 12 | should-fix | **fixed** | Cutover Steps 3 and 4 each have a second check: no message in the app's record since the day began, none in Brevo's sent list, and (Step 4) no converted Doc shared by link. The same three are rehearsal lines 16.2 to 16.4. How the counts are read is unconfirmed and owed by the app track. |
| 13 | should-fix | **fixed** | New rehearsal Path 17: going back a release (17.1), a failed backup stopping a deploy (17.2), the morning alert (17.3, 17.4), the one-day Calendly alert (17.5). Backups sections 2 and 4 and cutover Part 4 point at it. |
| 14 | should-fix | **fixed** | The accounts runbook is now three passes. Pass one, steps 1 to 9. Pass two: step 10, the first deploy on staging; step 11, the Google credential as its own numbered step; step 12, the app's Settings on staging. Pass three: step 13, production. Every "Tell Sancho" line can now be said when its step ends. Cutover Part 1 line 1 names steps 11 and 13. |
| 15 | should-fix | **fixed** | The certificate step moved to after the site exists (4.3 item 3). Both sites are created with push to deploy off; staging's is switched on as the last line of 4.4. Checked at Forge's page. [web:laravel.com/forge/docs/sites/deployments.md 2026-10-02] |
| 16 | minor | **fixed** | Cutover Part 4 has a new row 6 and a sentence under the table. |
| 17 | minor | **fixed in the parts touched** | Section 4: rules are now short "Rules for staging" and "Rules for production" lists, steps begin with a verb, storage is a plain step, and open questions that need nothing from Gordon sit in "Sancho settles these" lists (also in steps 7 and 8). One plain clause was added for: queue worker, zero-downtime deployments, commit ID, fingerprint, endpoint, region, custom domain, DNS check, shared path, environment. The two commands in the opening section are now described in words. Sections 2, 3, 6 and 9 were not restyled. |
| 18 | minor | **fixed** | Line 6.6 now cites the plan's list of message kinds and is marked Sancho's reading. The $475 row cites requirements for the price and the plan only for "entered by hand". |
| 19 | minor | **fixed** | All three markers replaced by the settled statement and its source: one retention for both places; `storage` is a shared path Gordon adds (now 4.3 item 2); a test record leaves staging by a committed command or a database started again, never a hand edit. Which of those two is still open and is owed by the app track. |
| 20 | minor | **fixed; one part owed** | (1) Cutover Part 1 line 12: the how-tos. (2) Accounts 9.2 names the four image files and where each is. [doc:current-system.md] [doc:survey-hdonline-home-directions.md] (3) The monthly upkeep checklist is listed as owed under "Not in this runbook"; it is not written. |
| 21 | minor | **fixed by noting; a choice remains** | Backups section 2 now states the difference between the plan and the kit spec, and Forge's ten-minute limit. The runbook still follows the plan. Question for Gordon and the app track: before a deploy, the whole archive (plan) or the database only (kit spec)? |
| 22 | minor | **fixed** | The sentence is gone from accounts step 3. Backups section 1 now says the hour and its clock are both unconfirmed and are written once when chosen. |
| 23 | minor | **fixed** | Four test people with four plus-tagged addresses (T4 added for line 3.5); 9.10 reads "three messages for this file"; 11.3 searches the month the test bookings fall in. |

No finding was judged "not a real problem".

### Questions left for Gordon, in order

1. **The first `main`** (finding 7). Nothing on GitHub as `main` until the first ship, and the production site made after it (as written)? Or one bare first commit as a named exception, so both sites are made together?
2. **Old invoice links** (finding 11). Make an invoice PDF at migration and redirect the old link to it, or leave old invoice links on v3 (as written)?
3. **Staging's mail account** (finding 5). A separate free Brevo account for staging, or a signed exception for a second key on the firm's account?
4. **The restore test before go-live** (finding 8). Is staging's own archive, taken after the import rehearsal, the right one? The documents do not say whose archive.
5. **The backup before a deploy** (finding 21). The whole archive, as the plan says, or the database only, as the kit spec says?

### Where the plan contradicts itself or another approved document

`plan-v2.md` was not changed. The runbooks follow the reading named here.

1. **Which letters move.** The plan says "the last twelve months" in four places (its description, section 1, the section 2 table, the opening of section 6) and "every letter since the last inspection" in section 6 step 2, which records the later decision. [doc:plan-v2.md lines 7, 17, 37, 107, 111] Followed: section 6 step 2.
2. **When production first exists.** The plan's step B has Gordon create both sites before the app is built. [doc:plan-v2.md section 7] The kit spec says `main`, production's branch, moves only at ship. [doc:laravel-kit-spec.md D2] A site cannot be made without its branch. Followed: the spec; production waits for the first ship. Question 1 above.
3. **What an old invoice link shows.** The plan sends the old address of "each migrated letter and invoice" to one PDF, "which is the letter". [doc:plan-v2.md section 6 step 3] Followed: invoice links left alone. Question 2 above.
4. **What is backed up before a deploy.** Plan and hosting decision: the whole archive. Kit spec: the database. [doc:plan-v2.md section 9] [doc:hosting-options.md Decision] [doc:laravel-kit-spec.md section 7, laravel-ship] Followed: the plan. Question 5 above.
5. **When Calendly is connected.** The plan has Gordon enter every key in Forge as part of setting up, and has Calendly "pointed at v4" only at go-live. [doc:plan-v2.md section 5, "Keys and passwords", and section 6 step 5] It does not say the production token waits. Followed: it waits.
6. Still standing from the first log: "Peter's ten-letter gate" against twenty letters by Gordon; and step J against section 8 on who reads production's log.

### Owed by the other tracks because of these fixes

For the app track:
- The example settings file must hold no seed password and nothing that is only right on this Mac. Forge copies it onto each server. (Already carried into the P1 review. [doc:build-state.md])
- A mail-trap setting for staging, with a test, if it does not exist.
- The 15-minute Calendly check must do nothing, quietly, while no token is set; and it must be clear what happens to a booking that arrives before the type map is set, and whether the type map can be set with no token in.
- The import and the conversion must send nothing and share no Doc, with a test that says so; and two counts Gordon can read on production: messages since a given time, and Docs shared by link.
- A way for Gordon to take the old-links list out of production.
- A way to start staging's database again, or a committed clean-up command.
- How the first login is made on a server, since the seeder refuses to run there.
- The review's option (b) for finding 1: a switch "take bookings from Calendly", off by default. Not in the plan; needs Gordon's yes.

For the kit track:
- The first ship happens before any production site exists. The ship script reads production's version line; on the first ship there is none to read.
- The monthly upkeep checklist the plan calls for is not written.
- The start-of-job check's line "both hooks registered and their tests passing" is what Gordon is shown before the staging key goes on.

### Path and line numbers that moved

- `runbook-dress-rehearsal.md`: Path 15 is now only the backup (15.1). Old line 15.2 is Path 18. Path 16 was renumbered: old 16.1 is 16.5 (and now asks for a consultation from before 2022-06-21), old 16.2 and 16.3 are 16.9 and 16.7, old 16.4 to 16.6 are 16.10 to 16.12. Path 17 and Path 18 are new. Clean-up C4 (write the results) is now C9.
- `runbook-accounts.md`: 4.1 item 3 is 4.3 item 3. Old 4.3 items 2 to 7 are 4.3 items 2, 4, 5, 6, 7, 8. Old 4.4 item 1 is 4.4 item 3. Old 8 items 5 and 7 and old 9.2 item 8 are step 12. Old 9.3 is step 11. "When all nine are done" is "When the thirteen are done".
- One slip fixed that no finding named: cutover Part 1 line 11 pointed at "Part 2, step 5" for the redirects; they are step 6.

### Markers after the fixes

Literal `Unconfirmed:` markers (`grep -o 'Unconfirmed:'`): accounts 38, backups 16, cutover 24, dress rehearsal 16; 94 in all, against 78 before. Two more read "Unconfirmed, and yours to decide" (accounts step 1, cutover Step 4). Three old markers were settled (finding 19). The new ones come from the checks and paths the review asked for: most wait on a part of the app that is not built. 17 of the 94 carry the exact wording "check on the vendor's page when you do this step". No em dash in any of the four files. No client data: the only names are Gordon, Peter and Maria Pia, the firm's mail addresses already in the plan, and invented test people.

### Vendor pages read by the fixer (text only, nothing signed in to, nothing created, nothing sent)

All on 2026-10-02, through the fetch tool. The three Forge pages and Laravel's page came back whole; the standard came back as a summary.
- laravel.com/forge/docs/sites/environment-variables.md: the example file is copied at site creation; the two follow-up actions after a change.
- laravel.com/forge/docs/sites/deployments.md: push to deploy on by default and where it is switched; only the environment file is shared by default; the ten-minute limit; four releases kept.
- laravel.com/forge/docs/sites/the-basics.md: a site made without a repository cannot be given one later; packages can be installed right after creation; the on-forge.com address is live as soon as a site exists.
- laravel.com/docs/13.x/configuration: the app's mode comes from one line; error display should always be off in production.
- rfc-editor.org/rfc/rfc2606.txt: names ending in `.invalid` are reserved as sure to be invalid.

### Not done, and why

- **The exact names of the lines to clear and replace in each site's environment.** The read of the example file was refused. The runbook says what each line is for and that Sancho gives the name.
- **Sections 2, 3, 6 and 9 of the accounts runbook were not restyled for the ear** beyond the words finding 17 named. They were not found wrong.
- **The monthly upkeep checklist** (finding 20, part 3). Owed by stage W2 or the kit track.
- **No second review.** The four runbooks changed a good deal in structure. They should be read again by an agent that did not fix them.
