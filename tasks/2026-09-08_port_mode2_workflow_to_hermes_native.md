# SUPERSEDED — do not execute

Status: `SUPERSEDED`

This task has been superseded by the user's revised architecture decision on 2026-09-08.

The superseded task attempted to port Mode 2 workflow into Hermes and centered the migration around a Hermes-native Mode 2 plus a Codex Luna specialist route. That is no longer the active direction.

The new direction is to treat Hermes primarily as a thin Brain/orchestrator that can:

- use many low-cost Ollama Cloud models as native execution Workers;
- dispatch bounded work to different already-capable external agents when their own skills, plugins, MCPs, tools, or research workflows provide material value;
- preserve those specialist agents' native environments instead of reimplementing all of their capabilities inside Hermes;
- keep final routing, synthesis, evidence review, and acceptance at the Hermes Brain layer;
- avoid a new scheduler, agent bridge, persistent orchestration runtime, or duplicated Mode 2 runtime.

Do not execute or continue this task. Preserve it only as decision history.

Replacement task:

`foo1maker/instructions/tasks/2026-09-08_audit_hermes_heterogeneous_agent_workers.md`
