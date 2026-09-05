# Task: Add configurable Worker model entry to Mode 2

STATUS: COMPLETED
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

## Required facts read before editing

- `SKILL.md`
- `README.md`
- `scripts/audit_policy.py`
- `references/task_contract.md`
- `references/lifecycle_and_recovery.md`
- `references/result_packet.md`

## Implemented configuration contract

```yaml
worker:
  model: inherit
  reasoning_effort: auto
```

Semantics now enforced by `SKILL.md`:

- `worker.model: inherit` -> omit `model` in ordinary Worker spawn calls.
- `worker.model: <exact model id>` -> pass that exact model id when the live `spawn_agent` schema supports model selection.
- `worker.reasoning_effort: auto` -> omit `reasoning_effort`.
- `worker.reasoning_effort: <explicit value>` -> pass that value only when compatible with the selected model/runtime schema.
- Current-task explicit user instructions override both fields for that task only.
- Persistent configured model ids are not silently rewritten or replaced by another model.
- If a configured or task-explicit model is unavailable, the route fails closed rather than silently falling back to host inheritance.
- Multimodal fallback may replace an inherited route, but may not override a persistent or task-explicit model unless the current task explicitly permits fallback.

## Files changed

- `SKILL.md`
- `README.md`
- `scripts/audit_policy.py`
- `config/worker_defaults.yaml`
- `tasks/2026-09-05_add_worker_model_configuration.md`

## Validation

VERIFIED:

- `config/worker_defaults.yaml` exists with `model: inherit` and `reasoning_effort: auto`.
- `SKILL.md` reads the config before first Worker spawn and defines precedence as current-task explicit choice > persistent config > host/runtime inheritance.
- `SKILL.md` preserves omission of model/effort overrides for the shipped defaults.
- `SKILL.md` prevents silent replacement of persistent or task-explicit Worker models.
- `README.md` documents the setting and an editable explicit-model example.
- `scripts/audit_policy.py` remains standard-library only and checks the Worker config file and required fields.
- The three runtime reference document blob SHAs are unchanged from the pre-task state:
  - `references/task_contract.md`: `4ab9de7b44fa4c5c9831d7b10a444e4917b7bedd`
  - `references/lifecycle_and_recovery.md`: `922f0d557f45d46d15ef28994e533f2792500dad`
  - `references/result_packet.md`: `eb6e3b413396732dfb125f585a811d5a7d6e5972`

NOT CLAIMED:

- No live third-party Worker model/provider smoke test was run in this repository-only change.
- Exact available model ids and supported reasoning values remain host/provider-dependent.

## Evidence boundary

- VERIFIED: repository files/tree/SHAs directly inspected.
- OBSERVED: configuration, policy, README, and audit changes committed to `main`.
- INFERRED: an installed host following `SKILL.md` will apply the persistent route when its `spawn_agent` schema exposes model overrides.
- UNKNOWN: exact provider compatibility outside the maintainer environment.
