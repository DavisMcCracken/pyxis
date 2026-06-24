# Platform Agnosticism

Two tiers (ADR-0002):

- The **`AGENTS.md` base is fully agent-agnostic** — any agent that reads it follows the rules.
- The **skill pack is written agnostic too.** Describe the *capability* in the main prose. Where a step genuinely benefits from a Claude-Code-specific feature (the Agent tool / sub-agents, a slash-command name), quarantine the concrete how in a labeled aside the reader can skip:

  > **Claude Code:** spawn the read-only walk with the Agent tool (`subagent_type=Explore`).

## Rules

- **Main prose names the capability, not the product.** "Explore in parallel if your harness supports sub-agents; otherwise read sequentially." The aside only adds the concrete invocation for Claude Code.
- **No skill depends on its asides.** Delete every `> **Claude Code:**` block and the procedure must still read correctly and run on a plain agent.
- **One greppable marker:** `> **Claude Code:**`. A single grep enumerates every platform-ism in the pack — that is the agnostic-audit check.
- **Issue-tracker commands are not asides.** They go through `docs/agents/issue-tracker.md` (the tracker indirection), so a skill names neither GitHub nor `gh` directly.
