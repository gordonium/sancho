---
name: Home Directions v4 hosting options
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: Where to host v4 and the Laravel apps after it; Cloudflare's edge ruled out; Forge compared with a bare server ("dev in place") and with the other contenders, weighed for simplicity because Gordon said cost is not the issue; Sancho's pick, what it costs, what the maintainer still owns, the production boundary, what is unverified
sources: ["[gordon 2026-10-01]", "[doc:hosting-claims.md: 227 researched claims; 210 confirmed at the vendor's page by a second reader, 6 with no verdict matched in the record (3 of those corroborated in the checkers' notes), 1 wrong, 1 outdated, 9 could not be verified]", "[doc:phase0-brief.md]", "[doc:plan.md]", "[doc:laravel-kit-spec.md]", "[sancho subagent review 2026-10-01, workflow wf_4aaefbba-f62: numbers audit of draft 1]", "[web: vendor pages listed under Sources]"]
status: DECIDED by Gordon 2026-10-01: Laravel Forge, one server, on condition of automatic off-site backups (section "Decision"); the sections after it are the comparison as written before the decision, kept as the record
---
# Hosting options for v4 (and the Laravel apps after it)

Gordon, first: "Where should we host it? Can we do it on Cloudflare Edge?" Then: "Do we really need Laravel Forge, or can we just 'dev in place' at a staging address directly in Digital Ocean? The cost isn't an issue, just looking for simplicity over complexity. What advantages does Laravel Forge offer us? What are the other top contenders ... and their pros & cons?" [gordon 2026-10-01]

Prices and limits were read at the vendors' own pages on 2026-10-01 and each claim re-checked by a second reader; the record is `hosting-claims.md`. Anything not confirmed is marked.

## Decision (2026-10-01)

**Forge, on one DigitalOcean server that Gordon owns, with automatic backups stored somewhere else.**

Gordon: "Forge sounds awesome". Then: "one machine is fine under one condition: we need a good schedule of automatic backups that get stored somewhere else. Otherwise, the risks are ok. This is a very infrequently used system by one person, my dad, so little downtimes are likely never going to be noticed, let alone a big problem." And: "For more robust client systems in the future, we'll probably expand to two." [gordon 2026-10-01]

So: staging and production are two sites on the same machine, each under its own user. The Mac's key is installed for the staging site's user only. Sancho's pick had been two servers; Gordon weighed the risks and chose one, and the reasoning for two is kept below for the day a client system needs it.

| Item | Monthly |
|---|---|
| Forge Hobby (one server of our own) | $12.00 |
| Droplet, 2 GB, New York | $12.00 |
| DigitalOcean daily backups of the machine (30 percent) | $3.60 |
| Off-site backup storage | about $0 at this size |
| **Total** | **about $27.60** |

### The backup schedule (Gordon's condition)

DigitalOcean's own backups are kept **in the same datacenter as the server** [web:docs.digitalocean.com/products/backups/details/features/, read 2026-10-01], so they do not count as "somewhere else". They are the fast way back after a bad day; the off-site copy is what survives losing the provider or the account. Both run by themselves.

| What | When | Where it goes | Kept |
|---|---|---|---|
| The database (a consistent copy of the SQLite file) and the stored PDFs, in one encrypted archive | every night | a storage bucket at a different company from the server | 14 daily, 8 weekly, 12 monthly, then one a year, kept |
| The same archive | before every deploy that changes the database; the deploy stops if it fails | same | with the dailies |
| The whole machine | daily, by DigitalOcean | DigitalOcean, same datacenter | DigitalOcean's rolling window (length not confirmed at their page) |
| A restore test: last night's archive loaded onto the staging site and its counts compared | every quarter, and once before go-live | staging | the result is written down |
| A check that last night's archive arrived | every morning | an alert to Gordon when it did not | n/a |

- **Where "somewhere else" is.** Pick: a bucket at Cloudflare (R2), where the domain's DNS already lives. It is a third company, independent of both DigitalOcean and Google; Laravel reads and writes it with its built-in driver; storage is free up to 10 GB. [web:developers.cloudflare.com/r2/pricing/] [web:laravel.com/docs/13.x/filesystem] The alternative is a folder in the firm's Google Drive, which Gordon and Peter could see without any tool, but the letters live in that same Google account, so one lock-out would take the letters and their backups together.
- **The letters themselves** are Google Docs and are not in these archives. Each sent letter's PDF snapshot is. A copy of the letters folder outside Google is a separate question for the plan.
- **The credential** the server uses for the bucket can reach that one bucket and nothing else.
- **Restoring is Gordon's action**, from a short written procedure the first restore test produces.
- The backup tool the research found (spatie/laravel-backup, which handles SQLite and writes to any storage Laravel knows) and its failure behaviour are confirmed at build. [doc:laravel-tooling-research.md]

What one machine costs in protection, as accepted: a runaway job on staging can slow or stop the live app; the wall between the agent and production is a permission between two users on the same machine, not a separate computer; system-level changes cannot be tried on staging first. The kit's checklist for a new project adds one test for this arrangement: from the staging site's user, production's folder cannot be read.

## The short answer

- **Cloudflare as the host: no.** Detail below.
- **A bare DigitalOcean server with no Forge: it works, and it is not the simpler choice.** It trades one vendor for a dozen hand-built parts that we would then own.
- **Pick: two small servers in a DigitalOcean account Gordon owns, with Laravel Forge managing them.** About $47 a month with cost set aside as he asked ($34 in the leaner variant). Later Laravel apps go on the same pair.

## Forge, or a bare server

**What Forge is.** A control panel, not a host. It logs in to servers you own and sets them up, and it keeps a button for each routine job. If Forge vanished the servers would keep running; they are ordinary Ubuntu.

**What it does that we would otherwise build and maintain by hand:**

| Job | With Forge | On a bare server |
|---|---|---|
| A new server, hardened (firewall, keys only, weekly security updates) | a form | a setup script we write and keep current |
| Web server and a site | a form | Nginx config by hand |
| Certificates, issued and renewed | automatic | certbot, and watching that renewal keeps working |
| PHP installed; a new PHP version switched in | a click per version | package work by hand each year |
| The queue worker, kept alive across crashes and reboots | a form | a Supervisor or systemd unit we write |
| The scheduler | a toggle | a cron line |
| Deploys that do not interrupt the site, the last four kept, a way back | built in | a release-folder script we write, and a rollback script |
| A Deploy button and a deploy log Gordon can read | built in | Gordon runs a command over SSH, or we build a trigger |
| Each site under its own user; the database file kept across releases | settings | by hand |
| A check after each deploy that the site answers | built in (plan to confirm) | by hand |
| The next app | repeat the forms | repeat all of the above |

[web:laravel.com/forge/docs: servers/security.md, sites/deployments.md, server-providers.md] [doc:hosting-claims.md]

**What Forge costs in complexity.** It is one more account, and it has defaults that must be set right once: deploy-on-push is on for new sites; organisation-level keys are copied to every server; its GitHub connection reaches every repository unless limited. The kit spec's checklist covers each. [doc:laravel-kit-spec.md §7 laravel-new, §8.1]

**What Forge does not do, either way:** reboot after a kernel fix; update PHP by itself; move the server to a new Ubuntu every five years or so; back up a SQLite file; alert on thresholds below its $39 plan. [doc:hosting-claims.md]

**"Dev in place".** Two different things hide in the phrase.
- *A staging address that always shows the current work.* Yes. That is in the pick: the agent pushes, staging updates within a minute or so, Gordon looks.
- *Editing the code on the staging server itself, as its only home.* That is the part to avoid. The working copy on the Mac is what the hourly snapshot protects and what the guard watches; a server that can push to GitHub holds a credential that can write to the repository; and tests run on a server holding client data have a way of wiping the wrong database. Laravel is built to run and be tested on the developer's machine in seconds, which WordPress never was.
  One consequence Gordon should know: **this Mac has no PHP or Composer today** (checked 2026-10-01; Node and SQLite are present). Local development needs PHP installed, which is one free app (Laravel Herd) and needs his say, as any new tool does.

**Verdict.** For one app, a hand-built server is perhaps a day of setup and looks simpler on day one. Over ten years and several apps it is the more complex choice, because every part in the right-hand column is ours to remember. Forge is the thing that makes an owned server simple. Keep Forge.

## The contenders

| | What it is | Monthly | Simple on day one | Simple over ten years | Fits the plan as drafted | Main risk |
|---|---|---|---|---|---|---|
| **Forge + two DigitalOcean servers (pick)** | Laravel's panel on servers Gordon owns | about $47 (lean: $34) | yes: forms, and a checklist done once | chores remain: monthly updates and a reboot, yearly PHP, a server move about 2031 | yes: SQLite, worker, cron, DomPDF, nothing in front of webhooks | the chores being skipped; Forge's defaults set wrong |
| **Bare DigitalOcean server, hand-built** | the same servers, no panel | about $28 for the same pair | looks simplest; a day of scripts | the most to own: everything Forge does, by hand, per app | yes | hand-built parts rot; no Deploy button; no one else's docs to lean on |
| **Laravel Cloud** | Laravel's managed platform; no server at all | about $15 awake ($5 asleep) | yes: connect the repo | nothing to patch; but the platform moves under you (several features retired in its first 19 months) | **no**: no SQLite; PDF by DomPDF unproven; queue and file storage done its way; its firewall cannot be tuned on the cheap plans | forced changes; a webhook silently blocked |
| **Ploi + own servers** | a Forge-like panel from a small Dutch firm | about $44 | yes | as Forge; its $16 plan adds file backups to Google Drive and monitoring, which Forge keeps for $39 | yes | a smaller vendor for a ten-year bet; none of Laravel's own docs assume it |
| **Fly.io** | containers on their machines | about $10 | no: we own a Dockerfile | no OS to patch; but short outage on every deploy, and the layout this app needs is the one their docs advise against | partly: SQLite on one machine only | company changed chief executive and direction in July 2026; frequent incidents |
| **Cloudways** | a managed server (DigitalOcean underneath) with a panel | $14 to $28 | yes | they patch the server; their bot protection sits in front | probably: worker and SQLite support unconfirmed | webhooks against their bot filter, untested |
| **Cloudflare's edge** | Workers or Containers | n/a | no | no | **no** | n/a |

Monthly figures are arithmetic from listed rates for staging plus production, not quotes. [doc:hosting-claims.md]

How the six real ones differ, in a sentence each:
- **Forge + own servers** keeps the app boring and the servers ours, at the price of a short list of recurring chores that go on the updates schedule.
- **A bare server** has the fewest logins and the most homework.
- **Laravel Cloud** has no homework and changes the app: a database service instead of a file, files in object storage, their queue. If "simple" means "nothing to maintain, ever", this is the one, and the plan would be redrawn around it. It is also the youngest product on the list.
- **Ploi** is Forge with better backups on the cheaper plan and a smaller company behind it.
- **Fly.io** is cheap and clever, and neither is what was asked for.
- **Cloudways** is the closest to how SiteDistrict feels (they run the server), with two unknowns that would need a trial.

## Why not Cloudflare's edge

1. **Workers has no PHP.** The supported languages are JavaScript, TypeScript, Python and Rust, plus WebAssembly. [web:developers.cloudflare.com/workers/languages/] The only PHP route is a one-person community WebAssembly build whose own notes list no held-open database transactions, one PHP execution at a time per isolate and a 96 MiB memory ceiling. [web:github.com/seanmorris/php-wasm CLOUDFLARE.md] No place for a queue worker.
2. **Cloudflare Containers runs PHP, against the grain.** Generally available since 2026-04-13 on the $5 Workers Paid plan. The disk is ephemeral: after a sleep the next start is a fresh disk, so SQLite on a file is out. There is no Cloudflare database with a maintained Laravel driver (the one community package Cloudflare lists last changed in October 2023); an outside MySQL or Postgres is implied reachable but undocumented. A resident queue worker and an every-minute scheduler have to be assembled from a Worker, a Durable Object and a Cron Trigger. The product was redesigned on 2026-09-30 around "agent sandboxes". [doc:hosting-claims.md, Cloudflare]
3. **What Cloudflare is good for here:** DNS (already there [dns:homedirections.net NS, 2026-10-01]). Optionally, later, Access in front of the login and a Tunnel so the server has no open ports; both mean proxying the hostname through Cloudflare, which also brings a 100 MB upload cap, a 125-second timeout, an allow rule for Forge's health checks, dependence on Cloudflare being up, and two bot features that must be kept off or skipped for the webhook paths (the free plan's Bot Fight Mode cannot be exempted by rule). [doc:hosting-claims.md] The pick starts with the hostname unproxied, which avoids all of it.

## The pick, in full

**Laravel Forge managing two servers in a DigitalOcean account Gordon owns: production (2 GB, New York, daily backups) and staging (2 GB).**

| Item | Monthly |
|---|---|
| Forge Growth (needed for two servers of our own; Hobby allows one) | $19.00 |
| Production droplet, 2 GB | $12.00 |
| Daily backups of production (30 percent) | $3.60 |
| Staging droplet, 2 GB | $12.00 |
| **Total** | **$46.60** |

The leaner variant in draft 1 was $33.60: Forge Hobby ($12), the same production server and backups, and a 1 GB staging server billed through Forge ($6). The difference buys two things: both servers are ours (a Forge-billed server cannot be kept if we leave Forge), and staging is the same size as production, so a deploy that fits one fits the other. [web:laravel.com/forge/pricing] [web:digitalocean.com/pricing/droplets] [web:docs.digitalocean.com/products/backups/details/pricing/]

Why this one:
1. **It keeps the plan as drafted.** SQLite on a disk, copied nightly to Drive; a resident queue worker; cron; DomPDF. [doc:plan.md §2, §5] Forge documents SQLite through a shared path that survives releases. [web:laravel.com/forge/docs/sites/deployments.md]
2. **Nothing sits in front of the webhooks.**
3. **Later apps cost nothing extra while they fit on the same pair** (how many a small server carries was not verifiable; unconfirmed). Gordon expects more Laravel projects. [gordon 2026-10-01]
4. **The servers are ours.** They can be detached from Forge and keep running. [web:laravel.com/forge/docs/servers/the-basics.md] Ownership itself costs nothing: a 2 GB droplet is $12 against $13 billed through Forge.
5. **Provider-level daily backups of the whole production server** on top of the nightly SQLite copy. Forge's own backup feature lists MySQL, MariaDB and Postgres only; SQLite is not listed (inferred from that, not stated outright). [web:laravel.com/forge/docs/resources/databases.md]
6. **Longest track record of the candidates**, and it is Laravel's own.

The 2 GB size is judgement, not evidence: it buys memory headroom for the build on the server (deploys are limited to 10 minutes) and for headless Chrome later. 1 GB would work today at $6.

Why DigitalOcean: New York is confirmed, and Forge provisions it directly. Provider stability over ten years was not researched for any of them. With backups, Vultr would be $3.60 a month cheaper and Akamai (Linode, Newark) $1.10; Hetzner roughly tripled its US prices on 2026-06-15 and is out. [doc:hosting-claims.md, servers]

## Why two servers, and whether one would do

Gordon asked. [gordon 2026-10-01] One server would do: Forge can run the staging site and the production site side by side, each under its own user, with the Mac's key installed for the staging site's user only. It is one machine to update, reboot and eventually move, instead of two. What the second server buys:

1. **The wall is a different machine, not a setting.** With two servers, the key on this Mac opens a computer that has no production data on it. With one, it opens the computer that holds forty years of client records, and what keeps the agent out of them is a file-permission boundary between two users. That boundary is real, but it is a configuration that can be set wrong, and Forge's own main login can read every site on the server. [doc:hosting-claims.md]
2. **Staging is where things go wrong on purpose.** The legacy import will be rehearsed there many times: large files, long jobs, a disk that fills. On a shared machine a rehearsal that runs away takes the live app down with it.
3. **Server changes get tried first.** A new PHP version can be tried per site on one machine; a system update, a new package (headless Chrome), or the move to a new Ubuntu cannot.

What it costs: a second machine on the monthly update-and-reboot list, and $12 to $19 a month, which Gordon has said is not the issue.

Pick: two. If one is preferred for simplicity, it is a sound choice with the per-site users set up as above, and splitting later is a small job in Forge (create the second server, move the staging site).

## What we still own on this pick

- **Reboots.** Forge installs security updates weekly but does not reboot; a kernel fix takes effect only after a manual reboot of each server. [web:laravel.com/forge/docs/knowledge-base/cve-2026-31431.md]
- **PHP updates.** Patch releases are a click per version; a new PHP minor is installed and switched by hand. [web:laravel.com/forge/docs/servers/php.md]
- **The operating system.** Ubuntu 26.04 has standard support to spring 2031. Forge's docs strongly advise against upgrading in place and recommend a new server and moving the sites; a self-upgraded server has been recognised since March 2026. Plan on a rebuild-and-move of each server about 2031 and again about 2035. [doc:hosting-claims.md]
- **Backups and a tested restore.**
- **Monitoring.** Threshold alerts are documented as $39-plan only; the pricing page and the docs disagree on what the cheaper plans include, so heartbeats and health checks must be confirmed in the dashboard. Unconfirmed.
- **Support.** On the cheaper plans it is community, best effort, no response time; Growth states a 24-hour goal on business days. [doc:hosting-claims.md]

All of these become rows in the updates schedule in `laravel-kit-spec.md` §9.

## The production boundary on this pick

The WordPress kit's release gate rests on one fact: pushing does not ship. [doc:~/Dev/clc-plugins/CLAUDE.md §9] On Forge the default is the opposite. The boundary has to be built, and the review found six places where the obvious version leaks. The kit spec's section 8 is the full design; in short:

1. **The agent holds no Forge token.** They are per user account with no documented per-server limit.
2. **No server key on GitHub.** Untick the option that adds it; each site gets its own read-only deploy key; Forge's GitHub connection is limited to the app's repository. [web:laravel.com/forge/docs/ssh.md] [web:laravel.com/forge/docs/sites/repository-access.md]
3. **Deploy-on-push is off for production. Gordon presses Deploy.**
4. **The Mac's key goes on the staging server only, never at organisation or account level.** Forge copies organisation keys to every server. [web:laravel.com/forge/docs/ssh.md]
5. **The production deploy-hook address is never stored anywhere the agent can read.** Every site has one, and it deploys for whoever holds it. [web:laravel.com/forge/docs/sites/deployments]
6. **Forge, DigitalOcean and GitHub's settings are signed in only in a browser the agent cannot drive.** The agent works through Gordon's real Chrome; a signed-in panel there is one click from Deploy.

No production SSH key and no production database credentials on the Mac. Two servers, so the staging key opens staging only; in the WordPress arrangement one staging key opens the whole hosting account. [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md §4]

## What would change the pick

- **"I never want to maintain a server, and I accept redrawing the plan."** Then Laravel Cloud. The database becomes MySQL or Postgres [web:laravel.com/cloud/docs/knowledge-base/sqlite.md]; PDFs may need a different renderer (Laravel's guide says the Dompdf renderer in its billing package does not work there; standalone DomPDF is untested) [web:laravel.com/cloud/docs/knowledge-base/generating-pdfs.md]; the queue follows Cloud's managed queues; webhooks pass a firewall that cannot be tuned on the cheaper plans. [web:laravel.com/cloud/docs/network.md] Its tokens can be limited to one environment, the cleanest agent boundary of any option (whether on the cheapest plan is unconfirmed). [web:laravel.com/cloud/docs/api/authentication.md]
- **"Someone else should run the server, the way SiteDistrict does."** Then a trial of Cloudways, to settle its two unknowns.

## Before committing

1. Does Gordon already have a Forge or DigitalOcean account? Nothing on disk says. [unconfirmed]
2. Which GitHub plan is the organisation on? Protected branches on private repositories need a paid one. [unconfirmed]
3. PHP on the Mac (Laravel Herd): his say.
4. In the Forge dashboard, once it exists: whether the plan includes heartbeats and health checks.

## Also learned, useful later

- **Calendly retries failed webhooks for 24 hours with backoff, then disables the subscription.** Source: a Calendly employee's community post from 2023-12-14, not the developer docs. [secondary; unconfirmed at primary] A day-long failure therefore needs a monitor.
- **Laravel Vapor is closed to new signups.** [web:vapor.laravel.com]
- **PHP 8.5, not 8.4**, for a server built now. [web:php.net/supported-versions.php] Supersedes "PHP 8.4" in `phase0-brief.md`.

## What was not verified

Of 227 claims: 9 could not be confirmed at a vendor page (Forge's annual prices; Forge-billed server regions; Forge object-storage price; how many sites a small server carries; whether Forge-billed servers have any server-level backup; the Railway and Upsun totals; whether SiteGround allows a resident worker); 6 have no second-reader verdict matched in the record, three of them bearing on Laravel Cloud (its firewall warning, its scoped tokens, its sleep behaviour) and corroborated in the checkers' notes; 1 was wrong and 1 outdated, neither changing a verdict. Vendor pages were not re-fetched for this revision.

## Sources

The per-claim record, with pages and verdicts: `hosting-claims.md`.

Cloudflare: developers.cloudflare.com/workers/languages/ · developers.cloudflare.com/changelog/post/2026-04-13-containers-sandbox-ga/ · developers.cloudflare.com/containers/faq/ · developers.cloudflare.com/d1/reference/community-projects/ · blog.cloudflare.com/faster-agent-sandboxes/ · developers.cloudflare.com/bots/get-started/bot-fight-mode/ · developers.cloudflare.com/waf/tools/browser-integrity-check/

Laravel: laravel.com/forge/pricing · laravel.com/forge/docs (servers/the-basics.md, servers/security.md, servers/php.md, sites/deployments.md, sites/repository-access.md, ssh.md, resources/databases.md, knowledge-base/cve-2026-31431.md, server-providers.md) · laravel.com/cloud/pricing · laravel.com/cloud/docs (knowledge-base/sqlite.md, knowledge-base/generating-pdfs.md, network.md, api/authentication.md) · vapor.laravel.com

Servers and platforms: digitalocean.com/pricing/droplets · docs.digitalocean.com/products/backups/details/pricing/ · api.linode.com/v4/linode/types · api.vultr.com/v2/plans · docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/ · ploi.io/pricing · docs.fly.io/about/pricing/ · fly.io/news (2026-07-24) · cloudways.com/en/pricing.php · docs.github.com/en/get-started/learning-about-github/githubs-plans
