# Revised Plan — synthesis of PATCH-REVIEW + INDEPENDENT-RECOMMENDATIONS

Date: 2026-06-15. Author: Opus 4.8.
Inputs: [PATCH-REVIEW.md](PATCH-REVIEW.md) (mine), [INDEPENDENT-RECOMMENDATIONS.md](INDEPENDENT-RECOMMENDATIONS.md) (independent), [FINDINGS.md](FINDINGS.md), the 12 per-run audits, and the actual `AGENTS.md` / `py-new` / `tdd` / `diagnose` sources.

**Status as of 2026-06-20: superseded / implemented.** This was the first synthesis plan. The implementation-ready revision is [REVISED-PLAN-SECOND-REVIEW.md](REVISED-PLAN-SECOND-REVIEW.md). The core patch landed in PR #1 / commit `08b5463`; the audit-provenance follow-up landed in PR #3 / commit `cbda9bd`. Treat this file as historical design rationale, not the current roadmap. Current remaining work is empirical validation of F1-F4 in [FINDINGS.md](FINDINGS.md) using [RUNBOOK.md](RUNBOOK.md).

## Design rule this plan is built on (Matt Pocock split)

From `skills/README.md`: **AGENTS.md = always-loaded constraints; skills = the procedural long form; no second source of truth.** Two consequences drive every choice below:

1. **AGENTS.md must be self-sufficient in a skill-less harness.** The opencode runs (deepseek, big-pickle) had *only* AGENTS.md — no `tdd`/`diagnose` to lean on. So the constraint each failure exposes must exist, tersely, in AGENTS.md.
2. **The procedure lives in the skill, stated once.** Valid-RED, the first-action gate, coverage-closure — the elaboration belongs in `tdd`, which already holds most of it. AGENTS.md references the constraint in one clause; it does not restate the procedure.

Net effect: AGENTS.md stays ~the same length (refined wording, +0 net bullets), and the skills carry the depth. Minimal, not maximal.

---

## Where the independent review changed my mind (concessions)

1. **Spike files: delete, not keep.** My PATCH-REVIEW recommended keeping spikes (opt1). That **contradicts `diagnose/SKILL.md:106`** ("`spike_*.py` never merges", harnesses deleted) and would push throwaway code toward commits. The checked-in `examples/spike_dedupe.py` is a *reference fixture*, not a lifecycle default. **Adopt deletion.** deepseek's delete was the aligned behaviour; the real gap is that AGENTS.md never stated the delete default that `diagnose` assumes.
2. **My single-total scorecard overstates compliance.** Several "passes" are vacuous (T2 C2 passes only because no tests were batched — but tests came after impl; big-pickle T3 C4 "passed" with no RED→GREEN loop at all). And T1 6/6 across the board credits an import/collection error as RED, which `tdd/SKILL.md` explicitly says is not RED. **Adopt 3-dimension scoring and de-vacuum the rubric** (below). Under the corrected rubric, **big-pickle T3 is 1/5, not 2/5** (C4 was a vacuous pass).
3. **Broadening `tdd` alone is wrong — change `tdd` and `diagnose` as a pair**, or they double-trigger on "reports a bug."

## Where I push back on the independent review (keep it minimal)

1. **Don't move the full valid-RED procedure into AGENTS.md.** The independent Priority-1 wording restates valid-RED and splits Workflow into "Existing codebase / New project" headers — that duplicates what `tdd` already owns and grows the always-loaded base. **AGENTS.md gets one clause** ("a collection or import error is not RED"); the full treatment stays in `tdd`.
2. **No mutation-testing step in the battery.** The lighter, objective **revert-each-changed-path-and-rerun** check (which the review also proposes for T3) is enough to catch coverage gaps. Full mutation tooling is over-engineering for a hand-run battery.
3. **Drop the ASCII/cp1252 portability rule from AGENTS.md.** A one-off Windows encoding hiccup the model recovered from doesn't earn a permanent always-loaded constraint. If wanted, it's a one-liner in `diagnose`'s spike note, not the base.

Everything else in the independent review I **adopt**: the pre-edit-gate *intent*, valid-RED, the `tdd`/`diagnose` pairing, the `py-new` finish-the-feature phase, spike deletion, rubric de-vacuuming, 3-dimension scoring, run isolation + metadata, and repeat-trials for causality.

---

## The revised patch set (exact)

### A. AGENTS.md `## Workflow` — both copies (root + `skills/py-new/templates/`)

Folds F3 (examples), F4 (RED-first, made operational as "don't edit first"), F1 (multi-path coverage), the scaffold-isn't-the-feature loophole, valid-RED (one clause), and spike-deletion. Same bullet count as today.

**Before:**
```
- Behavior change or new feature: write the failing test first, then implement.
- One test -> minimal implementation -> repeat. Don't batch-write all tests upfront — bulk tests encode imagined behavior, not actual behavior.
- Bug or regression: always reproduce with a failing test before fixing. No exceptions.
- Exploratory spike or throwaway script: tests optional, never merge it. Name it `spike_*.py` with a `THROWAWAY` header stating the question probed; record the verdict before moving on.
- Non-trivial design decision (new module, schema, public API, algorithm choice): state 2–3 candidate approaches with trade-offs, pick one, then implement. Skip for routine edits.
```

**After:**
```
- New behaviour or bug fix (a new function, CLI flag, option, endpoint, output format, or changed error all count): do not edit implementation first. Write one test, run it, and watch it fail with a real assertion error — a collection or import error is not RED — then implement. No exceptions. Scaffolding a new project isn't the feature: once the skeleton's verify loop is green, the requested behaviour still gets its own failing test (a smoke/import test doesn't count).
- One test -> minimal implementation -> repeat. Don't batch-write all tests upfront — bulk tests encode imagined behavior, not actual behavior.
- Bug or regression: keep the reproducing test in the suite. If the fix changes more than one code path or observable branch, assert each.
- Exploratory spike or throwaway script: tests optional, never merge it. Name it `spike_*.py` with a `THROWAWAY` header stating the question probed; run it, record the verdict, then delete it before handoff unless the user asks to keep it.
- Non-trivial design decision (new module, schema, public API, algorithm choice): state 2–3 candidate approaches with trade-offs, pick one, then implement. Skip for routine edits.
```

### B. AGENTS.md `## Tooling` — completion gate (one clause, optional but recommended)

Targets big-pickle T3 (claimed done without running the verify loop). Append to the existing verify-loop bullet:
```
… Don't report a change as done until this loop has passed; state the command run and its result.
```

### C. `tdd/SKILL.md` — proactive trigger + first-action gate + coverage gate

**Frontmatter description (was: gates on the user naming "TDD"):**
```yaml
description: Test-driven implementation of any new user-visible behaviour in an existing project — functions, CLI flags, options, endpoints, output formats, and ordinary reproducible bug fixes. Use proactively even when the user doesn't mention TDD or tests. Not for scaffolding-only work (see py-new) or hard/intermittent/unknown-cause diagnosis (see diagnose).
```

**Add near the top (before Philosophy) — the procedural gate weak models follow more reliably than prose:**
```md
## First action — before editing any production code

1. Name the public behaviour you're changing.
2. Write one test for it and run the narrowest command.
3. Confirm it failed on the assertion, not on a collection/import error (RED rule below).

Brand-new symbol: import the package and assert the symbol is exposed (`assert hasattr(pkg, "name")`), then drive its behaviour one test at a time — don't let the missing import stand in for RED.
```

**Add before the verify-loop step (coverage closure — the skill-side of F1):**
```md
Before the verify loop, check every production path you changed is exercised by a test assertion — including a change justified only "for consistency". Changed two call sites → assert both.
```

(Valid-RED itself is already in `tdd` at the tracer-bullet step and the checklist — not duplicated here.)

### D. `diagnose/SKILL.md` — tighten description to not collide with the broadened `tdd`

Aligns the description with the body's existing scope note (`:8`, "ordinary bug → AGENTS.md rule suffices"):
```yaml
description: Diagnosis loop for hard bugs — intermittent, cross-system, unknown-cause — and performance regressions. Use when no reliable repro exists yet or investigation/instrumentation is required. Not for an ordinary localized bug with an obvious failing test; use tdd.
```

### E. `py-new/SKILL.md` — finish the requested feature; stop relocating

Closes haiku T1 (shipped `slugify` with an existence smoke test only) and deepseek T1 (asked an unnecessary location question, built outside the run dir).

**New phase between `3. Verify` and `Hand over`:**
```md
## 4. Implement the requested behaviour

A green scaffold is not the deliverable if the request named behaviour (e.g. "converts titles to slugs"). Still required:

1. Add one real behaviour test and observe valid RED before implementing (follow `tdd`).
2. Implement one behaviour at a time; replace the generated smoke test once real coverage exists.
3. Re-run the full verify loop.

Don't hand over a requested feature covered only by an import/`hasattr`/callable test.
```

**Decision section — tighten:**
```md
- Name + kind already implied and no runtime dep mentioned → take defaults silently, don't ask.
- Create the project in the current directory unless the user names another location. Don't relocate it because the directory looks temporary or test-related.
```

### F. `TESTING.md` — de-vacuum the rubric (so totals mean something)

- **T1 C6 →** "a real behaviour test for the requested feature was written and observed failing **on a behavioural assertion** before implementation (import/collection error doesn't count)." Objective check: revert the core conversion → at least one test must fail.
- **T2 C2 →** N/A (not a pass) when C1 fails; a feature written impl-first can't earn "vertical slices."
- **T3 C4 →** N/A (not a pass) when no RED→GREEN loop occurred. Objective coverage check: revert each changed comparison independently → a regression test must fail for each.
- **Scoring → three dimensions, never one cross-harness total:** (1) functional result, (2) workflow compliance, (3) harness validity/isolation. A Claude Code skill-pack run and a skill-less opencode run don't share a leaderboard.

### G. RUNBOOK / protocol — make runs reproducible before validating any patch

- **Run every model outside the repo** (protocol §1 already says this; the opencode runs violated it — they read `.agents/skills`, other models' outputs, and `examples/`). Enforce.
- **Copy back source/tests/transcript/metadata only;** exclude `.git .venv .pytest_cache .ruff_cache .hypothesis __pycache__ *Zone.Identifier*` (this is P2; also kills the gitlink problem).
- **Write a `run.json` per run:** model requested, model the provider actually reported, harness, OS, cwd, isolation mode, skill-pack hash, AGENTS.md hash, prompt, timestamps, operator interventions. Model id comes from provider metadata, not a hand-typed log row (this is what produced the P3 haiku-4.6/4.5 typo and leaves `big-pickle` untraceable).
- **Normalize transcripts** or commit the base64→text extractor already used in these audits, so evidence doesn't depend on reading 350 KB HTML by hand.
- **Validate a wording patch with 2–3 trials**, same model+harness, before claiming causality — one post-patch rerun can be variance.

---

## What's safe now vs held

| Bucket | Items | Gate |
|---|---|---|
| **Safe now** (housekeeping, no behaviour risk) | P3 log id from metadata; P4 harness column; G copy-exclusions + `run.json` + extractor; TESTING.md rubric de-vacuum | none — these only improve the harness/record |
| **Held — rule text** (confirmed ≥2 occ, harness-independent) | A (AGENTS.md workflow), B (completion gate) | Davis lifts HOLD → apply to both copies → re-run T2/T3 ×2–3 |
| **Held — skills** (Davis deferred skill edits; needs a skill-capable harness to validate) | C (`tdd`), D (`diagnose`), E (`py-new`) | a Claude Code run confirms F2 trigger + the gates fire |

## Validation after applying A–E
Re-run **T1, T2, T3** in isolated, same-harness trials, 2–3× each. T1 is included deliberately — under the de-vacuumed rubric it's no longer a clean control. Confirm: feature tests go RED on a real assertion before impl; `__len__`-class second paths get asserted; spikes deleted; scaffold tasks finish the feature.

## Decisions for Davis
1. **Apply bucket "Safe now" immediately?** (rubric + protocol + metadata; no skill/AGENTS edits.) Rec: **yes** — it makes every future run trustworthy and is the precondition for validating anything else.
2. **Lift HOLD on bucket "rule text" (A+B)?** Confirmed across 3 models, harness-independent. Rec: **yes**, then validate with trials.
3. **Spike default = delete** (concession; aligns AGENTS.md with `diagnose`). Confirm.
4. **Skills (C/D/E): apply now, or wait for one Claude Code run?** Rec: apply alongside A given they're internally consistent and low-risk, but a Claude Code trial is what actually proves F2.

**Nothing here is applied. Awaiting your call.**
