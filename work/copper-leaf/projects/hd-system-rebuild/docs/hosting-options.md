---
name: Home Directions v4 hosting options
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: Answer to "can v4 run on Cloudflare's edge, and if not where"; four research angles each re-checked at the vendor's own pages on 2026-10-01; Sancho's pick (Laravel Forge with an own-account production server), what it costs, what the maintainer still owns, and what must be true before committing
sources: ["[gordon 2026-10-01]", "[doc:phase0-brief.md]", "[doc:plan.md]", "[sancho subagents 2026-10-01, workflow wf_36d1b645-ad7: 8 agents, 227 claims, 216 confirmed at the vendor's page, 1 wrong, 1 outdated, 9 could not be verified]", "[web: vendor pages listed under Sources]"]
status: for Gordon's decision; nothing here is approved
---
# Hosting options for v4 (and the Laravel apps after it)

Gordon asked: "Where should we host it? Can we do it on Cloudflare Edge? Otherwise, we need a task to shop hosting options." [gordon 2026-10-01] This is the shopping, done. Prices and limits were read at the vendors' own pages on 2026-10-01 and each claim was re-checked by a second reader; anything not confirmed is marked.

## The short answer

- **Cloudflare as the host: no.** Workers does not run PHP; Cloudflare's container product runs it but has no persistent disk and no supported Laravel database path.
- **Cloudflare in front: yes, later and optionally.** DNS is already there. [dns:homedirections.net NS, 2026-10-01]
- **Pick: Laravel Forge (Hobby, $12) managing a production server in a DigitalOcean account Gordon owns, plus a small Forge-billed staging server. About $34 a month, flat, and the next Laravel apps ride on the same pair for nothing extra.**

## Why not Cloudflare's edge

1. **Workers has no PHP.** The supported languages are JavaScript, TypeScript, Python and Rust, plus WebAssembly. [web:developers.cloudflare.com/workers/languages/] The only PHP route is a one-person community WebAssembly build whose own notes list no held-open database transactions, one PHP execution at a time per isolate, a 96 MiB memory ceiling and an in-memory filesystem. [web:github.com/seanmorris/php-wasm CLOUDFLARE.md] No place for a queue worker.
2. **Cloudflare Containers runs PHP, against the grain.** Generally available since 2026-04-13 on the $5 Workers Paid plan. [web:developers.cloudflare.com/changelog 2026-04-13] The disk is ephemeral: after a sleep the next start is a fresh disk. [web:developers.cloudflare.com/containers/faq/] So SQLite on a file is out. The D1 database is reachable from a container only through hand-written HTTP glue; Cloudflare has no official Laravel driver and the one community package it lists last changed in October 2023. [web:developers.cloudflare.com/d1/reference/community-projects/] [web:github.com/renoki-co/l1] A resident queue worker and an every-minute scheduler have to be assembled from a Worker, a Durable Object and a Cron Trigger. The product was redesigned on 2026-09-30 around "agent sandboxes". [web:blog.cloudflare.com/faster-agent-sandboxes/] That is the wrong direction for a system meant to sit still for ten years.
3. **What Cloudflare is good for here**, at $0: DNS (already), and optionally Access in front of the login (free to 50 users) and a Tunnel so the server has no open ports. [web:cloudflare.com/sase/products/access/] [web:developers.cloudflare.com/tunnel/] Two cautions if the hostname is ever proxied: the free plan's Bot Fight Mode cannot be exempted by rule, so it must stay off or Calendly and mail-provider webhooks can be challenged [web:developers.cloudflare.com/bots/get-started/bot-fight-mode/]; and Browser Integrity Check, on by default, needs a skip rule for the webhook paths. [web:developers.cloudflare.com/waf/tools/browser-integrity-check/] The pick below starts with the hostname unproxied (DNS only), which avoids both.

## The options that fit, side by side

| | Forge + own DigitalOcean server (pick) | Forge + Laravel VPS only | Laravel Cloud (Starter) | Fly.io | Plain server, no panel |
|---|---|---|---|---|---|
| Monthly, app one, staging + production | about $33.60: Forge $12, 2 GB droplet $12, daily backups $3.60, 1 GB staging $6 | $24 (two 1 GB) to $31 (2 GB production) | about $5 asleep, about $15 with production awake | about $9.50 | about $17 |
| Apps two and three | $0 extra on the same pair | $0 extra | about $14 to $15 each if awake | about $9.50 each | $0 extra |
| SQLite on a real disk | yes, documented | yes | **no**, not supported | yes, on one machine only | yes |
| Queue worker and scheduler | built in (Supervisor, cron) | built in | built in, but sleeps; managed queues are the intended route | hand-built in one machine | hand-built |
| Webhooks | always on, nothing in front | same | pass a firewall that cannot be tuned on Starter | always on if never stopped | always on |
| DomPDF | yes | yes | Laravel's own guide says the Dompdf renderer does not work there | yes | yes |
| Agent cannot reach production | by keys and a switch (below) | same | by a scoped token (best of the set) | by a per-app token | by keys |
| Who patches the server | Forge applies Ubuntu security updates weekly; reboots, PHP updates and the OS upgrade every few years are ours | same | nobody: no server | we own the Dockerfile | everything is ours |
| Server survives leaving the vendor | yes, it is our droplet | **no**: deleted when removed from Forge | no server; standard code and a database dump | Dockerfile and one file | yes |
| Track record | Forge: over a decade | same | changelog starts February 2025; several features already retired | new chief executive July 2026, strategy now "computers for agents"; about two dozen status entries in August 2026 | n/a |

Sources for the rows are listed at the end. The monthly totals are arithmetic from the vendors' listed rates, not quotes.

## The pick, in full

**Laravel Forge, Hobby plan, with production on a 2 GB DigitalOcean droplet in New York in an account Gordon owns, and staging on a 1 GB Forge-billed server.**

Why this one:
1. **It keeps the plan as drafted.** SQLite on a disk, copied nightly to Drive; a resident queue worker; cron; DomPDF. [doc:plan.md §2, §5] Forge documents SQLite through a shared path that survives releases. [web:laravel.com/forge/docs/sites/deployments.md]
2. **Nothing sits in front of the webhooks.** No bot filter, no cold start.
3. **Flat cost that does not grow with the next apps.** Forge Hobby allows unlimited sites, unlimited Forge-billed servers and one outside server. [web:laravel.com/forge/pricing] Gordon expects more Laravel projects. [gordon 2026-10-01]
4. **The production server is ours.** A server in our own DigitalOcean account can be detached from Forge and keeps running; a Forge-billed server cannot be archived or kept and is destroyed when removed. [web:laravel.com/forge/docs/servers/the-basics.md] For a ten-year system that asymmetry matters more than the $10 it costs.
5. **Provider-level daily backups of the whole production server** (30 percent of the droplet price) on top of the nightly SQLite copy. [web:docs.digitalocean.com/products/backups/details/pricing/] Forge's own backup feature needs the $39 plan and covers MySQL, MariaDB and Postgres only, not a SQLite file. [web:laravel.com/forge/docs/resources/databases.md]
6. **Longest track record of the candidates**, and it is Laravel's own.

Why 2 GB for production: Composer and the asset build run on the server inside a 10-minute deploy limit [web:laravel.com/forge/docs/sites/deployments.md], and headless Chrome, if it is ever wanted for PDFs, does not fit beside PHP in 1 GB (judgement, not a vendor statement). The 1 GB size at $6 would work today and saves $7.80 a month; resizing up later is supported, down is not.

## What we still own on this pick (the honest list)

- **Reboots.** Forge installs security updates weekly but does not reboot; a kernel fix takes effect only after a manual reboot of each server. [web:laravel.com/forge/docs/knowledge-base/cve-2026-31431.md]
- **PHP updates.** Patch releases are a click per version; a new PHP minor is installed and switched by hand. [web:laravel.com/forge/docs/servers/security.md]
- **The operating system, about every five years.** Ubuntu 26.04 has standard support to spring 2031. [web:ubuntu.com/about/release-cycle] An in-place upgrade is recognised by Forge since March 2026; a rebuild is the other route. [web:laravel.com/forge/docs/changelog.md]
- **Backups and a tested restore.** Ours on every Forge plan.
- **Monitoring.** Threshold alerts are documented as $39-plan only; the pricing page and the docs disagree on what Hobby includes, so heartbeats and health checks must be confirmed in the dashboard. Unconfirmed.

All of these become rows in the updates schedule in `laravel-kit-spec.md`, so none depends on memory.

## The production boundary on this pick (this shapes the kit's guard)

The WordPress kit's release gate rests on one fact: pushing does not ship. [doc:~/Dev/clc-plugins/CLAUDE.md §9] On Forge the default is the opposite: push-to-deploy is on for new sites. [web:laravel.com/forge/docs/sites/deployments.md] So the boundary has to be built, and the second reader found three ways the obvious version leaks:

1. Forge API tokens are per user account with no documented per-server limit. **The agent holds no Forge token at all.**
2. By default Forge adds each server's key to the GitHub account, which gives the server access to every repository that account can reach. [web:laravel.com/forge/docs/ssh.md] **Untick that option and use a read-only deploy key per site.**
3. Whoever can push to the production branch can deploy production while push-to-deploy is on. **Turn push-to-deploy off for the production site. Gordon presses Deploy in Forge.** That restores the WordPress kit's shape exactly: Claude pushes the commit and the tag; Gordon's own action ships. Branch protection on GitHub would be a second lock, but for private repositories it needs a paid GitHub plan [web:docs.github.com/en/get-started/learning-about-github/githubs-plans]; which plan the Copper Leaf organisation is on is not on disk. Unconfirmed.

And: **no production SSH key and no production database credentials on the Mac.** Two servers, so the staging key opens staging only; this is stronger than the WordPress arrangement, where one staging key opens the whole hosting account. [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md §4]

## What would change the pick

- **"I never want to own a server."** Then Laravel Cloud, at about $15 a month, and four things change: the database becomes MySQL or Postgres (no SQLite) [web:laravel.com/cloud/docs/knowledge-base/sqlite.md]; PDFs need a different renderer [web:laravel.com/cloud/docs/knowledge-base/generating-pdfs.md]; the queue design follows Cloud's managed queues; and webhooks pass a firewall we cannot tune on the $5 plan, which Laravel itself warns can flag server-to-server calls. [web:laravel.com/cloud/docs/network.md] Cloud's scoped tokens are the cleanest agent boundary of any option. [web:laravel.com/cloud/docs/api/authentication.md] It is also the youngest product here.
- **"Cheapest possible."** Forge with two 1 GB Forge-billed servers is $24; the cost is that the production server cannot outlive the Forge subscription and its region is not published.
- **A different server provider.** Akamai (Linode) in Newark is the same price with a flat $2.50 backup add-on. Hetzner is out: it roughly tripled US prices on 2026-06-15 (the 2 GB plan went from $6.99 to $20.49). [web:docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/] Vultr is $2 cheaper; nothing was found against it and nothing for it on stability.

## Before committing (small, and mostly Gordon's to look at)

1. Does Gordon already have a Forge or DigitalOcean account? Nothing on disk says. [unconfirmed]
2. Which GitHub plan is the organisation on (branch protection for private repositories)? [unconfirmed]
3. In the Forge dashboard: which regions the Forge-billed staging server offers, and whether Hobby includes heartbeats and health checks. [unconfirmed at any public page]
4. Whether the app's hostname stays unproxied at Cloudflare (pick: yes at first).

## Also learned, useful later

- **Calendly retries failed webhooks for 24 hours with backoff, then disables the subscription.** Source is a Calendly employee's community post from 2023-12-14, not the developer docs, which could not be fetched. [secondary; unconfirmed at primary] A day-long failure therefore needs a monitor, because the subscription must be re-created by hand.
- **Laravel Vapor is closed to new signups.** [web:vapor.laravel.com] Evidence that Laravel does retire products; Forge is the one with a decade behind it.
- **PHP 8.5, not 8.4**, for a server built now: Forge has provisioned 8.5 by default since May 2026 and 8.4 leaves active support on 2026-12-31. [web:laravel.com/forge/docs/changelog.md] [web:php.net/supported-versions.php] This supersedes the "PHP 8.4" in `phase0-brief.md`.

## What was not verified

Nine of 227 claims could not be confirmed at a vendor page: Forge's annual prices; Forge-billed server regions; Forge object-storage price; how many sites a 1 GB server carries; whether Forge-billed servers have any server-level backup; the Railway and Upsun totals (estimates from rates); and whether SiteGround allows a resident worker. One claim was wrong (whether a Cloudflare container can open non-web ports: the docs imply yes) and one outdated (Cloudflare shipped per-Worker tokens on 2026-09-15). Neither changes a verdict.

## Sources

Cloudflare: developers.cloudflare.com/workers/languages/ · developers.cloudflare.com/changelog/post/2026-04-13-containers-sandbox-ga/ · developers.cloudflare.com/containers/faq/ · developers.cloudflare.com/containers/platform-details/workers-connections/ · developers.cloudflare.com/d1/reference/community-projects/ · blog.cloudflare.com/faster-agent-sandboxes/ · developers.cloudflare.com/bots/get-started/bot-fight-mode/ · developers.cloudflare.com/waf/custom-rules/skip/ · developers.cloudflare.com/tunnel/ · cloudflare.com/sase/products/access/ · developers.cloudflare.com/r2/pricing/

Laravel: laravel.com/forge/pricing · vps.forge.laravel.com/api/prices · laravel.com/forge/docs/servers/laravel-vps.md · laravel.com/forge/docs/servers/the-basics.md · laravel.com/forge/docs/servers/security.md · laravel.com/forge/docs/sites/deployments.md · laravel.com/forge/docs/ssh.md · laravel.com/forge/docs/resources/databases.md · laravel.com/forge/docs/knowledge-base/cve-2026-31431.md · laravel.com/forge/docs/server-providers.md · laravel.com/cloud/pricing · laravel.com/cloud/docs/pricing.md · laravel.com/cloud/docs/knowledge-base/sqlite.md · laravel.com/cloud/docs/knowledge-base/generating-pdfs.md · laravel.com/cloud/docs/network.md · laravel.com/cloud/docs/compute.md · laravel.com/cloud/docs/api/authentication.md · vapor.laravel.com

Servers: digitalocean.com/pricing/droplets · docs.digitalocean.com/products/backups/details/pricing/ · docs.digitalocean.com/platform/regional-availability/ · api.linode.com/v4/linode/types · api.vultr.com/v2/plans · docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/ · aws.amazon.com/lightsail/pricing/ · ubuntu.com/about/release-cycle

Platforms: docs.fly.io/about/pricing/ · docs.fly.io/volumes/overview/ · docs.fly.io/security/tokens/ · fly.io/news (2026-07-24) · status.flyio.net/history · docs.railway.com/reference/pricing/plans · docs.railway.com/reference/volumes · cloudways.com/en/pricing.php · docs.github.com/en/get-started/learning-about-github/githubs-plans

The full per-claim record (claim, page, verdict, correction) is in the workflow journal named in the frontmatter.
