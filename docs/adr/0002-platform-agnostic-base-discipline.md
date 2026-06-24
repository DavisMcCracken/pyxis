# The `AGENTS.md` base carries cross-cutting rules; skills stay agent-agnostic with quarantined asides

Pyxis 0.1.0 leaked Claude Code specifics (the Agent tool, slash-command names)
into skill prose, weakening the "works for any agent" value proposition. 0.2.0
formalizes a **two-tier discipline**: the `AGENTS.md` base stays fully
agent-agnostic and also gains the **laziness ladder** (YAGNI-first ordering) as a
short, always-loaded section the build skills defer to; the **skill pack is
written agnostic**, with any Claude Code concretion quarantined in a clearly
labeled, ignorable aside (so a single grep finds every platform-ism). The issue
tracker is reached only through `docs/agents/issue-tracker.md`, so `to-issues`
names neither GitHub nor local-markdown — both are first-class, anything else is
delegated to that file's freeform prose.

**Considered Options:** a hard purge of all platform names (rejected — vaguer,
and loses the concrete hint for Claude Code users); a separate
`_shared/LAZINESS.md` (rejected for now — another non-always-loaded file; promote
only if the section outgrows `AGENTS.md`); weaving laziness lines into each skill
(rejected — duplication that drifts out of sync).

Status: accepted.
