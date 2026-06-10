---
name: tdd
description: Test-driven development with red-green-refactor loop. Use when user wants to build features or fix bugs using TDD, mentions "red-green-refactor", wants integration tests, or asks for test-first development.
---

# Test-Driven Development

## Philosophy

**Core principle**: Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't.

**Good tests** exercise real code paths through public APIs. They describe _what_ the system does, not _how_. A good test reads like a specification — "user can checkout with valid cart" tells you exactly what capability exists. These tests survive refactors because they don't care about internal structure.

**Bad tests** are coupled to implementation: they mock internal collaborators, test private functions, or verify through external means (querying the database directly instead of using the interface). The warning sign: your test breaks when you refactor but behavior hasn't changed.

See [tests.md](tests.md) for Python examples and the faking/mocking rules. The architecture vocabulary (module, interface, seam, depth) is defined in [../_shared/LANGUAGE.md](../_shared/LANGUAGE.md).

## Anti-Pattern: Horizontal Slices

**DO NOT write all tests first, then all implementation.** Bulk-written tests encode _imagined_ behavior, not actual behavior — they test the shape of things (signatures, data structures) rather than what callers care about, and they commit you to test structure before you understand the implementation.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED->GREEN: test1->impl1
  RED->GREEN: test2->impl2
  ...
```

One test -> minimal implementation -> repeat. Each test responds to what the previous cycle taught you. (This is the same rule as the AGENTS.md Workflow section — the skill is the long form.)

## Workflow

### 1. Plan

If the project keeps domain docs, use the `CONTEXT.md` glossary so test names and interface vocabulary match the project's language, and respect ADRs in the area you're touching.

Before writing any code:

- Confirm with the user: what should the public interface look like, and which behaviors matter most? You can't test everything — prioritize critical paths and complex logic over exhaustive edge cases.
- Design the interface for depth and testability: accept dependencies, don't create them; return results, don't produce side effects; small surface. See [../_shared/LANGUAGE.md](../_shared/LANGUAGE.md).
- List behaviors to test (not implementation steps).

For a non-trivial design (new module, schema, public API, algorithm choice), state 2–3 candidate approaches with trade-offs first — AGENTS.md Workflow rule. For a full interactive design session, the `grill-me` skill is the heavyweight version.

### 2. Tracer bullet

Write ONE test that confirms ONE thing end-to-end:

```
RED:   write test for first behavior -> watch it fail
GREEN: minimal code to pass -> watch it pass
```

The failure must be the assertion failing — a collection error or `ImportError` is not RED, it's a broken test.

### 3. Incremental loop

For each remaining behavior: RED -> GREEN. Rules:

- One test at a time; only enough code to pass it; don't anticipate future tests.
- Iterate with `uv run pytest --last-failed -x`.
- Collapse near-duplicate cases with `@pytest.mark.parametrize` instead of copy-pasting tests.
- Reach for `hypothesis` when the unit is a parser, serializer, or numeric edge-case farm.

### 4. Refactor

Only at GREEN, never while RED. Candidates:

- Duplication -> extract function/class
- Long functions -> private helpers (tests stay on the public interface)
- Shallow modules -> combine or deepen ([../_shared/LANGUAGE.md](../_shared/LANGUAGE.md))
- Feature envy -> move logic to where the data lives
- Primitive obsession -> introduce a value type
- Problems the new code reveals in existing code

Run tests after each refactor step. After the change set, run the full verify loop from AGENTS.md (`ruff check --fix` -> `ruff format` -> `ty check` -> `pytest`).

## Bug fixes

Enter the loop at RED: reproduce the bug with a failing test before touching the fix — no exceptions (AGENTS.md Workflow rule). If you can't reproduce it, stop TDD and switch to the `diagnose` skill; come back with its minimised repro as your first test.

## Checklist per cycle

```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive an internal refactor
[ ] RED was a real assertion failure, not a collection error
[ ] Code is minimal for this test
[ ] No speculative features added
```
