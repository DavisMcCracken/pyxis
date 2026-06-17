# Second review of REVISED-PLAN.md - implementation-ready revision

Date: 2026-06-15.

Scope: reviewed `REVISED-PLAN.md` against the model-test evidence, current `AGENTS.md`, `py-new`, `tdd`, `diagnose`, `skills/README.md`, and Matt Pocock's current source material for the same skills.

This is a proposal only. It does not apply the patch.

## Verdict

`REVISED-PLAN.md` is directionally correct and close to implementation. I would implement one coherent patch covering the rule base, skill routing, skill procedures, and test harness. I would not split it into a long series of pre-validation holds: the current failures already justify the change, and the relevant question is whether the combined patch improves behavior.

The plan still needs several reductions and corrections before implementation:

1. Its proposed first `AGENTS.md` bullet is too long and carries too many decisions.
2. "Assertion failure only" is too rigid; the real requirement is that the intended test collects, executes, and fails for the missing behavior.
3. The proposed `hasattr` first cycle encourages interface-shape tests, the same weak testing pattern seen in Haiku T1.
4. "Test every production path changed" is implementation-coupled. Require coverage of changed observable behavior instead.
5. Broadening `tdd` without reducing its mandatory user-confirmation language will cause unnecessary questions on clear tasks.
6. Three scored dimensions are unnecessary. Use two scores plus a run-validity label.
7. The fixture setup must always overlay the canonical current `AGENTS.md`; otherwise post-patch runs may still test stale fixture copies.

## Design principles

The implementation should preserve four principles from Matt Pocock's skills:

- Skills stay small, adaptable, and composable rather than owning the entire development process.
- Reliable engineering comes from short, deliberate feedback loops and vertical RED-GREEN slices.
- Skill descriptions contain specific positive triggers because the description is what the agent sees when choosing a skill.
- Progressive disclosure keeps `SKILL.md` concise; repeated or advanced detail belongs in supporting files.

Local translation:

- `AGENTS.md` contains short harness-independent constraints.
- Skills contain the procedure that helps a weaker model obey those constraints.
- A rule is stated once at each layer: terse constraint in `AGENTS.md`, operational sequence in the relevant skill.
- Do not add prose solely to address a single harmless incident or a model that ignored an already-explicit command.

Primary sources:

- [Matt Pocock skills README](https://github.com/mattpocock/skills)
- [Matt Pocock TDD skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md)
- [Matt Pocock diagnose skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/diagnose/SKILL.md)
- [Matt Pocock write-a-skill guidance](https://github.com/mattpocock/skills/blob/main/skills/productivity/write-a-skill/SKILL.md)

## Decisions on REVISED-PLAN.md

### Adopt

- Make test-first operational in `AGENTS.md`, including examples of behavior changes.
- State that scaffold completion does not replace testing requested product behavior.
- Keep regression tests and cover every intentionally changed observable behavior.
- Broaden `tdd` and narrow `diagnose` together.
- Make `py-new` finish requested product behavior before handoff.
- Delete throwaway spikes before handoff unless the user asks to retain them.
- Repair vacuous rubric passes and isolate future runs.
- Record requested and provider-reported model identities.
- Validate behavior changes with repeated same-condition trials.

### Modify

- Replace one overloaded workflow bullet with short imperative bullets.
- Define valid RED by test execution and relevance, not only by `AssertionError`.
- Update existing `tdd` sections instead of appending a new large first-action section; `tdd/SKILL.md` is already 95 lines and Matt's guidance favors a concise main file.
- Use positive, mutually exclusive skill triggers instead of long negative exclusions.
- Score functional outcome and workflow compliance separately; attach harness validity as metadata, not a third score.
- Use two validation trials first, with a third only when results split.

### Reject

- Reject `assert hasattr(pkg, "name")` as the prescribed first feature test. It tests interface shape, not requested behavior.
- Reject a permanent ASCII/cp1252 rule from `AGENTS.md`; the single spike recovered without help.
- Reject a new requirement to repeat the verify command in the final response. The exact command already exists; make "before handoff" explicit without adding reporting ceremony.
- Reject tests for internal paths solely because the implementation touched them.
- Reject `N/A` for dependent process checks when it can inflate a ratio. If no valid RED-GREEN slice occurred, the slice criterion fails.

## Final patch

### 1. AGENTS.md workflow

Apply the following to root `AGENTS.md` and `skills/py-new/templates/AGENTS.md`:

```md
## Workflow

- Behavior change or bug fix (including a new function, CLI flag, option, endpoint, output format, or error behavior): before editing production code, write one test and run it. RED means the intended test collected and executed, then failed for the missing or incorrect behavior; import, collection, syntax, fixture, and unrelated setup failures do not count. No exceptions.
- A new-project scaffold may reach green first, but requested product behavior still follows the rule above. A smoke, import, `hasattr`, or callability test does not count as behavior coverage.
- One test -> minimal implementation -> repeat. Don't batch-write all tests upfront - bulk tests encode imagined behavior, not actual behavior.
- Bug or regression: keep the reproducing test. If the fix intentionally changes multiple public operations or observable branches, assert each; do not test internal paths merely because they were edited.
- Exploratory spike or throwaway script: tests optional, never merge it. Name it `spike_*.py` with a `THROWAWAY` header stating the question; run it, record the verdict, then delete it before handoff unless the user asks to keep it.
- Non-trivial design decision (new module, schema, public API, algorithm choice): state 2-3 candidate approaches with trade-offs, pick one, then implement. Skip for routine edits.
```

This is one bullet longer than the current section, but each gate is independently scannable. Preserving bullet count is less important than avoiding one paragraph-sized instruction.

Change the verify-loop lead-in, without adding a new reporting rule:

```md
- After each change set and before handoff, run the verify loop (lint-fix before format - fixes can produce unformatted code):
```

### 2. tdd skill routing

Use a two-sentence positive description:

```yaml
description: Builds features and fixes straightforward reproducible bugs one vertical red-green-refactor slice at a time. Use when implementing or changing user-visible behavior in an existing codebase, including functions, CLI flags, endpoints, output formats, and ordinary bug fixes.
```

This is broad enough to trigger on T2 and ordinary T3-style bugs while leaving uncertain debugging to `diagnose` and initial scaffolding to `py-new`.

### 3. tdd procedure

Do not append the proposed standalone first-action section. Edit the existing workflow instead.

Replace the interactive planning bullets with:

```md
Before writing code, infer the public interface and highest-priority behavior from the request, existing code, glossary, and ADRs. Ask the user only when a material ambiguity remains; otherwise state any assumption briefly and proceed. List behaviors, not implementation steps.
```

This matters because proactive triggering otherwise turns every clear feature request into an unnecessary interview. `grill-me` remains the deliberate tool for unresolved design.

Strengthen the tracer-bullet section:

```md
Before editing production code, write ONE test for ONE observable behavior and run the narrowest useful command.

Valid RED means the intended test was collected and executed, and the failure points to the missing or incorrect behavior. Collection, import, syntax, fixture, and unrelated setup failures mean the test is broken, not RED.
```

This intentionally allows a new API test to fail during execution because the behavior does not yet exist. It does not require a contrived `hasattr` cycle and does not accept an import-time collection error.

Add one completion sentence before the full verify loop:

```md
Before the full verify loop, confirm tests cover every public operation or observable branch intentionally changed. Do not add tests for internal paths solely because they were edited.
```

Update the checklist's RED item to match. Compress nearby prose as needed to keep `tdd/SKILL.md` around its current length rather than growing beyond 100 lines.

### 4. diagnose routing

Use a positive description with no overlap:

```yaml
description: Diagnoses hard or uncertain bugs by building a feedback loop, reproducing, hypothesizing, instrumenting, fixing, and regression-testing. Use when reproduction or cause is unclear, the failure is intermittent or cross-system, or performance regressed.
```

The body already says ordinary reproducible bugs do not need the full diagnosis procedure. Keep that scope note.

### 5. py-new behavior handoff

Tighten decision handling rather than adding more questions:

```md
Infer answered decisions from the request. If name and kind are clear and no runtime dependency is mentioned, use no runtime dependencies and proceed without confirmation. Use the current working directory as the project parent unless the user specifies another location or that would overwrite an existing project.
```

Add a short phase after the scaffold's first green verify loop:

```md
## 4. Implement requested behavior

If the request includes product behavior, a green scaffold is not done:

1. Continue with the `tdd` tracer-bullet loop: one behavior test, valid RED, minimal implementation.
2. Replace the generated smoke test once real behavior coverage exists.
3. Run the full verify loop again.

Do not hand over requested behavior covered only by an import, `hasattr`, or callability test.
```

Renumber handoff to step 5 and remove "start the first feature" from next steps because the named feature must already be complete.

### 6. skills README consistency

Update `skills/README.md` in the same changeset:

- `py-new` is no longer "copied unchanged."
- Describe valid RED as an intended test that collected/executed and failed for the target behavior, not strictly an assertion failure.
- Keep the existing lifecycle and cross-skill handoff map.

### 7. Canonical AGENTS injection

Do not maintain separate rule snapshots manually in every fixture.

After preparing any T1-T4 workspace, the RUNBOOK should copy the canonical `skills/py-new/templates/AGENTS.md` into the run root and write `CLAUDE.md` as appropriate for the harness. T2/T3 fixture contents may remain stable, but their rules are overlaid at run time.

This ensures every validation run actually tests the patch under review.

### 8. Rubric corrections

Use explicit failures rather than vacuous passes or ratio-friendly `N/A` results:

- **T1 behavior check:** the requested conversion behavior was tested before implementation; the intended test collected and executed. Audit probe: reverting the core conversion makes at least one behavior test fail.
- **T2 slice check:** at least one complete one-test RED-GREEN slice occurred before later tests or implementation. Implementation-first and batch-tests-first both fail.
- **T3 loop check:** a valid repro test preceded the fix and drove a narrow RED-GREEN iteration. Without valid RED, the loop check fails.
- **T3 coverage check:** revert each independently changed observable behavior; a retained regression test must fail for each.

Report:

1. **Functional score** - requested behavior and final correctness.
2. **Workflow score** - test order, slice discipline, retained coverage, verify loop.
3. **Run validity label** - `valid`, `cross-harness`, or `contaminated`, with reason.

Do not merge scores across validity labels or harness types.

### 9. Protocol and metadata

Implement the smallest repeatable harness improvement:

- Run outside the repository.
- Copy back source, tests, transcript, audit, and `run.json`; exclude `.git`, environments, caches, bytecode, Hypothesis state, and Zone Identifier files.
- Store in `run.json`: requested model, provider-reported model, harness, run cwd, isolation/skill-pack mode, AGENTS hash, prompt, timestamps, and operator interventions.
- Add one small deterministic transcript-extraction script for the opencode HTML format. This is justified because the same conversion has already been repeated across eight transcripts.

Do not add a larger orchestration framework yet.

## Implementation order

Implement as one reviewable patch in this order:

1. Correct `TESTING.md` and `RUNBOOK.md`, including canonical AGENTS overlay and minimal `run.json`.
2. Edit canonical `skills/py-new/templates/AGENTS.md`, then copy it exactly to root `AGENTS.md`.
3. Edit `tdd`, `diagnose`, and `py-new`; update `skills/README.md`.
4. Add the transcript extractor and verify it against one DeepSeek and one big-pickle transcript.
5. Deploy the updated pack to the isolated test configuration.
6. Run the validation matrix below.

No additional pre-patch model run is needed. The old configuration's failure modes are already established.

## Minimal validation matrix

Start with two identical trials per condition; run a third only if the pair splits.

| Target | Harness | Task | Proves |
|---|---|---|---|
| AGENTS-only behavior | isolated skill-less | T2 x2 | operational test-first wording works without skills |
| tdd trigger/procedure | isolated pack-enabled | T2 x2 | feature prompt loads and follows `tdd` without unnecessary questions |
| py-new handoff | isolated pack-enabled | T1 x2 | scaffold completes requested behavior with valid RED |
| regression closure | isolated pack-enabled or bare, held constant | T3 x2 | both changed observable operations receive retained coverage |

T4 does not need immediate reruns unless the spike lifecycle wording changes again; delete-after-verdict is already represented by a successful run.

## Acceptance criteria

The patch is ready to keep when:

- T2 no longer goes implementation-first in both AGENTS-only trials.
- Pack-enabled T2 triggers the intended skill and does not ask questions already answered by the prompt/code.
- T1 includes a real conversion test that collects and executes before implementation.
- T3 retains tests for every intentionally changed public operation or observable branch.
- Every valid run completes the verify loop.
- No run can read this repository, reference solutions, other model outputs, or undeclared skills.

If a condition splits 1-1, run the third trial before revising prose. If it fails 0-2, inspect the transcript and make one targeted change; do not add broad emphasis everywhere.

## Final recommendation

Proceed to implementation with the patch above. The remaining risk is empirical, not conceptual. The best next move is a compact coherent edit followed by controlled trials, not another round of expanding the documents.
