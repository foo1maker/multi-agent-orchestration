# Multi-Agent Orchestration (Mode 2)

A Codex skill for disciplined native multi-agent execution. `Mode 2` is the user-facing alias: the Brain owns planning and final judgment, bounded Workers execute delegated contracts, the native Codex runtime owns agent lifecycle/waiting, and the Brain validates settled evidence before completion.

This is a community-maintained project and is not an official OpenAI project.

## Core model

```text
Brain thinks.
Brain delegates.
Worker executes.
Codex runtime waits.
Brain validates.
```

The skill is intentionally an orchestration policy, not a custom scheduler. It does not implement its own worker manager, heartbeat loop, completion database, watchdog, or recovery runtime.

## What it provides

- explicit Mode 2 activation and delegation boundaries;
- Brain-authored Worker Task Contracts;
- bounded `DISCOVERY`, `EXECUTION`, `ANALYSIS`, and `REVIEW` task modes;
- persistent default Worker model/reasoning configuration;
- clean-context worker spawning requirements;
- native agent lifecycle and quiescent-wait rules;
- result-packet normalization and Stage 2/Stage 3 validation;
- recovery rules that avoid treating elapsed time or token usage as proof of failure;
- lightweight policy/result-packet validation scripts.

## Requirements

The host must expose compatible native Codex multi-agent capabilities, including the equivalents of:

- `spawn_agent`
- `wait_agent`
- `followup_task`

The exact tool schema and available worker models are host-dependent. Model/provider compatibility observations recorded in `SKILL.md` are evidence from the maintainer environment, not universal guarantees for every Codex installation.

## Installation

Clone the repository into the skill location used by your Codex/agent host, or otherwise register the repository as a skill package:

```bash
git clone https://github.com/foo1maker/multi-agent-orchestration.git
```

The repository root contains `SKILL.md`; keep `config/`, `references/`, `agents/`, and `scripts/` beside it.

The exact installation directory is intentionally not hard-coded because Codex/agent installations differ across operating systems and host setups.

## Activation

The skill is designed for explicit activation, for example:

```text
mode2
Mode 2
启动模式2
开启模式2
使用模式2
```

Simple tasks should remain single-agent. Mode 2 is for tasks where bounded delegation provides real execution or review value.

## Worker model configuration

Persistent Worker routing is configured in:

```text
config/worker_defaults.yaml
```

The shipped default preserves native host inheritance:

```yaml
worker:
  model: inherit
  reasoning_effort: auto
```

Meaning:

- `model: inherit` — do not send a `model` override to `spawn_agent`;
- `reasoning_effort: auto` — do not send a `reasoning_effort` override;
- replace `inherit` with an exact model id to make that model the persistent Mode 2 Worker default;
- replace `auto` with a supported explicit reasoning value if desired.

Example:

```yaml
worker:
  model: glm-5.3-flash
  reasoning_effort: high
```

Resolution precedence is fixed:

```text
current-task explicit user choice
> config/worker_defaults.yaml
> host/runtime inheritance
```

A task-specific user choice therefore overrides the persistent default only for that task. The skill does not rewrite model ids or silently fall back to another model when an explicitly configured model is unavailable. Model ids and supported reasoning values remain host/provider-dependent.

## Repository layout

```text
SKILL.md                         Main runtime policy
config/worker_defaults.yaml      Persistent Worker model/reasoning defaults
agents/openai.yaml               Skill interface metadata
references/task_contract.md      Worker contract specification
references/lifecycle_and_recovery.md
                                 Native lifecycle, waiting, recovery rules
references/result_packet.md      Worker result and validation protocol
scripts/audit_policy.py          Read-only structural policy/config audit
scripts/lint_result_packet.py    RESULT_PACKET syntax/status linter
tasks/                           Maintainer task history
reports/                         Historical maintainer reports
```

`tasks/` and `reports/` are historical maintenance records. They are not runtime authority; current runtime behavior is defined by `SKILL.md`, `config/worker_defaults.yaml`, and the referenced runtime documents.

## Validation

From the repository root:

```bash
python scripts/audit_policy.py
```

The audit checks the repository-local skill and Worker routing configuration by default. Optional host/global policy files can be supplied explicitly; see `python scripts/audit_policy.py --help`.

A result packet can be linted from a file:

```bash
python scripts/lint_result_packet.py packet.txt
```

or through stdin.

These scripts validate structure and protocol syntax only. They do not determine whether a scientific, engineering, or research conclusion is correct.

## Design boundaries

- Brain owns final scientific/architectural judgment.
- Worker self-report is evidence, not proof.
- Runtime-native lifecycle state and `RESULT_PACKET STATUS` are separate concepts.
- A Worker is not failed merely because it is slow, uses many tokens, or produces no intermediate artifact.
- Do not duplicate a delegated task in the Brain thread just because the Brain is waiting.
- Do not replace the native runtime with a home-grown orchestration scheduler.

## Contributing

See `CONTRIBUTING.md`. Changes that alter runtime semantics should include a clear rationale and validation evidence. Portability fixes should avoid embedding machine-specific paths, credentials, or provider assumptions.

## Security

Never commit API keys, access tokens, credentials, private configuration snapshots, or secret-bearing logs. See `SECURITY.md`.

## License

MIT. See `LICENSE`.
