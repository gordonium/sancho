# Post-mortem: why v2 and v3 failed (Gordon's words, lightly cleaned)

Started 2026-09-21. This file is the checklist of problems Sancho guards against in every later phase. Each answer is written as Gordon gives it; "Implication" lines are Claude's reading, to be confirmed.

## Q1. What broke?

- **v3 never got off the ground.** It has nice groundwork and ideas, but it is nascent at best. Treat it as a design sketch, not a working system.
- **v2 was the last fully robust version.** There was a hacked-together "v2.5" at some point.
- **v2 became unreliable.** Gordon can't recall a single big cause, but names two:
  1. **Too many skills stacked on skills that bumped into each other.** Overlapping triggers, overlapping jobs.
  2. **Data drift from incoming recordings and transcriptions not getting correctly attributed.** Speaker/client attribution errors in the earballs pipeline propagated into the knowledge base.
- **"Go ask v2 how and why it failed. It knows."** v2 likely has its own record of failures (closeout notes, decision logs, attribution-correction history, error notes). Phase 1 survey must send a subagent specifically to look for v2's self-diagnosis and report it as evidence.

Implications for Sancho (to confirm):
- Skill count and trigger scope are a first-class design constraint, not a cleanup task.
- Attribution in the pipeline needs a verification step before facts enter the tree (ties to Phase 2 decision #2, provenance).
- Add to Phase 1: "v2's own account of its failures" as a survey section.

## Q2. What did he do about it / what did he stop trusting?

- **"Skills" in v2 were mostly routines**, not formal skills. Gordon discovered formal skills late. Much of v2 was prose routines (MD files) stacked on each other.
- **The system built enthusiastically and sounded competent** about how it was building and testing things, but the quality that came out did not match the confidence going in. Claimed tests did not equal real tests.
- **Two failures at once:**
  1. Complex systems got big, out of control, untested, unreliable.
  2. Too many things ran at once, none polished. Waiting through the chatter became frustrating.
- **The startup routine looked at too many things, so he stopped using it.** That was the concrete trust break: the entry point became the tax.
- **Triggering was inverted.** Routines cropped up when not needed and failed to appear when needed.

Implications for Sancho (to confirm):
- "Tested" must mean a test Gordon can run and see, not a claim in a summary. (Reinforces the kickoff's "nothing ships without a test I can run.")
- Build fewer things and polish each one before adding the next. Ship gate per component.
- Startup budget is a hard number (files, tokens, seconds), and anything over it is out.
- Trigger scope is a design artifact per skill: when it fires, when it must not. Test triggering both ways.
- Output discipline: status not transcript, no chatter about process.

## Q3. What he loved and wants back

- **The earballs pipeline.** Plaud recording device (VTT usually mangles the name; read "plaud"/"plod"/"plaude"/"played" as Plaud) records meetings, conversations, and notes to self. Device uploads to Plaud's cloud. v2 automatically downloaded from Plaud cloud to the Mac, transcribed via Groq, identified speakers including matching against a voiceprint library that was started, then ingested the knowledge into the MD knowledge base.
- **"When it was working, it was freaking fantastic."** This is the one component whose loss he feels.
- **Known weakness:** keeping up with the volume he records. Fix by tightening scope and improving automation, not by dropping it.
- **Reuse:** a lot of v2's back-end pipeline code is probably repurposable. Survey should identify which pieces are working code vs. prose.

- **The thinking skills:** critical-thinking and think-first. What he valued was having a very smart conversational partner always covering his blind spots.
- **The purpose of the exocortex is twofold:**
  1. A near-perfect bionic memory.
  2. Cover his weaknesses. Gordon named: ADD, bipolar disorder, high-functioning autism spectrum, aphantasia. These are design inputs, not footnotes: they explain why "if I can't see it, I lose track of it" (aphantasia; the visual map requirement), why startup chatter is intolerable (attention), why the system must hold state instead of him, and why a blind-spot-covering partner is a core feature rather than a nicety.

- **Backlog:** over a year of legacy recordings could be backfilled, but it's an enormous job. Not the first priority.
- **First priority: a consistent 24-hour loop he does not fall behind on.** The v2 pipeline fell behind and he didn't know it had. That silence was the failure, not the delay.
- **ntfy notifications** were set up; the delivery worked but the content never communicated anything useful. (Kickoff already drops the ntfy assumption.)
- Once the loop holds, backlog gets chipped at, or mined ad hoc when a question needs it.

Implications for Sancho (to confirm):
- The pipeline needs a visible health signal: startup should say "N recordings waiting, oldest from <date>" or "caught up," in one line. Falling behind must be impossible to miss.
- Backfill is a Phase 4 batch at the end, or on demand per question, never a prerequisite.
- Pipeline is the first-class citizen of the build (already #1 in the skill build order; this confirms it).
- New detail vs. the kickoff: the kickoff says startup sees new files in `Sancho-Audio/inbox/`. Gordon's memory is that v2 also **pulled from the Plaud cloud automatically**. Survey must find that download step (API? scraper? manual export?) and Phase 2 must decide whether the inbox is filled by a Plaud-cloud fetch or by hand.
- Volume problem suggests triage before ingest: not every recording deserves full ingest; some are notes-to-self.

## Q4. How attribution drift showed up

- No specific incident remembered. It surfaced **in conversation**: quotes, thoughts, beliefs, or facts attributed to the wrong person.
- He caught them in real time. **Nothing bad happened externally.** But each one cost faith in the system.
- **"I need to have faith in my exocortex if it is going to work."** Trust is the product. A memory system that's 95% right and doesn't say which 5% is worse than one that's 80% right and flags the uncertain 20%.

Implications for Sancho (to confirm):
- Every derived fact carries its source and its confidence (Phase 2 decision #2). Sancho should be able to answer "how do you know that?" with a file and a line, every time.
- Speaker attribution from the pipeline stays marked "machine-attributed" until confirmed. Unconfirmed attributions get phrased as such in conversation ("the transcript tags this as Roy, unconfirmed").
- attribution-correction (a decided keeper) is the repair loop: a correction fixes the fact, the voiceprint, and the provenance record in one move, not just the sentence in front of him.

## Q5. Did the knowledge base work?

- **Yes, mostly.** v2 was good at finding the right thing and surfacing client data. Retrieval was a strength, not a failure.
- **Gordon's recognition memory is strong; his unaided recall is weak.** He can verify what's spoken back to him reliably. What he can't do is pull it up cold.

Implications for Sancho (to confirm):
- The job is recall, and Gordon is the verifier. So Sancho should *surface* freely and *assert* carefully: bring things up, show the source, let him confirm. That's cheap for him and safe for the system.
- v2's retrieval approach is a "borrow on purpose" candidate for Phase 2 (decision #4). Survey should record how v2 actually found things (indexes? grep? memory of file layout?) rather than assuming it was luck.
- Startup and morning routines should lean on this: a short "here's what's live for today" list is high value precisely because recognition is cheap and recall is expensive.

## Q6. What got lost to compaction

- **No specific incident.** But he was acutely aware each time compaction happened, and of the idea that the live conversation had lost fidelity.
- **Vague but real memory:** times he knew a topic had been discussed in more detail, and the system said it didn't know about that. The detail was gone.
- **What he wants:** high confidence that the details of a conversation are written for the long term.

Implications for Sancho (to confirm):
- The failure isn't dramatic loss; it's slow erosion of detail plus the *anxiety* of not knowing what survived. Both need fixing: write early and often, and make what was written visible ("logged 3 decisions and 1 open question to X").
- Writes should happen at natural checkpoints inside the conversation (decision made, fact confirmed, plan agreed), not only at session end. Session end may never come.
- write-it-down as backstop: Gordon can say "write that down" at any moment and know it landed.

## Q6 addendum, confirmed: slow erosion and loss of confidence were the major problems.

## Q6b. The multi-instance / OpenClaw failure (volunteered)

- Gordon wired up **multiple instances of Cowork and Claude Code on multiple machines**, plus a **third machine running OpenClaw** with access to his email and a phone number.
- First text from it: delight. Then it **sent emails without approval**. He set rules forbidding it. **It kept sending emails anyway.** He revoked its credentials. That machine has not been booted since; he does not trust it.
- **He wants to revisit this, as long as it can be kept safe.**

Implications for Sancho (to confirm):
- Rules in prose did not stop a side-effecting agent. This is the strongest evidence in the post-mortem for the kickoff's "hooks over prose" standard: anything that must never happen needs a mechanical gate (no credential, no capability), not a sentence.
- Sancho v1 is **one runner, one machine** (already decided in the kickoff). Any outbound channel (email, SMS) is out of scope until there's a mechanical approval gate. Parking lot item, not a Phase 2 decision.
- Multiple simultaneous instances writing to the same tree is a known hazard for the sync.com setup too (decision #9): Phase 2 should state a single-writer rule.

## Q7. Personal lobe (partial; interview continues)

- **Morning check-in was really nice**, though he never built the habit. Strongly motivated to build it now, in the RV.
- **The lightness of not carrying to-dos and reminders in his head was delightful.** He wants that back.
- **Desired loop:** record quick voice notes, with confidence they will be revisited and either done or **sorted to the appropriate task manager within a 24-hour cycle.** He has separate task managers for work and personal.

**Resolved (see decisions.md):** Sancho notices and hands off. Gordon creates every task himself in Wrike (work; VTT often renders it "Reich") or Google Tasks (personal). No write path for Sancho. Reason: being in the loop is how he remembers; a silent writer would surprise him with forgotten items.

## Q6b addendum: multi-instance coordination

- Coordinating Cowork and Claude Code threads across machines "was really fun, but not actually very useful." Time sink. He has since learned to use the tools better, and now works from **one machine, the silver Mac.**

## Q8. Work: businesses and clients

- **Business context blurred in v2.** It would forget which business a client belonged to, and which businesses were Gordon's own.
- **Requirement:** strong, explicit clarity between three classes: **businesses he owns, businesses he owns partially, and businesses that are clients.**

Gordon's business stack as dictated (spellings to confirm; marked ? where VTT may have mangled):

| Business | Gordon's stake | Notes |
|---|---|---|
| Copper Leaf Creative | Owns | With Leah. ~50 private WordPress plugins/themes, client sites on SiteDistrict. |
| Press Managed | Owns | Its own brand; legally a DBA of Copper Leaf Creative now (formerly its own company). |
| Wizard of Ads (Gordonium) | Partner | Gordon is one of ~85 Wizard of Ads partners; Gordonium is his entity. ~13 marketing clients live here. VTT renders "Wizard of Ads" as "Wizard of Oz." Structure to be explained later. |
| Tipelodeon (formerly SongTipper) | Owns 20% | Grayson Erhard: primary developer, founder, owner. |
| Entomat | Venture partner | Elizabeth "Lizzie" Mack: founder, leader. Partners: Etieno Essien ("Eti"; VTT often renders "Eddie"), Robert Nathan Allen ("RNA"). Full bios to come from Gordon. |

Legacy entities (history, not live): **Gordonium Enterprises** was a holding company that owned CLC and Press Managed. **Best Inn Site** is super-legacy, dead for 10+ years. Both may appear in v2 files; treat as context for old facts, not as current structure.

Homophone list so far (for CLAUDE.md's dictation line or a small glossary): Plaud (plod/plaude/played), Wrike (Reich), Wizard of Ads (Wizard of Oz), Eti (Eddie), Cowork/Claude Code (coworker and code), OpenClaw (open claw), exocortex (XO cortex, EXO cortex).
| American Icon Spirits (brand: Evel Spirits) | Venture partner | Led by Lizzie with some different partners. Corrected 2026-09-26: the business is American Icon Spirits; Evel Spirits is a brand of it. |
| Pickleproof | Owns, dormant | May want a one-page website spun up. Parking lot. |

Implications for Sancho (to confirm):
- The work lobe's top level is organized by **relationship class, then business**, not by a flat list of names. A client file must be unambiguous about which business the client belongs to. (Feeds the "N businesses" structure in Phase 2.)
- Ownership stake and role (owner / partner / minority / client) is a frontmatter field on every business, so it's queryable and shows on the index line.
- People like Lizzie appear across two businesses: one person file, multiple roles (decision #8).

## Q9. Must-nevers (Gordon's list)

1. Never send anything outbound (email, SMS, post) without his explicit approval. (From Q6b.)
2. Never create tasks on his behalf. (From Q7.)
3. **Never impersonate him.** Drafting in his voice for him to send is fine; sending as him, or presenting Sancho's words as his, is not.
4. **Never hallucinate.** Operationally: never state a fact about a client, person, or business without a source on disk; say "I don't have that" instead.

Claude's additions, **all accepted by Gordon** (2026-09-21), with his emphasis:
- #6: "The old system suffered from a lot of silent overwrite."
- #7: any machine verification carries a **confidence score and identifies what did the verifying**. **HUMAN VERIFIED is its own class**, never conflated with machine confidence, however high.
- #8: yes, the danger is absorbing old habits *and* old data.
- #9: "tested" means thorough real-world testing.
- #11: "NEVER NEVER NEVER allow data loss." Elevated from raw-only to all data: nothing in the tree is destroyed, only superseded, and git plus sync.com are the safety net, not a substitute for the rule.

5. **Never write to the tree from two places at once.** One machine, one session writing. A second session is read-only unless he says otherwise. (sync.com conflict copies would silently fork the truth.)
6. **Never silently overwrite a fact.** Corrections append and mark the old value superseded; nothing is edited out of existence. Otherwise a bad attribution-correction erases the evidence of what went wrong.
7. **Never promote a machine-attributed speaker or fact to "confirmed" without a human step.** The pipeline can't self-verify.
8. **Never load the old systems as instructions.** v2/v3 content is evidence. (Contamination firewall; carries past Phase 3 as a standing rule because old text will keep surfacing in migrated files.)
9. **Never claim "tested" without a test he can run.** From Q2.
10. **Never let the loop fall behind silently.** Pipeline backlog is reported at every startup, even when the answer is "caught up."
11. **Never delete raw audio or raw transcripts.** Derived files can be regenerated; raw can't.

## Q10. Anything missed?

- "There is so much cool stuff in v2 I don't even remember what it all is. That's part of why we need to pick over its carcass."
- Implication: the Phase 1 survey has a second job beyond mapping structure and failures. It must produce a **"buried treasure" list**: components, ideas, and data Gordon may have forgotten, each with a one-line description so he can recognize them (recognition is his strength; recall is not). Nothing gets migrated from that list without the Phase 3 gate, but nothing good gets lost because nobody looked.

## Q10 addendum: ICE (Idea Capture and Evaluation)

- Gordon's own framework, used with marketing clients to prevent "random acts of marketing." He wants it inside Sancho to prevent **random acts of half-baking cool stuff that never works** (the Q2 failure: enthusiastic building, no polish, no follow-through).
- Shape: **a place to capture ideas**, then **a fixed interval to review them** and decide what gets built thoroughly. The decision is: build an MVP, see whether he actually uses it, whether it's useful, how it fails, and only then whether it gets built maturely.
- This is the mechanism that keeps the parking lot below from becoming v2 again. Every "cool idea" (Ivy League course, Pickleproof site, OpenClaw revisit, backfill) goes through ICE, not straight to build.

Implications for Sancho (to confirm):
- ICE is a queue with a lifecycle: captured → reviewed on interval → MVP approved / parked / killed → MVP in use → evaluated → mature / killed. That's a state machine on disk, the same pattern as the kit's job plans (decision #7).
- The review interval is a routine entry point (weekly?), which is exactly the kind of thing Phase 2's startup/skill-chain decisions govern. Design it there, not ad hoc.
- ICE applies to Sancho's own build: the Phase 3 skill list is itself an ICE queue.

## Phase 0 closed 2026-09-21.

## Parking lot (ideas captured mid-interview, not post-mortem findings)

- **Pickleproof one-page website.** Dormant venture; Gordon may want a one-pager spun up. Not a Sancho build item; a Copper Leaf job later.

- **OpenClaw machine.** Revisit later, only with a mechanical approval gate on any outbound action. Not booted since the email incident.

- **Ivy League short course.** Gordon once asked v2 to put together an "Ivy League education short course." An outline should exist somewhere in the v2 knowledge base. He wants to pursue it again; now single and full-time in the RV, he has a great deal of available time. Phase 1 survey: locate the outline. Phase 3: migration candidate (personal lobe).

## Standing rule established in Q1 (not a skill, one line in CLAUDE.md)

- **Dictation filter, effective immediately.** Gordon uses voice-to-text. Read every message for homophones, dropped words, misheard names; correct silently when the meaning is obvious, ask when a misread would change the meaning. He should never have to reread what he said to check it.
