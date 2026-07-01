---
name: to-prd
description: Turn a settled interview/design thread into a PRD document before the context is cleared. Use when a multi-session build has been grilled and needs capturing as a PRD to split into issues; skip for single-session changes that go straight to tdd.
---

# To PRD

Synthesize the current design thread into a PRD a fresh session can build from. Reach for this only on **multi-session builds** — a one-sitting change skips straight to `tdd`; a PRD for it is ceremony to delete (AGENTS.md Laziness ladder, rung 1).

## Inputs

- The settled `interview` thread — the decisions reached, not the back-and-forth.
- `CONTEXT.md`/`CONTEXT-MAP.md` and `docs/adr/` if the project keeps them. The PRD points at those terms and decisions; it doesn't restate them.

## The PRD

Write one markdown file, lazily, under `docs/` (e.g. `docs/prd-<slug>.md`). Each section earns its place — drop any that would be empty or merely narrate:

- **Why** — the problem and the cost of not doing it. One paragraph.
- **Non-goals** — what this release deliberately excludes, so scope can't creep.
- **Architecture** — the shape of the solution; reference the ADRs and `CONTEXT.md` terms instead of re-deriving them.
- **Deliverables** — one numbered slice per independently-shippable piece, each with scope and acceptance.
- **Done criteria** — the checks that say the whole thing is finished (verify loop green, etc.).
- **Sequencing** — only when deliverables have a real order or dependency.

Decisions and acceptance, not prose.

## Handoffs

- PRD written, build is multi-session → `to-issues` to split it.
- Context nearing the smart-zone before you finish → `handoff`, then resume fresh.
