---
name: interview
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. If the project keeps domain docs (CONTEXT.md, docs/adr/), challenges the plan against them and updates them inline as decisions crystallise. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

# Interview

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback before continuing.

If a question can be answered by exploring the codebase, explore the codebase instead.

## Docs layer (conditional)

Run the behaviours below only when the project already keeps domain docs (`CONTEXT.md`/`CONTEXT-MAP.md` at root, or `docs/adr/`) or the user asks to record decisions. Otherwise it's a plain interview — never seed doc conventions into a repo that hasn't opted in.

- **Glossary conflicts** — user's term contradicts `CONTEXT.md`? Call it immediately: "Glossary says 'cancellation' means X; you seem to mean Y — which?"
- **Fuzzy terms** — vague or overloaded word? Propose the canonical one: "'account' — Customer or User? They're different things here."
- **Concrete scenarios** — when domain relationships come up, invent edge-case scenarios that force precise boundaries between concepts.
- **Code as witness** — user claims a behaviour? Check whether the code agrees; surface contradictions: "Code cancels whole Orders, but you said partial cancellation exists — which is right?"
- **Inline CONTEXT.md updates** — a term resolves → write it immediately, never batch. Format: [../_shared/CONTEXT-FORMAT.md](../_shared/CONTEXT-FORMAT.md). Domain-expert terms only; no implementation details.
- **ADRs, sparingly** — offer only past the three-part gate (hard to reverse + surprising without context + real trade-off). Gate and format: [../_shared/ADR-FORMAT.md](../_shared/ADR-FORMAT.md).

## Handoffs

- Design settled, ready to build test-first → `tdd`.
- Plan turns out to hinge on an architectural problem → `refactor`.
