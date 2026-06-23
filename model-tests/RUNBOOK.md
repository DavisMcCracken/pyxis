# Test Runbook

One run = one model x one task. Rubric and scoring live in [TESTING.md](TESTING.md).

## Once

- [x] `C:\Users\Davis\model-test-runs` exists.
- [x] Isolated configs exist: `claude-test-pack` (pack only) and `claude-test-bare` (rules only).
- [ ] After any skill edit, redeploy `skills/` into `claude-test-pack\skills\` before testing.
- [ ] Confirm the chosen run directory does not already exist. Never reuse a dirty run directory.
- [ ] Confirm `run.json` will record the repo commit, AGENTS hash, skill-tree hash, and config directory used for this run.

## 1. Prepare

Set the variables for one run:

```powershell
$repo = "C:\Users\Davis\Documents\agent-refinement"
$model = "<model>"
$task = "<t1|t2|t3|t4>"
$trial = "trial-1"
$harness = "claude-code"
$isolation = "pack" # or bare / crowded
$claudeConfigDir = "C:\Users\Davis\claude-test-pack" # bare: claude-test-bare; crowded: $null
$run = "C:\Users\Davis\model-test-runs\$model\$task\$trial"

if (Test-Path $run) { throw "Run directory already exists: $run" }
New-Item -ItemType Directory -Force $run | Out-Null
```

Define a deterministic content hash for the deployed local skill tree:

```powershell
function Get-DirectoryContentSha256 {
  param([Parameter(Mandatory)][string]$Path)

  $root = (Resolve-Path $Path).Path
  $lines = Get-ChildItem $root -Recurse -File |
    Sort-Object FullName |
    ForEach-Object {
      $relative = $_.FullName.Substring($root.Length + 1).Replace('\', '/')
      $hash = (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower()
      "$relative $hash"
    }
  $bytes = [System.Text.Encoding]::UTF8.GetBytes(($lines -join "`n"))
  $sha = [System.Security.Cryptography.SHA256]::Create()
  [System.BitConverter]::ToString($sha.ComputeHash($bytes)).Replace("-", "").ToLower()
}
```

Choose the skill tree that the harness will actually see:

```powershell
$skillsHashRoot = if ($null -ne $claudeConfigDir -and (Test-Path "$claudeConfigDir\skills")) {
  "$claudeConfigDir\skills"
} else {
  "$repo\skills"
}
```

Copy the fixture when needed:

```powershell
if ($task -eq "t2") {
  robocopy "$repo\model-tests\fixtures\wordstats-baseline" $run /E `
    /XD .venv .git .pytest_cache .ruff_cache .hypothesis __pycache__ `
    /XF "*Zone.Identifier*"
}
if ($task -eq "t3") {
  robocopy "$repo\model-tests\fixtures\ttlcache-buggy" $run /E `
    /XD .venv .git .pytest_cache .ruff_cache .hypothesis __pycache__ `
    /XF "*Zone.Identifier*"
}
```

Always overlay the current canonical rules after fixture preparation:

```powershell
Copy-Item "$repo\skills\py-new\templates\AGENTS.md" "$run\AGENTS.md" -Force
Set-Content "$run\CLAUDE.md" "@AGENTS.md"
```

Select the exact prompt:

```powershell
$prompt = switch ($task) {
  "t1" { "Create a new Python library called slugger that converts titles into URL slugs. Set the project up properly and implement the basic conversion." }
  "t2" { 'Add a --json flag to the wordstats CLI. With --json, print a single JSON object {"words": N, "top": [["word", count], ...]} to stdout instead of the text format. Diagnostics must stay off stdout.' }
  "t3" { "Bug report: a key set with ttl=10 is still returned by get() at exactly 10 seconds after set(). The spec says an entry is expired once its age >= ttl. Find and fix it." }
  "t4" { "Quickly explore whether stdlib difflib.SequenceMatcher is good enough to flag near-duplicate changelog lines, or whether we'd need rapidfuzz. Throwaway exploration - just give me a verdict." }
}
```

Create `run.json` before launch:

```powershell
$metadata = [ordered]@{
  schema_version = 1
  task = $task
  trial = $trial
  requested_model = $model
  provider_reported_model = $null
  harness = $harness
  run_cwd = $run
  isolation_mode = $isolation
  claude_config_dir = $claudeConfigDir
  repo_commit = (git -C $repo rev-parse HEAD).Trim()
  agents_sha256 = (Get-FileHash "$run\AGENTS.md" -Algorithm SHA256).Hash.ToLower()
  skills_hash_root = $skillsHashRoot
  skills_tree_sha256 = Get-DirectoryContentSha256 $skillsHashRoot
  prompt = $prompt
  started_at = (Get-Date).ToUniversalTime().ToString("o")
  finished_at = $null
  operator_interventions = @()
}
$metadata | ConvertTo-Json -Depth 4 | Set-Content "$run\run.json"
```

## 2. Launch

Pack-enabled Phase 1:

```powershell
if ($null -eq $claudeConfigDir) {
  Remove-Item Env:\CLAUDE_CONFIG_DIR -ErrorAction SilentlyContinue
} else {
  $env:CLAUDE_CONFIG_DIR = $claudeConfigDir
}
Set-Location $run
claude --model $model
```

Use `claude-test-bare` for AGENTS-only trials. Crowded-environment trials omit `CLAUDE_CONFIG_DIR` and must be labeled separately.

## 3. Run Hands-Off

- Paste `$prompt` exactly.
- Approve permission prompts only.
- If the model asks anything, reply exactly `use your judgment` and record the question in `operator_interventions`.
- Do not run commands, hint, correct, or coach.

## 4. Finish and Export

1. When the model declares done, export the transcript into the run directory.
2. Exit the session.
3. Update `run.json` with the provider-reported model, finish time, and operator interventions.
4. For opencode HTML exports, generate the audit view:

```powershell
Set-Location $repo
uv run model-tests\scripts\extract_opencode_transcript.py `
  "$run\transcript.html" --output "$run\transcript.md"
```

The extractor intentionally omits hidden reasoning and preserves user text, assistant text, tool calls, and tool results.

### Claude Code skill invocation evidence

For stream-json transcripts, count a Claude Code skill as invoked only when the transcript contains an assistant `tool_use` event with `name: "Skill"` and `input.skill` equal to the expected skill name. The following `tool_result` usually says `Launching skill: <name>`, and Claude injects a synthetic user message containing the skill body.

The `init` event's `skills` and `slash_commands` fields prove only that a skill was available. They do not prove auto-trigger or procedure use. Behavior that matches a skill also does not prove invocation without the `Skill` tool-use event.

## 5. Copy Back

```powershell
$destination = "$repo\model-tests\runs\$model\$task\$trial"
robocopy $run $destination /E `
  /XD .venv .git .pytest_cache .ruff_cache .hypothesis __pycache__ `
  /XF "*.pyc" "*Zone.Identifier*"
```

Copy back source, tests, transcript, audit artifacts, and `run.json` only. The model must never run inside this repository.

## 6. Log and Audit

Append a row to [RUNS-LOG.md](RUNS-LOG.md) with date, requested model, provider-reported model, harness, isolation, task, trial, questions, validity, and notes. Keep the central log outside `runs/`; `runs/` is ignored so bulky transcripts and generated projects do not enter the repository.

Audit prompt:

> Audit `model-tests/runs/<model>/` against `TESTING.md`. Report functional score, workflow score, and run validity for each task. For each failed workflow check, classify it as a rule/skill gap or a model capability limit, with evidence from the transcript. Update each task's `AUDIT.md` and the findings ledger.

After a patch, run `trial-1` and `trial-2` under identical conditions. If they split 1-1, run `trial-3` before changing wording again.

## 7. OpenCode clean harness

OpenCode runs must follow the same isolation rule as Claude Code: run outside this repository, copy only the task fixture into a fresh run directory, overlay the current canonical `AGENTS.md`, record `run.json` before launch, and keep bulky artifacts out of git.

Host baseline verified 2026-06-23:

```bash
which -a opencode     # /usr/local/bin/opencode
opencode --version   # 1.17.9
opencode auth list   # may show 0 local credentials; smoke test is the real non-interactive auth check
```

Available model aliases at setup time:

```text
opencode/big-pickle
opencode/deepseek-v4-flash-free
opencode/mimo-v2.5-free
opencode/nemotron-3-ultra-free
opencode/north-mini-code-free
```

Smoke test outside the repo:

```bash
mkdir -p /home/hermes/model-test-runs/opencode-smoke
cd /home/hermes/model-test-runs/opencode-smoke
opencode run 'Respond with exactly: OPENCODE_SMOKE_OK'
opencode run --format json 'Respond with exactly: OPENCODE_SMOKE_OK' > opencode-smoke.jsonl
```

Expected plain output includes `OPENCODE_SMOKE_OK`; JSON output is newline-delimited events (`step_start`, `text`, `step_finish`) with `sessionID`, token counts, and cost. Capture both stdout/stderr or use `--format json` for transcript evidence.

Recommended calibrated run command shape, after preparing the run directory and writing `run.json`:

```bash
cd "$run"
opencode run --format json --model opencode/big-pickle "$prompt" \
  > transcript.jsonl 2> opencode_stderr.log
```

Record in `run.json`: requested model alias, model shown in the plain banner or JSON/session metadata if available, exact command, cwd, isolation mode, transcript format/path, prompt, start/finish time, operator interventions, exit code, and any OpenCode version/binary details. If provider-reported model is not available beyond the requested alias, set it to `null` and say so in the audit notes.

Do not compare new clean OpenCode results directly to historical contaminated in-repo OpenCode runs; mark those old runs as historical comparability caveats only.
