# Python Agent Skill Pack

Cohesive skill set built around the [AGENTS.md base](../AGENTS.md). AGENTS.md holds the always-loaded constraints; these skills hold the procedures. No skill is referenced from AGENTS.md — the base stays harness-agnostic and degrades gracefully without them.

Derived from [Matt Pocock's skills](https://github.com/mattpocock/skills) — his structure, phase ordering, and battle-tested sequencing are kept (that's the intent worth preserving); all prose is rewritten and compressed, examples re-derived, and everything re-grounded in this pack's Python stack. His four target failure modes still map: misalignment → `grill-me`; verbosity → `CONTEXT.md` shared language; buggy code → `tdd` + `diagnose` feedback loops; architectural decay → `improve-codebase-architecture`.

## Lifecycle map

| Stage | Skill | Role |
|---|---|---|
| Birth | `py-new` | Scaffold uv + ruff + ty + pytest + prek project, then finish requested product behavior test-first |
| Design | `grill-me` | One-question-at-a-time interview; updates CONTEXT.md/ADRs inline when the project keeps them |
| Build | `tdd` | Red-green-refactor, vertical slices; Python testing + faking rules for features and ordinary reproducible bugs |
| Broken | `diagnose` | Feedback-loop-first discipline for hard or uncertain bugs; hands repro to `tdd`-style regression test |
| Aging | `improve-codebase-architecture` | Find shallow modules, deepen them; implements via `tdd` |

Cross-references: `grill-me` -> `tdd` / `improve-codebase-architecture`; `tdd` -> `diagnose` (can't reproduce) and back (minimised repro becomes first test); `diagnose` -> `improve-codebase-architecture` (no correct seam = architecture finding); `improve-codebase-architecture` -> `tdd` (implement the deepened design).

`_shared/` holds vocabulary and formats used by multiple skills: `LANGUAGE.md` (module/interface/seam/depth), `CONTEXT-FORMAT.md`, `ADR-FORMAT.md`. Not a skill — no SKILL.md, never triggers.

## Changes vs the originals

- **`grill-me` absorbs `grill-with-docs`.** Identical core text existed in both. The docs layer is now conditional: it activates only when the project already has `CONTEXT.md`/`docs/adr/` or the user asks to record decisions. Plain grilling no longer seeds doc conventions into repos that didn't opt in. **Retire the old `grill-with-docs` folder on deploy.**
- **`tdd` went 6 files -> 2** (`SKILL.md`, `tests.md`). TypeScript/jest examples rewritten in Python (pytest, monkeypatch, hand-written fakes, `Protocol`). `deep-modules.md` + `interface-design.md` folded into `_shared/LANGUAGE.md` references; `refactoring.md` folded into the Refactor step. Faking preference order added: real thing -> hand-written fake -> monkeypatch -> MagicMock. New: valid RED means the intended test collects, executes, and fails for the target behavior; ordinary bug-fix entry point; verify-loop and coverage-closure exit.
- **`diagnose`** kept whole — strongest original. Added: scope note (ordinary bugs don't need it), narrowed trigger for uncertain/intermittent/cross-system/performance failures, `hypothesis` for fuzz loops, `tmp_path`/injected-clock determinism examples, throwaway harnesses follow the `spike_*.py` convention, full verify loop in Phase 6 checklist.
- **`improve-codebase-architecture`** kept whole. Refs repointed from `../grill-with-docs/` to `../_shared/`; grilling loop now names `grill-me` discipline; new step 4 (implement via `tdd`, replace-don't-layer); DEEPENING examples Pythonised (SQLite `:memory:`, `tmp_path`, `Protocol` ports); "mock adapter" -> "hand-written fake adapter".
- **`py-new`** now runs past a green scaffold when the request names product behavior: real behavior test, valid RED, minimal implementation, verify loop again. The canonical AGENTS.md template lives in its `templates/`.

## Shared principles (enforced across all)

- Trigger -> action wording; no "prefer/consider" vibes.
- Questions one at a time, each with a recommended answer.
- Lazy file creation; doc conventions are opt-in per project.
- Stack specifics (verify loop, faking rules) defer to AGENTS.md; skills are the long form, not a second source of truth.
- Spikes and throwaway harnesses: `spike_*.py`, `THROWAWAY` header, run and record the verdict, then delete before handoff unless the user asks to keep it.

## Deploy

Copy the contents of this folder into `~/.claude/skills/` — whole tree, `_shared/` relative links depend on sibling placement.

Migrating from Matt Pocock's originals? Remove the superseded pieces first: `grill-with-docs/` (merged into `grill-me`) and the old `tdd` support files (`deep-modules.md`, `interface-design.md`, `mocking.md`, `refactoring.md`). His other skills coexist fine.
