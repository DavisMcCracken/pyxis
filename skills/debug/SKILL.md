---
name: debug
description: Diagnoses hard or uncertain bugs by building a feedback loop, reproducing, hypothesizing, instrumenting, fixing, and regression-testing. Use when reproduction or cause is unclear, the failure is intermittent or cross-system, or performance regressed.
---

# Debug

Discipline for hard bugs. Skip a phase only with stated justification. Ordinary bug with an obvious repro? The AGENTS.md rule (failing test, then fix) suffices — this skill is the escalation path.

Before exploring, load the project's domain glossary (`CONTEXT.md`, if present) and check ADRs near the affected area.

## Phase 1 — Build a feedback loop

**This phase IS the skill.** A fast, deterministic, agent-runnable pass/fail signal makes the rest mechanical — bisection, hypothesis tests, and instrumentation all just consume it. Without one, staring at code is all you have.

Spend disproportionate effort here. Be aggressive, be creative, refuse to give up.

### Construction options, roughly in order

1. **Failing test** at whatever seam reaches the bug — unit, integration, e2e.
2. **HTTP script** (curl etc.) against a running dev server.
3. **CLI run** on a fixture input, output diffed against a known-good snapshot.
4. **Headless browser script** (Playwright) asserting on DOM/console/network.
5. **Trace replay** — capture a real request/payload/event log, replay it through the code path in isolation.
6. **Throwaway harness** — minimal slice of the system (one service, faked deps) hitting the bug path in a single call. Follows the AGENTS.md spike convention: `spike_*.py`, `THROWAWAY` header, PEP 723 deps if standalone.
7. **Property/fuzz loop** — for "sometimes wrong output", randomized inputs hunting the failure; `hypothesis` with its saved failing example beats a hand-rolled loop.
8. **Bisection harness** — bug appeared between two known states? Automate "boot at X, check" so `git bisect run` can drive it.
9. **Differential loop** — same input through old vs new version (or two configs), diff the outputs.
10. **HITL script** — last resort when a human must click. Drive *them* with `scripts/hitl-loop.template.sh` so even manual steps feed structured output back.

### Then improve the loop itself

Treat it as a product:

- **Faster** — cache setup, skip unrelated init, narrow scope (`uv run pytest --last-failed -x` for test-shaped loops).
- **Sharper** — assert the exact symptom, not "didn't crash".
- **More deterministic** — inject the clock, seed RNG, isolate filesystem via `tmp_path`, freeze network.

A 30-second flaky loop barely beats none. A 2-second deterministic loop is a superpower.

### Non-deterministic bugs

Chase reproduction *rate*, not perfection: loop the trigger 100×, parallelise, add stress, squeeze timing windows. 50% flake is debuggable; 1% is not. Raise the rate until it is.

### Genuinely can't build one?

Say so explicitly, list what you tried, and ask the user for: (a) access to a reproducing environment, (b) a captured artifact (HAR, log dump, core dump, timestamped recording), or (c) permission for temporary production instrumentation. Never hypothesise loopless.

**Gate: no loop you believe in → no Phase 2.**

## Phase 2 — Reproduce

Run the loop; watch the bug happen. Confirm:

- [ ] It's the failure the **user** described, not a nearby lookalike — wrong bug = wrong fix
- [ ] Reproducible across runs (or at a rate high enough to debug)
- [ ] Exact symptom captured (message, wrong value, timing) so the fix can be verified against it

**Gate: not reproduced → not diagnosed.**

## Phase 3 — Hypothesise

Write **3–5 ranked hypotheses** before testing any — a single hypothesis anchors you to the first plausible story.

Each must be falsifiable, with its prediction stated:

> "If <X> is the cause, then <changing Y> makes the bug vanish / <changing Z> makes it worse."

No prediction = vibe. Sharpen or discard.

Show the ranked list to the user before probing — they often re-rank instantly ("we deployed #3's area yesterday") or kill hypotheses they've already ruled out. Don't block on a reply; proceed with your ranking if they're AFK.

## Phase 4 — Instrument

Every probe maps to one Phase 3 prediction. **One variable at a time.**

1. **Debugger / REPL** first where the env allows — one breakpoint beats ten logs.
2. **Targeted logs** at the seams that distinguish hypotheses.
3. Never "log everything and grep".

Tag every debug log with a unique prefix (`[DEBUG-a4f2]`) — cleanup becomes one grep. Untagged logs outlive the bug.

**Performance regressions:** logs lie about time. Baseline first (timing harness, profiler, query plan), then bisect. Measure, then fix.

## Phase 5 — Fix + regression test

Regression test **before** the fix — the AGENTS.md bug rule — but only at a **correct seam**: one where the test exercises the real bug pattern as it occurred at the call site. A too-shallow seam (single-caller unit test for a multi-caller interaction bug) gives false confidence.

**No correct seam? That IS a finding.** Document it — the architecture is blocking the bug from being locked down — and flag it for Phase 6.

With a correct seam:

1. Minimised repro → failing test at that seam
2. Watch it fail
3. Apply the fix
4. Watch it pass (`uv run pytest --last-failed -x` while iterating)
5. Re-run the Phase 1 loop on the original, un-minimised scenario

## Phase 6 — Cleanup + post-mortem

Done means:

- [ ] Original repro dead (Phase 1 loop re-run)
- [ ] Regression test green — or the missing seam documented
- [ ] All `[DEBUG-...]` instrumentation gone (grep the prefix)
- [ ] Throwaway harnesses deleted — `spike_*.py` never merges
- [ ] Full verify loop green (`uv run ruff check --fix && uv run ruff format && uv run ty check && uv run pytest`)
- [ ] Winning hypothesis stated in the commit/PR message — the next debugger learns

Last question: **what would have prevented this?** If the answer is architectural (no test seam, tangled callers, hidden coupling), hand the specifics to `refactor` — after the fix lands, not before. You know more now.
