# AGENTS.md — Python Project Base

Template: copy into each repo, trim or extend to fit the project.

## Tooling

- Manage environments and dependencies with `uv`. Run everything through `uv run`.
- New project: `uv init --lib` (or `--app`), then `uv add --dev pytest ruff ty hypothesis prek`.
- Add dependencies with `uv add` (`--dev` for dev tools). Never hand-edit dependencies in `pyproject.toml`.
- Commit `uv.lock`. After pulling, run `uv sync`.
- Single-file scripts declare dependencies inline via PEP 723 (`# /// script`); run with `uv run script.py`.
- All tool config (ruff, ty, pytest) lives in `pyproject.toml` — single source of truth.
- Ruff lint: default rules plus `I`, `UP`, `B`, `SIM`, `RUF`. Leave line length to the formatter — don't enable the full `E` class.
- After each change set and before handoff, run the verify loop (lint-fix before format — fixes can produce unformatted code):
  `uv run ruff check --fix && uv run ruff format && uv run ty check && uv run pytest`
- Git hooks run via `prek` (config in `.pre-commit-config.yaml`; `prek install` once per clone). Fix hook failures; never bypass with `--no-verify`.

## Workflow

- Behavior change or bug fix (including a new function, CLI flag, option, endpoint, output format, or error behavior): before editing production code, write one test and run it. RED means the intended test collected and executed, then failed for the missing or incorrect behavior; import, collection, syntax, fixture, and unrelated setup failures do not count. No exceptions.
- A new-project scaffold may reach green first, but requested product behavior still follows the rule above. A smoke, import, `hasattr`, or callability test does not count as behavior coverage.
- One test -> minimal implementation -> repeat. Don't batch-write all tests upfront — bulk tests encode imagined behavior, not actual behavior.
- Bug or regression: keep the reproducing test. If the fix intentionally changes multiple public operations or observable branches, write a retained test for each — reverting any one changed operation alone must fail a test. Do not test internal paths merely because they were edited. Example: if one bug fix edits the validation logic in both an `add()` and a `contains()` method, each change needs its own retained assertion at the failing input — reverting either `add()` or `contains()` alone must break a test.
- Exploratory spike or throwaway script: tests optional, never merge it. Name it `spike_*.py` with a `THROWAWAY` header stating the question; run it, record the verdict, then delete it before handoff unless the user asks to keep it.
- Non-trivial design decision (new module, schema, public API, algorithm choice): state 2–3 candidate approaches with trade-offs, pick one, then implement. Skip for routine edits.

## Laziness

- Understand the problem before writing code — trace the real flow end to end. The ladder below shortens the solution, never the reading; a small diff in the wrong place is a second bug.
- Then take the first rung that holds: (1) does this need to exist at all? Speculative need → skip it. (2) Already in this codebase — a helper, type, or pattern? Reuse it. (3) Stdlib does it? Use it. (4) Native platform or language feature covers it? Use it over a dependency. (5) An already-installed dependency solves it? Use it — never add a new dep for what a few lines do. (6) Can it be one line? One line. (7) Only then: the minimum code that works.
- Deletion over addition; boring over clever. No abstraction with one caller, no factory for one product, no config for a value that never changes, no scaffolding "for later".
- Bug fix = root cause, not symptom. Grep every caller of the function you're about to touch; fix it once where they all route through, not per-caller.
- Mark a deliberate shortcut with a `# shortcut:` comment naming the ceiling and the upgrade path (e.g. `# shortcut: O(n^2) scan, index if the list grows`). Never simplify away input validation, error handling that prevents data loss, security, or accessibility.

## Testing

- Test real code. Fake only at system boundaries: network, clock, filesystem, env.
- Prefer `monkeypatch` or hand-written fakes over `unittest.mock.MagicMock`. Never mock the unit under test.
- Put fixtures shared by 2+ test modules in `conftest.py`; keep single-use fixtures local.
- Use `@pytest.mark.parametrize` instead of copy-pasted test variants.
- Use `hypothesis` for parsers, serializers, and numeric edge cases.
- Iterate on failures with `uv run pytest --last-failed -x`.
- Configure pytest in `[tool.pytest.ini_options]` with `--import-mode=importlib`, `--strict-markers`, `--strict-config`.

## Code Style

- Type hints on all public function signatures.
- Never use `cast()`, `# type: ignore`, or `Any` to silence the type checker — fix the types. Exception: boundary layers (deserialization, third-party gaps), each with a short reason comment.
- Modern typing: `X | None` not `Optional[X]`; `list[str]` not `typing.List`. On 3.12+, use PEP 695: `type Alias = ...` for aliases, `def f[T](x: T) -> T` for generics — no `TypeVar` ceremony.
- Annotate signatures, not locals. Let inference handle local variables.
- Docstrings: Google style, public API only. One-line summary minimum; extended sections only when behavior is non-obvious. Doctests optional, pure functions only.
- Library code logs via `logging`, never `print`. CLIs: program output to stdout, diagnostics via logging to stderr.
- Module-level `logger = logging.getLogger(__name__)`; configure logging only at the entrypoint.
- CLI tools take a `--verbose` flag (sets log level DEBUG; default INFO).
- CLI entrypoint: `def main(argv: list[str] | None = None) -> int` so tests can call it directly; `sys.exit(main())` only under `if __name__ == "__main__"`.
- Never `except Exception: pass`. Catch narrow exceptions, re-raise or `logger.exception()`. Let unexpected errors crash loudly.

## Layout & Security

- Use `src/` layout; tests mirror the package structure under `tests/`.
- Never put secrets in code or version control. Read them from env vars or a config layer.
