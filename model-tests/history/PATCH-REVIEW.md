# Patch Review — cross-model synthesis (pre-implementation)

Date: 2026-06-15. Author: Opus 4.8 (audit synthesis).
**Status: REVIEW GATE — nothing implemented. All patches HELD per Davis's standing decision.** Per-finding evidence: [FINDINGS.md](FINDINGS.md). Per-run scoring: `runs/<model>/<task>/AUDIT.md`.

## 1. Results across 3 models

| Task | haiku-4.5 (Claude Code) | deepseek-v4-flash-free (opencode) | big-pickle (opencode) |
|---|---|---|---|
| T1 — scaffold | 6/6 | 6/6 | 6/6 |
| T2 — feature TDD | **4/5** | **4/5** | **4/5** |
| T3 — bug fix | 5/5 | 5/5 | **2/5** |
| T4 — spike | 4/4 | 4/4 | 4/4 |
| **Total** | 19/20 | 19/20 | 16/20 |

Caveat (P4): haiku ran under Claude Code (skills available); deepseek + big-pickle ran under the opencode harness (4 tools, **no skill layer**, AGENTS.md injected). Cross-harness ⇒ the opencode runs are a robustness signal, not a controlled comparison with haiku.

## 2. The one universal failure: T2 / C1 (new-feature test-first)

All three models failed it — by **three different mechanisms**:

| Model | T2 C1 failure mode |
|---|---|
| haiku | Wrote **no** behavior test at all (the `tdd` skill never auto-triggered). |
| deepseek | Wrote **correct** capsys tests, but **after** the implementation (no RED). |
| big-pickle | Same as deepseek — recognized the feature, wrote good tests, but after impl. |

big-pickle additionally failed T3 (C1 + C3 + C5): fixed both comparisons correctly, but skipped test-first, kept no regression test (used a throwaway `python -c`), and never ran the verify loop.

## 3. The doc-fault vs model-fault split (the point of the campaign)

| Failure | Rule state | Verdict |
|---|---|---|
| deepseek/big-pickle T2 C1 | Feature bullet is **soft** ("write the failing test first, then implement" — no RED/No-exceptions emphasis) | **doc-fault → patchable** (F3/F4) |
| haiku T2 C1 | Skill didn't fire | **doc-fault → patchable in Claude Code only** (F2) |
| haiku/deepseek T3 `__len__` | Coverage gap — regression test pins only one changed path | **doc-fault → patchable** (F1) |
| big-pickle T3 collapse | Bug rule + verify-loop rule already **maximally explicit** ("No exceptions", exact command) | **model-fault → NOT patchable** (F5) |

Key tell: big-pickle followed the workflow perfectly on T1 — it even self-corrected a batch-write by recalling the AGENTS.md rule — because it read the `py-new` skill's procedure. On T3 there was no procedural skill to read, and the rule text alone didn't hold it. Capability is present; discipline-without-a-scaffold is the gap.

---

## 4. Proposed changes (exact)

### A. AGENTS.md rule patches — folds F3 + F4 + F1

Apply to **both** canonical copies: repo-root `AGENTS.md` and `skills/py-new/templates/AGENTS.md`.

**Workflow section. Before:**

```
- Behavior change or new feature: write the failing test first, then implement.
- Bug or regression: always reproduce with a failing test before fixing. No exceptions.
```

**After:**

```
- Behavior change or new feature (a new function, CLI flag, option, endpoint, or output format all count): write the failing test first and run it to see it fail (RED) before writing any implementation. No exceptions.
- Bug or regression: always reproduce with a failing test before fixing. No exceptions. The regression test must exercise every code path you change — if the fix touches multiple call sites, assert each.
```

- Feature-bullet parenthetical = **F3** (haiku failed to classify a flag-add as a feature). 2 occ.
- Feature-bullet RED clause = **F4** (deepseek + big-pickle wrote tests after impl). 2 occ.
- Bug-bullet final sentence = **F1** (haiku + deepseek pinned `get()` but not the co-fixed `__len__`). 2 occ.

All three are harness-independent and have ≥2 occurrences → strongest candidates.

### B. Spike bullet — DECISION REQUIRED (divergent behavior)

deepseek deleted its spike; big-pickle kept its spike. Same rule, opposite behavior, neither wrong under current wording → the rule is under-specified. Pick one:

```
# opt1 (keep — recommended): leave the throwaway as the record
- Exploratory spike or throwaway script: tests optional, never merge it. Name it `spike_*.py` with a `THROWAWAY` header stating the question probed; record the verdict, and leave the file in place as the record — don't delete it.

# opt2 (bless deletion): allow either
- Exploratory spike or throwaway script: tests optional, never merge it. Name it `spike_*.py` with a `THROWAWAY` header stating the question probed; record the verdict, then delete or keep it — either is fine.
```

Recommendation: **opt1 (keep)** — the repo already keeps `examples/spike_dedupe.py`, so persistence matches the project's own convention.

### C. tdd SKILL.md broadening (F2) — HOLD, cannot confirm yet

Broaden the `tdd` skill description so it auto-fires on any feature/flag/endpoint/behavior change, not only when the user names "TDD". This is **Claude-Code-only** — the opencode harness has no skills, so deepseek/big-pickle cannot test it. Needs a **Claude Code 2nd-model run** to confirm. This is a skill-file change (the category Davis deferred).

### D. Housekeeping (protocol)

- **P3** (trivial, safe now): `runs/log.md` records `claude-haiku-4.6`; transcripts say Haiku 4.5. Correct the rows to `claude-haiku-4.5`.
- **P4** (small): add a harness/isolation column to `runs/log.md` so opencode vs Claude Code runs are distinguishable.
- **P2** (at commit time only): run dirs carry nested `.git`, `.venv`, caches, and `Zone.Identifier` cruft. Strip before any `git add` (or `slugger/.git` becomes a gitlink and the source is lost). Update RUNBOOK robocopy: `/XD .venv .git .pytest_cache .ruff_cache .hypothesis __pycache__`.

### E. No patch — F5 (record only)

big-pickle T3 discipline collapse is model-fault: the bug rule and verify-loop command are already maximal. Recorded as a model-selection signal, no doc change.

---

## 5. Decisions needed from Davis

1. **Apply Patch A now?** (F3+F4+F1, both AGENTS.md copies.) Confirmed ≥2 occ each, harness-independent. Recommendation: **yes**.
2. **Spike rule: opt1 (keep) or opt2 (bless delete)?** Recommendation: **opt1**.
3. **F2 + the Claude Code run: keep HOLD** until a sonnet/haiku Claude Code run confirms the skill-trigger gap? Recommendation: **yes, hold**.
4. **P3 log typo + P4 harness column: do now?** Cheap, safe. Recommendation: **yes**.

## 6. Post-patch verification

After Patch A lands, re-run **T2** once (and **T3** for big-pickle) per RUNBOOK to confirm the wording change actually moves behavior. Patches go to both AGENTS.md copies; if F2 is later applied, also re-deploy `tdd` to `~/.claude/skills` + `claude-test-pack`.

**Nothing in this document has been applied. Awaiting review.**
