# Native Lifecycle, Waiting, and Recovery

## Native Wait Discipline

After spawning, Brain may continue only with genuinely independent,
non-duplicative work. When none exists, call native `wait_agent`.

`wait_agent` is an ANY-child mailbox wait, not an all-workers barrier. One child
settlement does not mean the parallel batch is complete. Consume the settled
result, make any immediate decision it requires, and re-wait while other live
Workers remain.

`Wait timed out.` means only that the current wait operation expired. It is not
a Worker task timeout, failure, stall, token-budget signal, or recovery trigger.
When Workers remain live and there is no new user input or concrete failure
evidence, call `wait_agent` again without progress inspection.

`Wait interrupted by new input.` means user or steered input returned control.
Handle the new input, then reassess live Workers. Do not cancel them by default.

Do not build barriers, counters, status files, heartbeat files, or progress
monitors around native waiting. Do not inspect files, directories, logs,
processes, database rows, external APIs, token use, reasoning duration, or
repeated `list_agents` calls merely to estimate progress.

## Running Worker Immunity

```text
elapsed time != failure evidence
no artifact yet != failure evidence
high reasoning usage != failure evidence
Wait timed out. != Worker failure evidence
```

A live Worker is allowed to remain `running`. Do not remind, replace, or
interrupt it merely for slowness. Artifacts are acceptance evidence after
settlement, not heartbeats during execution.

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

1. The user explicitly requests stop or redirection.
2. The Worker explicitly reports it cannot continue.
3. Native lifecycle confirms a terminal failure such as `errored`,
   `interrupted`, or `shutdown`.
4. Direct evidence shows the Worker is executing the wrong objective.
5. Direct evidence shows it crossed a clear contract boundary.
6. A dangerous, destructive, or unauthorized operation is occurring.
7. A user-specified hard deadline in the Task Contract has actually fired.

Do not add hard time or token watchdogs. Native lifecycle remains authoritative.
