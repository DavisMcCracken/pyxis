# Product Requirements Document: agent-refinement / skills

Status: Working PRD
Owner: Davis McCracken
Last updated: 2026-06-22
Tracking issues: #4, #11, #17, #22

## 1. Summary

`agent-refinement/skills` is a docs-first workflow project for making Python-oriented AI coding agents more reliable. It provides:

- a canonical `AGENTS.md` Python project rule base,
- a deployable procedural skill pack under `skills/`,
- reference Python projects under `examples/`, and
- a model-test battery under `model-tests/` for validating whether agents actually follow the workflow.

The product is not an application or package today. The product is an operational workflow kit: rules, skills, examples, tests, and runbooks that help Davis build with AI while keeping main usable.

## 2. Current stable baseline

The repository is considered stable when all of the following are true:

- `main` is clean and matches `origin/main`.
- Root `AGENTS.md` and `skills/py-new/templates/AGENTS.md` are byte-identical.
- `model-tests/` verification passes.
- `examples/wordstats` verification passes.
- `examples/ttlcache` verification passes.
- Markdown links resolve.
- Bulky model-test run artifacts stay out of the repository path.

The current baseline is documented in [PROJECT-STATUS.md](PROJECT-STATUS.md).

## 3. Users and use cases

### Primary user: Davis

Davis uses this repo to:

- keep a reusable Python agent workflow rule base,
- deploy a matching skill pack into agent environments,
- test whether different models/harnesses follow the workflow,
- preserve evidence for rule/skill changes, and
- evolve the system safely through issues, branches, and PRs.

### Secondary user: AI coding agent

An agent working in this repo needs clear source-of-truth documents and small, reviewable tasks. It should not infer stale roadmap state from historical planning documents.

### Future user: another developer or future Davis

A future maintainer should be able to clone the repo, read the README and PRD, run verification, understand the current roadmap, and make changes through issues and PRs without needing chat history.

## 4. Product goals

1. Keep `main` always usable.
2. Make the workflow kit easy to understand from checked-in docs alone.
3. Make every change traceable from issue to branch to PR to verification result.
4. Validate rule/skill changes empirically before treating them as proven.
5. Preserve useful model-test evidence without committing bulky or contaminated artifacts.
6. Prefer small, boring, reversible improvements over broad rewrites.

## 5. Non-goals

For the current phase, this project will not:

- add new feature work before the validation baseline is complete,
- build a web app or service,
- package and publish a Python library,
- add a large orchestration framework for model tests,
- commit bulky transcripts or generated run directories,
- treat unvalidated prompt/rule changes as proven,
- bypass issue/branch/PR workflow for non-trivial changes.

## 6. Source-of-truth map

| Area | Source of truth |
|---|---|
| Stable baseline and current state | [PROJECT-STATUS.md](PROJECT-STATUS.md) |
| Product requirements and workflow policy | This PRD |
| Python project rules | [AGENTS.md](AGENTS.md) and `skills/py-new/templates/AGENTS.md` |
| Skill pack lifecycle and deployment | [skills/README.md](skills/README.md) |
| Model-test protocol | [model-tests/TESTING.md](model-tests/TESTING.md) |
| Model-test operator steps | [model-tests/RUNBOOK.md](model-tests/RUNBOOK.md) |
| Findings and validation state | [model-tests/FINDINGS.md](model-tests/FINDINGS.md) |
| Historical design rationale | `model-tests/REVISED-PLAN*.md`, `model-tests/PATCH-REVIEW.md`, `model-tests/INDEPENDENT-RECOMMENDATIONS.md` |
| Committed run index | [model-tests/RUNS-LOG.md](model-tests/RUNS-LOG.md) |

## 7. Active roadmap

### Phase 0 — Stable baseline

Status: complete.

Acceptance criteria:

- Branches cleaned up.
- Bulky historical runs archived out of repo path.
- Stable status documented.
- Full verification baseline passes.

### Phase 1 — Empirical validation

Status: in progress. Issues #6, #7, and #8 are complete; #9 validation performed (F1 rule-text patch insufficient); #19 pack-enabled T3 follow-up also negative; #10, #14, and F1 wording follow-up #22 remain open.

Goal: validate the already-implemented rule/skill changes before adding new features.

Required validation matrix:

| Target | Harness | Task | Trials | Proves |
|---|---|---|---:|---|
| AGENTS-only behavior | isolated skill-less | T2 | 2 | Operational test-first wording works without skills |
| `tdd` trigger/procedure | isolated pack-enabled | T2 | 2 | Feature prompt loads and follows `tdd` without unnecessary questions |
| `py-new` handoff | isolated pack-enabled | T1 | 2 | Scaffold completes requested behavior with valid RED |
| Regression closure | held-constant harness | T3 | 2 | Both changed observable operations receive retained coverage — **#9 validation (2026-06-21, bare/haiku): rule text alone did NOT achieve this; `get()` boundary guarded but `__len__()` unguarded in both trials. #19 validation (2026-06-22, pack/haiku): pack visibility also did NOT achieve this; same W2 failure in both trials. F1 wording follow-up #22 required.** |

If a pair splits 1-1, run a third trial before editing wording.

Acceptance criteria:

- F1-F4 in `model-tests/FINDINGS.md` are updated from `validation pending` to validated or follow-up required.
- Every new run has `run.json` provenance per `RUNBOOK.md`.
- `RUNS-LOG.md` records each run summary.
- Bulky run artifacts remain ignored or archived.

Tracking issues:

- #6 Validate AGENTS-only T2 behavior — complete.
- #7 Validate pack-enabled T2 `tdd` trigger/procedure — complete, with #14 follow-up for explicit skill-trigger evidence.
- #8 Validate pack-enabled T1 `py-new` handoff — complete.
- #9 Validate T3 regression closure — validation performed 2026-06-21 (held-constant bare, haiku); F1 rule-text patch insufficient: both trials fixed `get()`→`>=` and `__len__`→`<` but wrote a boundary test for `get()` only, leaving `__len__()` unguarded (audit probe: revert stays green).
- #19 Validate pack-enabled T3 F1 follow-up — validation performed 2026-06-22 (Claude Code print, pack, haiku); pack visibility did not close F1: both trials repeated the same W2 failure. Follow-up #22 tracks stronger explicit multi-operation rule wording and re-validation.
- #10 Summarize validation results and update ledgers.
- #14 Investigate Claude Code skill auto-trigger evidence for `tdd`.
- #22 Strengthen multi-operation rule wording and re-validate T3.

### Phase 2 — Workflow hardening

Status: proposed after Phase 1.

Potential work, only if supported by validation evidence:

- tighten any rule/skill wording that fails validation,
- add a small issue/PR template set if repeated PRs show missing information,
- add a lightweight validation checklist script for repository invariants,
- improve operator ergonomics in `RUNBOOK.md` without changing the test protocol,
- set up and document a clean OpenCode model-test harness in #17 after Phase 1 is summarized.

### Phase 3 — New features

Status: deferred.

New feature work may begin after Phase 1 validates the baseline or explicitly records why the baseline is good enough to proceed.

Potential feature categories:

- additional model-test tasks,
- richer run summaries,
- better skill deployment guidance,
- additional example projects,
- automation for non-interactive audit checks.

Each feature must start as a GitHub issue and move through the workflow below.

## 8. Issue → branch → PR workflow

All non-trivial work should follow this path.

### 8.1 Create or select an issue

An issue should include:

- problem / goal,
- scope,
- non-goals,
- acceptance criteria,
- verification commands,
- affected files or docs if known.

Use labels where helpful:

- `documentation`
- `validation`
- `workflow`
- `model-tests`
- `bug`
- `enhancement`

### 8.2 Create a branch from clean `main`

Before branching:

```bash
git checkout main
git pull --ff-only origin main
git status --short --branch
```

Branch naming:

- docs: `docs/issue-N-short-name`
- validation: `validation/issue-N-short-name`
- bug fix: `fix/issue-N-short-name`
- feature: `feat/issue-N-short-name`

### 8.3 Keep changes small

A PR should do one coherent thing. If a change needs multiple independent decisions, split it into multiple issues/PRs.

A good PR should include:

- linked issue: `Closes #N` or `Refs #N`,
- summary,
- validation commands and results,
- notes on any deferred work.

### 8.4 Verify before opening or merging

Run the relevant checks for changed areas. For broad repo changes, run the full baseline from `PROJECT-STATUS.md`.

Minimum documentation-only checks:

- Markdown link check or targeted link review.
- `git diff --check`.
- Relevant repository verification if docs describe behavior or commands.

Minimum code/test checks:

- affected project verify loop,
- affected tests,
- full baseline if shared rules, model-test harness, or templates changed.

### 8.5 Merge only from a reviewed PR

Do not commit directly to `main` except for emergency cleanup explicitly called out in chat.

Preferred merge style:

- squash merge,
- delete remote branch after merge,
- confirm local `main` is updated and clean.

After merge:

```bash
git checkout main
git pull --ff-only origin main
git status --short --branch
```

### 8.6 Development gates and worktrees

Before Phase 1 is complete, work should stay limited to validation, status-sync, and stabilization tasks.

After Phase 1, future development should follow this default operating model:

1. Create or select a GitHub issue with clear acceptance criteria.
2. Start from clean, current `main`.
3. Use an isolated branch or worktree per issue when parallel work would otherwise dirty the main checkout.
4. Keep each PR scoped to one issue or one coherent decision.
5. Merge only after review and relevant verification.

Recommended worktree pattern for parallel feature work:

```bash
git checkout main
git pull --ff-only origin main
git worktree add ../skills-issue-N -b feat/issue-N-short-name main
```

Remove the worktree after merge:

```bash
git worktree remove ../skills-issue-N
```

## 9. Stability requirements

A change is not ready if it:

- leaves `main` without a passing verification path,
- creates a second source of truth without marking one document historical,
- changes root `AGENTS.md` without syncing `skills/py-new/templates/AGENTS.md`,
- commits bulky run artifacts under `model-tests/runs/`,
- updates rules/skills without updating `FINDINGS.md` or validation state when relevant,
- adds feature work before Phase 1 validation without an explicit decision.

## 10. Open questions

1. Should GitHub issue templates be added now, or only after a few manual issues show a stable pattern?
2. Should validation runs be managed as GitHub issues, one issue per validation condition? Answered for Phase 1: yes, issues #6-#10 with follow-up issues for unresolved validation findings.
3. Should `PROJECT-STATUS.md` be updated after every merge, or only after stabilization milestones?
4. Should local archives under `/home/hermes/projects/archive/` eventually be copied to durable external storage?

## 11. Immediate next action

Finish the remaining Phase 1 validation work before any new feature work:

1. #9 and #19 validation are complete with negative results: both rule text alone and pack visibility were insufficient for F1 on T3. Resolve #22 by strengthening the F1 rule with an explicit multi-operation example and re-validating T3.
2. #10 Summarize Phase 1 validation results and update `FINDINGS.md` / `PROJECT-STATUS.md`.
3. #14 Resolve or precisely defer Claude Code `tdd` skill-trigger evidence.
4. #17 Set up and document a clean OpenCode model-test harness after Phase 1 is summarized.

Completed Phase 1 validation: #6, #7, #8, #9 (performed; negative), and #19 (performed; negative — F1 wording follow-up #22 required).
