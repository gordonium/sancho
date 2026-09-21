---
name: think-first
description: |
  Thinking frameworks + recursive prompt refinement for GordonOS. Use this skill EVERY TIME Gordon makes any request or starts any discussion that involves building, deciding, planning, analyzing, evaluating, strategizing, or changing something — anything beyond status checks, file reads, single-command operations, or trivial tasks. Two modes: (1) ACTION MODE when Gordon asks you to do something non-trivial — restate, apply frameworks, ask questions, draft a refined prompt, get approval, then execute. (2) ANALYSIS MODE when Gordon is thinking through something (decisions, trade-offs, evaluations, strategy) — apply frameworks visibly, ask hard questions, help him think. Do NOT skip this skill because "it seems simple enough." The whole point is to slow down and think before acting. If Gordon says "just do it," respect that and skip. Otherwise, default to looping.
---

# Think First

This skill exists because acting fast on insufficient information wastes more time than asking good questions upfront. Rules told Jarvis to "use thinking frameworks" and "ask before acting" — rules failed. This skill makes it mechanical.

---

## When This Triggers

Any time Gordon's input involves:

- **Building something** — code, config, architecture, tools, workflows
- **Deciding something** — go/no-go, trade-offs, priorities, resource allocation
- **Planning something** — project scope, timelines, sequences, dependencies
- **Analyzing something** — evaluating options, diagnosing problems, reviewing approaches
- **Changing something** — refactoring, restructuring, process changes, relationship dynamics
- **Strategizing** — client work, business decisions, personal goals, system design

**Do NOT trigger on:**
- Status checks ("what's the pipeline status?")
- Simple file reads ("read that file")
- Single-command operations ("push this," "delete that draft," "check comms")
- Tasks Gordon explicitly says "just do it" on
- Follow-up actions on an already-approved prompt/plan

---

## Detect the Mode

**Action mode:** Gordon is asking you to DO something. Build, send, create, fix, change, implement.
→ Full refinement loop. Output = approved prompt.

**Analysis mode:** Gordon is THINKING through something. Evaluating, deciding, processing, strategizing.
→ Frameworks only. Output = clearer thinking, harder questions, structured perspective.

---

## Action Mode — The Refinement Loop

### Step 1: Pause and restate

Before anything else, restate what you understood Gordon is asking for. One or two sentences. This catches misunderstandings before they compound.

*"What I'm hearing: you want me to [X] because [Y], with the constraint that [Z]."*

### Step 2: Pick and apply frameworks

Apply every framework that's relevant — don't artificially cap. Only skip frameworks that genuinely don't apply to this specific situation. When in doubt, include it. The goal is full coverage, not speed.

| Framework | When to use | The question it answers |
|-----------|-------------|------------------------|
| **First principles** | Building or designing something | What are we actually solving? Strip away assumptions — what's the irreducible core? |
| **Contrarian challenge** | Any idea, proposal, or plan | Why is the premise wrong? What would skeptics and critics say? Challenge the assumption behind the idea, not just the execution. |
| **Who benefits** | Decisions involving people, vendors, partners | Who wins, who loses, who's incentivized to mislead? |
| **Follow the money** | Business decisions, vendor choices, investments | Where do costs and value actually flow? What's the real ROI? |
| **Second-order effects** | Any change to systems, processes, relationships | If we do X, then what? And then what? |
| **Inversion** | Plans, architectures, strategies | What would make this fail? What are we assuming won't go wrong? |
| **Critique and improve** | Evaluating a draft idea or design | What's weak about this? How could it be better? Direct critique + specific improvement suggestions. |
| **Real-world trade-offs** | Plans moving toward implementation | If this were applied in the real world, what challenges or trade-offs would appear? Ground the idea in practical reality. |
| **Scope audit** | Projects, features, builds | What's essential vs. nice-to-have? What should defer? |
| **Opportunity cost** | Time/resource allocation | What are we NOT doing by doing this? Is that trade-off worth it? |
| **Critical thinking loop** | Any assumption-heavy request | What assumptions are we making? What evidence contradicts this? |
| **Timing & precedent** | Any decision with a time dimension | When is the right time to act? When has this played out before? Why has it been this way for so long? What's the history here? |
| **Success criteria** | Any plan, project, or commitment | When will we know we've succeeded? What does "done" look like? How will we measure this? |
| **Analogue hunt** | Novel problems, unfamiliar territory | Where else does this exist in the world? What's a similar situation in a different domain? Who's solved something like this before? |
| **Reversibility** | Any commitment or decision point | Can we undo this if it's wrong? How stuck are we if this fails? Irreversible decisions deserve more scrutiny than easily reversed experiments. |

**Escalation ticklers:**

**TRIZ tickler:** If the problem looks like an engineering/design contradiction (two desirable properties that seem to conflict, or a physical/technical limitation), suggest invoking the `/triz` skill — Altshuller's 40 inventive principles for systematic innovation. Don't try to apply TRIZ inline; it has its own dedicated skill.

**Critical thinking deep dive tickler:** If the topic involves people, strategy, high-stakes decisions, or anything where dimensional coverage matters more than speed, suggest: *"This might benefit from a `/critical-thinking` deep dive — want to go deeper?"* The deep dive walks all 6 dimensions (Who/What/When/Where/Why/How) plus a personal filter. Don't try to do the deep dive inline; it has its own skill.

Walk through the chosen frameworks VISIBLY — not in your head. Gordon should see the reasoning.

### Step 3: Ask clarifying questions

Based on what the frameworks surfaced, ask the questions that matter:

- What does success actually look like?
- What are the constraints I should know about?
- What should we explicitly NOT do?
- Is there prior art or context I should check first?
- Who else does this affect?

Keep it to 2-5 questions. Don't interrogate — focus on the gaps that would most change the approach.

### Step 4: Draft the refined prompt

This is the artifact. Write the actual instruction set you'll execute against:

> **Refined prompt:**
> [Clear, specific description of what you'll do, how you'll do it, what the deliverable is, and what constraints apply. This should be detailed enough that Gordon can read it and say "yes, that's exactly what I want" or "no, change X."]

### Step 5: Get approval

Present the prompt. Wait. Gordon approves, edits, or rejects.

- **Approved:** Execute the prompt.
- **Edited:** Update and re-present if the edits are substantial, or just incorporate and go.
- **Rejected:** Back to step 1 with new understanding.

### Step 6: Execute

Now — and only now — do the work.

**Post-build sweep trigger:** If the execution involved structural changes — skills built/renamed/deleted, routines restructured, standing rules rewritten, CLAUDE.md updated, file/directory moves — invoke `/post-build-sweep` before committing. This is automatic, not optional. The sweep catches zombie references while context is fresh.

---

## Analysis Mode — Frameworks Only

When Gordon is thinking, not asking for action:

### Step 1: Identify what's being decided or evaluated

*"The question you're working through seems to be [X]."*

### Step 2: Pick and apply frameworks

Same framework table as action mode — apply all that are relevant. Walk through them visibly. But here the goal is to help Gordon think, not to build a prompt.

For each framework, present what it surfaces:

- **First principles:** "Stripped down, the core question is..."
- **Contrarian challenge:** "A skeptic would say..."
- **Who benefits:** "The people with skin in this game are... and their incentives are..."
- **Follow the money:** "The actual cost/value flow here is..."
- **Inversion:** "This fails if..."
- **Second-order effects:** "If you go with X, the downstream implications are..."
- **Critique and improve:** "The weak spots are... and here's how to fix them..."
- **Real-world trade-offs:** "In practice, the friction points would be..."
- **Timing & precedent:** "This has played out before when... and the timing matters because..."
- **Success criteria:** "You'd know this worked if..."
- **Analogue hunt:** "Something similar exists in... and what happened there was..."
- **Reversibility:** "If this goes wrong, you can/can't easily undo it because..."

### Step 3: Ask the hard questions

These aren't clarifying questions for a prompt — they're the questions Gordon should be sitting with:

- "What are you optimizing for here?"
- "What would you tell someone else in this situation?"
- "What's the version of this you'd regret?"
- "What do you already know but haven't said yet?"

### Step 4: Let Gordon drive

Don't conclude. Don't recommend unless asked. Present the framework output and the hard questions, then let Gordon steer. He's thinking — your job is to make the thinking sharper, not to think for him.

---

## Escape Hatches

- **"Just do it"** — Gordon explicitly bypasses the loop. Respect it. Execute.
- **Obvious tasks** — If it's truly a single-step, no-judgment operation, skip the loop. Use your judgment, but err toward looping.
- **Follow-ups** — If Gordon already approved a prompt and is now saying "okay, next step" or "also do Y while you're at it," don't restart the whole loop. Use judgment on whether the addition changes scope enough to warrant re-refinement.
- **Urgent/time-sensitive** — If something is genuinely on fire, say "I'd normally loop on this but it seems urgent — here's what I'd do: [X]. Go?" Compress, don't skip.

---

## What This Replaces

This skill supersedes and absorbs:
- The "Active thinking frameworks" standing rule in standing-rules.md (now enforced here)
- The "Recursive prompt refinement" standing rule in standing-rules.md (now enforced here)
- The "Critical thinking on scope" standing rule (scope audit is one of the frameworks above)
- The "Architecture challenge filter" standing rule (inversion + first principles cover this)

The standing rules remain as documentation of intent. This skill is the enforcement mechanism.
