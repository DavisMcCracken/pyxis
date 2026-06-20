# agent-refinement

Workshop for a Python agent workflow: an `AGENTS.md` rule base plus a matching skill pack (uv + ruff + ty + pytest + hypothesis + prek, tiered TDD).

## Layout

| Path | What |
|---|---|
| [AGENTS.md](AGENTS.md) | The rule base — live copy governing this repo. Canonical template: `skills/py-new/templates/AGENTS.md` (what `/py-new` stamps into new repos). Keep the two in sync. |
| [CLAUDE.md](CLAUDE.md) | One line: `@AGENTS.md` — Claude Code reads the same rules. |
| [PRD.md](PRD.md) | Working product requirements, phase roadmap, stability rules, and issue → branch → PR workflow. |
| [PROJECT-STATUS.md](PROJECT-STATUS.md) | Current stable baseline, verification commands, archive locations, and active validation roadmap. |
| [skills/](skills/) | The skill pack: `py-new`, `grill-me`, `tdd`, `diagnose`, `improve-codebase-architecture`, `_shared/`. Deploy + provenance: [skills/README.md](skills/README.md). |
| [examples/](examples/) | Reference projects built under the rules: `wordstats` (lib+CLI, TDD), `ttlcache` (clock seam, regression drill), `spike_dedupe.py` (throwaway tier). |
| [model-tests/](model-tests/) | Battery for testing how well a model follows the workflow: fixtures, rubric, scorecard. See [model-tests/TESTING.md](model-tests/TESTING.md). |
| [archive/](archive/) | History (original draft). |

## Quickstart

- **Use the rules in a new project:** install the skill pack (copy `skills/` contents to `~/.claude/skills/`), then ask for a new Python project — `/py-new` scaffolds it green from commit zero. Without skills: follow the bootstrap lines at the top of `AGENTS.md`.
- **Evaluate a model against the workflow:** follow [model-tests/TESTING.md](model-tests/TESTING.md).

## Provenance

Skill pack derived from [Matt Pocock's skills](https://github.com/mattpocock/skills) — structure and sequencing kept, prose rewritten, Python-grounded. The AGENTS.md base was developed and then validated by building the `examples/` projects under its own rules; findings fed back as patches.
