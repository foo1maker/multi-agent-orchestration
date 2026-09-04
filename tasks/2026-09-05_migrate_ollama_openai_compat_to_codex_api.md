# Task — Migrate Ollama Cloud in CPA from OpenAI compatibility to Codex API / Responses

## Execution locator

- GitHub repo: `foo1maker/multi-agent-orchestration`
- Local worktree: `D:\Github\multi-agent-orchestration`
- Branch: `main`
- Task file: `tasks/2026-09-05_migrate_ollama_openai_compat_to_codex_api.md`

Do not rediscover the repository or task path unless one of these exact locators fails after `git fetch` / `git pull --ff-only`.

## Objective

Replace the current active Ollama Cloud CPA route that uses `openai-compatibility` / Chat Completions with the already-tested CPA **Codex API / `codex-api-key`** route so Codex reaches Ollama Cloud through native Responses:

```text
BEFORE
Codex -> CPA /v1/responses -> Responses→Chat conversion -> https://ollama.com/v1/chat/completions

AFTER
Codex -> CPA /v1/responses -> CodexExecutor -> https://ollama.com/v1/responses
```

This is a production configuration migration, not another feasibility test. Use the smallest config-only change that preserves current model names/aliases and existing Codex/CC Switch behavior.

## Completion standard

The migration is complete only when:

1. the current Ollama provider is no longer active under `openai-compatibility`;
2. the equivalent provider is active under CPA `Codex API` / `codex-api-key` using the exact current CPA schema;
3. the upstream base URL remains `https://ollama.com/v1` — **do not append `/responses` to the configured base URL**;
4. the current Ollama models/aliases remain usable, including the currently configured `glm-5.3-flash` and `deepseek-v4-flash:0731` if they still exist in live config;
5. real runtime evidence shows migrated requests go to `POST https://ollama.com/v1/responses`;
6. no migrated request is sent to `https://ollama.com/v1/chat/completions`;
7. bounded Codex response/tool-call smoke tests pass and terminate normally;
8. unrelated CPA providers, Codex config, CC Switch routing mode, Mode 2 files, skills, agents, and AGENTS.md remain unchanged.

If any required acceptance check fails, restore the original CPA config byte-for-byte and report `ROLLED_BACK` rather than leaving a half-migrated state.

## Must read / authority before writing

Read the real live state first. At minimum:

1. `D:\00_SYSTEM\DRIVE_MAP.md` if present.
2. Applicable global/project `AGENTS.md` files.
3. `D:\Github\multi-agent-orchestration\tasks\2026-09-04_test_cpa_codex_api_ollama_responses.md`.
4. The prior protocol diagnosis report if present:
   `D:\Temp\CodexPendingReports\INBOX_20260904_234641_ccswitch-cpa-ollama-protocol-diagnosis.md`.
5. The successful Responses compatibility report if present:
   `D:\Temp\CodexPendingReports\INBOX_20260905_001200_cpa_codex_api_ollama_responses_test.md`.
6. Current active CPA config, running CPA process/core version, and exact config path in use.
7. Current Codex config (`~/.codex/config.toml`) and CC Switch state only to verify they still match the known topology; do not modify them unless an actual incompatibility is proven and this task explicitly permits it. This task currently does **not** permit such expansion.
8. Exact CPA 7.2.149 / current-running-version schema/source for `codex-api-key` if the running version changed or the config syntax cannot be recovered from the successful temporary provider test.

Priority: live config/runtime > exact-version source > prior reports > task starting assumptions.

## Confirmed starting evidence to re-verify

Previous work established:

```text
CPA GUI: EasyCLIProxyAPI 0.2.71
CPA core: CLIProxyAPI 7.2.149, commit 2a6b87ac
Codex: wire_api="responses"
Codex base_url: http://127.0.0.1:8317/v1
CC Switch local proxy: disabled; CC Switch is config writer only
Existing Ollama provider: relay_ollama under openai-compatibility
Existing Ollama base-url: https://ollama.com/v1
Existing upstream: https://ollama.com/v1/chat/completions
OpenAICompatExecutor: Responses -> Chat Completions translation
Codex API / codex-api-key test: COMPATIBLE_OBSERVED
CodexExecutor test upstream: https://ollama.com/v1/responses
Minimal response + streaming + tool-call E2E: PASS
```

Re-verify these facts. If live state differs, stop treating the stale value as authoritative and record the difference.

## Core change

Migrate the existing Ollama Cloud provider semantics from:

```text
provider family: openai-compatibility
provider: relay_ollama
base-url: https://ollama.com/v1
upstream protocol: Chat Completions
```

to the exact current CPA `Codex API` / `codex-api-key` schema proven by the successful temporary test:

```text
provider family: codex-api-key (or exact current equivalent)
base-url: https://ollama.com/v1
upstream protocol: Responses
```

Preserve, as far as the CPA schema permits without changing behavior:

- current model IDs;
- current model aliases presented to Codex;
- current Ollama Cloud API key/credential reference;
- direct/no-proxy behavior unless live config says otherwise;
- all unrelated providers and settings.

Prefer preserving the externally visible provider/model naming needed by current Codex and CC Switch configuration so they do not require changes.

Do not guess the YAML shape. Use the exact schema and syntax from the running version and the already-successful temporary `codex-api-key` provider test.

## Migration procedure and safeguards

### 1. Pre-change snapshot

Before editing:

- identify the single active CPA config file;
- save a local rollback copy outside Git-tracked repos;
- record SHA256 of the active config;
- record the exact existing `relay_ollama` definition in a secret-safe manner;
- record CPA process/version and current `/v1/models` output relevant to the Ollama aliases;
- confirm CPA is healthy before migration.

Do not copy API keys into reports or GitHub.

### 2. Build the replacement from verified syntax

Use the exact successful `codex-api-key` configuration shape from the prior test/current version.

The configured base URL must be:

```text
https://ollama.com/v1
```

not:

```text
https://ollama.com/v1/responses
```

because `CodexExecutor` appends `/responses`.

Migrate all currently intended Ollama models in the active provider. Re-verify exact IDs from live config; do not invent or rename models.

### 3. Atomic/minimal switch

Make the smallest edit needed so there is one unambiguous active Ollama route for the migrated model aliases.

After the replacement is valid, remove the old active `relay_ollama` entry from `openai-compatibility` so Codex cannot continue routing those aliases through Chat Completions by accident.

Do not leave two active providers exposing the same model aliases unless the CPA routing implementation requires a short transient overlap during validation. If transient overlap is required, remove it immediately after validation.

Historical task/report evidence is sufficient for the old route; do not keep a dead duplicate in active config solely for history.

### 4. Reload/validation

Use CPA's normal config reload/restart behavior. Do not patch or rebuild CPA.

Verify:

- config parses successfully;
- CPA remains healthy/listening on the expected port;
- migrated models appear as expected via CPA model discovery/listing;
- unrelated providers remain present;
- Codex can select/use the same expected model aliases without changing `~/.codex/config.toml`.

If reload fails or model aliases disappear unexpectedly, restore the backup immediately before further investigation.

## Runtime acceptance

Use bounded tests only. Do not run Mode 2 or broad workloads unless needed for the historical loop fixture described below.

### A. GLM smoke test

For `glm-5.3-flash` if still configured:

1. one minimal normal response;
2. one minimal tool-call roundtrip;
3. confirm normal stream termination;
4. confirm tool result is matched once and not repeated.

### B. DeepSeek smoke test

For `deepseek-v4-flash:0731` if still configured:

1. one minimal normal response;
2. one minimal tool-call roundtrip;
3. confirm normal stream termination;
4. confirm tool result is matched once and not repeated.

If either model is no longer present in live config, do not recreate it; report that fact and test the models that are actually present.

### C. Upstream protocol proof

Temporarily use existing safe CPA request logging/usage evidence only as needed, then restore logging settings.

For migrated model requests, prove:

```text
POST https://ollama.com/v1/responses
```

and verify no corresponding migrated request used:

```text
POST https://ollama.com/v1/chat/completions
```

The final verdict must be based on runtime evidence, not the provider label.

### D. Historical loop regression — bounded

If an existing minimal fixture/test command from the prior GLM/DeepSeek Codex loop investigation is available, run one bounded instance per available migrated model using that existing fixture.

Do not create a new large benchmark or long stress harness in this task.

Record only:

```text
COMPLETED_NORMALLY
REPEATED_REASONING_LOOP
REPEATED_TOOL_LOOP
RETRY/TRANSPORT_ERROR
```

The migration does not require proving that all historical looping is permanently solved. It does require showing that the new production route passes bounded normal Codex agent behavior.

## Evidence boundary

Use:

- `VERIFIED`: config/source/log directly proves it.
- `OBSERVED`: actual runtime behavior in this migration.
- `INFERRED`: reasonable interpretation.
- `UNKNOWN`: not established.

Do not claim:

```text
"Chat Completions was the sole cause of all previous loops"
```

unless a controlled historical reproduction proves it. The required production conclusion is narrower:

```text
The active Ollama CPA route now uses Responses upstream and no longer performs Responses→Chat protocol conversion.
```

## Forbidden changes

Do not:

- modify `D:\Github\multi-agent-orchestration\SKILL.md` or its references;
- modify Mode 2 behavior/model-routing policy;
- enable CC Switch local proxy;
- modify CC Switch provider/routing configuration unless the existing aliases cannot work after migration — if that occurs, stop and report instead of expanding scope;
- modify `~/.codex/config.toml` unless this task is explicitly re-authorized after a demonstrated need;
- patch/rebuild CPA;
- change Ollama model IDs without live evidence;
- add temperature/body/header overrides as a workaround;
- expose or duplicate secrets;
- delete unrelated providers/logs/configs;
- refactor the overall proxy architecture.

## Rollback

If any of the following occurs, restore the original CPA config from the pre-change backup and verify its original SHA256/semantic state:

- config invalid/reload failure;
- migrated models cannot be routed;
- `/v1/responses` upstream fails for a model that previously passed the compatibility test and the failure cannot be attributed to a transient transport issue with one bounded retry;
- tool-call roundtrip is broken;
- unrelated provider regression;
- safe secret handling cannot be maintained.

After rollback, return `ROLLED_BACK` and exact evidence. Do not leave partial edits.

## Acceptance criteria

Report `COMPLETED` only if all applicable items are true:

```text
CURRENT_STATE_REVERIFIED: YES
PRECHANGE_CONFIG_SHA256: <hash>
CPA_CONFIG_SCHEMA_VALID: YES
CPA_HEALTH_AFTER_MIGRATION: PASS

OLD_OLLAMA_PROVIDER_FAMILY: openai-compatibility
NEW_OLLAMA_PROVIDER_FAMILY: codex-api-key | <exact equivalent>
OLLAMA_BASE_URL: https://ollama.com/v1
OLD_OPENAI_COMPAT_OLLAMA_ACTIVE: NO

GLM_MODEL_PRESERVED: YES | NOT_PRESENT
DEEPSEEK_MODEL_PRESERVED: YES | NOT_PRESENT
MODEL_ALIASES_PRESERVED: YES

GLM_BASIC_RESPONSE: PASS | NOT_PRESENT
GLM_TOOL_CALL: PASS | NOT_PRESENT
DEEPSEEK_BASIC_RESPONSE: PASS | NOT_PRESENT
DEEPSEEK_TOOL_CALL: PASS | NOT_PRESENT

CPA_OLLAMA_UPSTREAM_ENDPOINT: https://ollama.com/v1/responses
CPA_INTERNAL_PROTOCOL_CONVERSION: NONE_CROSS_PROTOCOL
CHAT_COMPLETIONS_USED_FOR_MIGRATED_OLLAMA: NO

HISTORICAL_LOOP_FIXTURE_GLM: PASS | LOOP | NOT_AVAILABLE | NOT_PRESENT
HISTORICAL_LOOP_FIXTURE_DEEPSEEK: PASS | LOOP | NOT_AVAILABLE | NOT_PRESENT

CC_SWITCH_CONFIG_CHANGED: NO
CODEX_CONFIG_CHANGED: NO
MODE2_FILES_CHANGED: NO
AGENTS_CHANGED: NO
UNRELATED_CPA_PROVIDERS_CHANGED: NO
SECRETS_EXPOSED: NO
ROLLBACK_REQUIRED: NO
```

If the migration cannot meet these criteria, restore the old route and report `ROLLED_BACK` or `BLOCKED` with the narrowest cause.

## Provenance / report

Record:

- CPA GUI/core version and core commit/build identifier;
- active CPA executable/config paths;
- pre/post config SHA256;
- sanitized diff of only the migrated provider definition;
- model IDs/aliases before and after;
- exact timestamps of smoke tests;
- sanitized runtime proof of upstream `/v1/responses`;
- whether any `/v1/chat/completions` request occurred for migrated models after the switch;
- any historical loop fixture result;
- final rollback status.

Write the factual execution report to the current normal local report/exchange location. Do not commit secrets or raw config snapshots containing credentials.

## Final output

Return a compact factual report:

```text
TASK_STATUS:

CPA_GUI_VERSION:
CPA_CORE_VERSION:
CPA_CORE_COMMIT:
PRECHANGE_CONFIG_SHA256:
POSTCHANGE_CONFIG_SHA256:

OLD_OLLAMA_PROVIDER_FAMILY:
NEW_OLLAMA_PROVIDER_FAMILY:
OLD_OPENAI_COMPAT_OLLAMA_ACTIVE:
OLLAMA_BASE_URL:

GLM_MODEL_PRESERVED:
DEEPSEEK_MODEL_PRESERVED:
MODEL_ALIASES_PRESERVED:

GLM_BASIC_RESPONSE:
GLM_TOOL_CALL:
DEEPSEEK_BASIC_RESPONSE:
DEEPSEEK_TOOL_CALL:

CPA_OLLAMA_UPSTREAM_ENDPOINT:
CPA_INTERNAL_PROTOCOL_CONVERSION:
CHAT_COMPLETIONS_USED_FOR_MIGRATED_OLLAMA:

HISTORICAL_LOOP_FIXTURE_GLM:
HISTORICAL_LOOP_FIXTURE_DEEPSEEK:

CC_SWITCH_CONFIG_CHANGED:
CODEX_CONFIG_CHANGED:
MODE2_FILES_CHANGED:
AGENTS_CHANGED:
UNRELATED_CPA_PROVIDERS_CHANGED:
SECRETS_EXPOSED:
ROLLBACK_REQUIRED:

STRONGEST_EVIDENCE:
EVIDENCE_BOUNDARY:
KNOWN_LIMITATIONS:
NEXT_MINIMAL_ACTION:
```

## Stop conditions

Stop and report instead of broadening scope if:

- the live CPA config/provider no longer matches the intended Ollama route and the correct target cannot be identified unambiguously;
- the applicable AGENTS.md forbids the required config migration;
- current CPA version/schema differs from the tested version and exact syntax cannot be established safely;
- preserving existing model aliases would require unrelated Codex/CC Switch changes;
- the migration would require code changes rather than config changes;
- safe deterministic rollback cannot be guaranteed.
