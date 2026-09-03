# Native Lifecycle, Waiting, and Recovery

## Native Wait Discipline

After spawning, Brain may continue only with genuinely independent,
non-duplicative work whose execution is required for a current decision. The
test is whether the action is needed now to decide something, not whether it
merely avoids duplicating a Worker. When no such work exists, enter
quiescent wait: call native `wait_agent` and do not invent commands to stay
busy.

`wait_agent` is an ANY-child mailbox wait, not an all-workers barrier. One child
settlement does not mean the parallel batch is complete. Consume the settled
result, make any immediate decision it requires, and re-wait while other live
Workers remain.

When the live `wait_agent` schema exposes `timeout_ms`, pass an integer near
5 minutes (`300000`) when the schema maximum allows it; otherwise pass the
schema-reported maximum. If it exposes `target`, `targets`, or `agents`, pass
the still-live Worker names rather than an empty wait. Do not invent
parameters the schema does not list, and do not pass a JSON float. Omitting
`timeout_ms` uses the configured default. A longer window only reduces
wakeups; timeout semantics are unchanged.

## Spawn Confirmation

Parallel spawning of independent Workers is allowed and normal. Whatever call
form is used, read every native result: a rejected, errored, or unconfirmed
spawn creates no Worker even though the call appeared to request one. A
parallel or multi-tool wrapper that the runtime rejects (for example an
unsupported `multi_tool_use.parallel` batch) creates nothing; when a wrapper
form is rejected, re-issue those spawns as individual `spawn_agent` calls
rather than assuming anything was created. The same confirmation discipline
applies to any other batched native agent call.

A Worker exists only after the native runtime confirms the spawn. A rejected,
errored, or unconfirmed spawn result means that Worker does not exist. If a
spawn is rejected because the requested reasoning effort is unsupported for the
target model, re-issue that spawn once with a supported effort. If every spawn
in the round failed, nothing is live: correct the contracts and re-spawn, or
stop and report `BLOCKED` or `ERROR`. Never enter quiescent wait for a round in
which no Worker was confirmed.

`Wait timed out.` means only that the current wait operation expired. It is not
a Worker task timeout, failure, stall, token-budget signal, or recovery trigger.
When it returns with no Worker settlement, no native failure, no Worker request
for input, no new user input, and no concrete new error evidence, immediately
call `wait_agent` again unless a scheduled audit below is due. The only actions
allowed between those waits are the empty-set audit and the five-minute output
check. Insert no other progress-related or speculative execution: no `git
status` or repo scan, no listing of unnamed directories, no log or database
read, no external progress query, no extra `list_agents`, no checksum, no early
test of unsettled artifacts, no speculative Stage 2 or validation checklist, no
next-round preparation, no reread of the same policy, and no doing part of a
live Worker's task.

## Empty-Set Audit

Quiescent wait can only settle something if at least one confirmed Worker is
live. On an empty or fully terminal agent set, `wait_agent` returns nothing but
timeouts forever, so consecutive silent timeouts are the one signal that
justifies a native lifecycle check:

- After two consecutive `wait_agent` timeouts with no settlement, no native
  failure, no Worker input request, and no new user input, call `list_agents`
  once.
- If any Worker is still `running`, resume quiescent wait immediately. The
  audit reads native lifecycle state; it is not progress inspection, produces
  no failure evidence against a live Worker, and does not weaken Running
  Worker Immunity.
- If no live Worker remains — an empty listing, or every Worker `errored`,
  `interrupted`, or `shutdown` — stop waiting. Waiting cannot produce a
  settlement with no live Worker. Consume any results not yet processed, then
  follow Recovery, or report `PARTIAL`, `BLOCKED`, or `ERROR` when there is
  nothing to recover.

The timeout count is a scheduling cue for when to consult the native lifecycle.
It lives in Brain's reasoning only, never as a file, counter artifact, or
monitor. It never measures Worker progress, never infers failure from elapsed
time, and never authorizes `interrupt_agent` by itself.

## Five-Minute Output Check

Every ~5 minutes of consecutive silent wait — no settlement, no native
failure, no Worker input request, and no new user input — Brain checks once
whether each still-running Worker has produced its named contract outputs.

Count elapsed wait in Brain's reasoning from the last settlement, native
failure, user input, or previous output check. Do not write a timer file. If
each `wait_agent` window is shorter than 5 minutes, run the check when
consecutive timeouts sum to at least 5 minutes.

The check reads only paths named in that Worker's `DELIVERABLES` /
`ACCEPTANCE` / `SCOPE & TARGETS` outputs: existence and nonempty. Do not
read file contents, do not scan the repository, and do not inspect unnamed
paths.

- Named output exists: re-wait. Do not start Stage 2 on unsettled artifacts.
- No named output: send one `followup_task` telling that Worker to write the
  named deliverable now from evidence already in hand, with no further probes
  except that write, then settle `SUCCESS`, `PARTIAL`, or `BLOCKED`. Then
  re-wait. Repeat this check every ~5 minutes while that Worker stays live
  and unsettled.

This check does not authorize `interrupt_agent` and is not Worker failure
evidence. Repeat it on the same cadence; do not poll faster.

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
Workers with no named output get the write-now `followup_task` above. Do not
`interrupt_agent` on that first phrasing alone.

A second, explicit kill (`真的卡了`, `还是卡住`, `停掉`, `杀掉`, stop/kill
the workers) is condition 1 below. Interrupt only Workers that still have no
named deliverable. Then confirm native death with `list_agents` before doing
anything in their SCOPE.

Do not build barriers, counters, status files, heartbeat files, or progress
monitors around native waiting. Do not inspect files, directories, logs,
processes, database rows, external APIs, token use, reasoning duration, or
repeated `list_agents` calls merely to estimate progress, except the
five-minute named-output check above.

## Running Worker Immunity

```text
elapsed time != failure evidence
no artifact yet != failure evidence
high reasoning usage != failure evidence
Wait timed out. != Worker failure evidence
```

A live Worker is allowed to remain `running`. Do not replace or interrupt it
merely for slowness. The five-minute named-output check is the only scheduled
nudge: missing named outputs get one `followup_task` that cycle; existing
named outputs get none. Artifacts remain acceptance evidence after
settlement, not a reason to start Stage 2 early.

## Recovery

Recovery follows a settled insufficient result or concrete failure evidence:

```text
settled result insufficient
-> existing Worker context still useful? yes: followup_task
-> otherwise: new Worker
```

Recovery may also follow a native terminal failure, a verified contract
violation, or an explicit user change of direction. Do not trigger recovery
solely from elapsed time, token use, no artifact, reasoning duration, or a wait
timeout.

`interrupt_agent` is exceptional. Use it only when at least one concrete
condition applies:

1. The user explicitly requests stop or redirection, including a second
   stuck/kill steering after the write-now followup above.
2. The Worker explicitly reports it cannot continue.
3. Native lifecycle confirms a terminal failure such as `errored`,
   `interrupted`, or `shutdown`.
4. Direct evidence shows the Worker is executing the wrong objective.
5. Direct evidence shows it crossed a clear contract boundary.
6. A dangerous, destructive, or unauthorized operation is occurring.
7. A user-specified hard deadline in the Task Contract has actually fired.

Do not add hard time or token watchdogs. Native lifecycle remains authoritative.

An empty `followup_task` result is not proof the Worker received it. Do not
retry in a tight loop. Re-wait until the next output check or user steering.

After `interrupt_agent`, call `list_agents` once. `previous_status: running`
on the interrupt result is not death. If that Worker is still `running`,
native interrupt did not terminate it: do not start the same SCOPE on the
main thread, and do not assume the child is idle. Report that it is still
live. Only take over that SCOPE after native status is `interrupted`,
`shutdown`, `errored`, or `completed`.
