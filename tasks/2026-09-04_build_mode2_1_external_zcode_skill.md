# Task: Build isolated Mode 2.1 external ZCode worker skill

STATUS: ABANDONED / SUPERSEDED_BY_CLEANUP
SUPERSEDED_BY: tasks/2026-09-04_remove_mode2_1_and_restore_mode2.md
ABANDONED_NOTE: Mode 2.1 / external-worker experiment abandoned by user decision on
2026-09-04. This record is historical audit only; it must not participate in routing
or runtime behavior. Active Mode 2.1 assets were removed by the cleanup task.
DATE: 2026-09-04
OWNER: Codex Root / Brain
EXECUTOR: ZCode
TASK_TYPE: ENGINEERING / ARCHITECTURE / INTEGRATION

## 1. Objective

Build **Mode 2.1** as a **new, standalone Codex skill/runtime package** whose orchestration semantics match the current Mode 2 Brain/Worker model, while replacing substantive Codex-native Worker execution with **external ZCode harness sessions**.

The required user-facing architecture is:

```text
Codex Root / Brain
  - understands the task
  - plans / decomposes
  - authors Worker Contracts
  - owns scientific / architectural judgment
  - validates results and decides follow-up
          |
          | native Codex spawn_agent
          v
Codex native subagent shell (thin dispatcher only)
          |
          | agent-scoped MCP/tool bridge
          v
ZCode external harness session
          |
          v
GLM Flash (exact runtime model id must be discovered/verified)
```

The native Codex subagent is only a **thin shell/dispatcher**. It MUST NOT perform the substantive implementation itself. The external ZCode harness does the actual reading/editing/command execution for delegated Worker tasks.

The result should feel like DSH Crew from the host side: native Codex subagent lifecycle/progress remains visible, while the actual Worker runtime is external.

## 2. Completion standard

This task is complete only when all of the following are true:

1. A separate skill/source package exists for Mode 2.1; the current `multi-agent-orchestration` Mode 2 implementation remains functionally untouched.
2. `Mode 2` still follows its existing native Codex Worker path.
3. `Mode 2.1` can spawn a native Codex thin-dispatcher subagent that delegates the task to ZCode.
4. A controlled end-to-end fixture proves that the **file/code changes were actually performed by ZCode**, not by the Codex dispatcher shell.
5. ZCode session identity and provenance are returned to Brain.
6. At least one follow-up can resume/continue the same ZCode session, or the implementation clearly documents and tests the best supported continuation mechanism if the installed ZCode version cannot do so.
7. Failure of ZCode/bridge fails closed as `BLOCKED`/`ERROR`; it does not silently fall back to direct GLM-as-Codex-provider execution.
8. Original Codex/Mode 2 paths and existing configuration are proven unchanged except for explicitly additive, isolated Mode 2.1 installation assets.
9. Tests, installation instructions, rollback instructions, and provenance are committed and pushed to a dedicated GitHub repository.

## 3. Authoritative sources that MUST be read first

Before changing or creating implementation files, read the applicable local `AGENTS.md` files in scope, including the nearest repository/global Codex instructions that govern `D:\Github` and the selected new repository. Record the exact files read in the implementation report.

Then read these pinned sources.

### A. Current Mode 2 source of truth

Repository: `foo1maker/multi-agent-orchestration`

Pinned starting commit:

`35b359bf1c94a6a30feb9db8d145f0f64cbb62db`

Must read:

- `SKILL.md`
- `references/task_contract.md`
- `references/lifecycle_and_recovery.md`
- `references/result_packet.md`
- relevant `agents/` and `scripts/` files

Current verified architectural facts:

- Mode 2 is Brain-owned orchestration: Brain thinks/delegates/validates; Worker executes bounded contracts.
- Current Mode 2 explicitly uses Codex native agent lifecycle.
- Current Mode 2 currently routes ordinary Workers toward `glm-5.3-flash` as a Codex subagent model. **Mode 2.1 exists specifically to avoid that direct provider path.**
- Brain scientific judgment and final completion authority must remain with Brain.

Do NOT reinterpret Mode 2 from memory; use the pinned repository files.

### B. DSH Crew reference implementation

Repository: `ZSeven-W/dsh-crew`

Pinned reference commit:

`10be55597909bb6a64ecbcb009d276a503a337e2`

Must inspect at minimum:

- `README.md` / `README.zh.md`
- `codex/agents/ds-flash.toml`
- `codex/agents/ds-pro.toml`
- `.mcp.json`
- the MCP server implementation behind `dsh_run_worker`
- job/session/progress/continuation code paths that are relevant to Codex host integration

Important reference pattern already verified from upstream:

```text
native Codex subagent shell
    -> MCP dsh_run_worker(...)
    -> external DSH session
```

The Codex agent TOML is a thin dispatcher with an **agent-scoped MCP server**, which is the preferred isolation pattern to investigate first.

Do not copy blindly. Distill the architecture and reproduce only what is required for ZCode. Respect the MIT license and preserve notices for any copied code.

### C. ZCode external bridge/reference

Repository: `tizerluo/zcode-open-bridge`

Pinned reference commit:

`2c1f4ad36fa6942a22b86f23d3d1bbf9643c5fff`

Must inspect at minimum:

- `README.md`
- CLI invocation and JSON output behavior
- session creation / resume behavior (`--resume` or installed-version equivalent)
- current ZCode protocol/version compatibility notes
- MCP/ACP bridge implementation only as needed
- permission/tool restrictions and Windows behavior

Known upstream facts to verify against the installed version:

- ZCode CLI supports prompt execution and JSON output.
- Upstream documents session continuation/resume.
- `zcode-open-bridge` is community/unofficial; do not assume it is a stable official API.

Use it as a reference, not an unquestioned dependency.

## 4. Core design decision

Mode 2.1 MUST be a **separate skill/package**, not a patch that changes Mode 2 behavior.

Preferred source repository name:

`foo1maker/mode2-1-external-workers`

Preferred local source path:

`D:\Github\mode2-1-external-workers`

Preferred installed skill path after QC only:

`C:\Users\1\.agents\skills\mode2-1-external-workers`

A dedicated thin Codex agent may be installed additively under:

`C:\Users\1\.codex\agents\`

with a unique name such as:

`zcode-flash.toml`

Do not overwrite an existing file of the same name. If a collision exists, choose a namespaced Mode 2.1 name and document it.

The implementation SHOULD prefer an **agent-scoped MCP server declaration** in the thin dispatcher TOML, analogous to DSH Crew, so that Mode 2.1 does not require replacing or globally rerouting Codex model providers.

## 5. Non-negotiable compatibility boundary

### MUST NOT modify for implementation

Do not modify the functional contents of:

- `D:\Github\multi-agent-orchestration\SKILL.md`
- `D:\Github\multi-agent-orchestration\references\*`
- `D:\Github\multi-agent-orchestration\agents\*`
- `D:\Github\multi-agent-orchestration\scripts\*`
- installed original Mode 2 skill files
- existing Codex model-provider definitions used by the normal Codex path

The only approved mutation in `foo1maker/multi-agent-orchestration` for this task is this task specification and, if needed later, a task status update. Do not use the old repository as the implementation workspace.

### Existing Codex config

Prefer **zero edits** to the existing global Codex config.

If an additive global config change is genuinely unavoidable, STOP before making it and report exactly why an agent-scoped/project-scoped solution cannot work. Do not make such a change without explicit approval.

### No direct GLM provider route

Mode 2.1 MUST NOT solve the problem by putting `glm-5.3-flash` back into `~/.codex/config.toml` as a Codex model/provider.

The required path is:

```text
Codex native shell -> bridge/tool -> ZCode harness -> GLM
```

not:

```text
Codex native shell -> custom GLM provider
```

## 6. Mode 2.1 semantic requirements

The new skill must preserve the current Mode 2 principles unless a principle is specifically tied to Codex-native Worker execution and must therefore be adapted.

At minimum preserve:

- Brain owns planning, task decomposition, final judgment, scientific reasoning, validation, recovery decisions, and Stage 3 completion.
- Worker receives a bounded Brain-authored Task Contract.
- Worker does not become a second Brain.
- `DISCOVERY`, `EXECUTION`, `ANALYSIS`, `REVIEW` semantics remain compatible where meaningful.
- `RESULT_PACKET` is normalized before Brain accepts completion.
- Worker self-report is evidence, not proof; Brain validates critical outputs.
- No raw forwarding of the user's entire parent transcript as a substitute for a Worker Contract.
- Reviewer behavior remains read-only unless explicitly authorized.

Mode 2.1-specific change:

```diff
- substantive Worker runtime = Codex native model execution
+ substantive Worker runtime = ZCode external harness session
```

Do not duplicate or invent a new scientific decision framework.

## 7. Thin dispatcher requirements

Create a Codex native agent definition whose only substantive role is dispatch.

Its instructions must enforce the equivalent of:

1. Receive the Brain-authored Worker Contract.
2. Pass that contract and explicitly provided paths/context to the Mode 2.1 ZCode bridge/tool.
3. Wait for ZCode to settle.
4. Return the normalized external Worker result/provenance to Brain.
5. Never edit files itself.
6. Never run task implementation commands itself.
7. Never answer the delegated task from its own model knowledge.
8. On bridge/ZCode failure, report the failure and stop.

The shell model should be a small reliable native Codex/OpenAI model that can call the MCP tool. Do not spend a strong model on implementation work that the shell is forbidden to do. Use the installed Codex-supported model set rather than inventing an unavailable id.

## 8. ZCode bridge requirements

Implement the smallest reliable bridge needed for general bounded Worker execution.

The external-facing logical interface should support at least:

```text
run_worker(contract, cwd, permissions/mode, optional session_id)
```

and return at least:

```text
status
response/result
zcode_session_id
usage if available
stop/error reason if available
exact harness/CLI version
exact model id/config if discoverable
```

Continuation should use the same ZCode session where supported by the installed version.

Do not assume the existing `zcode-open-bridge` MCP review tools are sufficient for general implementation. Inspect them first. It is acceptable—and likely preferable—to create a small Mode 2.1-specific MCP wrapper around the local ZCode CLI/session protocol rather than depending on unrelated review APIs.

The bridge must:

- invoke ZCode in the contract's explicit `cwd`;
- avoid shell interpolation of untrusted task text;
- pass arguments as structured process arguments, not concatenated shell strings;
- fail closed on missing ZCode/login/model/session;
- emit machine-readable logs/provenance without leaking credentials;
- never print API keys/tokens/config secrets;
- support Windows paths correctly;
- enforce a bounded timeout and return a settled error rather than looping forever.

## 9. Model selection inside ZCode

Target worker model: **GLM Flash via ZCode**.

Do not hardcode an unverified spelling/model id. Detect or verify the exact model id accepted by the installed ZCode/runtime and record it.

If GLM Flash cannot be selected in the installed ZCode build, settle `BLOCKED_MODEL_SELECTION` with evidence. Do not silently switch Mode 2.1 to a different backend/model.

## 10. Activation and routing

The new skill must have a unique name and explicit activation for **Mode 2.1**.

Required behavior:

- `Mode 2` -> original `multi-agent-orchestration` behavior remains unchanged.
- `Mode 2.1` -> new external-worker skill.

Because `Mode 2.1` text may semantically overlap the current Mode 2 trigger, explicitly test skill-routing behavior.

Do not modify the original Mode 2 skill merely to resolve an activation collision.

If the host router cannot reliably distinguish the two while both are installed, fail closed and document a non-overlapping explicit alias for Mode 2.1 as a temporary compatibility route (for example a namespaced `external-mode2` invocation). Do not hide the collision.

## 11. Isolation and write safety

For implementation/testing:

- use a dedicated new repository/worktree;
- use disposable fixture repositories for destructive tests;
- never let the dispatcher and ZCode both perform implementation writes;
- do not allow two parallel write Workers to mutate the same working tree;
- preserve git history;
- no `rm -rf`, recursive destructive cleanup, or broad deletion outside disposable fixtures;
- do not delete or rewrite the existing Mode 2 repository/install.

For future parallel Mode 2.1 workers, document the requirement for per-worker worktree isolation or an equivalent explicit single-writer guarantee.

## 12. Required implementation deliverables

Create a dedicated Mode 2.1 repository containing, at minimum:

- `SKILL.md`
- `README.md`
- `LICENSE` if required by copied/derived code
- `agents/` or `codex/agents/` thin dispatcher definition(s)
- bridge/server implementation
- `references/` containing the Mode 2.1 Worker Contract / lifecycle / result protocol used at runtime
- tests
- installation script or deterministic installation instructions
- rollback/uninstall instructions
- `docs/architecture.md`
- `docs/provenance.md`
- `docs/compatibility.md`

If Mode 2 semantics are vendored/copied, record:

- source repository
- source commit `35b359bf1c94a6a30feb9db8d145f0f64cbb62db`
- which files/sections were copied or adapted
- any deliberate semantic differences

If DSH Crew code is copied rather than merely studied, preserve MIT license/attribution and list exact files/commits.

## 13. Required QC / tests

### QC-A: baseline integrity

Before implementation, record SHA-256 hashes or git tree/commit state for:

- source `multi-agent-orchestration` repository functional files
- installed original Mode 2 skill functional files
- existing `~/.codex/config.toml`
- existing `~/.codex/agents/` file list and hashes for any files that could collide

After installation, prove those protected originals remain unchanged unless an explicitly approved additive file was created.

### QC-B: bridge unit/integration tests

Test:

- ZCode executable discovery
- missing-ZCode failure
- JSON parsing
- nonzero exit handling
- timeout handling
- Windows path with spaces
- task text containing quotes/newlines/shell metacharacters
- credential redaction
- model verification
- session id capture
- resume/continuation if supported

### QC-C: dispatcher purity

Prove the Codex dispatcher does not perform implementation itself.

At minimum:

- dispatcher instructions forbid edits/commands except the bridge tool;
- test fixture/log evidence shows actual changes originate during the ZCode call;
- shell returns external result rather than reconstructing the answer independently.

### QC-D: end-to-end native-UI path

Run a disposable fixture task through actual Codex Mode 2.1:

```text
Codex Brain
 -> native zcode dispatcher subagent
 -> Mode 2.1 bridge
 -> ZCode harness
 -> GLM Flash
 -> fixture edit/test
 -> result back to dispatcher
 -> result back to Brain
```

Capture enough evidence to verify:

- Codex spawned a native subagent shell;
- host showed the child in the normal subagent/progress path to the extent supported by the installed Codex build;
- ZCode performed the actual edit/commands;
- Brain received a settled result;
- no direct GLM Codex provider route was used.

Do not claim native UI equivalence unless it was actually observed.

### QC-E: Mode 2 regression

Run a separate baseline test proving ordinary `Mode 2` still uses the original path and does not require Mode 2.1/ZCode.

### QC-F: routing collision

Test explicit prompts for at least:

- `Mode 2`
- `启动模式2`
- `Mode 2.1`
- `启动模式2.1`

Record which skill(s) activate and whether the result is unambiguous.

## 14. Acceptance artifacts

Produce machine-readable or text artifacts that allow later audit, including:

- pre/post protected-path hash manifest
- environment/version manifest
- test results
- one successful end-to-end transcript/log with secrets redacted
- one controlled failure-case log
- session-resume test result
- routing-collision test result
- final architecture decision record

Do not store credentials or raw secret-bearing ZCode config.

## 15. Provenance requirements

Record at minimum:

- OS and shell
- Codex version
- ZCode version
- exact ZCode worker model id observed
- Node/Python/runtime versions used by the bridge
- source commit of Mode 2
- source commit of DSH Crew reference
- source commit of zcode-open-bridge reference
- dependency versions and lockfile
- test commands and exit codes
- final repository commit SHA
- remote branch pushed

Where deterministic tests use seeds, record them.

## 16. Conflict handling

Priority:

1. User's current task specification
2. applicable local `AGENTS.md`
3. current pinned Mode 2 repository facts for orchestration semantics
4. actual installed Codex/ZCode behavior
5. DSH Crew/zcode-open-bridge reference implementations
6. assumptions

If a reference README conflicts with actual installed behavior, trust reproducible runtime evidence and document the discrepancy.

If this task conflicts with an applicable `AGENTS.md`, STOP and report the exact conflict before modifying protected assets.

## 17. GitHub requirements

### Existing Mode 2 repository

Do not implement Mode 2.1 inside `foo1maker/multi-agent-orchestration`.

This repository remains the original Mode 2 source plus historical task specification.

### New repository

Preferred remote:

`foo1maker/mode2-1-external-workers`

If it does not exist and authenticated `gh` can create private repositories, create it as **private**.

If remote creation is unavailable, do not put implementation into the original Mode 2 repository. Create the standalone local repository, complete local QC, and settle with `SYNC_PENDING_REMOTE_CREATE`, including the exact command needed to create/push the remote.

Commit logical stages rather than one opaque dump. Preserve negative/failed attempts in history or an engineering log when materially informative.

Push final accepted work to the new remote `main` only after tests pass.

Do not describe a remote commit as proof that another local worktree is synchronized.

## 18. Installation / rollback boundary

Do not install into live Codex paths until the standalone repository passes unit/integration tests.

Before live installation, take the baseline hashes in QC-A.

Installation must be additive and reversible.

Rollback must be able to remove only Mode 2.1 assets and restore the exact pre-install state without touching original Mode 2.

## 19. Evidence boundary

VERIFIED means supported by repository contents, runtime output, hashes, logs, or tests.

OBSERVED means directly seen in the actual Codex/ZCode integration run.

INFERRED means architectural interpretation not directly proven by a run.

UNKNOWN means not tested or unavailable.

Do not report:

- "native UI identical" unless observed;
- "ZCode did the work" without external-session/log evidence;
- "Mode 2 unaffected" without pre/post integrity/regression evidence;
- "persistent session works" without a resume test;
- "GLM Flash selected" without runtime/config evidence.

## 20. Final report format

Return a concise completion packet containing:

```text
TASK_STATUS: COMPLETED | BLOCKED | SYNC_PENDING_REMOTE_CREATE
MODE21_REPO:
MODE21_REMOTE:
MODE21_COMMIT:
ORIGINAL_MODE2_COMMIT_BASELINE:
ORIGINAL_MODE2_PROTECTED_HASH_VERDICT:
CODEX_CONFIG_VERDICT:
ZCODE_VERSION:
ZCODE_WORKER_MODEL:
NATIVE_SUBAGENT_SHELL_VERDICT:
EXTERNAL_EXECUTION_VERDICT:
SESSION_RESUME_VERDICT:
MODE2_REGRESSION_VERDICT:
MODE21_ROUTING_VERDICT:
TESTS:
KNOWN_LIMITATIONS:
INSTALL_STATE:
ROLLBACK_VERIFIED:
NEXT_MINIMAL_ACTION:
```

Do not claim completion if critical evidence remains only assumed.