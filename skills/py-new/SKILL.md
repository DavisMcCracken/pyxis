---
name: py-new
description: Scaffold a new Python project on the uv + ruff + ty + pytest + prek stack with the AGENTS.md base, green verify loop from commit zero. Use when the user wants to start, create, bootstrap, or scaffold a new Python project, package, library, CLI, or repo.
---

# New Python Project

Scaffold a project that passes the verify loop green before handover. The base rules live in [templates/AGENTS.md](./templates/AGENTS.md) — that copy is canonical; edit it there when the base evolves (existing repos keep their snapshots).

## 1. Resolve decisions (lightweight — not a full grill)

Ask one at a time, each with a recommended default. Skip any question the user's request already answers. If the user says "defaults" or "just set it up", take all defaults silently and proceed.

1. **Name** — package name (snake_case importable). Default: derive from the user's description.
2. **Kind** — what is it?
   - Importable library (default) -> `uv init --lib <name>`
   - CLI tool -> `uv init --app --package <name>` (gives `src/` layout + `[project.scripts]` entry)
   - Bare `uv init --app` is off the table — AGENTS.md mandates `src/` layout.
3. **Known runtime dependencies** — any to add now? Default: none; add later with `uv add`.

Do not ask about git remotes, CI, or licensing — out of scope, user wires those later.

## 2. Scaffold

Run in order:

1. `uv init --lib <name>` (or `--app --package <name>`)
2. `uv add --dev pytest ruff ty hypothesis prek` then `uv add <runtime deps>` if any
3. Append [templates/pyproject-snippet.toml](./templates/pyproject-snippet.toml) to the generated `pyproject.toml`
4. Copy [templates/AGENTS.md](./templates/AGENTS.md) into the repo root as `AGENTS.md`; write `CLAUDE.md` containing exactly `@AGENTS.md`. If either file already exists, don't overwrite — show a diff against the template and ask.
5. Copy [templates/pre-commit-config.yaml](./templates/pre-commit-config.yaml) to `.pre-commit-config.yaml`
6. Write `tests/test_smoke.py` — import the package's public surface and make one real assertion (e.g. against the generated `hello()`), so pytest collects at least one test (zero tests = exit code 5 = verify loop red). Note in the test that it should be replaced by the first real test.
7. `git init` if not already a repo, then `uv run prek install`

## 3. Verify

Run the full loop from `AGENTS.md`:

```
uv run ruff check --fix && uv run ruff format && uv run ty check && uv run pytest
```

All four must pass. Fix anything red before handing over — the user receives a working repo, not a TODO list. Offer (don't auto-run) an initial commit.

## 4. Hand over

Report: tree of what was created, the verify-loop result, and next steps — `uv add` real dependencies, trim `AGENTS.md` sections that don't fit this project, start the first feature test-first (the `/tdd` skill fits here).
