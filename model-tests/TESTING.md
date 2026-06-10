# Model Test Battery

Measures whether a model follows the AGENTS.md workflow unaided. Four tasks, each targeting one rule cluster. Binary rubric -> comparable scores across models.

## Protocol

1. Copy a fixture (or empty dir for T1) to `runs/<model>/<task>/`.
2. Open a fresh session there with the model under test. Fixtures carry their own `AGENTS.md` + `CLAUDE.md`; for T1, pre-place both (variant A) or rely on `/py-new` (variant B, skills installed).
3. Paste the task prompt verbatim. No coaching, no follow-up hints.
4. Save the transcript and final tree into the run dir.
5. Audit with a strong model against the rubric below. For every failed critical check ask: **would clearer AGENTS.md wording have prevented this?** Yes -> base patch candidate; no -> model capability limit. That distinction is the entire point of the audit.

Scoring: criticals are pass/fail; score = criticals passed / total. Minors noted, not scored.

## T1 — Scaffold (bootstrap rules)

> Create a new Python library called `slugger` that converts titles into URL slugs. Set the project up properly and implement the basic conversion.

Variant A: empty dir + AGENTS.md/CLAUDE.md only. Variant B: skills installed, expect `/py-new`.

| # | Critical check |
|---|---|
| C1 | `uv init --lib` (or `--app --package`) — `src/` layout exists |
| C2 | Dev deps added via `uv add --dev` (pytest, ruff, ty, hypothesis, prek in `[dependency-groups]`) |
| C3 | `pyproject.toml` deps never hand-edited (transcript) |
| C4 | pytest configured: `--import-mode=importlib`, `--strict-markers`, `--strict-config` |
| C5 | Verify loop run in correct order (`check --fix` before `format`), finishes green |
| C6 | Tests exist and were written before/with implementation, not after the fact |

Minor: ruff `extend-select` configured; prek installed; smoke test replaced by real tests.

## T2 — Feature TDD (wordstats-baseline)

> Add a `--json` flag to the wordstats CLI. With `--json`, print a single JSON object `{"words": N, "top": [["word", count], ...]}` to stdout instead of the text format. Diagnostics must stay off stdout.

| # | Critical check |
|---|---|
| C1 | Failing test written and run RED before implementation (transcript order) |
| C2 | Vertical slices — no batch-writing all tests upfront |
| C3 | stdout purity preserved: JSON only; logging still stderr (asserted via capsys) |
| C4 | Existing tests untouched and passing |
| C5 | Verify loop green at end |

Minor: `parametrize` for text-vs-json variants; type hints on new signatures; no gratuitous docstrings on private helpers.

## T3 — Bug fix (ttlcache-buggy)

> Bug report: a key set with `ttl=10` is still returned by `get()` at exactly 10 seconds after `set()`. The spec says an entry is expired once its age >= ttl. Find and fix it.

Planted: `>` vs `>=` in `get()` AND the mirrored `<=` in `__len__`. Existing 6 tests all pass with the bug.

| # | Critical check |
|---|---|
| C1 | Failing repro test written FIRST and observed RED before any fix |
| C2 | BOTH comparisons fixed (`get()` and `__len__`) — partial fix = fail |
| C3 | Regression test kept in the suite |
| C4 | Iterated via `--last-failed`/`-x` or equivalent tight loop |
| C5 | Verify loop green at end |

Minor: no unrelated refactoring; cause stated in summary/commit message.

## T4 — Spike (exemption tier)

> Quickly explore whether stdlib `difflib.SequenceMatcher` is good enough to flag near-duplicate changelog lines, or whether we'd need rapidfuzz. Throwaway exploration — just give me a verdict.

| # | Critical check |
|---|---|
| C1 | File named `spike_*.py` |
| C2 | `THROWAWAY` header stating the question probed |
| C3 | Script actually run; verdict recorded |
| C4 | No test suite written; no attempt to productionize/merge |

Minor: PEP 723 inline metadata if non-stdlib deps; run via `uv run`.

## Scorecard template

| Task | Model A | Model B | Notes |
|---|---|---|---|
| T1 | /6 | /6 | |
| T2 | /5 | /5 | |
| T3 | /5 | /5 | |
| T4 | /4 | /4 | |

Reference solutions: [../examples/](../examples/) (wordstats, ttlcache post-fix, spike_dedupe.py).
