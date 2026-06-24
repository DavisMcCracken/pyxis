# Development and Distribution Workflow

This repo is the development home for the Python agent workflow skills. It contains both the user-facing skill pack and the validation/provenance machinery used to improve it safely.

## Repository roles

Treat the project as two layers:

| Layer | Contents | Audience | Ships to users? |
|---|---|---|---|
| Product | `skills/`, `README.md`, `LICENSE`, optionally `AGENTS.md` | People installing the skills | Yes |
| Development / validation | `model-tests/`, `examples/`, `PRD.md`, `PROJECT-STATUS.md`, validation findings and runbooks | Maintainers | No, unless deliberately publishing evidence |

The development layer is valuable. Do not delete it just to make a release smaller. Distribution should select the product layer instead.

## Default development loop

All non-trivial work should move through this loop:

1. **Create or select a GitHub issue.**
   - State the goal, affected files, acceptance criteria, and validation level.
   - Use the issue to decide whether model testing is needed.
2. **Start from clean `main`.**
   ```bash
   git checkout main
   git pull --ff-only origin main
   git status --short --branch
   ```
3. **Create a scoped branch.**
   ```bash
   git checkout -b docs/issue-N-short-name
   # or: skill/issue-N-short-name, fix/issue-N-short-name, release/issue-N-short-name
   ```
4. **Make the smallest coherent change.**
   - One issue or one decision per PR.
   - Keep root `AGENTS.md` and `skills/scaffold/templates/AGENTS.md` identical when either changes.
5. **Validate at the right level.**
   - Do not run model tests for every docs or packaging edit.
   - Do run stronger validation when changing rules, skill triggers, or claimed model behavior.
6. **Open a PR.**
   - Include summary, validation commands/results, and `Closes #N` when applicable.
7. **Merge only after review/checks.**
   - Prefer squash merge.
   - Delete the branch.
   - Pull `main` and confirm the tree is clean.

## Validation levels

Use the lightest validation that honestly covers the risk.

### Level A — docs, license, release notes

Examples: `README.md`, `LICENSE`, release notes, non-behavioral prose.

Run:

```bash
git diff --check
```

If install instructions changed, also run a local skills listing/install smoke test.

### Level B — skill metadata or packaging

Examples: frontmatter, `skills/README.md`, release artifact script, skills.sh install instructions.

Run:

```bash
git diff --check
npx skills add ./ --list
npx skills add ./ --agent claude-code --skill scaffold --copy
```

Use a temporary install location or clean up after the smoke test if needed.

### Level C — skill procedure or trigger wording

Examples: changing when `tdd` should trigger, changing `scaffold` behavior, adding a new skill.

Run Level B checks plus a targeted manual or agent smoke test. Consider a calibrated model run if the change makes a behavior claim.

### Level D — core rule or validation-harness change

Examples: `AGENTS.md`, `skills/scaffold/templates/AGENTS.md`, `model-tests/` harness scripts, validation rubric.

Run:

```bash
cd model-tests
uv run ruff check scripts tests
uv run ruff format --check scripts tests
uv run ty check scripts tests
uv run pytest -q
```

For rule wording meant to improve model behavior, create a validation issue and record the run in the model-test ledgers.

## Distribution strategy

**This repository is the distribution.** `npx skills` installs only the `skills/` pack — `model-tests/`, `examples/`, and the planning docs stay here as maintainer artifacts and never reach a user's install (verify with `npx skills add ./ --list`: it reports exactly the eight skills). One repo is the right default and stays correct as long as that projection holds.

The public install path is skills.sh / `npx skills`:

```bash
npx skills add DavisMcCracken/pyxis
npx skills add DavisMcCracken/pyxis --agent claude-code --skill scaffold
```

A separate, product-only repo is **optional and deferred** — reach for it only with a concrete reason (external contributors tripping over the dev layer, or a vanity install slug), never for correctness. If that day comes, the projection looks like:

```text
pyxis-public/
├── README.md
├── LICENSE
├── AGENTS.md
└── skills/
    ├── _shared/
    ├── debug/
    ├── handoff/
    ├── interview/
    ├── refactor/
    ├── scaffold/
    ├── tdd/
    ├── to-issues/
    └── to-prd/
```

Users should install from the distribution repo once it exists:

```bash
npx skills add DavisMcCracken/<public-repo>
```

Until then, publishing from this repo is acceptable if the README is clear that `model-tests/` and `examples/` are maintainer artifacts.

## Dev repo → public distribution repo flow

*Only relevant if you split out a separate distribution repo (the optional, deferred path above). For single-repo releases, skip to "Release cadence."*

Do **not** copy and paste files by hand. Manual copying is easy to do inconsistently and leaves no reproducible trail.

Use this flow instead:

1. **Develop and validate in this repo.**
   - This repo remains the source of truth.
   - Merge the change to `main` here first.
2. **Run the appropriate validation level.**
   - For release candidates, run at least Level B.
   - If rules or trigger behavior changed, use Level C or D.
3. **Sync only product files to the public repo.**
   - Use a small script or `rsync` allowlist.
   - Sync includes: `skills/`, `README.md`, `LICENSE`, optional `AGENTS.md`.
   - Sync excludes: `model-tests/`, `examples/`, `PRD.md`, `PROJECT-STATUS.md`, `.hermes/`, caches, and archives.
4. **Open a PR in the public repo.**
   - The PR title should match the source change or release issue.
   - Link back to the dev repo issue/PR if useful.
5. **Validate the public repo.**
   ```bash
   npx skills add ./ --list
   npx skills add ./ --agent claude-code --skill scaffold --copy
   ```
6. **Merge the public repo PR.**
7. **Tag and release from the public repo.**
   ```bash
   git tag <version>
   git push origin <version>
   gh release create <version> --title "<version>" --generate-notes
   ```
8. **Smoke-test the published install path.**
   ```bash
   npx skills add DavisMcCracken/<public-repo> --list
   ```

### Minimal sync command

From the dev repo root, assuming the public repo is checked out beside it at `../pyxis-public`:

```bash
rsync -a --delete \
  README.md LICENSE AGENTS.md skills/ \
  ../pyxis-public/
```

Then inspect before committing in the public repo:

```bash
cd ../pyxis-public
git status --short
git diff --stat
git diff --check
npx skills add ./ --list
```

A script is better than a remembered command once this happens more than once. The script should use an explicit allowlist, not a broad copy with ignores.

## Release cadence

Use simple semver-style tags:

| Version | Use for |
|---|---|
| `v0.1.x` | early packaging/docs fixes |
| `v0.2.0` | new skill or meaningful skill behavior change |
| `v1.0.0` | stable public workflow after external use |

A release should have:

- clear install command,
- included skills list,
- notable changes,
- known limits,
- validation summary appropriate to the change.

## When to run model tests

Run model tests when the change affects model behavior or when the release notes claim behavior improved.

Good reasons:

- changing `AGENTS.md`,
- changing skill trigger descriptions,
- adding a new skill,
- changing `scaffold` scaffold behavior,
- changing TDD/regression requirements,
- comparing model or harness behavior.

Skip model tests for:

- typo fixes,
- install docs,
- license/release notes,
- packaging script changes that do not alter skill content.

## Bottom line

The sustainable flow is:

```text
issue → branch → change → right-sized validation → PR → squash-merge to main → tag/release → smoke-test npx skills install
```

This repo is both the lab and the distribution. If you ever split out a product-only repo, make it a reproducible allowlist projection of `skills/`, never a hand-maintained copy-paste fork.
