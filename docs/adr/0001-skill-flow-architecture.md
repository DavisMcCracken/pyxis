# Skills sequence along one spine with marked detours, headed by `interview`

Pyxis 0.1.0 documented no ordering, so it was unclear which skill kicked off work
(`scaffold` and `interview` both looked like starts). 0.2.0 arranges all eight
skills as one **spine** — `interview` (universal head) → `scaffold` (detour, new
repos only) → a **fork** (multi-session: `to-prd` → `to-issues` → fresh session
per issue → `tdd`; single change: `tdd` directly) — with `debug` as a detour off
`tdd` and `refactor` as an on-ramp feeding `interview`. `interview` is the head
even before a repo exists; its stack decisions reach `scaffold` through the same
context window (no scratch file), and `scaffold` stamps them into the new repo's
`AGENTS.md`. The map is the rewritten `skills/README.md` — one canonical map, no
second file to drift from it.

**Considered Options:** a true single sequence everything passes through
(rejected — it lies about the real branches, and users bounce when their case
does not fit); a `scaffold`-first head for new projects (rejected — bootstraps
before the design is known and splits the entry point in two).

**Consequences:** `handoff` covers any session break between `interview` and
`scaffold`. `to-prd`/`to-issues` are skipped for single-session work, keeping the
lazy path lazy. `handoff` is a conditional bridge (agent-suggested when the
smart-zone is neared, runnable manually anytime), not a fixed stop; it is not the
between-issues mechanism — a fresh session carrying the PRD plus one issue is.

Status: accepted.
