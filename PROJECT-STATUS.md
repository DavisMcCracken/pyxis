# Project Status

Status date: 2026-06-20
Baseline commit before this note: `ad7cf05`

## Stable usable state

The repository is in a stable docs-and-test baseline suitable for normal use of the rule base, skill pack, examples, and model-test harness.

Current stable scope:

- Root `AGENTS.md` and `skills/py-new/templates/AGENTS.md` are the canonical synchronized Python project rules.
- `skills/` contains the deployable skill pack: `py-new`, `grill-me`, `tdd`, `diagnose`, `improve-codebase-architecture`, and `_shared` references.
- `examples/wordstats` and `examples/ttlcache` are green reference projects.
- `model-tests/` contains the model-test rubric, runbook, findings ledger, transcript extractor, and committed run index.
- Bulky historical run artifacts are intentionally not in the repository path; they are archived locally under `/home/hermes/projects/archive/skills-model-test-runs-2026-06-20`.
- Stale branch tips were preserved in `/home/hermes/projects/archive/skills-stale-branches-2026-06-20.bundle` before branch cleanup.

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

Latest full audit result before this file was added:

- `model-tests`: 5 tests passed; ruff, format check, and ty passed.
- `examples/wordstats`: 19 tests passed; ruff, format check, and ty passed.
- `examples/ttlcache`: 7 tests passed; ruff, format check, and ty passed.
- Markdown relative links resolved.
- Skill frontmatter checked clean.
- Working tree was clean on `main` and matched `origin/main`.

## Active roadmap

No new feature work is planned before validation.

The remaining work is empirical validation of the already-implemented workflow/rule changes:

- See `model-tests/FINDINGS.md` for F1-F4 rows marked `validation pending`.
- See `model-tests/REVISED-PLAN-SECOND-REVIEW.md` for the validation matrix and acceptance criteria.
- See `model-tests/RUNBOOK.md` for the operator procedure.
- See `PRD.md` for the issue -> branch -> PR workflow and phase roadmap.

Recommended next validation sequence:

1. AGENTS-only T2 x2.
2. Pack-enabled T2 x2.
3. Pack-enabled T1 x2.
4. T3 x2 under a held-constant harness.
5. If any pair splits 1-1, run a third trial before changing wording.

## Do not confuse with current work

- `model-tests/REVISED-PLAN.md` is historical rationale, not the current roadmap.
- `model-tests/REVISED-PLAN-SECOND-REVIEW.md` is implemented guidance plus validation criteria.
- `model-tests/runs/` is ignored by design; do not reintroduce bulky transcripts or generated projects into the repository.
