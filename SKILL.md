---
name: multi-agent-orchestration
description: Use when the user explicitly activates Mode 2 (including "启动模式2", "开启模式2", or "使用模式2") or requests parallel native multi-agent execution. Governs Brain-authored task contracts, Codex native agent lifecycle and waiting, result fan-in, validation, and bounded recovery. Do not use for simple single-agent tasks or requests that merely mention agents without asking for delegation.
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
  decomposes work, writes Worker contracts, integrates results, performs Stage
  2 validation, decides Stage 3 completion, and chooses any next round.
- Worker executes only its current Task Contract. It does not re-plan the whole
  user objective, make the final completion decision, expand scope, or start a
  new round.
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
  batch checksum or hash verification, data transforms, broad tests, and any
  large volume of deterministic commands. Brain judges substantiality from
  context, not from fixed file counts or time thresholds.
- Delegate substantial, independent work with clear execution or review value.
  Large work should not be retained by Brain solely to avoid delegation.
- Do not skip validation merely to reduce cost. Brain may decide another round
  after settled evidence shows it is needed.
- Once Brain delegates a concrete execution task, it must not secretly repeat
  that same task in the main thread. Brain may still do independent analysis,
  gather non-duplicative context, prepare decisions, process other results, and
  perform final validation.

## Before First Spawn

Read all three references before the first spawn in a Mode 2 task:

1. [Task contracts](references/task_contract.md)
2. [Lifecycle and recovery](references/lifecycle_and_recovery.md)
3. [Result packets and validation](references/result_packet.md)

Use Codex native `spawn_agent`, `wait_agent`, and `followup_task`. Do not start a
second Codex runtime from a terminal.

Root keeps the user's selected model and reasoning effort. Model routing for
subagents is:

- Ordinary Worker, Explorer, and Reviewer tasks default to
  `deepseek-v4-flash:0731` with `max` reasoning unless the user explicitly
  specifies another model or reasoning value for the task.
- The DS Ollama route for `deepseek-v4-flash:0731` supports `max`, not `xhigh`;
  do not request `xhigh` for that model.
- Tasks requiring image, scanned-document, visual-page, or other multimodal
  input default to `gemini-3.7-flash-high`.
- Do not retry a confirmed multimodal compatibility failure with another
  text-only model.

Use a clean or bounded fork when setting a model override because full-history
forks inherit the parent model and do not accept overrides. Reviewer Workers are
read-only. Use an Inspector only when a formal-task acceptance risk justifies an
independent, read-only, clean-context check.

An explicit user model or reasoning choice overrides these defaults only for the
task where it was requested and only when the `spawn_agent` schema supports that
override. Without an explicit override, do not silently substitute another model
for `deepseek-v4-flash:0731`. When another model is selected, use a reasoning
effort supported by that model/provider rather than copying the DS setting.

Task names use lowercase letters, digits, and underscores. Prefer a clean Worker
context; inherit only the context the contract actually needs.

## Operating Boundaries

- Never raw-forward the user's long prompt. Brain writes a scoped Task Contract.
- Never treat `RESULT_PACKET STATUS` as a Codex native lifecycle state.
- Never infer Worker failure from elapsed time, token use, reasoning duration,
  a wait timeout, or absence of an intermediate artifact.
- Never poll files, logs, processes, or repeated agent listings to supervise a
  live Worker.
- Never interrupt or replace a Worker solely because it appears slow.
- Stage 2 verifies settled evidence and critical artifacts; it does not redo the
  entire delegated workflow unless reproduction is an acceptance requirement.

Scripts in this skill validate policy structure and result-packet syntax only:

- `scripts/audit_policy.py` checks policy placement, references, and forbidden
  runtime filenames.
- `scripts/lint_result_packet.py` checks the text protocol and allowed status
  values. It does not judge whether the result is correct or sufficient.

Scripts do not run the workflow or make delegation, waiting, recovery,
interrupt, research, engineering, or Stage 3 completion decisions.
