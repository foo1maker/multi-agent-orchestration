# Mode 2 Skill: Local vs GitHub Comparison

**Date:** 2026-09-09
**Repository:** https://github.com/foo1maker/multi-agent-orchestration
**Compared commit:** `560da94` (origin/main)
**Local skill path:** `C:\Users\1\.codex\skills\multi-agent-orchestration`
**Repo worktree path:** `D:\Github\multi-agent-orchestration`

## File-by-file comparison

| File | Status | Detail |
| --- | --- | --- |
| `SKILL.md` | **DIFFERENT** | 8 insertions, 7 deletions |
| `references/task_contract.md` | IDENTICAL | — |
| `references/lifecycle_and_recovery.md` | IDENTICAL | — |
| `references/result_packet.md` | IDENTICAL | — |
| `config/worker_defaults.yaml` | **DIFFERENT** | 4 insertions, 4 deletions |
| `agents/openai.yaml` | IDENTICAL | — |
| `scripts/audit_policy.py` | IDENTICAL | — |
| `scripts/lint_result_packet.py` | IDENTICAL | — |

## `SKILL.md` difference

The local copy replaces the GitHub version's "default configuration preserves current behavior" block (`model: inherit`, `reasoning_effort: auto`) with a persistent default that explicitly sets `model: gpt-5.6-luna` and `reasoning_effort: max` (lunamax). It also adds a note that Mode 2 dispatched workers use lunamax (1M context) unless the current task overrides it, and instructs Brain to never omit the `model` override because omitting it would inherit the host startup model (`gpt-6-astra`).

The corresponding paragraph about worker routing is updated from "with the shipped defaults, omit the `model` and `reasoning_effort` overrides" to "with the current defaults, pass `model=gpt-5.6-luna` and `reasoning_effort=max`".

## `config/worker_defaults.yaml` difference

The local copy replaces the GitHub version's `model: inherit` and `reasoning_effort: auto` comments and values with:

```yaml
worker:
  model: gpt-5.6-luna
  reasoning_effort: max
```

The comments explain that the default should not inherit the host startup model (`config.toml model=gpt-6-astra`) and that the default dispatched worker is lunamax (`gpt-5.6-luna`, 1M context — not 10k).

## Runtime mismatch observation

On the current host, the live `spawn_agent` tool rejects `gpt-5.6-luna` with:

```
Unknown model `gpt-5.6-luna` for spawn_agent.
Available models: glm-5.3-flash, muse-spark-1.3-contributor
```

The local config therefore cannot be honoured by the current runtime. Brain falls back to `glm-5.3-flash` on a rejected spawn. The config expectation and the runtime capability are out of sync; this report documents the mismatch for future reconciliation.
