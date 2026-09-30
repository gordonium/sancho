---
name: WordPress updates across all client sites, with post-update tests
id: ice-2026-09-30-wp-updates-with-tests
title: WordPress updates across all client sites, with post-update tests
type: idea
lobe: work
area: copper-leaf
project:
description: WordPress updates across all client sites, with post-update tests
captured: 2026-09-30
source: "[gordon 2026-09-30]"
status: captured
next_review: 2026-11-02
log:
  - 2026-09-30 captured from _design/seeds/work-ice.md
---
# WordPress updates across all client sites, with post-update tests
- **Area:** copper-leaf (and press-managed brand). Stacked skill on top of the kit.
- **What:** run core/plugin/theme updates on every client site, then prove nothing broke: visual regression (before/after screenshots of key pages), form submissions, live checkouts on e-commerce sites, and other per-site functional checks.
- **Review questions:** this touches **production**, which the kit's rules and the live-site guard currently forbid Claude to change; the MVP needs an explicit, gated exception (per site or per batch, human approval before and a rollback path after), probably built as a kit skill (`site-update`) with the same human gates as `plugin-ship`. Where do the per-site test definitions live (the plugin registry in `work/copper-leaf/plugins/`, extended to sites)? What's the rollback (SiteDistrict snapshot? staging first?). Leah likely runs this; Astra needs it too, so it's a shared business skill (§15.2).
