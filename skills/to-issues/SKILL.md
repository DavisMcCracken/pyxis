---
name: to-issues
description: Split a PRD into independent, agent-ready issues recorded in the project's configured tracker. Use after to-prd on a multi-session build, when the work must become pieces a fresh session can each pick up alone.
---

# To Issues

Turn a PRD into issues, each independently grabbable — a fresh session opening one needs no other context to start.

## Read the tracker config first

Where issues live is recorded in `docs/agents/issue-tracker.md`. Read it and follow its conventions. Never shell out blindly; the config is the single source of where issues go. Labels come from `docs/agents/triage-labels.md`. See [../_shared/PLATFORM.md](../_shared/PLATFORM.md).

If that config is absent, don't guess — ask the user where issues should live before creating anything.

If the user asks for a dry run, smoke test, or review draft, write issue drafts where they requested instead of publishing to the tracker.

## One issue per independent slice

- Map each PRD deliverable to an issue. Split further only when a deliverable has parts that can ship separately; merge two that can't.
- Each issue is **agent-ready**: enough to start cold — context (link the PRD plus the relevant ADR/`CONTEXT.md` terms), scope, acceptance, and any hard dependency stated explicitly ("depends on #N", not an assumption that numbers are sequential).
- Label them with the tracker string for `ready-for-agent`. These are issues *you* authored from a PRD — already specified, so they skip triage (triage is for incoming reports only).

## Handoffs

- Issues created → start a **fresh session per issue**, passing it the PRD plus that one issue, and run `tdd`. Don't carry this session's context into the build; the issue stands alone.
