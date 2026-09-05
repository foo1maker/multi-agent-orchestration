---
name: multi-agent-orchestration
description: Use when the user explicitly activates Mode 2 (including "启动模式2", "开启模式2", "使用模式2", "mode2", or "Mode 2") or requests parallel native multi-agent execution. Governs Brain-authored task contracts, Codex native agent lifecycle and waiting, result fan-in, validation, and bounded recovery. Do not use for simple single-agent tasks or requests that merely mention agents without asking for delegation.
---

# Multi-Agent Orchestration

Mode 2 is the user-facing alias for this skill. Load this skill before the first
`spawn_agent` whenever Mode 2 is activated. Its activation lasts only for the
current task and ends when the task finishes or the user says to stop Mode 2.

## Architecture

```text
Brain thinks.
Brain delegates.
Worker executes.
Codex runtime waits.
Brain validates.
```

- Brain understands the objective, decides whether delegation adds value,
  decomposes work, writes Worker contracts, integrates results, owns all
  scientific judgment, performs Stage 2 validation and scientific synthesis,
  decides Stage 3 completion, and chooses any next round.
- Worker executes only its current Task Contract. It gathers evidence, runs
  computations, and may propose rankings or interpretations, but does not
  make final completion or scientific decisions, expand scope, or start a new
  round.
- Scientific judgment is Brain-owned and must not be delegated. Worker scores
  and rankings are evidence for Brain rather than final decisions.
- Codex native runtime owns agent lifecycle and waiting. Do not build a custom
  scheduler, watchdog, heartbeat, barrier, completion database, state machine,
  wait loop, recovery engine, or side-channel orchestration runtime.

## Delegation Decision

- Keep simple tasks single-agent. Do not spawn to reach an agent count.
- Parallelism determines whether independent Workers should run concurrently;
  it is not a prerequisite for delegation. Small, bounded work—a few read-only
  checks, light validation, or trivial execution—may remain with Brain. But
  substantial execution should normally be delegated even when the work is
  sequential.
- Substantial execution includes, but is not limited to: multi-file creation or
  modification, batch file operations, longer command chains, artifact
  packaging, Git staging/commit/push workflows, external sync (Drive, cloud),
  batch checksum or hash verification, data transforms, broad tests, mechanical
  schema/existence checks, and any large volume of deterministic commands.
  Brain judges substantiality from context, not from fixed file counts or time
  thresholds. Brain preferentially spends its own reasoning budget on scientific
  synthesis and decision-making rather than mechanical artifact validation that
  a worker can perform reliably.
- Pre-spawn reconnaissance is not exempt from delegation. Brain may read only
  the minimum already-named control-plane facts needed to define the objective,
  authority boundary, permissions, and a bounded first contract. Repository or
  data-package reconnaissance, path discovery, manifest discovery, schema
  inspection, broad existence checks, or similar execution-level reconnaissance
  should not be performed by Brain merely to make a later contract more complete.
  If those execution facts are unresolved, delegate them as a bounded
  `TASK_MODE: DISCOVERY` contract.
- Delegate substantial, independent work with clear execution or review value.
  Large work should not be retained by Brain solely to avoid delegation.
- Do not skip validation merely to reduce cost. Brain may decide another round
  after settled evidence shows it is needed.
- Once Brain delegates a concrete execution task, it must not secretly repeat
  that same task in the main thread. Brain may reason, process settled results,
  or execute work a current decision actually requires. Idle time is
  not a reason to create work. Repo, file, log, and progress checks, and
  speculative validation prep, are not independent work unless a concrete new
  decision needs them.

## Before First Spawn

Read all three references before the first spawn in a Mode 2 task:

1. [Task contracts](references/task_contract.md)
2. [Lifecycle and recovery](references/lifecycle_and_recovery.md)
3. [Result packets and validation](references/result_packet.md)

Also read `config/worker_defaults.yaml` before resolving Worker model routing.
The configuration is a persistent default, not a replacement for current-task
user instructions. Resolve Worker model settings in this order:

1. Explicit model or reasoning-effort choice in the current user task.
2. `config/worker_defaults.yaml`.
3. Host/runtime inheritance.

The default configuration preserves current behavior:

```yaml
worker:
  model: inherit
  reasoning_effort: auto
```

`model: inherit` means omit the `model` override. `reasoning_effort: auto` means
omit the `reasoning_effort` override. Any other `model` value is an exact model
id and must not be silently rewritten or aliased. Any explicit configured
reasoning value is passed only when the live schema supports the override and it
is compatible with the selected model. If the configuration file exists but is
malformed or omits the required `worker.model` / `worker.reasoning_effort`
fields, stop before spawning and report `BLOCKED` rather than guessing a route.

Use Codex native `spawn_agent`, `wait_agent`, and `followup_task`. Do not start a
second Codex runtime from a terminal.

`mode2` / `Mode 2` / `启动模式2` / `开启模式2` / `使用模式2` is an explicit
spawn request. After the three references and Worker defaults are loaded, the
next native call in that Mode 2 task must be `spawn_agent`, or `BLOCKED` if the
live tool list has no `spawn_agent`. If Brain cannot yet write a normal
EXECUTION, ANALYSIS, or REVIEW contract because target paths, manifests,
schemas, or authoritative inputs are unresolved, the first spawn must be a
bounded `DISCOVERY` contract. Missing execution facts are not permission for
Brain to perform substantial reconnaissance before the first spawn. Do not emit
a user-facing "Mode 2 activated" / "I will spawn" message and then end the
turn. Writing a contract without calling `spawn_agent` in the same turn is a
protocol failure. A spawn that uses a full-history fork or a prose stub instead
of a scoped contract is also a protocol failure: do not compensate for an
unfinished contract by copying parent history. Do not call MCP servers named
`codex` or `file_system`; read skill files with the native shell
(`Get-Content -LiteralPath` on PowerShell).

Root keeps the user's selected model and reasoning effort. Model routing for
subagents is:

- Ordinary Worker, Explorer, and Reviewer tasks use the resolved Worker model
  settings above. With the shipped defaults, omit the `model` and
  `reasoning_effort` overrides and inherit the Codex host's normal native worker
  model path. OBSERVED 2026-09-04: on this host, clean-context (`fork_turns:
  none`) workers on relay provider models (`glm-5.3-flash`,
  `gemini-3.7-flash-high`) could not consume the encrypted `NEW_TASK` contract
  payload and settled without executing the contract, while GPT-5.6-class
  workers executed identical contracts correctly.
- If the current task or persistent configuration selects a relay-provider
  Worker model (`glm-5.3-flash`, `gemini-3.7-flash-high`, `grok-4.6`), spawn it
  with the resolved reasoning setting. Treat a settled no-execution or
  role-inverted result as insufficient evidence under the normal recovery
  rules; do not silently substitute another model merely because the configured
  route is less reliable on the maintainer host.
- The GLM route for `glm-5.3-flash`, when selected, supports
  `max`/`high`/`medium`/`low`, not `xhigh` or `ultra`. Do not request `xhigh`
  for that model. When the current task explicitly authorizes fallback to
  another provider model, choose a reasoning effort supported by that fallback
  rather than copying an incompatible effort from the original route.
- Tasks requiring image, scanned-document, visual-page, screenshot, or other
  multimodal input may use `glm-5.3-flash` when selected. If an inherited model
  route has a confirmed multimodal compatibility failure, the existing fallback
  order may use `gemini-3.7-flash-high`, then `grok-4.6`. If the model came from
  `config/worker_defaults.yaml` or an explicit current-task model choice, do not
  substitute another model unless the current user task explicitly permits
  fallback.
- Do not retry a confirmed multimodal compatibility failure with a text-only
  model.

Every `spawn_agent` call must use a clean Worker context. When the live schema
exposes `fork_turns`, pass `none`. If it uses another name for a clean or
bounded fork, pass that clean value. Full-history fork (`all` or equivalent) is
a protocol failure: it copies the parent conversation and parent model, and
model overrides do not apply. Put needed paths and facts in the Task Contract
`message`; do not rely on parent history.

When the schema exposes `model` and `reasoning_effort`, use the resolved Worker
settings above. Omit either field when its resolved value is `inherit` or
`auto`, respectively. If the current user task selected a value, that value
wins for that task only. Reviewer Workers are read-only. Use an Inspector only
when a formal-task acceptance risk justifies an independent, read-only,
clean-context check.

Do not silently substitute another model for an explicit task or persistent
configuration choice. If a spawn is rejected because the reasoning effort is
unsupported for the selected model, re-issue it once on the same model with a
supported effort. If the selected model itself is unavailable or rejected,
report the route as `BLOCKED`/insufficient instead of silently falling back to
the host model. Parallel spawning of independent Workers is allowed; only a
runtime-confirmed spawn result counts as a live Worker, and a rejected wrapper
call is re-issued as individual `spawn_agent` calls.

Task names use lowercase letters, digits, and underscores. The Worker
assignment is the Task Contract in `message`, not the parent transcript.

## Operating Boundaries

- Never raw-forward the user's long prompt. Brain writes a scoped Task Contract.
  REVIEW/ANALYSIS contracts are deliverable-first (see task_contract.md): name
  the files that already hold counts, hashes, or summaries; do not assign
  recursive full-content scans of a data package. `DISCOVERY` is the only mode
  in which final target paths may still be unresolved; it must use concrete,
  bounded `DISCOVERY ROOTS`, closed target criteria, and a named deliverable.
- Scientific judgment is Brain-owned: never delegate the final scientific
  ranking, trade-off choice, or route recommendation to a Worker.
- Worker rankings and score tables are evidence, not decisions. Brain must not
  lock a ranking solely because a Worker score table ordered candidates that way.
- Never treat `RESULT_PACKET STATUS` as a Codex native lifecycle state.
- Never infer Worker failure from elapsed time, token use, reasoning duration,
  a wait timeout, or absence of an intermediate artifact.
- Never poll files, logs, processes, or repeated agent listings to supervise a
  live Worker, except the audits in lifecycle_and_recovery.md: the empty-set
  `list_agents` check, and the five-minute named-output check.
- Never enter quiescent wait with zero confirmed live Workers; a rejected or
  unconfirmed spawn creates no Worker.
- Quiescent wait has two bounded audits: after two consecutive silent
  timeouts, one `list_agents` empty-set check; every ~5 minutes of silent
  wait, one named-output check. Waiting on an empty or fully terminal agent
  set cannot settle.
- Never interrupt or replace a Worker solely because it appears slow. User
  `卡住` is steering: run the named-output check now (lifecycle_and_recovery.md).
  Do not take over a Worker SCOPE while native status is still `running`.
- Stage 2 verifies settled evidence and critical artifacts; it does not redo the
  entire delegated workflow unless reproduction is an acceptance requirement.

Scripts in this skill validate policy structure and result-packet syntax only:

- `scripts/audit_policy.py` checks policy placement, references, Worker routing
  configuration, and forbidden runtime filenames.
- `scripts/lint_result_packet.py` checks the text protocol and allowed status
  values. It does not judge whether the result is correct or sufficient.

Scripts do not run the workflow or make delegation, waiting, recovery,
interrupt, research, engineering, or Stage 3 completion decisions.