---
name: WoA client roster evidence (v2 and v3)
type: doc
lobe: work
status: quarantine
description: Read-only extraction of every client entity in v2 and v3 with cited status, lead partner and role; evidence for batch B2, not yet confirmed by Gordon; nothing here is a fact until a client folder cites it
sources: ["[v2:work/dashboard.md]", "[v2:work/clients/]", "[v3:work/clients/]", "[derived: sancho subagent 2026-10-01]"]
---
# WoA / Copper Leaf client roster, extracted from gordon-os-v2 and jarvis-v3

Extraction date: 2026-10-01. Read-only evidence pass. Sources:

- Source A: `gordon-os-v2/work/dashboard.md` (dashboard last updated 2026-03-25, line 2). Cited as `[v2:work/dashboard.md:N]`.
- Source B: the 32 files in `gordon-os-v2/work/clients/*.md` whose frontmatter is `type: client` (33 counting the sync-conflict duplicate of Travis Crawford). Cited as `[v2:work/clients/<file>:N]`. Files typed `client-doc`, `document`, etc. (songtipper-*, tipelodeon-*, together-financial-*, aeo-*, lottoedge-*, comfort-masters-*) are not client entities and are noted only where they bear on a roster question.
- Source C: `jarvis-v3/work/clients/` (three folders: `precision-chiro`, `society-hill`, `travis-crawford-hvac`). Cited as `[v3:work/clients/<path>:N]`.

Everything below is what the files say. Anything I concluded rather than read is marked (inferred). All statuses are as of the files' own dates, which mostly stop between March and August 2026; nothing here is confirmed current.

---

## 1. Every client entity found (v2 `type: client` files)

Business key: WoA = Wizard of Ads; CLC = Copper Leaf Creative; PM = Press Managed (hosting/maintenance). "Live/former" is the file's own status field plus the latest dated marker in the file.

| Slug | Display name | Business (per evidence) | Live or former (evidence) | Lead partner (WoA) | Gordon's role | Industry / city | Sources |
|---|---|---|---|---|---|---|---|
| action-air | Action Air Plumbing & Septic (aka Action West) | WoA (tag `woa`) | Live: "Status is active"; dashboard Active; last updated 2026-03-30 | Craig Arthur | Digital: LSA, GBP, PPC, website rebuild, reporting; Craig runs the relationship | HVAC, plumbing, septic; Lubbock TX | [v2:work/clients/action-air.md:12,20,22,44,48,53,72], [v2:work/dashboard.md:16] |
| atlas-bio | Atlas Bio (DBA Take Five Supply) | CLC + PM (tags `clc`, `press-managed`) | Former: "Status is historical (no recent activity)"; latest dated item 2024-04-16 | none stated | Web/WooCommerce catalog build with Leah (inferred from key facts) | Lab supplies, serum; city not stated | [v2:work/clients/atlas-bio.md:9,25,26,32,35,77] |
| checkvet | CheckIN Vet / CheckOUT Vet / Marshall Pet Care | WoA (tag `woa`) | Live: "Status is active, post-Tara cleanup underway"; last updated 2026-04-06; dashboard "Disorganized" | Johnny Molson (history: Syre Klenke, Peter Nevland interim) | Digital: PPC, LSA, website, SEO; joined early summer 2025 | Veterinary; Sun Prairie WI | [v2:work/clients/checkvet.md:12,30,31,33,43,47,52,74], [v2:work/dashboard.md:14] |
| comfort-masters-dfw | Comfort Masters DFW | WoA (tag `woa`) | Live but flagged: "Status: Concern"; latest dated update 2026-04-16; dashboard "Concern" | Peter Nevland | Website, LSA, PPC oversight (with Luis Castaneda), digital infrastructure; not the lead | HVAC; Fort Worth TX | [v2:work/clients/comfort-masters-dfw.md:18,25,29,57,87,614,628], [v2:work/dashboard.md:17,42] |
| cult-your-brand | Cult Your Brand | CLC + PM (tags `clc`, `press-managed`) | Former: "Status is historical"; latest dated item 2023-11-13 | none stated | Web work; Jack Heald is a thinking partner more than a client | Marketing consulting; city not stated | [v2:work/clients/cult-your-brand.md:9,18,22,23,30,33,75] |
| david-genova | David Genova (Vestry Concerts, Wellmont Theater, NJ Event Space, Preservation Partners) | CLC + PM (tags `clc`, `press-managed`) | Former/unknown: "Status is historical (recordings from 2023-2025)"; body "Status: Unknown" | none stated | Built sites and custom WooCommerce subscription system; Leah invoices and supports | Events, entertainment; Montclair NJ | [v2:work/clients/david-genova.md:9,14,16,29,30,39,40,59] |
| dm-heating | D&M Heating & Air Conditioning | WoA (tag `woa`); self-originated, not WoA-referred | Live: "Status: Active"; last updated 2026-04-17; dashboard Active | None named as lead; dashboard says "Gordon (sole)"; Peter Nevland is strategist and final copy editor | Digital lead; single point of contact; writing with Peter's edits | HVAC; Milwaukee WI | [v2:work/clients/dm-heating.md:6-8,15,27,29,51,60,108], [v2:work/dashboard.md:18,43] |
| dragonfly-dpc | Dragonfly DPC ("Client Zero") | Venture (tag `venture`); not WoA, not CLC | Live, unpaid: "Status is active, no payment yet, proving the model"; latest dated item 2026-04-08; dashboard lists DPC Venture as "Strategic development" | none | Strategic partner and digital growth consultant, unpaid proof of concept | Direct primary care; Loveland CO | [v2:work/clients/dragonfly-dpc.md:9,20,21,29,38,52,103], [v2:work/dashboard.md:68,79] |
| duchess-and-mimi | Duchess & Mimi | Tagged both `woa` and `press-managed`; body says "WoA + Press Managed" | Former: "Status is historical (recording from 2023)" | none stated | One-page website build with Leah; Leah does monthly maintenance | Gift boutique; city unknown (Chicago area inferred by file) | [v2:work/clients/duchess-and-mimi.md:6,19,20,27,29,30,44] |
| epic-escape-game | Epic Escape Game | CLC + PM (tags `clc`, `press-managed`) | Former: "Status is historical (recording from March 2025)" | none stated | Built original site 2016; retaining maintenance/hosting; referred redesign out | Escape rooms; Greenwood Village CO | [v2:work/clients/epic-escape-game.md:6,10,14,19,24,25,34,35] |
| filmadelphia | Filmadelphia (Philadelphia Film Society) | CLC + PM (tags `clc`, `press-managed`) | Former/unknown: "Status is historical (recordings from 2023-2025)" | none stated | PM hosting on Site District (migrated from WP Engine) | Nonprofit film theaters; Philadelphia PA | [v2:work/clients/filmadelphia.md:6,8,17,22,23,32,33] |
| gammons-home-services | Gammons Home Services | PM only; explicitly Peter Nevland's WoA client, not Gordon's | Live: "Status: Active"; created and last updated 2026-03-29 | Peter Nevland (his client) | Press Managed hosting/maintenance only | Home services; city not stated | [v2:work/clients/gammons-home-services.md:6-8,12,13,17,22,25,26,27] |
| governors-art-show | Governor's Art Show | CLC + PM (body line; tags lack `clc` but say wordpress/hosting) | Former/unknown: "Status is historical (recording from April 2025)" | none stated | Website, SEO, hosting, technical maintenance | Annual art show; Loveland CO | [v2:work/clients/governors-art-show.md:6,8,14,23,24,33,34] |
| gulley-greenhouse | Gulley Greenhouse (Ground Lovers, Jeepers Creepers) | CLC + PM (tags `clc`, `press-managed`) | Conflicting: key_facts "Status is active" and "quiet, steady client"; body "Status: Unknown (historical recording)"; last updated 2026-03-29; new payment page March 2026 | none | Website, hosting, e-commerce, product data (with Leah) | Garden center, nursery; Loveland CO | [v2:work/clients/gulley-greenhouse.md:6,8,12,13,21,24,25,29,35] |
| happy-outlet | The Happy Outlet | WoA (tag `woa`) | Live: "Status is active with solid relationship"; last updated 2026-03-30; dashboard "Solid" | Rick Willis (Matt Willis also) | Supporting partner: website, reporting dashboard, Google Ads, LSA, GBP, AEO | Residential electrical; Reno NV | [v2:work/clients/happy-outlet.md:9,11,15,16,35,39,44,64], [v2:work/dashboard.md:13] |
| jane-brewer-precision-chiro | Precision Chiro Co. (Dr. Jane Brewer) | WoA since Oct 2025 and CLC/PM for 5+ years (tags `woa`, `press-managed`) | Live: "Status is active, long relationship, new WoA engagement"; last updated 2026-03-30; dashboard "New site launching"; v3 work dated 2026-06-03 | none stated; dashboard "Gordon (sole)" | WoA digital consultant; website and hosting under CLC/PM | Neurostructural chiropractic; Johnstown CO | [v2:work/clients/jane-brewer-precision-chiro.md:6,8,21,22,32,36,42,64,72-74], [v2:work/dashboard.md:21,66], [v3:work/clients/precision-chiro/_active/olivia-bio-final.md:5] |
| lake-day | Lake Day | Personal project (tag `personal-project`); not a client business | In planning: "Status is in planning"; no dates in file | none | Building the site himself | Personal event site; no city | [v2:work/clients/lake-day.md:6,8,17,22] |
| lottoedge | LottoEdge | WoA (tag `woa`) | Live: "Status is active"; last updated 2026-04-22; price change dated 2026-05-01; dashboard "Redesign in progress" | Gordon leads; Brian Brushwood is WoA partner consulting on audience | Lead, single-handing ~2 years: growth dashboard, funnel, newsletter, technical SEO, checkout, homepage | Lottery odds subscription; no city stated | [v2:work/clients/lottoedge.md:6-9,13,14,16,17,29,31,35,39,62], [v2:work/dashboard.md:20,33] |
| mitchells-magic | Mitchell's Magic (+ Cullins Heating & Air) | WoA (tag `woa`) | Live: "Status is active"; last updated 2026-03-30; latest dated item 2026-04-07; dashboard Active | Tom Wanek (took over from Peter Nevland) | Digital lead; brought in May 2024 | HVAC franchise; Cleveland and Columbus OH | [v2:work/clients/mitchells-magic.md:6-9,11,12,20,21,22,37,41,46,68], [v2:work/dashboard.md:15,39] |
| peacework | Peacework | Unknown; only recording is a misfiled family call | Unknown: "Status is unknown"; file recommends verifying the client exists | none | Unknown | Unknown | [v2:work/clients/peacework.md:6,8,12,14,24,41] |
| plunkett-home-services | Plunkett Home Services (formerly Tailored Mechanical) | WoA (tag `woa`), plus `press-managed` tag | Live: "Paid up and active as of April 2026"; last updated 2026-04-10; dashboard "Onboarding" (3/25) | Daniel Whittington (Dave Young also on account) | Supporting partner under Daniel's lead; LSA, Google Ads, site | HVAC, water treatment; Tucson AZ | [v2:work/clients/plunkett-home-services.md:9,11,13,17,18,22,23,40,44,49,66], [v2:work/dashboard.md:12,38] |
| racquet-depot | Racquet Depot | PM (tag `press-managed`) | Live: "Status is active"; created 2026-03-29; paid $1,000 March 2026 | none | PM hosting and maintenance; Leah handles resource issue | Racquet sports retail; city not stated | [v2:work/clients/racquet-depot.md:6,11,12,15,19,25,26] |
| service-professionals | Service Professionals | CLC + PM (tags `clc`, `press-managed`) | Former/unknown: "Status is historical (recording from July 2024)" | none stated (Vi Wickam is creative director) | Technical lead on WordPress build; Locations plugin | Home services; location unknown | [v2:work/clients/service-professionals.md:6-9,19,25,26,35,36] |
| sheridan-pubfactory | Sheridan PubFactory | CLC + PM (tags `press-managed`; body "CLC + Press Managed") | Former/unknown: "Status is historical (recording from Nov 2024)" | none | PM technical backend; troubleshooting | Publishing, printing; location unknown | [v2:work/clients/sheridan-pubfactory.md:6,8,13,18,19,28,29] |
| society-hill | Society Hill Plumbing | WoA (tag `woa`); v3 calls the 2026 site build a Copper Leaf Creative engagement | Live: "Status is active, one of Gordon's favorites"; last updated 2026-04-07; latest dated marker 2026-08-14; v3 kickoff 2026-06-11; dashboard "Active, favorite" | None; Gordon single-handing; Gordon Atkinson is WoA writer on payroll; Ryan Chute brought Greg in | Effectively single-handing: direct mail, B2B site, rebuild, membership | Plumbing; Philadelphia PA | [v2:work/clients/society-hill.md:9,11,16,17,19,20,44,48,53,70,75,300], [v2:work/dashboard.md:19,36], [v3:work/clients/society-hill/society-hill.md:3,10] |
| sportpro | SportPro | Unclear; WoA partner lead "unknown, needs confirming" | Live (assumed): "Status is active (assumed)"; created 2026-03-18 | unknown | Unknown; did spam audit, site fatal errors in March 2026 | Unknown industry; New York City | [v2:work/clients/sportpro.md:6,8,9,14,15,16,20,24] |
| straight-line-fitness | Straight Line Fitness Studio (file actually about Thriving Financial) | CLC + PM (tags `clc`, `press-managed`) | Former: "Status is historical (filing discrepancy)"; Keith and Shelley are ~20-year clients | none | Radio-to-video project for a financial advisory client (misfiled) | Financial advisory (per content); Fort Collins/Loveland CO | [v2:work/clients/straight-line-fitness.md:6,8,9,12,17,18,27,28] |
| travis-crawford | Travis Crawford HVAC / Plumbing / Electric | WoA (tag `woa`) | Live: "Status is active, tight-scope engagement"; last updated 2026-07-24; latest dated item 2026-08-05; v3 file status `active`, last meeting 2026-06-03; dashboard "Strong results" | Stephen Semple | Tightly scoped: 3 LSA accounts + Google PPC; not the lead | HVAC, plumbing, electrical; Charlotte NC | [v2:work/clients/travis-crawford.md:9,11,16,21,36,40,107,158,179], [v2:work/dashboard.md:22], [v3:work/clients/travis-crawford-hvac/travis-crawford-hvac.md:5,8-12,29] |
| travis-crawford-CONFLICT-1 | (duplicate of travis-crawford) | same | same | same | same | same | [v2:work/clients/travis-crawford-CONFLICT-1.md:1-40] |
| university-christian-church | University Christian Church | CLC + PM (tags `press-managed`; body "CLC + Press Managed") | Former/unknown: "Status is historical (recording from Nov 2024)"; two annual PM plans signed | none | PM hosting and maintenance; migrated two sites from WP Engine | Church; Fort Worth TX | [v2:work/clients/university-christian-church.md:6,8,13,14,17,24,25,34,35] |
| wy-real-estate-school | WY Real Estate School | CLC + PM (tags `clc`, `press-managed`) | Former: "Status is historical (no recent activity)"; latest dated item 2024-12-18 | none | Digital/web strategy; course selector | Real estate school; Cheyenne WY | [v2:work/clients/wy-real-estate-school.md:9,11,13,16,23,24,30,34,63] |
| wycares | WyCARES / Crossed Arrows Real Estate | CLC + PM (tags `clc`, `press-managed`) | Former/unknown: "Status is historical (recordings from 2024)" | none | PM hosting and website for both Rob Shank sites; course selector tool | Real estate brokerage/school; Cheyenne WY | [v2:work/clients/wycares.md:9,11,12,17,18,31,32,41,42] |
| zane-forshee | Zane Forshee (Art is a Real Job) | CLC + PM (tags `clc`, `press-managed`) | Former: "Status is historical (no recent activity)"; latest dated item 2025-05-02 | none | Website redesign (Marissa Ezell implementing) | Musician, educator; city not stated | [v2:work/clients/zane-forshee.md:6,8,11,12,20,21,28,31,74] |

Entities that appear in the clients folder only as documents, with no `type: client` file:

| Entity | What exists | Evidence |
|---|---|---|
| SongTipper, renamed Tipelodeon | 20+ `type: document` and `type: client-doc` files (business model, projections, partnership, ICP, pricing, character diamond). Rename to Tipelodeon locked 2026-05-07. Latest dated docs 2026-09-10. Dashboard treats it as a partnership (Gordon 15% sweat + capital equity), not a client. | [v2:work/clients/songtipper-ads-system.md:8], [v2:work/clients/tipelodeon-pricing-tiered-fee-2026-09.md:2-5,22], [v2:work/dashboard.md:23,34] |
| Together Financial Group (Thrivent practice, Loveland CO; lead advisor Andrew Flanscha) | Five `client-doc*` files (bios for Amy Hloucal and Beth Haley, dated 2026-04-16 to 2026-05-15); `parent_entity: together-financial-group` but no such client file. | [v2:work/clients/together-financial-amy-bio-edits-2026-04-16.md:4,7,11], [v2:work/clients/together-financial-beth-bio-final.md:4-6] |

Source C summary (jarvis-v3/work/clients):

| v3 folder | Name | Status | Last date in folder |
|---|---|---|---|
| precision-chiro | Olivia La bio drafts v1 to v4 plus final (`parent_entity: precision-chiro`) | final "gordon-final-awaiting-olivia-review" | 2026-06-03 [v3:work/clients/precision-chiro/_active/olivia-bio-final.md:5,6] |
| society-hill | Society Hill Plumbing client stub + publishing-stack buildout + hosting doc | Stub; buildout kickoff, hosting "provisioning pending"; "Copper Leaf Creative client. New website build" | 2026-06-11 [v3:work/clients/society-hill/society-hill.md:3,10], [v3:work/clients/society-hill/infra/hosting.md:3,9] |
| travis-crawford-hvac | Travis Crawford HVAC / Plumbing / Electric + competitor intel | `status: active`; created 2026-06-05 from the 6/03 team meeting | 2026-06-05 [v3:work/clients/travis-crawford-hvac/travis-crawford-hvac.md:5,28,29], [v3:work/clients/travis-crawford-hvac/competitor-intel-brothers.md:7] |

---

## 2. The dashboard's own roster, transcribed

WoA Client Roster, dashboard last updated 2026-03-25 [v2:work/dashboard.md:2,8-23]:

| Line | Client | Location | Industry | Lead Partner | Gordon's Role | Status |
|---|---|---|---|---|---|---|
| 12 | Plunkett Home Services | Tucson AZ | HVAC | Daniel Whittington | Support | Onboarding (yellow) |
| 13 | The Happy Outlet | Reno NV | Electrical | Rick Willis | Support | Solid (green) |
| 14 | CheckIN/OUT Vet + Marshall | Sun Prairie WI | Veterinary | Johnny Molson | Digital | Disorganized (red) |
| 15 | Mitchell's Magic + Cullins | Cleveland/Columbus OH | HVAC (franchise) | Tom Wanek | Digital | Active (green) |
| 16 | Action Air | Lubbock TX | HVAC/Plumbing/Septic | Craig Arthur | Digital | Active (green) |
| 17 | Comfort Masters DFW | Fort Worth TX | HVAC | Peter Nevland | Website + LSA | Concern (yellow) |
| 18 | D&M Heating | Milwaukee WI | HVAC | Gordon (sole) | Full digital | Active (green) |
| 19 | Society Hill Plumbing | Philadelphia PA | Plumbing | Gordon (sole) | Full digital | Active, favorite (green) |
| 20 | LottoEdge | (none) | Subscription/data | Gordon + Brushwood | Lead | Redesign in progress (yellow) |
| 21 | Jane Brewer / Precision Chiro | Johnstown CO | Chiropractic | Gordon (sole) | Full digital | New site launching (green) |
| 22 | Travis Crawford HVAC | Charlotte NC | HVAC/Plumbing/Electrical | Stephen Semple | LSA + PPC | Strong results (green) |
| 23 | SongTipper | (none) | Music/SaaS | Gordon (partner) | Marketing + Capital | Pre-launch partnership (yellow) |

Non-Client Businesses table [v2:work/dashboard.md:62-70]:

| Line | Entity | Status | Note (summarized) |
|---|---|---|---|
| 66 | Copper Leaf Creative | Legacy / de-emphasized | Web strategy/dev; outdated site; Jane Brewer remains active CLC client |
| 67 | Press Managed | Active / recurring | WP hosting + maintenance; full client list not yet captured |
| 68 | DPC Venture | Strategic development | Dragonfly DPC as Client Zero; revenue covering expenses, not yet paying salaries |
| 69 | American Icon Spirits | Active opportunity | Lizzie Mack's company; courting Gordon as CMO, equity TBD |
| 70 | Entomat (insect protein) | Stalled | Also Lizzie Mack; waiting on paperwork 12+ months |

Other dashboard lines that bear on the roster: Copper Leaf client tech refresh assumes "~40 Copper Leaf clients" [v2:work/dashboard.md:83]; "Press Managed client list: full roster unknown" [v2:work/dashboard.md:103]; 2026 growth moratorium, say yes only to warm referrals [v2:work/dashboard.md:56]; WoA recurring revenue $210K at 22 months as of 2026-03-18 [v2:work/dashboard.md:58].

---

## 3. Discrepancies

### 3a. In the dashboard but with no client file

1. **SongTipper** (dashboard line 23). No `type: client` file. Only documents, and the product was renamed Tipelodeon on 2026-05-07 with the file rename "deferred" [v2:work/clients/songtipper-ads-system.md:8]. The dashboard itself calls it a partnership with equity, not a client [v2:work/dashboard.md:23,34].
2. **Cullins Heating & Air** (dashboard line 15, 39) has no file of its own; it lives inside `mitchells-magic.md` as an alias [v2:work/clients/mitchells-magic.md:3].
3. **Marshall Pet Care** (dashboard line 14) likewise lives inside `checkvet.md` as an alias and a separate LLC [v2:work/clients/checkvet.md:3,34].
4. Non-client table entries **Press Managed**, **American Icon Spirits**, **Entomat** have no client files (there are `work/press-managed.md` and `work/entomat-*.md` files, not read for this pass).

### 3b. Client files with no dashboard roster line

- CLC/PM historical files, none on the dashboard: atlas-bio, cult-your-brand, david-genova, duchess-and-mimi, epic-escape-game, filmadelphia, governors-art-show, gulley-greenhouse, service-professionals, sheridan-pubfactory, straight-line-fitness, university-christian-church, wy-real-estate-school, wycares, zane-forshee (15 files). The dashboard says "~40 Copper Leaf clients" [v2:work/dashboard.md:83] and that the PM roster is unknown [v2:work/dashboard.md:103], so these 15 are a partial list at best.
- PM-only files marked active but absent from the dashboard: gammons-home-services, racquet-depot (both created 2026-03-29, four days after the dashboard's last update).
- Stubs with no business attribution: sportpro ("WoA Partner lead unknown" [v2:work/clients/sportpro.md:14]), peacework (possibly not a client at all [v2:work/clients/peacework.md:12,41]).
- lake-day is a personal project filed under clients [v2:work/clients/lake-day.md:6,8].
- dragonfly-dpc appears on the dashboard only indirectly under "DPC Venture" [v2:work/dashboard.md:68], not in the client roster.
- Together Financial Group has five bio documents and no client file; it is not on the dashboard. Its lead advisor is "Andrew Flanscha" in Loveland [v2:work/clients/together-financial-amy-bio-edits-2026-04-16.md:7]; `straight-line-fitness.md` describes a "Thriving Financial" practice with principal "Andrew" in Fort Collins/Loveland [v2:work/clients/straight-line-fitness.md:9,12]. Same entity, with "Thriving" a mishearing of "Thrivent" (inferred, unconfirmed).

### 3c. Conflicting status between sources

1. **Plunkett**: dashboard "Onboarding" as of 2026-03-25 [v2:work/dashboard.md:12]; file says "Paid up and active as of April 2026 (was onboarding March 2026)" [v2:work/clients/plunkett-home-services.md:23]. File is newer.
2. **CheckVET**: dashboard "Disorganized" (red) [v2:work/dashboard.md:14]; file (2026-04-06) says "active, post-Tara cleanup underway, leadership team stepped up" [v2:work/clients/checkvet.md:43,52]. LSA accounts "not set up" in both [v2:work/dashboard.md:30], [v2:work/clients/checkvet.md:36,89].
3. **Gulley Greenhouse**: internal conflict. Frontmatter "Status is active" [v2:work/clients/gulley-greenhouse.md:25] vs body "Status: Unknown (historical recording)" [v2:work/clients/gulley-greenhouse.md:35], with a dated March 2026 payment page [v2:work/clients/gulley-greenhouse.md:21].
4. **Society Hill**: v2 files it as a WoA client with Gordon single-handing [v2:work/clients/society-hill.md:9,70]; v3 files the 2026 website build as a "Copper Leaf Creative client" engagement [v3:work/clients/society-hill/society-hill.md:10]. Not necessarily contradictory (WoA marketing plus CLC site build), but the business attribution differs by source.
5. **Jane Brewer**: dashboard roster lists her as WoA [v2:work/dashboard.md:21] and the non-client table says she "remains active CLC client" [v2:work/dashboard.md:66]; file confirms both (WoA since Oct 2025, CLC/PM 5+ years) [v2:work/clients/jane-brewer-precision-chiro.md:21,22].
6. **D&M Heating**: dashboard "Gordon (sole)" as lead partner [v2:work/dashboard.md:18]; file names no lead partner but has Peter Nevland as WoA partner/strategist doing final copy edits [v2:work/clients/dm-heating.md:6-8,29]. Dashboard also says Elliott Stark onboarded as writer [v2:work/dashboard.md:43]; file says Elliott stepped off 2026-04-17 [v2:work/clients/dm-heating.md:29].
7. **Duchess & Mimi**: tagged `woa` [v2:work/clients/duchess-and-mimi.md:6] but historical (2023 recording) and not on the WoA roster. The WoA tag is unsupported by anything in the first 40 lines beyond the label itself.
8. **Dragonfly DPC**: file "Last updated: 2026-03-09" [v2:work/clients/dragonfly-dpc.md:33] but contains a dated entry 2026-04-08 [v2:work/clients/dragonfly-dpc.md:103]. Minor staleness of the header.
9. **Travis Crawford**: v2 file last updated 2026-07-24 with GA4 outage work [v2:work/clients/travis-crawford.md:40,44]; v3 file deliberately starts clean, "NOT a v2 import" [v3:work/clients/travis-crawford-hvac/travis-crawford-hvac.md:34]. Two parallel files for one client with no cross-sync.

### 3d. Duplicate entities / two names

1. **travis-crawford.md** and **travis-crawford-CONFLICT-1.md**: identical frontmatter and header; 318 vs 316 lines. A sync-conflict copy. Also a third copy in v3 (`travis-crawford-hvac`).
2. **wycares.md** vs **wy-real-estate-school.md**: both say they are separate businesses with the same owner Rob Shank [v2:work/clients/wy-real-estate-school.md:11], [v2:work/clients/wycares.md:11-12], but they disagree on which is the school: `wy-real-estate-school.md` says the school is wyrealestateschool.com and WyCARES is the brokerage [v2:work/clients/wy-real-estate-school.md:8,12]; `wycares.md`'s H1 expands WyCARES as "Wyoming Continuing and Real Estate School" and lists wycares.com as the school [v2:work/clients/wycares.md:35,38] while its own key facts say WyCARES is the brokerage at prostairsrealestate.com [v2:work/clients/wycares.md:11,13].
3. **jane-brewer-precision-chiro** (v2) vs **precision-chiro** (v3): same client, different slugs.
4. **travis-crawford** (v2) vs **travis-crawford-hvac** (v3): same client, different slugs.
5. **SongTipper / Tipelodeon**: one venture under two names; files use both prefixes [v2:work/clients/songtipper-ads-system.md:8].
6. **Straight Line Fitness / Thriving Financial / Together Financial**: one file named for a fitness studio whose content is about a financial advisory practice [v2:work/clients/straight-line-fitness.md:8,32], plus five Together Financial docs; likely one financial-advisory client under three labels (inferred).
7. **Plunkett Home Services / Tailored Mechanical / Happy Tucson**: one client, rebranded Feb 2026 [v2:work/clients/plunkett-home-services.md:3,13].
8. **Atlas Bio / Take Five Supply**: one client with a DBA [v2:work/clients/atlas-bio.md:3,16].

---

## 4. Profiles: the live Wizard of Ads clients

Criteria: on the dashboard WoA roster [v2:work/dashboard.md:12-22] AND the client file says active with a `woa` tag. Eleven clients. SongTipper/Tipelodeon is excluded because both sources call it a partnership, not a client [v2:work/dashboard.md:23,34]. Dragonfly, Gammons, Racquet Depot and SportPro are excluded because none is attributed to WoA with Gordon as partner.

### Action Air Plumbing & Septic (Lubbock TX)
Owned by Megan and Jordan Ohlmann; an HVAC, plumbing and septic company in Lubbock, family-owned since 1985 [v2:work/clients/action-air.md:14,16,17]. Craig Arthur, the first WoA Partner ever, is the lead partner and runs the relationship; Jason Skaggs is the writer [v2:work/clients/action-air.md:20,21,72]. Gordon's role is digital: LSA, Google Business Profile, PPC (added May 2025 at $600/month), website rebuild, heat-map tracking and reporting [v2:work/clients/action-air.md:22,33,72]. Gordon has been engaged at least since early 2025; April 2025 was the client's biggest month ever [v2:work/clients/action-air.md:23,80]. Status active; one of Gordon's favorite accounts [v2:work/clients/action-air.md:43,44], [v2:work/dashboard.md:16].

### The Happy Outlet (Reno NV)
Owned by Jesse Olson; a strictly residential electrical company serving Reno, Carson City, Gardnerville/Minden and Dayton, with 2024 revenue around $3 million [v2:work/clients/happy-outlet.md:11,14,17,32]. Rick Willis is the lead WoA Partner and crafts the radio; his son Matt Willis is also on the team [v2:work/clients/happy-outlet.md:15,53,54]. Gordon is the supporting partner: website, digital reporting dashboard, Google Ads, LSA, GBP and AEO strategy, and he contributes to brand strategy beyond pure digital [v2:work/clients/happy-outlet.md:16,64]. Rick and Matt have had the account about 18 to 19 months and Gordon about a year as of March 2026 [v2:work/clients/happy-outlet.md:71,72]. Status active with a solid relationship; another of Gordon's favorites [v2:work/clients/happy-outlet.md:34,35,44], [v2:work/dashboard.md:13].

### CheckIN Vet / CheckOUT Vet / Marshall Pet Care (Sun Prairie WI)
Owned by Dr. Marty Greer (Westminster Veterinarian of the Year) with husband Dan Greer; three veterinary brands in Sun Prairie and Marshall, Wisconsin, including the state's first drive-through vet clinic [v2:work/clients/checkvet.md:14-17,19,26,34]. Johnny Molson is the current lead WoA Partner after a messy history (Syre Klenke to Peter Nevland to Syre to Johnny) [v2:work/clients/checkvet.md:30,31,67-69]. Gordon joined in early summer 2025 in a digital role: PPC, LSA, website and SEO, replacing Charlie Moger's digital team [v2:work/clients/checkvet.md:32,33,74]. He built a custom podcast hosting plugin for Dr. Marty's podcast appearances [v2:work/clients/checkvet.md:38]. The dashboard rates the client "Disorganized" and overdue on LSA setup and branded PPC [v2:work/dashboard.md:14,30]; the file (2026-04-06) says active, with a leadership team stepping up after the practice manager was fired in April 2026 [v2:work/clients/checkvet.md:20,43,52].

### Mitchell's Magic + Cullins Heating & Air (Cleveland and Columbus OH)
Owned by Josh Bullock, with wife Danelle and daughter Brittany involved; a One Hour Heating & Air franchise in business 27+ years, Mitchell's in Cleveland and Cullins added in Columbus in 2026 [v2:work/clients/mitchells-magic.md:11,12,16,17,18,44]. Tom Wanek is the lead WoA Partner, having taken over after Josh asked Peter Nevland to step back [v2:work/clients/mitchells-magic.md:20,59,60]. Gordon is the digital lead, brought in May 2024 by Peter Nevland to replace Charlie Moger's team; the file calls it his longest-running active WoA digital account at about two years [v2:work/clients/mitchells-magic.md:21,22,68]. Josh pays $50K per year; the work spans LSA, PPC, CTV and a TV commercial shoot Gordon attended April 7 [v2:work/clients/mitchells-magic.md:23,27,31,35]. Status active [v2:work/clients/mitchells-magic.md:37,46], [v2:work/dashboard.md:15,39].

### Comfort Masters DFW (Fort Worth TX)
Owned by Stephen Moore, who founded it around 2011, with co-owner and wife Amanda Moore; an HVAC company in Fort Worth competing in one of the five toughest HVAC markets in the country [v2:work/clients/comfort-masters-dfw.md:20,23,24,44]. Peter Nevland is the lead WoA Partner; Jack Heald writes and Adam Donmoyer buys media [v2:work/clients/comfort-masters-dfw.md:25-27,70-72]. Gordon handles website, LSA, PPC oversight with Luis Castaneda, and all technical digital infrastructure, explicitly not as lead [v2:work/clients/comfort-masters-dfw.md:29,87]. The previous agency, Wit Digital, was terminated Dec 2024/Jan 2025, which bounds Gordon's tenure at roughly a year as of early 2026 (inferred) [v2:work/clients/comfort-masters-dfw.md:32]. Status is "Concern": 2022 peak of $4.5M, flat since, and two tough weather years [v2:work/clients/comfort-masters-dfw.md:34,35,57], [v2:work/dashboard.md:17,42]; the file's latest dated entry is a 2026-04-16 keyword deliverable [v2:work/clients/comfort-masters-dfw.md:614].

### D&M Heating & Air Conditioning (Milwaukee WI)
Owned by Karen Sartler (primary), Jeff and Tim, who bought it from Karen's father; a heating-and-cooling-only HVAC company in Milwaukee, family-owned since 1979 [v2:work/clients/dm-heating.md:17,19,23,24,26]. This is Gordon's self-originated account, not WoA-referred: Karen found WoA through Vi Wickam's CapitalHVAC site footer [v2:work/clients/dm-heating.md:27,28,113]. Gordon is the digital lead and single point of contact; the dashboard lists him as sole lead partner [v2:work/clients/dm-heating.md:108], [v2:work/dashboard.md:18]. Peter Nevland is the WoA strategist on the account and does final copy edits; Adam Donmoyer buys media and Nathan Ingram is rebuilding the website on a $7,500 budget [v2:work/clients/dm-heating.md:6-8,29,30,31]. Tenure is not stated as a start date in the file. Status active; last updated 2026-04-17 [v2:work/clients/dm-heating.md:51,60], [v2:work/dashboard.md:43].

### Society Hill Plumbing (Philadelphia PA)
Owned by Greg Moore, a Master Plumber and former government employee who named the company for upscale connotations; a Philadelphia plumbing company with a city contract and about 25% direct-to-consumer revenue [v2:work/clients/society-hill.md:11,14,23,24,27]. Ryan Chute brought Greg into WoA; Gordon Atkinson is the WoA writer on payroll but underutilized, and Gordon is effectively single-handing the account [v2:work/clients/society-hill.md:16,17,19,70]. The work includes the idigforplumbers.com B2B excavation site Gordon built, a seven-postcard Monet direct-mail series, a free flapper campaign and a planned rebuild of the main site [v2:work/clients/society-hill.md:12,29,30,32]. The engagement started July 2025 and Gordon wants to use it as his working example for the AWG course [v2:work/clients/society-hill.md:20,33,75]. Status active and one of Gordon's favorites [v2:work/clients/society-hill.md:21,44,53], [v2:work/dashboard.md:19,36]; the v3 tree picked the site rebuild up as a Copper Leaf Creative build on 2026-06-11 [v3:work/clients/society-hill/society-hill.md:3,10].

### LottoEdge (no city stated)
Owned by founder Jared James, a career accountant; a subscription website selling lottery scratch-off odds data, with about 2,100 subscribers as of March 2026 [v2:work/clients/lottoedge.md:11,13,21]. Gordon is the lead and single-handed the account for about two years before Brian Brushwood, a WoA Partner, joined in late 2025/early 2026 to consult on audience building [v2:work/clients/lottoedge.md:6-8,14,16,62]. Gordon runs the growth dashboard, conversion funnel, technical SEO, checkout flow, homepage redesign and alternates writing the Thursday newsletter with Jared [v2:work/clients/lottoedge.md:27,28,62]. WoA's fee is 1% of revenue quarterly plus kickers [v2:work/clients/lottoedge.md:18]. The file calls it the longest-running active client at 2+ years as of March 2026 [v2:work/clients/lottoedge.md:17]. Status active; a price increase to $5.95/month took effect 2026-05-01 [v2:work/clients/lottoedge.md:29,31,39], [v2:work/dashboard.md:20,33].

### Precision Chiro Co. / Dr. Jane Brewer (Johnstown CO)
Owned by Dr. Jane Brewer, one of fewer than 100 chiropractors worldwide with the DCCJP credential; a neurostructural, upper-cervical chiropractic practice in Johnstown serving Loveland and Fort Collins [v2:work/clients/jane-brewer-precision-chiro.md:8,10,11,12,13]. Gordon has known her 10+ years, has hosted her site under CLC and Press Managed for 5+ years, and became her WoA digital consultant in October 2025 [v2:work/clients/jane-brewer-precision-chiro.md:15,21,22,64,71-74]. No lead partner is named; the dashboard lists Gordon as sole, full digital [v2:work/dashboard.md:21]. The current work is a new site launching from SiteDistrict dev, and in v3 a bio for associate Dr. Olivia La finalized 2026-06-03 [v2:work/clients/jane-brewer-precision-chiro.md:9,30], [v3:work/clients/precision-chiro/_active/olivia-bio-final.md:5]. Status active; the only chiropractic/medical client in the WoA roster outside the DPC venture [v2:work/clients/jane-brewer-precision-chiro.md:31,32,42].

### Travis Crawford HVAC / Plumbing / Electric (Charlotte NC)
Owned by Travis Crawford, who founded it in 2009; a multi-trade home services company in Charlotte with a $17M annual target for 2026 [v2:work/clients/travis-crawford.md:11,15], [v3:work/clients/travis-crawford-hvac/travis-crawford-hvac.md:49]. Stephen Semple is the lead WoA Partner and brought Gordon in with a specific scope; Mick and Chris Torbay are the account team and Kyle Caldwell buys media [v2:work/clients/travis-crawford.md:16-19,167]. Gordon's role is tightly scoped: babysitting three LSA accounts and Google PPC, where he turned off all non-branded campaigns and freed about $250K for radio [v2:work/clients/travis-crawford.md:21,22,179,185-189]. A start date is not stated in either file. Status active with strong results in v2 (last updated 2026-07-24, after a GA4 tracking outage) and `active` in v3 with a last meeting of 2026-06-03 [v2:work/clients/travis-crawford.md:36,40,158], [v3:work/clients/travis-crawford-hvac/travis-crawford-hvac.md:5,29], [v2:work/dashboard.md:22].

### Plunkett Home Services (Tucson AZ)
Owned by Chris Plunkett, who founded it in 2013, with wife Scarlett as ops manager; an HVAC, water treatment and water heater company serving Tucson, Oro Valley and Green Valley, rebranded from Tailored Mechanical in February 2026 [v2:work/clients/plunkett-home-services.md:11,13,15,16,19]. Daniel Whittington, Chancellor of Wizard Academy and Gordon's friend, is the lead WoA Partner, with Dave Young also on the account [v2:work/clients/plunkett-home-services.md:17,18,59,60]. Gordon is the supporting partner under Daniel's lead, handling the site, LSA and Google Ads during a simultaneous WoA onboarding and rebrand [v2:work/clients/plunkett-home-services.md:9,22,35,66]. The digital onboarding call was 2026-03-05; Chris signed for $5K WoA plus $5K radio [v2:work/clients/plunkett-home-services.md:24,37,73]. Dashboard shows onboarding as of 3/25; the file shows paid up and active as of April 2026 [v2:work/dashboard.md:12,38], [v2:work/clients/plunkett-home-services.md:23,40,49].
