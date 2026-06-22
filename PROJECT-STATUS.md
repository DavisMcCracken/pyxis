# Project Status

Status date: 2026-06-22
Latest verified PRD baseline commit: `148dc4a`

## Stable usable state

The repository is in a stable docs-and-test baseline suitable for normal use of the rule base, skill pack, examples, and model-test harness. PRD.md now governs the phase roadmap and issue -> branch -> PR workflow.

Current stable scope:

- Root `AGENTS.md` and `skills/py-new/templates/AGENTS.md` are the canonical synchronized Python project rules.
- `skills/` contains the deployable skill pack: `py-new`, `grill-me`, `tdd`, `diagnose`, `improve-codebase-architecture`, and `_shared` references.
- `examples/wordstats` and `examples/ttlcache` are green reference projects.
- `model-tests/` contains the model-test rubric, runbook, findings ledger, transcript extractor, and committed run index.
- Bulky historical run artifacts are intentionally not in the repository path; they are archived locally under `/home/hermes/projects/archive/skills-model-test-runs-2026-06-20`.
- Active validation runs (issues #6-#9) and reusable launch/audit helper scripts live under `/home/hermes/model-test-runs/`; each run dir has `run.json` provenance and a `transcript.jsonl`. This path is outside the repo and gitignored.
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

Latest full audit result after PR #16 merged:

- `model-tests`: 5 tests passed; ruff, format check, and ty passed.
- `examples/wordstats`: 19 tests passed; ruff, format check, and ty passed.
- `examples/ttlcache`: 7 tests passed; ruff, format check, and ty passed.
- Markdown relative links resolved.
- Skill frontmatter checked clean.
- Working tree was clean on `main` and matched `origin/main`.

## Active roadmap

No new feature work is planned before validation. Future feature development should start from GitHub issues and use isolated branches or worktrees after Phase 1 is complete or explicitly waived in PRD.md.

The remaining Phase 1 work is empirical validation of the already-implemented workflow/rule changes:

- See `model-tests/FINDINGS.md` for F1-F4 rows marked `validation pending`.
- See `PRD.md` for the current validation matrix and acceptance criteria.
- See `model-tests/RUNBOOK.md` for the operator procedure.
- See `model-tests/REVISED-PLAN-SECOND-REVIEW.md` for historical implemented guidance behind the matrix.

Open validation / follow-up issues:

1. #22 F1 follow-up: strengthen multi-operation rule wording and re-validate T3.
2. #10 Summarize validation results and update ledgers.
3. #14 Investigate Claude Code skill auto-trigger evidence for `tdd`.
4. #17 Set up clean OpenCode model-test harness after Phase 1 summary.

Recommended next validation sequence:

1. Resolve the F1 wording follow-up (#22): add an explicit multi-operation example, then re-validate T3.
2. Summarize Phase 1 and update ledgers (#10).
3. Resolve or precisely defer the `tdd` skill-trigger evidence question (#14).
4. After Phase 1 is summarized, set up and document a clean OpenCode harness (#17).

Completed Phase 1 validation:

- #6 AGENTS-only T2 x2: validated.
- #7 Pack-enabled T2 x2: behavior validated; explicit `tdd` trigger evidence remains #14.
- #8 Pack-enabled T1 x2: `py-new` handoff validated.
- #9 T3 regression closure x2 (held-constant bare, haiku): validation performed; **negative result** — both trials fixed `get()` and `__len__` but guarded `get()` only, leaving `__len__()` unguarded (audit probe: revert stays green). F1 rule-text patch insufficient.
- #19 Pack-enabled T3 follow-up x2 (Claude Code print, haiku): validation performed; **negative result** — both trials repeated the same gap despite the skill pack being visible. Pack visibility did not close F1; follow-up #22 tracks explicit multi-operation rule wording and re-validation.

## Do not confuse with current work

- `model-tests/REVISED-PLAN.md` is historical rationale, not the current roadmap.
- `model-tests/REVISED-PLAN-SECOND-REVIEW.md` is implemented guidance plus validation criteria.
- `model-tests/runs/` is ignored by design; do not reintroduce bulky transcripts or generated projects into the repository.
