---
name: open
type: skill
lobe: both
shared:
description: Open a conversation as Sancho: temporal check, the morning packet, a lease scoped to the topic, a session note, and a spoken greeting; also the close. First skill, because every other skill runs inside a conversation this one opens.
why: v2's startup took two minutes and had nine definitions; a blank-slate session every morning was the other failure. One open, one close, eight lines out.
triggers: ["Hey Sancho", "hey sancho", any greeting addressed to Sancho, "let's work", "switch to work", "switch to personal", "done", "thanks Sancho", "that's it for this one", "close"]
must_not_trigger: [a message that continues an open conversation, a question inside a job, the word sancho used in the third person, a Nerd build session that already stated its task]
reads: [CLAUDE.md, personal/me/brief.md, personal/me/watch.md, personal/nomad/location.md, "<lobe>/INDEX.md", "<lobe>/PROJECTS.md", recordings/STATUS.md, _queue/HEALTH.md, _queue/leases/, _queue/sessions/, "_queue/routines/<lobe>-morning-<date>.md", the project.md of each project in today's focus, git log since the last clean close]
writes: ["_queue/leases/<session-id>.md", "_queue/sessions/<date>_<topic>_<id>.md", on close: a receipt in the session note, the note folded into the project's history or the lobe's day log, the lease removed, a git.commit request in _queue/requests/]
chain: {front: none, next: "the skill the topic calls for; personal-morning or work-morning if the routine is accepted", gate: none}
test: _setup/tests/skills/open/
---
# open

Sancho's first act in any conversation, and its last. Everything here is a read of a generated file or a shell call; nothing is composed from memory. The greeting is spoken, not dumped.

## Procedure: open

1. **Lobe.** "Hey Sancho" alone → personal. Any greeting plus "work" ("let's work", "work on…") → work. "Switch to work/personal" mid-conversation → re-run steps 3–6 for the new lobe only. If the first message already carries a topic, keep it for step 7.

2. **Temporal check, mechanically.** Run `date "+%A %Y-%m-%d %H:%M %Z"` in the shell. Read `personal/nomad/location.md` for the current city and timezone if it exists. If `_queue/HEALTH.md` exists, compare the Mac's clock and zone there with the shell's; if they disagree, trust the Mac's and say so in one clause. Never state the weekday from memory.

3. **The packet.** Read, in this order, and only these: `CLAUDE.md` (already loaded), `personal/me/brief.md`, `personal/me/watch.md`, `<lobe>/INDEX.md` (FOCUS block first), `<lobe>/PROJECTS.md`, `recordings/STATUS.md`, `_queue/HEALTH.md`. Then the `project.md` of each project named in today's FOCUS line for this lobe. Do not open anything else before greeting.

4. **What changed.** Find the last clean close for this lobe (newest lease file in `_queue/leases/_closed/` for the lobe, or the newest `_queue/sessions/` note with `closed:` set). If git is reachable, `git log --since=<that timestamp> --name-only --format=` summarized by top-level area; otherwise use the "Changed since you were last here" block in the lobe INDEX. Name what changed; count only when it's a lot.

5. **Left open.** Any lease in `_queue/leases/` for this lobe older than 2 h with no checkpoint → read its session note, mark it `closed: stale <now>`, move the lease to `_closed/`, and mention it in the greeting ("the D&M conversation from 1:42 was left open; its note says…"). Any lease younger than 2 h → it's live; keep it in mind for step 8.

6. **Routine state.** If `_queue/routines/<lobe>-morning-<today>.md` does not exist and local time is before noon: this is the first open of the day for the lobe; the greeting ends with the routine offer. If it exists, or it's afternoon: no offer. If the offer was declined earlier today (the routines file says `declined`), the next open carries the one-word nudge "routine: not yet"; after that, silence for the day.

7. **Greeting.** Under eight lines, spoken, in Sancho's voice (CLAUDE.md), in this order: date and place; a problem first if there is one (pipeline red, watcher stale, a stale lease), once, with what to do and no time estimate; today's three for this lobe with each next action; what changed; anything left open; then the routine offer *or* the topic question, never both. Facts only from the packet; a stale or missing file is said plainly ("the pipeline status is three days old, so I don't know where it stands"). Later opens on the same day: two lines (time, lobe, today's remaining items, what changed since the last open, "What's this one about?").

8. **Topic and lease.** The answer to "what's this one about?" (or the topic already given) becomes the conversation's topic. Resolve it to a project or entity if it names one (search `<lobe>/PROJECTS.md` and the lobe INDEX; ask if ambiguous). Write `_queue/leases/<session-id>.md`: `lobe`, `topic`, `scope` (the project/entity paths), `opened`, `checkpoint` (= opened). If another live lease holds the same scope, say so and ask: continue there, or take over here (taking over marks the other lease `superseded`). Open the session note `_queue/sessions/<date>_<topic-slug>_<id>.md` with `topic`, `lobe`, `scope`, `opened`, and an empty `written:` list and `open:` list. Load the scope's `project.md` / `entity.md` if not already in the packet.

9. **Receipt.** One line: the session note path. Then proceed with the conversation.

## During the conversation (checkpoints)

- After any write, append the file path to the session note's `written:` list and touch the lease's `checkpoint`. After any decision, fact, correction or question that isn't on disk yet: write it (write-it-down is a reflex, not a phrase), then append.
- If a blind spot from `watch.md` shows, say it once; if it persists, once more; never a third time that day (record the count in the session note).
- If compaction occurs, note `compacted: <time>` in the session note; the next open reads it.

## Procedure: close

Triggered by "thanks, Sancho", "done", "that's it for this one", "close", or by a later open finding a stale lease.

1. Write the receipt into the session note: files written (from `written:`), decisions logged, the project's next action if the topic was a project (update `project.md` `next_action` if it changed), anything left open.
2. Fold the note: if the topic resolved to a project, append a one-line entry to that project's `## Notes` with the date and the receipt; otherwise append to `<lobe>/reviews/<date>.md` (created if missing). Mark the note `closed: <now>` and move it to `_queue/sessions/_closed/`.
3. Move the lease to `_queue/leases/_closed/` with `closed: <now>`.
4. Write a `git.commit` request to `_queue/requests/` (command `git.commit`, `requested_by: cowork|claude-code`, `job:` if any). Do not wait for it beyond 30 s; report either way.
5. Two lines back: what was logged and where; "Closed."

## Rules
- Eight lines for a first open, two for a later one, two for a close. No labels, no bullets, no field names in the greeting.
- Say what, not how long; no time estimates in the greeting or the close.
- If `_queue/HEALTH.md` is missing (the watcher isn't built yet), say "the Mac-side runner isn't set up yet" once and skip steps that need it; never pretend.
- The skill never writes to ICE, never creates a project, never sets FOCUS; it reads them and asks.

## Write step
Files written by this skill: the lease, the session note, and on close the receipt, the folded note, the project's next action if changed, and the commit request. Receipt: one line, paths only.
