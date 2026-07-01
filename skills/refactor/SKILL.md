---
name: refactor
description: Find deepening opportunities — turn shallow modules into deep ones. Use when the user wants to improve a codebase's architecture, consolidate tightly-coupled modules, or make code more testable and AI-navigable.
---

# Refactor

Surface architectural friction and propose **deepening opportunities** — refactors that turn shallow modules into deep ones. Goal: testability and AI-navigability.

Vocabulary and principles live in [../_shared/LANGUAGE.md](../_shared/LANGUAGE.md) — **module, interface, implementation, depth, seam, adapter, leverage, locality**; use those terms exactly. Three of its principles carry most of the weight here: the **deletion test**, **the interface is the test surface**, and **one adapter = hypothetical, two = real**.

The project's domain model informs the skill: domain language names the good seams; ADRs record decisions not to re-litigate.

## Process

### 1. Explore

Read `CONTEXT.md` (if present) and ADRs near the target area first. Then walk the codebase read-only and organically, no rigid heuristics — using parallel sub-agents if your harness has them, otherwise reading sequentially.

> **Claude Code:** use the Agent tool with `subagent_type=Explore` for the read-only walk.

Note friction:

- Understanding one concept requires bouncing across many small modules
- **Shallow** modules — interface nearly as complex as the implementation
- Pure functions extracted "for testability" while the real bugs live in how they're called (no **locality**)
- Coupled modules leaking across their seams
- Code that's untested — or untestable through its current interface

Apply the deletion test to every shallow suspect: "deleting concentrates complexity" is the signal you want.

### 2. Present candidates

Numbered list; per candidate:

- **Files** — modules involved
- **Problem** — the friction, concretely
- **Solution** — plain-English change
- **Benefits** — in terms of locality, leverage, and how tests improve

Domain nouns come from `CONTEXT.md`; architecture nouns from LANGUAGE.md. If the glossary says "Order," it's "the Order intake module" — not "FooBarHandler," not "the Order service."

**ADR conflicts:** surface a candidate that contradicts an ADR only when the friction justifies reopening it, marked plainly (_"contradicts ADR-0007 — worth reopening because…"_). Don't enumerate every refactor an ADR forbids.

No interface proposals yet. Ask: "Which of these would you like to explore?"

### 3. Grilling loop

User picks a candidate → switch to the `interview` discipline: one question at a time, recommended answer each, codebase over questions. Walk the design tree — constraints, dependencies, the deepened module's shape, what hides behind the seam, which tests survive.

Side effects land inline as decisions crystallise:

- New module named after a concept missing from `CONTEXT.md` → add the term ([../_shared/CONTEXT-FORMAT.md](../_shared/CONTEXT-FORMAT.md)). Create the file lazily — only if the project keeps domain docs or the user wants to start.
- Fuzzy term sharpened mid-conversation → update `CONTEXT.md` right there.
- Candidate rejected for a load-bearing reason → offer an ADR ("record this so future reviews don't re-suggest it?"). Only when a future explorer would need the reason; skip ephemeral ("not now") and self-evident ones. Gate and format: [../_shared/ADR-FORMAT.md](../_shared/ADR-FORMAT.md).
- Alternative interfaces worth exploring → [INTERFACE-DESIGN.md](INTERFACE-DESIGN.md).

### 4. Implement

Settled design → build with the `tdd` skill; the new interface is the test surface. [DEEPENING.md](DEEPENING.md) maps each dependency category to its testing strategy. Replace, don't layer: delete old unit tests on absorbed shallow modules once interface-level tests cover them. The AGENTS.md Laziness ladder applies to the deepening too — build the smallest seam that holds; "one adapter = hypothetical, two = real" is that ladder's first rung.
