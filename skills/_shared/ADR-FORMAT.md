# ADR Format

ADRs live in `docs/adr/`, numbered sequentially: `0001-slug.md`, `0002-slug.md`. Create the directory lazily, on the first ADR. Number = highest existing + 1.

## Template

```md
# {Short title of the decision}

{1–3 sentences: context, decision, why.}
```

A single paragraph is a complete ADR. The value is recording *that* a decision happened and *why* — not filling out sections.

Optional, only when they earn their lines: `status` frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`), **Considered Options** (rejected alternatives worth remembering), **Consequences** (non-obvious downstream effects).

## The three-part gate

Offer an ADR only when ALL three hold:

1. **Hard to reverse** — changing your mind later costs real effort
2. **Surprising without context** — a future reader would ask "why on earth?"
3. **Real trade-off** — genuine alternatives existed and one was chosen for reasons

Easy to reverse → you'll just reverse it. Not surprising → nobody will wonder. No alternative → nothing to record beyond "did the obvious thing."

## What qualifies

- **Architectural shape** — "write model is event-sourced; read model projects into Postgres"
- **Integration patterns between contexts** — "Ordering and Billing communicate via events, not synchronous HTTP"
- **Lock-in technology choices** — database, message bus, auth provider. Not every library; only the quarter-to-swap-out ones
- **Boundary and ownership decisions** — "Customer data owned by the Customer context; others reference by ID." Explicit no-s count as much as yes-s
- **Deliberate deviations from the obvious path** — "manual SQL, no ORM, because X." Stops the next engineer from "fixing" the deliberate thing
- **Constraints invisible in code** — compliance bans, partner-contract latency budgets
- **Non-obvious rejections** — picked REST over GraphQL for subtle reasons? Record it, or the suggestion returns in six months
