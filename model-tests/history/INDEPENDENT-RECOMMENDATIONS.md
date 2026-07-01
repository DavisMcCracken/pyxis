# Independent recommendations from the model-test results

Date: 2026-06-15.

Scope: reviewed `PATCH-REVIEW.md`, `FINDINGS.md`, `TESTING.md`, `RUNBOOK.md`, all 12 per-run audits, the available transcripts, produced code/tests, root `AGENTS.md`, and the relevant `py-new`, `tdd`, and `diagnose` skills.

This document proposes changes only. It does not apply them.

## Executive verdict

The existing patch review correctly identifies the universal T2 failure and the missing `__len__` regression coverage. I would apply the intent of Patch A, but not exactly as written.

The strongest result is not merely that weak models need more emphatic prose. It is that they follow a short procedural sequence more reliably than a distributed set of rules. The improvements should therefore combine:

1. A compact pre-edit gate in `AGENTS.md`.
2. A proactive `tdd` skill with a concrete first-action checklist.
3. A `py-new` handoff that treats requested domain behavior as separate from scaffolding.
4. Non-overlapping `tdd` and `diagnose` triggers.
5. A stricter battery that does not award credit for invalid RED states or vacuous workflow checks.

The current totals overstate workflow compliance. T1 was scored 6/6 for every model, but:

- Haiku never ran a feature test RED and left the actual slug conversion untested.
- DeepSeek and big-pickle treated an import/collection error as RED, despite `tdd/SKILL.md` explicitly saying that does not count.
- The opencode T1 runs were contaminated by reading `py-new` from the parent repository.

Those are battery and skill-design findings, not just model findings.

## Priority 1: replace the soft feature rule with a pre-edit gate

Patch A adds examples and `No exceptions`. Keep those ideas, but make the rule operational and distinguish existing projects from new scaffolds.

Proposed `AGENTS.md` wording:

```md
## Workflow

- Existing codebase: for any user-visible behavior change or bug fix, do not edit production code first. Add one test, run it, and observe it fail for the expected behavioral reason before changing implementation. Collection errors, import errors, and unrelated failures do not count as RED. No exceptions.
- New project: scaffold the project and get the baseline verify loop green first. Then treat the requested domain behavior as a feature: observe a real behavior test fail before implementing it. A smoke/import test does not replace a behavior test.
- A new function, CLI flag, option, endpoint, output format, or changed error behavior all count as behavior changes.
- One test -> minimal implementation -> repeat. Do not batch-write the full test matrix before the first implementation.
- Bug or regression: keep the reproducing test in the suite. If the fix changes multiple public call paths or observable branches, add assertions for each changed path.
```

Why this is stronger than the current Patch A:

- It addresses the shared opencode pattern: editing existing production code before tests.
- It closes the T1 loophole where a scaffold smoke test substitutes for the requested feature test.
- It defines valid RED, preventing collection/import failures from being mislabeled.
- It retains the useful examples from F3 and the multi-path coverage rule from F1.

Apply this to both `AGENTS.md` copies, then add an automated equality check because `skills/py-new/templates/AGENTS.md` is documented as canonical while the root copy governs this repo.

## Priority 2: change `tdd` and `diagnose` together

Broadening only the `tdd` description creates a collision with `diagnose`, whose current frontmatter says to trigger whenever a user reports any bug even though its body says ordinary bugs do not need the skill.

Proposed `tdd` frontmatter:

```yaml
name: tdd
description: Test-driven implementation for any new user-visible behavior in an existing project, including functions, CLI flags, options, endpoints, output formats, and ordinary reproducible bug fixes. Use proactively even when the user does not mention TDD or tests. Do not use for scaffolding-only work or hard, intermittent, unknown-cause diagnosis.
```

Proposed `diagnose` frontmatter:

```yaml
name: diagnose
description: Diagnose hard-to-reproduce, intermittent, cross-system, unknown-cause bugs and performance regressions. Use when a reliable repro does not yet exist or investigation and instrumentation are required. Do not use for an ordinary localized bug with an obvious failing test; use tdd instead.
```

Add this near the top of `tdd/SKILL.md`, before the philosophy section:

```md
## Non-negotiable first action

Before editing production code:

1. Name the public behavior being changed.
2. Add one test for that behavior.
3. Run the narrowest useful test command.
4. Confirm the test executed and failed for the expected assertion.

An import error, collection error, syntax error, or unrelated failure is not RED. For a brand-new public symbol, first import the package/module and assert that the public symbol is exposed without importing the missing symbol directly; then drive its behavior one test at a time.
```

Add a finish gate to `tdd/SKILL.md`:

```md
Before the full verify loop, review the production paths changed by the patch. Every intentionally changed public path or observable branch must be exercised by a test assertion. A source change justified only as "for consistency" still needs a test if it changes behavior.
```

That final sentence directly targets both T3 runs that changed `__len__` without pinning its boundary behavior.

## Priority 3: make `py-new` finish the requested feature

`py-new` auto-triggered successfully for Haiku T1, but its procedure ends after a green scaffold and merely suggests `/tdd` as a next step. That allowed the model to implement `slugify()` with only an existence smoke test.

Add a phase between `Verify` and `Hand over`:

```md
## 4. Implement requested behavior

If the user's request includes behavior beyond project setup, the task is not complete when the scaffold is green.

1. Load/follow the `tdd` procedure if available.
2. Add one real behavior test and observe valid RED before implementing the behavior.
3. Implement one behavior at a time.
4. Replace the generated smoke test only after real behavior coverage exists.
5. Run the full verify loop again.

Do not hand over a requested feature with only an import, `hasattr`, or callability test.
```

Also tighten the decision section:

- If name and project kind are already specified and no runtime dependency is implied, take defaults silently.
- Create the project under the current working directory unless the user names another location. Do not relocate it because the directory looks temporary or test-related.

This would have prevented DeepSeek T1 from asking unnecessary questions and writing outside the prepared run directory.

## Priority 4: choose deletion for throwaway spikes

I disagree with `PATCH-REVIEW.md`'s recommendation to keep spike files by default.

The current `diagnose` skill already says `Throwaway harnesses deleted - spike_*.py never merges`. Changing `AGENTS.md` to require keeping spikes would create a direct cross-document contradiction and increase the chance that throwaway code is committed.

Recommended rule:

```md
- Exploratory spike or throwaway script: tests optional, never merge it. Name it `spike_*.py` with a `THROWAWAY` header stating the question probed; run it, record the verdict in the final response or a durable project note, then delete the script before handoff unless the user asks to keep it or the repo has a designated experiments area.
```

The checked-in `examples/spike_dedupe.py` is a test/reference fixture, not a good default lifecycle for production repositories.

Update T4 so deletion after the verdict remains a clean pass. The transcript should prove C1-C3; final file presence should not be required.

## Priority 5: fix rubric inflation before using totals for decisions

### T1

Replace C6 with two checks:

- A real slug-conversion behavior test existed before substantive feature implementation.
- The test was run and failed for the expected behavioral assertion. Import/collection failure does not count.

Add a test-adequacy mutation: temporarily replace the implementation with a constant or revert the core conversion and confirm at least one new test fails.

### T2

- C2 cannot pass vacuously when no tests were written. Mark it FAIL or N/A and do not count it as a pass.
- Separate functional correctness from workflow discipline. A correct feature written implementation-first should not look like a near-perfect task result when TDD ordering is the purpose of the task.

### T3

- C4 cannot pass when no RED-GREEN loop occurred. Big-pickle's ad-hoc check is not a tight iteration loop.
- Automate the coverage check: revert each changed comparison independently and run the resulting regression tests. If either revert stays green, regression coverage is incomplete.

### Overall scoring

Report three dimensions instead of one cross-harness total:

1. Functional result.
2. Workflow compliance.
3. Harness validity/isolation.

Do not compare a Claude Code skill-pack run directly with a skill-less opencode run in one total. The latter is still useful as an instruction-robustness test.

## Priority 6: make runs reproducible and auditable

Before more patch validation:

- Run every model outside this repository so it cannot read reference solutions, other model outputs, `.agents/skills`, or the fact that it is under test.
- Copy back only source, tests, transcript, and metadata. Exclude `.git`, `.venv`, caches, `__pycache__`, `.hypothesis`, and `Zone.Identifier` artifacts.
- Record a machine-readable `run.json` with model requested, model actually reported by the provider, harness, OS, cwd, isolation mode, skill-pack identity/hash, `AGENTS.md` hash, prompt, timestamps, and operator interventions.
- Normalize transcripts to one format or provide a small extractor so audit evidence does not depend on manually reading large HTML exports.
- Validate a wording patch with repeated trials. One post-patch rerun can be model variance; use at least two or three runs of the affected task on the same model/harness before claiming causality.

The model identifier should come from transcript/provider metadata, not a manually typed log row. This avoids the existing Haiku 4.5/4.6 mismatch and makes codenames such as `big-pickle` traceable to the response model when available.

## Lower-priority improvements

### Portable standalone scripts

Haiku T4 crashed on Unicode status characters under Windows cp1252. Add a small spike/CLI portability note:

```md
Standalone scripts and CLI diagnostics default to ASCII unless Unicode output is a requirement and encoding is controlled.
```

This is low priority because the model recovered and the behavior was not central to the test.

### Exact completion claim

Add a final AGENTS.md line:

```md
- Do not claim a change is complete until the required verify loop has finished successfully. In the final response, report the command run and whether it passed.
```

This will not make a weak skill-less model fully reliable, but it gives procedural skills a clear handoff gate and makes skipped verification easier to audit.

## Recommended implementation order

1. Fix the run protocol, metadata, copy exclusions, and rubric loopholes.
2. Apply the `AGENTS.md` pre-edit/valid-RED/coverage wording to both copies and add a sync check.
3. Update `tdd` and `diagnose` descriptions as a pair; add first-action and finish gates to `tdd`.
4. Add the requested-behavior phase to `py-new`.
5. Clarify spike deletion consistently across `AGENTS.md`, `diagnose`, T4, and examples/documentation.
6. Re-run T1, T2, and T3 in isolated, same-harness trials. T1 is necessary because the current review treats it as a clean control even though its RED/test-quality criteria are too weak.

## What I would not change

- Do not add more generic emphasis to the verify-loop command; it is already exact.
- Do not add a separate narrow rule for every observed missed assertion. Use one coverage-closure gate.
- Do not treat big-pickle T3 as proof that more AGENTS prose will solve instruction-following. Test the procedural skill changes in a skill-capable harness; retain the skill-less result as a model-selection signal.
- Do not merge cross-harness totals into a single leaderboard score.
