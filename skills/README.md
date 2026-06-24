# Python Agent Skill Pack

Cohesive skill set built around the [AGENTS.md base](../AGENTS.md). AGENTS.md holds the always-loaded constraints; these skills hold the procedures. No skill is referenced from AGENTS.md — the base stays agent-agnostic and degrades gracefully without them.

## The flow

Most work travels one **spine**, idea to shipped code; a few **detours** and **on-ramps** merge onto it. Vocabulary: [../CONTEXT.md](../CONTEXT.md).

**Start here** — match your situation:

- **An idea (new or existing codebase)** → `interview`. The head; always start here.
- **Aging codebase, no specific idea** → `refactor` to surface one, then `interview`.
- **A bug** → `tdd` if you can reproduce it; `debug` if you can't or the cause is unclear.

```
  interview ......... the head: grill the idea (works even before a repo exists)
    |  └─ new repo? → scaffold (bootstrap green, stamp the stack into AGENTS.md), then continue
    |
  FORK — multi-session build?
    ├─ yes → to-prd → to-issues → [clear context, fresh session per issue] → tdd
    └─ no  → tdd  (same window)
                └─ can't reproduce / unclear → debug → repro becomes first tdd test

  on-ramp:  refactor — run anytime; a finding becomes an idea you carry back to interview
  bridge:   handoff  — at any long phase, when context nears the smart-zone, resume in a fresh session
```

1. **`interview`** — grill the idea until the design is sharp; record terms in `CONTEXT.md` and decisions in `docs/adr/` when the project keeps them. The one entry point, new project or old.
2. **`scaffold`** *(detour, new repos only)* — bootstrap a green uv + ruff + ty + pytest + prek project; the stack decisions from the interview get stamped into the new `AGENTS.md`.
3. **Fork — multi-session?**
   - **Yes** → **`to-prd`** (capture the thread as a PRD) → **`to-issues`** (split into independent, agent-ready issues). Then clear context and run each issue in a **fresh session** carrying the PRD + that one issue.
   - **No** → straight to `tdd`, same window.
4. **`tdd`** — build each slice red-green-refactor; minimal per the Laziness ladder.
5. **`debug`** *(detour off `tdd`)* — when a bug won't reproduce or the cause is unclear; the minimized repro becomes the first `tdd` test, back onto the spine.
6. **`refactor`** *(on-ramp / upkeep)* — run anytime to keep the codebase deep and navigable; a finding becomes an idea for `interview`.
7. **`handoff`** *(bridge)* — when a long phase nears the smart-zone, or you need to fork, compact the thread to a file and resume in a fresh session.

## Skills

| Skill | Reach for it when |
|---|---|
| `interview` | Sharpening an idea or plan — the head of every flow |
| `scaffold` | Starting a new Python project — green verify loop from commit zero |
| `to-prd` | Capturing a settled multi-session design as a PRD |
| `to-issues` | Splitting a PRD into independent, agent-ready issues |
| `tdd` | Building a feature or fixing an ordinary bug — red-green-refactor slices |
| `debug` | A hard, intermittent, or unclear-cause bug needs reproduce-first work |
| `refactor` | Improving architecture — find shallow modules and deepen them |
| `handoff` | Crossing context windows — compact a thread so a fresh session resumes it |

`_shared/` holds references used by multiple skills: `LANGUAGE.md` (module / interface / seam / depth), `CONTEXT-FORMAT.md`, `ADR-FORMAT.md`, `PLATFORM.md` (agent-agnostic prose + the `> **Claude Code:**` aside convention). Not skills — no SKILL.md, never trigger.

## Shared principles (enforced across all)

- Trigger → action wording; no "prefer/consider" vibes.
- Questions one at a time, each with a recommended answer.
- Lazy file creation; doc conventions are opt-in per project.
- Laziness ladder (AGENTS.md): reuse → stdlib → native → installed dep → one line → minimal code. Skills defer to it, never restate it.
- Agent-agnostic prose; any Claude-Code specific quarantined in a `> **Claude Code:**` aside (`_shared/PLATFORM.md`). Grep the marker to audit.
- Stack specifics (verify loop, faking rules) defer to AGENTS.md; skills are the long form, not a second source of truth.
- Spikes and throwaway harnesses: `spike_*.py`, `THROWAWAY` header, run and record the verdict, then delete before handoff unless the user asks to keep it.

## Provenance

Derived from [Matt Pocock's skills](https://github.com/mattpocock/skills) — his structure, phase ordering, and sequencing kept; prose rewritten and compressed, examples re-derived, everything re-grounded in this pack's Python stack. His four target failure modes still map: misalignment → `interview`; verbosity → `CONTEXT.md` shared language; buggy code → `tdd` + `debug`; architectural decay → `refactor`. 0.2.0 adds the connective skills (`to-prd`, `to-issues`, `handoff`), the Laziness ladder in the base, and the two-tier agnostic discipline.

## Deploy

```bash
npx skills add DavisMcCracken/pyxis --agent claude-code
```

For local or manual install, copy the contents of this folder into `~/.claude/skills/` — the whole tree; `_shared/` relative links depend on sibling placement.
