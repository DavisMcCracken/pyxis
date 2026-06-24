# Interface Design

Explore 3+ radically different interfaces for a chosen deepening candidate, in parallel where the harness allows. Rationale: "Design It Twice" (Ousterhout) — the first idea is rarely the best. Vocabulary: [../_shared/LANGUAGE.md](../_shared/LANGUAGE.md); platform asides: [../_shared/PLATFORM.md](../_shared/PLATFORM.md).

## Process

### 1. Frame the problem space

Write a user-facing brief for the candidate before exploring anything:

- Constraints any interface must satisfy
- Dependencies and their categories ([DEEPENING.md](DEEPENING.md))
- A rough illustrative sketch — grounds the constraints, not a proposal

Show it, then move straight to step 2; the user reads while exploration runs.

### 2. Explore divergent designs

Explore 3+ designs, each forced toward a **radically different** interface by its own design constraint. Run them as parallel sub-agents if your harness supports them, otherwise work through them sequentially:

- Design 1 — minimize: 1–3 entry points, maximum leverage per entry point
- Design 2 — maximize flexibility: many use cases, extension room
- Design 3 — optimize the common caller: default case trivial
- Design 4 (when cross-seam deps exist) — ports & adapters throughout

> **Claude Code:** spawn one Agent-tool sub-agent per design constraint so they run in parallel.

Each exploration gets a self-contained technical brief — file paths, coupling details, dependency categories, what hides behind the seam — written in LANGUAGE.md + `CONTEXT.md` vocabulary so naming stays consistent. The brief is separate from the step 1 user-facing framing.

Required output per design:

1. Interface — types, methods, params, plus invariants, ordering, error modes
2. Caller usage example
3. What the implementation hides behind the seam
4. Dependency strategy and adapters
5. Trade-offs — where leverage is high, where thin

### 3. Present and compare

Designs sequentially, then a prose comparison across **depth**, **locality**, and **seam placement**. End with your own recommendation — strongest design and why, or a hybrid if pieces combine well. Be opinionated; the user wants a strong read, not a menu.
