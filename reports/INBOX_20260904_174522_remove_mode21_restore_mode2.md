# Status

Formal task: remove Mode 2.1 completely and restore/verify plain Mode 2
(task file: tasks/2026-09-04_remove_mode2_1_and_restore_mode2.md).

STATUS: COMPLETED_WITH_OBSERVED_FIX (routing restored and observed; one
minimal model-routing-only fix applied after an observed execution defect,
per task Scope F; remote Mode 2.1 repo deletion blocked by permission).

MODE2_COMMIT: 855d77d61abaa71d237229c0756f229f42188649

# Conclusion

Mode 2.1 is fully removed from all active runtime/discovery surfaces.
Plain Mode 2 is the only Mode-2-related skill/runtime path. All three plain
triggers (`mode2`, `启动模式2`, `开启模式2`) were observed in fresh
independent host sessions (headless Codex CLI, codex-cli 0.153.2) to load
`multi-agent-orchestration` and to perform native `spawn_agent` execution.
A real defect in the previously hard-coded default worker model route was
observed and minimally fixed; default routing now inherits the host model
path, and a post-fix retest passed.

# Completed

- MODE21_LOCAL_REPO_REMOVED: YES (D:\Github\mode2-1-external-workers deleted;
  one leftover keepalive node.exe holding the repo CWD was terminated first)
- MODE21_INSTALLED_SKILLS_REMOVED: YES
  (C:\Users\1\.agents\skills\zcode-external-workers — junction to
  C:\Users\1\.codex\skills\zcode-external-workers — single real copy deleted;
  legacy mode2-1-external-workers never existed)
- MODE21_CUSTOM_AGENT_REMOVED: YES (C:\Users\1\.codex\agents\zcode-flash.toml)
- MODE21_TEMP_ASSETS_REMOVED: YES (D:\Temp\mode21, mode21-e2e, mode21-refs,
  mode21_zw1_20260904_162003023, and the empty disposable workspace
  C:\Users\1\Documents\Codex\2026-09-04\external-mode2-zw-1-single-worker;
  5 leftover idle node/node_repl processes from the 16:19 e2e run were
  terminated to release the directory)
- MODE21_ACTIVE_ROUTING_REFERENCES: ZERO (sweeps over .agents\skills,
  .codex\skills, .codex\agents, .codex\config.toml, AGENTS.md x2,
  .codex\prompts, hooks.json, memories sqlite, _shared: zero matches)
- REMOTE_MODE21_REPO_DELETE: BLOCKED_PERMISSION (repo foo1maker/
  mode2-1-external-workers verified twice; DELETE returned 403 "Must have
  admin rights"; token scopes are `gist, repo, workflow` — no delete_repo.
  No credentials were broadened, per task rules)
- config.toml Mode 2.1-specific entry removed: only
  `[projects.'c:\users\1\documents\codex\2026-09-04\external-mode2-zw-1-single-worker']`
  was deleted; backup config.toml.bak-mode21-cleanup-20260904_163346 kept
- Mode 2.1 build task marked ABANDONED / SUPERSEDED_BY_CLEANUP (commit 0db196a,
  pushed; remote ref verified equal after push)
- MODE2_SOURCE_INSTALL_MATCH: YES (all 7 functional files byte-identical
  between D:\Github\multi-agent-orchestration and
  C:\Users\1\.codex\skills\multi-agent-orchestration, re-verified after the fix)
- MODE2_ROUTE_mode2: PASS_OBSERVED (fresh session 01a06b97: skill + 3
  references loaded, native spawn confirmed)
- MODE2_ROUTE_启动模式2: PASS_OBSERVED (fresh session 01a06bb5)
- MODE2_ROUTE_开启模式2: PASS_OBSERVED (fresh session 01a06bbd)
- MODE2_NATIVE_SPAWN: PASS_OBSERVED (multiple confirmed spawns with
  task_name + nickname returned by the native runtime; native child visible
  as `running`/`completed` and as separate subagent sessions)
- MODE2_NATIVE_WORKER_SETTLED: PASS_OBSERVED (Scope E worker settled with a
  well-formed RESULT_PACKET)
- MODE2_MODEL_ROUTE: PASS_OBSERVED after the fix; before the fix the
  hard-coded glm-5.3-flash default was OBSERVED-BROKEN (see Errors)
- MODE2_BRAIN_VALIDATION: PASS_OBSERVED (byte-level Stage 2 acceptance:
  15/16-byte exact content + hex match)
- MODE2_DUPLICATE_WORK: NO (in every test the Brain waited natively, used
  followup_task/respawn per recovery rules, and never performed the Worker's
  file work in the main thread)
- MODE2_FILES_CHANGED: SKILL.md only (commit 855d77d) + task-history audit
  marking (commit 0db196a); install copy synced
- UNRELATED_CONFIG_CHANGED: NO (config.toml diffs vs backups are exactly the
  removed Mode 2.1 project entry and the removed
  `default_subagent_model = "glm-5.3-flash"` line)
- UNRELATED_SKILLS_CHANGED: NO (only multi-agent-orchestration/SKILL.md synced;
  zcode-external-workers deleted as authorized)
- UNRELATED_AGENTS_CHANGED: NO (ds-flash.toml, ds-pro.toml untouched)

# Outputs

- D:\Github\multi-agent-orchestration (commits 0db196a, 855d77d; both pushed
  and remote refs verified: origin/main = 855d77d)
- Updated installed skill: C:\Users\1\.codex\skills\multi-agent-orchestration\SKILL.md
- Backups: C:\Users\1\.codex\config.toml.bak-mode21-cleanup-20260904_163346,
  C:\Users\1\.codex\config.toml.bak-scopef-20260904_173949
- Test transcripts: D:\Temp\mode2_restore_test\route_mode2.jsonl,
  test_a_startup.jsonl, test_b_mode2.jsonl, test_c_open.jsonl,
  test_e_native.jsonl, test_f_retest.jsonl

# Non-C Drive Files

- Deleted: D:\Github\mode2-1-external-workers (repo),
  D:\Temp\mode21*, D:\Temp\mode21-e2e, D:\Temp\mode21-refs,
  D:\Temp\mode21_zw1_20260904_162003023
- Created: D:\Temp\mode2_restore_test (test scratch + transcripts)

# C Drive Exceptions

- Deleted: C:\Users\1\.codex\skills\zcode-external-workers (via junction target
  C:\Users\1\.agents\skills\zcode-external-workers),
  C:\Users\1\.codex\agents\zcode-flash.toml,
  C:\Users\1\Documents\Codex\2026-09-04\external-mode2-zw-1-single-worker (empty)
- Modified: C:\Users\1\.codex\config.toml (two entries, backed up);
  C:\Users\1\.codex\skills\multi-agent-orchestration\SKILL.md (synced from repo)
- Upgraded: @openai/codex npm package 0.147.0 → 0.153.2 (test prerequisite; the
  0.147 CLI could not start any session against the configured relay because of
  a collaboration tool schema mismatch, independent of Mode 2)

# Errors

- Scope F observed defect (pre-existing, not caused by cleanup): the skill's
  hard-coded default worker route (`glm-5.3-flash` / `max`) failed in three
  fresh-host real runs. Clean-context (`fork_turns: none`) workers on
  `glm-5.3-flash` and `gemini-3.7-flash-high` could not consume the encrypted
  `NEW_TASK` contract payload: worker 1 answered "tell me the task" twice,
  worker 2 inverted roles into a coordinator and tried to spawn its own
  sub-workers, worker 3 claimed SUCCESS with `OUTPUTS: none`. The same
  contracts executed correctly on GPT-5.6-class workers. Evidence in the
  test transcripts and subagent session rollouts.
- Minimal fix applied per task Scope F option 4: ordinary workers now inherit
  the host's normal native worker model path (omit model/reasoning overrides);
  relay models remain available only on explicit user request
  (SKILL.md, commit 855d77d; `default_subagent_model` removed from
  config.toml [agents]).
- Post-fix retest: default-route worker (inherited gpt-5.6-sol / max) executed
  the contract, wrote `MODE2_INHERIT_OK` (16 bytes, hex verified), Brain Stage 2
  byte validation passed. MODE2_DEFAULT_ROUTE_RETEST: PASS.
- Minor: Scope F retest worker settled `BLOCKED` because Brain's contract
  wrongly said "15 bytes" while the true content is 16 bytes; Brain still
  performed its own byte-level acceptance (passed) rather than accepting the
  contradictory contract. Worker behavior was protocol-correct.
- Test-harness notes (not Mode 2 defects): `codex exec` under bash `timeout`
  killed the parent process, which also killed the spawned child (observed in
  the first route test); resolved by running sessions in background. Two
  followup `wait_agent` calls in the first session ended when the killed
  parent's user input re-injected; no protocol violation by the Brain.

# Validation

- Execution: fresh independent host sessions (headless `codex exec`, one
  thread per test, cwd D:\Temp\mode2_restore_test) on codex-cli 0.153.2;
  routing verdicts from runtime observation, not static inspection.
- Internal Validation: file-level sweeps for Mode 2.1 references; byte-diff
  of source vs install for all 7 functional Mode 2 files; config.toml diffs
  vs pre-change backups; git diff scoped to SKILL.md + task audit file;
  remote refs verified by `git rev-parse origin/main` after each push.
- Reviewer: not used (no separate Inspector spawn was justified for this
  cleanup; all acceptance evidence is runtime-observed or byte-diffed).
- Independent Audit: static checks confirm zero Mode 2.1 strings in all
  active skill/agent/config locations after cleanup; hello.txt contents in
  Scope E and Scope F retest were hex-verified by both Worker and Brain.

# Safety

- Deletion targets were verified by path, content, and identity before
  deletion; ambiguous targets were not deleted.
- The dedicated remote repo was NOT deleted (403; permission not broadened).
- No git history rewrite; only forward commits and pushes.
- ZCode, Gemini CLI, Grok CLI installations untouched. Unrelated agents
  (ds-flash, ds-pro), unrelated skills, global AGENTS.md files, auth, and
  credentials untouched.
- Processes terminated were idle leftovers (0% CPU) whose CWD was inside the
  abandoned Mode 2.1 fixture/repo, plus one keepalive node.exe; each was
  identified by CWD and command line before termination.

# Next Step

- Optional: delete foo1maker/mode2-1-external-workers from a session with
  delete_repo/admin permission, then no Mode 2.1 trace remains anywhere.
- Optional: renew or retire the GLM Coding Plan provider if relay-model
  workers are wanted again; SKILL.md now treats relay-provider worker models
  as explicit-request-only.
- The three status reports written by the test Brain sessions under
  D:\Temp\CodexPendingReports are audit-only leftovers of the acceptance
  runs and can be deleted at will.