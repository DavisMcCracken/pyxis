# Model Test Battery

Measures functional results and workflow compliance under a recorded harness. Four tasks target the main rule clusters.

## Protocol

1. **Run outside this repository.** Use a path such as `C:\Users\Davis\model-test-runs\<model>\<task>`. A model that can read this repo, reference solutions, other runs, or undeclared skills is contaminated.
2. Copy the task fixture into the clean run directory. Then overlay the current canonical `skills/py-new/templates/AGENTS.md`; do not rely on the fixture's stored snapshot.
3. Record `run.json` before launch: requested model, harness, cwd, isolation mode, AGENTS hash, prompt, start time, and operator interventions. Add provider-reported model and finish time after the run.
4. **Phase 1 default:** use an isolated config. `claude-test-pack` contains only this skill pack; `claude-test-bare` contains no skills. Pack auto-triggering is expected and scored.
5. Launch from the run directory, fresh session per task, and paste the prompt verbatim. No coaching. If the model asks a question, answer exactly `use your judgment` and record it.
6. Approve permission prompts only. When the model declares done, export the transcript and close the session.
7. Copy source, tests, transcript, and metadata back to `runs/<model>/<task>/<trial>/`. Exclude nested Git data, environments, caches, bytecode, Hypothesis state, and Zone Identifier files.
8. Audit against the rubric. For each workflow failure ask whether clearer rules or a procedural skill could reasonably prevent it; otherwise record a model capability limit.

Reference solutions under `examples/` are for auditors only and must not be reachable by the model during a run.

## Reporting

Report two scores and one validity label per task:

1. **Functional score** - requested behavior and final correctness.
2. **Workflow score** - test order, vertical slices, retained coverage, and verification.
3. **Run validity** - `valid`, `cross-harness`, or `contaminated`, with a short reason.

Do not merge scores across harness types or validity labels. A failed prerequisite is a failed workflow check, not a vacuous pass or ratio-friendly N/A.

## Valid RED

The intended test must collect and execute, then fail for the missing or incorrect behavior. Import, collection, syntax, fixture, and unrelated setup failures do not count.

## T1 - Scaffold

> Create a new Python library called `slugger` that converts titles into URL slugs. Set the project up properly and implement the basic conversion.

Variant A: rules only. Variant B: pack installed; expect `py-new`.

| ID | Dimension | Critical check |
|---|---|---|
| F1 | Functional | `uv init --lib` (or `--app --package`) produced a `src/` layout |
| F2 | Functional | Dev dependencies were added via `uv add --dev`: pytest, ruff, ty, hypothesis, prek |
| F3 | Functional | Dependencies were never hand-edited in `pyproject.toml` |
| F4 | Functional | pytest has `--import-mode=importlib`, `--strict-markers`, `--strict-config` |
| F5 | Functional | Basic slug conversion is correct and covered by a behavior test |
| W1 | Workflow | A real conversion test was written and observed at valid RED before feature implementation |
| W2 | Workflow | Full verify loop ran in the required order and finished green |

Audit probe: revert or replace the core conversion; at least one behavior test must fail. An import, `hasattr`, or callability smoke test is insufficient.

Minor: ruff `extend-select` configured; prek installed; generated smoke test replaced once real coverage exists.

## T2 - Feature TDD

> Add a `--json` flag to the wordstats CLI. With `--json`, print a single JSON object `{"words": N, "top": [["word", count], ...]}` to stdout instead of the text format. Diagnostics must stay off stdout.

| ID | Dimension | Critical check |
|---|---|---|
| F1 | Functional | JSON output matches the requested shape and respects `--top` |
| F2 | Functional | stdout is JSON only and diagnostics remain on stderr, asserted via `capsys` |
| F3 | Functional | Existing behavior remains passing |
| W1 | Workflow | One behavior test reached valid RED before any production edit |
| W2 | Workflow | At least one complete one-test RED-GREEN slice occurred before later tests; implementation-first and batch-tests-first fail |
| W3 | Workflow | Full verify loop finished green |

Minor: `parametrize` for related variants; type hints on changed public signatures; no gratuitous private docstrings.

## T3 - Bug Fix

> Bug report: a key set with `ttl=10` is still returned by `get()` at exactly 10 seconds after `set()`. The spec says an entry is expired once its age >= ttl. Find and fix it.

Planted bug: `>` vs `>=` in `get()` and mirrored `<=` in `__len__`. Existing tests pass before the fix.

| ID | Dimension | Critical check |
|---|---|---|
| F1 | Functional | Both public behaviors are corrected: `get()` and `len()` expire at the boundary |
| W1 | Workflow | A reproducing test reached valid RED before any fix |
| W2 | Workflow | Retained regression assertions cover both intentionally changed public operations |
| W3 | Workflow | The repro drove a narrow RED-GREEN iteration (`--last-failed`, `-x`, or targeted equivalent) |
| W4 | Workflow | Full verify loop finished green |

Audit probe: independently revert each comparison; a retained regression test must fail for each revert.

Minor: no unrelated refactor; cause stated in the final summary or commit message.

## T4 - Spike

> Quickly explore whether stdlib `difflib.SequenceMatcher` is good enough to flag near-duplicate changelog lines, or whether we'd need rapidfuzz. Throwaway exploration - just give me a verdict.

| ID | Dimension | Critical check |
|---|---|---|
| F1 | Functional | Script was run and produced evidence supporting a clear verdict |
| W1 | Workflow | Temporary file was named `spike_*.py` and carried a `THROWAWAY` header stating the question |
| W2 | Workflow | No test suite or production integration was added |
| W3 | Workflow | Verdict was recorded, then the spike was deleted before handoff unless the user asked to keep it |

The transcript proves creation and execution; final file presence is not required. Minor: PEP 723 metadata for third-party dependencies; run via `uv run`.

## Scorecard Template

| Task | Functional | Workflow | Validity | Notes |
|---|---:|---:|---|---|
| T1 | /5 | /2 | | |
| T2 | /3 | /3 | | |
| T3 | /1 | /4 | | |
| T4 | /1 | /3 | | |

Reference solutions: [../examples/](../examples/). Audit procedure: [RUNBOOK.md](RUNBOOK.md).
