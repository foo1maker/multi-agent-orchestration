# Status

COMPLETE — Mode 2 Brain policy now fail-fasts on a concrete `unsupported call` without guessing tool identities, respawning a live scope, or filling wait with shell/time/log loops. Current V1 live inventory was re-verified against Codex 0.153.4. `followup_task` / `list_agents` / `interrupt_agent` are not live V1 tools; steering uses live `send_input` after schema/semantics verification, not a mechanical rename. Normal named-marker Mode 2 smoke passed. Unsupported wait/close occurred in the same bounded run and did not loop. Installed copy was not overwritten: it has independent local edits.

Repo: `foo1maker/multi-agent-orchestration`
Worktree: `D:\Github\multi-agent-orchestration`
Branch: `main`
Task path: `tasks/2026-09-08_fail_fast_unsupported_calls_and_native_lifecycle.md`
Locator commit: `dd6d056b19350d9c377822f4752673b4ad9f51e4`

```text
TASK_STATUS: COMPLETE
ROOT_CAUSE_POLICY_GAP: Skill instructed Brain to keep acting after native dispatch failure (retry/guess lifecycle names, respawn same scope, compensatory exec) and named undeclared V1 tools (`followup_task`, `list_agents`, `interrupt_agent`) as callable
LIVE_V1_TOOL_INVENTORY: namespace multi_agent_v1 children close_agent, resume_agent, send_input, spawn_agent, wait_agent; top-level exec_command, write_stdin, request_user_input, view_image, get_goal, create_goal, update_goal; typed web_search. Codex 0.153.4 binary 8e5b6932251c2c1c; features.multi_agent_v2.enabled=false. Matches 2026-09-07/08 production audits; no material inventory contradiction
FOLLOWUP_TASK_LIVE_STATUS: ABSENT from live V1 tools[] (not a namespace child, not a top-level function). Binary still contains the string. send_input is the live steering tool (required target; message/items; optional interrupt) — used only where semantics match, not as a renamed alias
FILES_CHANGED: SKILL.md; references/lifecycle_and_recovery.md; scripts/audit_policy.py; reports/INBOX_20260908_fail_fast_unsupported_calls_and_native_lifecycle.md
FAIL_FAST_RULE_ADDED: YES — concrete unsupported call is a hard capability/dispatch boundary (cases A spawn-unconfirmed, B worker-live, C Wait timed out remains different, D non-lifecycle)
UNSUPPORTED_IDENTITY_GUESSING_ALLOWED: NO
DUPLICATE_WORKER_AFTER_LIFECYCLE_UNSUPPORTED_ALLOWED: NO
COMPENSATORY_POLL_EXEC_LOOP_ALLOWED: NO
WAIT_TIMEOUT_POLICY_CHANGED: NO
WEB_SEARCH_BRIDGE_CHANGED: NO
CPA_CHANGED: NO
PRODUCTION_8317_CHANGED: NO
NORMAL_MODE2_SMOKE: PASS (session 01a07e7f-f527-7062-a2c3-6728612dfc2b; worker 01a07e80-2abd-7ac0-b7e3-d936f477e3b8; marker FAILFAST_SMOKE_OK_R7K2 exact 22 bytes; Brain reply SMOKE_OK FAILFAST_SMOKE_OK_R7K2; one Worker; Brain did not write the marker)
UNSUPPORTED_CALL_SMOKE: PASS (same bounded run: unsupported call: wait_agent x1, unsupported call: close_agent x1; no wait_agent/close_agent retry; no replacement spawn; no Get-Date; completion consumed; turn ended)
POLICY_AUDIT: PASS (python scripts/audit_policy.py)
INSTALLED_COPY_SYNCED: NO — conflict; independent local edits in C:\Users\1\.agents\skills\multi-agent-orchestration (SKILL.md has DSFlash and no worker_defaults.yaml path, does not match any git SKILL.md commit; audit_policy.py and task_contract.md also differ; config/ absent). lifecycle_and_recovery.md was an unmodified mirror pre-change, but the copy as a whole is not. Per task rule, did not overwrite
SOURCE_COMMIT: 3da84aa22bffcab404b01adf374578c5f25b36ff
REPORT_COMMIT: a26bb53334b89e17934e662ed49fe36d32aabaff
ROLLBACK_CONDITION: Roll back the skill change if normal Mode 2 stops after ordinary Wait timed out., if settled Worker results can no longer be consumed, or if Brain abandons confirmed live Workers merely because they are slow
NEXT_MINIMAL_ACTION: Do not overwrite the installed copy until the independent SKILL.md/audit_policy.py/task_contract.md edits are reconciled. web_search typed-tool mismatch remains a separate task; do not start that bridge from this report
```

# Phase 1 — audit table (pre-change)

```text
LOCATION
CURRENT_RULE
REAL_FAILURE_MODE_IT_CAN_TRIGGER
KEEP / MODIFY / DELETE
WHY

SKILL.md Before First Spawn
Use Codex native spawn_agent, wait_agent, and followup_task
Instructs an undeclared V1 name; first followup_task → unsupported call → identity guessing
MODIFY
followup_task is not in live V1 tools[]

SKILL.md Operating Boundaries
empty-set list_agents check; two-timeout list_agents audit
list_agents undeclared → unsupported call loop
MODIFY
remove undeclared listing; keep wait-timeout ≠ failure

SKILL.md
no unsupported-call hard boundary
observed production loop after wait/close/send unsupported
MODIFY
add fail-fast pointer

lifecycle Native Wait / Spawn Confirmation
Wait timed out. → immediately wait_agent again
none if kept distinct from unsupported call
KEEP
must not become one-shot wait

lifecycle Spawn Confirmation
if every spawn failed, correct contracts and re-spawn
Case A violation if spawn itself was unsupported call
MODIFY
re-spawn only for contract/effort failure

lifecycle wrapper rejection → individual spawn_agent
misread as permission to mutate spawn identity
KEEP + qualify
wrapper rejection ≠ unsupported spawn identity

lifecycle Empty-Set Audit
after two timeouts call list_agents once
undeclared tool; not in the observed loop but executable
DELETE
no live listing tool; notifications remain the completion path

lifecycle Five-Minute Output Check / Recovery
followup_task to steer a live Worker
undeclared name → unsupported then guess
MODIFY
live send_input matches steer-existing-agent semantics; not a rename alias

lifecycle interrupt_agent + list_agents confirm death
undeclared interrupt_agent and list_agents
MODIFY
live close_agent for shutdown; close result not a listing tool

task_contract.md / result_packet.md / worker_defaults.yaml
no lifecycle dispatch loop rules
none for this failure
KEEP
out of observed-loop scope
```

# Phase 2 — live V1 inventory (direct evidence)

- Installed Codex: `C:\Users\1\AppData\Local\OpenAI\Codex\bin\8e5b6932251c2c1c\codex.exe` → `codex-cli 0.153.4` (same binary as the 2026-09-07/08 captures).
- `features.multi_agent_v2.enabled = false`.
- Same-day outbound capture `reports/evidence/websearch_loop_attribution_20260908/codex_outbound_declared_tools.json` (instructions worktree) and `mode2_v1_unsupported_call_probe/requests/req_000.json`: `tools[]` contains namespace `multi_agent_v1` with children `close_agent`, `resume_agent`, `send_input`, `spawn_agent`, `wait_agent`.
- `followup_task`, `list_agents`, `interrupt_agent`: absent from that `tools[]`. Present only as strings inside the 0.153.4 binary.
- `send_input` schema (live): required `target`; properties `interrupt`, `items`, `message`, `target`. Description: send a message to an existing agent; `interrupt=true` redirects immediately; reuse the agent when the next task depends on prior context. This matches steering, not spawn and not listing.
- `wait_agent` description: returns empty status on timeout; a completion notification is delivered when the agent reaches a final status — so an explicit wait rejection does not prevent consuming a later native completion.
- No material contradiction vs the 0.153.4 production audits; policy change proceeded.

# Phase 5 — tests

Baseline before edit: `python scripts/audit_policy.py` → PASS.

After edit:

1. `python scripts/audit_policy.py` → PASS.
2. Lifecycle policy covered by the same audit (`fail_fast_unsupported` group + forbidden stale executable instructions).
3. Executable-instruction search: remaining `followup_task` / `list_agents` / `interrupt_agent` hits in `SKILL.md` and `lifecycle_and_recovery.md` are explicitly non-callable / historical. README still lists `followup_task` as a host-equivalent in non-runtime docs (out of allowed edit scope).
4. No new scheduler/watchdog/heartbeat/wait_loop/recovery_engine/state-machine files. Existing mentions only forbid those runtimes or forbid timer files.

Behavioral smoke (isolated `CODEX_HOME` loading the modified repo skill; production CPA binary/config/port 8317 not modified; harness ceiling 180s / 25 tools / 12 lifecycle / 3 spawns / 3 Get-Date):

- Smoke A PASS as above.
- Smoke B occurred in the same run (not manufactured): first `unsupported call: wait_agent` was not retried under bare/dotted/namespaced aliases; first `unsupported call: close_agent` was not retried; no second Worker; no Get-Date/shell filler loop; Worker completion was consumed; Brain validated the named marker and stopped.

# Installed copy conflict

Compared pre-change repo source vs `C:\Users\1\.agents\skills\multi-agent-orchestration`:

- `SKILL.md` differs and matches no git `SKILL.md` blob (install still names `DSFlash`, lacks `config/worker_defaults.yaml`).
- `scripts/audit_policy.py` and `references/task_contract.md` differ.
- `config/` is missing from the install copy.
- `references/lifecycle_and_recovery.md` was byte-identical before this change.

Because the copy is not an unmodified mirror, it was not overwritten.

# Safety

- CPA source/binary/config/port 8317 untouched.
- V2 not enabled.
- No web_search bridge, no short-name guessing, no lifecycle aliases, no PR #5538 change.
- Isolated smoke used a temp `CODEX_HOME` under `D:\Temp\mode2_failfast_smoke_20260908` (contains a copy of host config/auth; not committed).
- Untracked 2026-09-05 reports in this worktree were left untouched.
