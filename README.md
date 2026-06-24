# Pyxis

A Python agent workflow you can install: an `AGENTS.md` rule base plus a matching Claude Code skill pack — uv + ruff + ty + pytest + hypothesis + prek, with tiered test-driven development built in. Install the pack and your coding agent scaffolds new Python projects green from commit zero, builds features test-first, and debugs reproduce-first.

## Install

```bash
npx skills add DavisMcCracken/pyxis                     # all five skills
npx skills add DavisMcCracken/pyxis --skill scaffold    # or just one
```

Only the `skills/` pack is installed — `model-tests/` and `examples/` are maintainer artifacts and never reach your install. No skills tool? Copy `skills/` into `~/.claude/skills/` by hand. Working without skills at all: follow the bootstrap lines at the top of [`AGENTS.md`](AGENTS.md).

## Skills

| Skill | Reach for it when |
|---|---|
| [`scaffold`](skills/scaffold/SKILL.md) | Starting a new Python project — green verify loop from commit zero |
| [`tdd`](skills/tdd/SKILL.md) | Building a feature or fixing an ordinary bug — red-green-refactor slices |
| [`debug`](skills/debug/SKILL.md) | A hard, intermittent, or unclear-cause bug needs reproduce-first investigation |
| [`interview`](skills/interview/SKILL.md) | Stress-testing a plan or design before you build it |
| [`refactor`](skills/refactor/SKILL.md) | Improving architecture — find shallow modules and deepen them |

See [skills/README.md](skills/README.md) for how the skills hand off to each other, plus deploy and provenance notes.

## Repository layout

| Path | What | Audience |
|---|---|---|
| [skills/](skills/) | The installable skill pack, plus `_shared/` references | Users |
| [AGENTS.md](AGENTS.md) | The rule base governing this repo. Canonical template: `skills/scaffold/templates/AGENTS.md` (what `/scaffold` stamps into new repos) | Users |
| [CLAUDE.md](CLAUDE.md) | One line — `@AGENTS.md`, so Claude Code reads the same rules | Users |
| [examples/](examples/) | Reference projects built under the rules: `wordstats`, `ttlcache`, `spike_dedupe.py` | Maintainers |
| [model-tests/](model-tests/) | Battery measuring how well a model follows the workflow | Maintainers |
| [PRD.md](PRD.md) · [DEVELOPMENT.md](DEVELOPMENT.md) · [PROJECT-STATUS.md](PROJECT-STATUS.md) | Requirements, contribution/release workflow, current status | Maintainers |
| [archive/](archive/) | History (original draft) | — |

## Provenance

Skill pack derived from [Matt Pocock's skills](https://github.com/mattpocock/skills) — structure and sequencing kept, prose rewritten, Python-grounded. The `AGENTS.md` base was developed and then validated by building the `examples/` projects under its own rules; findings fed back as patches.

## License

[MIT](LICENSE).
