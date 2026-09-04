# Task — Remove Mode 2.1 completely and restore/verify plain Mode 2

## User decision

Mode 2.1 / external-worker experiment is abandoned. Do not repair it further. Remove its active/runtime assets and ensure plain Mode 2 is again the only Mode-2-related runtime/skill path.

The priority is reliability and a clean native Codex Mode 2 path, not preserving the abandoned experiment.

## Authority and starting point

1. Read the current real filesystem and installed Codex/agent state before deleting anything.
2. Read current `D:\Github\multi-agent-orchestration\SKILL.md`, its three references, install copy, and relevant Codex agent/config state.
3. Treat current remote `multi-agent-orchestration` main as source of truth for Mode 2. Its functional baseline before the Mode 2.1 task-only commit is `35b359bf1c94a6a30feb9db8d145f0f64cbb62db`; current main may contain later task-history files but functional Mode 2 files must not be rolled back blindly.
4. Do not assume the cause of Mode 2 trigger failure. First remove the competing Mode 2.1 runtime/discovery assets, then test plain Mode 2 in a fresh host session. Modify Mode 2 only if a remaining failure is observed.

## Scope A — Remove abandoned Mode 2.1 active/runtime assets

Find and remove only assets belonging to the abandoned Mode 2.1 / external-ZCode-worker experiment. Expected candidates include, but are not limited to:

- local repo: `D:\Github\mode2-1-external-workers`
- installed skill: `C:\Users\1\.agents\skills\zcode-external-workers`
- legacy installed skill: `C:\Users\1\.agents\skills\mode2-1-external-workers`
- Codex custom agent: `C:\Users\1\.codex\agents\zcode-flash.toml`
- disposable Mode 2.1 temp roots such as `D:\Temp\mode21*` and `D:\Temp\mode21_*`
- Mode 2.1-only local audit/install artifacts outside the dedicated repo, if any
- active router/discovery references to `external-mode2`, `zcode-external-workers`, `mode2-1-external-workers`, `mode21`, or the dedicated repo path, but only when they are demonstrably part of Mode 2.1

Do **not** uninstall or delete ZCode itself, Gemini CLI, Grok CLI, unrelated credentials/providers, or unrelated user projects. The abandoned orchestration integration is being removed; the standalone CLIs are not.

Do **not** modify `~/.codex/config.toml` unless an actual Mode 2.1-specific entry is found there. If such an entry exists, remove only that exact entry and preserve byte-for-byte all unrelated settings.

### Dedicated GitHub repo

The user has explicitly abandoned this experiment and requested its artifacts be removed. If the authenticated GitHub CLI/account has permission to delete exactly `foo1maker/mode2-1-external-workers`, delete that dedicated remote repository after verifying the owner/name twice. Do not delete any other repository. If remote deletion permission is unavailable, report `REMOTE_MODE21_REPO_DELETE: BLOCKED_PERMISSION` and continue with local/runtime cleanup; do not broaden credentials or permissions automatically.

### Historical record in the original Mode 2 repo

Do not delete historical task records from `foo1maker/multi-agent-orchestration` merely to erase history. They are non-runtime audit records. Mark the previous Mode 2.1 build task as `ABANDONED / SUPERSEDED_BY_CLEANUP` if needed, but it must not participate in routing or runtime behavior.

## Scope B — Prove Mode 2.1 no longer participates in routing

After cleanup, search active installed/discoverable skill and agent locations for:

- `external-mode2`
- `zcode-external-workers`
- `mode2-1-external-workers`
- `zcode-flash`
- `mode21-zcode-bridge`
- `D:\Github\mode2-1-external-workers`

Expected result: zero active/discoverable runtime matches. Historical text inside the original repo's task history may remain and must be reported separately, not treated as active contamination.

Do not add replacement aliases or another compatibility skill.

## Scope C — Audit plain Mode 2 before changing it

Verify the current plain Mode 2 source and installed copy:

- source repo: `D:\Github\multi-agent-orchestration`
- installed skill: `C:\Users\1\.agents\skills\multi-agent-orchestration`
- current `SKILL.md` frontmatter
- three referenced protocol files
- any installed native worker agent definitions actually used by Mode 2

Confirm the frontmatter explicitly owns plain Mode 2 phrases such as:

- `mode2`
- `Mode 2`
- `启动模式2`
- `开启模式2`
- `使用模式2`

Check source/install byte equality for functional Mode 2 files. Do not rewrite the skill just for consistency if source and install are already valid.

## Scope D — Fresh-host routing acceptance

Use independent fresh Codex host sessions. Test at minimum:

1. `mode2`
2. `启动模式2`
3. `开启模式2`

For each, record the actual UI/runtime-observed skill selection.

Required:

```text
MODE2_SKILL_LOADED: multi-agent-orchestration
MODE21_SKILL_LOADED: NO
OTHER_MODE2_COLLISION: NO
```

Static metadata inspection is only a pre-check. Final routing verdict requires fresh-host observation.

If cleanup alone restores correct routing, **do not modify Mode 2 routing metadata further**.

## Scope E — Native Mode 2 execution acceptance

After routing passes, run one minimal real Mode 2 task in a fresh host session to prove it does more than load the skill.

Use a bounded disposable fixture and a small Worker Contract. Required observations:

```text
BRAIN_LOADED_MODE2: YES
SPAWN_AGENT_CALLED: YES
NATIVE_CHILD_VISIBLE: YES
WORKER_RECEIVED_SCOPED_CONTRACT: YES
WORKER_SETTLED: YES
BRAIN_WAITED_WITHOUT_DUPLICATING_WORK: YES
BRAIN_VALIDATED_RESULT: YES
```

Do not use any Mode 2.1 bridge, external dispatcher, ZCode harness, or second Codex runtime.

## Scope F — Model routing audit; fix only if observed broken

The current Mode 2 skill may contain explicit default/fallback worker model routing. Do not assume it is healthy merely because the skill loads.

The user has already observed direct GLM/DS Flash paths inside Codex can exhibit looping behavior. Therefore:

1. Test the current actual Mode 2 default worker route once with a tiny bounded task.
2. If the current hard-coded default model route works normally, leave it unchanged.
3. If it reproduces looping, rejected model ids, repeated retries, or other provider/harness instability, classify that as a separate observed Mode 2 execution defect and make the **smallest model-routing-only change**.
4. Preferred minimal fallback when a hard-coded custom provider route is the defect: stop forcing that custom provider/model as the ordinary default and use the Codex host's normal native worker model path (for example, inherit the working host model when the live schema permits) rather than inventing another custom provider ladder.
5. Do not hard-code a new unverified model id. Do not rebuild an external harness. Do not add Gemini/Grok/ZCode routing in this cleanup task.

The success criterion is a stable native Codex child, not preserving any particular worker model.

## Scope G — Regression and protected assets

Protect unrelated assets. At minimum verify before/after:

- `~/.codex/config.toml` except any exact Mode 2.1-specific entry found and removed
- global `AGENTS.md`
- original Mode 2 functional files except a narrowly justified routing/model fix after an observed failure
- unrelated `~/.codex/agents/*`
- unrelated `~/.agents/skills/*`
- ZCode/Gemini/Grok installations themselves

If a Mode 2 fix is required, make one minimal change, test it, and stop. Do not refactor unrelated Mode 2 policies.

## Success criteria

Only report `COMPLETED` when all applicable items are true:

```text
MODE21_LOCAL_REPO_REMOVED: YES
MODE21_INSTALLED_SKILLS_REMOVED: YES
MODE21_CUSTOM_AGENT_REMOVED: YES
MODE21_TEMP_ASSETS_REMOVED: YES
MODE21_ACTIVE_ROUTING_REFERENCES: ZERO
REMOTE_MODE21_REPO_DELETE: YES | BLOCKED_PERMISSION

MODE2_SOURCE_INSTALL_MATCH: YES
MODE2_ROUTE_MODE2: PASS_OBSERVED
MODE2_ROUTE_CN_1: PASS_OBSERVED
MODE2_ROUTE_CN_2: PASS_OBSERVED
MODE2_NATIVE_SPAWN: PASS_OBSERVED
MODE2_NATIVE_WORKER_SETTLED: PASS_OBSERVED
MODE2_BRAIN_VALIDATION: PASS_OBSERVED
MODE2_DUPLICATE_WORK: NO

MODE2_MODEL_ROUTE: PASS_OBSERVED
UNRELATED_CONFIG_CHANGED: NO
UNRELATED_SKILLS_CHANGED: NO
UNRELATED_AGENTS_CHANGED: NO
```

If routing works but execution/model route remains broken, return `PARTIAL_MODE2_EXECUTION_BLOCKED` with exact observed evidence. Do not claim Mode 2 is restored based only on frontmatter.

## Final report

Return only a compact factual report:

```text
TASK_STATUS:
MODE2_COMMIT:

MODE21_LOCAL_REPO_REMOVED:
MODE21_INSTALLED_SKILLS_REMOVED:
MODE21_CUSTOM_AGENT_REMOVED:
MODE21_TEMP_ASSETS_REMOVED:
MODE21_ACTIVE_ROUTING_REFERENCES:
REMOTE_MODE21_REPO_DELETE:

MODE2_SOURCE_INSTALL_MATCH:
MODE2_ROUTE_mode2:
MODE2_ROUTE_启动模式2:
MODE2_ROUTE_开启模式2:
MODE2_NATIVE_SPAWN:
MODE2_NATIVE_WORKER_SETTLED:
MODE2_MODEL_ROUTE:
MODE2_BRAIN_VALIDATION:
MODE2_DUPLICATE_WORK:

MODE2_FILES_CHANGED:
UNRELATED_CONFIG_CHANGED:
UNRELATED_SKILLS_CHANGED:
UNRELATED_AGENTS_CHANGED:

ROOT_CAUSE_IF_FOUND:
KNOWN_LIMITATIONS:
NEXT_MINIMAL_ACTION:
```

## Stop conditions

- If deletion target identity is ambiguous, stop before destructive deletion and report the ambiguity.
- If fixing Mode 2 would require broad policy/runtime redesign, stop and report evidence instead of expanding scope.
- Do not recreate Mode 2.1 under another name.
