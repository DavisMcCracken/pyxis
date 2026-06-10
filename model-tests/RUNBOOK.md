# Test Runbook — follow per run

Operator checklist. One run = one model × one task. Rubric and scoring live in [TESTING.md](TESTING.md); this file is just the actions.

## Once, before the first run ever

- [x] Skill pack deployed to `~\.claude\skills\` (done 2026-06-10)
- [x] `New-Item -ItemType Directory -Force C:\Users\Davis\model-test-runs | Out-Null`

## Per run

### 1. Prepare the workspace

Pick `<model>` (start: `haiku`) and `<task>` (order: t3, t1, t2, t4). Then ONE of:

**t1 or t4** (clean dir + rules):

```powershell
$run = "C:\Users\Davis\model-test-runs\<model>\<task>"
New-Item -ItemType Directory -Force $run | Out-Null
Copy-Item C:\Users\Davis\Documents\agent-refinement\skills\py-new\templates\AGENTS.md $run
Set-Content "$run\CLAUDE.md" "@AGENTS.md"
```

**t2**:

```powershell
robocopy C:\Users\Davis\Documents\agent-refinement\model-tests\fixtures\wordstats-baseline C:\Users\Davis\model-test-runs\<model>\t2 /E /XD .venv
```

**t3**:

```powershell
robocopy C:\Users\Davis\Documents\agent-refinement\model-tests\fixtures\ttlcache-buggy C:\Users\Davis\model-test-runs\<model>\t3 /E /XD .venv
```

### 2. Launch

```powershell
cd C:\Users\Davis\model-test-runs\<model>\<task>
claude --model <model>
```

### 3. Paste the task prompt — exactly this, nothing else

- **t1**: `Create a new Python library called slugger that converts titles into URL slugs. Set the project up properly and implement the basic conversion.`
- **t2**: `Add a --json flag to the wordstats CLI. With --json, print a single JSON object {"words": N, "top": [["word", count], ...]} to stdout instead of the text format. Diagnostics must stay off stdout.`
- **t3**: `Bug report: a key set with ttl=10 is still returned by get() at exactly 10 seconds after set(). The spec says an entry is expired once its age >= ttl. Find and fix it.`
- **t4**: `Quickly explore whether stdlib difflib.SequenceMatcher is good enough to flag near-duplicate changelog lines, or whether we'd need rapidfuzz. Throwaway exploration — just give me a verdict.`

### 4. During the run — hands off

- Approve permission prompts. That is your ONLY input.
- Model asks you anything → reply exactly: `use your judgment` (then note that it asked).
- Never run commands yourself, never hint, never correct.

### 5. End the run

1. Model declares done → type `/export`, save as `transcript.md` in the run dir.
2. Exit the session.
3. Copy results back for audit:

```powershell
robocopy C:\Users\Davis\model-test-runs\<model>\<task> C:\Users\Davis\Documents\agent-refinement\model-tests\runs\<model>\<task> /E /XD .venv
```

### 6. Log it

Append one line to `runs/log.md` (create on first run): `<date> <model> <task> — done; asked questions: y/n; anything odd you noticed`.

## After a model finishes all four tasks

Open a session with the strong model in `C:\Users\Davis\Documents\agent-refinement` and say:

> Audit model-tests/runs/<model>/ against the TESTING.md rubric. Score each task, fill the scorecard, and classify every failed critical as doc-fault (AGENTS.md/skill wording could have prevented it — propose the patch) or model-fault.

Patches that come out of the audit go to BOTH `AGENTS.md` copies (root + `skills/py-new/templates/`) — then re-run the failed task once to confirm the patch lands.
