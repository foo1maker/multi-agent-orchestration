# Task: port Mode 2 workflow to Hermes-native orchestration and add a Codex Luna specialist route

## Objective

Advance the current Hermes pilot from a blank/default installation into a minimally customized primary Brain that can reuse the valuable workflow logic already developed in Mode 2 without duplicating Codex-specific runtime orchestration.

The target architecture is:

```text
Hermes Brain
├─ Hermes native delegate_task workers
│  └─ inexpensive / parallel model workers as configured by Hermes
└─ Codex specialist worker
   └─ GPT-5.6 Luna through the real OpenAI/Codex provider path
      + existing Codex AGENTS.md / skills / plugins / MCP / project workflow
```

This task is not a full migration away from Codex. It is the first controlled migration step:

1. preserve the current Codex Mode 2 source and installed Codex behavior;
2. create a Hermes-native variant of the orchestration workflow that keeps the valuable Brain/Worker contract, scientific judgment, validation, QC, provenance, and anti-duplication rules;
3. remove Codex-specific `spawn_agent` / `wait_agent` / V1 lifecycle assumptions from the Hermes variant and use Hermes native delegation instead;
4. create a minimal Hermes route for using Codex as an external specialist Worker, pinned to GPT-5.6 Luna for that invocation only;
5. verify the result with bounded live smokes before making Hermes the default Brain.

Do not modify Codex `AGENTS.md` in this task. The user's current intent is to keep the official/current Codex AGENTS rules unchanged while Hermes orchestration is evaluated.

---

## Authoritative repository and execution locator

- Repo: `foo1maker/multi-agent-orchestration`
- Worktree: `D:\Github\multi-agent-orchestration`
- Branch: `main`
- Current authoritative Codex Mode 2 source: repository root `SKILL.md` + `references/` + `config/`
- Current installed shared Codex skill payload: `C:\Users\1\.agents\skills\multi-agent-orchestration`

Known verified repository state from the latest reconciliation report:

- `C:\Users\1\.agents\skills` is a junction to `C:\Users\1\.codex\skills`.
- The installed Codex Mode 2 payload was reconciled to repository source and matched hashes.
- Do not place Hermes-only skills into this shared `.agents/.codex` skill tree unless the audit proves that doing so cannot pollute Codex routing.

Treat the real filesystem and current live tool schemas as authoritative over this task's known-state notes.

---

## Must read before any modification

### Repository / Mode 2

Read at minimum:

- `SKILL.md`
- `references/task_contract.md`
- `references/lifecycle_and_recovery.md`
- `references/result_packet.md`
- `config/worker_defaults.yaml`
- `reports/INBOX_20260908_reconcile_installed_mode2_skill_and_sync.md`

Identify explicitly which rules are:

- host-neutral workflow / reasoning policy worth preserving;
- Codex-only lifecycle/runtime policy that must not be copied into Hermes;
- obsolete or redundant under Hermes native delegation.

### Live Hermes state

Inspect the real installed Hermes environment before deciding any path. Record:

- Hermes Desktop/CLI version;
- actual `HERMES_HOME` / config path on this Windows host;
- `config.yaml` relevant sections;
- current local Hermes skill directory;
- current `skills.external_dirs` values;
- how Hermes currently sees `multi-agent-orchestration`: local copied skill, imported skill, external/shared skill, or another mechanism;
- whether a local Hermes skill with the same `name` shadows an external skill on this installed version;
- live `delegate_task` schema and actual supported model-routing fields;
- current delegation limits/configuration;
- bundled Codex skill path/content currently installed by Hermes.

Use current official Hermes documentation only as supporting evidence and verify behavior against the live installation. In particular, do not assume per-task model override exists merely because an earlier test report claimed it: inspect the live schema. Current official docs may describe `delegation.model` as a global child-model pin; live installed behavior wins.

### Live Codex state

Read-only inspect:

- Codex CLI version;
- `codex --help` / relevant exec/config help;
- current `~/.codex/config.toml` provider/model routing needed to understand safe per-run override;
- current global/project `AGENTS.md` locations and scope;
- available model catalog or other authoritative live evidence for the exact GPT-5.6 Luna model identifier;
- the current OpenAI/Codex provider/auth route that works without editing global configuration.

Do not modify Codex global config, AGENTS.md, OAuth state, plugin installation, CPA, or the current default provider/model.

---

## Core questions Brain must answer before implementation

1. What is the smallest Hermes-native replacement for the orchestration part of Mode 2?
2. Which Mode 2 rules remain valuable independent of Codex runtime?
3. Which rules must be removed because Hermes owns delegation lifecycle natively?
4. How should Hermes shadow or avoid the Codex-specific `multi-agent-orchestration` skill without modifying the shared Codex copy?
5. Can the same user-facing Mode 2 trigger be preserved in Hermes safely through a Hermes-local skill that shadows the external Codex skill, or is a distinct Hermes skill name safer on the live version?
6. What exact command/config override reliably launches a Codex specialist Worker using GPT-5.6 Luna through the real OpenAI/Codex provider for that run only?
7. Can that external Codex Worker still read the target repo's AGENTS.md and use the already-installed Codex Skills / Plugins / MCP without Hermes reimplementing them?
8. What minimal completion contract is needed so Hermes can accept Codex output and terminate a lingering `codex exec` process without building a watchdog/runtime?

Do not preselect an answer where the live installation contradicts it.

---

## Required architecture boundaries

### Hermes Brain owns

- understanding the user's objective;
- scientific / architectural judgment;
- deciding whether delegation has value;
- selecting native Hermes Worker vs Codex specialist Worker;
- writing a scoped Worker contract instead of forwarding the raw user prompt;
- integrating evidence;
- conflict handling;
- final validation and acceptance.

### Hermes native Worker owns

- bounded execution / search / analysis specified by its Worker contract;
- returning evidence and limitations;
- no project-level final scientific decision.

Use Hermes native `delegate_task` and native lifecycle. Do not recreate Codex `spawn_agent` / `wait_agent` semantics in prompt rules.

### Codex specialist Worker owns

- execution that materially benefits from existing Codex ecosystem assets, including project AGENTS.md, Codex Skills, Plugins/apps, MCP, GitHub/Drive/project workflows, local coding and reproducibility workflows;
- reading its own real environment after launch;
- completing the scoped contract and returning a concise evidence-bearing result.

Codex is not automatically selected because a task is merely difficult. Prefer Codex when the task needs Codex-specific ecosystem capability.

By default, Hermes should launch one Codex specialist process. Do not explicitly trigger nested Mode 2 inside Codex unless the task independently requires it and Brain can justify the extra orchestration layer.

---

## Phase 0 — audit and decision record

Before edits, produce a concise audit table:

```text
RULE / CAPABILITY
CURRENT CODEX MODE2 LOCATION
HOST-NEUTRAL OR CODEX-SPECIFIC
HERMES NATIVE EQUIVALENT
KEEP / ADAPT / DROP
RATIONALE
```

At minimum classify:

- delegation decision rules;
- Brain must not repeat delegated execution;
- Worker contract schema;
- DISCOVERY / EXECUTION / ANALYSIS / REVIEW semantics;
- scientific judgment ownership;
- result packet / evidence requirements;
- Stage 2 validation / final acceptance;
- lifecycle waiting/recovery;
- unsupported-call handling;
- worker model routing;
- clean-context/fork rules;
- polling/watchdog prohibitions;
- nested delegation rules.

Also document the exact current Hermes skill discovery route for Mode 2 and whether shadowing is safe.

If the current Hermes install cannot isolate a Hermes-specific variant from the Codex shared skill without modifying the Codex copy, stop and report the smallest safe alternative. Do not overwrite the shared Codex skill to make Hermes work.

---

## Phase 1 — implement the Hermes-native workflow skill

After Phase 0 only, implement the smallest maintainable Hermes-specific workflow representation.

Preferred design if live behavior supports it:

- keep repository root `SKILL.md` and current Codex Mode 2 payload unchanged;
- add a clearly separated Hermes-specific source subtree in this repository, for example under `hermes/` or another self-explanatory path;
- install/sync the Hermes-specific variant only into Hermes' own local skill directory, not `.agents/.codex`;
- if safe local-name shadowing is verified, preserving the user-facing `multi-agent-orchestration` / Mode 2 trigger is acceptable; otherwise use a distinct Hermes-native skill name and document the trigger change.

The Hermes variant should retain only useful workflow policy, including as applicable:

- Brain thinks / delegates / validates;
- delegate only when delegation adds value;
- never raw-forward the user's long prompt;
- Brain-authored bounded Worker contract;
- bounded DISCOVERY for unresolved execution facts;
- scientific judgment remains Brain-owned;
- Worker outputs are evidence, not final project decisions;
- Brain must not duplicate a task already delegated;
- explicit scope / forbidden actions / deliverables / acceptance;
- evidence/provenance/QC boundaries;
- no runtime scheduler/watchdog/heartbeat/state-machine invention;
- final acceptance belongs to Brain.

Do not copy Codex-specific native tool names or V1 lifecycle/recovery text into the Hermes variant unless a rule is genuinely host-neutral and rewritten without Codex tool identities.

Keep the Hermes skill materially shorter than the current Codex Mode 2 skill unless live evidence demonstrates additional text is required. Prefer deletion and host-native behavior over duplicated policy.

---

## Phase 2 — implement the Codex Luna specialist route

Create the smallest Hermes-side workflow needed to invoke Codex as a specialist Worker.

Requirements:

1. The target semantic model is **GPT-5.6 Luna**.
2. Resolve the exact live Codex CLI model ID from authoritative local/model-catalog evidence; do not guess or alias.
3. Use the real OpenAI/Codex provider/auth path, not CPA/Ollama/custom relay.
4. Pin model/provider for the individual `codex exec` invocation only. Do not edit global `config.toml` defaults.
5. If the live CLI requires a provider override in addition to `--model`, verify the exact valid key/value before using it.
6. If Luna is unavailable on the current authenticated Codex account/CLI, return `BLOCKED`; do not silently substitute Sol, a relay model, or another provider.
7. Launch Codex in the actual target worktree so it can discover that repo's AGENTS.md normally.
8. Do not inject a replacement AGENTS policy from Hermes.
9. Hermes passes a compressed Worker contract, not the parent conversation.
10. Codex should return at minimum:

```text
STATUS
OBJECTIVE_COMPLETED
EVIDENCE
FILES_CHANGED
TESTS / VALIDATION
LIMITATIONS
NEXT_ACTION_IF_BLOCKED
```

11. Establish a simple completion/termination rule for the observed case where Codex prints a complete final answer but its process remains alive. Prefer a bounded process cleanup after a complete final result is captured. Do not build a persistent watchdog, polling loop, or scheduler.

If Hermes already has a bundled Codex skill, prefer a thin wrapper or minimal extension rather than copying the bundled skill wholesale. Do not modify an update-managed bundled file unless there is no safer user-skill mechanism and that conclusion is demonstrated.

---

## Phase 3 — bounded tests

Run targeted tests only. Do not use a real research project write workflow yet.

### Test A — Hermes-native Mode 2 workflow

Use a harmless task that genuinely benefits from two independent Workers.

Acceptance:

- Hermes Brain loads the Hermes-native workflow, not the Codex-specific external version;
- Brain writes scoped contracts;
- native `delegate_task` is used;
- two Workers execute independently;
- Brain does not duplicate their execution;
- Brain waits/receives results through Hermes native behavior;
- Brain performs a real conflict/evidence check before final answer;
- no Codex `spawn_agent` / `wait_agent` policy leaks into the Hermes execution trace.

### Test B — Codex Luna specialist

Hermes launches one Codex specialist Worker on a bounded, read-only task inside a non-critical repo/worktree.

Acceptance:

- effective Codex model is proven as GPT-5.6 Luna from the strongest available runtime evidence;
- provider/auth path is OpenAI/Codex, not CPA/Ollama relay;
- global Codex defaults remain unchanged;
- target repo AGENTS.md is discovered normally;
- at least one existing Codex Skill is visible/usable;
- at least one existing read-only Plugin/MCP/app action is actually exercised if a currently authenticated safe option exists; if none can be exercised without reauthorization, mark `UNKNOWN/CONFIGURED_ONLY` rather than changing auth;
- Codex returns the required result contract;
- Hermes validates the result rather than redoing the task;
- any lingering Codex process is cleaned up with the minimal bounded mechanism.

### Test C — no cross-host pollution

Prove:

- original repository-root Codex Mode 2 payload is unchanged unless an independently justified host-neutral bug was found;
- `C:\Users\1\.agents\skills\multi-agent-orchestration` remains the current Codex payload and was not replaced by Hermes-specific rules;
- Hermes-specific skill source/install is isolated from the shared Codex skill tree;
- Codex can still load its original Mode 2 after the Hermes work.

---

## QC / validation

At minimum:

- run existing Mode 2 source policy audit (`python scripts/audit_policy.py`) before and after;
- hash/compare original Codex skill payload before/after to prove no accidental mutation;
- validate Hermes skill metadata and references using Hermes' own skill discovery/view commands if available;
- inspect actual execution traces for Tests A/B rather than accepting self-reported success;
- distinguish `OBSERVED`, `CONFIGURED_ONLY`, `INFERRED`, and `UNKNOWN` in the report;
- do not claim an effective Worker model solely from requested call arguments if runtime evidence cannot confirm it.

---

## Forbidden scope

Do not:

- modify Codex `AGENTS.md`;
- redesign or delete the existing Codex Mode 2 skill;
- overwrite the shared `.agents/.codex` skill payload with Hermes-specific content;
- modify CPA, OpenCodex, V1/V2 routing, namespace compatibility, port 8317, or Ollama routing;
- migrate every Codex Skill or Plugin into Hermes;
- rewrite Codex Plugins as Hermes Plugins;
- add a custom scheduler, agent bridge, persistent daemon, heartbeat, watchdog, DAG engine, or state database;
- configure nested Hermes → Codex → Mode2 delegation as the default path;
- reauthorize plugins/accounts merely to make a smoke pass;
- delete historical task/report files;
- make unrelated skill cleanup or refactors.

If a needed change falls outside this scope, report it as a follow-up rather than expanding this task.

---

## Provenance / Evidence Boundary

Record:

- exact Hermes version and live config paths;
- exact Codex version and model/provider evidence;
- exact source/install paths and hashes of any skill files changed;
- commands used for each smoke;
- subagent IDs / transcript or manifest paths when Hermes provides them;
- Codex process invocation and result evidence;
- every config/file modified and its rollback path.

Do not interpret requested model names, configured plugin entries, or enumerated MCP resources as proof of actual runtime use. Effective model/plugin/tool claims require runtime evidence; otherwise label them `CONFIGURED_ONLY` or `UNKNOWN`.

---

## Rollback

Before modifying any Hermes local skill/config file:

1. create a timestamped backup under `D:\Temp`;
2. record SHA256 manifest;
3. record exact restore steps;
4. verify the backup before writing.

The Codex Mode 2 source/install must remain rollback-independent because this task should not modify it.

---

## Deliverables

1. Hermes-specific skill source added to this repository only if Phase 0 validates the design.
2. Minimal source for the Codex Luna specialist route if needed.
3. Installation/sync of those Hermes-specific assets into the actual Hermes local profile with verified hashes.
4. A report:

`reports/INBOX_20260908_port_mode2_workflow_to_hermes_native.md`

Report at minimum:

```text
TASK_STATUS:
HERMES_VERSION:
HERMES_HOME:
HERMES_MODE2_SOURCE_BEFORE:
HERMES_SKILL_SHADOWING_VERIFIED:
CODEX_MODE2_SOURCE_CHANGED:
CODEX_INSTALLED_PAYLOAD_CHANGED:
HERMES_NATIVE_SKILL_CREATED:
HERMES_NATIVE_SKILL_PATH:
HERMES_NATIVE_SKILL_LINES:
CODEX_SPECIFIC_RULES_REMOVED:
HOST_NEUTRAL_RULES_PRESERVED:
DELEGATE_TASK_LIVE_SCHEMA:
HERMES_NATIVE_DELEGATION_SMOKE:
CODEX_CLI_VERSION:
LUNA_EXACT_MODEL_ID:
LUNA_PROVIDER_ROUTE:
LUNA_EFFECTIVE_MODEL_EVIDENCE:
CODEX_AGENTS_DISCOVERY:
CODEX_SKILL_SMOKE:
CODEX_PLUGIN_MCP_SMOKE:
CODEX_PROCESS_COMPLETION_BEHAVIOR:
CODEX_PROCESS_CLEANUP_METHOD:
GLOBAL_CODEX_CONFIG_CHANGED:
CODEX_AGENTS_CHANGED:
CPA_CHANGED:
ROLLBACK_DIR:
ROLLBACK_VERIFIED:
FINAL_VERDICT:
NEXT_MINIMAL_ACTION:
```

Use final verdict values:

- `HERMES_PRIMARY_BRAIN_PILOT_READY`
- `PARTIAL`
- `BLOCKED`

---

## Completion criteria

`HERMES_PRIMARY_BRAIN_PILOT_READY` requires all of the following:

1. Hermes has an isolated native orchestration workflow that does not depend on Codex lifecycle tool names.
2. The valuable Mode 2 Brain/Worker contract and validation principles are preserved in a materially simpler Hermes form.
3. Existing Codex Mode 2 source/install remains intact.
4. Hermes native delegation smoke passes without Brain/Worker duplicate execution.
5. Hermes can launch a Codex specialist Worker using verified GPT-5.6 Luna through the OpenAI/Codex route without changing global Codex defaults.
6. That Codex Worker discovers the target AGENTS.md normally and retains meaningful access to existing Codex workflow assets.
7. Hermes validates the Codex result and does not redo the specialist task.
8. No new orchestration runtime/infrastructure layer was introduced.
9. All changes are backed up, documented, committed, and pushed.

If any gate fails, return `PARTIAL` or `BLOCKED` with the exact smallest next action. Do not broaden scope.

---

## Git closeout

- Preserve all historical tasks/reports.
- Commit only intended files.
- Push `main` to `origin`.
- Verify remote `main` contains the final report and any intended Hermes-specific source.
- If the implementation supersedes any Hermes-local imported Mode 2 copy, mark that relationship `SUPERSEDED` in the report; do not mark the authoritative Codex Mode 2 source as superseded.
