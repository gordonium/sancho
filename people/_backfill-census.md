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
| adam-donmoyer | Adam Donmoyer | Adam | no; entity.md + knowledge.md comfort-masters-dfw, dm-heating | adam-donmoyer.md | no | WoA media buyer | 1 |  |  |  |
| albert-plunkett | Albert |  | no; knowledge.md plunkett-home-services (wrap installer) | no | no | vendor (inferred) | 1 |  |  | surname not given |
| alex-post | Alex Post | Alex, Alexandra, Andrea | yes (thin); people/alex-post.md; work/tipelodeon/summaries/2026-09-15_rec_0d8753ed18.md | alex-post.md; MANIFEST.md row | alex-post (voice profile only) | friend | 1 |  |  | v2 gives legal name Andrea |
| alicia-mitchells-magic | Alicia |  | no; entity.md + knowledge.md mitchells-magic | no | alicia (voice profile only) | client person (marketing coordinator) | 1 |  |  | surname not given |
| allie-wickham | Allie Wickham | Allie | no; recordings/2026/rec_640701d84d/summary-personal.md ("Allie & Mike's wedding") | allie-wickham.md; MANIFEST.md row | no | friend | 1 |  |  | v2 flags Ali Woll vs Allie Wickham as a voice-to-text disambiguation risk; fiance Mike has no file |
| amanda-moore | Amanda Moore | Amanda | no; entity.md + knowledge.md comfort-masters-dfw | amanda-moore.md | no | client person (Comfort Masters co-owner) | 1 |  |  |  |
| andrew-mccanse | Andrew McCanse | Dr. Andrew McCanse | no; knowledge.md precision-chiro | no | no | client-adjacent (Vermont practice) | 1 |  |  |  |
| brian-brushwood | Brian Brushwood | Brian, Brushwood, shwood | no; knowledge.md travis-crawford-hvac (referenced, not on the account); work/wizard-of-ads/clients/_roster-evidence-v2.md (LottoEdge) | partners/brian-brushwood.md | brian-brushwood (voice profile only) | WoA partner | 1 |  |  |  |
| brittany-mitchells-magic | Brittany Bullock | Brittany, Bernie (transcript error) | no; entity.md + knowledge.md mitchells-magic | no | brittany-bullock (voice profile only) | client person | 1 |  |  | v3 gives surname Bullock; Sancho slug could become brittany-bullock |
| calvert-plunkett | Calvert |  | no; knowledge.md plunkett-home-services (vehicle-wrap production) | no | no | vendor (inferred) | 1 |  |  | surname not given |
| carmyn-wilson | Carmyn Wilson | Carmyn, Colin (former name) | no; recordings/inbox/rec_564c0541a8/summary.md and corrections.md | carmyn-wilson.md | carmyn-wilson (voice profile only) | WoA partner; friend | 1 |  |  |  |
| charlie-moger | Charlie Moger |  | no; knowledge.md checkvet, mitchells-magic (previous digital team) | no | no | vendor (inferred) | 1 |  |  |  |
| chelsea-entomat | Chelsea |  | no; work/entomat/business.md (family foundation contact) | no | no | venture contact (inferred) | 1 |  |  | surname not given; a different Chelsea (Ullman) appears in v2 kay-ullman.md |
| chris-comfort-masters | Chris |  | no; knowledge.md comfort-masters-dfw (technician) | no | no | client person | 1 |  |  | surname not given |
| chris-noco-sportscenter | Chris |  | no; knowledge.md precision-chiro (NoCo SportsCenter marketing director) | no | no | client-side contact | 1 |  |  | surname not given |
| chris-plunkett | Chris Plunkett | Chris | no; entity.md + knowledge.md plunkett-home-services | no | no | client person (Plunkett owner) | 1 |  |  |  |
| chris-torbay | Chris Torbay |  | no; entity.md + knowledge.md travis-crawford-hvac | no | chris-torbay (voice profile only) | WoA writer | 1 |  |  |  |
| christy-secoy | Christy Secoy |  | no; entity.md + knowledge.md mitchells-magic | no | no | client person (office/admin) | 1 |  |  |  |
| clarissa-dm-heating | Clarissa |  | no; entity.md + knowledge.md dm-heating | clarissa-dm-heating.md | no | client person (former front desk) | 1 |  |  | surname not given |
| cody-travis-crawford | Cody |  | no; knowledge.md travis-crawford-hvac ("electronic guy next door") | no | no | client-side contact | 1 |  |  | surname not given |
| craig-arthur | Craig Arthur | Craig | no; entity.md + knowledge.md action-air; knowledge.md plunkett-home-services names a "Craig (surname not given)" on the 2026-04-06 call | partners/craig-arthur.md | no | WoA partner | 1 |  |  | the Plunkett "Craig" may be the same person; unconfirmed |
| dan-griffiths | Dan Griffiths | Daniel Griffiths, Dan Greer (v2 error) | no; entity.md + knowledge.md checkvet | no | no | client person (CheckVet co-owner) | 1 |  |  | v2 wrote the surname as Greer; the signed MSA has Griffiths per knowledge.md |
| danelle-bullock | Danelle Bullock | Danelle | no; entity.md + knowledge.md mitchells-magic | no | no | client person | 1 |  |  |  |
| daniel-whittington | Daniel Whittington | Daniel | no; entity.md + knowledge.md plunkett-home-services | partners/daniel-whittington.md | daniel-whittington (voice profile only) | WoA partner; friend | 1 |  |  |  |
| dave-young | Dave Young | Dave | no; entity.md + knowledge.md plunkett-home-services | partners/dave-young.md | no | WoA partner | 1 |  |  |  |
| david-comfort-masters | David |  | no; knowledge.md comfort-masters-dfw (video producer) | no | no | vendor (inferred) | 1 |  |  | surname not given |
| david-mckinnis | David McKinnis | David McInnis | no; knowledge.md plunkett-home-services (Newsworthy.ai founder) | MANIFEST.md row as "David McInnis" (PRWeb founder; no file) | no | vendor / Wizard Academy donor (inferred) | 1 |  |  | spelling differs between Sancho (McKinnis) and v2 MANIFEST (McInnis); likely one person, unconfirmed |
| devin-wright | Devin Wright | Devin | no; entity.md + knowledge.md action-air; knowledge.md mitchells-magic; knowledge.md checkvet names a "Devin, radio buyer" | no | no | WoA media buyer | 1 |  |  | the CheckVet "Devin" may be the same person; unconfirmed |
| dirk-dm-heating | Dirk |  | no; knowledge.md dm-heating (Carrier rep) | no | no | vendor (inferred) | 1 |  |  | surname not given |
| doug-huckaba | Doug Huckaba | Doug | yes (thin); people/doug-huckaba.md; work/tipelodeon/summaries/2026-09-15_rec_21434802cb.md | doug.md (first name only, flooring crew) possibly the same person | no | friend | 1 |  |  | v2 doug.md is first-name only; same person unconfirmed |
| dr-hepworth | Dr. Hepworth |  | no; entity.md + knowledge.md precision-chiro | no | no | client referral contact (surgeon) | 1 |  |  | first name not given |
| dr-johnson-checkvet | Dr. Johnson |  | no; knowledge.md checkvet (Marshall) | no | no | client person (veterinarian) | 1 |  |  | first name not given |
| dr-scheller | Dr. Scheller |  | no; knowledge.md checkvet | no | no | client person (veterinarian) | 1 |  |  | first name not given |
| dustin | Dustin |  | no (pending request to create); rec_0b2f65c077/speakers.md human-confirmed 2026-10-01; knowledge.md dm-heating technicians list | no | no | client person (D&M staff) | 1 |  |  | surname not given; speakers.md slug is dustin, client-staff convention would be dustin-dm-heating |
| elliott-stark | Elliott Stark | Elliott | no; entity.md + knowledge.md dm-heating | elliott-stark.md (auto stub); partners/elliott-stark.md | elliott-stark (profile.md stub + voice profile) | WoA partner (writer) | 1 |  |  | three legacy files for one person |
| erica-comfort-masters | Erica |  | no; knowledge.md comfort-masters-dfw | no | no | client person (CSR) | 1 |  |  | surname not given |
| etieno-essien | Etieno Essien | Eti, Eddie (misheard), Edi (v2 spelling) | no; work/entomat/business.md; personal/me/brief.md; recordings/lexicon.md | edi.md (name given only as Edi) likely the same person | no | venture (Entomat partner) | 1 |  |  | LIKELY DUPLICATE of v2 edi.md (Entomat scientist); unconfirmed |
| evan-mitchells-magic | Evan |  | no; knowledge.md mitchells-magic (TV producer) | no | no | vendor (inferred) | 1 |  |  | surname not given |
| george-mitchells-magic | George |  | no; knowledge.md mitchells-magic (WoA partner on the account; surname unknown) | no | no | WoA partner | 1 |  |  | surname unknown |
| gordon | Gordon Seirup | Gordon, Gordonium, Gordo | yes (thin); people/gordon.md | gordon-seirup.md (pointer to v2 CORE.md) | gordon (voice profile only) | principal | 1 |  |  | v2 adds alias Gordo |
| gordon-atkinson | Gordon Atkinson | Atkinson | no; entity.md + knowledge.md society-hill-plumbing | partners/gordon-atkinson.md; MANIFEST.md row | no | WoA partner (writer) | 1 |  |  | not to be confused with gordon (Seirup) |
| grayson-erhard | Grayson Erhard | Grayson, Erhard, Grayson Ehrhardt | yes (full); people/grayson-erhard.md; work/tipelodeon; personal/ice/ice-2026-10-01-camping-with-grayson.md | grayson-ehrhardt.md; grayson.md (auto stub) | no | venture (Tipelodeon) | 1 |  |  | v2 spells the surname Ehrhardt; Sancho and lexicon use Erhard; grayson.md stub is the same person |
| greg-moore | Greg Moore | Greg | no; entity.md + knowledge.md society-hill-plumbing | no | no | client person (Society Hill owner) | 1 |  |  |  |
| isaac | Isaac | Iggy (lexicon) | no (pending people/isaac.md); recordings/inbox/rec_564c0541a8/summary.md (Ignite owner, Mankato MN); recordings/lexicon.md | no | no | client person (Ignite; CLC web-maintenance client per the summary) | 1 |  |  | surname not given; pending request uses slug isaac; client folder home (copper-leaf vs wizard-of-ads) undecided |
| jack-heald | Jack Heald | Jack | no; entity.md + knowledge.md comfort-masters-dfw | jack-heald.md; partners/jack-heald.md | no | WoA partner (writer) | 1 |  |  | two v2 files (people and partners) |
| jaden-lewis | Jaden Lewis | Jay Lewis | no; knowledge.md comfort-masters-dfw | no | no | client person (CSR) | 1 |  |  |  |
| jake-williams | Jake Williams | Jake | no; recordings/inbox/rec_564c0541a8/summary.md ("Jake", inferred to be Jake Williams) | MANIFEST.md row only (no file) | no | WoA (president) (inferred) | 1 |  |  | identity of the "Jake" in rec_564c0541a8 is inferred from the v2 MANIFEST role; unconfirmed |
| james-gilbert | James Gilbert | James | yes (thin); people/james-gilbert.md | james-gilbert.md | no | friend | 1 |  |  | v2 names a partner Felix in the first lines (see felix row) |
| jane-brewer | Jane Brewer | Dr. Jane Brewer | no; entity.md + knowledge.md precision-chiro | no (v2 has a client entity jane-brewer-precision-chiro, not a person file) | no | client person (Precision Chiro owner); CLC-PM client | 1 |  |  |  |
| jane-fisher | Jane Fisher |  | no; entity.md + knowledge.md dm-heating | no | no | media buyer (local) | 1 |  |  |  |
| jared-james | Jared James | Jared | no; work/wizard-of-ads/clients/_roster-evidence-v2.md (LottoEdge) | jared-james.md | no | client person (LottoEdge founder) | 1 |  |  |  |
| jason-skaggs | Jason Skaggs | Jason, Skaggs | no; entity.md + knowledge.md action-air; knowledge.md dm-heating | partners/jason-skaggs.md | no | WoA partner (writer) | 1 |  |  |  |
| jeff-carpenter | Jeff Carpenter |  | no; entity.md + knowledge.md travis-crawford-hvac | no | jeff-carpenter (voice profile only) | client person (GM) | 1 |  |  |  |
| jeff-collins | Jeff Collins |  | no; knowledge.md mitchells-magic (previous Cullins owner) | no | no | client person (former owner) | 1 |  |  |  |
| jeff-goff | Jeff Goff | Jeff | no (pending request to create); entity.md dm-heating lists jeff-dm-heating; rec_0b2f65c077/speakers.md has jeff-goff human-confirmed 2026-10-01; lexicon | jeff.md (auto stub, same recording batch as karen-sartler.md) | no | client person (D&M Heating co-owner) | 1 |  |  | two Sancho slugs (jeff-dm-heating, jeff-goff) for one person |
| jenn-rahn | Jenn Rahn |  | no; knowledge.md precision-chiro (bio and headshot on file; role not stated) | no | no | unknown | 1 |  |  |  |
| jeremy-vargas | Jeremy Vargas | Jay Vargas | no; knowledge.md comfort-masters-dfw | no | no | client person (operations/HR) | 1 |  |  |  |
| jesse-olson | Jesse Olson | Jesse | no; entity.md + knowledge.md happy-outlet | no | no | client person (Happy Outlet owner) | 1 |  |  |  |
| jessica-happy-outlet | Jessica |  | no; entity.md + knowledge.md happy-outlet | no | no | client person (staff) | 1 |  |  | surname not given |
| johnny-molson | Johnny Molson | Johnny | no; entity.md + knowledge.md checkvet | partners/johnny-molson.md | johnny-molson (voice profile only) | WoA partner | 1 |  |  |  |
| jordan-ohlmann | Jordan Ohlmann | Jordan | no; entity.md + knowledge.md action-air | no | no | client person (Action Air owner) | 1 |  |  |  |
| josh-bullock | Josh Bullock | Josh | no; entity.md + knowledge.md mitchells-magic | no | josh-bullock (voice profile only) | client person (Mitchell's Magic owner) | 1 |  |  |  |
| josh-plunkett-web | Josh | Yosh | no; knowledge.md plunkett-home-services (previous web developer) | no | no | vendor (inferred) | 1 |  |  | name heard as Yosh/Josh; surname not given |
| karen-dodge | Karen Dodge | Karen, Karen Sartler | no (pending request to create); entity.md dm-heating lists karen-sartler; recordings/inbox/rec_0b2f65c077/speakers.md has karen-dodge human-confirmed 2026-10-01; recordings/lexicon.md | karen-sartler.md (auto stub) | karen-sartler (voice profile only) | client person (D&M Heating owner) | 1 |  |  | NAME CONFLICT: v2, v3, entity.md and knowledge.md say Sartler; Sancho speakers.md and lexicon say Dodge [confirmed gordon 2026-10-01]; two Sancho slugs (karen-sartler, karen-dodge) for one person |
| ken-goodrich | Ken Goodrich | Ken | no; entity.md + knowledge.md happy-outlet | no | no | client-side advisor (inferred) | 1 |  |  |  |
| kevin-lin | Kevin Lin | Dr. Kevin Lin | no; knowledge.md precision-chiro | no | no | client-adjacent (Florida practice) | 1 |  |  |  |
| kevin-skalure | Kevin Skalure |  | no (pending request to create); rec_0b2f65c077/speakers.md human-confirmed 2026-10-01; lexicon (spelling unconfirmed) | no | no | client person (D&M Heating) | 1 |  |  | surname spelling unconfirmed per speakers.md |
| kyle-caldwell | Kyle Caldwell |  | no; entity.md + knowledge.md travis-crawford-hvac | no | kyle-caldwell (voice profile only) | WoA media buyer | 1 |  |  |  |
| kyle-collins | Kyle Collins |  | no; knowledge.md mitchells-magic | no | no | client person (Cullins) | 1 |  |  |  |
| larry-bloom | Larry Bloom | Molly Bloom's dad | yes (thin); people/larry-bloom.md; people/gordon.md | no | no | personal (former professor) | 1 |  |  |  |
| lathan | Lathan | Latham (misheard) | no; work/american-icon-spirits/business.md; recordings/lexicon.md | lathan.md; MANIFEST.md row | no | venture (American Icon Spirits co-owner) | 1 |  |  | surname not given anywhere |
| leah | Leah Ashley | Leah, Leah Elizabeth Ashley | yes (full); people/leah.md; entity.md precision-chiro, travis-crawford-hvac; knowledge.md People in checkvet, comfort-masters-dfw, dm-heating, happy-outlet, mitchells-magic, plunkett-home-services, precision-chiro, travis-crawford-hvac | leah-ashley.md (pointer; full file is v2 relationships/leah.md); leah.md (auto stub) | leah (voice profile only) | family (spouse); Copper Leaf operations | 1 |  |  | two v2 files for one person (leah-ashley.md, leah.md stub) |
| lizzie-mack | Elizabeth Mack | Lizzie, Lizzie Mack, Lizzie Mac | yes (full); people/lizzie-mack.md; work/entomat, work/american-icon-spirits | lizzie-mack.md | no | venture (Entomat, American Icon Spirits) | 1 |  |  |  |
| luis-castaneda | Luis Castaneda | Luis, Luis Casteneda | no; entity.md + knowledge.md comfort-masters-dfw; knowledge.md travis-crawford-hvac ("Luis, WoA Digital", inferred same) | no | luis-casteneda (voice profile only; spelling differs) | WoA PPC manager | 1 |  |  | v3 folder spells Casteneda |
| maria-pia-seirup | Maria Pia Seirup | Mom | no; referenced as "Mom" in work/copper-leaf/projects/hd-system-rebuild/docs/requirements.md:20 (identity unconfirmed there) | MANIFEST.md row only (no file) | no | family (mother) | 1 |  |  | Sancho doc says unconfirmed whether "Mom" is Maria Pia Seirup; v2 MANIFEST names her as Gordon's mother; v2 peter-seirup.md relationships list maria-pia-seirup |
| mark-mitchells-magic | Mark |  | no; knowledge.md mitchells-magic (media buyer; surname unknown) | no | no | WoA media buyer | 1 |  |  | surname unknown |
| marty-greer | Marty Greer | Dr. Marty Greer, Dr. Greer | no; entity.md + knowledge.md checkvet | no | no | client person (CheckVet owner) | 1 |  |  |  |
| matt-dm-heating | Matt |  | no; knowledge.md dm-heating (IT/hosting owner) | no | no | vendor (inferred) | 1 |  |  | surname not given; not the same as v2 matt-builder or matt-mcintosh as far as the evidence says |
| matt-willis | Matt Willis | Matt | no; entity.md + knowledge.md happy-outlet | no | no | WoA partner | 1 |  |  |  |
| megan-ohlmann | Megan Ohlmann | Megan | no; entity.md + knowledge.md action-air | no | no | client person (Action Air owner) | 1 |  |  |  |
| mick-torbay | Mick Torbay |  | no; entity.md + knowledge.md travis-crawford-hvac | no | mick-torbay (voice profile only) | WoA account team | 1 |  |  |  |
| molly-bloom | Molly Bloom |  | no; people/larry-bloom.md, people/lizzie-mack.md, people/gordon.md | no | no | reference (public figure, Larry Bloom's daughter) | 1 |  |  | probably no file needed; referenced only via larry-bloom |
| nathan-ingram | Nathan Ingram | Nathan, Ingram | no (pending people/nathan.md); entity.md + knowledge.md dm-heating; recordings/inbox/rec_564c0541a8/summary.md ("Nathan") | nathan-ingram.md | no | vendor and friend (web developer) | 1 |  |  | pending request names people/nathan.md; use nathan-ingram |
| nicole-checkvet | Nicole |  | no; knowledge.md checkvet (Marshall Pet Care office manager) | no | no | client person | 1 |  |  | surname not given; a different Nicole (Laura Holden's friend) is in v2 MANIFEST |
| olivia-la | Olivia La | Dr. Olivia La | no; entity.md + knowledge.md precision-chiro | no | no | client person (associate chiropractor) | 1 |  |  |  |
| patience-checkvet | Patience |  | no; knowledge.md checkvet | no | no | client person (social media) | 1 |  |  | surname not given |
| peter-nevland | Peter Nevland | Peter, Nevland | no (pending request to create); entity.md checkvet, comfort-masters-dfw, dm-heating, mitchells-magic; knowledge.md same; recordings/inbox/rec_0b2f65c077 and rec_564c0541a8 speakers.md human-confirmed 2026-10-01 | peter-nevland.md; partners/peter-nevland.md; MANIFEST.md row | peter-nevland (voice profile only) | WoA partner | 1 |  |  | two v2 files (people and partners); recordings/inbox/_pending-requests.md:33 already asks for people/peter-nevland.md |
| peter-seirup | Peter Seirup | Peter, Dad, Peter Seirup P.E., Gordon's dad, Gordon's father | yes (full); people/peter-seirup.md; entity.md home-directions | peter-seirup.md; MANIFEST.md row | no | family (father); CLC-PM client (Home Directions) | 1 |  |  |  |
| piper-comfort-masters | Piper |  | no; knowledge.md comfort-masters-dfw | no | no | client person (CSR) | 1 |  |  | surname not given |
| rick-willis | Rick Willis | Rick | no; entity.md + knowledge.md happy-outlet | partners/rick-willis.md | no | WoA partner | 1 |  |  |  |
| robert-nathan-allen | Robert Nathan Allen | RNA, R&A | yes (full); people/robert-nathan-allen.md; work/entomat | rna.md (name given only as RNA) | no | venture (Entomat) | 1 |  |  | v2 file is rna.md; same person per Sancho lexicon |
| robin-kressbach | Robin Kressbach | Robin | no; entity.md + knowledge.md plunkett-home-services | partners/robin-kressbach.md | no | WoA partner (design) | 1 |  |  |  |
| rondell-comfort-masters | Rondell |  | no; knowledge.md comfort-masters-dfw (technician) | no | no | client person | 1 |  |  | surname not given |
| roy-williams | Roy Williams | Roy, The Wizard | no; entity.md + knowledge.md society-hill-plumbing (advisor via the AWG course) | roy-williams.md | no | WoA founder; mentor | 1 |  |  |  |
| ryan-chute | Ryan Chute | Ryan | no; entity.md + knowledge.md happy-outlet, society-hill-plumbing | no | no | WoA partner | 1 |  |  |  |
| sarah-service-excellence | Sarah |  | no; knowledge.md society-hill-plumbing (Service Excellence, with Todd Lyles) | no | no | consultant (inferred) | 1 |  |  | surname not given |
| scarlett-plunkett | Scarlett Plunkett | Scarlett | no; entity.md + knowledge.md plunkett-home-services | no | no | client person (ops manager) | 1 |  |  |  |
| sosa-travis-crawford | Sosa |  | no; knowledge.md travis-crawford-hvac (previous digital/social person; last name unknown) | no | no | client person (former) | 1 |  |  | name as given |
| stephanie-dm-heating | Stephanie |  | no; knowledge.md dm-heating (office assistant) | no | no | client person | 1 |  |  | surname not given |
| stephen-moore | Stephen Moore | Steven Moore, Steve, Stephen, Steven | no; entity.md + knowledge.md comfort-masters-dfw | steven-moore.md | no | client person (Comfort Masters owner) | 1 |  |  | v2 file name uses Steven; name field says Stephen |
| stephen-semple | Stephen Semple | Stephen, Semple | no; entity.md + knowledge.md travis-crawford-hvac | partners/stephen-semple.md | stephen-semple (voice profile only) | WoA partner | 1 |  |  |  |
| stett-comfort-masters | Stett |  | no; knowledge.md comfort-masters-dfw (tech trainer) | no | no | client person | 1 |  |  | surname not given |
| steve-rae | Steve Rae | Steve | no; entity.md + knowledge.md society-hill-plumbing | MANIFEST.md row only (no file) | no | WoA partner (media buyer/advisor) | 1 |  |  |  |
| stevie-comfort-masters | Stevie |  | no; knowledge.md comfort-masters-dfw (office/data) | no | no | client person | 1 |  |  | surname not given |
| syre-klenke | Syre Klenke | Syre | no; entity.md + knowledge.md checkvet | partners/syre-klenke.md | no | WoA partner | 1 |  |  |  |
| tammy-parker | Tammy Parker |  | no; entity.md + knowledge.md precision-chiro (Unicycle Consulting) | no | no | client-side contractor (fractional HR) | 1 |  |  |  |
| tara-checkvet | Tara |  | no; knowledge.md checkvet | no | no | client person (former practice manager) | 1 |  |  | surname not given |
| tim-silva | Tim Silva | Tim | no (pending request to create); entity.md dm-heating lists tim-dm-heating; rec_0b2f65c077/speakers.md has tim-silva human-confirmed 2026-10-01; lexicon | tim-silva.md (auto stub) | tim-silva (voice profile only) | client person (D&M Heating co-owner) | 1 |  |  | two Sancho slugs (tim-dm-heating, tim-silva) for one person |
| todd-comfort-masters | Todd |  | no; knowledge.md comfort-masters-dfw (the connection to Peter Nevland; surname not given) | no | no | unknown | 1 |  |  | possibly todd-lyles; unconfirmed |
| todd-lyles | Todd Lyles | Todd | no; entity.md society-hill-plumbing; knowledge.md dm-heating, society-hill-plumbing | no | no | WoA partner; ops consultant (Service Excellence) | 1 |  |  | see todd-comfort-masters |
| tom-wanek | Tom Wanek | Tom, Wanek | no; entity.md + knowledge.md mitchells-magic | partners/tom-wanek.md | wanek (voice profile only) | WoA partner | 1 |  |  | v3 folder is surname only |
| travis-crawford | Travis Crawford | Travis | no; entity.md + knowledge.md travis-crawford-hvac | travis-crawford.md (auto stub) | no | client person (Travis Crawford HVAC owner) | 1 |  |  |  |
| tricia-lewis | Tricia Lewis | Tricia, T. Lewis | no; knowledge.md comfort-masters-dfw | no | no | client person (CSR) | 1 |  |  |  |
| trish-precision-chiro | Trish |  | no; knowledge.md precision-chiro (former office manager) | no | no | client person | 1 |  |  | surname not given |
| tyler-mitchells-magic | Tyler |  | no; knowledge.md mitchells-magic (technician) | no | no | client person | 1 |  |  | surname not given |
| vi-wickam | Vi Wickam | Vi, Vi Wickham | no; entity.md dm-heating (referral); _roster-evidence-v2.md (Service Professionals) | partners/vi-wickam.md | vi-wickam (voice profile only) | WoA partner (senior) | 1 |  |  | v2 spells Wickam; allie-wickham.md spells the family name Wickham |
| wes-brewer | Wes Brewer |  | no; entity.md + knowledge.md precision-chiro | no | no | client person (Jane's husband) | 1 |  |  |  |
| william-lordan | William Lordan | Bill Lordan, Dr. Lordan | no; knowledge.md precision-chiro (Precision Chiro CT) | no | no | CLC-PM client (DINABY site) | 1 |  |  | separate CLC client under _CLIENTS/Precision Chiro CT per knowledge.md |
| zakk-mitchells-magic | Zakk |  | no; knowledge.md mitchells-magic (Charlie Moger's team) | no | no | vendor (inferred) | 1 |  |  | surname not given |
| cedric-yau | Cedric Yau | Cedric | no | partners/cedric-yau.md | no | WoA partner (SEO) | 2 |  |  |  |
| dnelle-dowis | D'nelle Dowis | D'nelle, Dnelle | no | dnelle-dowis.md | no | friend; consulting client (v2 tag) | 2 |  |  |  |
| dom-mcclellan | Dom McClellan | Dom | no | dom-mcclellan.md; MANIFEST.md row | no | venture contact (spirits distribution) (inferred) | 2 |  |  |  |
| guy-hanington | Guy Hanington | Guy | no | no | guy-hanington (profile.md) | personal (Leah's partner) | 2 |  |  | v3 only; v3 status active |
| jeff-sexton | Jeff Sexton | Jeff | no | jeff-sexton.md | no | WoA partner | 2 |  |  | v2 file is tagged sensitive/discretion-required |
| josh-agajanian | Josh Agajanian | Josh | no | josh-agajanian.md; MANIFEST.md row | no | venture contact (potential partner) (inferred) | 2 |  |  |  |
| laura-holden | Laura Holden | Laura | no | laura-holden.md; MANIFEST.md row | no | friend; Press Managed client (v2 tag) | 2 |  |  |  |
| lucy-entomat | Lucy |  | no | lucy-entomat.md; MANIFEST.md row | no | venture (Entomat partner) | 2 |  |  | surname not given |
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
| megan-together-financial | Megan | Megan (Together Financial) | no | megan-together-financial.md (auto stub) | no | unknown (vendor contact, inferred) | 3 |  |  | stub only; a different Megan (Paige's roommate) appears in paige.md |
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
