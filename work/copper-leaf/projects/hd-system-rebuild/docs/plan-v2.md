---
name: Home Directions v4 plan, version 2
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: The plan for approval: what v4 is, every decision Gordon made on 2026-10-01 with its source, the data model shaped for the legacy merge, the cutover from v3 (history imported from WordPress, the last twelve months of letters moved into Google Docs, redirects), the build order with gates, backups, risks, and the short list still open; supersedes plan.md
sources: ["[doc:plan.md, the draft this replaces]", "[doc:phase0-brief.md, Decisions and Plan questions: every [gordon 2026-10-01] quote]", "[doc:requirements.md]", "[doc:census-2026-10-01.md]", "[doc:census-part2-2026-10-01.md]", "[doc:hosting-options.md]", "[doc:laravel-kit-spec.md]", "[rec_8d15ed467e 2026-09-29]"]
status: for Gordon's approval; written 2026-10-01 night by the planning thread; not independently reviewed; nothing is built; approval of this plan is the point at which real code starts, and Gordon is to be warned before that
---
# Home Directions v4: the plan (version 2)

Version 1 was a draft with fifteen open questions. All fifteen are answered, the stack and hosting are chosen, the data has been counted, and the order of work has been corrected: build and cut over first, the legacy audit second. This version says what will be built. Where it rests on Sancho's reading of an answer, it says so.

## 1. What v4 is

A small web app for one engineer. It hears Calendly, opens a **file** for each job with its **client** and **property**, creates a **Google Doc letter** from a template, makes and sends the **invoice**, records payment, sends the letter as a live link with a PDF copy, keeps a log of every message, and lets a name or address be corrected once and be right everywhere. Three screens: Dashboard, File, Settings. Three people use it: Peter, Maria Pia, Gordon. From its first day it holds the firm's whole client history as WordPress has it, and the last twelve months of letters as editable Google Docs.

## 2. Decided

| What | Decision | Source |
|---|---|---|
| Stack | Laravel 13, PHP 8.5, SQLite | [gordon 2026-10-01]; versions [doc:laravel-kit-spec.md D9] |
| Code style | Idiomatic Laravel; the WordPress Readability Rule does not apply | [gordon 2026-10-01] |
| Hosting | Laravel Forge on one DigitalOcean server Gordon owns; staging and production as two sites under separate users | [gordon 2026-10-01]; [doc:hosting-options.md, Decision] |
| Backups | Automatic, stored somewhere else; schedule in section 9 | [gordon 2026-10-01], his condition for one server |
| Google | The firm's existing Workspace (Business Starter; super admin office@homedirections.net) | [gordon 2026-10-01] |
| Mail | Sent as office@homedirections.net through Brevo, which is already set up on the domain | [gordon 2026-10-01]; [dns 2026-10-01] |
| Calendly | Paid plan; two appointment types (Professional Opinion, Structural Design); the booking form already requires the property address; instant notice plus a check every 15 minutes | [gordon 2026-10-01] |
| A Calendly cancellation | The file is marked cancelled and kept; an untouched Doc goes to Drive's trash, an edited one stays | [gordon 2026-10-01] |
| Deleting a file | Hidden and recoverable, never destroyed; for an upcoming Calendly booking the dialog offers to cancel it in Calendly too | [gordon 2026-10-01] |
| What the client receives | The live link and a PDF of the letter as sent | [gordon 2026-10-01] |
| Stamp | By the property's state for every job, virtual visits included: Connecticut, New York, none elsewhere; Peter can override | [gordon 2026-10-01] |
| Invoice numbers | Not a running count; the last three digits random and unique. Read as `HD-2610-482` (year, month, three random digits) | [gordon 2026-10-01]; format is Sancho's reading |
| Maria Pia Seirup | Her own login; she records payments | [confirmed gordon 2026-10-01] |
| Property facts | Address, year built (optional, may be removed later), notes | [gordon 2026-10-01] |
| Cutover | History imported from WordPress; every job of the last twelve months migrated with its letter as a Google Doc; v3 frozen | [gordon 2026-10-01] |
| Legacy audit | Phase 2, on its own thread, after cutover | [gordon 2026-10-01] |
| Harness | Plan, write the plan, then code, enforced; a model-and-effort check before coding; both kits compared perpetually; an updates schedule | [gordon 2026-10-01]; [doc:laravel-kit-spec.md] |
| GitHub | Copper Leaf organisation, Free plan, no upgrade | [gordon 2026-10-01] |
| Website clean-up | Already done; not part of this | [gordon 2026-10-01] |

## 3. The phases

- **Phase 0, decisions: done** with this plan's approval.
- **Phase 1: build, then cut over from v3.** Sections 4 to 10.
- **Phase 2: the legacy.** Audit v2's database and every backup, v1, the newest Access file and the Word files; reconstruct what the 2015 bug and the 2008 gap lost; attach a PDF to every old job; redirect every old link; retire v3 and v2. On a dedicated thread. [gordon 2026-10-01] Outline in section 12.

## 4. Data model

Shaped so that Phase 2 can load into it without changing it. The census found what the old data needs: a second person on a client, an inspector on a job, brokers and attorneys, the fee as charged, and the identifiers each record had in earlier systems. [doc:census-part2-2026-10-01.md]

```
users           Peter (owner), Maria Pia (treasurer), Gordon (admin)
clients         first and last name, second person's first and last name, display name,
                email, phones, mailing address, company, notes, merged_into
properties      address lines, city, state, zip, a normalised address key, a geocoded place key (nullable),
                year_built (nullable), notes, merged_into
files           the job: client, property, service (opinion | design | hourly), mode (site | virtual | design),
                scheduled_at, status (booked, visited, drafting, sent, paid, closed, cancelled), price,
                narrative, stamp (ct | ny | none), inspector, Calendly identifiers,
                letter doc id, hidden_at (the recoverable "delete")
file_contacts   other people on a job, each with a role (broker, attorney, additional), and whether they are copied
invoices        file, number, description, lines, subtotal, discount, total, issued_at, paid_at, paid_by, the PDF as sent
sends           every message: file, kind (invoice, paid copy, letter), to, subject, the service's message id,
                sent_at, delivered_at, opened_at, the PDF sent, the Doc revision sent
settings        the three invoice texts, the letter template ids, the from address, the stamp images, the Calendly type map
history         who changed what, from what, to what, when (the audit trail behind "fix it once")
sources         for every imported row: which system it came from (wordpress, v2, v1, access, word),
                its identifier there, when it was imported, and whether a person has verified it
old_links       an old web address, and what it should lead to now
```

Rules:
- **Nothing is destroyed.** Merges, cancellations and deletions are marks; the row stays. [doc:phase0-brief.md Q5, Q6]
- **Duplicates are suggested, never merged silently.** Clients match on email first (reliable from about 2010 on, when 94 percent have one), then on name with phone or address. Properties match on the geocoded key, then on the normalised address. A likely match shows on the file with one click to link or keep apart. [doc:census-part2-2026-10-01.md]
- **Every imported row knows where it came from**, so Phase 2 can replace a WordPress-sourced value with a better one from an older source and show that it did. Gordon: WordPress is "our only truth right now", to be improved "as we merge in the legacy data". [gordon 2026-10-01]
- The census's design load: two to three new jobs a week, about 10,000 historical jobs, about 40,000 records. SQLite is comfortable at that size. [doc:census-2026-10-01.md]

## 5. How the parts work

**Letters.** One Google Doc template per service, kept by Peter in Docs, carrying the letterhead and the address block. A new file copies the template, fills in the names, address and date, and names the Doc `Home-Directions-letter_YYYYMMDD_property-address_client-name`, for example `Home-Directions-letter_20261014_12-Shad-Hill-Rd-Ridgefield_Smith`. [gordon 2026-10-01, superseding R3.2] The filled-in places are tagged inside the Doc, so a corrected name or address is replaced exactly there and the Doc is renamed. [R2.3] The stamp image is placed by state (section 2). Peter and Maria Pia edit in Google Docs as long as they like. [R3.3]

**Sending a letter.** Sets the Doc to "anyone with the link can view", makes a PDF of it as it stands, and emails the client the link and the PDF. The system keeps that PDF and notes which revision was sent. Later edits show at the link; the PDF is the record of what was sent. [R3.5; Q7]

**Invoices.** Made when the file is created, from the service's text in Settings, editable on the file, with a stored total. Sent as a PDF. "Mark paid" records who and when and sends the client a paid copy. Resend is a button. [R4] Numbers per section 2.

**Mail.** Through Brevo, as office@homedirections.net, with a copy to that mailbox. Each message's delivered and opened reports are recorded against it: the closest honest thing to a return receipt. [R5; Q8]

**Calendly.** A booking creates the file, the client and the property (or links to existing ones, with the duplicate check). A cancellation marks the file cancelled. A reschedule moves the date. The system also asks Calendly every 15 minutes for anything it missed. Each booking is acted on once, however many times Calendly reports it. [R1; Q4, Q5]

**Hourly design work** is entered by hand; it does not come through Calendly. [R1.3]

**Screens.**
1. *Dashboard:* New File, a search box (client, address, month), recent files with their status and the next thing to do.
2. *File:* client and property, edited in place; "been here before" with links; the job's facts; the narrative; the invoice panel (preview, send, mark paid, resend); the letter panel (open the Doc, send); the message log; the change history; delete.
3. *Settings:* the three invoice texts, the letter templates, the from address, the stamp images, the Calendly type map, users.

**Google access.** The letters live in the firm's Workspace, in one folder shared with the Google accounts Peter and Maria Pia actually use. Which Workspace user owns the folder, and the exact kind of credential, are settled at the start of the build, with one fixed rule from the kit's review: staging uses a separate test Google account that owns nothing real, and the credential on production can reach only what the app needs. [doc:laravel-kit-spec.md 8.2] The draft's "act as any user in the Workspace" credential is dropped.

## 6. Cutover from v3

What Gordon set: the history comes in from WordPress, the last twelve months come across fully, Peter works in one place from day one. [gordon 2026-10-01]

1. **Import the history from WordPress** (rehearsed on staging against the clone, then run once against live at cutover). Clients, properties, job records and who was copied, for all 10,212 jobs. For the 9,442 that came from v2, read v2's own tables that sit inside the WordPress database, cross-checked against the WordPress records; for the 770 made in v3, read WordPress. [doc:census-part2-2026-10-01.md] Every row is recorded in `sources` as from WordPress and not verified. Counts are reconciled before and after: jobs by year and type must match the census tables.
   *Sancho's reading of "import all the historic client db": clients, properties and job records. If Gordon meant clients only, steps 1 and 3 shrink.*
2. **Migrate the last twelve months in full.** Every job dated in the twelve months before cutover (125 letters by the census, more by the time of cutover): the letter's text and images go into a copy of the new template as a Google Doc, named by the rule, filed with its job; its invoice comes across with its text, total and paid state. The census found these letters are paragraphs and images, with six tables and a few lists, so the conversion is plain; the tables are checked by eye. [doc:census-2026-10-01.md] **Gate: Peter opens ten of them and says they are right.**
3. **Old links for what moved.** Each migrated letter and invoice had a public address on v3. Those addresses are sent to the PDF made at migration, which is the letter as the client last saw it. While v3 is still up, the redirect lives on v3 (its Redirection plugin is already installed [doc:census-2026-10-01.md]); that is a change on the live WordPress site, done through the WordPress kit with Gordon's say.
4. **Freeze v3.** No new appointments there. It stays up, read-only in practice, for the documents of older jobs, whose links keep working exactly as now until Phase 2 replaces them.
5. **Go live.** Calendly is pointed at v4. **Gate: Peter runs one real job end to end.**

What cutover deliberately does not do: verify or repair the history (Phase 2), print PDFs of older documents (Phase 2), touch v2 (Phase 2).

## 7. Build order, with gates

Built in a separate thread, after this plan is approved, with the effort level raised. [gordon 2026-10-01] Every piece of work goes plan, written plan, code, review, ship. [doc:laravel-kit-spec.md 7.0]

| Step | What | Gate |
|---|---|---|
| A | **The kit, first slice:** the rules file, the guard for this host, the plan gate and the model-and-effort check, the gate script, the project template, the first three skills | each has its own tests; the guard's tests pass before any staging key exists |
| B | **The host:** Gordon creates the server and the two sites in Forge from the kit's checklist; backups running; a restore tested | the checklist, item by item; a restore that works |
| C | **Skeleton:** the app, the tables in section 4, logins for three people, Dashboard and File with entry by hand and the duplicate prompts | usable by hand on staging |
| D | **Letters:** templates, Doc creation, naming, correction of names and addresses inside the Doc | a corrected name changes in the system, in the Doc and in its name |
| E | **Invoices and mail:** numbers, texts in Settings, PDF, Brevo, send, mark paid, resend, the log | **Peter runs one real job on staging** |
| F | **Calendly:** bookings, cancellations, reschedules, the 15-minute check | a test booking and a test cancellation each do the right thing once |
| G | **Search, history, delete, Settings polish** | Peter and Maria Pia use it for a week on staging |
| H | **Import and migration rehearsal** (section 6, steps 1 and 2) on staging | counts reconcile; Peter approves ten letters |
| I | **Cutover** (section 6) | Peter runs one real job in production |
| J | **Four weeks of real use** | Peter says it is easier than before (R2.2); every message in the log is what he meant to send |

Step A is the pilot for the kit; the WordPress skills were revised after their first real job, and the same is expected here. The remaining kit pieces (the updates skill, the parity skill) follow once the app is live.

## 8. What Gordon does himself

Creates the Forge and DigitalOcean accounts, the server and the sites; installs keys; anything with a password. Approves each plan. Says "ship it". **Presses Deploy.** Starts a restore. Changes the model and effort level. The agent holds no Forge token, no production key and no production database credential. [doc:laravel-kit-spec.md 8.1, 13]

By Gordon's choice this app's remaining protections rest on instruction rather than on a wall: GitHub is on the Free plan, so nothing there can refuse a bad push; and GitHub may be signed in in the browser the agent drives. He will "tighten up the ship as needed" for more important systems. [gordon 2026-10-01]

## 9. Backups and upkeep

- **Every night**, and before any deploy that changes the database: the database and the stored PDFs, in one encrypted archive, to **two** places: Cloudflare storage and a folder in the firm's Google Drive. ("could we do both?? I love redundancy" [gordon 2026-10-01]) Kept as 14 daily, 8 weekly, 12 monthly, then one a year.
- **Daily:** DigitalOcean's backup of the whole machine (same datacenter, so not the off-site copy).
- **Every morning:** a check that last night's archive arrived; an alert to Gordon if not.
- **Every quarter, and once before go-live:** a restore onto staging, counts compared.
- **Monthly:** system updates, PHP patch releases and a reboot, from a checklist. **Yearly:** the Laravel upgrade (one a year is the floor, not one every two years as first stated) and the PHP version. [doc:hosting-options.md, Decision] [doc:laravel-kit-spec.md 9]
- The letters themselves are Google Docs and are not in the archive; each sent letter's PDF is.

## 10. Risks

- **The letter conversion looks wrong** (image sizes, tables). Rehearsed on staging; Peter's ten-letter gate; the original stays on v3 untouched.
- **The import carries WordPress's errors.** Expected and accepted: every row is marked unverified with its source, and Phase 2 corrects it. [gordon 2026-10-01]
- **Wrong merges of clients or properties.** Never automatic; one click to confirm; reversible through the history.
- **A correction replaces the wrong text in a Doc.** Only the tagged places are replaced; tested with a letter that mentions the client's name in its body.
- **A message goes to a real client from staging.** Staging mail goes to a trap; staging uses test accounts.
- **Calendly stops notifying.** The 15-minute check covers it; a failure lasting a day is alerted, because Calendly then switches its notifications off (secondary source; confirmed when built). [doc:hosting-options.md]
- **One machine.** A runaway job on staging can slow the live app; accepted by Gordon for a system one person uses occasionally.
- **Peter does not like it.** Three screens, one obvious next step per file, and two gates that are his real work, not a demonstration.
- **The kit delays the app.** Step A is a slice, not the whole kit.

## 11. Still open (none blocks approval)

1. Invoice number format `HD-2610-482`: confirmed. [gordon 2026-10-01]
2. Import scope: the whole history. [gordon 2026-10-01]
3. Off-site backups: both Cloudflare storage and Google Drive. [gordon 2026-10-01]
4. Mail test: does a message to office@homedirections.net reach `homedirectionsinc@gmail.com`, the one Gmail box Peter and Maria Pia use? [gordon 2026-10-01, correcting the address] Gmail stopped fetching other accounts in January 2026, so this is worth five minutes.
5. Brevo: confirm the account is the one in use (Gordon is "90% sure").
6. Which Workspace user owns the letters folder. Peter and Maria Pia probably both edit as `homedirectionsinc@gmail.com`. [gordon 2026-10-01]
7. Calendly's plan tier, confirmed against the account when it is connected.
8. Whether Forge is kept out of the browser the agent drives (Sancho's suggestion; unanswered).

## 12. Phase 2, in outline

On its own thread, later. What is already known for it: the sources are on this Mac and listed in `legacy-sources.md`; v2's database is `homedire_hdo_a2`, and backups of it from 2014 to 2021 include five live copies across 2015, the year of the bug; the newest Access file cannot be opened with the tool installed tonight and is probably in an older format; the 2008 gap runs from December 2007 to September 2008 and Gordon thinks that is when v1 replaced Access. Scope as he set it: the newest Access backup only; v1 gone through; v2 under a microscope; the Word files audited as they are attached to client records and turned into PDFs. Then a PDF for every old document, a redirect for every old link (R7.2), and v3 and v2 retired. [gordon 2026-10-01]

## 13. What happens next

Gordon reads this and approves it or changes it. On approval the next act is real code, and he has asked to be warned first: he raises the effort level and the build moves to its own thread, starting at step A with this document, `laravel-kit-spec.md` and `requirements.md` as its inputs. This planning thread stops there.
