# Status

COMPLETE — the installed Mode 2 skill copy was audited file-by-file, no installed-only behavior was worth merging into source, the whole installed directory was snapshotted on D:, and the skill payload was synchronized to the authoritative source. Installed payload hashes now match source. Policy audit passes on both trees. A bounded Mode 2 smoke that loaded the installed payload spawned one Worker, accepted the named marker, and fail-fasted a single `unsupported call: wait_agent` without alias guessing, respawn, or Get-Date filler.

```text
TASK_STATUS: COMPLETE
SOURCE_HEAD_BEFORE: 5fa5241059b3a1551678d09ddaef00777c28db17
SOURCE_HEAD_AFTER: 6958261d44c1b91b1ed12f9e75c707fb088cce15
INSTALLED_COPY_CONFLICT_CONFIRMED: YES
INSTALLED_ONLY_FILES: none (skill files); leftover scripts/__pycache__ bytecode only
INSTALLED_ONLY_BEHAVIORS_REVIEWED: YES
PRESERVED_BEHAVIORS: none
DROPPED_STALE_BEHAVIORS: DSFlash hardcoded worker default; callable followup_task; list_agents empty-set audit; host-hardcoded audit_policy.py paths; pre-fail-fast lifecycle text; CRLF-only task_contract.md
UNKNOWN_BEHAVIORS: none
SOURCE_FUNCTIONAL_CHANGE_REQUIRED: NO
FAIL_FAST_POLICY_PRESERVED: YES
WORKER_DEFAULTS_PRESENT_SOURCE: YES
WORKER_DEFAULTS_PRESENT_INSTALLED: YES
INSTALLED_BACKUP_DIR: D:\Temp\mode2_skill_install_backup_20260908_091158
INSTALLED_BACKUP_VERIFIED: YES (9/9 files, SHA256 match, ROLLBACK.txt present)
INSTALLED_COPY_SYNCED: YES
INSTALLED_COPY_MATCHES_SOURCE_PAYLOAD: YES
SOURCE_POLICY_AUDIT: PASS
INSTALLED_POLICY_AUDIT: PASS
NORMAL_MODE2_SMOKE: PASS (worker 01a07e99-5bb2-7a11-beaf-3620d430c05e; marker SYNC_MODE2_OK_K7Q2; Brain SMOKE_OK SYNC_MODE2_OK_K7Q2; one Worker)
UNSUPPORTED_FAIL_FAST_SMOKE: PASS (same run: unsupported call: wait_agent x1, no retry, no replacement spawn, no Get-Date command; completion consumed)
CPA_CHANGED: NO
PRODUCTION_8317_CHANGED: NO
WEB_SEARCH_CHANGED: NO
V2_CHANGED: NO
ROLLBACK_USED: NO
NEXT_MINIMAL_ACTION: none required for this conflict. C:\Users\1\.agents\skills is a junction to C:\Users\1\.codex\skills, so both paths now see the same synced payload.
```

Repo: `foo1maker/multi-agent-orchestration`
Worktree: `D:\Github\multi-agent-orchestration`
Branch: `main`
Task path: `tasks/2026-09-08_reconcile_installed_mode2_skill_and_sync.md`
Locator commit: `5fa5241059b3a1551678d09ddaef00777c28db17`

# Phase 0 — state

- Source HEAD before work: `5fa5241` = `origin/main`. Working tree clean except two unrelated untracked 2026-09-05 reports, which were left untouched.
- Fail-fast ancestor `3da84aa` is present.
- Installed path `C:\Users\1\.agents\skills\multi-agent-orchestration` exists.
- Layout discovery: `C:\Users\1\.agents\skills` is a Windows junction to `C:\Users\1\.codex\skills`. There is one physical skill payload, not two independent copies. This task edited that payload via the `.agents` path specified in the task.

Pre-sync hashes (installed):

```text
SKILL.md                               529c3e943bb61e8eb2519f8366378906b59236716dd7aee99dad5cec24fd8b28  DIFF
agents/openai.yaml                     6178869308c894f600946fd2f725628d9971972c85fc9118b266a97caea2ec43  SAME
references/lifecycle_and_recovery.md   5d20eb5bc75dee7ab1fe5137d39e50f897a26b3066fbf2d8e0e6d8bca27fcfce  DIFF (pre-fail-fast)
references/result_packet.md            5094a73cf2eb974524d78d16e452e9b333e9f7c2cca32cf5bbb1715257510c7a  SAME
references/task_contract.md            09ceee1f2ff68d701678e2c534349e7103f3971923fd316bf82ce0e1ca87284f  CRLF-only vs source
scripts/audit_policy.py                b6b3f8570327abe213e85b51d3fcdba00061c56a5ee0170d147f33ed68e9cd42  DIFF
scripts/lint_result_packet.py          cdb8d5a11b69071473bf1a7486468d6956c9096eb49f3dcacc70e5d518858cf8  SAME
config/worker_defaults.yaml            ABSENT from install; present in source
```

Source-only non-payload (not part of the installed skill convention): `.gitignore`, `README.md`, `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, `tasks/`, `reports/`. Those were not copied.

# Phase 1 — classification

```text
PATH
SOURCE STATE
INSTALLED STATE
ORIGIN IF IDENTIFIABLE
BEHAVIORAL EFFECT
CURRENT RELEVANCE
KEEP / MERGE / DROP / UNKNOWN
EVIDENCE

SKILL.md
current fail-fast + worker_defaults inherit routing + live V1 names
DSFlash default deepseek-v4-flash:0731; GLM visual exception; callable followup_task; list_agents audits; no fail-fast
local 2026-09-07 edit, matches no git SKILL.md blob
forces a host-specific Worker model; instructs undeclared V1 names; lacks unsupported-call hard boundary
stale. Persistent routing is already covered by config/worker_defaults.yaml. DSFlash hardcoding is host-specific nostalgia. Callable followup_task/list_agents contradict live V1 inventory.
DROP
installed routing vs source worker_defaults.yaml; live V1 tools[] from 2026-09-07/08; task forbids DSFlash hardcoding when the generic config covers the same need

scripts/audit_policy.py
portable --skill-dir default, worker_defaults audit, fail-fast required tokens
hardcoded C:\Users\1\.codex and D:\00_SYSTEM paths; DSFlash required tokens; no fail-fast group
companion to the local DSFlash SKILL
would fail or require host paths; would not protect fail-fast
stale
DROP
file diff; installed parse_args defaults

references/task_contract.md
LF content
same content with CRLF (156 CR bytes)
line-ending only
none
none
DROP (normalize to source LF)
identical after stripping CR

references/lifecycle_and_recovery.md
fail-fast cases A–D; send_input steering; close_agent shutdown; Wait timed out. kept distinct
pre-fail-fast text with followup_task / list_agents / interrupt_agent as callable
unmodified mirror of older source (mtime 2026-09-03)
would re-enable undeclared-tool recovery loops
stale relative to 3da84aa
DROP
hash 5d20eb5b vs source 52483c6c; installed lacks "unsupported call"

references/result_packet.md
current
byte-identical
n/a
none
KEEP
hash match

agents/openai.yaml
current
byte-identical
n/a
none
KEEP
hash match

scripts/lint_result_packet.py
current
byte-identical
n/a
none
KEEP
hash match

config/worker_defaults.yaml
present (model: inherit, reasoning_effort: auto)
absent
source 2026-09-05 portable routing
install could not resolve persistent Worker defaults
current; required
ADD FROM SOURCE (not an installed-only behavior)
source-only payload file

scripts/__pycache__/*.pyc
not in source payload
present
Python cache of old installed scripts
none once .py is newer
not skill behavior
KEEP as non-payload cache (not UNKNOWN; not copied from source)
```

DSFlash review: the installed rule intended a fixed cheap Worker model and a GLM visual exception. Source already provides a generic persistent default (`config/worker_defaults.yaml`) plus current-task override. Putting `deepseek-v4-flash:0731` into GitHub source would re-hardcode one host. Classified DROP. No merge.

No UNKNOWN. No justified source functional change.

# Phase 3 — source validation before sync

`python scripts/audit_policy.py` → PASS.

`config/worker_defaults.yaml` exists with `worker.model` / `worker.reasoning_effort`. SKILL.md references resolve. Fail-fast present. `Wait timed out.` remains distinct from `unsupported call`. Callable undeclared-tool instructions absent. No forbidden runtime files.

# Phase 4 — backup

```text
D:\Temp\mode2_skill_install_backup_20260908_091158\
  multi-agent-orchestration\   (full pre-sync tree, 9 files)
  SHA256SUMS.txt
  ROLLBACK.txt
```

Every installed file was present in the backup with matching SHA256. Rollback procedure is in `ROLLBACK.txt`. Backup was not used.

# Phase 5 — sync

Copied only the installed skill payload from source:

`SKILL.md`, `agents/openai.yaml`, `config/worker_defaults.yaml`, `references/*.md`, `scripts/audit_policy.py`, `scripts/lint_result_packet.py`.

Did not copy `tasks/`, `reports/`, or repo-root docs. Did not delete `__pycache__`.

Post-sync payload SHA256:

```text
SKILL.md                               5aa8f9e8681f9f783ec2aac4f43888644a260d1bf70f03464ea2ad97a468c020
agents/openai.yaml                     6178869308c894f600946fd2f725628d9971972c85fc9118b266a97caea2ec43
config/worker_defaults.yaml            ead931d6eb372cc85a39bf52dd8ee342f71bb38aa308a4a6c021ec89e40de44e
references/lifecycle_and_recovery.md   52483c6c77dd87fd1387c1221e338f10f2aa97eded65bdc943c4f88c7413717e
references/result_packet.md            5094a73cf2eb974524d78d16e452e9b333e9f7c2cca32cf5bbb1715257510c7a
references/task_contract.md            cc1096e8de6e8985fb0ed8f3d1441330c0f18e9c4e4e2b5839496100d17e67d3
scripts/audit_policy.py                a393c7036d38cf354c7a14cd3dd22962c41b1fb16f837a02792a4209b1be700c
scripts/lint_result_packet.py          cdb8d5a11b69071473bf1a7486468d6956c9096eb49f3dcacc70e5d518858cf8
```

All eight payload files match source.

`INSTALLED_COPY_MATCHES_SOURCE_PAYLOAD: YES`

# Phase 6 — installed validation and smoke

Installed `python scripts/audit_policy.py --skill-dir <installed>` → PASS.

Installed SKILL includes fail-fast, live V1 names (`spawn_agent`, `wait_agent`, `send_input`, `close_agent`, `resume_agent`), non-callable warnings for `followup_task`/`list_agents`/`interrupt_agent`, and `config/worker_defaults.yaml`.

Bounded Codex exec smoke used a real copy of that installed payload (byte-identical to `C:\Users\1\.agents\skills\multi-agent-orchestration`) under an isolated `CODEX_HOME` so production `.codex/config.toml` was not edited. Ceiling: 90s / 25 tools / 12 lifecycle / 3 spawns / 3 Get-Date.

Successful run (67.2s, abort none):

- one Worker `01a07e99-5bb2-7a11-beaf-3620d430c05e`
- spawn_agent succeeded
- `unsupported call: wait_agent` once; no wait_agent retry; native wait item then completed with Worker SUCCESS
- Brain Stage 2 read `marker.txt` via `Get-Content` (not a filler loop)
- marker bytes exactly `SYNC_MODE2_OK_K7Q2`
- Brain final: `SMOKE_OK SYNC_MODE2_OK_K7Q2`
- no followup_task, list_agents, replacement spawn, or Get-Date command

A first attempt that pointed isolated skills at the install path through a Windows junction was aborted after a spawn `unsupported call` retry burst and no Worker. That attempt is treated as a harness-path failure (junction), not as installed-payload behavior. The repeat with a real directory copy of the same installed bytes passed.

# Safety

- No source functional diff.
- CPA / 8317 / web_search / V2 / namespace restore / PR #5538 untouched.
- Unrelated untracked 2026-09-05 reports untouched.
- Isolated smoke config/auth stayed under `D:\Temp\mode2_reconcile_smoke_20260908` and is not committed.
