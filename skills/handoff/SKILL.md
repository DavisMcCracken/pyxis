---
name: handoff
description: Compact the live thread into a self-contained markdown file so a fresh session can resume the work. Use when context nears the model's smart-zone mid-phase, when forking off to a separate session, or when the user wants to stop and continue clean later.
---

# Handoff

Write a self-contained handoff file, then continue in a **fresh session** that reads it — the bridge between context windows.

## When it fires

- **Context nears the smart-zone** — the ~120k-token window (on current models) within which reasoning stays sharp — before the current phase finishes. Suggest a handoff rather than pushing on a degraded thread.
- **Forking** — you need a separate session (e.g. to answer a question with throwaway code) but must preserve the current thinking.
- **The user calls it** — they are watching plan usage, or just want to stop. Run it on demand, any time.

Not the between-issues mechanism: independent issues from `to-issues` are already self-contained, so a fresh session carrying the PRD plus one issue is enough — no handoff needed.

## The handoff file

Write one markdown file (e.g. `docs/handoff-<slug>.md`, or a scratch location):

- **Goal** — what we are trying to do, in a sentence or two.
- **Decided** — the settled decisions, so they are not re-litigated.
- **Open** — the live questions, and where each was heading.
- **Files** — what changed or was created, and where (paths, branch).
- **Next** — the single concrete next action for the resuming session.

Self-contained: assume the next session has none of this conversation. State and decisions, never a verbatim transcript.

## After

- File written → open a fresh session and reference it to continue. Letting the current thread auto-summarize in place is a *different* move — handoff forks to a clean session, it does not continue in place.
