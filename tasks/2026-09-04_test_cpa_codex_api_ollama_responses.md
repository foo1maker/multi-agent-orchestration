# Task — Test whether CPA Codex API can use Ollama Cloud Responses upstream directly

## Objective

Determine, with runtime evidence, whether EasyCLIProxyAPI / CLIProxyAPI's **Codex API** provider path can use Ollama Cloud as a direct Responses-compatible upstream and therefore avoid the currently confirmed `Responses -> Chat Completions -> Responses` conversion used by `openai-compatibility`.

This is a bounded compatibility test. Do not redesign CPA, CC Switch, Codex, or Mode 2.

The target question is:

```text
Can CPA Codex API be configured against https://ollama.com/v1 so that a Codex /v1/responses request is forwarded upstream as:

POST https://ollama.com/v1/responses

with no Responses->Chat protocol conversion?
```

## Completion standard

The task is complete only when the answer is supported by actual configuration/source/runtime evidence and one minimal end-to-end test if configuration is safely possible.

A UI label such as `Codex API`, `OpenAI compatible`, or `Responses` is not sufficient evidence.

## Authority and facts to read first

Before changing anything, read the real local state and current governing instructions.

At minimum:

1. `D:\00_SYSTEM\DRIVE_MAP.md` if present.
2. The current applicable global/project `AGENTS.md` files.
3. Current Codex configuration, including `~/.codex/config.toml`.
4. Current CC Switch state/configuration and whether its local proxy is enabled.
5. Current CPA GUI/core configuration and running process/version.
6. `D:\Software\EasyCLIProxyAPI\...` active CPA config and logs/usage DB paths actually in use.
7. The prior protocol diagnosis report if still present:
   `D:\Temp\CodexPendingReports\INBOX_20260904_234641_ccswitch-cpa-ollama-protocol-diagnosis.md`
8. Current upstream provider definitions for the existing Ollama provider, including the provider named `relay_ollama` if it still exists.
9. Current CLIProxyAPI source corresponding exactly to the installed/running binary version, or official source at the exact commit if local source is absent.

Do not assume paths or versions remain unchanged. Verify them.

## Current confirmed starting state to re-verify

The previous diagnosis reported the following. Treat these as a starting hypothesis that must be checked against current live state before execution:

```text
Codex wire_api = responses
Codex base_url = http://127.0.0.1:8317/v1
Port 8317 = CPA / cli-proxy-api.exe
CC Switch local proxy = disabled; CC Switch is configuration writer only
CPA core = CLIProxyAPI 7.2.149, commit 2a6b87ac
Existing provider relay_ollama = openai-compatibility
relay_ollama base-url = https://ollama.com/v1
Existing upstream runtime path = https://ollama.com/v1/chat/completions
CPA OpenAICompatExecutor converts Responses -> Chat Completions for this provider
```

If any of these no longer match current state, record the difference and use the live state.

## Core scientific/engineering question

Distinguish these possibilities explicitly:

### Case A — True Responses-compatible Codex API path

```text
Codex
  -> CPA /v1/responses
  -> CPA Codex API executor/provider
  -> https://ollama.com/v1/responses
  -> Ollama Cloud
```

with:

```text
CPA_INTERNAL_PROTOCOL_CONVERSION = NONE
```

### Case B — Codex-specific path that is not generic Responses-compatible

CPA's `Codex API` provider may require OpenAI/Codex-specific headers, account semantics, model naming, endpoint behavior, auth behavior, response events, or other assumptions that Ollama Cloud does not satisfy.

### Case C — It still converts or targets another endpoint

If `Codex API` does not produce a true `/v1/responses` upstream request, identify what it actually does.

Do not infer the answer from naming alone.

## Scope A — Inspect the Codex API provider implementation before testing

Locate the implementation used by CPA's GUI entry labelled **Codex API** / configuration corresponding to `codex-api-key` or its current equivalent.

For the exact installed version, determine:

1. Which executor handles this provider type.
2. Which upstream endpoint it constructs for normal non-compact Responses requests.
3. Whether the endpoint is hard-coded, derived from inbound endpoint, or configurable.
4. Whether `base-url=https://ollama.com/v1` would produce:
   - `https://ollama.com/v1/responses`
   - another endpoint
   - an invalid path
5. Whether it performs request translation before upstream transmission.
6. Whether it requires Codex/OpenAI-specific headers beyond generic Bearer authentication.
7. Whether it assumes ChatGPT OAuth semantics or whether API-key based third-party Responses-compatible upstreams are intentionally supported.
8. Whether model aliases/mapping are supported and how the upstream model ID is emitted.
9. Whether streaming Responses SSE is passed through or translated.
10. Whether tool calls, reasoning items, finish states, and response item IDs are transformed.

Record exact source file paths, function names, relevant line ranges/commit, and installed binary/version evidence.

If source inspection already proves Ollama Cloud cannot possibly work with this provider, do not force a runtime test. Return `NOT_COMPATIBLE_BY_IMPLEMENTATION` with evidence.

## Scope B — Verify Ollama Cloud's actual Responses contract

Use official Ollama documentation or an already-installed/current client implementation to confirm the current Ollama Cloud API behavior for:

```text
https://ollama.com/v1/responses
```

Confirm at minimum:

- authentication scheme
- model ID format for the exact model under test
- streaming support
- tool calling support if documented
- whether Responses requests accept the fields Codex/CPA will send

Prefer official Ollama documentation. Do not rely on third-party examples if official evidence exists.

Do not expose the API key in logs or the report.

## Scope C — Create an isolated temporary test provider only if implementation supports it

Do **not** modify or replace the existing `relay_ollama` provider.

If Scope A shows that the Codex API provider is plausibly generic Responses-compatible, create a separate temporary CPA provider, for example:

```text
name: ollama_responses_test
provider type: Codex API / codex-api-key equivalent
base URL: https://ollama.com/v1
API key: existing Ollama Cloud key, referenced securely
model: exact existing Ollama Cloud model ID
```

Use the model ID already verified in the current environment. Prefer `glm-5.3-flash` for the first minimal test if it is still available and correctly named. Do not invent a new model ID.

Do not make this provider the global default and do not delete or mutate `relay_ollama`.

Before any config write:

- save the current relevant CPA config hash/backup or otherwise ensure deterministic rollback;
- record the exact file changed;
- make only the minimum provider-entry addition needed for this test.

Do not modify Codex, CC Switch, Mode 2, AGENTS.md, skills, or unrelated providers for this step.

## Scope D — Minimal direct CPA test

Test CPA directly first, without involving Mode 2 or a long Codex agent workflow.

Send one minimal Responses request to the CPA inbound endpoint using the temporary provider/model routing required by the current implementation.

The test must answer:

```text
CPA_INBOUND_ENDPOINT
CPA_SELECTED_EXECUTOR
CPA_SELECTED_PROVIDER
CPA_UPSTREAM_URL
CPA_UPSTREAM_PROTOCOL
CPA_REQUEST_TRANSLATION
CPA_RESPONSE_TRANSLATION
HTTP_STATUS
BASIC_RESPONSE_VALID
```

Highest-value runtime evidence is the actual upstream URL observed in CPA logs/errors/tracing.

Required success evidence:

```text
POST https://ollama.com/v1/responses
```

If it instead shows `/chat/completions`, another endpoint, or cannot route to Ollama, record that exactly.

Do not add a packet sniffer or permanent logging infrastructure. Use existing CPA logs/usage DB/debug facilities when sufficient. If temporary runtime-only debug logging is necessary and safe, revert it immediately after the test and prove the persistent config was restored.

## Scope E — Minimal Codex end-to-end test only after Scope D passes

Only if Scope D proves the upstream is truly `/v1/responses` and the minimal response is valid, run one bounded Codex test through the temporary provider.

Use a trivial prompt first, then one minimal tool-call fixture if supported and necessary to test agent compatibility.

Do not use Mode 2, multi-agent orchestration, long-context research, or production project work for this acceptance test.

Record:

```text
CODEX_REQUEST_COMPLETED
STREAM_TERMINATED_NORMALLY
TOOL_CALL_IF_TESTED
TOOL_RESULT_MATCHED
REPEATED_REASONING_LOOP
REPEATED_TOOL_LOOP
CPA_UPSTREAM_URL
```

The purpose is compatibility verification, not performance benchmarking.

## Scope F — Compare against the existing openai-compatibility route

Using already-existing evidence plus at most one equivalent minimal request, compare:

### Existing route

```text
relay_ollama
openai-compatibility
Responses inbound -> Chat Completions upstream
https://ollama.com/v1/chat/completions
```

### Candidate route

```text
ollama_responses_test
Codex API
Responses inbound -> ? upstream
```

Report whether the candidate route actually removes the protocol conversion.

Do not claim that removal of conversion fixes the previously observed GLM/DeepSeek loop unless the bounded Codex test directly supports that conclusion.

## Evidence boundary

Use these labels in the report:

- `VERIFIED`: direct source/config/runtime/log evidence.
- `OBSERVED`: behavior seen in the actual minimal test.
- `INFERRED`: reasonable interpretation not directly proven.
- `UNKNOWN`: not established by this task.

Specifically:

```text
"Codex API means Responses" must not be reported as VERIFIED merely from the UI label.
```

It becomes VERIFIED only if implementation/runtime evidence shows a `/v1/responses` upstream path or otherwise documents the exact supported Responses contract.

## Protected assets / forbidden actions

Do not:

- overwrite or delete `relay_ollama`;
- change the user's existing working CPA provider routes except the isolated test entry;
- make the test provider permanent/default without explicit user approval;
- modify CC Switch routing mode;
- enable CC Switch local proxy;
- modify Mode 2 / `multi-agent-orchestration` functional files;
- modify global/project `AGENTS.md`;
- modify Codex model defaults globally;
- expose API keys, OAuth tokens, bearer tokens, or full secrets in logs/report/Git;
- patch CPA source or rebuild CPA in this task;
- add a new protocol adapter;
- broadly refactor CPA configuration;
- delete historical logs or prior diagnostic reports.

If the Codex API provider is incompatible with Ollama Cloud, stop at the evidence and report it. Do not repair CPA in this task.

## Rollback requirement

This test must leave the environment no worse than before.

If a temporary `ollama_responses_test` provider is added, after collecting evidence:

- remove it unless the user has separately approved keeping it;
- restore any temporary logging/debug setting;
- verify the original `relay_ollama` definition is unchanged;
- verify Codex's previous default/provider configuration is restored if it was temporarily switched for Scope E.

Record before/after hashes or exact config diffs where practical.

## Acceptance criteria

Return `COMPLETED` only if all applicable checks are resolved:

```text
CURRENT_STATE_REVERIFIED: YES
CPA_CODEX_API_IMPLEMENTATION_IDENTIFIED: YES
CPA_CODEX_API_UPSTREAM_ENDPOINT_LOGIC: VERIFIED
OLLAMA_RESPONSES_CONTRACT_CHECKED: YES
EXISTING_RELAY_OLLAMA_CHANGED: NO
UNRELATED_CONFIG_CHANGED: NO
SECRETS_EXPOSED: NO

TEMP_CODEX_API_PROVIDER_CREATED: YES | NOT_NEEDED | NOT_COMPATIBLE_BY_IMPLEMENTATION
CPA_DIRECT_TEST: PASS | FAIL | NOT_RUN
CPA_OLLAMA_UPSTREAM_ENDPOINT: <exact URL or N/A>
CPA_INTERNAL_PROTOCOL_CONVERSION: NONE | <exact conversion> | UNKNOWN
OLLAMA_UPSTREAM_PROTOCOL: RESPONSES | CHAT_COMPLETIONS | OTHER | UNKNOWN

CODEX_E2E_TEST: PASS | FAIL | NOT_RUN
CODEX_LOOP_OBSERVED: YES | NO | NOT_TESTED

TEMP_CONFIG_ROLLED_BACK: YES | NOT_APPLICABLE
ORIGINAL_RELAY_OLLAMA_PRESERVED: YES
```

## Decision logic

### If true Responses upstream works

Report:

```text
CPA_CODEX_API_OLLAMA_RESPONSES: COMPATIBLE_OBSERVED
```

and state whether it produced:

```text
Codex -> CPA Responses -> Ollama /v1/responses
```

with no Chat conversion.

Do not automatically migrate the user's production Ollama route. Recommend the smallest next action only.

### If source permits it but runtime fails

Report:

```text
CPA_CODEX_API_OLLAMA_RESPONSES: IMPLEMENTATION_PLAUSIBLE_RUNTIME_FAILED
```

and classify the actual failure: auth, endpoint, headers, model, request schema, streaming, response event, tool calling, or other.

### If Codex API is not generic Responses-compatible

Report:

```text
CPA_CODEX_API_OLLAMA_RESPONSES: NOT_COMPATIBLE_BY_IMPLEMENTATION
```

with exact implementation evidence. Do not attempt a workaround.

## Provenance

Record:

- CPA GUI version
- CLIProxyAPI core version
- CLIProxyAPI commit/build identifier
- running executable path and SHA256 if feasible
- CC Switch version
- Codex CLI version
- Ollama API documentation retrieval date
- relevant config paths and before/after hashes
- source files/functions/commit used for protocol determination
- exact timestamps of runtime tests
- sanitized upstream endpoint logs

## GitHub / reporting

This task file is the formal execution specification. Do not rewrite it during execution except to mark it superseded in a future distinct decision.

Do not commit secrets or local configuration snapshots containing credentials.

The execution result should be written as a separate factual report in the normal local report/exchange location used by the current environment. Do not modify `SKILL.md` or Mode 2 policy as part of this task.

## Final output format

Return a compact factual report:

```text
TASK_STATUS:

CURRENT_STATE_REVERIFIED:
CPA_GUI_VERSION:
CPA_CORE_VERSION:
CPA_CORE_COMMIT:
CC_SWITCH_VERSION:
CODEX_VERSION:

CPA_CODEX_API_PROVIDER_IMPLEMENTATION:
CPA_CODEX_API_EXPECTED_UPSTREAM_ENDPOINT:
CPA_CODEX_API_REQUEST_TRANSLATION:
CPA_CODEX_API_RESPONSE_TRANSLATION:

OLLAMA_RESPONSES_OFFICIAL_SUPPORT:
OLLAMA_TEST_MODEL:

TEMP_CODEX_API_PROVIDER_CREATED:
CPA_DIRECT_TEST:
CPA_OLLAMA_UPSTREAM_ENDPOINT:
OLLAMA_UPSTREAM_PROTOCOL:
CPA_INTERNAL_PROTOCOL_CONVERSION:

CODEX_E2E_TEST:
CODEX_LOOP_OBSERVED:

EXISTING_RELAY_OLLAMA_CHANGED:
TEMP_CONFIG_ROLLED_BACK:
UNRELATED_CONFIG_CHANGED:
SECRETS_EXPOSED:

CPA_CODEX_API_OLLAMA_RESPONSES:
STRONGEST_EVIDENCE:
EVIDENCE_BOUNDARY:
KNOWN_LIMITATIONS:
NEXT_MINIMAL_ACTION:
```

## Stop conditions

Stop and report rather than expanding scope if:

- the applicable `AGENTS.md` forbids the required temporary provider/config change;
- the active CPA config cannot be unambiguously identified;
- the running binary/version differs from the source being inspected and exact matching source cannot be obtained;
- safe rollback cannot be guaranteed;
- using Codex API would require patching/rebuilding CPA;
- validating it would require modifying unrelated Codex/CC Switch/Mode 2 configuration;
- secrets would need to be exposed or committed.
