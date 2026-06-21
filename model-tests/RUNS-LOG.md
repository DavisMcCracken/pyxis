# Run Log

Durable index of model-test runs. Bulky per-run artifacts live under `model-tests/runs/`, which is ignored; this file is the committed summary that operators update after each audit.

| date | requested model | provider-reported model | harness | isolation | task | trial | questions asked | validity | notes |
|---|---|---|---|---|---|---|---:|---|---|
| 2026-06-10 | claude-haiku-4.5 | Haiku 4.5 | Claude Code | pack | t3 | legacy-1 | none | valid | Completed quickly with a small number of permission requests. |
| 2026-06-12 | claude-haiku-4.5 | Haiku 4.5 | Claude Code | pack | t1 | legacy-1 | none | valid | Many permission requests; completed without task interruption. |
| 2026-06-12 | claude-haiku-4.5 | Haiku 4.5 | Claude Code | pack | t2 | legacy-1 | none | valid | Completed quickly. |
| 2026-06-12 | claude-haiku-4.5 | Haiku 4.5 | Claude Code | pack | t4 | legacy-1 | none | valid | Completed quickly. |
| 2026-06-13 | deepseek-v4-flash-free | deepseek-v4-flash | opencode/pi | in-repo | t1 | legacy-1 | Asked about dependencies and location. | contaminated | Read repository-local skill material; created the project outside the task fixture. |
| 2026-06-13 | deepseek-v4-flash-free | deepseek-v4-flash | opencode/pi | in-repo | t2 | legacy-1 | none | contaminated | In-repo execution allowed access to unrelated project material. |
| 2026-06-13 | deepseek-v4-flash-free | deepseek-v4-flash | opencode/pi | in-repo | t3 | legacy-1 | none | contaminated | In-repo execution allowed access to unrelated project material. |
| 2026-06-13 | deepseek-v4-flash-free | deepseek-v4-flash | opencode/pi | in-repo | t4 | legacy-1 | none | contaminated | In-repo execution allowed access to unrelated project material. |
| 2026-06-14 | big-pickle | deepseek-v4-flash | opencode/pi | in-repo | t1 | legacy-1 | none | contaminated | Provider-reported model differs from the requested alias. |
| 2026-06-14 | big-pickle | deepseek-v4-flash | opencode/pi | in-repo | t2 | legacy-1 | none | contaminated | Provider-reported model differs from the requested alias. |
| 2026-06-14 | big-pickle | deepseek-v4-flash | opencode/pi | in-repo | t3 | legacy-1 | none | contaminated | Provider-reported model differs from the requested alias. |
| 2026-06-14 | big-pickle | deepseek-v4-flash | opencode/pi | in-repo | t4 | legacy-1 | none | contaminated | Provider-reported model differs from the requested alias. |
| 2026-06-20 | haiku | claude-haiku-4-5-20251001 | Claude Code print | skill-less | t2 | trial-1 | none | valid | Issue #6 validation: wrote T2 behavior test first, observed valid RED, implemented JSON output, and all verification components passed. |
| 2026-06-20 | haiku | claude-haiku-4-5-20251001 | Claude Code print | skill-less | t2 | trial-2 | none | valid | Issue #6 validation: wrote T2 behavior test first, observed valid RED, implemented JSON output, and ran full verify loop green. |
| 2026-06-20 | haiku | claude-haiku-4-5-20251001 | Claude Code print | pack | t2 | trial-1 | none | valid | Issue #7 validation: pack visible, no unnecessary questions, valid RED before implementation, full verification passed; no explicit `tdd` Skill event observed. |
| 2026-06-20 | haiku | claude-haiku-4-5-20251001 | Claude Code print | pack | t2 | trial-2 | none | valid | Issue #7 validation: pack visible, no unnecessary questions, valid RED before implementation, diagnostics explicitly tested, full verification passed after formatting fix; no explicit `tdd` Skill event observed. |
