---
name: Laravel kit spec
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: Spec for a Laravel development kit built to the standard of the Copper Leaf WordPress plugin kit (rules, skills, guard, backup, handoff), plus the updates schedule for every Laravel project and the mechanism that keeps the two kits compared; what carries over, what changes, what the Laravel kit adds, what the WordPress kit should take back; decisions for Gordon; build order for the Nerd
sources: ["[gordon 2026-10-01]", "[doc:wp-kit-map.md]", "[doc:~/Dev/clc-plugins/CLAUDE.md]", "[doc:~/Dev/clc-plugins/skills/]", "[doc:~/Dev/clc-plugins/bin/]", "[doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md]", "[doc:hosting-options.md]", "[doc:hosting-claims.md]", "[doc:laravel-tooling-research.md]", "[doc:guard-check-2026-10-01.md]", "[sancho subagent review 2026-10-01, workflow wf_4aaefbba-f62: five independent readers, 113 findings on draft 1]"]
status: draft 2 (D1 decided 2026-10-01: the Readability Rule is WordPress-only; hosting decided: Forge, one server), revised after an independent review of draft 1 (4 blockers, 59 major, 50 minor findings across this and three other documents; what was changed is listed in section 16); nothing is built; hosting is Sancho's pick, not yet Gordon's decision; lives here until the kit has a home of its own
---
# Laravel kit: spec (draft 2)

Gordon, 2026-10-01: "let's start building a similar skill harness for Laravel and perpetually compare the two to cross-apply improvements and lessons." And: "we just need to build an updates schedule for this and all future Laravel projects, I expect there will be more." [gordon 2026-10-01]

Sancho plans; the Nerd builds; nothing below exists yet. The WordPress kit was read line by line first (465 cited items in `wp-kit-map.md`), so this is a mapping, not a fresh invention. Draft 1 was then given to five independent readers who were asked to break it. They did, in the production boundary above all. This draft is the repaired version, and it marks plainly which protections are mechanical and which rest on instruction.

Sections 7 and 8 are written for Laravel Forge. **Decided 2026-10-01: Forge, and for this first app one server, with staging and production as two sites under separate users, on condition of automatic off-site backups.** [gordon 2026-10-01] [doc:hosting-options.md, Decision] Sections 7 and 8 below were written for two servers and are to be read with that change: wherever they say "separate servers" or "the staging key opens staging only", the boundary for this app is the per-site user on one machine, the Mac's key is installed for the staging site's user only, and the new-project checklist tests that the staging user cannot read production's folder. Two servers remain the kit's default for "more robust client systems in the future". [gordon 2026-10-01]

## 1. The shape

A second kit beside the first: its own parent folder so the WordPress rules do not load for Laravel repos; a rules file with the same twelve sections; skills that chain the same way (edit, review, ship) plus three more (new project, updates, parity); a guard; the same hourly backup; one handoff document. Three things differ in kind:

1. **Laravel has automatic tests, so gates can be checked by a script.** The WordPress kit has no test gate anywhere; testing is a hand-written matrix on staging. [doc:wp-kit-map.md, skills weaknesses]
2. **Pushing can ship.** The WordPress release gate rests on "Pushing commits or tags does NOT ship." [CLAUDE.md:136] On Forge, deploy-on-push is the default for a new site. [web:laravel.com/forge/docs/sites/deployments] The Laravel kit rebuilds the gate so that Claude pushes and Gordon's own action ships.
3. **Software under it expires.** Security fixes end two years after a Laravel major's release and four years after a PHP release. [web:laravel.com/docs/releases] [web:php.net/supported-versions.php] The WordPress kit has no rule about keeping anything current. [doc:wp-kit-map.md, rules weaknesses]

## 2. Decisions for Gordon

Three shape everything else. The rest have a pick that stands unless he objects.

### The three

**D1. The Readability Rule in Laravel. DECIDED 2026-10-01: it does not apply.** Gordon: "those rules should apply to WP only. Let's go whole-hog elegant inside Laravel, as I never intend to read the code. That's all you, boo." [gordon 2026-10-01] So Laravel code is written the way good Laravel is written: idiomatic, concise, the framework's own conventions, with comments where a reader who knows Laravel would want one. The WordPress kit's rule ("the most important style rule" there [CLAUDE.md:67-76]) stays in the WordPress kit, where Gordon and Leah do read the code. What follows from the decision:
- No readability check script, and no sixth "readability" reviewer (D11).
- The standard is mechanical where it can be: the formatter (Pint), the analyser (Larastan), the tests, the architecture tests.
- Plain language still governs everything Gordon reads: plans, hand-overs, the change log, the per-project file. That rule is about him, not about the code.
- In the parity ledger this is a recorded difference between the kits, with its reason, not a gap.
(Draft 2 proposed keeping the rule for our own logic with a list of allowed framework shapes and a token-based check; superseded by this decision.)

**D2. The release gate: `main` is production's branch, and nothing reaches it unattended.**
*Pick:*
- All work happens on a branch (`feature/<name>`, or `updates/<date>` for dependency updates).
- A third branch, `staging`, is only a pointer: the agent moves it to the branch under test, and the staging site deploys it.
- `main` moves only at ship, by one kit script, to the exact commit that was gated, reviewed and run on staging. The production site has deploy-on-push off. **Gordon presses Deploy.**
- Dependency updates are no exception. The update bot opens pull requests; nothing merges by itself; the updates go through the same chain in an update session.
This replaces draft 1, in which the agent pushed `main` before review and updates merged into it unattended. Two readers showed that a ship would then carry commits no reviewer was pointed at. It also retires the WordPress rule "quick-turn fixes commit directly on `master`" [CLAUDE.md:139] for Laravel: that rule is safe only where a push to the default branch cannot be what production deploys.

**D3. A browser the agent cannot use for the hosting panel. DECIDED 2026-10-01: yes.** Gordon: "Yes, either a separate chrome profile or even a separate browser." [gordon 2026-10-01] As proposed: The kit's sessions drive Gordon's real, signed-in Chrome. [plugin-edit:94] If Forge, DigitalOcean or GitHub is signed in there, the agent is one click from Deploy, from switching deploy-on-push back on, or from adding a key to production, with no token and no shell command. The guard is a hook on shell commands and never sees it. [config/claude-settings-hooks.json:5]
*Pick:* Forge, DigitalOcean and GitHub's settings are signed in only in a browser profile that does not have the Claude extension. A second hook on the browser tools refuses those sites by address, as a net under that. Until both exist, "Gordon presses Deploy" rests on instruction, and this spec says so wherever it matters.

### The rest

**D4. Home and name. Owner DECIDED 2026-10-01: Copper Leaf.** "Copper Leaf. Free plan" [gordon 2026-10-01], that is the `CopperLeafCreative` organisation, beside the plugin kit. Parent folder `~/Dev/clc-laravel/`, the kit's files at its top level, each app cloned beneath it, as `~/Dev/clc-plugins/` works. [HANDOFF §3, §17.2] A Laravel repo must never be cloned under `~/Dev/clc-plugins/`. Kit repo `clc-laravel-dev-kit`, private (name is Sancho's suggestion).

**D5. A paid GitHub plan for the organisation. OPEN.** The organisation is on the Free plan. [gordon 2026-10-01] On Free, a private repository cannot have a protected branch. [web:docs.github.com/en/get-started/learning-about-github/githubs-plans] So today nothing at GitHub can refuse a force-push to `main`, a deletion, or a commit whose checks are not green; that part of the release gate rests on the ship script and on Gordon comparing the commit before he presses Deploy (section 8.1). The Team plan would make GitHub itself refuse. Price: **$4 per user per month**. That is what GitHub's pricing page displays (read in a browser 2026-10-01), and it has been the Team price since GitHub cut it from $9 on 2020-04-14. [web:github.com/pricing] [web:github.blog/news-insights/product-news/github-is-now-free-for-teams/] (An earlier reading, "$4 ... for the first 12 months", came from a hidden block in the page's markup for yearly billing, not shown to a visitor and with no footnote on the page; what yearly billing does after a year is therefore unconfirmed, and monthly billing avoids the question.) Team also brings 3,000 Actions minutes a month against 2,000. [web:docs.github.com/en/get-started/learning-about-github/githubs-plans] **Seats today: 3 members (`copperleaf`, `copperleah`, `marvelous-maezel`) and 1 outside collaborator (`carmynwilson`); no pending invitations.** [github:orgs/CopperLeafCreative/people, read 2026-10-01 at Gordon's request in his signed-in Chrome] So $12 a month for the members; whether the outside collaborator is billed as a fourth seat depends on whether they have access to a private repository (GitHub bills those; not checked), making it $12 or $16. *Pick: upgrade.* It would serve the plugin repositories too.

**D6. Update bot.** GitHub Dependabot, opening pull requests only. Renovate only if grouping proves too coarse.

**D7. The yearly Laravel upgrade.** Laravel Boost's upgrade prompt first (first-party, free), a Laravel Shift run ($19) as the cross-check on the first app, then decide which to keep.

**D8. Laravel Boost otherwise.** Boost is Laravel's own kit for AI agents: version-matched guidelines, a documentation search limited to the installed versions, and tools that read the app (routes, schema, logs, last error). [doc:laravel-tooling-research.md] *Pick, changed after D1: install it, as a development-only package.* Draft 2 kept it out because its vendor guidelines would have fought the Readability Rule; with idiomatic Laravel now the goal, its guidelines are an asset, and its documentation search matters because Laravel 13 is newer than much of what an agent knows by heart. Three conditions: its database tool is treated as able to write until checked, so the local `.env` never points at anything but a local database; its own rule store is switched off so rules live in one place; and its generated text is reference, never rules, where it differs from the kit.

**D9. Versions for a project started now.** Laravel 13, **PHP 8.5** (8.4 leaves active support 2026-12-31), **Pest 5** (what the installer resolves on PHP 8.5; one reader read this in the installer's source), Larastan 3, Pint 1, Composer 2.10, Node 24 until Node 26 has been LTS for sixty days. Supersedes "PHP 8.4" in `phase0-brief.md`.

**D10. One guard for both kits.** One shared core that reads a small rules file per host, built in the Laravel kit first; the WordPress guard moves onto it later, with Gordon's say. [HANDOFF §17.5] With two guards, a hole fixed in one stays open in the other; eight are open in the WordPress guard today (section 11).

**D11. How many reviewers.** The WordPress chain runs three, every time, about 210k tokens. [HANDOFF:88] *Pick: five* (the three, plus tests, and deploy readiness), every time, with the same small-fix exception. Under double the cost per ship. Fallback: four. (Was six; the readability reviewer went with D1.)

**D12. Continuous integration.** GitHub Actions running the gate on pushes to `feature/**`, `updates/**`, `staging` and `main`, on pull requests, and nightly on `main`. Never on the hourly `wip/**` snapshots. It holds no secret of any kind.

**D13. Monitoring at the start.** Laravel's `/up` route, a version line the app serves, and the host's own post-deploy health check reporting to Gordon (whether Forge's cheapest plan includes it is unconfirmed). *Not* Laravel Nightwatch yet: its connector can change issue status, has no read-only mode, and brings production request data into the agent's session. [doc:laravel-tooling-research.md]

**D14. Who looks at production after a deploy.** The WordPress kit lets Claude view production pages read-only through the signed-in Chrome. [CLAUDE.md:102] [plugin-ship:65] In this app a signed-in production session is one click from sending a real client a real invoice. *Pick: the agent checks two addresses that need no login (`/up` and the version line); Gordon looks at the pages, from a short list the agent prepares.* Later option: a login in the app that can view and cannot act.

**D15. Where assets are built.** On the server, by the deploy script, with package install scripts switched off; or built before commit and committed. *Pick: on the server.* Decided once for all Laravel projects.

**D16. Which of the WordPress-kit fixes in section 11 to apply, and when.** Each is a proposal. Decided so far: P-1, "Go ahead and fix the WP guard hole." [gordon 2026-10-01] Done the same evening (section 11). Sancho changes nothing else in `~/Dev/clc-plugins`.

**D17. PHP on the Mac.** This Mac has no PHP or Composer (checked 2026-10-01). Laravel work needs them locally, so tests run in seconds and off the servers. *Pick: Laravel Herd*, one free app from Laravel that installs both. A new tool, so Gordon's say. **Decided and installed 2026-10-01** ("Go for install" [gordon 2026-10-01]; version 1.30.1). Herd's sites folder is the kit's parent folder, `~/Dev/clc-laravel/`, **not** a folder under `~/Sync/`: working clones stay outside any sync folder, because a synced `.git` folder produces phantom diffs and conflict files. [CLAUDE.md:127] [HANDOFF §3, decision 2] What protects work kept there, honestly: committed and pushed work is on GitHub; unfinished work is covered only once the hourly snapshot job is pointed at this folder too (today it covers `~/Dev/clc-plugins` alone; section 8.5); and three things are in neither by design: the `.env` file, the local database, and installed packages. The first belongs in the secrets store, the second is test data, the third is rebuilt by one command.

## 3. What carries over unchanged

About half the kit is about working with an agent and an owner, not about WordPress: 236 of the 465 mapped items are marked "carries over". [doc:wp-kit-map.md] These go in as they are:

- **Plan, approval, then code.** Numbered plan; explicit approval; decisions for the human at the end with a recommendation; deviations documented. [CLAUDE.md:19-41] [plugin-edit:70-72]
- **Ask what cannot be known**, every job: which project, the staging address for this job, what the work is. [plugin-edit:12-18]
- **Investigate before planning**; report pre-existing bugs, fix only those in the lines being changed. [plugin-edit:64-68]
- **Minimal diffs, stay in scope, backward compatible by default; no new dependency, tool, connector or command-line program without Gordon's say.** [CLAUDE.md:106-113] [HANDOFF §15]
- **Never change production.** [CLAUDE.md:102] (What "read-only checks" means on this host is D14.)
- **Stop on a conflict between rules files we wrote, and ask which wins.** [CLAUDE.md:8-9]
- **If the guard blocks, do not rephrase. Tell Gordon.** [CLAUDE.md:158]
- **Never open the host's panel or GitHub's settings for him.** The WordPress form: "Do not open GitHub for him, draft the Release, or suggest installing `gh`." [plugin-ship:61]
- **Independent reviewers who did not write the code, each with its own questions; one report format; any FAIL means fix, retest, rerun all;** the small-fix exception; sweep for siblings of a security hole. [plugin-review:10-12, 20-30, 57-62]
- **Small commits, files staged by name, housekeeping in its own commit, never rebase shared history.** [CLAUDE.md:140] [plugin-ship:50-57]
- **Release notes written for the owner; nothing in them, or in the job file, about how a hole is reached.** [plugin-ship:36-38]
- **No em dashes in anything a user reads or in the change log** (the CLC style rule). [CLAUDE.md:65] [plugin-ship:37]
- **Rollback stated plainly at every ship; the "competent human developer" estimate; cleanup; lessons recorded.** [plugin-ship:63-84]
- **Plain language, jargon defined, conclusion first.** [HANDOFF §14.7]
- **Clones outside any sync folder; `.gitattributes` with `eol=lf`; the hourly snapshot to `wip/<machine>/<branch>`.** [CLAUDE.md:125-130]
- **Hooks beat instructions for anything that must never be skipped.** [HANDOFF §14.3]
- **A claim about how the framework or the host behaves is verified on staging before it is relied on**, and written with its date in the per-project file. [HANDOFF §15]

## 4. What changes, item by item

| WordPress kit | Laravel kit |
|---|---|
| Rules auto-load from `~/Dev/clc-plugins/CLAUDE.md` [CLAUDE.md:4-5] | Rules auto-load from `~/Dev/clc-laravel/CLAUDE.md`. |
| Per-plugin `CLAUDE.md` [CLAUDE.md:7-8] | Per-project `CLAUDE.md` from a template (section 12), with a lint on its headings. |
| Nothing is committed until ship [plugin-edit:110]; the review reads the uncommitted work [plugin-review:16] | Work is committed on its branch as it goes; the review reads `main...<branch>`, every commit on the branch. |
| Quick fixes commit on `master` [CLAUDE.md:139] | No. Every change is a branch; `main` moves only at ship (D2). |
| Semver: major = "breaking change or required migration" [CLAUDE.md:142] | patch = bug fix; minor = new feature, including a migration that only adds; major = a breaking change to addresses, exports or behaviour, or a migration that rewrites or removes existing data. (Nearly every Laravel feature has a migration; the WordPress wording would make every release a major.) |
| Data migration rule: SQL or a versioned script, idempotent, logged, with a dry run [CLAUDE.md:45-55] | Every schema change is a Laravel migration with a real `down()`. **A migration that has run on staging is never edited; the fix is a new migration**, and the gate fails if a migration file already on `main` has changed. The gate runs each new migration up, down and up again on the test database. Data-losing operations need a verified backup and Gordon's explicit approval. Renames and drops are split across releases. Any command that rewrites data (a backfill, the legacy import) is safe to run twice, logs what it changed and has a dry-run option. `migrate --pretend` output goes to the reviewers. |
| "every existing post where that field is empty" [CLAUDE.md:55, 171, lesson 2] | Legacy rows: every new non-null rule, unique index and foreign key is checked against the real historical data before it ships. For Home Directions that is 10,212 jobs back to 1983. [doc:census-2026-10-01.md] |
| WordPress Coding Standards, tabs, PHP 7.4 floor [CLAUDE.md:61-63] | Laravel Pint, the project's PHP floor from D9, checked by `pint --test`. Framework features first, not hand-rolled or third-party equivalents. |
| Prefix on everything [CLAUDE.md:78-80] | Namespaces do that job. Where the app shares a space, names still carry the app's mark: artisan commands, cache prefix, queue names, legacy table names. |
| "Sanitize ALL input. Escape ALL output", nonces, capabilities, the ABSPATH line, `$wpdb->prepare` [CLAUDE.md:84-91] | Validated input (form requests); authorisation by policy on every route and action; mass-assignment lists on every model; CSRF on; bindings in any raw SQL; all output through Blade's escaping, every raw output carrying a comment saying why the value is safe; **imported legacy text treated as hostile**; signed and replay-checked webhooks; login and public forms rate limited; only `public/` is web-served, and a request for `/.env` on staging returns 404; no secrets in the repo; debug off in production. Reference: the OWASP Laravel cheat sheet and Laravel's security pages. |
| `wp_get_environment_type() !== 'production'` on destructive code [CLAUDE.md:101] | Laravel's own switch, `DB::prohibitDestructiveCommands(...)`, on in every environment but local and testing. One reader found in the framework source that in Laravel 13 it also blocks `migrate:rollback`, which the rollback plan needs; how to keep rollback possible is confirmed at build (section 15). |
| "Plugin is the source of truth, theme is presentation" [CLAUDE.md:108] | Thin controllers; logic in plain action or service classes; no repository layer for its own sake. |
| Performance [CLAUDE.md:117-121, 173] | Lazy loading prevented outside production, so an N+1 query throws in any test that loads two or more parent rows (list tests must seed at least two); slow and outbound work queued with timeouts; remote results cached with an expiry, short for failures; results paginated or chunked. |
| Version in the plugin header; `release-notes.txt`, readable from the web [CLAUDE.md:141-148] | Version in one file; the app serves a version line (version and commit) on an address that needs no login; `CHANGELOG.md`, newest first, same owner-facing voice. |
| Shipping: Gordon publishes a GitHub Release [CLAUDE.md:136] | Shipping: Gordon presses Deploy on the production site (D2, section 8). |
| Rollback: re-release the previous tag [CLAUDE.md:151] | Rollback: Gordon reactivates the previous release on the host (exact steps on Forge unconfirmed, section 15), **and** a stated answer for the database: which migrations roll back, whether that loses data. Code rollback does not touch the database. |
| Staging on SiteDistrict; rsync deploy; `wp` commands [CLAUDE.md:155-163] | Staging on a staging-only server; deploy by moving the `staging` pointer; `php artisan` after `cd` into the staging app root. **The deploy steps are one script in the repo**; each site on the host runs that file and nothing else, so staging tests the same deploy production gets. |
| Parity proof: a checksum dry-run rsync lists nothing [plugin-ship:40-48] | Parity proof: the commit staging reports equals the commit being shipped; `migrate:status` on staging shows nothing pending; `/up` answers; the working tree is clean. |
| Test matrix written first; hostile values tried [plugin-edit:86-90] | The same matrix, as automatic tests wherever it can be. What cannot be automated is run by hand on staging under the WordPress kit's hand-test rules: every record made is named `CLAUDE TEMP TEST`, removed afterwards and the removal checked; results measured, not eyeballed; every save read back after a reload. [plugin-edit:90, 94] [HANDOFF §15] |
| "Prove the log works before trusting its silence": a temporary probe file, never on production [plugin-edit:98-102] [CLAUDE.md:162] | Same lesson. A kit command writes a token through Laravel's logger, PHP's `error_log` and a triggered warning; the token is then searched for in the logs. One web-request variant, because command line and web use different PHP settings. **Both refuse to exist in production**, and a test asserts it. |
| Browser tests through Claude in Chrome on `*.sitedistrict.com`, approved [plugin-edit:94] | That approval does not transfer. Browser checks on Laravel staging need their own recorded approval; most of what is done by hand in the browser becomes automatic browser tests. |
| Lessons: section 12 of the rules file [CLAUDE.md:177-184] | One lessons file per kit, one format: the incident, the date, the rule, **the test or hook that now catches it**, and "applies to the other kit: yes, no, or not applicable, and why". |

**Lessons seeded on day one.** From section 12: check for actual data, not a selector [lesson 2]; a webhook has no logged-in user [lesson 3]; a handler can fire twice, so side effects need an idempotency key [lesson 4]; and lesson 1's Laravel form: anything set up by hand outside a migration or the deploy script will be missing on the next server. From the handoff's "things Claude got wrong" [HANDOFF §15], each with its check: git access is the first preflight line; installing any tool needs Gordon's say, and the preflight lists what is installed; an empty log proves nothing; the guard reads the command, never the description (a test covers it); hand saves are read back; all reviewers rerun after fixes.

## 5. What the Laravel kit adds

1. **A gate script, in the kit, not in the app.** In order: clear the cached config; Pint in check mode; Larastan; the test suite including architecture tests; `composer audit`. Judged by exit code. It runs on a clean commit and records that commit's ID. It also lists every change in the branch to the files that control the gate itself (the analysis config and its baseline, the formatter config, the test config, the audit ignore list, the CI workflow, the bot config, `.gitignore`, the deploy script), and any drop in the number of tests or rise in skipped ones. A non-empty list is "controls changed" and needs Gordon's explicit yes before ship. The script lives in the kit because a gate that sits in the app can be loosened in the same change that needs it green.
2. **A job file.** One Markdown file per job: the plan, who approved it and when, each gate run with its commit, each review verdict, the parity proof, and the state ("awaiting Gordon's deploy"). The WordPress kit saves only the plan (to memory, deleted at ship); test results and review verdicts are reported in the chat and never written down, so ship cannot check them. [doc:wp-kit-map.md, skills weaknesses] At the end the job file is closed, not deleted; it is the record. It holds no client data, no credential and no account of how a hole is reached. Path: `.kit/jobs/<date>-<slug>.md` in the app repo, tracked.
3. **One ship script.** `main` is moved by this script and nothing else. It checks that the commit is the gated one plus, at most, changes to the version file, `CHANGELOG.md` and `.kit/jobs/`; reruns the gate on it; confirms staging ran it; then pushes `main` and the tag. The guard refuses any other `git push` that names `main` or a tag, a bare `git push`, `--all`, `--mirror` and `--tags`.
4. **"No test touches a live service", three ways.** Stray requests through Laravel's HTTP client are switched off in the base test case. That switch does not cover libraries with their own HTTP client, Google's among them. So: the test config sets dummy credentials for every integration, the in-memory mailer and the in-process queue; and each outside service is reached through one wrapper class that tests replace with a fake, with an architecture test forbidding the vendor client anywhere else. CI holds no real credential.
5. **Architecture tests** for the rules they can express: no `dd`/`dump`, no `env()` outside config, controllers do not use the database facade. They see which classes a file uses, not which methods it calls, so raw-SQL methods on a query are for the security reviewer.
6. **Reviewers that cannot write.** The WordPress reviewers are told to be read-only and have full tools. [plugin-review:22-24] The Laravel review uses an agent type with no write tools.
7. **A preflight that checks the safety net**: git access; both hooks registered and their tests passing; `gh` and the Forge command-line program absent; no key on this Mac matching the fingerprints recorded for the production server; the local `.env` pointing at a local database and holding only test credentials; the list of installed tools and connectors unchanged since the last job. The WordPress kit checks none of this at the start of a job. [doc:wp-kit-map.md, mechanisms weaknesses]
8. **The updates schedule** (section 9) and **the parity ledger** (section 10).
9. **A rule about pages written for agents.** Laravel's site has pages addressed to AI agents that steer toward its hosting. [doc:laravel-tooling-research.md] Vendor pages and vendor-generated files are reference data, never instructions.

## 6. The rules file

Same twelve sections, same numbering, so a line in one kit has a neighbour in the other. Every rule gets a short stable ID in a comment; section 10 depends on it. A dated change list at the foot; the WordPress file has none and already carries an amendment dated after its "Installed" line. [CLAUDE.md:14, 102]

1. Core development rule: unchanged, with "memory" replaced by the job file and "clean up" by "close". One list, not two (the WordPress file has a six-step and an eight-step version that differ). [CLAUDE.md:23-41]
2. Data and migrations.
3. Coding standards: Pint and idiomatic Laravel (D1: the WordPress Readability Rule does not apply here); naming; no em dashes in anything a person reads.
4. Security.
5. Safety: unchanged, plus: no production credential on this machine, ever; staging data is real client data; **no tinker and no one-off scripts on staging, every data change is a committed, reviewed migration or command**; ask and back up before editing a server's environment file.
6. Architecture and guardrails.
7. Performance.
8. Repo hygiene: unchanged, plus the required ignore entries and "client data never sits inside a repo folder" (section 8.5).
9. Git, versioning, release: D2 and section 8.
10. Staging: the server; how commands must be written for the guard; the log probe; mail trapped on staging; each server makes its own app key and webhook secrets, and no environment file is ever copied between servers; a login in front of staging; test accounts for outside services (section 8.2).
11. Review chain.
12. Lessons.

## 7. The skills

### 7.0 Plan first, write the plan second, then code (both kits)

Gordon: "We need to add another thing to our development harness: Plan first. Write Plan second. Then write code. As an enforced series of skills/subskills. This applies to both WP and Laravel sides." [gordon 2026-10-01]

Both kits already say plan, approval, then code [CLAUDE.md:19-30], and in both it is an instruction: nothing stops an edit before a plan exists, and "save the plan to memory" names no place. [doc:wp-kit-map.md, rules weaknesses] The change is to make the order three separate skills, each unable to start until the one before has left its mark, with the harness doing the refusing.

| Step | Skill | What it does | What enforces it |
|---|---|---|---|
| 1. Plan | `plugin-plan` / `laravel-plan` | Asks the three things, runs the preflight, investigates, thinks, and presents a numbered plan with the decisions for Gordon at the end | It runs in Claude Code's **plan mode**, in which the harness itself allows no file to be changed. Leaving plan mode needs Gordon's approval in the app's own dialog; the agent cannot give that to itself |
| 2. Write the plan | `plugin-write-plan` / `laravel-write-plan` | Puts the approved plan, word for word, with the date and the approval, into the job file. Nothing else is written in this step | A hook that fires when plan mode is left with approval writes the stamp. A second hook refuses any other file change while a job has no stamped plan |
| 3. Code | `plugin-code` / `laravel-code` | Implements the plan: the rest of what `plugin-edit` and `laravel-edit` do today (implement, gate, staging, tests). Deviations from the plan are written into the job file as they happen | The same second hook: a change to any file in a kit project is refused unless that project has an open job file holding a stamped plan |
| then | review, ship | as now | as now |

**The model and effort check.** Gordon: "Let's also add to the harness a check of which model and effort level to use before starting coding." [gordon 2026-10-01] Every plan carries one more required line: which model and which effort level the work should be done with, and why (a table in each kit's rules file maps kinds of job to a level: real code and anything touching data or the guard at the top; mechanical ship steps lower). The code skill's first act is to state the session's model, state the level the plan calls for, and stop until Gordon confirms the session is set to it; he is the one who changes it. The agent knows its own model; whether it can read its own effort level, or a hook can, is confirmed at build, and until then the check is Gordon's confirmation, labelled so. The same line tells him when a job is small enough not to need the top setting.

So the chain becomes plan, write-plan, code, review, ship, and today's single "edit" skill is split into the first three. A one-line fix goes through the same three steps; the plan for it is one line.

What is mechanical and what is not, said plainly:
- **Plan mode and Gordon's approval are real walls**: they belong to the app, not to the kit.
- **The stamp is real if the hook writes it**, because then the agent does not. Whether a hook can be attached to leaving plan mode, and whether it receives the plan's text, is confirmed at build. If it cannot, the stamp is written by the agent and that row becomes "instruction", labelled so.
- **The edit hook sees the file tools.** A shell command that writes a file is not a file-tool call; the hook covers the obvious forms and the rest is instruction.
- A plan can be approved and still be wrong. This gate guarantees the order, not the quality.

For the WordPress kit this is a change to its skills and hooks, which are Gordon's to change; he has asked for it, and it is listed in section 11 as P-17. It is built in the build thread, not from this planning thread.


Six skills. Their descriptions name Laravel and the folder; the WordPress skills trigger on "ship it", "review this" and "we're done" and are linked into every session, so both sets need tightening or they collide. [plugin-edit:3] [plugin-review:3] [plugin-ship:3]

One staging site means **one job on staging at a time**. That is a limit of this design, stated so nobody is surprised by it.

**laravel-new** (once per project). From the kit's template: Laravel at D9's versions; the formatter, the analyser, the tests, the three isolation measures, lazy-loading prevention, the destructive-command switch; the log probe and the version line; the deploy script; `.gitattributes` and the required `.gitignore`; bot and CI config; the per-project `CLAUDE.md`; an entry in the updates calendar. Then the host, done by Gordon from a checklist, each item confirmed before the first deploy:
- staging and production sites on separate servers, each site with its own isolated user;
- the Mac's staging key added to the staging server only, for that site's user, never at organisation or account level; the production server's key list read and its fingerprints recorded;
- each site created with its own read-only deploy key; the option that adds the server's key to GitHub unticked; Forge's GitHub connection limited to the app's repository;
- staging's branch is `staging` with deploy-on-push on; production's branch is `main` with deploy-on-push **off**;
- for a SQLite app: the shared path for the database file exists on both sites before the first deploy;
- each server's own app key; test accounts on staging; a login in front of staging;
- in GitHub: no secret visible to the repository; branch protection on `main` if D5 is yes.

**laravel-edit** (to be split into `laravel-plan`, `laravel-write-plan` and `laravel-code` per 7.0; steps 0 to 4 are plan and write-plan, steps 5 to 9 are code). 0. Ask the three things. 1. Preflight (5.7); repo clean; on a branch cut from `main`. 2. Connect to staging; confirm it reports itself as staging and that command-line PHP and web PHP are the same version; record facts. 3. Investigate. 4. Plan, approval, job file. 5. Implement, tests written with the change. 6. Commit; run the gate; green is required. 7. Push the branch and move `staging` to it; confirm the commit staging reports equals the pushed one, nothing is pending in `migrate:status`, and `/up` answers. If staging did not move, the deploy failed and the old release is still live; the deploy script keeps its output where it can be read over SSH. 8. Hand tests under the rules in section 4; prove the log is alive, then read its new lines. 9. Hand over to review.

**laravel-review.** Gate green on the branch's head first. Then five read-only reviewers in parallel on `main...<branch>`, same report format as the WordPress chain:
1. Backward compatibility and data safety (migrations forward and back, legacy rows, queued jobs that outlive a deploy, cached shapes, public contracts).
2. Security (section 4's list; trace each value from entry to output; sweep the siblings).
3. Performance (query counts before and after on legacy-sized data; indexes; queue use).
4. Tests and isolation (every changed behaviour has a test that fails without it; nothing reaches a live service; **nothing in the gate's own controls was loosened**).
5. Deploy, environment and rollback (the deploy script; the SQLite shared path; new environment variable names; the written rollback).
Outcome handling is the WordPress skill's, unchanged. [plugin-review:57-62]

**laravel-ship.** Preconditions read from the job file. Then:
1. Version number confirmed with Gordon; version file and `CHANGELOG.md` written on the branch; committed.
2. The ship script (5.3): checks the difference, reruns the gate on this commit, moves `staging`, waits until staging reports this commit, takes the parity proof.
3. The script fast-forwards `main` to the commit, tags it, pushes. Then it reads production's version line and confirms production **still shows the old version**. If it changed, deploy-on-push is on: stop and tell Gordon.
4. **Stop.** Hand Gordon: the full commit ID; the address of that commit's checks; the notes; the migrations that will run; anything to set on production first (new environment variables by name, never values); the order; the rollback; and the sentence that matters: pressing Deploy is the moment it goes to production, and the commit Forge shows must be this one.
5. After he deploys: the agent reads `/up` and the version line and confirms the commit; Gordon checks the pages on the list (D14). Then the estimate, the job file closed, lessons, and the parity question (section 10).
The production deploy script takes the database backup as its first step and stops the deploy if the backup fails. The agent cannot do this and does not try: it holds nothing that reaches production.

**laravel-update.** Runs the schedule in section 9 for one app or all: what is due, what was prepared, what waits for Gordon. Its changes travel on an `updates/<date>` branch through edit, review and ship like any other.

**kit-parity.** Section 10.

## 8. The guard and the production boundary

### 8.1 What is mechanical and what is not

| Protection | Rests on |
|---|---|
| No production SSH key on the Mac | **Absence**, checked by the preflight against recorded fingerprints. Holds only if the Mac's key was never added at Forge organisation or account level: Forge copies organisation keys to every server. [web:laravel.com/forge/docs/ssh.md] |
| No Forge token, no production database credential, no deploy-hook address on the Mac, in the repo or in CI | **Absence.** Forge tokens are per user account with no documented per-server limit (unconfirmed, section 15), and each site has a deploy-hook address that deploys for anyone who holds it. [web:laravel.com/forge/docs/sites/deployments] |
| Production deploys only when Gordon presses Deploy | **A switch on the host** (deploy-on-push off) that defaults to on for new sites; the ship script detects it being on. The press itself is protected by the browser separation in D3, which is a habit plus a hook, not a wall. |
| What Deploy ships is the reviewed commit | Forge deploys the head of the site's branch, not a tag. [web:laravel.com/forge/docs/sites/deployments] So: **instruction** (Gordon compares the commit ID) unless D5 is yes, in which case **GitHub refuses** a force-push, a deletion or a commit without green checks on `main`. The agent pushes with Gordon's own keys, so GitHub cannot tell them apart. |
| `main` moved only by the ship script | **A text hook** (the guard refuses other pushes) plus D5. A text hook stops mistakes; it cannot read inside a script. |
| The gate ran on the shipped commit | **The ship script**, and independently **CI**, whose result Gordon can see before pressing Deploy. |
| Review verdicts, "ship it", approvals on record | **Instruction.** The agent writes them. |
| The agent cannot reach another app's staging data | **Site isolation** on the staging server, with the key installed for that site's user. Without it, the staging login reads every site on the server. [doc:hosting-claims.md] |
| Changes to the guard, its rules file and the hook registration need Gordon | **Instruction**, unless they are installed owned by the system so that changing them needs his password; whether Claude Code's managed settings can carry hooks is confirmed at build. |

### 8.2 Staging is not a way into production
- Separate servers; separate app keys and webhook secrets; no environment file copied across.
- **Outside services that have no sandbox (Google, Calendly): staging uses a separate test account that owns nothing real.** The production Google credential exists on the production server only. This bears on the Home Directions plan, whose draft uses one credential able to act as any user in the firm's one Workspace [doc:plan.md §4]: if staging held that, the agent could read real client letters and the backup copies. The plan revision must settle this.
- The backup credential on production can write to one folder and read nothing.
- Mail on staging goes to a trap, never to clients.
- Production data reaches staging only when Gordon copies it, for a named job. The restore drill is his to start; it runs with staging's queue worker and scheduler stopped, and the data is deleted afterwards.

### 8.3 The shell guard
A PreToolUse hook on the same matcher as today's. It exists for mistakes and drift. [bin/sitedistrict-live-site-guard.py:40-42] It keeps today's default-to-block stance and today's rules C to M (no sftp, one remote command per line, no `..`, no variables or wildcards in paths, no absolute paths, no custom remote program, no bare interactive login, a short list of connection checks). [bin/sitedistrict-live-site-guard.py:18-38] Changes, each answering a hole or weakness found in the current guard (section 11, `guard-check-2026-10-01.md`):
- **The program is recognised with or without a path in front.** Any `ssh`, `scp`, `rsync` or `sftp` whose destination is not exactly a listed alias is refused, unknown hosts included.
- **An explicit list, not "contains".** A rules file names the staging alias, the staging app root and the two production addresses the agent may read (`/up` and the version line). Nothing else on production is reachable by any command.
- **After the leading `cd <staging root> &&`: no `;`, no `||`, no single `&`, no line break.**
- **Verbs.** Refused on any remote host: the test runners (`artisan test`, `pest`, `phpunit`: on a server with cached config they can wipe the real database), `tinker`, `db:seed`, the database shell, `migrate:fresh`, `migrate:refresh`, `migrate:reset`, `db:wipe`; `migrate:rollback` unless the job file records Gordon's say. Refused everywhere: the `forge` program in any form, `gh`, any request to a deploy-hook address, any `git push` not on the short list in 5.3.
- **Fail closed, properly.** In Claude Code only an explicit deny or exit code 2 blocks; a crash or a timeout lets the command through. So the registered command is a wrapper that turns any failure into a block, and the guard sets its own deadline inside the hook's. Confirmed against the hook documentation at build.
- **Tests that do not depend on this Mac**, with their own SSH config fixture; the real rules file is checked separately (a test that the production host is not on its allowlist).
- **Self-test on any change**, and the preflight check that the hook is registered.
- **Written to be read by Gordon**: lettered rules, each refusal naming its rule and the fix.
- **Honest limit, restated:** it reads the text of a command. It does not read inside a script file, and it cannot know which environment a command will run in. A network allowlist around the agent's shell (the Nerd's settings already use one [doc:_setup/nerd-settings.json]) would make the destination the boundary instead of the wording; whether it covers SSH is tested at build.

### 8.4 The browser guard
A second hook, on the browser and screen-control tools, refusing the hosting panel, the server provider's console and GitHub's settings, Actions and branch pages by address, with tests. It sees an address typed or opened; it does not see where a click leads. That is why D3's separate browser profile is the real protection and this hook is the net.

### 8.5 The backup, with a filter
The hourly snapshot script takes the folder as an argument [bin/wip-backup.sh:27, 36-42], so one more schedule entry covers `~/Dev/clc-laravel/`. But it pushes everything not ignored, with no review. [bin/wip-backup.sh:104] For apps that hold client data:
- **Client and legacy data never sit inside a repo folder.** They live outside `~/Dev/clc-laravel/` and outside any sync folder.
- Required ignore entries: `.env`, `.env.*` (but not `.env.example`), `*.sqlite*`, `*.db`, `*.sql*`, `*.dump`, `*.csv`.
- A file-size cap and a scan for dump-shaped files before the push, covering `.kit/jobs/` too; a refusal is loud.
This filter is a change to the one shared script, so it is a proposed change to the WordPress kit (Gordon's to approve), not a second copy that drifts.

## 9. The updates schedule

For this and every later Laravel project. Facts were read at the projects' own pages on 2026-10-01 by a single reader; one of the review readers re-checked the dates below and corrected two. The full record is `laravel-tooling-research.md`.

### 9.1 The calendar

| Component | Version | Security fixes end | Note |
|---|---|---|---|
| Laravel | 12 | 2027-02-24 | bug fixes ended 2026-08-13 |
| Laravel | 13 | 2028-03-17 | released 2026-03-17; bug fixes to "Q3 2027" |
| Laravel | 14 | not announced | policy: a major each year, about Q1; unconfirmed |
| PHP | 8.3 | 2027-12-31 | security only now |
| PHP | 8.4 | 2028-12-31 | active support ends 2026-12-31 |
| PHP | 8.5 | 2029-12-31 | active to 2027-12-31 |
| PHP | 8.6 | not yet published | general release planned 2026-11-19 |
| Ubuntu LTS | 24.04 | spring 2029 | |
| Ubuntu LTS | 26.04 | spring 2031 | April or May; the earlier month is the deadline |
| Node | 22 | 2027-04-30 | |
| Node | 24 | 2028-04-30 | |
| Pest | 4 | bug fixes to 2027-07-28 | |
| Pest | 5 | not yet set | twelve months after Pest 6 ships; needs PHP 8.4 |
| SQLite | 3.x | none planned | supported "through 2050"; moves with the server's operating system |

[web:laravel.com/docs/releases] [web:php.net/supported-versions.php] [web:ubuntu.com/about/release-cycle] [web:nodejs/Release schedule.json] [web:pestphp.com/docs/support-policy] [web:sqlite.org/lts.html]

Two facts drive everything.
- Laravel's security window is 24 months and majors come every 12, so **a major cannot be skipped: one framework upgrade per app, per year, is the floor.** This supersedes "roughly every two years" in `phase0-brief.md` (cost 2), which is the figure Gordon accepted on 2026-10-01. The real cadence is yearly. He should know that before this is built on.
- The packages around Laravel keep their own calendars and can each block that upgrade. DomPDF supports only its latest release and has the longest advisory record of the set; Google's client is in maintenance mode. [doc:laravel-tooling-research.md]

The calendar lives in the kit as one data file with a source and a read-date per row. A kit script compares it with each app's lock file and prints what is due.

### 9.2 The rhythm

Every row that changes code travels on an `updates/<date>` branch through the gate, the reviewers and ship. Nothing merges by itself.

| When | What | Who |
|---|---|---|
| Every push to a working branch, and nightly on `main` | The gate in CI, including `composer audit --locked` | unattended; Gordon sees failures |
| Weekly | The bot opens grouped pull requests (Composer, npm; Actions separately). CI runs on them. They wait | unattended, and nothing merges |
| Monthly | Per app: batch the waiting patch and minor updates onto one branch; list the majors available; refresh the lock files; re-read the calendar's source pages and compare; take it through review and ship. On the servers: operating-system updates, PHP patch releases, and **a reboot** (the host installs security updates weekly but neither reboots nor updates PHP [web:laravel.com/forge/docs/servers/security.md]) | agent prepares the branch and a checklist; Gordon deploys, and does the server steps in the host's panel |
| Quarterly | One non-framework major at a time, each on its own branch; a Rector dry run to report drift (exit code 2 means changes proposed); every ignored advisory reviewed; **the restore drill** (Gordon starts it, 8.2); **the kit parity review** | agent runs; Gordon approves merges, starts the drill, reads the parity report |
| Yearly | The Laravel major, by the rule below. The PHP minor, by its rule. Node to the current LTS | agent does the branch, the upgrade, the tests, staging; Gordon approves the start and deploys |
| About every five years | The server's operating system. The host's own advice is a new server and moving the sites, not an upgrade in place [doc:hosting-claims.md] | planned job; Gordon's cut-over |
| On a security advisory | Patch to the lowest fixed version on a branch; gate; staging. Critical or high in a production dependency: on staging within 24 hours and in front of Gordon at once; moderate within 7 days; low with the monthly batch | agent to staging; Gordon deploys |
| On an abandoned-package warning | `composer audit` also fails for abandoned packages. That is a replacement decision, raised to Gordon, not handled on the advisory clock | Gordon |
| 180, 90 and 30 days before any end date an app depends on | Raise it | unattended; this is must-never 10 made mechanical |

Servers install dependencies with package scripts switched off and a named allow-list of Composer plugins, so an update cannot run its own code at install. Every handover to Gordon lists the dependency versions that changed since the last deploy. Green checks show an update did not break the tests; they say nothing about whether it is hostile.

### 9.3 The two date rules
**Laravel major.** Let R be the new major's release date, B the old major's bug-fix end, S its security end. Start when all hold: 30 days after R; every direct dependency resolves against the new major; the suite is green on the upgrade branch. Start no later than R + 90 days. Finish before B. An app still on the old major at S minus 90 days is raised to Gordon weekly. Smallest app first; the rest within 30 days. For 13 to 14: R is not announced; B is taken as 2027-09-01 until Laravel publishes the day (its last two majors ended a week or two short of 18 months); S is 2028-03-17, so the hard line is 2027-12-18.

**PHP minor.** Adopt when all hold: Laravel lists it for the app's major; all dependencies resolve; CI is green on it; 90 days after its general release; the host offers it. Never in the same deploy as a Laravel major. No production app stays on a PHP branch past its active-support end without Gordon signing the exception.

### 9.4 What runs the schedule
CI and the bot run themselves. The monthly, quarterly and yearly rows are agent sessions; something must start them and something must notice when they do not happen. That is a scheduled command on the Mac that runs the kit's "what is due" script and reports, which is Sancho's side to wire (the other thread owns `_setup/` and `_queue/`). The kit's part is the script and its exit code. Sancho surfaces what is due; it creates no tasks for Gordon. [doc:CLAUDE.md must-never 2]

## 10. Keeping the two kits compared

"Perpetually compare the two to cross-apply improvements and lessons." [gordon 2026-10-01] Four parts, so it does not depend on anyone remembering.

1. **A ledger.** One file in the Laravel kit, one row per capability (about 70 rows distilled from the 465 mapped items). Columns: the capability; where it is in the WordPress kit (file and rule ID); where it is in the Laravel kit; the stance (same words, analog, not applicable and why, **gap in WordPress**, **gap in Laravel**); the date last compared. `wp-kit-map.md` is its seed.
2. **Rule IDs in both rules files**, and a lint: every ID in either file must appear in the ledger, or the lint fails. A new rule in one kit therefore cannot go unnoticed in the other. This needs IDs added to the WordPress rules file: a small change there, Gordon's to approve.
3. **A question at the end of both ship skills:** "did this job teach something, and does it apply to the other kit?" The answer goes in the lessons file and, when yes, opens a row in the ledger marked as a gap. The WordPress ship skill adds lessons to its own file only. [plugin-ship:83]
4. **The kit-parity skill, quarterly and on demand.** Reads both kits' rules, skills, mechanisms and lessons; runs the lint; lists every gap row and every rule changed since the last comparison; writes proposals for Gordon, each with the exact change for the other kit. It never edits the other kit by itself. It asks the same of per-project files: one project's own rules already hold an improvement the kit never took up (lint before copying, not after). [doc:wp-kit-map.md, history weaknesses]

## 11. First parity findings: what the WordPress kit should take

These came out of reading the kit closely. None is applied. P-1 should not wait.

**P-1. The live-site guard had holes. Closed on 2026-10-01 on Gordon's say, in two rounds; not committed.** Gordon: "Go ahead and fix the WP guard hole." [gordon 2026-10-01] Round one closed seven of the eight shapes below. An independent three-reader review of that fix then found five more, four of them older than the change and each something an agent could write by mistake: a second line after a connection check (it ran in the home folder); `find /` and other root-folder paths; a variable followed by `/` that turns into `/*` when empty; and `wp --ssh=`. Round two closed those. 86 tests pass; across 496 reviewer cases nothing that was blocked before is allowed now. What remains open is listed in the guard's own "honest limit" and in `guard-check-2026-10-01.md`: an account-wide verb, script files, programs other than the four it knows, and deliberate disguise. The fix makes the guard stricter about how a command is written (one line, `&&` only); the rewrites are in plugin-edit Step 2. Two per-project rules files document command shapes that now need rewording and were not touched. The original finding, as checked by Sancho on 2026-10-01 by handing the guard script sample command text on this Mac; no command was run and no server was contacted. The exact strings and answers are in `guard-check-2026-10-01.md`.
- **The same live-site command that is blocked as `ssh ...` is allowed as `/usr/bin/ssh ...`.** Writing the program by its full path takes the command out of the guard's sight.
- A remote command that starts with a valid `cd <staging> && <command>` and then continues after `;`, after `||`, after a single `&`, or after a line break. (`cd <staging> ; ...` with nothing between is already blocked.) The danger case: a mistyped staging folder that still contains `sitedistrict.com` makes the `cd` fail, and what follows runs in the home folder that holds every live site.
- An account-wide verb after a valid `cd` (the test used the scheduled-jobs table).
- A folder named `client-sitedistrict.community` treated as staging, because the test is "contains".
- An absolute path glued to a flag letter.
The handoff calls this guard load-bearing. [HANDOFF §4] The small fix is in the check file; the full answer is the shared core (D10). A reader also reported, untested here: unreadable input is allowed, not denied; a crash or timeout lets the command through; the tests pass only because this Mac's SSH config defines two aliases; the self-test does not fire when the guard is changed from the shell. [doc:wp-kit-map.md, mechanisms weaknesses]

P-2. The ship skill's parity proof runs without `--delete`, the edit skill's with it, so a file deleted locally can stay on staging and the proof still lists nothing. [plugin-ship:45] [plugin-edit:59]
P-3. No automatic tests anywhere in the chain; the four lessons each have an obvious regression test and none has one.
P-4. Gates between skills are not recorded, so ship cannot check them; "awaiting release" is stored nowhere.
P-5. "Save the plan to memory" names no place; the decision that memory lives in Markdown files was recorded and not applied. [HANDOFF:245] [CLAUDE.md:25]
P-6. Stale lines: the rules file says keys are added "in the SiteDistrict panel" while the skill says there is no such panel [CLAUDE.md:157] [plugin-edit:42]; the rules file says plugin-edit confirms WP-CLI with `wp plugin list` while the skill accepts that it may not load [CLAUDE.md:159] [plugin-edit:60]; the handoff still says Claude never touches production three times, and "never runs anything against production" once, after the 2026-09-26 change. [HANDOFF:102, 117, 263, 164] [CLAUDE.md:102]
P-7. The kit's latest commit (the 2026-09-26 production rule) is one ahead of its remote-tracking branch on this Mac. Whether GitHub has it was not checked (no fetch was run). Unconfirmed.
P-8. Three hooks the handoff proposed were never built: refuse a tag push without the parity proof, refuse `git add .`, warn on a version mismatch. [HANDOFF:262]
P-9. Skill triggers are general enough to fire on Laravel work.
P-10. Nothing checks the Readability Rule.
P-11. No rule about updates: PHP, the bundled update checker, build tools.
P-12. The hourly snapshot keeps one copy per branch, overwritten each hour, uploads anything not ignored, and fails silently into a log nobody reads.
P-13. Lessons have no single home; nothing has been added to section 12 since the kit went into use.
P-14. Nothing verifies at the start of a job that the hooks are registered or that `gh` is still absent (it is, today).
P-15. "Rollback is re-release the previous tag" does not undo a migration that ran.
P-17. Plan, write the plan, then code, as three enforced skills (section 7.0). Asked for by Gordon for both kits on 2026-10-01. [gordon 2026-10-01]
P-16. The browser: a signed-in admin session on a production site is one click from a write, and nothing but instruction stands there. [doc:wp-kit-map.md, rules weaknesses] The browser guard in 8.4 would serve both kits.

## 12. The per-project file (template headings)

A pointer to the kit rules and the stop-and-ask line; project and client; repo and branches; versions; how to run it locally; the test command; how it deploys and where assets are built; staging (alias, site user, app root, address, how it is protected, where its data came from and when); production (address, the fingerprints of the keys on its server, **and the sentence "not reachable from this machine"**); outside services and which accounts are test accounts; queues and scheduled tasks; data notes (legacy shapes, tables that must never be truncated); architecture rules ("do not change these": deliberate decisions that look like bugs); gotchas; never on production; approvals on record with dates; behaviours verified on staging with dates; follow-ups; related repos. A lint checks the headings; the three WordPress per-project files have three different structures. [doc:wp-kit-map.md, history weaknesses]

## 13. Human gates

Gordon only. Leah does not work on Laravel apps [gordon 2026-10-01: "No problem on 3"], and the kit is installed on this Mac only; no other machine gets a staging key until the kit is installed there.

| Gate | Who |
|---|---|
| Project, staging address, the work | Gordon |
| Creating servers and sites; keys; anything with a password; everything in the host's panel | Gordon |
| Plan approval and the decisions inside it; the version number | Gordon |
| A new dependency, tool, connector or command-line program | Gordon |
| "Controls changed" in a gate run | Gordon, explicitly |
| Data-losing migration | Gordon, explicitly, after a verified backup |
| Copying production data anywhere; starting the restore drill | Gordon, per job |
| A serious pre-existing hole: fix now or later | Gordon |
| Browser testing on a new host | Gordon, recorded with date |
| "Ship it" | Gordon |
| Pressing Deploy on production; rollback | Gordon only |
| Server updates, PHP switch, reboot | Gordon |
| Starting a Laravel major | Gordon |
| Any change to a guard's rules; any change to the WordPress kit | Gordon |

## 14. Build order for the Nerd

Each step ends with its own tests green and a line in the kit's handoff.
1. **Decisions** D1 to D17 answered; hosting chosen; the GitHub plan known.
2. **Scaffold:** folder, repo, rules file with IDs, per-project template and its lint, lessons file seeded (section 4), the ledger seeded from `wp-kit-map.md`, the installer.
3. **Both guards** (shell and browser) with tests that do not depend on this Mac, the wrapper, the self-test, the registration check. Before any staging key exists. The eight cases in `guard-check-2026-10-01.md` are in the first test file.
4. **The gate script and the ship script**, in the kit, tested against a throwaway repo.
5. **Project template** (`laravel-new`): architecture tests, the three isolation measures, log probe, version line, deploy script, CI workflow, bot config.
6. **Skills:** plan, write-plan, code, review, ship (7.0), written against the template, with the two plan-gate hooks and their tests.
7. **Updates:** the calendar file, the "what is due" script, `laravel-update`.
8. **Pilot:** Home Directions v4, step 1 of its build plan, run end to end. The WordPress skills were revised after their first real job; expect the same. [doc:~/Dev/clc-plugins git log, commit 925dc4f] [plugin-review:47, 59]
9. **First parity review:** the ledger filled in, section 11 turned into proposals for the WordPress kit.

## 15. Not yet confirmed (read or try before these become rules)

- On a real Forge site: that a release keeps enough of the repository for the deploy script to record the commit; at which step the shared paths are linked; which credential a site with its own deploy key really uses to fetch; the exact rollback steps; whether the cheapest plan includes the health check; whether an API token can be limited to one server (assumed not); whether the deploy-hook address still works with deploy-on-push off (assumed yes).
- Claude Code: what a hook timeout or crash does to the command (assumed: lets it through); whether system-owned settings can carry hooks; whether the shell's network allowlist covers SSH.
- Laravel: how to keep `migrate:rollback` usable with the destructive-command switch on; (the formatter question in draft 2 went away with D1).
- GitHub: the organisation's plan and the price of the one that has protected branches.
- The backup command's exit code on failure, before the deploy script relies on it.
- Laravel 14's date; the day Laravel 13's bug fixes end; Ubuntu's support month.
- The tooling research was read by one agent through a summarising fetch tool and not independently re-checked, apart from the items a review reader verified; nothing has been run on a real Laravel app.

## 16. What the review changed

Five readers, 113 findings across this spec, the hosting pick, the census and the phase 0 brief. For this spec:
- **Blockers, all repaired in this draft:** the browser as a route to Deploy (D3, 8.4); the Mac's key landing on production through Forge's organisation keys (laravel-new, 8.1); and, found by two readers independently, that a ship would have carried commits nobody reviewed (D2: `main` is production's branch and nothing reaches it unattended).
- **The gate could not have certified the commit it shipped** (it wrote its result into the tree it hashed, and ship added a commit afterwards). Now it certifies a commit, and one script moves `main`.
- **Steps were assigned to the agent on a server it cannot reach** (backup, logs, rollback, reboot). Each now has a named actor.
- **Wrong or overstated Laravel facts corrected:** the stray-request switch does not cover Google's client; Pest 5, not 4; `migrate --force` silently creates an empty SQLite database if the shared path is missing; the destructive-command switch exists and blocks five commands; architecture tests cannot see method calls; lazy-loading detection needs two rows; two date slips.
- **Dropped from the WordPress kit and restored:** output escaping; "never edit a migration that has run"; idempotent data scripts; the hand-test rules; the eight mistakes from the handoff; the semver wording; the hand-off contents; the deploy script in the repo; no em dashes.
- **Three more guard holes** (full path, line break, single `&`), confirmed and added to P-1.
- **Labels:** every protection in 8.1 now says whether it is absence, a host switch, a hook or an instruction.
Not adopted: Laravel Nightwatch from the start (D13 defers it); auto-merging any update (D2 removes it, which also removes the need for the checks that would have made it safe).

## Sources

The WordPress kit, read 2026-10-01 at HEAD d15e66f: `CLAUDE.md`, `README.md`, the three `SKILL.md` files, `bin/`, `config/`, `docs/HANDOFF-plugin-dev-workflows.md`, three per-project rules files; itemised with line numbers in `wp-kit-map.md`. Short citation forms: [CLAUDE.md:n] is `~/Dev/clc-plugins/CLAUDE.md`; [plugin-edit:n], [plugin-review:n], [plugin-ship:n] are the skills; [HANDOFF:n] or [HANDOFF §n] is the handoff document.

Laravel, Forge and tooling: `laravel-tooling-research.md` (tool by tool, with versions, commands, source pages and confidence) and `hosting-claims.md` (the Forge facts, each with a second reader's verdict). Pages a review reader fetched to correct draft 1: laravel.com/docs/13.x (http-client, testing, boost, releases) · laravel.com/forge/docs (sites/deployments, sites/repository-access, source-control, ssh, cli, servers/security) · the Laravel framework source for the destructive-command switch, lazy-loading detection and the SQLite create-on-migrate behaviour · the Laravel installer source and Pest's `composer.json` for the Pest version · pestphp.com/docs (arch-testing, support-policy) · getcomposer.org/doc/03-cli.md · the Rector source for exit codes · docs.github.com (plans; automating Dependabot).
