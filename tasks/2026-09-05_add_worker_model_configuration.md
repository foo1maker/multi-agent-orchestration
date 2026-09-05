# Task: Add configurable Worker model entry to Mode 2

STATUS: IN_PROGRESS
DATE: 2026-09-05
OWNER: ChatGPT / repository maintainer
TASK_TYPE: SKILL MAINTENANCE / CONFIGURATION

## Objective

Add a simple persistent configuration entry for the default Mode 2 Worker model without changing Brain/Worker responsibilities, native lifecycle semantics, Task Contract rules, or validation/recovery behavior.

## Completion standard

1. Add `config/worker_defaults.yaml` with a portable default that preserves current behavior.
2. Support a persistent default Worker model and reasoning-effort setting.
3. Precedence must be: current-task explicit user choice > skill configuration > host/runtime inheritance.
4. `model: inherit` must preserve the current behavior by omitting a model override.
5. `reasoning_effort: auto` must omit the reasoning-effort override and let the runtime/provider choose its normal supported behavior.
6. An explicit configured model must be passed to `spawn_agent` when the live schema supports model override.
7. A rejected/unavailable configured model must not silently fall back to another model; report the route failure or use the existing same-model supported-effort retry rule where applicable.
8. Preserve clean Worker context and all existing lifecycle/recovery rules.
9. Document the setting in `README.md`.
10. Extend `scripts/audit_policy.py` to verify the configuration entry exists and has the required fields without adding external Python dependencies.

## Required facts to read before editing

- `SKILL.md`
- `README.md`
- `scripts/audit_policy.py`
- `references/task_contract.md`
- `references/lifecycle_and_recovery.md`
- `references/result_packet.md`

## Configuration contract

Create:

```yaml
worker:
  model: inherit
  reasoning_effort: auto
```

Semantics:

- `worker.model: inherit` -> omit `model` in ordinary Worker spawn calls.
- `worker.model: <exact model id>` -> pass that exact model id when the live `spawn_agent` schema supports model selection.
- `worker.reasoning_effort: auto` -> omit `reasoning_effort`.
- `worker.reasoning_effort: <explicit value>` -> pass that value only when compatible with the selected model/runtime schema.
- Current-task explicit user instructions override both fields for that task only.
- Do not create provider-specific aliases or silently rewrite model ids.

## Scope

Allowed edits:

- `SKILL.md`
- `README.md`
- `scripts/audit_policy.py`
- new `config/worker_defaults.yaml`
- this task file

Do not modify the three runtime reference documents unless implementation reveals a real semantic dependency; configuration should remain a spawn-routing concern in `SKILL.md`.

## Forbidden changes

- No custom scheduler/runtime.
- No provider configuration changes.
- No Codex global config changes.
- No change to Brain scientific authority.
- No change to Task Contract, RESULT_PACKET, waiting, or Running Worker Immunity semantics.
- No hard-coded maintainer machine paths.
- No forced default to a relay-provider model.

## Validation

- Verify `SKILL.md` documents the configuration read and precedence.
- Verify default config preserves host inheritance.
- Verify README includes editable examples.
- Verify `scripts/audit_policy.py` checks for `config/worker_defaults.yaml`, `model`, and `reasoning_effort`.
- Verify the repository-local audit remains dependency-free.
- Confirm no runtime reference document changed.

## Evidence boundary

- VERIFIED: repository files and commits directly inspected.
- OBSERVED: committed configuration/docs/policy changes.
- INFERRED: host/provider compatibility behavior not exercised in this repository-only edit.
- UNKNOWN: exact model IDs and supported reasoning values on third-party installations.
