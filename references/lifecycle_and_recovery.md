# Native Lifecycle, Waiting, and Recovery

## Native Wait Discipline

After spawning, Brain may continue only with genuinely independent,
non-duplicative work whose execution is required for a current decision. The
test is whether the action is needed now to decide something, not whether it
merely avoids duplicating a Worker. When no such work exists, enter
quiescent wait: call the live session's declared wait tool and do not invent
commands to stay busy.

The declared wait tool is an ANY-child mailbox wait, not an all-workers
barrier. One child settlement does not mean the parallel batch is complete.
Consume the settled result, make any immediate decision it requires, and
re-wait while other live Workers remain.

When the live wait tool schema exposes `timeout_ms`, pass an integer near
5 minutes (`300000`) when the schema maximum allows it; otherwise pass the
schema-reported maximum. If it exposes `target`, `targets`, or `agents`, pass
the still-live Worker names rather than an empty wait. Do not invent
parameters the schema does not list, and do not pass a JSON float. Omitting
`timeout_ms` uses the configured default. A longer window only reduces
wakeups; timeout semantics are unchanged.

## Unsupported Call Fail-Fast

A concrete `unsupported call` is a hard capability/dispatch boundary for that
attempted tool identity in the current task state. Brain must not keep trying
alternate spellings, namespace forms, aliases, or repeated calls for the same
semantic action merely to make the runtime accept it.

This is not `Wait timed out.`. A normal native wait timeout remains a wait
wakeup only. Only an actual dispatch/capability failure such as
`unsupported call: ...` triggers this hard boundary.

After the first concrete unsupported dispatch for a semantic action:

- do not retry that action under guessed bare, dotted, namespaced, or alias
  identities;
- do not repeat the same unsupported call;
- do not invent any tool name the live session does not declare as a
  substitute;
- do not start shell, `Get-Date`, log, file, repo, or progress loops merely to
  stay busy.

### A. Spawn was not confirmed

If the live declared spawn action returns `unsupported call` and no Worker
was confirmed:

- treat that spawn as failed;
- do not retry the same semantic spawn under guessed/bare/dotted/renamed
  identities;
- do not enter wait for a nonexistent Worker;
- do not quietly execute the delegated Worker scope in Brain merely because
  delegation failed;
- report `BLOCKED` or use an already-defined non-delegated path only when the
  task/user explicitly permits that fallback.

Re-issuing a rejected parallel wrapper as individual live declared spawn
calls is allowed only when the wrapper itself was rejected and nothing was
created. It is not permission to mutate the spawn tool identity. A
reasoning-effort rejection on the same model may still be retried once with a
supported effort. An `unsupported call` on spawn is not an effort retry.

### B. Worker was already confirmed live

If a Worker was successfully created and a later lifecycle action (any live
declared lifecycle tool, such as wait, steering, resume, or shutdown) returns
`unsupported call`:

- do not create replacement Workers for the same scope;
- do not mutate the tool identity and retry variants;
- do not take over the live Worker scope;
- do not perform compensatory polling or shell activity merely to stay busy;
- consume a native completion notification/result if it arrives — the native
  wait lifecycle can deliver a completion notification even when an
  explicit wait call is later rejected;
- if the runtime leaves no safe declared lifecycle action to proceed, stop
  further orchestration attempts and report the precise degraded/`BLOCKED`
  state rather than looping.

### C. `Wait timed out.` remains different

`Wait timed out.` means only that the current wait operation expired. It is
not a Worker failure, not an `unsupported call`, and not this fail-fast
boundary. When it returns with no Worker settlement, no native failure, no
Worker request for input, no new user input, and no concrete new error
evidence, immediately call the declared wait tool again unless the five-minute
named-output check below is due.

### D. Non-lifecycle unsupported tools

If an unrelated tool such as search returns `unsupported call`:

- do not retry the same unsupported identity repeatedly;
- do not guess aliases or alternate spellings;
- do not launch unrelated command loops merely to compensate;
- continue only with genuinely supported work that still advances the user
  goal and does not pretend the missing capability succeeded;
- if that capability is required for correctness, report `BLOCKED`/insufficient
  evidence.

Do not implement a search compatibility layer from this rule.

## Spawn Confirmation

Parallel spawning of independent Workers is allowed and normal. Whatever call
form is used, read every native result: a rejected, errored, or unconfirmed
spawn creates no Worker even though the call appeared to request one. A
parallel or multi-tool wrapper that the runtime rejects (for example an
unsupported parallel batch wrapper) creates nothing; when a wrapper form is
rejected, re-issue those spawns as individual spawn calls declared by the
live session rather than assuming anything was created. The same
confirmation discipline applies to any other batched native agent call.

A Worker exists only after the native runtime confirms the spawn. A rejected,
errored, or unconfirmed spawn result means that Worker does not exist. If a
spawn is rejected because the requested reasoning effort is unsupported for the
target model, re-issue that spawn once with a supported effort. If every spawn
in the round failed from contract or effort issues, nothing is live: correct
the contracts and re-spawn, or stop and report `BLOCKED` or `ERROR`. If the
spawn failure was `unsupported call`, follow case A; do not re-spawn under a
guessed identity. Never enter quiescent wait for a round in which no Worker
was confirmed.

`Wait timed out.` means only that the current wait operation expired. It is not
a Worker task timeout, failure, stall, token-budget signal, or recovery trigger.
When it returns with no Worker settlement, no native failure, no Worker request
for input, no new user input, and no concrete new error evidence, immediately
call the declared wait tool again unless the five-minute named-output check
below is due.
The only action allowed between those waits is that named-output check. Insert
no other progress-related or speculative execution: no `git status` or repo
scan, no listing of unnamed directories, no log or database read, no external
progress query, no undeclared listing tool, no checksum, no early test of
unsettled artifacts, no speculative Stage 2 or validation checklist, no
next-round preparation, no reread of the same policy, no `Get-Date` or other
time probe, and no doing part of a live Worker's task.

Do not call a lifecycle name the live session does not declare; the formal
Mode 2 route does not depend on undeclared listing tools. Consecutive silent
timeouts are not permission to invent a listing, close, or respawn action.
Consume a native completion or failure notification if one arrives. If
the declared wait tool itself returned `unsupported call`, follow case B
above instead of waiting, listing, or spawning a replacement Worker.

## Five-Minute Output Check

Every ~5 minutes of consecutive silent wait — no settlement, no native
failure, no Worker input request, and no new user input — Brain checks once
whether each still-running Worker has produced its named contract outputs.

Count elapsed wait in Brain's reasoning from the last settlement, native
failure, user input, or previous output check. Do not write a timer file. If
each wait window is shorter than 5 minutes, run the check when
consecutive timeouts sum to at least 5 minutes.

The check reads only paths named in that Worker's `DELIVERABLES` /
`ACCEPTANCE` / `SCOPE & TARGETS` outputs: existence and nonempty. Do not
read file contents, do not scan the repository, and do not inspect unnamed
paths.

- Named output exists: re-wait. Do not start Stage 2 on unsettled artifacts.
- No named output: if the live schema declares a steering tool, send one
  queued steering call (`target` = that Worker id, `message` = write the named
  deliverable now from evidence already in hand, with no further probes except
  that write, then settle `SUCCESS`, `PARTIAL`, or `BLOCKED`; omit
  `interrupt`).
  Then re-wait. Repeat this check every ~5 minutes while that Worker stays
  live and unsettled. The five-minute nudge uses the currently declared
  steering tool of the live session, and do not treat it as a renamed alias of
  an undeclared name.

This check does not authorize shutdown or takeover and is not Worker failure
evidence. Repeat it on the same cadence; do not poll faster. If the steering
call returns `unsupported call`, follow case B; do not retry variants.

Brain thinking is internal and does not require tool calls. Shell commands,
repo inspections, file reads, tests, data transforms, and external calls are
not required merely because a wait returned, except the audits in this file.
"No new decision; live Workers remain; wait again" is a correct state, not an
idle failure.

Quiescent wait does not freeze Brain. After a settlement, native failure,
Worker `BLOCKED`/request for input, or new user steering, resume decision work.
Process only the settled result. If it does not change still-running Workers,
re-wait rather than inspecting or pre-validating them.

`Wait interrupted by new input.` means user or steered input returned control.
Handle the new input, then reassess live Workers. Do not cancel them by default.

User steering that the turn is stuck (`卡住`, `卡了`, `stuck`, and similar)
is not elapsed-time failure evidence. On that first phrasing, run the
named-output check immediately rather than waiting for the five-minute cadence.
Workers with no named output get the write-now steering call above. Do not
shutdown a Worker on that first phrasing alone.

A second, explicit kill (`真的卡了`, `还是卡住`, `停掉`, `杀掉`, stop/kill
the workers) is condition 1 below. Close only Workers that still have no named
deliverable, using the live session's declared shutdown tool. Then read that
close result before doing anything in their SCOPE.

Do not build barriers, counters, status files, heartbeat files, or progress
monitors around native waiting. Do not inspect files, directories, logs,
processes, database rows, external APIs, token use, reasoning duration, or
repeated listings merely to estimate progress, except the five-minute
named-output check above.

## Running Worker Immunity

```text
elapsed time != failure evidence
no artifact yet != failure evidence
high reasoning usage != failure evidence
Wait timed out. != Worker failure evidence
```

A live Worker is allowed to remain `running`. Do not replace or interrupt it
merely for slowness. The five-minute named-output check is the only scheduled
nudge: missing named outputs get one queued steering call that cycle; existing
named outputs get none. Artifacts remain acceptance evidence after
settlement, not a reason to start Stage 2 early.

## Recovery

Recovery follows a settled insufficient result or concrete failure evidence:

```text
settled result insufficient
-> existing Worker context still useful? yes: live declared steering tool
-> otherwise: new Worker
```

Use the live declared lifecycle tools exactly as the current runtime exposes
them. Do not invent or translate tool identities in the skill. Call the
session's declared steering tool for in-turn steering; do not treat it as a
renamed alias of another undeclared name, and do not call undeclared tools for
steering.

Recovery may also follow a native terminal failure, a verified contract
violation, or an explicit user change of direction. Do not trigger recovery
solely from elapsed time, token use, no artifact, reasoning duration, a wait
timeout, or an `unsupported call`. An `unsupported call` follows the fail-fast
rule above, not this recovery fork.

Shutdown is exceptional. Use the live session's declared shutdown tool; do
not call undeclared shutdown alternatives unless the live session explicitly
declares them. Shutdown only when at least one concrete condition
applies:

1. The user explicitly requests stop or redirection, including a second
   stuck/kill steering after the write-now steering call above.
2. The Worker explicitly reports it cannot continue.
3. Native lifecycle confirms a terminal failure such as `errored`,
   `interrupted`, or `shutdown`.
4. Direct evidence shows the Worker is executing the wrong objective.
5. Direct evidence shows it crossed a clear contract boundary.
6. A dangerous, destructive, or unauthorized operation is occurring.
7. A user-specified hard deadline in the Task Contract has actually fired.

Do not add hard time or token watchdogs. Native lifecycle remains authoritative.

An empty steering result is not proof the Worker received it. Do not retry
in a tight loop. Re-wait until the next output check or user steering. If the
steering call returns `unsupported call`, follow case B.

After shutdown, read the close result. `previous_status: running` on that
result is not death. If native completion or a still-running indication
remains, do not start the same SCOPE on the main thread, and do not assume the
child is idle. Report that it is still live. Only take over that SCOPE after
native status is `interrupted`, `shutdown`, `errored`, or `completed`.
