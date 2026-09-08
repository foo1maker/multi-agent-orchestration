# Task — Harden Mode 2 fail-fast behavior for unsupported native calls

## Objective

Audit the current `multi-agent-orchestration` skill against the real Codex V1 production evidence from 2026-09-07/08, then make the smallest policy-only change needed to stop Brain from turning a concrete `unsupported call` into repeated tool-name mutation, repeated lifecycle calls, compensatory polling/exec loops, or duplicate Worker creation.

This task is about **Brain policy / skill behavior**, not CPA protocol translation.

Target architecture remains:

```text
Brain thinks
→ Worker executes
→ Brain waits/accepts native completion
→ Brain validates
```

The skill must continue to rely on Codex native lifecycle semantics. Do not build a scheduler, watchdog, retry controller, heartbeat, state machine, alias recovery layer, or side-channel runtime.

## Repository / source of truth

- Repo: `foo1maker/multi-agent-orchestration`
- Worktree: `D:\Github\multi-agent-orchestration`
- Branch: `main`
- Installed copy, if present: `C:\Users\1\.agents\skills\multi-agent-orchestration`

The Git repository is authoritative. Do not edit the installed copy first.

## Required evidence to read before changing anything

Read the real current files; do not rely on memory or old chat summaries:

1. `SKILL.md`
2. `references/lifecycle_and_recovery.md`
3. `references/task_contract.md`
4. `references/result_packet.md`
5. `config/worker_defaults.yaml`
6. `scripts/audit_policy.py`
7. Any current tests or reports in this repository that constrain lifecycle behavior.

Also read the latest production evidence in the instructions worktree if present:

- `D:\Github\instructions\reports\INBOX_20260908_000000_audit_stabilize_production_websearch_loop_after_v1_restore.md`
- `D:\Github\instructions\reports\INBOX_20260907_133313_deploy_validated_v1_exact_namespace_restore_to_production.md`
- the 2026-09-07 wait-agent identity audit report referenced by those reports.

If the exact report filenames have changed, locate the corresponding current reports by title/date. Do not substitute unrelated sessions.

## Known observations to verify, not assume

The latest audit reported all of the following. Re-verify the relevant parts before using them as a basis for edits:

- Production V1 exact dotted namespace restore is deployed and should be kept.
- A real dotted `multi_agent_v1.spawn_agent` call restored and created a real Worker.
- Later model emissions sometimes used bare lifecycle names such as `wait_agent`, `spawn_agent`, `close_agent`, or `send_input`, which Codex rejected as unsupported.
- The affected session then produced repeated unsupported lifecycle calls and large compensatory command bursts.
- `web_search` is a separate typed-tool compatibility gap and is not to be fixed in this task.
- The 2026-09-07 V1 inventory audit reported namespace `multi_agent_v1` children `close_agent`, `resume_agent`, `send_input`, `spawn_agent`, and `wait_agent`; it also reported that `followup_task` was not a V1 namespace child in Codex 0.153.4.

Do not treat the final bullet as permission to mechanically rename `followup_task` to `send_input`. First verify the live/current tool inventory and semantics.

## Phase 1 — Audit the current skill for loop-enabling instructions

Identify every current rule that can cause Brain to keep acting after a concrete native dispatch failure, especially:

- retrying a lifecycle action after `unsupported call`;
- changing between dotted, bare, namespaced, or guessed tool-name forms;
- replacing a failed `wait_agent` with new `spawn_agent` calls when an existing Worker is already confirmed live;
- repeated `close_agent`, `send_input`, `wait_agent`, `list_agents`, or equivalent calls merely to escape an unsupported lifecycle call;
- repeated shell commands, time/date probes, log reads, repo reads, or progress checks merely because a native lifecycle/tool call failed;
- instructions that name tools not actually present in the current V1 live inventory;
- rules that conflate `Wait timed out.` with `unsupported call`;
- rules that authorize broad recovery after a protocol/capability failure without a new decision.

Produce a concise audit table before modification:

```text
LOCATION
CURRENT_RULE
REAL_FAILURE_MODE_IT_CAN_TRIGGER
KEEP / MODIFY / DELETE
WHY
```

Do not change text that is unrelated to the observed loop.

## Phase 2 — Verify current native lifecycle names and semantics

Using the real installed Codex build/config, inspect the live V1 multi-agent tool inventory in an isolated/non-production-safe way.

At minimum determine:

- which V1 lifecycle tools are actually declared;
- whether `followup_task` exists anywhere in the live tool inventory;
- whether `send_input` is the supported native steering equivalent, and if so what its semantics/schema are;
- whether `list_agents` is available and under what identity;
- whether completion notifications can arrive after a successful Worker spawn even when a later explicit wait call is rejected.

Record direct evidence. Do not infer equivalence solely from similar names.

If current Codex differs materially from the 0.153.4 evidence, stop broad modification and report the difference before changing policy.

## Phase 3 — Minimal policy design

Prefer one small fail-fast rule plus only the minimum cleanup required to make existing lifecycle guidance consistent with it.

The intended invariant is:

> A concrete `unsupported call` is a hard capability/dispatch boundary for that attempted tool identity in the current task state. Brain must not keep trying alternate spellings, namespace forms, aliases, or repeated calls for the same semantic action merely to make the runtime accept it.

The final policy must distinguish at least these cases:

### A. Spawn was not confirmed

If `spawn_agent` or the live declared spawn action returns `unsupported call` and no Worker was confirmed:

- treat that spawn as failed;
- do not retry the same semantic spawn under guessed/bare/dotted/renamed identities;
- do not enter wait for a nonexistent Worker;
- do not quietly execute the delegated Worker scope in Brain merely because delegation failed;
- report `BLOCKED` or use an already-defined non-delegated path only when the task/user explicitly permits that fallback.

### B. Worker was already confirmed live

If a Worker was successfully created and a later lifecycle action (`wait`, steering/input, close, etc.) returns `unsupported call`:

- do not create replacement Workers for the same scope;
- do not mutate the tool identity and retry variants;
- do not take over the live Worker scope;
- do not perform compensatory polling or shell activity merely to stay busy;
- consume a native completion notification/result if it arrives;
- if the runtime leaves no safe declared lifecycle action to proceed, stop further orchestration attempts and report the precise degraded/blocked state rather than looping.

### C. `Wait timed out.` remains different

Preserve the existing principle that a normal native wait timeout is not a Worker failure. Do not accidentally turn the new fail-fast rule into a one-shot wait policy.

Only an actual dispatch/capability failure such as `unsupported call: ...` should trigger the new hard boundary.

### D. Non-lifecycle unsupported tools

Within Mode 2, if an unrelated tool such as search returns `unsupported call`:

- do not retry the same unsupported identity repeatedly;
- do not guess aliases or alternate spellings;
- do not launch unrelated command loops merely to compensate;
- continue only with genuinely supported work that still advances the user goal and does not pretend the missing capability succeeded;
- if that capability is required for correctness, report `BLOCKED`/insufficient evidence.

Do **not** implement `web_search` compatibility in this task.

## Phase 4 — Remove stale native-tool assumptions only if verified

The current `SKILL.md` and lifecycle reference contain hard-coded references such as `followup_task`. Audit them against the live V1 tool list.

If a named tool is not declared in the current native V1 environment:

- do not leave policy that instructs Brain to call it;
- do not invent an alias or compatibility wrapper;
- do not mechanically rename it without semantic verification;
- use the actual native supported steering mechanism only where the semantics match;
- otherwise rewrite the rule in terms of the live declared capability or remove the unsupported recovery path.

Keep the change local. Do not rewrite the whole lifecycle policy.

## Allowed modification scope

Prefer modifications only to:

- `SKILL.md`
- `references/lifecycle_and_recovery.md`
- `scripts/audit_policy.py` only if a very small structural regression check is justified
- an existing test file if one already covers lifecycle policy

Do not modify other references unless the audit proves a direct contradiction that would leave the new rule inconsistent.

## Forbidden scope

Do not:

- modify CPA source, binary, config, or port 8317;
- roll back the deployed exact namespace restore;
- implement Ollama `web_search` bridge;
- add short-name guessing;
- add lifecycle aliases or V1/V2 alias families;
- add `spawn_agent`, `wait_agent`, `close_agent`, `send_input`, or model-specific special cases in CPA/runtime;
- add GLM/DeepSeek-specific policy branches unless a model name is already required by existing routing policy and is unrelated to this fix;
- enable V2;
- touch PR #5538;
- add scheduler/watchdog/heartbeat/retry-controller/state-machine code;
- add permanent counters, timer files, progress databases, or side-channel monitoring;
- broadly refactor task-contract/result-packet architecture;
- weaken Brain/Worker separation;
- make Brain perform delegated work after a failed spawn unless an existing explicit fallback contract already permits it.

## Phase 5 — Tests

Before modification, run the current repository policy/tests and record baseline.

After modification, run at minimum:

1. `scripts/audit_policy.py` using the repository's documented invocation.
2. Any existing lifecycle/policy tests.
3. A text search proving no stale unsupported lifecycle name remains in an executable instruction unless it is explicitly documented as historical/non-callable.
4. A text search proving the new rule does not create a custom wait/retry engine.

Then perform targeted behavioral checks with real Codex, bounded to avoid runaway loops:

### Smoke A — normal Mode 2 success path

Use a trivial named-marker task that requires one Worker and returns a tiny deterministic result. Confirm:

- Brain creates the Worker using the native declared spawn tool;
- Brain does not duplicate the Worker scope;
- a successful Worker result is accepted and validated;
- normal successful Mode 2 behavior was not broken by fail-fast wording.

### Smoke B — unsupported-call behavior

Use the safest reproducible method available to present or reproduce a real `unsupported call` lifecycle condition without modifying production CPA.

Acceptance if the condition occurs:

- after the first concrete unsupported dispatch for a semantic lifecycle action, Brain does not try alternate bare/dotted/namespaced names for that same action;
- Brain does not repeatedly spawn replacement Workers for an already-live scope;
- Brain does not enter shell/time/date/log/progress loops to compensate;
- the turn terminates in a precise `BLOCKED`/degraded result or consumes an already-arriving completion notification.

If the provider does not reproduce an unsupported emission during the bounded test, do **not** manufacture a production failure. Mark this behavioral subtest `NOT_REPRODUCED`, retain static/policy evidence, and do not expand scope.

### Boundedness requirement

Any behavioral smoke must have an explicit observation ceiling. Abort the test harness if it exceeds a small fixed number of lifecycle/tool actions or a short bounded duration. This ceiling is for the **test harness only**, not a new production runtime policy.

## Phase 6 — Compare behavior and decide

Compare before/after against the real loop evidence.

The modification is successful only if all are true:

- normal Mode 2 success remains intact;
- policy now treats `unsupported call` as non-retryable for that semantic tool action;
- no alternate-identity guessing is authorized;
- no duplicate Worker replacement is authorized when a live Worker exists;
- no compensatory command/polling loop is authorized;
- wait-timeout behavior remains unchanged;
- stale unsupported native-tool instructions are removed or corrected only where verified;
- no CPA/runtime change was needed;
- repository policy audit passes.

Rollback the skill change if it causes normal successful Mode 2 runs to stop after ordinary `Wait timed out.`, prevents legitimate bounded recovery from settled Worker results, or makes Brain abandon confirmed live Workers merely because they are slow.

## Phase 7 — Sync and publish

Only after tests pass:

1. Commit the minimal source changes in `D:\Github\multi-agent-orchestration`.
2. Push `main` normally; no force push.
3. If the installed copy exists, first compare it against the pre-change repo source. If it was an unmodified mirror, sync only the changed skill files from the tested repo source to `C:\Users\1\.agents\skills\multi-agent-orchestration` and verify hashes. If it contains independent local changes, do not overwrite it; report the conflict.
4. Do not modify unrelated untracked files.

## Required report

Write a concise report under this repository's `reports/` directory and commit/push it with:

```text
TASK_STATUS:
ROOT_CAUSE_POLICY_GAP:
LIVE_V1_TOOL_INVENTORY:
FOLLOWUP_TASK_LIVE_STATUS:
FILES_CHANGED:
FAIL_FAST_RULE_ADDED:
UNSUPPORTED_IDENTITY_GUESSING_ALLOWED: NO
DUPLICATE_WORKER_AFTER_LIFECYCLE_UNSUPPORTED_ALLOWED: NO
COMPENSATORY_POLL_EXEC_LOOP_ALLOWED: NO
WAIT_TIMEOUT_POLICY_CHANGED: NO
WEB_SEARCH_BRIDGE_CHANGED: NO
CPA_CHANGED: NO
PRODUCTION_8317_CHANGED: NO
NORMAL_MODE2_SMOKE:
UNSUPPORTED_CALL_SMOKE:
POLICY_AUDIT:
INSTALLED_COPY_SYNCED:
SOURCE_COMMIT:
REPORT_COMMIT:
ROLLBACK_CONDITION:
NEXT_MINIMAL_ACTION:
```

## Stop conditions

Stop and report instead of broadening the task if:

- the current live V1 tool inventory materially contradicts the latest production audit;
- fixing the behavior would require CPA/runtime code rather than skill policy;
- the only proposed solution is alias guessing or repeated retries;
- the installed skill copy has independent edits that would be overwritten;
- unrelated tests fail and cannot be shown to pre-exist;
- a clean minimal change cannot be isolated to the Mode 2 lifecycle policy.

Do not start the separate Ollama `web_search` bridge task in this task. That decision comes only after Mode 2 fail-fast behavior is independently validated.
