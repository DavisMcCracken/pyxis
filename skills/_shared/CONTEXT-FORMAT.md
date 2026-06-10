# CONTEXT.md Format

A project glossary the agent and team share. Payoff: "a problem in the materialization cascade" replaces a paragraph of re-explanation — fewer tokens, consistent naming in code.

## Structure

```md
# {Context Name}

{1–2 sentences: what this context is, why it exists.}

## Language

**Loan**:
A copy of a title checked out to a member, with a due date.
_Avoid_: rental, checkout, borrow record

**Hold**:
A member's claim on the next available copy of a title.
_Avoid_: reservation, queue entry

## Relationships

- A **Loan** is held by exactly one **Member**
- A **Hold** converts to a **Loan** when a copy returns

## Example dialogue

> **Dev:** "When a **Hold** converts, does the **Member** get the full loan period?"
> **Domain expert:** "No — conversion uses the reduced pickup window first."

## Flagged ambiguities

- "checkout" meant both **Loan** creation and the payment flow — resolved: payment flow is **Purchase**.
```

## Rules

- **Be opinionated.** One canonical word per concept; list the others under _Avoid_.
- **Definitions: one sentence, what it IS** — not what it does.
- **Flag ambiguities explicitly**, with the resolution.
- **Show relationships** with bold term names and cardinality where obvious.
- **Project-specific terms only.** General programming concepts (timeouts, retries, error types) never belong, however often the project uses them.
- **Group under subheadings** only when natural clusters emerge; otherwise flat list.
- **Include an example dialogue** — it demonstrates boundaries between related terms faster than prose.

## Single vs multi-context repos

- One `CONTEXT.md` at the repo root — the default, most repos.
- Multiple contexts: `CONTEXT-MAP.md` at the root lists each context, where its `CONTEXT.md` lives, and how contexts relate (events consumed, shared types).

Inference order: `CONTEXT-MAP.md` exists → multi-context, read it. Root `CONTEXT.md` only → single. Neither → create a root `CONTEXT.md` lazily when the first term is resolved. In multi-context repos, infer which context the topic belongs to; ask if unclear.
