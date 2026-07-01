# Change Log

## 2026-06-15 — Revised plan implementation

### Agent rules

- Required a valid RED before production edits for behavior changes and bug fixes.
- Defined valid RED as a test that collects, executes, and fails because the requested behavior is missing or wrong.
- Clarified that scaffold smoke tests do not replace tests of requested behavior.
- Required assertions for each intentionally changed public operation or observable branch, without prescribing internal-path tests.
- Required throwaway spikes to be deleted before handoff unless the user asks to keep them.
- Kept the root `AGENTS.md` and the `py-new` template synchronized.

### Skills

- Broadened `tdd` to trigger on user-visible behavior changes and straightforward reproducible bugs.
- Made `tdd` infer settled interface and design decisions from the request and repository before asking questions.
- Narrowed `diagnose` to uncertain, intermittent, cross-system, performance, or unclear-cause failures.
- Extended `py-new` through the first requested behavior instead of ending at a passing scaffold.
- Updated the skill catalog to match the revised lifecycle and spike policy.

### Evaluation protocol

- Split scoring into functional correctness and workflow adherence.
- Added a separate validity label so contaminated or incomplete runs cannot pass silently.
- Required the canonical `AGENTS.md` overlay for every run.
- Added `run.json` metadata for requested model, provider-reported model, harness, isolation, prompt, rule hash, timestamps, and interventions.
- Added copy exclusions for VCS, environment, cache, and harness artifacts.
- Added repeated-trial guidance for noisy model outcomes.
- Added explicit trial identifiers and fail-if-exists run directories so repeated trials cannot overwrite each other.

### Transcript tooling

- Added `model-tests/scripts/extract_opencode_transcript.py` to produce reviewable Markdown from opencode HTML exports while omitting hidden reasoning. Diagnostics go through `logging` to stderr with a `--verbose` flag; transcript output goes to stdout or `--output`.
- Added focused tests covering file and stdout rendering, messages, tool calls, tool results, provider/model metadata, malformed and missing exports, and a `hypothesis` property test that arbitrary session-data payloads never crash the parser. Tests call `main()` directly.
- Added `model-tests/pyproject.toml` and `uv.lock` so the harness runs the standard `uv run ruff/ty/pytest` verify loop with pinned dev dependencies.

### Records

- Added a committed run-log format separating requested and provider-reported models, harness, isolation, and validity.
- Marked historical in-repo opencode runs as contaminated rather than directly comparable.
- Updated `FINDINGS.md` to distinguish implemented patches from validation still required.

### Deliberate omissions

- Did not add an `hasattr()` scaffold cycle; it would reward structural smoke tests over behavior.
- Did not require tests for internal implementation paths; the rule targets observable behavior.
- Did not add a repository-wide ASCII-only rule or mandatory final-command recital; neither was supported by the model-test evidence.

### Validation

- Transcript extractor: Ruff lint/format clean, `ty` clean, 5 tests passed, and real Deepseek and big-pickle exports rendered tool events without hidden reasoning.
- Root/template `AGENTS.md`: byte-identical SHA-256 `6ECBAE38C34FB186A011ACCE77BCFBD5CE56FFB2EFFDD67B032D43A34E161CD9`.
- `examples/ttlcache`: full verify loop passed, including 7 tests.
- `examples/wordstats`: full verify loop passed, including 19 tests.
- Isolated pack deployment: revised `tdd`, `diagnose`, `py-new`, and canonical AGENTS template copied to `C:\Users\Davis\claude-test-pack\skills` and hash-checked.
- Skill structure: `tdd`, `diagnose`, and `py-new` all passed the `skill-creator` `quick_validate.py` check.
- Empirical acceptance matrix: not run in this change set; it requires interactive model sessions. Use the two-trial conditions in `RUNBOOK.md` and `REVISED-PLAN-SECOND-REVIEW.md` before marking F1-F4 validated.

## 2026-06-18 — Pre-ship audit-record fixes

- Added [RUNS-LOG.md](RUNS-LOG.md) as the committed run index; `model-tests/runs/` remains ignored for bulky transcripts, generated projects, and caches.
- Extended the runbook's `run.json` recipe with `repo_commit`, `skills_hash_root`, `skills_tree_sha256`, and `claude_config_dir` so future runs preserve both rule and skill provenance.
- Updated the runbook to launch from the same `claude_config_dir` recorded in `run.json`.
- Corrected stale changelog wording around the run-log path, pack/config metadata, and transcript-extractor test count.

## 2026-06-20 — Roadmap status cleanup

- Marked [REVISED-PLAN.md](REVISED-PLAN.md) as superseded historical rationale rather than an active hold.
- Marked [REVISED-PLAN-SECOND-REVIEW.md](REVISED-PLAN-SECOND-REVIEW.md) as implemented with validation pending.
- Clarified that the active roadmap is now the F1-F4 validation matrix in [FINDINGS.md](FINDINGS.md) and [RUNBOOK.md](RUNBOOK.md).
