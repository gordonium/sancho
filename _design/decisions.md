# Sancho decisions log

One line per decision, newest at the bottom. Date, decision, reason. Decisions pre-made in the kickoff prompt (two lobes, git in `~/.sancho.git`, no handoff, audio in `Sancho-Audio/`, name Sancho, eight keeper skills) are recorded there and not repeated here.

| Date | Decision | Reason |
|---|---|---|
| 2026-09-21 | Dictation filter is a standing stance, one line in CLAUDE.md, active from Phase 0 onward. | Gordon dictates; rereading to check wastes the time dictation saves. |
| 2026-09-21 | Tasks: option A, "notice and hand off." Sancho extracts commitments and to-dos from voice notes and transcripts into a list for Gordon; Gordon creates every task himself in Wrike (work) or Google Tasks (personal). Sancho gets no write path into either. | Gordon is the human in the loop on purpose: creating the task by hand helps him remember it. Option B (Sancho writes tasks directly) rejected as too silent, and he'd be surprised by things he forgot. |
| 2026-09-21 | One machine: the silver Mac is the only runner. No multi-instance coordination. | Multi-instance experiments were fun but wasted time coordinating threads; one machine keeps it clean. |
| 2026-09-21 | ICE (Idea Capture and Evaluation) is a Sancho component: capture queue, interval review, MVP-then-evaluate gate before anything is built maturely. Phase 2 designs it as a state machine on disk. | Gordon's own client framework; prevents random acts of half-baked building, the Q2 failure. |
| 2026-09-21 | v2 folder is NOT mounted this session, at Gordon's call. | Contamination risk to this conversation. Phase 1 proceeds on what is mounted; v2 gets its own dedicated survey session. |
| 2026-09-21 | WIP limit: at most three things in development at any time. Each feature is built to maturity and habit before the next one starts. | "If you're focused on more than three things you're not focused on anything." Guards the Q2 failure directly. |
| 2026-09-21 | Phase 1 paused (v3 copy in progress, v2 unmounted). Session pivots to capturing Gordon's foundational-routine ideas that don't depend on the old versions, into `_design/`. Still read-only; no building. | Gordon's call; get the ideas out of his head while they're fresh. |
| 2026-09-21 | Must-never list adopted (11 items, postmortem.md Q9). Standouts: no data loss ever, no silent overwrites, HUMAN VERIFIED is a distinct class from any machine confidence score, old-system text is never instructions. | Each maps to a v2 trust failure. These become CLAUDE.md invariants and, where possible, hooks. |
