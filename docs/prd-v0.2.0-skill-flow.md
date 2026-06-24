# Pyxis 0.2.0 — Skill Flow PRD

Status: draft. Scope: turn the 0.1.0 skill set into one legible, mostly-linear
workflow, add three connective skills, and tighten platform-agnosticism. Design
of record: `CONTEXT.md` (flow glossary), `docs/adr/0001-skill-flow-architecture.md`,
`docs/adr/0002-platform-agnostic-base-discipline.md`.

## Why

0.1.0 shipped five good skills with no documented ordering — `scaffold` and
`interview` both read as "the start," and nothing said what comes next. It also
leaked Claude Code specifics into skill prose, undercutting the "works for any
agent" promise. 0.2.0 makes the path obvious (one spine, marked detours) and the
base honestly agent-agnostic.

## Non-goals

- No new product behavior in the example projects or the `AGENTS.md` Python stack.
- No `prototype` or `triage` skill this release (revisit later; design leaves room).
- No rename of the existing five skills.
- No automated plan-usage trigger for `handoff` (no reliable signal exists).

## Architecture (summary; see ADR-0001)

```
interview (HEAD, always) → [scaffold if new repo] → FORK
  FORK multi-session → to-prd → to-issues → [fresh session/issue] → tdd
  FORK single change  → tdd
  tdd ⇄ debug (can't reproduce)
  refactor = on-ramp → feeds interview
  handoff  = bridge, fires near smart-zone (agent-suggested) or manually
```

## Conventions every new skill must follow (Pyxis idiom)

These are the rules the existing five already obey; the three new skills must match
them rather than be ported verbatim from Matt Pocock's originals.

1. **Trigger → action wording.** No "prefer/consider" vibes; name the trigger, name the action.
2. **One question at a time**, each with a recommended answer (where the skill interviews).
3. **Lazy file creation.** Create docs/artifacts only when a real decision or output demands them.
4. **Two-tier agnosticism (ADR-0002).** Agnostic prose by default; any Claude Code concretion goes in a labeled `> **Claude Code:**` aside that a non-Claude reader can skip. No hard dependency on the Agent tool, slash-command names, or `gh`.
5. **Defer stack specifics to `AGENTS.md`.** Skills are the long form, not a second source of truth for the verify loop, faking rules, or the laziness ladder.
6. **Issue tracker via indirection.** Read `docs/agents/issue-tracker.md`; never hardcode GitHub or local-markdown.

## Deliverables

### D1 — `AGENTS.md`: laziness ladder section

Add one short, always-loaded section encoding the YAGNI-first decision order:
need it at all? → reuse what's here → stdlib → native platform feature → an
already-installed dep → one line → minimal code that works. Frame as a reflex that
runs *after* understanding the problem. Build skills (`scaffold`, `tdd`,
`refactor`) reference it instead of restating it. Keep it agent-agnostic. Mirror
the change into `skills/scaffold/templates/AGENTS.md` (the canonical stamp).

### D2 — new skill `to-prd`

Turn an `interview` thread into a PRD document. Pyxis idiom, not a verbatim port.
- **Trigger:** user has finished grilling a multi-session build and wants it captured before context is cleared.
- **Action:** synthesize the thread (and any `CONTEXT.md`/ADRs) into a PRD with Why, Non-goals, Architecture, Deliverables, Done criteria. Write it lazily under `docs/` (e.g. `docs/prd-<slug>.md`).
- **Agnostic:** no platform features needed; pure document synthesis.
- **Hands off to:** `to-issues`.

### D3 — new skill `to-issues`

Split a PRD into independently-grabbable issues.
- **Trigger:** a PRD exists and the build is multi-session.
- **Action:** read the PRD, derive one issue per independent slice, each agent-ready (context, acceptance, deps noted). Create them through the configured tracker (`docs/agents/issue-tracker.md`) — GitHub via `gh` OR local-markdown OR recorded prose. Never assume GitHub.
- **Agnostic:** tracker indirection is the whole point; the `gh` calls live behind the config doc, with a `> **Claude Code:**`-style aside only where a concrete command helps.
- **Hands off to:** a fresh session per issue running `tdd`.

### D4 — new skill `handoff`

Compact a live thread to a markdown file so a fresh session resumes it.
- **Trigger:** context nears the smart-zone (~120k tokens) mid-phase, or the user wants to fork/branch the session, or plan usage is getting tight (user-initiated).
- **Action:** write a self-contained handoff markdown (what's decided, what's open, where the files are, what to do next); instruct opening a fresh session that references it. Not the between-issues mechanism — that's a fresh session carrying PRD + one issue.
- **Agnostic:** "fresh session" stated generically; smart-zone math explained, not assumed.

### D5 — agnostic audit + Claude-aside convention across the existing five

Define the `> **Claude Code:**` aside convention once (in `skills/README.md` or
`_shared/`), then sweep `scaffold`, `tdd`, `debug`, `interview`, `refactor`:
move every Claude-specific concretion (Agent tool, slash commands, session
mechanics) into a labeled aside or neutralize the wording. Acceptance: a grep for
the aside marker enumerates every remaining platform-ism, and the base + prose
read correctly for a non-Claude agent.

### D6 — rewrite `skills/README.md` as the flow map

One canonical map: a "start here" decision (new project / existing idea / aging
codebase), the linear spine as a numbered list, detours/on-ramps called out
inline, and the eight-skill table updated. Small ASCII spine sketch if it stays
one screen. Retire the old Birth/Design/Build/Broken/Aging table (superseded).

### D7 — docs sync

Update root `README.md` (skill count 5→8, the new flow sentence), `PROJECT-STATUS.md`,
and any deploy/provenance notes. Bump version to 0.2.0 where versioned.

## Done criteria

- All three new skills exist, follow the six conventions, and are exercised once end-to-end (interview → to-prd → to-issues → tdd on a toy change).
- `AGENTS.md` carries the laziness ladder; build skills defer to it; template mirror updated.
- Grepping the Claude-aside marker lists every platform-ism and nothing leaks outside an aside.
- `skills/README.md` is the single flow map; old lifecycle table gone; no second map.
- Verify loop green; root README and status reflect 0.2.0.

## Sequencing note

D1 and D5's aside-convention should land first (they set rules the new skills
obey). D2→D3→D4 next. D6 after the skills exist (it maps them). D7 last.
