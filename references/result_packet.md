# Result Packets and Completion

Workers return a concise structured result. Omit empty fields for trivial work.

```text
RESULT_PACKET
STATUS: SUCCESS | PARTIAL | BLOCKED | ERROR
SCOPE: ...
OUTPUTS: ...
KEY_RESULTS: ...
VALIDATION: ...
ISSUES: none | ...
CHANGES_OUTSIDE_SCOPE: none | ...
NEXT_RECOMMENDATION: ...
```

`RESULT_PACKET STATUS` is a Mode 2 text protocol. It is not the Codex native
child lifecycle, whose observed states may include `running`, `interrupted`,
`shutdown`, `completed`, `errored`, and `null`.

## Three-Stage Completion

```text
Stage 1: Worker Settlement
Stage 2: Validate evidence, artifacts, tests, and critical claims
Stage 3: Decide whether the original objective is satisfied
```

Worker success is not task completion. Brain performs Stage 2 after settlement
and then makes the Stage 3 decision for the original user objective.

Stage 2 checks the evidence proportional to risk: inspect the claimed artifact,
run focused tests, or verify critical claims. It does not reproduce the entire
delegated workflow unless reproduction is itself required by acceptance.

If evidence is incomplete, use the recovery rules in
[lifecycle_and_recovery.md](lifecycle_and_recovery.md). Preserve uncertainty and
report `PARTIAL`, `BLOCKED`, or `ERROR` rather than upgrading weak evidence to
success.
