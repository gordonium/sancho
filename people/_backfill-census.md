---
name: People backfill census
type: doc
lobe: both
status: quarantine
description: Every person found in the Sancho tree, v2 relationships/people and work/partners, and v3 memory/people, one row each with where they appear; the work list for the backfill-people job (2026-10-01); not facts, pointers
sources: ["[doc:people/]", "[doc:work/]", "[v2:relationships/people/]", "[v2:work/partners/]", "[v3:memory/people/]", "[derived: sancho subagent 2026-10-01]"]
---
# People backfill census

Pointers only: name, aliases, role word and where each person appears. Nothing here is a fact until a `people/<slug>.md` cites it. `in_sancho` = existing file (yes/thin/no) and what references the person. `v2` = file name under `relationships/people/` or `partners/<name>.md` under `work/partners/`; "MANIFEST.md row" = listed in v2's roster index without a file. `v3` = folder under `memory/people/`. `kind` is what the evidence says; `(inferred)` marks a guess. `priority`: 1 = referenced in the Sancho tree already, 2 = live client or partner in v2/v3, 3 = everything else. `status` and `needs_gordon` are for the job to fill.

| slug | name | aliases | in_sancho | v2 | v3 | kind | priority | status | needs_gordon | note |
|---|---|---|---|---|---|---|---|---|---|---|
| adam-donmoyer | Adam Donmoyer | Adam | no; entity.md + knowledge.md comfort-masters-dfw, dm-heating | adam-donmoyer.md | no | WoA media buyer | 1 | done | yes | 2026-10-01: new file, 21 cited lines; sources: v2 people (adam-donmoyer, jack-heald, steven-moore, gene-vann), v2 clients (comfort-masters-dfw, dm-heating), v2 dashboard, Sancho entity files, rec_36f02fd22c; no v3; no contact details found; asks Gordon whether the "Adam" in rec_36f02fd22c is him |
| albert-plunkett | Albert |  | no; knowledge.md plunkett-home-services (wrap installer) | no | no | vendor (inferred) | 1 | folded | yes | surname not given. 2026-10-01: new file, 8 cited lines; sources: v2 client file plunkett-home-services (line 28 is the only mention), Sancho knowledge.md; no v2 people/partners file, no v3, nothing in _CLIENTS/Plunkett, no recordings; no contact details found; asks Gordon whether Albert and Calvert (`calvert-plunkett`) are one person |
| alex-post | Alex Post | Alex, Alexandra, Andrea | yes (thin); people/alex-post.md; work/tipelodeon/summaries/2026-09-15_rec_0d8753ed18.md | alex-post.md; MANIFEST.md row | alex-post (voice profile only) | friend | 1 | done | yes | v2 gives legal name Andrea. 2026-10-01: existing file thickened, 55 cited lines added, 3 existing lines kept; sources: v2 people (alex-post, lily-post, brent-ballard, ali-woll, paula-bernander, laura-holden, mark-benn, tom-boldt, MANIFEST), v2 client file prime-directive, v3 voice profile (enrollment history only), _CLIENTS/Prime Directive Counseling (listing), rec_640701d84d, rec_0d8753ed18; no contact details found; asks Gordon: which year the reconnection coffee was (v2 dates contradict), where things stand with Jake, and whether rec_868fb07db8 (inbox, closely held material) is filed here or in Private |
| alicia-mitchells-magic | Alicia |  | no; entity.md + knowledge.md mitchells-magic | no | alicia (voice profile only) | client person (marketing coordinator) | 1 | folded |  | surname not given |
| allie-wickham | Allie Wickham | Allie | no; recordings/2026/rec_640701d84d/summary-personal.md ("Allie & Mike's wedding") | allie-wickham.md; MANIFEST.md row | no | friend | 1 |  |  | v2 flags Ali Woll vs Allie Wickham as a voice-to-text disambiguation risk; fiance Mike has no file |
| amanda-moore | Amanda Moore | Amanda | no; entity.md + knowledge.md comfort-masters-dfw | amanda-moore.md | no | client person (Comfort Masters co-owner) | 1 | done | yes | 2026-10-01: new file, 51 cited lines; sources: v2 people (amanda-moore, steven-moore, adam-donmoyer, jack-heald, peter-nevland, gene-vann, MANIFEST), v2 clients (comfort-masters-dfw, whitespark-keywords, aeo-strategy, content-map), Sancho entity + knowledge files and stephen-moore.md, _CLIENTS/comfortmastersdfw (listing only), rec_1dc87f7565; no v3, no v2 partners; no contact details found; asks Gordon whether SPEAKER_04 in rec_1dc87f7565 is her; open: co-owner vs office manager title in v2, "Amanda" in the CSR list |
| andrew-mccanse | Andrew McCanse | Dr. Andrew McCanse | no; knowledge.md precision-chiro | no | no | client-adjacent (Vermont practice) | 1 | folded |  |  |
| brian-brushwood | Brian Brushwood | Brian, Brushwood, shwood | no; knowledge.md travis-crawford-hvac (referenced, not on the account); work/wizard-of-ads/clients/_roster-evidence-v2.md (LottoEdge) | partners/brian-brushwood.md | brian-brushwood (voice profile only) | WoA partner | 1 | done | yes | 2026-10-02: new file, 56 cited lines; sources: v2 partners (brian-brushwood), v2 clients (lottoedge, lottoedge 2026-04-21 and 2026-05-05 meetings, lottoedge-ice-pick, lottoedge-voice-profile, travis-crawford, songtipper-partnership-notes, songtipper-brushwood-comp-model), v2 dashboard, v2 people (jared-james, grayson-ehrhardt), v2 contacts-merge-validation, v3 voice profile (enrollment history only), v3 work/tipelodeon and scratch notes, rec_c7110cf37e, Sopris locations list, _CLIENTS LottoEdge (listing only); no v2 people file; contact field left empty; asks Gordon: is the 2023 Sopris address (Austin) current, and where Brian stands on LottoEdge now it is retired; open: LottoEdge start month (Oct 2025 vs "late 2025/early 2026"), whether the Tipelodeon advisor offer was ever made, bonnie-brushwood has no row; not read: v2 LottoEdge email dump and ~37 legacy earballs transcripts naming him (outside the skill's paths) |
| brittany-mitchells-magic | Brittany Bullock | Brittany, Bernie (transcript error) | no; entity.md + knowledge.md mitchells-magic | no | brittany-bullock (voice profile only) | client person | 1 | folded |  | v3 gives surname Bullock; Sancho slug could become brittany-bullock |
| calvert-plunkett | Calvert |  | no; knowledge.md plunkett-home-services (vehicle-wrap production) | no | no | vendor (inferred) | 1 | folded |  | surname not given |
| carmyn-wilson | Carmyn Wilson | Carmyn, Colin (former name) | no; recordings/inbox/rec_564c0541a8/summary.md and corrections.md | carmyn-wilson.md | carmyn-wilson (voice profile only) | WoA partner; friend | 1 | done | yes | 2026-10-02: new file, 53 cited lines; sources: v2 people (carmyn-wilson, adrian-van-zelfden), v2 client file service-professionals, v2 speaker-profiles, earballs-ingest-progress, personal/action-items, 10 v2 earballs transcripts (2025-08-25 to 2026-04-03; name-matched lines only, machine speaker labels), v3 voice profile (enrollment history only) and memory index, 11 v3 transcripts (2026-03-25 to 2026-08-05; name-matched lines only), rec_564c0541a8 with its summary and corrections, laravel-kit-spec (GitHub collaborator `carmynwilson`, by name only); no v2 partners file, no v3 person profile, no _CLIENTS folder (not a client's person); contact field left empty; asks Gordon: confirm the spelling Carmyn (every transcript hears Carmen), whether her partner paperwork closed and which accounts she is on, and which year she left Vi's employ (v2 dates conflict); open: v2 "Carmyn Wickam" credit on a persuasion PDF (blend with Vi Wickam or another person), a child "Carmen" in a v3 2026-08-27 transcript read as a different person; not read: ~30 further legacy transcripts naming Carmen once or twice and the bodies of rec_dd36abdf0f, rec_02926ce570, rec_0f41cfd425 beyond cited lines; v2 tools/standing-rules.md names her and was refused by rule |
| charlie-moger | Charlie Moger |  | no; knowledge.md checkvet, mitchells-magic (previous digital team) | no | no | vendor (inferred) | 1 | folded |  |  |
| chelsea-entomat | Chelsea |  | no; work/entomat/business.md (family foundation contact) | no | no | venture contact (inferred) | 1 | folded |  | surname not given; a different Chelsea (Ullman) appears in v2 kay-ullman.md |
| chris-comfort-masters | Chris |  | no; knowledge.md comfort-masters-dfw (technician) | no | no | client person | 1 | folded |  | surname not given |
| chris-noco-sportscenter | Chris |  | no; knowledge.md precision-chiro (NoCo SportsCenter marketing director) | no | no | client-side contact | 1 | no-folder |  | surname not given; Chris, marketing director at NoCo SportsCenter; no NoCo SportsCenter client folder (already listed in precision-chiro/knowledge.md People as Jane's sponsorship contact) |
| chris-plunkett | Chris Plunkett | Chris | no; entity.md + knowledge.md plunkett-home-services | no | no | client person (Plunkett owner) | 1 | done | yes | 2026-10-02: new file, 42 cited lines; sources: v2 client file plunkett-home-services, v2 partners (dave-young, daniel-whittington, robin-kressbach), v2 dashboard, Sancho entity + knowledge files and roster evidence, _CLIENTS/_Wizards of Ads CLIENTS/Plunkett (listing; signed MSA is a scan, not re-read this pass); no v2 people file, no v3 people folder, no Sancho recordings; contact field left empty (v2 gives an email with no stated source); asks Gordon to confirm that email; open: Craig vs Robin as the speaker offering creative input on the 2026-04-06 call, nothing naming him after 2026-04-10, 20 legacy earballs transcripts mentioning Plunkett not read (outside the skill's paths) |
| chris-torbay | Chris Torbay |  | no; entity.md + knowledge.md travis-crawford-hvac | no | chris-torbay (voice profile only) | WoA writer | 1 | done | yes | 2026-10-02: new file, 34 cited lines; sources: rec_c7110cf37e (Roy on the mining-video exemption), Sancho entity + knowledge files travis-crawford-hvac and business.md, v2 client file travis-crawford, v2 earballs transcript 2026-04-03, v3 client files (travis-crawford-hvac, competitor-intel-brothers), v3 scratch note 2026-08-18, v3 voice profile (enrollment history only), 6 v3 earballs transcripts (2026-04-01 to 2026-08-19; name-matched lines, machine speaker labels), _CLIENTS/traviscrawfordhvac.com (listing only); no v2 people or partners file; v3 _dmz import not read (never-read list); no contact details or location found; asks Gordon whether Chris is a WoA partner in his own right and where he is based |
| christy-secoy | Christy Secoy |  | no; entity.md + knowledge.md mitchells-magic | no | no | client person (office/admin) | 1 | folded |  |  |
| clarissa-dm-heating | Clarissa |  | no; entity.md + knowledge.md dm-heating | clarissa-dm-heating.md | no | client person (former front desk) | 1 | folded |  | surname not given |
| cody-travis-crawford | Cody |  | no; knowledge.md travis-crawford-hvac ("electronic guy next door") | no | no | client-side contact | 1 | folded |  | surname not given |
| craig-arthur | Craig Arthur | Craig | no; entity.md + knowledge.md action-air; knowledge.md plunkett-home-services names a "Craig (surname not given)" on the 2026-04-06 call | partners/craig-arthur.md | no | WoA partner | 1 | done | yes | the Plunkett "Craig" may be the same person; unconfirmed. 2026-10-02: new file, 41 cited lines; sources: v2 partners (craig-arthur), v2 clients (action-air, plunkett-home-services), v2 dashboard, gordon-professional, frontmatter-review, 8 v2 earballs transcripts (2025-08-25 to 2026-03-13; name-matched lines only, machine speaker labels), 6 v3 earballs transcripts (2026-03-13 to 2026-08-07; name-matched lines only), Sancho entity + knowledge files action-air and plunkett-home-services, business.md, chris-plunkett.md, _CLIENTS actionairlubbock.com (the two Feb 2025 distribution forms read; rest listing only) and Plunkett (listing); no v3 people folder, no Sancho recordings; no contact details found; asks Gordon whether the Plunkett "Craig" is Craig Arthur (a v3 recording of 2026-04-27 has Gordon saying he is on that team; machine label) |
| dan-griffiths | Dan Griffiths | Daniel Griffiths, Dan Greer (v2 error) | no; entity.md + knowledge.md checkvet | no | no | client person (CheckVet co-owner) | 1 | done | yes | v2 wrote the surname as Greer; the signed MSA has Griffiths per knowledge.md. 2026-10-01: new file, 19 cited lines; sources: v2 client file checkvet (the only legacy file naming him), Sancho entity + knowledge files and roster evidence, _CLIENTS/Check In and Out Vet (listing; signed MSA is a scan, not re-read this pass); no v2 people/partners file, no v3, no recordings; no contact details found; asks Gordon to confirm the surname Griffiths |
| danelle-bullock | Danelle Bullock | Danelle, Danelle Bulloch (v2 Zoom log spelling) | no; entity.md + knowledge.md mitchells-magic | no | no | client person | 1 | done | yes | 2026-10-01: new file, 29 cited lines; sources: v2 client file mitchells-magic (the only legacy file naming her), Sancho entity + knowledge files and roster evidence, rec_b24483399a (inbox, speakers unconfirmed), _CLIENTS/_Wizards of Ads CLIENTS/mitchellsmagic (listing; no document names her); no v2 people/partners file, no v3; contact field left empty (a Gmail address in v2 comes from a Zoom transcript, spelling unverified); asks Gordon: surname Bullock vs Bulloch, and whether the "Danelle" on the 2026-09-22 call is her; open: whether she holds ownership, "Ashley" has no file or census row |
| daniel-whittington | Daniel Whittington | Daniel | no; entity.md + knowledge.md plunkett-home-services | partners/daniel-whittington.md | daniel-whittington (voice profile only) | WoA partner; friend | 1 |  |  |  |
| dave-young | Dave Young | Dave | no; entity.md + knowledge.md plunkett-home-services | partners/dave-young.md | no | WoA partner | 1 |  |  |  |
| david-comfort-masters | David |  | no; knowledge.md comfort-masters-dfw (video producer) | no | no | vendor (inferred) | 1 | folded |  | surname not given |
| david-mckinnis | David McKinnis | David McInnis | no; knowledge.md plunkett-home-services (Newsworthy.ai founder) | MANIFEST.md row as "David McInnis" (PRWeb founder; no file) | no | vendor / Wizard Academy donor (inferred) | 1 |  |  | spelling differs between Sancho (McKinnis) and v2 MANIFEST (McInnis); likely one person, unconfirmed |
| devin-wright | Devin Wright | Devin | no; entity.md + knowledge.md action-air; knowledge.md mitchells-magic; knowledge.md checkvet names a "Devin, radio buyer" | no | no | WoA media buyer | 1 |  |  | the CheckVet "Devin" may be the same person; unconfirmed |
| dirk-dm-heating | Dirk |  | no; knowledge.md dm-heating (Carrier rep) | no | no | vendor (inferred) | 1 | folded |  | surname not given |
| doug-huckaba | Doug Huckaba | Doug | yes (thin); people/doug-huckaba.md; work/tipelodeon/summaries/2026-09-15_rec_21434802cb.md | doug.md (first name only, flooring crew) possibly the same person | no | friend | 1 |  |  | v2 doug.md is first-name only; same person unconfirmed |
| dr-hepworth | Dr. Hepworth |  | no; entity.md + knowledge.md precision-chiro | no | no | client referral contact (surgeon) | 1 | folded |  | first name not given |
| dr-johnson-checkvet | Dr. Johnson |  | no; knowledge.md checkvet (Marshall) | no | no | client person (veterinarian) | 1 | folded |  | first name not given |
| dr-scheller | Dr. Scheller |  | no; knowledge.md checkvet | no | no | client person (veterinarian) | 1 | folded |  | first name not given |
| dustin | Dustin |  | no (pending request to create); rec_0b2f65c077/speakers.md human-confirmed 2026-10-01; knowledge.md dm-heating technicians list | no | no | client person (D&M staff) | 1 | folded |  | surname not given; speakers.md slug is dustin, client-staff convention would be dustin-dm-heating |
| elliott-stark | Elliott Stark | Elliott | no; entity.md + knowledge.md dm-heating | elliott-stark.md (auto stub); partners/elliott-stark.md | elliott-stark (profile.md stub + voice profile) | WoA partner (writer) | 1 |  |  | three legacy files for one person |
| erica-comfort-masters | Erica |  | no; knowledge.md comfort-masters-dfw | no | no | client person (CSR) | 1 | folded |  | surname not given |
| etieno-essien | Etieno Essien | Eti, Eddie (misheard), Edi (v2 spelling) | no; work/entomat/business.md; personal/me/brief.md; recordings/lexicon.md | edi.md (name given only as Edi) likely the same person | no | venture (Entomat partner) | 1 |  |  | LIKELY DUPLICATE of v2 edi.md (Entomat scientist); unconfirmed |
| evan-mitchells-magic | Evan |  | no; knowledge.md mitchells-magic (TV producer) | no | no | vendor (inferred) | 1 | folded |  | surname not given |
| george-mitchells-magic | George |  | no; knowledge.md mitchells-magic (WoA partner on the account; surname unknown) | no | no | WoA partner | 1 | folded |  | surname unknown |
| gordon | Gordon Seirup | Gordon, Gordonium, Gordo | yes (thin); people/gordon.md | gordon-seirup.md (pointer to v2 CORE.md) | gordon (voice profile only) | principal | 1 |  |  | v2 adds alias Gordo |
| gordon-atkinson | Gordon Atkinson | Atkinson | no; entity.md + knowledge.md society-hill-plumbing | partners/gordon-atkinson.md; MANIFEST.md row | no | WoA partner (writer) | 1 |  |  | not to be confused with gordon (Seirup) |
| grayson-erhard | Grayson Erhard | Grayson, Erhard, Grayson Ehrhardt | yes (full); people/grayson-erhard.md; work/tipelodeon; personal/ice/ice-2026-10-01-camping-with-grayson.md | grayson-ehrhardt.md; grayson.md (auto stub) | no | venture (Tipelodeon) | 1 |  |  | v2 spells the surname Ehrhardt; Sancho and lexicon use Erhard; grayson.md stub is the same person |
| greg-moore | Greg Moore | Greg, Gregg (folder-name spelling in _CLIENTS) | no; entity.md + knowledge.md society-hill-plumbing | no | no | client person (Society Hill owner) | 1 | done | yes | 2026-10-01: new file, 75 cited lines; sources: v2 client files (society-hill, greg-voice-profile, meet-greg FINAL, uncovery extraction 2026-06-10), v2 handoff 2026-06-11, v2 partners/gordon-atkinson, v2 retreat agenda, v3 client stub society-hill, v3 legacy transcripts (8, speakers unconfirmed), Sancho entity + knowledge + guidelines, _CLIENTS/_Wizards of Ads CLIENTS/societyhillplumbing (listing, about-us.html, build-decisions, handoff-to-mac; the signed PDF could not be opened this pass); no v2 people/partners file, no v3 people folder, no Sancho recording; contact: phone only, from documents; asks Gordon: Greg vs Gregg spelling, and two contradictions only Greg can settle (2 or 4 years with the excavator; 35+ or 40 years a Master Plumber); open: other Gregs in the legacy transcripts kept apart, whether the new site has launched |
| isaac | Isaac | Iggy (lexicon) | no (pending people/isaac.md); recordings/inbox/rec_564c0541a8/summary.md (Ignite owner, Mankato MN); recordings/lexicon.md | no | no | client person (Ignite; CLC web-maintenance client per the summary) | 1 | no-folder |  | surname not given; pending request uses slug isaac; client folder home (copper-leaf vs wizard-of-ads) undecided; Isaac, owner and contact at Ignite HVAC (Copper Leaf client per Gordon's moderation); no Ignite client folder yet, goes into its knowledge.md when created |
| jack-heald | Jack Heald | Jack | no; entity.md + knowledge.md comfort-masters-dfw | jack-heald.md; partners/jack-heald.md | no | WoA partner (writer) | 1 |  |  | two v2 files (people and partners) |
| jaden-lewis | Jaden Lewis | Jay Lewis | no; knowledge.md comfort-masters-dfw | no | no | client person (CSR) | 1 | folded |  |  |
| jake-williams | Jake Williams | Jake | no; recordings/inbox/rec_564c0541a8/summary.md ("Jake", inferred to be Jake Williams) | MANIFEST.md row only (no file) | no | WoA (president) (inferred) | 1 |  |  | identity of the "Jake" in rec_564c0541a8 is inferred from the v2 MANIFEST role; unconfirmed |
| james-gilbert | James Gilbert | James | yes (thin); people/james-gilbert.md | james-gilbert.md | no | friend | 1 |  |  | v2 names a partner Felix in the first lines (see felix row) |
| jane-brewer | Jane Brewer | Dr. Jane Brewer | no; entity.md + knowledge.md precision-chiro | no (v2 has a client entity jane-brewer-precision-chiro, not a person file) | no | client person (Precision Chiro owner); CLC-PM client | 1 | done | yes | 2026-10-01: new file, 75 cited lines; sources: v2 client files (jane-brewer-precision-chiro, jane-brewer-stay-sharp-stand-tall), v2 dashboard, copper-leaf-creative, press-managed, presentation-frameworks, gordonos-v3-planning, v2 people (lizzie-mack, MANIFEST row), v3 client folder precision-chiro (olivia-bio-final, olivia-bio-draft-v1), Sancho entity + knowledge + guidelines, people/_sopris-locations.md, _CLIENTS/_Wizards of Ads CLIENTS/Precision Chiropractic (listing; no document opened this pass); no v2 people/partners file, no v3 people folder, no Sancho recording; contact field left empty (the only phone and address found are the practice's); asks Gordon: whether the Sopris-list "Jane Brewer" (Fort Collins, 2023) is her and current, and which month the Trish notice / Wes's mother's death / Leo fell in (v2 says early March 2026 and also logs them in a 2026-02-04 call); open: front desk start dates, Feb 2026 trip length, annual revenue, "Ashley" vs Olivia |
| jane-fisher | Jane Fisher |  | no; entity.md + knowledge.md dm-heating | no | no | media buyer (local) | 1 | folded |  |  |
| jared-james | Jared James | Jared | no; work/wizard-of-ads/clients/_roster-evidence-v2.md (LottoEdge) | jared-james.md | no | client person (LottoEdge founder) | 1 | done | yes | 2026-10-01: new file, 56 cited lines; sources: v2 people (jared-james), v2 partners (brian-brushwood), v2 clients (lottoedge, 2026-04-21 / 2026-05-05 / 2026-07-02 meeting files, ice-pick sheet), v2 dashboard, five v2 exported emails, v3 tipelodeon notes (2026-07-16), _CLIENTS/LottoEdge (listing + Part Two contract PDF), Sancho roster evidence, business.md, decisions.md; no v3 people folder, no Sancho recording; contact (email, phone) from his own email signature; asks Gordon whether the 2026-07-28 wrap happened and the quarterly call is live; open: contract fee vs v2 fee, two origin-story versions, location inferred (Charlotte area), Allie Wickham here vs census friend |
| jason-skaggs | Jason Skaggs | Jason, Skaggs | no; entity.md + knowledge.md action-air; knowledge.md dm-heating | partners/jason-skaggs.md | no | WoA partner (writer) | 1 |  |  |  |
| jeff-carpenter | Jeff Carpenter |  | no; entity.md + knowledge.md travis-crawford-hvac | no | jeff-carpenter (voice profile only) | client person (GM) | 1 | done | yes | 2026-10-02: new file, 43 cited lines; sources: v2 client file travis-crawford (plus two v2 inbox notes on the 2026-07-24 reply and the annual-review ingest), v3 client folder travis-crawford-hvac (client file, competitor-intel-brothers), v3 voice profile, v3 scratch 2026-08-18 (annual meeting attendees), v3 legacy transcripts (4: 2026-03-18, 06-03, 07-01, 08-19; speaker by machine voiceprint hint, unconfirmed), Sancho entity + knowledge files, _CLIENTS traviscrawfordhvac.com (listing; no document names him, an LSA lead list left unopened); no v2 people/partners file, no Sancho recording; no contact details found; asks Gordon: is the GM title right and since when; open: 2026 target $17M vs $17.4M, 2025 total, the May YTD discrepancy, 2026-03-18 "Jeff (last name unknown)" in v2 |
| jeff-collins | Jeff Collins |  | no; knowledge.md mitchells-magic (previous Cullins owner) | no | no | client person (former owner) | 1 | folded |  |  |
| jeff-goff | Jeff Goff | Jeff | no (pending request to create); entity.md dm-heating lists jeff-dm-heating; rec_0b2f65c077/speakers.md has jeff-goff human-confirmed 2026-10-01; lexicon | jeff.md (auto stub, same recording batch as karen-sartler.md) | no | client person (D&M Heating co-owner) | 1 | done | no | two Sancho slugs (jeff-dm-heating, jeff-goff) for one person. 2026-10-02: new file, 51 cited lines; sources: v2 client file dm-heating, v2 sacrosanct copy, photo brief, voice profile, one cooling outline, v2 people stub jeff.md, v2 earballs transcript 2026-04-23 rec_79307c8d5d (machine speaker labels), Sancho entity + knowledge + guidelines + 2026-09-10 summary, transcript and speakers file, karen-dodge.md, raw rec_36f02fd22c (speakers unconfirmed), _CLIENTS dmheating (listing; file names only, one spells Goff); no v2 partners file, no v3 people folder, Goff appears nowhere in v2/v3; slug conflict resolved by the entity file's 2026-10-01 note (jeff-dm-heating gets no file); contact left empty; open: start year at D&M, whether Jeffrey is his first name, the occupation details v2 dropped 2026-04-17, v3 D&M transcripts not read |
| jenn-rahn | Jenn Rahn |  | no; knowledge.md precision-chiro (bio and headshot on file; role not stated) | no | no | unknown | 1 |  |  |  |
| jeremy-vargas | Jeremy Vargas | Jay Vargas | no; knowledge.md comfort-masters-dfw | no | no | client person (operations/HR) | 1 | folded |  |  |
| jesse-olson | Jesse Olson | Jesse | no; entity.md + knowledge.md happy-outlet | no | no | client person (Happy Outlet owner) | 1 | done | yes | 2026-10-02: new file, 59 cited lines; sources: v2 client file happy-outlet (the only v2 entity file naming him), v2 tickler 2026-06-20, session-state, ingest draft 2026-04-06, v2 earballs transcripts (2025-09-15, 2026-01-14, 2026-02-11, 2026-02-16, 2026-02-26, 2026-03-17; speakers unconfirmed), v3 legacy transcripts (2026-04-06, 2026-06-10, 2026-06-15, 2026-07-31, four on 2026-08-04, 2026-08-06, 2026-08-20; speakers unconfirmed), Sancho entity + knowledge files, _CLIENTS/_Wizards of Ads CLIENTS/thehappyoutlet.com (listing; "Jesse as a kid" folder and photos by filename; docx files not opened, lead and form exports not read); no v2 people/partners file, no v3 people folder, no Sancho recording; no contact details found; asks Gordon whether the four 2026-08-04 recordings are the Portland strategy day with Jesse; open: girlfriend and daughter names (Josie, Mary) unassigned, 26 years vs "23-year-old company", birthday filename not used, other Jesses in legacy kept apart |
| jessica-happy-outlet | Jessica |  | no; entity.md + knowledge.md happy-outlet | no | no | client person (staff) | 1 | folded |  | surname not given |
| johnny-molson | Johnny Molson | Johnny | no; entity.md + knowledge.md checkvet | partners/johnny-molson.md | johnny-molson (voice profile only) | WoA partner | 1 |  |  |  |
| jordan-ohlmann | Jordan Ohlmann | Jordan | no; entity.md + knowledge.md action-air | no | no | client person (Action Air owner) | 1 | done | no | 2026-10-02: new file, 25 cited lines; sources: v2 client file action-air (the only legacy file naming him), Sancho entity + knowledge files, _CLIENTS/_Wizards of Ads CLIENTS/actionairlubbock.com (email signature block, six radio scripts, staff-page and campaign file names); no v2 people/partners file, no v3 people folder, no recordings; contact (email, two phones) taken from his signature block dated 2026-01-20; open: whether 806.789.6614 is his personal mobile, ownership split with Megan; other "Jordan" hits in v2 gulley-greenhouse and two v3 scratch transcripts are not him |
| josh-bullock | Josh Bullock | Josh | no; entity.md + knowledge.md mitchells-magic | no | josh-bullock (voice profile only) | client person (Mitchell's Magic owner) | 1 | done | yes | 2026-10-01: new file, 58 cited lines; sources: v2 client file mitchells-magic, v2 partners (peter-nevland, tom-wanek), v2 earballs ingest notes 2026-04-07, v3 voice profile (enrollment history only), Sancho entity + knowledge files and danelle-bullock.md, _CLIENTS/mitchellsmagic (listing only), rec_b24483399a; no v2 people file; contact left empty (v2's cell number comes from a machine transcript); asks Gordon whether SPEAKER_03 in rec_b24483399a is him and to state the cell number; open: Cullins ownership ("confirm" in v2), surname spelling shared with Danelle |
| josh-plunkett-web | Josh | Yosh | no; knowledge.md plunkett-home-services (previous web developer) | no | no | vendor (inferred) | 1 | folded |  | name heard as Yosh/Josh; surname not given |
| karen-dodge | Karen Dodge | Karen, Karen Sartler | no (pending request to create); entity.md dm-heating lists karen-sartler; recordings/inbox/rec_0b2f65c077/speakers.md has karen-dodge human-confirmed 2026-10-01; recordings/lexicon.md | karen-sartler.md (auto stub) | karen-sartler (voice profile only) | client person (D&M Heating owner) | 1 | done | yes | NAME CONFLICT: v2, v3, entity.md and knowledge.md say Sartler; Sancho speakers.md and lexicon say Dodge [confirmed gordon 2026-10-01]; two Sancho slugs (karen-sartler, karen-dodge) for one person. 2026-10-02: seeded file thickened, 68 cited lines added (existing lines kept); sources: v2 client file dm-heating, v2 photo brief, v2 people stub karen-sartler, two v2 earballs transcripts of 2026-04-23 (rec_79307c8d5d, rec_2ae657c225; machine speaker labels), v3 voice profile (enrollment history only), v3 transcript voiceprint hints (14 recordings, hint lines only, listed as leads), Sancho entity + knowledge + guidelines + 2026-09-10 summary, transcript and speakers file, raw rec_36f02fd22c (speakers unconfirmed), _CLIENTS dmheating/from-client (listing only; docx not opened); name conflict resolved by Gordon's 2026-10-01 note (Dodge); contact left empty (only the company's address and main line are on file); asks Gordon whether her brother's illness is filed (read back 2026-10-01, awaiting his yes) and whether "primary owner" still holds |
| ken-goodrich | Ken Goodrich | Ken | no; entity.md + knowledge.md happy-outlet | no | no | client-side advisor (inferred) | 1 | done | yes | 2026-10-02: new file, 48 cited lines; sources: v2 clients (happy-outlet, comfort-masters-dfw, society-hill), v2 people (steven-moore), v2 transcripts (rec_0959f8493f, rec_653d0069e7, rec_734e09745f, rec_c32ce8021e), v3 excerpts (2026-05-27 and 2026-09-01 Roy Williams Goettl tellings), v3 transcripts (rec_aac46b33c2, rec_42dfc84bc2, rec_62f9957a84), _CLIENTS/thehappyoutlet.com (the 2025-04-09 call transcript, read whole from Ken's arrival), Sancho entity + knowledge files; no v2 people/partners file, no v3 people folder, no Sancho recording; no contact details found; asks Gordon whether the 2026-08-04 account of the declined partnership (speaker asked it stay in the room) stays here or goes to Private; open: who made the 2026-03-13 remark about him (v2 says Stephen Moore, the transcript label says Adam Donmoyer), the can-opener story's date, Goettl sale figures; kind is closer to "outside advisor to a client's owner; Roy Williams client" than client-side |
| kevin-lin | Kevin Lin | Dr. Kevin Lin | no; knowledge.md precision-chiro | no | no | client-adjacent (Florida practice) | 1 | folded |  |  |
| kevin-skalure | Kevin Skalure |  | no (pending request to create); rec_0b2f65c077/speakers.md human-confirmed 2026-10-01; lexicon (spelling unconfirmed) | no | no | client person (D&M Heating) | 1 | done | yes | surname spelling unconfirmed per speakers.md. 2026-10-02: new file, 42 cited lines; sources: Sancho D&M knowledge, summary, speakers, corrections, lexicon, rec_0b2f65c077, rec_36f02fd22c (raw, speakers unconfirmed), v3 transcripts rec_566665cedd (2026-07-02), rec_33c6c258d0 (2026-07-23), rec_e4d4e0ce56 (2026-08-27), v2 transcript rec_dfb75c1583 (one line), _CLIENTS/dmheating (listing only); no v2 people/partners file, no v3 people folder; no contact details found; kind here is superseded by the evidence: he is on the Wizard of Ads side (ad writer with Peter Nevland), not a D&M person; asks Gordon for the surname spelling (Skalure / "scalur" / "schooler" on file), his standing at WoA, and whether the March 31 birthday from a machine-labelled transcript is right |
| kyle-caldwell | Kyle Caldwell |  | no; entity.md + knowledge.md travis-crawford-hvac | no | kyle-caldwell (voice profile only) | WoA media buyer | 1 |  |  |  |
| kyle-collins | Kyle Collins |  | no; knowledge.md mitchells-magic | no | no | client person (Cullins) | 1 | folded |  |  |
| larry-bloom | Larry Bloom | Molly Bloom's dad | yes (thin); people/larry-bloom.md; people/gordon.md | no | no | personal (former professor) | 1 |  |  |  |
| lathan | Lathan | Latham (misheard) | no; work/american-icon-spirits/business.md; recordings/lexicon.md | lathan.md; MANIFEST.md row | no | venture (American Icon Spirits co-owner) | 1 |  |  | surname not given anywhere |
| leah | Leah Ashley | Leah, Leah Elizabeth Ashley | yes (full); people/leah.md; entity.md precision-chiro, travis-crawford-hvac; knowledge.md People in checkvet, comfort-masters-dfw, dm-heating, happy-outlet, mitchells-magic, plunkett-home-services, precision-chiro, travis-crawford-hvac | leah-ashley.md (pointer; full file is v2 relationships/leah.md); leah.md (auto stub) | leah (voice profile only) | family (spouse); Copper Leaf operations | 1 |  |  | two v2 files for one person (leah-ashley.md, leah.md stub) |
| lizzie-mack | Elizabeth Mack | Lizzie, Lizzie Mack, Lizzie Mac | yes (full); people/lizzie-mack.md; work/entomat, work/american-icon-spirits | lizzie-mack.md | no | venture (Entomat, American Icon Spirits) | 1 |  |  |  |
| luis-castaneda | Luis Castaneda | Luis, Luis Casteneda | no; entity.md + knowledge.md comfort-masters-dfw; knowledge.md travis-crawford-hvac ("Luis, WoA Digital", inferred same) | no | luis-casteneda (voice profile only; spelling differs) | WoA PPC manager | 1 |  |  | v3 folder spells Casteneda |
| maria-pia-seirup | Maria Pia Seirup | Mom | no; referenced as "Mom" in work/copper-leaf/projects/hd-system-rebuild/docs/requirements.md:20 (identity unconfirmed there) | MANIFEST.md row only (no file) | no | family (mother) | 1 |  |  | Sancho doc says unconfirmed whether "Mom" is Maria Pia Seirup; v2 MANIFEST names her as Gordon's mother; v2 peter-seirup.md relationships list maria-pia-seirup |
| mark-mitchells-magic | Mark |  | no; knowledge.md mitchells-magic (media buyer; surname unknown) | no | no | WoA media buyer | 1 | folded |  | surname unknown |
| marty-greer | Marty Greer | Dr. Marty Greer, Dr. Greer | no; entity.md + knowledge.md checkvet | no | no | client person (CheckVet owner) | 1 | done | yes | 2026-10-02: new file, 46 cited lines; sources: v2 client files checkvet and checkin-veterinary-policy-diagnosis (the only legacy files naming her; mitchells-magic "Marty" is Marty Ritchie, a different person), Sancho entity + knowledge files and dan-griffiths.md, _CLIENTS/Check In and Out Vet (listing; three press-release PDFs read; signed MSA is a scan, not re-read; from-client/Marty Greer/ identity documents not read by rule), rec_640701d84d; no v2 people/partners file, no v3; contact: one email from the press-release contact block, nothing else; asks Gordon whether the "Marty" in rec_640701d84d is her and how ownership (sole vs joint with Dan) is to be phrased |
| matt-dm-heating | Matt |  | no; knowledge.md dm-heating (IT/hosting owner) | no | no | vendor (inferred) | 1 | folded |  | surname not given; not the same as v2 matt-builder or matt-mcintosh as far as the evidence says |
| matt-willis | Matt Willis | Matt | no; entity.md + knowledge.md happy-outlet | no | no | WoA partner | 1 |  |  |  |
| megan-ohlmann | Megan Ohlmann | Megan | no; entity.md + knowledge.md action-air | no | no | client person (Action Air owner) | 1 | done | no | 2026-10-02: new file, 31 cited lines; sources: v2 client file action-air (the only legacy file naming her), Sancho entity + knowledge files, _CLIENTS/_Wizards of Ads CLIENTS/actionairlubbock.com (her email signature block, the Feb 2025 distribution form, eight radio and campaign scripts, the Buyback collateral checklist, portrait and staff-page file names); no v2 people/partners file, no v3 memory file, no recordings; contact (email, two phones) taken from her signature block dated 2025-12-11; open: v2 says "Owner, handles operations" while her signature says "Marketing Director, Co-Owner", whether 806.928.3172 is her personal mobile, ownership split with Jordan; other "Megan" hits in v2 (megan-together-financial, straight-line-fitness, checkvet "Dr. Megan", Paige's roommate) are not her |
| mick-torbay | Mick Torbay | Mick, Torbay, Michael Torbay, Mick Torban (transcript error) | no; entity.md + knowledge.md travis-crawford-hvac | no | mick-torbay (voice profile only) | WoA account team | 1 | done | yes | 2026-10-02: new file, 52 cited lines; sources: v2 client file travis-crawford, 12 v2 earballs transcripts (2025-08-24 to 2026-04-03; name-matched lines only, machine or missing speaker labels), v3 voice profile (enrollment history only), v3 client file travis-crawford-hvac, v3 scratch note on the 2026-07-27 annual meeting, 8 v3 transcripts (2026-03-18 to 2026-09-02; name-matched passages only), Sancho entity + knowledge files, roster evidence, chris-torbay, travis-crawford and jeff-carpenter files, _CLIENTS traviscrawfordhvac.com (listing only); no v2 people or partners file, no Sancho recording names him; contact field left empty; location Toronto rests on one undiarized remark; asks Gordon: is Mick a WoA partner in his own right, does he live in Toronto, and was his unsolicited testimonial used in the AEO/SEO video; open: writing split between the brothers, transcript spellings in his origin story of the account ("Peter Nevlin", "Charlie Mosher", "Winbrook"), two bare "Mick" mentions that may be someone else; not read: body of the five-hour 2026-07-27 recording beyond name-matched passages, v3 comms inbox and voiceprint library, v2 data index/export files |
| molly-bloom | Molly Bloom |  | no; people/larry-bloom.md, people/lizzie-mack.md, people/gordon.md | no | no | reference (public figure, Larry Bloom's daughter) | 1 |  |  | probably no file needed; referenced only via larry-bloom |
| nathan-ingram | Nathan Ingram | Nathan, Ingram | no (pending people/nathan.md); entity.md + knowledge.md dm-heating; recordings/inbox/rec_564c0541a8/summary.md ("Nathan") | nathan-ingram.md | no | vendor and friend (web developer) | 1 |  |  | pending request names people/nathan.md; use nathan-ingram |
| nicole-checkvet | Nicole |  | no; knowledge.md checkvet (Marshall Pet Care office manager) | no | no | client person | 1 | folded |  | surname not given; a different Nicole (Laura Holden's friend) is in v2 MANIFEST |
| olivia-la | Olivia La | Dr. Olivia La | no; entity.md + knowledge.md precision-chiro | no | no | client person (associate chiropractor) | 1 | done | yes | 2026-10-01: new file, 47 cited lines; sources: v2 client file jane-brewer-precision-chiro (the only v2 file naming her), v3 bio drafts v1 to v4 and Gordon's final (work/clients/precision-chiro/_active), Sancho entity + knowledge + guidelines files and jane-brewer.md, _CLIENTS/_Wizards of Ads CLIENTS/Precision Chiropractic (listing; images not opened); no v2 people/partners file, no v3 people folder, no recordings; no contact details found; asks Gordon whether she approved the bio; open: residency vs clinical rotation, license date vs Jane's Feb 2026 trip, Johnstown vs Windsor in the drafts, v2's Ashley/Olivia guess, start date; fiance Brian has no file or census row |
| patience-checkvet | Patience |  | no; knowledge.md checkvet | no | no | client person (social media) | 1 | folded |  | surname not given |
| peter-nevland | Peter Nevland | Peter, Nevland | no (pending request to create); entity.md checkvet, comfort-masters-dfw, dm-heating, mitchells-magic; knowledge.md same; recordings/inbox/rec_0b2f65c077 and rec_564c0541a8 speakers.md human-confirmed 2026-10-01 | peter-nevland.md; partners/peter-nevland.md; MANIFEST.md row | peter-nevland (voice profile only) | WoA partner | 1 |  |  | two v2 files (people and partners); recordings/inbox/_pending-requests.md:33 already asks for people/peter-nevland.md |
| peter-seirup | Peter Seirup | Peter, Dad, Peter Seirup P.E., Gordon's dad, Gordon's father | yes (full); people/peter-seirup.md; entity.md home-directions | peter-seirup.md; MANIFEST.md row | no | family (father); CLC-PM client (Home Directions) | 1 |  |  |  |
| piper-comfort-masters | Piper |  | no; knowledge.md comfort-masters-dfw | no | no | client person (CSR) | 1 | folded |  | surname not given |
| rick-willis | Rick Willis | Rick | no; entity.md + knowledge.md happy-outlet | partners/rick-willis.md | no | WoA partner | 1 |  |  |  |
| robert-nathan-allen | Robert Nathan Allen | RNA, R&A | yes (full); people/robert-nathan-allen.md; work/entomat | rna.md (name given only as RNA) | no | venture (Entomat) | 1 |  |  | v2 file is rna.md; same person per Sancho lexicon |
| robin-kressbach | Robin Kressbach | Robin | no; entity.md + knowledge.md plunkett-home-services | partners/robin-kressbach.md | no | WoA partner (design) | 1 |  |  |  |
| rondell-comfort-masters | Rondell |  | no; knowledge.md comfort-masters-dfw (technician) | no | no | client person | 1 | folded |  | surname not given |
| roy-williams | Roy Williams | Roy, The Wizard | no; entity.md + knowledge.md society-hill-plumbing (advisor via the AWG course) | roy-williams.md | no | WoA founder; mentor | 1 |  |  |  |
| ryan-chute | Ryan Chute | Ryan | no; entity.md + knowledge.md happy-outlet, society-hill-plumbing | no | no | WoA partner | 1 |  |  |  |
| sarah-service-excellence | Sarah |  | no; knowledge.md society-hill-plumbing (Service Excellence, with Todd Lyles) | no | no | consultant (inferred) | 1 | no-folder |  | surname not given; Sarah, Service Excellence (price book and membership pricing, with Todd Lyles); no Service Excellence client folder (already listed in society-hill-plumbing/knowledge.md People) |
| scarlett-plunkett | Scarlett Plunkett | Scarlett | no; entity.md + knowledge.md plunkett-home-services | no | no | client person (ops manager) | 1 | done | yes | 2026-10-02: new file, 16 cited lines; sources: v2 client file plunkett-home-services, v2 partners dave-young (line 48), Sancho entity + knowledge files and roster evidence, people/chris-plunkett.md; no v2 people/partners file of her own, no v3 people folder, no Sancho recordings, nothing readable in _CLIENTS/_Wizards of Ads CLIENTS/Plunkett names her (form and lead exports not opened); contact field left empty (v2 gives an email with no stated source); asks Gordon to confirm that email; open: no direct contact with Gordon on record, nothing naming her after 2026-04-10, legacy earballs transcripts not read (outside the skill's paths) |
| sosa-travis-crawford | Sosa |  | no; knowledge.md travis-crawford-hvac (previous digital/social person; last name unknown) | no | no | client person (former) | 1 | folded |  | name as given |
| stephanie-dm-heating | Stephanie |  | no; knowledge.md dm-heating (office assistant) | no | no | client person | 1 | folded |  | surname not given |
| stephen-moore | Stephen Moore | Steven Moore, Steve, Stephen, Steven | no; entity.md + knowledge.md comfort-masters-dfw | steven-moore.md | no | client person (Comfort Masters owner) | 1 | done | yes | v2 file name uses Steven; name field says Stephen. 2026-10-01: existing file thickened, 67 cited lines added, 5 existing lines kept; sources: v2 people (steven-moore, jack-heald, peter-nevland, gene-vann), v2 clients (comfort-masters-dfw, aeo-strategy), Sancho entity + knowledge files and amanda-moore.md, _CLIENTS/comfortmastersdfw (the "Why" docx, Brandable Chunks, folder listing), rec_d32d657ed1, rec_d46f439a37, rec_1dc87f7565; no v3 folder, no v2 partners; no contact details found; asks Gordon: two daughters or three (the "Why" copy says two, v2 and the client photo say three), and whether he speaks in rec_1dc87f7565; open: the "prison" and Detroit references, who Donnie is |
| stephen-semple | Stephen Semple | Stephen, Semple | no; entity.md + knowledge.md travis-crawford-hvac | partners/stephen-semple.md | stephen-semple (voice profile only) | WoA partner | 1 |  |  |  |
| stett-comfort-masters | Stett |  | no; knowledge.md comfort-masters-dfw (tech trainer) | no | no | client person | 1 | folded |  | surname not given |
| steve-rae | Steve Rae | Steve | no; entity.md + knowledge.md society-hill-plumbing | MANIFEST.md row only (no file) | no | WoA partner (media buyer/advisor) | 1 |  |  |  |
| stevie-comfort-masters | Stevie |  | no; knowledge.md comfort-masters-dfw (office/data) | no | no | client person | 1 | folded |  | surname not given |
| syre-klenke | Syre Klenke | Syre | no; entity.md + knowledge.md checkvet | partners/syre-klenke.md | no | WoA partner | 1 |  |  |  |
| tammy-parker | Tammy Parker |  | no; entity.md + knowledge.md precision-chiro (Unicycle Consulting) | no | no | client-side contractor (fractional HR) | 1 | folded |  |  |
| tara-checkvet | Tara |  | no; knowledge.md checkvet | no | no | client person (former practice manager) | 1 | folded |  | surname not given |
| tim-silva | Tim Silva | Tim | no (pending request to create); entity.md dm-heating lists tim-dm-heating; rec_0b2f65c077/speakers.md has tim-silva human-confirmed 2026-10-01; lexicon | tim-silva.md (auto stub) | tim-silva (voice profile only) | client person (D&M Heating co-owner) | 1 | done | no | two Sancho slugs (tim-dm-heating, tim-silva) for one person; resolved for the slug by entity.md's note [confirmed gordon 2026-10-01], tim-dm-heating gets no file. 2026-10-02: new file, 58 cited lines; sources: v2 client files (dm-heating, sacrosanct-copy, photo-brief, voice-profile, content-definition, peace-of-mind draft), v2 people stub tim-silva, v2 transcript rec_79307c8d5d, v3 voice profile (enrollment record only) and the header of v3 rec_2d62e0a1e9, Sancho entity + knowledge + guidelines + summary + speakers files, lexicon, rec_0b2f65c077, rec_36f02fd22c (raw, speakers unconfirmed), _CLIENTS/_Wizards of Ads CLIENTS/dmheating (listing; file names only); no v2 partners file; no contact details found; open: whether he sells, whether the "doesn't like pictures" site line came off, the written boiler-song steps, whether v3 rec_2d62e0a1e9 is the same meeting as v2 rec_79307c8d5d |
| todd-comfort-masters | Todd |  | no; knowledge.md comfort-masters-dfw (the connection to Peter Nevland; surname not given) | no | no | unknown | 1 | folded |  | possibly todd-lyles; unconfirmed |
| todd-lyles | Todd Lyles | Todd | no; entity.md society-hill-plumbing; knowledge.md dm-heating, society-hill-plumbing | no | no | WoA partner; ops consultant (Service Excellence) | 1 |  |  | see todd-comfort-masters |
| tom-wanek | Tom Wanek | Tom, Wanek | no; entity.md + knowledge.md mitchells-magic | partners/tom-wanek.md | wanek (voice profile only) | WoA partner | 1 |  |  | v3 folder is surname only |
| travis-crawford | Travis Crawford | Travis | no; entity.md + knowledge.md travis-crawford-hvac | travis-crawford.md (auto stub) | no | client person (Travis Crawford HVAC owner) | 1 | done | yes | 2026-10-02: new file, 52 cited lines; sources: v2 people stub (no facts) and the recording it points to (rec_91be02ce4b, 2025-12-19, lines naming him only), v2 client file travis-crawford, v2 partners (stephen-semple), v2 dashboard, v3 client file travis-crawford-hvac, v3 scratch 2026-08-18 (annual meeting attendees), v3 legacy transcripts (4: 2026-03-18, 07-01, 07-27 opening 130 lines, 08-19; speakers by machine hint or untagged), Sancho entity + knowledge files, business.md, jeff-carpenter.md, _CLIENTS traviscrawfordhvac.com (listing; signed MSA and annual deck not readable, no PDF renderer; credentials files left unopened); no v3 people folder, no Sancho recording; no contact details found (he prefers text, no mobile on file); asks Gordon whether the opening voice of the 2026-07-27 annual meeting (SPEAKER_01 in rec_74b997b2bf) is Travis; open: Mexico vs Toronto for the annual gathering (superseded by the 2026 folder), rest of the annual transcript and about 30 other legacy transcripts not read |
| tricia-lewis | Tricia Lewis | Tricia, T. Lewis | no; knowledge.md comfort-masters-dfw | no | no | client person (CSR) | 1 | folded |  |  |
| trish-precision-chiro | Trish |  | no; knowledge.md precision-chiro (former office manager) | no | no | client person | 1 | folded |  | surname not given |
| tyler-mitchells-magic | Tyler |  | no; knowledge.md mitchells-magic (technician) | no | no | client person | 1 | folded |  | surname not given |
| vi-wickam | Vi Wickam | Vi, Vi Wickham | no; entity.md dm-heating (referral); _roster-evidence-v2.md (Service Professionals) | partners/vi-wickam.md | vi-wickam (voice profile only) | WoA partner (senior) | 1 |  |  | v2 spells Wickam; allie-wickham.md spells the family name Wickham |
| wes-brewer | Wes Brewer |  | no; entity.md + knowledge.md precision-chiro | no | no | client person (Jane's husband) | 1 | done | yes | 2026-10-01: new file, 26 cited lines; sources: v2 client file jane-brewer-precision-chiro, v2 relationships/leah.md, v2 tickler 2026-08-01, v2 backlog table of contents (calendar line), v2 transcripts rec_15536f3c3d and rec_c7e406fa14, v3 transcripts rec_3860b59c59 and rec_5565f30055, Sancho entity + knowledge files and jane-brewer.md, _CLIENTS/Precision Chiropractic (listing only); no v2 people/partners file, no v3 people folder; no contact details found; asks Gordon whether the "Wes" in rec_5565f30055 is him and which month his mother died (v2 contradicts itself); open: "Wes prefers first class" vs the transcript, whose dad booked the Caribbean cruise |
| william-lordan | William Lordan | Bill Lordan, Dr. Lordan | no; knowledge.md precision-chiro (Precision Chiro CT) | no | no | CLC-PM client (DINABY site) | 1 | done |  | separate CLC client under _CLIENTS/Precision Chiro CT per knowledge.md. 2026-10-02: new file, 36 cited lines; sources: _CLIENTS/Precision Chiro CT (signed MSA 2025-09-07, DINABY homework and workbook 2025-09-19, folder listing and file dates), _CLIENTS/_Wizards of Ads CLIENTS/Precision Chiropractic splash page (index.html, README-BUILD, design handoff), Sancho precision-chiro entity + knowledge files and jane-brewer.md; no match for his name anywhere in v2 or v3, no Sancho recordings; contact field left empty (only the practice's office line and Facebook page are on disk); open, none needing Gordon to proceed: town not stated, June 2026 "new property" images unexplained, site launch date and Press Managed plan status not evidenced |
| zakk-mitchells-magic | Zakk |  | no; knowledge.md mitchells-magic (Charlie Moger's team) | no | no | vendor (inferred) | 1 | folded |  | surname not given |
| cedric-yau | Cedric Yau | Cedric | no | partners/cedric-yau.md | no | WoA partner (SEO) | 2 |  |  |  |
| dnelle-dowis | D'nelle Dowis | D'nelle, Dnelle | no | dnelle-dowis.md | no | friend; consulting client (v2 tag) | 2 |  |  |  |
| dom-mcclellan | Dom McClellan | Dom | no | dom-mcclellan.md; MANIFEST.md row | no | venture contact (spirits distribution) (inferred) | 2 |  |  |  |
| guy-hanington | Guy Hanington | Guy | no | no | guy-hanington (profile.md) | personal (Leah's partner) | 2 |  |  | v3 only; v3 status active |
| jeff-sexton | Jeff Sexton | Jeff | no | jeff-sexton.md | no | WoA partner | 2 |  |  | v2 file is tagged sensitive/discretion-required |
| josh-agajanian | Josh Agajanian | Josh | no | josh-agajanian.md; MANIFEST.md row | no | venture contact (potential partner) (inferred) | 2 |  |  |  |
| laura-holden | Laura Holden | Laura | no | laura-holden.md; MANIFEST.md row | no | friend; Press Managed client (v2 tag) | 2 |  |  |  |
| lucy-entomat | Lucy |  | no | lucy-entomat.md; MANIFEST.md row | no | venture (Entomat partner) | 2 | folded |  | surname not given |
| temple-grandin | Temple Grandin | Temple | no | temple-grandin.md; MANIFEST.md row | no | venture advisor (Entomat) (inferred) | 2 |  |  | public figure |
| zac-smith | Zac Smith | Zac, Zach | no | zac-smith.md; partners/zac-smith.md | no | WoA partner; friend | 2 |  |  | two v2 files (people and partners) |
| adrian-van-zelfden | Adrian Van Zelfden | Adrian | no | adrian-van-zelfden.md | no | WoA attorney and CPA | 3 |  |  |  |
| alexia-blackwood | Alexia Blackwood | Lexi, Alexia | no | alexia-blackwood.md; MANIFEST.md row (as Lexi Blackwood) | no | friend | 3 |  |  |  |
| ali-woll | Ali Woll | Ali | no | ali-woll.md; MANIFEST.md row | no | friend | 3 |  |  | disambiguation risk with allie-wickham (v2 note); allie-woll.md is a deprecated merge, see junk list |
| amanda-mikhail-partner | Amanda |  | no | MANIFEST.md row only (no file) | no | personal (Mikhail Voloshin's partner) | 3 |  |  | surname not given; not amanda-moore |
| amber-crummy | Amber Crummy | Amber, Ber | no | amber-crummy.md | amber-crummy (voice profile only) | friend (of Leah) | 3 |  |  | v2 says the alias Burr is a speech-to-text artifact |
| amy-ehrhardt | Amy Ehrhardt | Amy | no | amy-ehrhardt.md | no | venture-adjacent (Grayson's wife) | 3 |  |  | surname follows v2's Ehrhardt spelling; Sancho uses Erhard for Grayson |
| ansel-courant | Ansel Courant | Ansel | no | ansel-courant.md; MANIFEST.md row | no | family (Leah's step-brother); friend | 3 |  |  |  |
| beatrice-ratte | Beatrice Ratte | Aunt Bea | no | MANIFEST.md row only (no file) | no | family (great aunt) | 3 |  |  | manifest row only |
| billy-walker | Billy Walker |  | no | MANIFEST.md row only (no file); named in lizzie-mack.md and dom-mcclellan.md first lines | no | venture-adjacent (whiskey industry) | 3 |  |  | manifest row only |
| bob-ratte | Bob Ratte | Popere | no | MANIFEST.md row only (no file) | no | family (grandfather) | 3 |  |  | manifest row only |
| brent-ballard | Brent Ballard | Brent | no | brent-ballard.md; MANIFEST.md row | no | friend | 3 |  |  |  |
| brian-neighbor | Brian |  | no | brian-robin-neighbors.md (one file for two people) | no | personal (neighbor) | 3 |  |  | surname not given; shares a v2 file with robin-neighbor |
| chad-cohen | Chad Cohen | Chad, Trad (misheard) | no | chad-cohen.md; MANIFEST.md row | chad-cohen (voice profile + scratch.md) | friend | 3 |  |  |  |
| chris-lema | Chris Lema | Chris, Lema | no | chris-lema.md | no | industry figure (WordPress) (inferred) | 3 |  |  | v2 tags negative-relationship |
| dan-morman | Dan Morman |  | no | MANIFEST.md row only (no file) | no | friend (Austin circle) | 3 |  |  | manifest row only |
| delia | Delia |  | no | MANIFEST.md row only (no file) | no | friend (college) | 3 |  |  | surname not given; manifest row only |
| donna-thomas | Donna Thomas |  | no | MANIFEST.md row only (no file); relationship entity in leah-ashley.md | no | family (Leah's stepmother) | 3 |  |  | manifest row only |
| dora-ratte | Dora Ratte | Nonna | no | MANIFEST.md row only (no file) | no | family (grandmother) | 3 |  |  | manifest row only |
| dr-mitch-janosik | Mitch Janosik | Dr. Mitch Janosik, Dr. Janosik, Mitch | no | dr-mitch-janosik.md | no | personal (physician) | 3 |  |  | slug keeps the v2 form |
| ella-jess-daughter | Ella |  | no | MANIFEST.md row only (no file) | no | family (Jess's daughter) | 3 |  |  | minor; manifest row only |
| elliott-scott | Elliott Scott | Elliott, Elena Seirup (birth name) | no | elliott-scott.md; MANIFEST.md row | no | family (sibling) | 3 |  |  | not to be confused with elliott-stark |
| emily-sheehan | Emily Sheehan | Emily | no | emily-sheehan.md; MANIFEST.md row | emily-sheehan (voice profile only) | friend | 3 |  |  |  |
| eric-pommier | Eric Pommier | Eric | no | eric-pommier.md; MANIFEST.md row | no | friend (Laura Holden's husband) | 3 |  |  |  |
| felix | Felix |  | no | named in james-gilbert.md (James's partner); no file | no | friend-adjacent (inferred) | 3 |  |  | surname not given |
| gene-vann | Gene Vann | Gene, GMBAN | no | gene-vann.md | no | friend | 3 |  |  |  |
| gina-cizek | Gina Cizek |  | no | MANIFEST.md row only (no file) | no | family (godmother) | 3 |  |  | manifest row only |
| greg-verbanic | Greg Verbanic |  | no | MANIFEST.md row only (no file); relationship entity in rob-rowe.md | no | friend (childhood) | 3 |  |  | manifest row only |
| gwen-goldrich | Gwen |  | no | MANIFEST.md row only (no file) | no | personal (neighbor; Mark Goldrich's wife) | 3 |  |  | surname inferred from Mark Goldrich; manifest row only |
| hazel | Hazel |  | no | no | hazel (voice profile only) | unknown | 3 |  |  | v3 voice profile only; no role anywhere |
| holly-cohen | Holly Cohen | Holly | no | MANIFEST.md row only (no file); relationship entity in chad-cohen.md | holly-cohen (voice profile only) | friend | 3 |  |  |  |
| isabel-jackson | Isabel Jackson |  | no | MANIFEST.md row only (no file) | no | friend | 3 |  |  | manifest row only; context TBD there |
| jamie-joseph | Jamie Joseph |  | no | MANIFEST.md row only (no file) | no | personal (estranged from the friend group per manifest) | 3 |  |  | manifest row only |
| jeffrey-ratte | Jeffrey Ratte |  | no | MANIFEST.md row only (no file) | no | family (uncle) | 3 |  |  | manifest row only |
| jess-paula-cousin | Jess |  | no | MANIFEST.md row only (no file) | no | family (Paula's cousin) | 3 |  |  | surname not given; manifest row only |
| joan-tropiano-tucci | Joan Tropiano Tucci |  | no | MANIFEST.md row only (no file) | no | family | 3 |  |  | manifest row only |
| john-mark-patterson | John Mark Patterson |  | no | john-mark-patterson.md | no | personal (potential attorney) | 3 |  |  | v2 says no-show, no prior interaction |
| john-marron | John Marron | John, Marron, Jonathan | no | john-marron.md; john-marron-leah-summary.md and john-marron-working.md (documents, not person files); MANIFEST.md row | john-marron (profile.md, merges the three v2 files) | friend | 3 |  |  | v2 tags sensitive |
| john-metcalf | John Metcalf | Metcalf | no | john-metcalf.md | no | friend | 3 |  |  |  |
| kay-ullman | Kay Ullman | Kay | no | kay-ullman.md; MANIFEST.md row | no | personal (mentor; deceased per v2) | 3 |  |  |  |
| kyle-heustis | Kyle Heustis | Kyle | no | kyle.md; MANIFEST.md row | no | friend | 3 |  |  | v2 file name is kyle.md; MANIFEST also lists a "Kyle (builder contact)", possibly the same person |
| leslie-hong | Leslie Hong | Leslie, Leslie Seirup | no | leslie-hong.md; MANIFEST.md row | no | family (sister) | 3 |  |  |  |
| lily-post | Lily Post | Lily | no | lily-post.md; MANIFEST.md row | no | family of friend (Alex Post's daughter) | 3 |  |  | minor |
| luke-bernander | Luke Bernander | Luke | no | luke-bernander.md; MANIFEST.md row | luke-bernander (profile.md, v2 port) | family (Leah's father) | 3 |  |  |  |
| mark-benn | Mark Benn | Mark | no | mark-benn.md; MANIFEST.md row | no | personal (psychologist; mentor) | 3 |  |  |  |
| mark-effinger | Mark Effinger |  | no | MANIFEST.md row only (no file) | no | Wizard Academy donor | 3 |  |  | manifest row only |
| mark-goldrich | Mark Goldrich |  | no | MANIFEST.md row only (no file) | no | personal (neighbor) | 3 |  |  | manifest row only |
| matt-builder | Matt | Matt the Builder, Matt contractor | no | matt-builder.md; MANIFEST.md row (Matt (contractor)) | no | personal (contractor) | 3 |  |  | surname unknown |
| matt-mcintosh | Matt McIntosh | Mac, Matt, Matthew McIntosh | no | matt-mcintosh.md; mac.md (duplicate); MANIFEST.md row | no | friend | 3 |  |  | DUPLICATE in v2: mac.md and matt-mcintosh.md are the same person |
| megan-together-financial | Megan | Megan (Together Financial) | no | megan-together-financial.md (auto stub) | no | unknown (vendor contact, inferred) | 3 | no-folder |  | stub only; a different Megan (Paige's roommate) appears in paige.md; Megan, Together Financial; no Together Financial client folder (see work/wizard-of-ads/clients/_roster-evidence-v2.md) |
| mike-catan | Mike Catan |  | no | MANIFEST.md row only (no file) | mike-catan (voice profile only) | friend | 3 |  |  |  |
| mike-orth | Mike Orth | Mikey, Morth, Mike | no | mikey.md | no | friend | 3 |  |  | v2 file name is mikey.md |
| mikhail-voloshin | Mikhail Voloshin | Mikhail | no | mikhail-voloshin.md | no | friend (Wizard Academy circle) | 3 |  |  |  |
| nathan-gutters | Nathan | Nathan Gutters | no | nathan-gutters.md | no | personal (subcontractor) | 3 |  |  | surname unknown; not nathan-ingram (v2 says so explicitly) |
| nicole-laura-friend | Nicole |  | no | MANIFEST.md row only (no file) | no | friend of Laura Holden | 3 |  |  | surname not given; not nicole-checkvet |
| paige | Paige | Paige (housecleaner) | no | paige.md | paige (profile.md + voice profile) | personal (former housecleaner) | 3 |  |  |  |
| patrick-rauland | Patrick Rauland | Piyar, Patrick, Patrick Rowland, Patrick Rowan | no | patrick-rauland.md; MANIFEST.md row (as Patrick Rowland) | no | friend | 3 |  |  | MANIFEST spells Rowland; file spells Rauland |
| paula-bernander | Paula Bernander | Paula | no | paula-bernander.md; MANIFEST.md row | no | family (Leah's sister) | 3 |  |  |  |
| pegeen-reilly | Pegeen Reilly | Pegeen | no | pegeen-reilly.md | no | Wizard Academy board (inferred) | 3 |  |  |  |
| pennie-williams | Pennie Williams | Princess Pennie | no | MANIFEST.md row only (no file) | no | WoA-adjacent (Roy's wife) | 3 |  |  | manifest row only |
| pierre-ratte | Pierre Ratte |  | no | MANIFEST.md row only (no file) | no | family (uncle) | 3 |  |  | manifest row only |
| ren-rauland | Ren | Ren Rauland, Ren Rowland | no | ren.md; MANIFEST.md row | no | friend (Patrick's wife) | 3 |  |  | surname unconfirmed in v2 |
| rex-williams | Rex Williams |  | no | MANIFEST.md row only (no file); relationship entity in roy-williams.md, wizard-academy.md | no | Wizard Academy (Roy's son) | 3 |  |  | manifest row only |
| rob-rowe | Rob Rowe | Rob | no | rob-rowe.md; MANIFEST.md row | no | friend | 3 |  |  |  |
| robin-neighbor | Robin |  | no | brian-robin-neighbors.md (one file for two people) | no | personal (neighbor) | 3 |  |  | surname not given; shares a v2 file with brian-neighbor |
| russell-quintero | Russell Quintero |  | no | MANIFEST.md row only (no file) | no | friend | 3 |  |  | manifest row only; context TBD there |
| ryan-deiss | Ryan Deiss | Ryan, Ryan Dice (misheard) | no | ryan-deiss.md | no | Wizard Academy board (inferred) | 3 |  |  | public figure |
| ryan-painter | Ryan | Ryan (painter) | no | MANIFEST.md row only (no file) | no | personal (house painter) | 3 |  |  | surname not given; manifest row only |
| sara-moorehead | Sara Moorehead | Sarah Morehead (misspelling per manifest) | no | MANIFEST.md row only (no file) | no | family (aunt) | 3 |  |  | manifest row only |
| sawyer-rauland | Sawyer | Sawyer Rowland | no | MANIFEST.md row only (no file) | no | family of friend (Patrick and Ren's daughter) | 3 |  |  | minor; manifest row only |
| scott-beasley | Scott Beasley | Beasley, Scott | no | beasley.md; MANIFEST.md row | no | friend | 3 |  |  | v2 file name is beasley.md |
| shannon-janelle | Shannon Janelle |  | no | MANIFEST.md row only (no file) | no | friend | 3 |  |  | manifest row only; context TBD there |
| stan-tucci-sr | Stan Tucci Sr. |  | no | MANIFEST.md row only (no file) | no | family (cousin of Gordon's mother) | 3 |  |  | manifest row only |
| stanley-tucci | Stanley Tucci |  | no | MANIFEST.md row only (no file) | no | family (first cousin once removed) | 3 |  |  | public figure; manifest row only |
| stephanie-steward | Stephanie Steward | Stephanie | no | stephanie-steward.md | no | personal (realtor) | 3 |  |  |  |
| ted-klontz | Ted Klontz | Ted | no | ted-klontz.md; MANIFEST.md row | ted-klontz (profile.md + voice profile) | personal (therapist) | 3 |  |  |  |
| teri-ashley | Teri Ashley | Teri Anne Wiganowski (former name, sp?) | no | MANIFEST.md row only (no file); relationship entity in leah-ashley.md, paula-bernander.md, tom-boldt.md | no | family (Leah's mother) | 3 |  |  | manifest row only |
| tom-boldt | Tom Boldt | Tom | no | tom-boldt.md | no | family (Leah's mother's partner) | 3 |  |  |  |
| tom-godaddy | Tom | Tom (GoDaddy domain broker) | no | tom-godaddy.md | no | vendor (domain broker) | 3 |  |  | surname unknown |
| tom-merritt | Tom Merritt |  | no | no | tom-merritt (voice profile only) | unknown | 3 |  |  | v3 voice profile only; no role anywhere |

## Likely duplicates (same person under two slugs or names)

- karen-sartler (entity.md dm-heating, v2 karen-sartler.md, v3 karen-sartler) and karen-dodge (recordings/inbox/rec_0b2f65c077/speakers.md, human-confirmed 2026-10-01; recordings/lexicon.md). One person, two surnames across sources; the census uses karen-dodge. Needs Gordon.
- jeff-dm-heating (entity.md dm-heating) and jeff-goff (rec_0b2f65c077 speakers.md); v2 jeff.md is an auto stub from the same recording batch.
- tim-dm-heating (entity.md dm-heating) and tim-silva (rec_0b2f65c077 speakers.md, v2 tim-silva.md stub, v3 tim-silva).
- etieno-essien (Sancho work/entomat/business.md, lexicon "Eti") and v2 edi.md ("Edi", Entomat scientist). Likely one person; unconfirmed.
- grayson-erhard (Sancho) and v2 grayson-ehrhardt.md plus grayson.md stub; also amy-ehrhardt.md carries the v2 spelling.
- robert-nathan-allen (Sancho) and v2 rna.md.
- matt-mcintosh.md and mac.md in v2 are the same person (v2 says so in mac.md).
- leah-ashley.md and leah.md in v2 (pointer file and auto stub) are the same person.
- elliott-stark: v2 relationships/people/elliott-stark.md (stub), v2 work/partners/elliott-stark.md, v3 elliott-stark; one person. Not elliott-scott (Gordon's sibling).
- Four WoA partners have both a v2 people file and a v2 partners file: jack-heald, peter-nevland, zac-smith, (brian-brushwood has partners plus v3). One row each here.
- brittany-mitchells-magic (entity.md) and v3 brittany-bullock; v3 also notes a merged "Brittany" voice entry.
- david-mckinnis (Sancho knowledge.md plunkett) and "David McInnis" (v2 MANIFEST); spelling differs, likely one person.
- doug-huckaba (Sancho) and v2 doug.md (first name only); unconfirmed.
- "Craig" in knowledge.md plunkett-home-services may be craig-arthur; "Devin" in knowledge.md checkvet may be devin-wright; "Todd" in knowledge.md comfort-masters-dfw may be todd-lyles; "Luis" in knowledge.md travis-crawford-hvac is inferred to be luis-castaneda (v3 spells Casteneda). All unconfirmed.
- ali-woll vs allie-wickham: two different people that voice-to-text conflates (v2 flags it); allie-woll.md was the bad merge.
- kyle-heustis (v2 kyle.md) and the MANIFEST "Kyle (builder contact)" may be the same person.
- Same first name, different people, kept apart here: nicole-checkvet vs nicole-laura-friend; amanda-moore vs amanda-mikhail-partner; matt-dm-heating vs matt-builder vs matt-mcintosh vs matt-willis; chris-comfort-masters vs chris-noco-sportscenter vs chris-plunkett vs chris-torbay; gordon vs gordon-atkinson; megan-ohlmann vs megan-together-financial.

## Named in the Sancho tree but not rowed (name only, no role or relationship to carry)

- knowledge.md happy-outlet: team members pictured on the site, names from photo filenames only (Jason Thorkildson, Alex Arellano, Nate Aviero, Eric, Brett, Carmelo, Emily, Carla, Racheal, Renald).
- knowledge.md travis-crawford-hvac: staff with photos on file (Christopher Stone, Chris Baker, Charlie Ashe, Timothy Vanhoose); the unnamed new social media hire.
- knowledge.md dm-heating: technicians named in evidence (Alyssa, David, Erik, Sean, Kraig, Elijah); Karen's father (unnamed).
- knowledge.md society-hill-plumbing: crew named in reviews (Louis, Derrick, Dave); Greg's wife, daughter, brother and buddy Max; the unnamed former Philadelphia Gas Company employee; "Laney/Lainey" (Greg's mother).
- knowledge.md checkvet: "Lamira web person" (unclear whether a person or a firm); unnamed CSRs in action-air; two unnamed front desk hires in precision-chiro.
- knowledge.md mitchells-magic: Marty Ritchie (Myrtle Beach; a reference figure, not on the account).
- work/entomat/business.md: "Jake and Chris" at the VFW (not the WoA Jake as far as the evidence says).
- action-air: "Cheddar" is the Ohlmann family dog.

## v2 relationship-only names, not rowed (appear only as `entity:` targets or in body lines, no file and no MANIFEST row)

shane-mares (Ali Woll's husband), christina and mike (Allie Wickham's mother and fiance), patrick-esser (Leah's ex-spouse), leanne-smith (Zac Smith's wife), brenda-anderson (in ted-klontz.md), daniel-winning (Wizard Academy chancellor, in wizard-academy.md), vicki and goldie (Peter Nevland's wife and daughter), kris (Matt McIntosh's wife), joe-courant (Leah's late step-father), jes-jewitt (Rob Rowe's wife), carl-ullman and chelsea-ullman (in kay-ullman.md), kylie (Stephen Moore's daughter, in jack-heald.md), vincent (punchlist subcontractor, in nathan-gutters.md), patrick (Alexia's colleague).

## Skipped junk files in v2 relationships/people (not people, or not usable)

- Auto-created stubs from earballs processing whose "name" is not a person: and-and.md, but-but.md, channel-0.md, channel-1.md, cuddy-sark.md, google-ads.md, if-if.md, it-it.md, jack-daniels.md, so-so.md, south-bend.md, the-the.md, united-states.md, we-we.md, you-you.md.
- donald-trump.md: auto stub of a public figure mentioned in a recording; no relationship to Gordon on file.
- allie-woll.md: deprecated redirect (a bad merge of Ali Woll and Allie Wickham, resolved 2026-04-04 in v2).
- wizard-academy.md: type organization, not a person.
- MANIFEST.md: roster index (its "file needed" rows are folded into the table as "MANIFEST.md row only").
- john-marron-leah-summary.md and john-marron-working.md: type document, processing notes, not person files (folded into the john-marron row).
- gordon-seirup.md and leah-ashley.md are pointer files to v2 CORE.md and relationships/leah.md (folded into the gordon and leah rows).
- Auto stubs that ARE people and were folded into a row: elliott-stark.md, grayson.md, jeff.md, karen-sartler.md, leah.md, megan-together-financial.md, tim-silva.md, travis-crawford.md.
- v3 memory/people: every folder was kept as a row; most hold only a voice-profile.md (voiceprint enrollment record, no biography). hazel and tom-merritt have no role anywhere.

Census notes added by Cowork 2026-10-01: `karen-dodge` and `karen-sartler` are one person (Dodge is the maiden name, back in use after a divorce; Sartler was the married name) [gordon 2026-10-01]; file `people/karen-dodge.md` seeded; the backfill stage adds to it and `karen-sartler` gets no file of its own.

## Recomb 2026-10-01 (Cowork, after Gordon's moderation; proposal, job gated until he says go)

Rule learned [gordon 2026-10-01]: a slug that is a first name plus a client company is an employee of that company and belongs in the client's `knowledge.md` People section under the right name, not in a person file; first-name-only slugs are noise unless Gordon knows the person. Groups:


### A_noise_to_client_knowledge (44)
1. albert-plunkett
2. alicia-mitchells-magic
3. brittany-mitchells-magic
4. clarissa-dm-heating
5. jessica-happy-outlet
6. lucy-entomat
7. megan-together-financial
8. charlie-moger
9. jaden-lewis
10. tricia-lewis
11. jeremy-vargas
12. kyle-collins
13. jeff-collins
14. kevin-lin
15. andrew-mccanse
16. josh-plunkett-web
17. calvert-plunkett
18. dr-scheller
19. dr-johnson-checkvet
20. chelsea-entomat
21. chris-comfort-masters
22. chris-noco-sportscenter
23. cody-travis-crawford
24. david-comfort-masters
25. dirk-dm-heating
26. erica-comfort-masters
27. evan-mitchells-magic
28. george-mitchells-magic
29. mark-mitchells-magic
30. matt-dm-heating
31. nicole-checkvet
32. patience-checkvet
33. piper-comfort-masters
34. rondell-comfort-masters
35. sarah-service-excellence
36. sosa-travis-crawford
37. stephanie-dm-heating
38. stett-comfort-masters
39. stevie-comfort-masters
40. todd-comfort-masters
41. trish-precision-chiro
42. tyler-mitchells-magic
43. zakk-mitchells-magic
44. tara-checkvet


### B_client_principals (28)
1. amanda-moore
2. stephen-moore
3. christy-secoy
4. dan-griffiths
5. danelle-bullock
6. josh-bullock
7. greg-moore
8. jane-brewer
9. wes-brewer
10. olivia-la
11. tammy-parker
12. dr-hepworth
13. jared-james
14. jesse-olson
15. ken-goodrich
16. jordan-ohlmann
17. megan-ohlmann
18. marty-greer
19. jeff-carpenter
20. chris-plunkett
21. scarlett-plunkett
22. travis-crawford
23. karen-dodge
24. jeff-goff
25. tim-silva
26. kevin-skalure
27. jane-fisher
28. william-lordan


### C_woa_partners_team_vendors (41)
1. adam-donmoyer
2. brian-brushwood
3. carmyn-wilson
4. chris-torbay
5. mick-torbay
6. craig-arthur
7. daniel-whittington
8. dave-young
9. devin-wright
10. elliott-stark
11. gordon-atkinson
12. jack-heald
13. jake-williams
14. jason-skaggs
15. johnny-molson
16. kyle-caldwell
17. luis-castaneda
18. matt-willis
19. rick-willis
20. peter-nevland
21. robin-kressbach
22. roy-williams
23. ryan-chute
24. stephen-semple
25. steve-rae
26. syre-klenke
27. todd-lyles
28. tom-wanek
29. vi-wickam
30. cedric-yau
31. jeff-sexton
32. zac-smith
33. david-mckinnis
34. nathan-ingram
35. adrian-van-zelfden
36. pennie-williams
37. rex-williams
38. mark-effinger
39. pegeen-reilly
40. ryan-deiss
41. chris-lema


### D_ventures (6)
1. etieno-essien
2. dom-mcclellan
3. josh-agajanian
4. temple-grandin
5. amy-ehrhardt
6. billy-walker


### E_family (20)
1. maria-pia-seirup
2. elliott-scott
3. leslie-hong
4. bob-ratte
5. dora-ratte
6. jeffrey-ratte
7. pierre-ratte
8. beatrice-ratte
9. sara-moorehead
10. gina-cizek
11. joan-tropiano-tucci
12. stan-tucci-sr
13. stanley-tucci
14. luke-bernander
15. paula-bernander
16. teri-ashley
17. tom-boldt
18. ansel-courant
19. donna-thomas
20. guy-hanington


### F_friends_personal (40)
1. alex-post
2. allie-wickham
3. doug-huckaba
4. james-gilbert
5. larry-bloom
6. alexia-blackwood
7. ali-woll
8. amber-crummy
9. brent-ballard
10. chad-cohen
11. holly-cohen
12. dan-morman
13. dnelle-dowis
14. emily-sheehan
15. eric-pommier
16. laura-holden
17. gene-vann
18. greg-verbanic
19. isabel-jackson
20. jamie-joseph
21. john-marron
22. john-metcalf
23. kyle-heustis
24. lily-post
25. matt-mcintosh
26. mike-catan
27. mike-orth
28. mikhail-voloshin
29. patrick-rauland
30. rob-rowe
31. russell-quintero
32. scott-beasley
33. shannon-janelle
34. kay-ullman
35. mark-benn
36. ted-klontz
37. dr-mitch-janosik
38. stephanie-steward
39. john-mark-patterson
40. mark-goldrich


### G_gordon_decides (23)
1. dustin
2. isaac
3. lathan
4. delia
5. felix
6. hazel
7. paige
8. brian-neighbor
9. robin-neighbor
10. matt-builder
11. nathan-gutters
12. ryan-painter
13. tom-godaddy
14. gwen-goldrich
15. amanda-mikhail-partner
16. ella-jess-daughter
17. jess-paula-cousin
18. nicole-laura-friend
19. ren-rauland
20. sawyer-rauland
21. molly-bloom
22. tom-merritt
23. jenn-rahn


### existing_full (6)
1. gordon
2. leah
3. grayson-erhard
4. lizzie-mack
5. robert-nathan-allen
6. peter-seirup

## Gordon's moderation, 2026-10-01 (every line [gordon 2026-10-01]; the backfill stage for a slug writes its line into the file, cited)

### Reclassified out of "WoA partner" (still get files; group H, Wizard Academy circle)
- david-mckinnis: not a WoA partner; a seriously major donor to Wizard Academy.
- adrian-van-zelfden: not a partner; Roy Williams's CPA and attorney.
- pennie-williams: not a partner; Roy Williams's wife.
- rex-williams: not a partner; Roy Williams's son. Gordon's read: probably at least a low-level sociopath.
- mark-effinger: major Wizard Academy donor; former employee of David McKinnis; seriously into mushrooms, last Gordon checked.
- pegeen-reilly: Wizard Academy board member.
- ryan-deiss: Wizard Academy board member.
- chris-lema: not related to WoA at all; WordPress world. Moves to group F (industry contact).
- mike-catan: IS a WoA partner. Moves from F to C.

### Not in Gordon's mental rolodex (files still built from evidence, flagged `needs_gordon`; "the fact they're not in my mental rolodex says something")
- christy-secoy (Mitchell's Magic office/admin per v2), tammy-parker (fractional HR who ran Precision Chiro's front-desk hiring per v2), jane-fisher (D&M's local media buyer per v2): Gordon does not recognise them. Rule applies: client-side staff and vendors fold into the client's knowledge.md (group A), no person file.
- dom-mcclellan, josh-agajanian, billy-walker (venture-adjacent per v2 inference), john-mark-patterson (v2: a no-show attorney, no prior interaction), mark-goldrich (v2 manifest only): Gordon does not recognise them. Dropped from the job; rows kept here.

### Too small for a file
- dr-hepworth: known, but folds into precision-chiro/knowledge.md (group A).

### Group G, decided
- dustin: strike; D&M employee, into dm-heating/knowledge.md.
- isaac: Ignite HVAC client contact; into the Ignite client file (Copper Leaf client; folder to be created in B3/B4), no person file.
- lathan: partner in Evel Spirits (American Icon Spirits); keep, file.
- delia: ambiguous: Delia Marchison (friend) or Viader (client)? Gordon unsure; stage must show both readings and ask.
- felix: James Gilbert's partner; into people/james-gilbert.md, no own file.
- hazel: keep; aka Zach, and Azazel; last name unknown.
- paige: Paige Austin; former housecleaner, friend; keep.
- brian-neighbor: strike; into robin-neighbor's file.
- robin-neighbor: keep; pickleballer.
- matt-builder: keep.
- nathan-gutters: strike.
- ryan-painter: keep; Intermountain Painting; Gordon wants to refer him ("he's great").
- tom-godaddy: business contact, not a friend; keep as contact-only.
- gwen-goldrich: Gordon has no idea who this is; dropped.
- amanda-mikhail-partner: into people/mikhail-voloshin.md, no own file.
- ella-jess-daughter: strike; into paula-bernander's file.
- jess-paula-cousin: strike; into paula-bernander's file.
- nicole-laura-friend: strike.
- ren-rauland: keep; married to Patrick Rauland; friend; owns Audacious Immersive.
- sawyer-rauland: keep; Patrick and Ren's daughter.
- molly-bloom: keep; may become relevant later.
- tom-merritt: Gordon does not know who this is; dropped.
- jenn-rahn: Gordon does not know who this is; dropped.

### Corrections to kinds
- guy-hanington: not family; Leah's new boyfriend.
- larry-bloom: former professor more than a friend; a friend of Mark Benn.
- mark-benn: former professor and Gordon's shrink (psychologist).
- dr-mitch-janosik: Gordon's GP; friendly, never met outside the office.

### Sopris address book (2026-10-01)
`people/_sopris-locations.md` holds 104 kept households with addresses [gordon 2026-10-01 moderation]. A backfill stage for a slug that appears there fills `location.city` and the `contact.address` from that row, cited `[doc:people/_sopris-locations.md post <id>]` (an address Gordon keeps on his own list counts as stated by him). Melissa Meli's address is flagged for update; do not treat it as current.
