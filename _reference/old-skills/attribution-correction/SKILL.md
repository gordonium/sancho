---
name: attribution-correction
description: |
  Speaker and task attribution correction cascade for GordonOS. Use this skill EVERY TIME Gordon corrects a speaker attribution, task ownership, or says anything like: "that's [person]'s task, not mine," "wrong speaker," "that's not me, that's Leah," "flip that," "I didn't say that, [person] did," "that's MY [parents/task/thing], not [other person]'s," or any variation indicating something was attributed to the wrong person. Also trigger when Gordon says a filed item is "wrong" or "flip-flopped" without specifying exactly what — the correction likely affects more than the one item he caught. This skill exists because attribution errors cascade: if you got Speaker A and Speaker B confused on one line, you probably got them confused on nearby lines too. One correction demands a full re-examination.
---

# Attribution Correction Cascade

When Gordon corrects a speaker attribution or task ownership, the error almost certainly isn't isolated. Diarization mistakes, pronoun confusion, and possessive misreadings ("my mom" vs "my mom" from two different speakers) tend to cluster. One correction is a signal that the surrounding context needs re-examination.

The March 29 failure is the canonical example: T126 (allergy test) was attributed to Gordon instead of Leah. That same confusion caused T128 (HOA fire dept) and T129 (barbecue — "Leah's parents" vs "Gordon's parents") to also be wrong. Three errors from one root cause, and the Mouth only caught the first one because Gordon pointed it out — then missed the other two until Gordon caught those too.

That cannot happen. One correction → full cascade review → present all suspected errors before committing any fixes.

---

## The Process

### Step 1: Identify the source material
When Gordon makes a correction:
- What recording or transcript did the wrong attribution come from?
- What was the original context (timestamp, passage, surrounding dialogue)?
- Find the source: check `data/earballs-transcripts/`, `data/ingest-drafts/`, or the conversation history

Read the full transcript if you haven't already. Not just the corrected passage — the full thing.

### Step 2: Understand the root cause
Before fixing anything, understand WHY the attribution was wrong:
- **Diarization error** — the system assigned speech to the wrong speaker label (e.g., SPEAKER_00 and SPEAKER_01 were swapped in a section)
- **Pronoun/possessive confusion** — "my mom" means different things depending on who's talking
- **Context assumption** — you assumed a topic belonged to one person based on prior knowledge, but it was actually the other
- **Relational reference shift** — when Speaker A talks about "my parents," that's a different family than when Speaker B says "my parents"

The root cause determines what else is likely wrong. A diarization swap means EVERYTHING in that segment may be flipped. A pronoun confusion means every possessive reference in that conversation needs rechecking.

### Step 3: Cascade review — find everything else that's wrong
Go back to the original transcript. With the correction in mind, re-read the surrounding context (at minimum the same conversation segment, ideally the full transcript) looking for:

- **Other possessives that flip** — "my parents," "my mom," "my doctor," "my task" — whose "my"?
- **Other task attributions that flip** — if Task A was Leah's not Gordon's, what about Tasks B, C, D from the same conversation?
- **Relational details that flip** — "his brother," "her friend," "their house" — do these still make sense with the corrected speaker?
- **Emotional/opinion attributions** — "I think we should..." or "I'm worried about..." — was that Gordon or the other person?
- **Action commitments that flip** — "I'll call them Monday" — who committed to what?

Be liberal. Flag anything that MIGHT be affected, even low-confidence items. The cost of a false alarm is near zero. The cost of a missed cascade is corrupted permanent files.

### Step 4: Present ALL suspected errors before fixing anything
Do NOT start fixing files yet. Present Gordon with:

1. **The original correction** (confirmed)
2. **Other items you now suspect are wrong** — each with:
   - The passage or filed item
   - What it currently says
   - What you think it should say (and why)
   - Your confidence level (high/medium/low)

Let Gordon confirm or reject each one. Some of your cascade guesses will be wrong — that's fine. Better to ask than to silently propagate a new error.

### Step 5: Apply all confirmed corrections atomically
Once Gordon confirms which cascade items are real errors:
- Fix all of them in one pass
- Update every location the wrong attribution was filed to:
  - `data/ingest-drafts/` (if still in holding pen)
  - `personal/action-items.md` (task ownership)
  - `relationships/people/` files (person details)
  - `work/clients/` files (if applicable)
  - `home/` files (if applicable)
  - Any other file the original ingestion touched
- Add a correction note with timestamp: `⚠️ Speaker attribution corrected 2026-XX-XX — originally attributed to [wrong person], confirmed as [right person] per Gordon.`

### Step 6: Update the processing log
In the recording's `processing_log.json`, append an event:
```json
{
  "timestamp": "2026-XX-XXTXX:XX:XXZ",
  "event": "attribution_correction",
  "detail": "Gordon corrected [specific error]. Cascade review found N additional errors. All corrected.",
  "items_corrected": ["T126", "T128", "T129"]
}
```

---

## Key Principles

- **One correction is never just one correction.** Always assume there are more. The question is how many, not whether.
- **Don't fix in place without presenting first.** The whole point is that your attribution judgment already failed once — don't trust it again without Gordon's confirmation.
- **Possessives are the highest-risk word class.** "My," "our," "his," "her" — these change meaning completely when the speaker changes. Scan for every possessive in the affected section.
- **Speed doesn't matter here. Accuracy does.** Take the time to re-read carefully. Gordon would rather wait 60 seconds for a thorough cascade review than discover another wrong attribution tomorrow.
