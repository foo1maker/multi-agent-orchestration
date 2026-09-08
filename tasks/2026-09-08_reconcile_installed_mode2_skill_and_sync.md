# Task: reconcile installed Mode 2 skill copy and sync safely

## Objective

Reconcile the independently modified installed copy at:

`C:\Users\1\.agents\skills\multi-agent-orchestration`

against the authoritative source repository:

`D:\Github\multi-agent-orchestration`

then make the installed copy an intentional, verified mirror of the authoritative source without losing any genuinely useful local behavior.

This task exists because the 2026-09-08 fail-fast change was completed in the source repository but the installed copy was intentionally not overwritten after a conflict was detected.

The desired end state is:

```text
source repo = authoritative
installed copy = verified mirror of source
no untracked local behavior hidden only in install
fail-fast change present in installed copy
worker model routing config present in installed copy
```

Do not assume the local installed edits are wrong. Audit them individually first.

---

## Known evidence to verify, not blindly trust

The previous report recorded:

- source fail-fast commit: `3da84aa22bffcab404b01adf374578c5f25b36ff`
- source repo main later advanced through report commits
- installed copy was not synced
- installed `SKILL.md` contained DSFlash-related content and did not match any git `SKILL.md` blob checked at the time
- installed `scripts/audit_policy.py` differed
- installed `references/task_contract.md` differed
- installed `config/` was absent
- installed `references/lifecycle_and_recovery.md` had been an unmodified mirror before the fail-fast edit

Re-verify all of this from the real filesystem and repository before acting.

---

## Authority and scope

### Authoritative source repository

- Repo: `foo1maker/multi-agent-orchestration`
- Worktree: `D:\Github\multi-agent-orchestration`
- Branch: `main`

### Installed copy

- `C:\Users\1\.agents\skills\multi-agent-orchestration`

### Allowed modifications

You may modify only:

1. files inside `D:\Github\multi-agent-orchestration` that are directly required to preserve a justified installed-only behavior;
2. the installed skill directory after reconciliation is complete;
3. a task report under the source repo `reports/`;
4. tests or policy audit files only if directly needed by a preserved behavior.

### Forbidden modifications

Do not modify:

- CPA source or production binary;
- port 8317 process/config;
- Codex global config except read-only verification if needed;
- V1/V2 routing;
- namespace restore behavior;
- web_search compatibility;
- PR #5538;
- unrelated skills;
- any other installed skill;
- project research assets;
- runtime/scheduler/watchdog/state-machine logic.

Do not redesign Mode 2 in this task.

---

## Phase 0 — verify repository and installation state

Before editing anything:

1. Confirm the source repo path, branch, HEAD, remote, and clean/dirty state.
2. Confirm the task file exists in the specified repo.
3. Record the installed copy path and enumerate its files.
4. Record SHA256 for every file that exists in both source and installed copy.
5. Record source-only and install-only files/directories.
6. Confirm whether any installed file is newer only by timestamp but identical by content; do not treat timestamps as authority.
7. Confirm the current source contains the fail-fast changes from `3da84aa...`.
8. Confirm current live V1 policy in source still treats these as declared current V1 lifecycle children:
   - `spawn_agent`
   - `wait_agent`
   - `send_input`
   - `close_agent`
   - `resume_agent`
9. Confirm source does not instruct callable use of undeclared V1 `followup_task`, `list_agents`, or `interrupt_agent`.

If the source repo contains unrelated uncommitted edits, do not overwrite or discard them. Report them and continue only if the reconciliation can be isolated safely.

---

## Phase 1 — classify every installed-only difference

For every differing installed file, create an audit table with:

```text
PATH
SOURCE STATE
INSTALLED STATE
ORIGIN IF IDENTIFIABLE
BEHAVIORAL EFFECT
CURRENT RELEVANCE
KEEP / MERGE / DROP / UNKNOWN
EVIDENCE
```

At minimum inspect:

- `SKILL.md`
- `scripts/audit_policy.py`
- `references/task_contract.md`
- `references/lifecycle_and_recovery.md`
- `references/result_packet.md`
- `config/worker_defaults.yaml`
- any install-only files
- any source-only files absent from install

### Required review of DSFlash/local model content

For every DSFlash or older worker-routing rule found only in the installed copy:

1. Determine what behavior it was intended to provide.
2. Check whether the current source already provides an equivalent or better behavior through `config/worker_defaults.yaml` and current routing rules.
3. If current source fully supersedes it, classify the installed rule as stale and do not preserve it.
4. If it provides a still-required behavior not represented in source, preserve only the smallest semantically necessary rule by merging it into source first.
5. Do not preserve model-specific historical wording merely because it existed locally.
6. Do not introduce DSFlash-specific hardcoding if the current generic worker model entry already covers the same need.

### Decision standard

Preserve an installed-only behavior only if all are true:

- its purpose is still current;
- current source does not already cover it;
- it does not conflict with the current Brain/Worker architecture;
- it does not reintroduce unsupported tool names or retry loops;
- it can be stated more simply than the installed legacy form;
- there is a concrete reason to keep it.

When uncertain, do not merge it. Classify `UNKNOWN` and stop before destructive sync.

---

## Phase 2 — source reconciliation

If no installed-only behavior is worth preserving:

- make no functional source changes;
- proceed to testing and synchronization.

If one or more installed-only behaviors must be preserved:

1. Merge them into the source repo first.
2. Make the smallest possible source diff.
3. Prefer generic policy/config wording over host/model-specific special cases.
4. Do not copy the installed file wholesale over source.
5. Do not restore obsolete lifecycle instructions.
6. Do not weaken the 2026-09-08 fail-fast policy.
7. Do not reintroduce:
   - `followup_task` as callable V1 tool;
   - `list_agents` as callable V1 tool;
   - `interrupt_agent` as callable V1 tool;
   - repeated alias guessing;
   - compensatory shell/Get-Date/log/file polling;
   - same-scope replacement spawn after lifecycle unsupported.

Show the source diff before sync and explain why each functional change is necessary.

If there is no justified functional source change, say so explicitly.

---

## Phase 3 — source validation before touching installed copy

Run the repository's existing targeted checks, at minimum:

```text
python scripts/audit_policy.py
```

Also run any other existing lightweight repository checks directly relevant to files changed in Phase 2.

Verify structurally that:

- `config/worker_defaults.yaml` exists and contains required worker model/default fields;
- all references linked by `SKILL.md` exist;
- fail-fast policy is present;
- `Wait timed out.` remains distinct from `unsupported call`;
- only live declared V1 lifecycle names are instructed as callable;
- no forbidden orchestration runtime files were introduced.

Do not expand into unrelated broad testing.

If source validation fails, stop. Do not sync the installed copy.

---

## Phase 4 — create rollback snapshot of installed copy

Before replacing any installed file:

1. Create a timestamped backup under a D: path, preferably:

`D:\Temp\mode2_skill_install_backup_<timestamp>`

2. Copy the entire installed skill directory there preserving relative paths.
3. Record a manifest with SHA256 hashes.
4. Verify the backup contains every installed file.
5. Write a short `ROLLBACK.txt` with exact restore commands/procedure.

Do not use the source repo as the backup location.

---

## Phase 5 — synchronize installed copy

Only after Phases 1–4 are complete:

1. Synchronize the installed skill directory to the authoritative reconciled source.
2. The installed copy should become a file-for-file mirror for the actual skill payload.
3. Include missing source content such as `config/worker_defaults.yaml`.
4. Remove stale install-only files only when they were explicitly classified `DROP` in Phase 1.
5. Do not remove anything classified `UNKNOWN`.
6. Do not blindly copy repo-only development/history artifacts that are not part of the installed skill payload if the current installation convention excludes them; determine the existing install layout first.

After sync, compare content hashes for every installed payload file against source.

Required result:

```text
INSTALLED_COPY_MATCHES_SOURCE_PAYLOAD: YES
```

If not, stop and restore the install backup unless the mismatch is explicitly explained as an intentional non-payload repository file.

---

## Phase 6 — installed-copy validation

Run policy validation against the installed copy itself, not only source.

At minimum prove:

- installed `SKILL.md` includes fail-fast behavior;
- installed current V1 callable lifecycle names are correct;
- installed copy does not instruct callable `followup_task`, `list_agents`, `interrupt_agent`;
- installed `config/worker_defaults.yaml` exists and parses correctly;
- installed references resolve;
- installed audit policy passes using an appropriate invocation from the installed directory.

Then perform one bounded Mode 2 smoke using the normal installed skill path.

Smoke objective:

- one Worker only;
- simple named marker task;
- verify Worker spawn succeeds when provider emits a supported/restorable identity;
- verify Brain does not duplicate Worker scope;
- if `Wait timed out.` occurs, it may re-wait normally;
- if a lifecycle `unsupported call` occurs, verify no alias guessing, same-scope respawn, Get-Date loop, shell polling, or repeated unsupported retry;
- consume a completion notification/result if one arrives;
- stop within a bounded number of lifecycle/tool actions.

This is a behavior check, not a stress test.

Do not test web_search in this task.

---

## Phase 7 — Git and report

If source files changed functionally:

- commit those source changes separately with a focused message.

Then add a report:

`reports/INBOX_20260908_reconcile_installed_mode2_skill_and_sync.md`

Report at minimum:

```text
TASK_STATUS:
SOURCE_HEAD_BEFORE:
SOURCE_HEAD_AFTER:
INSTALLED_COPY_CONFLICT_CONFIRMED:
INSTALLED_ONLY_FILES:
INSTALLED_ONLY_BEHAVIORS_REVIEWED:
PRESERVED_BEHAVIORS:
DROPPED_STALE_BEHAVIORS:
UNKNOWN_BEHAVIORS:
SOURCE_FUNCTIONAL_CHANGE_REQUIRED:
FAIL_FAST_POLICY_PRESERVED:
WORKER_DEFAULTS_PRESENT_SOURCE:
WORKER_DEFAULTS_PRESENT_INSTALLED:
INSTALLED_BACKUP_DIR:
INSTALLED_BACKUP_VERIFIED:
INSTALLED_COPY_SYNCED:
INSTALLED_COPY_MATCHES_SOURCE_PAYLOAD:
SOURCE_POLICY_AUDIT:
INSTALLED_POLICY_AUDIT:
NORMAL_MODE2_SMOKE:
UNSUPPORTED_FAIL_FAST_SMOKE:
CPA_CHANGED:
PRODUCTION_8317_CHANGED:
WEB_SEARCH_CHANGED:
V2_CHANGED:
ROLLBACK_USED:
NEXT_MINIMAL_ACTION:
```

Commit and push all intended source/report changes to `main`.

Verify the remote branch points to the final commit.

---

## Success criteria

This task succeeds only if:

1. every previously independent installed edit was explicitly classified;
2. no useful current behavior was lost silently;
3. stale historical rules were not preserved merely for compatibility nostalgia;
4. source remains authoritative;
5. installed payload matches source after reconciliation;
6. fail-fast behavior is present in the installed copy;
7. worker defaults/config are present in the installed copy;
8. policy audit passes on source and installed copy;
9. one bounded normal Mode 2 smoke passes or gives a clearly provider-limited result without loop;
10. no CPA/web_search/V2/runtime changes were made.

---

## Stop conditions

Stop without destructive sync if any of the following occurs:

- an installed-only behavior is still `UNKNOWN` and could be important;
- source repo has conflicting unrelated uncommitted changes that cannot be isolated;
- source validation fails;
- installed backup cannot be verified;
- current installation layout cannot be determined safely;
- synchronizing would require overwriting unrelated local user assets;
- current live Codex tool inventory materially contradicts the current source assumptions.

In that case, report the exact conflict and the smallest next action. Do not broaden the task.
