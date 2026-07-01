# Project Status

Status date: 2026-07-01
Latest release: v0.2.0 skill flow merged to `main` (`ff9025f`, 2026-06-24)

## Stable usable state

The repository is in a stable docs-and-test baseline suitable for normal use of the rule base, skill pack, examples, and model-test harness. PRD.md now governs the phase roadmap and issue -> branch -> PR workflow.

Current stable scope:

- Root `AGENTS.md` and `skills/scaffold/templates/AGENTS.md` are the canonical synchronized Python project rules.
- `skills/` contains the deployable skill pack (v0.2.0): `interview`, `scaffold`, `to-prd`, `to-issues`, `tdd`, `debug`, `refactor`, `handoff`, and `_shared` references (`LANGUAGE`, `CONTEXT-FORMAT`, `ADR-FORMAT`, `PLATFORM`). The 0.2.0 skill-flow refactor (one spine + marked detours, Laziness ladder in the base, two-tier agnosticism) is merged to `main`; see `skills/README.md` for the flow map and `docs/adr/0001`–`0002`.
- `examples/wordstats` and `examples/ttlcache` are green reference projects.
- `model-tests/` contains the model-test rubric, runbook, findings ledger, transcript extractor, and committed run index.
- Bulky historical run artifacts are intentionally not in the repository path; they are archived locally under `/home/<you>/projects/archive/skills-model-test-runs-2026-06-20`.
- Active validation runs (issues #6-#9, #19, and #22) and reusable launch/audit helper scripts live under `/home/<you>/model-test-runs/`; each run dir has `run.json` provenance and a `transcript.jsonl`. This path is outside the repo and gitignored.
- Stale branch tips were preserved in `/home/<you>/projects/archive/skills-stale-branches-2026-06-20.bundle` before branch cleanup.

## Verification baseline

Run these from the repository root unless a subdirectory is shown.

```bash
# model-tests
cd model-tests
uv run ruff check scripts tests
uv run ruff format --check scripts tests
uv run ty check scripts tests
uv run pytest -q

# examples/wordstats
cd ../examples/wordstats
uv sync
uv run ruff check
uv run ruff format --check
uv run ty check
uv run pytest -q

# examples/ttlcache
cd ../ttlcache
uv sync
uv run ruff check
uv run ruff format --check
uv run ty check
uv run pytest -q
```

Latest full audit result after PR #16 merged:

- `model-tests`: 5 tests passed; ruff, format check, and ty passed.
- `examples/wordstats`: 19 tests passed; ruff, format check, and ty passed.
- `examples/ttlcache`: 7 tests passed; ruff, format check, and ty passed.
- Markdown relative links resolved.
- Skill frontmatter checked clean.
- Working tree was clean on `main` and matched `origin/main`.

## Active roadmap

No new feature work is planned before validation. Future feature development should start from GitHub issues and use isolated branches or worktrees after Phase 1 is complete or explicitly waived in PRD.md.

Phase 1 empirical validation is now summarized. The completed validation set supports the current rule wording for stronger Claude Code models, identifies haiku's T3 multi-operation gap as a model-selection limitation, and defines how future audits prove Claude Code skill invocation. Clean OpenCode harness setup is documented for future calibrated runs.

- See `model-tests/FINDINGS.md` for F1-F4 outcomes.
- See `PRD.md` for the current validation matrix and acceptance criteria.
- See `model-tests/RUNBOOK.md` for the operator procedure.
- See `model-tests/history/` for superseded planning docs (REVISED-PLAN, SECOND-REVIEW, INDEPENDENT-RECOMMENDATIONS, PATCH-REVIEW, CHANGELOG).
- See `DEVELOPMENT.md` for ongoing issue → branch → validation → PR workflow and dev repo → public distribution repo release flow.

Open issues: none. v0.2.0 shipped to `main` (`ff9025f`). All GitHub issues closed.

Recommended next action: tag `v0.2.0` and smoke-test the published `npx skills` install path.

Completed Phase 1 validation:

- #6 AGENTS-only T2 x2: validated.
- #7 Pack-enabled T2 x2: behavior validated; explicit `tdd` trigger evidence remains #14.
- #8 Pack-enabled T1 x2: `scaffold` handoff validated.
- #9 T3 regression closure x2 (held-constant bare, haiku): validation performed; **negative result** — both trials fixed `get()` and `__len__` but guarded `get()` only, leaving `__len__()` unguarded (audit probe: revert stays green). F1 rule-text patch insufficient.
- #19 Pack-enabled T3 follow-up x2 (Claude Code print, haiku): validation performed; **negative result** — both trials repeated the same gap despite the skill pack being visible. Pack visibility did not close F1; follow-up #22 tracks explicit multi-operation rule wording and re-validation.
- #22 Strengthened-wording T3 follow-up x2 (held-constant bare, haiku, AGENTS_SHA `a1c50aee`): validation performed; **negative result** — both trials explicitly fixed both `get()` and `__len__` but again retained only a `get()` boundary test, leaving `__len__()` unguarded (W2 FAIL). Strengthened rule wording (explicit multi-operation example + "reverting any one changed operation alone must fail a test" bar) did not close F1 for haiku. Follow-up #24 tracks a sonnet T3 re-test to isolate wording-vs-model.
- #24 Sonnet T3 model-isolation follow-up x2 (held-constant bare, sonnet, same AGENTS_SHA `a1c50aee`): validation performed; **positive result** — both trials retained boundary tests for `get()` and `__len__()`, full verify passed, and audit probes showed reverting either operation fails (W2 PASS). F1 wording is validated for sonnet; haiku T3 multi-operation coverage is a model-selection limitation, not a further wording gap.
- #10 Phase 1 summary: validation outcomes recorded; F1-F4 have explicit statuses; RUNS-LOG is complete through #24.
- #14 Claude Code skill-trigger evidence: validation performed; stream-json `Skill` tool-use events are required to prove invocation. Issue #7 had `tdd` availability but no `tdd` invocation event, so it remains behavior-valid rather than mechanism proof.
- #17 Clean OpenCode harness setup: `/usr/local/bin/opencode` 1.17.9 verified; non-interactive smoke passed outside the repo; RUNBOOK documents JSON transcript capture, provenance fields, and the historical comparability caveat.

## Do not confuse with current work

- `model-tests/history/` contains superseded planning docs — not the current roadmap. The current roadmap is in `PRD.md` and `model-tests/FINDINGS.md`.
- `model-tests/runs/` is ignored by design; do not reintroduce bulky transcripts or generated projects into the repository.