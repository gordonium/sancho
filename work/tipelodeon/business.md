---
name: Tipelodeon
type: business
lobe: work
stake: partial 20%
status: active
description: Formerly SongTipper; Grayson Erhard is founder, owner and primary developer; Gordon holds 20%
sources: ["[gordon 2026-09-21]", "[gordon 2026-09-26]"]
---
Formerly SongTipper; Grayson Erhard is founder, owner and primary developer; Gordon holds 20% [gordon 2026-09-21]

## Reference (from recordings)
- Lyrics: no publisher license at launch. Users upload their own lyrics and get only their own back; DMCA agent registration for safe harbor; the cached-lyrics feature is mothballed or super-user-gated; in-app message frames it as a licensing-money problem on the roadmap [rec_9c3c3bbece 2026-09-11 00:04:50, 00:10:44, 00:14:40]
- No subscription or pricing decisions until a year of real fee data; licensing deals are a post-revenue money play, negotiated as long multi-year contracts while small [rec_9c3c3bbece 2026-09-11 00:07:24, 00:13:25]
- Platform earns roughly 10% of what performers make (Grayson's figure) [rec_9c3c3bbece 2026-09-11 00:07:48]
- Competitor: Ultimate Guitar, licensed with the majors; its moat is the one Tipelodeon would need [rec_9c3c3bbece 2026-09-11 00:12:35]
- Core pillar as stated: not making money off the musician; costs passed through, big-business music industry is the villain [rec_9c3c3bbece 2026-09-11 00:06:48, 00:14:40]
- Lyrics vendors: LyricFind (conversation opened by Grayson; they wanted a call, Grayson prefers email) and Musixmatch (~$2,000/month quoted; too much pre-revenue). Ask: cache on our server and pay per deduplicated song; willing to contractually give up public lyric display, public search and fragment search for a better price [rec_0d8753ed18 2026-09-15 00:04:21, 00:05:35, 00:06:27, 00:07:38]
- Charts: legal sourcing runs through Hal Leonard / Harry Fox Agency; chords transcribed by someone else carry an engraver's license; Tipelodeon's position is the user uploads the chart and initiates the ChordPro conversion [rec_0d8753ed18 00:12:35, 00:36:12]
- Ultimate Guitar exporter is the riskiest piece (users copying licensed material through our tool). Gordon's fix: the exporter pulls only song titles and artists, and Tipelodeon supplies properly licensed charts [rec_0d8753ed18 00:32:10–00:38:04]
- Risk posture agreed 2026-09-15: low exposure surface (don't advertise or walk through the sensitive features), actively pursue licensing, keep a good-faith paper trail; the industry would rather collect from a cash-flowing business than kill it [rec_0d8753ed18 00:15:51–00:18:27]
- Attorney: Brian (did the operating agreement). Grayson's rule: do most of the legwork with AI, bring Brian specific questions to check, so he's familiar enough to stand behind it in court; also ask him whether he's right for patents [rec_0d8753ed18 00:01:36, 00:18:27, 00:19:26, 00:43:27]
- Patents: Grayson wants to find what's patentable in case Ultimate Guitar builds its own tipping; licensing first, patents later [rec_0d8753ed18 00:42:43, 00:44:44]
- Apple: as of 2026-09-15 the business (not the app; app not yet submitted) was stuck in review, forwarded to a senior person; Tipelodeon can't go live until it can say lyrics are licensed [rec_0d8753ed18 00:21:30–00:22:20]
- Milestones (Gordon): 1) Apple approval, App Store release, website written, built and launched; 2) content engine: Monday-morning weekend-in-review on Zoom (even while Grayson tours), weekly feature walkthroughs, user interviews, a weekly content roadmap; 3) funded video ads, sized by cash flow [rec_0d8753ed18 00:23:59]
- Radio idea (Gordon): after revenue, a 52-week schedule in Nashville (~$4–5k/month guess) to become a household name among musicians; run past his Wizard of Ads sages first [rec_0d8753ed18 00:48:43, 00:51:37, 00:53:06]
- Seasonality (Grayson): summer is too busy for musicians to switch platforms; Jan–Mar is when big signups happen; Jan–Feb is a dead zone for gigs, picks up in March, dies off in October [rec_0d8753ed18 00:54:05–00:55:32]
- Target: solo and duo musicians first; Grayson knows most of the acts in Chris Brown's booking list ("One One Live", name unverified) [rec_0d8753ed18 00:50:14]
- Ops: in-app bug reporting exists; Grayson is building a Sentry + scheduled Claude loop (3 am) that reads new errors, opens self-healing PRs and updates Flutter and packages [rec_0d8753ed18 00:56:49, 00:57:22]
- Design standard (Gordon): simple, obvious, convenient, every screen [rec_0d8753ed18 00:47:55]
- Weekly Gordon–Grayson call: on for 9/23, skipped 9/30 and 10/7, back 10/14 [rec_0d8753ed18 00:28:18]
- Website copy: not written before Italy; Gordon amended this with Grayson: he'll power-dump the copy on the flights home (~2026-10-07) [gordon 2026-10-01]
- Wizard of Ads: Roy Williams waived his 15% on Gordon's Tipelodeon cut, 2026-09-21, "this is not a precedent"; his read: a goofy tech startup, selling to musicians is the hard part, a coin toss at best [rec_c7110cf37e 2026-09-21 00:48:07, 00:51:45, 00:52:34]


## Added 2026-10-02 (batch B3, from legacy evidence; every line cited; legacy lines are history until confirmed)

Target: `work/tipelodeon/business.md`. Append below the existing text; no existing line changes.
Legend: `[v3:<path>:<line>]` = jarvis-v3 `work/tipelodeon/` (best-kept folder; its CONFIRMED / LOCKED flags are cited as such), `[v2:<path>:<line>]` = gordon-os-v2. Every legacy line is history, unconfirmed since its date. Note: v2 holds Tipelodeon files dated 2026-09-10, newer than anything in the v3 folder (latest 2026-07-22); where they disagree the v2 Sept files win on date.

## What it is
- Tipelodeon, formerly SongTipper; Grayson is founder, owner and primary developer; Gordon owns 20% [gordon 2026-09-22].
- An app that lets the audience at small gigs scan a QR code, search the performer's repertoire, request a song and tip with it; built for "small gig working for TIPS performers" (history, as of 2026-07-21, unconfirmed since) [v3:work/tipelodeon/self-babble-2026-07-21-summary.md:21] [v3:work/tipelodeon/self-babble-2026-07-21-summary.md:102-108]
- Alongside tipping it ships free utilities (setlist, chart and live request management) that work whether or not money moves; v2's character diamond calls these the brand's "surprise" (history, as of 2026-09-10, unconfirmed since) [v2:work/clients/tipelodeon-character-diamond.md:29-30]
- Core value as Gordon frames it: "We never make money from the musician. We make money from the audience, same as you do." (history, as of 2026-09-10, unconfirmed since) [v2:work/clients/tipelodeon-character-diamond.md:32-33] [v3:work/tipelodeon/tipelodeon.md:172-177]
- Rename: SongTipper became Tipelodeon, locked 2026-05-07 after Grayson signed off between 4/22 and 5/7 (history, as of 2026-05-07, unconfirmed since) [v2:work/clients/songtipper-ads-system.md:8]
- Entity: an LLC with Grayson as Managing Member, to be registered in Colorado (history, as of 2026-07-21, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:33] [v3:work/tipelodeon/tipelodeon.md:48]

## People
- Grayson (Sancho spells "Erhard"; v2 and v3 spell "Ehrhardt", unresolved): musician and developer; built the app; owned all pre-existing code, app and brand IP (history, as of 2026-03-17, unconfirmed since) [v3:work/tipelodeon/partnership-notes.md:24-30]. Gordon gave Grayson his first job out of college (history, as of 2026-07-21, unconfirmed since) [v3:work/tipelodeon/self-babble-2026-07-21-summary.md:238]
- Gordon: marketing strategist, writer and capital; runs marketing ("will run by Grayson but not asking permission"), stays out of tech (history, as of 2026-07-21, CONFIRMED in v3 6/17 section, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:103-105]
- Brian Hanning: attorney, Fort Collins; engaged for Tipelodeon 2026-06-09; flat fee, most projects under $1,500, $225/hour for reviews (history, as of 2026-07-21, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:326-333]. Sancho already has "Attorney: Brian" from rec_0d8753ed18.
- Leah: proposed bookkeeper at market rate (history, as of 2026-07-21, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:340]
- ~~Brian Brushwood: advisor at $2K upfront + $500/month for 6 months + 2% equity~~ (history, as of 2026-03-17) [v3:work/tipelodeon/partnership-notes.md:91] [superseded by v3 2026-06-10: "Brushwood out of the deal entirely" [v3:work/tipelodeon/v3.1-model-spec.md:30-33] and 6/17 "No Brushwood. No advisor pool." [v3:work/tipelodeon/tipelodeon.md:75]]
- Adelita's Way: touring band; their manager Rick wanted someone to oversee a Tipelodeon rollout on their tours; Grayson invited Gordon on the bus (history, as of 2026-07-16, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:60] [v3:work/tipelodeon/tipelodeon.md:246-252]

## Numbers
- Ownership CONFIRMED 2026-06-17: Grayson 80% (Class A, sweat, immediate); Gordon 15% Class A sweat + 5% Class B capital (history, as of 2026-07-21, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:65-71]. Matches Gordon's 20% [gordon 2026-09-22].
- Valuation $400K; Gordon's capital is $20K for 5%; Grayson's IP valued at $320K in the OA v2 draft (history, as of 2026-07-21, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:31] [v3:work/tipelodeon/tipelodeon.md:73] [v3:work/tipelodeon/oa-v2-review-notes.md:18]
- Gordon's expansion right: up to $52K more at the same $400K valuation in $4K minimum chunks until annual revenue exceeds $400K; capital equity capped at 18%; each addition needs Grayson's approval (history, as of 2026-07-21, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:85-89]
- ~~Ownership shapes before 6/17: 3/25 Gordon 15% sweat + 2 to 5% capital; 5/20 Grayson 67 / Gordon 15 + 3 / Brushwood 2 / advisor pool ~13; 6/10 Grayson 75 / Gordon 25~~ [v3:work/tipelodeon/partnership-notes.md:277] [v3:work/tipelodeon/tipelodeon.md:385-387] [superseded by v3 6/17 CONFIRMED 80/20 [v3:work/tipelodeon/tipelodeon.md:388]]
- Platform fee schedule (current on disk): a banded fee paid by the audience, built by Gordon, banding deliberate; $2 up to a $50 tip then stepping up through 27 bands to $320 at $9,501 to $10,000, targeting about 3.2 to 4.4% of the tip; bands sit just above round numbers so the round number stays in the cheaper band; rebalanced the same day so no band runs negative (history, as of 2026-09-10, unconfirmed since) [v2:work/clients/tipelodeon-pricing-tiered-fee-2026-09.md:8] [v2:work/clients/tipelodeon-pricing-tiered-fee-2026-09.md:11] [v2:work/clients/tipelodeon-pricing-tiered-fee-2026-09.md:43-45] [v2:work/clients/tipelodeon-pricing-tiered-fee-2026-09.md:98-100] [v2:work/clients/tipelodeon-pricing-tiered-fee-2026-09.md:119-121]
- ~~Fee table $0-50 = $2, $50-100 = $4, $100-250 = $10, $250-650 = $20~~ (history, as of 2026-07-16) [v3:work/tipelodeon/tipelodeon.md:254-263]; ~~extended on 7/21 with $600-1000 = $30~~ [v3:work/tipelodeon/self-babble-2026-07-21-summary.md:150-156] [superseded by the v2 banded schedule, 2026-09-10]
- ~~Earnings-based subscription: free until $200/month in tips, then $20/month, $50/month above $2,500, with auto-pause and catch-up billing~~ (history, as of 2026-03-25) [v3:work/tipelodeon/partnership-notes.md:248-250] [v3:work/tipelodeon/partnership-notes.md:324] [superseded: Gordon's 7/21 story says that model was dropped as "too goddamn convoluted" [v3:work/tipelodeon/self-babble-2026-07-21-summary.md:221], replaced by the audience-paid fee]
- Tip-back program (Tipelodeon pays performers at milestones), fixed ladder v2: $5 first tipped gig, $5 at $100 platform revenue, $10 at 10th gig, $20 first 8-gig month, $10 bad night after 3 months, $100 at 100th gig, $52 or $12 on the first-gig anniversary; capped at $202 per performer lifetime and self-funding except the first $5 (history, as of 2026-09-10, unconfirmed since) [v2:work/clients/tipelodeon-tip-back-program.md:99-110] [v2:work/clients/tipelodeon-tip-back-program.md:118] [v2:work/clients/tipelodeon-tip-back-program.md:128]
- Traction: 9 beta users (up from 4 on 6/17); Grayson himself $1K+/month in tips on the platform (history, as of 2026-07-21, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:52-53]. Earlier: Grayson went from $40 to $400 in tips at the same venue; $187 through the app across 3 gigs in March 2026 (history, as of 2026-03-25, unconfirmed since) [v3:work/tipelodeon/partnership-notes.md:248-249]
- Legal budget: ~$4K to $5K all-in (trademark ~$1,500, LLC $50, OA, EULA $1K to $1.5K, ToS) (history, as of 2026-07-21, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:334]
- Grayson's own platform-take figure (~10% of what performers make) is in the existing Reference lines [rec_9c3c3bbece 2026-09-11].

## History
- 2026-03-15: first deal conversation; Gordon pitches a minority stake ("not a 50/50 thing"); product already on Stripe Connect Express with all money flowing to the musician (history, as of 2026-03-17, unconfirmed since) [v3:work/tipelodeon/partnership-notes.md:63-78]
- 2026-03-18: ~~exit agreed as build-to-sell, 2 to 5 years, not less than 7 figures~~ [v3:work/tipelodeon/partnership-notes.md:174-178] [superseded by v3 2026-07-16: still build-to-sell in theory, but Gordon "I'd rather ride it all the way out than watch somebody hollow out my baby and kill it" [v3:work/tipelodeon/tipelodeon.md:233-234]]
- 2026-03-25: DJs ruled out as a market; houses of worship flagged as a large new market (history, unconfirmed since) [v3:work/tipelodeon/partnership-notes.md:210-213] [v3:work/tipelodeon/partnership-notes.md:256-259]
- 2026-05-07: rename to Tipelodeon locked (history, unconfirmed since) [v2:work/clients/songtipper-ads-system.md:8]
- 2026-06-09: Brian Hanning engaged; 2026-06-17 ownership 80/20 CONFIRMED and spending thresholds LOCKED (history, as of 2026-07-21, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:329] [v3:work/tipelodeon/tipelodeon.md:65] [v3:work/tipelodeon/tipelodeon.md:109]
- 2026-07-16: Adelita's Way tour opportunity (Sept 2026, maybe Nov 2026, Feb 2027); request-taking feature launch set for 2027 (history, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:247-248]
- 2026-07-21: Grayson's OA v2 revisions memo reviewed for Gordon (history, unconfirmed since) [v3:work/tipelodeon/oa-v2-review-notes.md:7]
- 2026-07-22: website site map, homepage angle ("sitting across from this person in the bar... sharing the secret") and "pricing conspicuously absent from the homepage" LOCKED (history, unconfirmed since) [v3:work/tipelodeon/website-outline-v1.md:26-40]
- 2026-09-10: character diamond drafted; banded fee schedule built and rebalanced; tip-back ladder set, with song-play awards moved to manual discretion (history, unconfirmed since) [v2:work/clients/tipelodeon-character-diamond.md:19] [v2:work/clients/tipelodeon-pricing-tiered-fee-2026-09.md:22] [v2:work/clients/tipelodeon-tip-back-program.md:151-153]

## How it works
- Product flow: audience scans a QR code, picks from the repertoire, picks a tip (optional), pays by card or wallet; requests arrive sorted by price; the performer marks them played and opens the chart; after-gig stats show top-earning songs and average tip (history, as of 2026-07-21, unconfirmed since) [v3:work/tipelodeon/self-babble-2026-07-21-summary.md:134-137]
- Setup: import a song list (200 songs went from an hour to two minutes via RapidSoundNet and MusicBrainz), receive a QR code and a printable PDF; "bare metal" two-minute onboarding offered alongside full setup (history, as of 2026-07-21, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:55] [v3:work/tipelodeon/tipelodeon.md:287-296] [v3:work/tipelodeon/self-babble-2026-07-21-summary.md:135]
- Money: tips flow to the performer's own Stripe Connect Express account; the audience pays Tipelodeon's fee; Tipelodeon pays the card fees (history, as of 2026-07-21, unconfirmed since) [v3:work/tipelodeon/partnership-notes.md:68] [v3:work/tipelodeon/self-babble-2026-07-21-summary.md:158]
- Governance: percent-weighted voting, so Grayson decides; Gordon can't block; the OA v2 draft adds mutual no-ouster protection and a short unanimous list (amendments, ownership changes, admissions, transfers, dissolution, sale, member pay, IP) (history, as of 2026-07-21, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:97-98] [v3:work/tipelodeon/oa-v2-review-notes.md:19-20]
- Spending rule LOCKED 6/17: single first-time purchase limit = $2,000 + 10% of cash reserve + 10% of last month's revenue, max 3 large purchases a month, leases count at total contract value (history, as of 2026-07-21, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:109-125]. Contested in OA v2, see Open threads.
- Waterfall: hard costs, then a cash reserve (20% of positive operating cash flow, starting early), then Grayson takes everything up to $2K/month, then 80/20 distributions; no W-2 salary by default (history, as of 2026-07-21, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:147-162]. OA v2 sets Grayson's priority at $2,500/month, which means Gordon reaches $2K/month only at $12,500/month net income (history, as of 2026-07-21, unconfirmed since) [v3:work/tipelodeon/oa-v2-review-notes.md:78-88]
- IP: Grayson's pre-existing code and brand stay his; company IP after formation belongs to the LLC; Gordon's marketing IP assigned on creation; OA v2 conditions the IP assignment on Gordon's $20K arriving (history, as of 2026-07-21, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:222-227] [v3:work/tipelodeon/oa-v2-review-notes.md:24]
- Gordon's role in practice: marketing lead (strategy, all copy, ad production and buying, website); the client-style rule applies, Grayson gets go/no-go on ads, not word-by-word edits (history, as of 2026-03-25, unconfirmed since) [v3:work/tipelodeon/partnership-notes.md:276-279]. Content plan: 30 days of daily organic content before any paid ads (history, as of 2026-06-17, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:300-306]
- Standing meeting: Wednesdays 10am (history, as of 2026-07-21, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:372]; the Sept/Oct schedule is in the existing Reference lines.

## Open threads
- As of 2026-07-21, six OA v2 items for Gordon and Grayson to settle before send-back to Brian (history, unconfirmed since) [v3:work/tipelodeon/oa-v2-review-notes.md:119-126] [v3:work/tipelodeon/oa-v2-review-notes.md:146-153]:
  1. Vesting: Grayson's v2 has the 15% sweat vest only after passing reviews at 12, 18 and 24 months, with two warnings in 12 months forfeiting all 15% at $0; Gordon's position was a single vest at 12 months or cash-flow-positive, whichever first [v3:work/tipelodeon/oa-v2-review-notes.md:43-47]
  2. Drag-along floor $250K in the first 36 months vs Gordon's "7 figures" [v3:work/tipelodeon/oa-v2-review-notes.md:67-69]
  3. Spending cap: v2 has a flat $2,500 with a 3% annual escalator, dropping the LOCKED 6/17 formula [v3:work/tipelodeon/oa-v2-review-notes.md:57-59]
  4. Schedule 2 deliverables for Gordon (5 hours a week, 2 posts a week across 4 platforms, 1 asset a month, 1 campaign a quarter, monthly report) [v3:work/tipelodeon/oa-v2-review-notes.md:98-103]
  5. Symmetric specificity for Grayson's own deliverables [v3:work/tipelodeon/oa-v2-review-notes.md:110]
  6. Arbitration provider (AAA or JAMS) and non-compete geography [v3:work/tipelodeon/oa-v2-review-notes.md:122-123]
- As of 2026-07-21: sequence still OA, Colorado registration, EIN, bank account, then Gordon's $20K, then pay Brian (history, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:48]. Whether the OA is signed is not on disk.
- As of 2026-07-21: conflict-driven buy-sell ("civilization breakdown") still unsolved (history, unconfirmed since) [v3:work/tipelodeon/tipelodeon.md:218-220]
- As of 2026-09-10: which fee table is live (Table 2 still has the wrong formula); per-session fee cap or end-of-night tab for repeat tippers; chargeback exposure on large tips; tip-back delivery rail and the definition of a "gig" (history, unconfirmed since) [v2:work/clients/tipelodeon-pricing-tiered-fee-2026-09.md:67] [v2:work/clients/tipelodeon-pricing-tiered-fee-2026-09.md:78] [v2:work/clients/tipelodeon-pricing-tiered-fee-2026-09.md:110] [v2:work/clients/tipelodeon-tip-back-program.md:43-44]
- As of 2026-09-10: proposed monthly ritual for manual awards (first Wednesday, end of the standing meeting) not confirmed (history, unconfirmed since) [v2:work/clients/tipelodeon-tip-back-program.md:167]
- As of 2026-09-10: character diamond archetype not chosen (history, unconfirmed since) [v2:work/clients/tipelodeon-character-diamond.md:47]
- Website copy: see existing line (Gordon to write it on the flights home ~2026-10-07) [gordon 2026-10-01].
</content>
</invoke>
