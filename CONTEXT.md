# Pyxis Skill Flow

The vocabulary for how Pyxis's skills sequence into one workflow. Pyxis is an
installable Python agent workflow (an `AGENTS.md` rule base plus a matching skill
pack); this glossary names the shape that connects the skills so it is clear what
to run first.

## Language

**Spine**:
The single main path most work travels, idea to shipped code: `interview` → (`scaffold` if new) → fork → `tdd`.
_Avoid_: pipeline, main flow, happy path

**Head**:
The one skill every path starts at — `interview` — whether the project is new or existing.
_Avoid_: entry point, start node

**Detour**:
A skill reached conditionally off the spine that returns to it (`scaffold`, `debug`).
_Avoid_: side-quest, branch

**On-ramp**:
A starting situation that generates work and merges into the head (`refactor` feeding `interview`).
_Avoid_: entry flow

**Fork**:
The one branch point after `interview`: a multi-session build goes through `to-prd` → `to-issues`; a single change goes straight to `tdd`.
_Avoid_: split, gate

**Bridge**:
`handoff` — a conditional cross-session step that compacts a live thread to a markdown file so a fresh session can resume it.
_Avoid_: handover, transfer

**Smart-zone**:
The ~120k-token window within which the model still reasons sharply; nearing it is the trigger to offer a `handoff`.
_Avoid_: context limit, context budget

**Laziness ladder**:
The YAGNI-first decision order (need it at all? → reuse → stdlib → native → installed dep → one line → minimal code) recorded in the `AGENTS.md` base and deferred to by the build skills.
_Avoid_: ponytail rules, simplicity rules

**Two-tier agnosticism**:
The platform discipline — the `AGENTS.md` base is fully agent-agnostic; the skill pack is agnostic prose with any Claude Code specific quarantined in a labeled aside.
_Avoid_: portability, platform support

**Claude Code aside**:
The labeled, ignorable block in a skill where a Claude-Code-specific concretion (the Agent tool, a slash command) is named as an example, never as a requirement.
_Avoid_: Claude note, platform note

**Tracker indirection**:
`docs/agents/issue-tracker.md` — the per-repo config that lets `to-issues` target GitHub or local-markdown without naming either in the skill.
_Avoid_: issue config

## Relationships

- The **Spine** has exactly one **Head** (`interview`) and one **Fork** (after `interview`).
- A **Detour** always returns to the **Spine**; an **On-ramp** always merges into the **Head**.
- The **Bridge** can fire off any long phase when the **Smart-zone** is neared.
- Every build skill defers to the **Laziness ladder**; every skill obeys **Two-tier agnosticism**.

## Example dialogue

> **Dev:** "Is `scaffold` on the spine or a detour?"
> **Maintainer:** "Detour — it fires only when the idea needs a fresh repo, then returns to the fork. The head is always `interview`."

## Flagged ambiguities

- "flow" meant both the whole map and the spine alone — resolved: **Spine** is the main path; "flow" is the whole map (spine + detours + on-ramps).
- "entry point" was ambiguous between **Head** (`interview`, where you start) and **On-ramp** (a situation that generates work) — resolved: **Head** for the start skill, **On-ramp** for the generating situation.
