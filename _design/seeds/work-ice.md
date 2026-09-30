---
name: Work ICE seeds
type: doc
lobe: work
description: Capability ideas captured during Phase 2, to be filed as individual ICE entries in work/ice/ at scaffold
status: seed
---
# Work ICE seeds (captured 2026-09-30)

Each becomes its own file in `work/ice/` at scaffold, `status: captured`, `next_review` at the first monthly work review. All from Gordon; none approved for MVP yet. Listed with the first questions each would face at review.

## 1. WordPress updates across all client sites, with post-update tests
- **Area:** copper-leaf (and press-managed brand). Stacked skill on top of the kit.
- **What:** run core/plugin/theme updates on every client site, then prove nothing broke: visual regression (before/after screenshots of key pages), form submissions, live checkouts on e-commerce sites, and other per-site functional checks.
- **Review questions:** this touches **production**, which the kit's rules and the live-site guard currently forbid Claude to change; the MVP needs an explicit, gated exception (per site or per batch, human approval before and a rollback path after), probably built as a kit skill (`site-update`) with the same human gates as `plugin-ship`. Where do the per-site test definitions live (the plugin registry in `work/copper-leaf/plugins/`, extended to sites)? What's the rollback (SiteDistrict snapshot? staging first?). Leah likely runs this; Astra needs it too, so it's a shared business skill (§15.2).

## 2. Monthly reporting data for WoA clients, gathered by API
- **Area:** wizard-of-ads. Per client.
- **What:** pull Google Search Console, GA4, Google Business Profile, Local Services Ads, and Google Ads data monthly into a per-client report; **fetch the LSA Phone Responsiveness score via API**, which alone replaces a $160/month tool.
- **Review questions:** which client folders need which sources (a `reporting:` block in `entity.md`); OAuth for five Google APIs on the Mac (one Google Cloud project, one consent, tokens in the encrypted secrets file); output template per client; the Phone Responsiveness fetch is the obvious first MVP because the ROI is immediate and it's one API. Runs as a scheduled command on the Mac; the report draft is a skill.

## 3. Wrike time logs → client billing sheets; timesheet audit → invoice list
- **Area:** copper-leaf / wizard-of-ads (whichever bills by time).
- **What:** read logged time from Wrike tasks and transcribe it into each client's Google Doc/Sheet timesheet (or a new, better structure); then audit all client timesheets and present the list of invoices to send.
- **Review questions:** read-only Wrike access first (already an ICE item, §17.4); write access to Google Sheets is a new capability with a must-never nearby (Sancho writes to the sheet, but Gordon sends the invoice); whether the "new improved system" is a Sheet or a Markdown ledger in the client folder with a generated Sheet view. Natural second step after #2's Google OAuth exists.

## 4. Map Copper Leaf operations for automation opportunities
- **Area:** copper-leaf.
- **What:** read (never send) the CLC operations mailbox and Wrike activity to map what the recurring operational work actually consists of, then propose what can be automated.
- **Review questions:** read-only by construction (mail READ scope only; the email must-never stands); a time-boxed analysis (one month of data), then a report and a list of candidate skills.

## Notes for Phase 3
- #1 produces a **shared business skill** for Astra; #2 and #3 are Gordon's own.
- #2's Phone Responsiveness fetch is the smallest, highest-ROI MVP on this list.
- "Never touch live" will be dialed in when #1 is designed: updates run in staging, then are promoted to live through a gated step; the exact workflow is a later conversation.
