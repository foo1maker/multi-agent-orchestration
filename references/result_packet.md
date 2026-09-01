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
Brain Scientific Synthesis: synthesize evidence and make project-level judgment
Remaining-work check: determine whether substantial execution is still required
Stage 3: Decide whether the original objective is satisfied
```

Worker success is not task completion. Brain performs Stage 2 after settlement,
personally conducts scientific synthesis, and then makes the Stage 3 decision for
the original user objective.

Stage 2 checks the evidence proportional to risk: inspect the claimed artifact,
run focused tests, or verify critical claims. It does not redo the entire
delegated workflow unless reproduction is itself required by acceptance.
Mechanical artifact checks (such as file existence, row counts, JSON parsing, and
schema checks) can be delegated or spot-checked so Brain reserves its reasoning
budget for scientific judgment.

### Brain Scientific Synthesis

Scientific judgment is Brain-owned and must not be delegated. A Worker-generated
score, ranking, or recommendation is evidence, not a final decision. Brain must
not lock a scientific ranking solely because a Worker score table ordered
candidates in that way.

Before locking any major conclusion, ranking, route change, or delegating final
packaging, Brain must personally evaluate:
1. Which evidence matters most, and which is weak, biased, heterogeneous, or
   potentially misleading?
2. Does benchmark performance actually support the intended downstream use, or is
   a candidate merely technically easier to execute rather than scientifically better?
3. What is the strongest alternative explanation, and why does the preferred option
   beat nearest alternatives?
4. What realistic uncertainty could reverse this decision?

Brain records a concise decision rationale (decision, supporting evidence, key
weakness/trade-off, alternative comparison, confidence/uncertainty) without exposing
raw chain-of-thought.

### Packaging and Remaining Work

Before Stage 3 completion, Brain reassesses remaining work. If substantial execution
remains—such as formatting, figure generation, README/RUN_SUMMARY creation, packaging,
Git staging/commit/push, or external sync—Brain should delegate it to a packaging
Worker.

A packaging Worker may format and assemble Brain-approved conclusions, but must not
independently set or reinterpret the scientific ranking. Brain may provide the
approved ranking and rationale to the Worker for faithful packaging.

Brain may directly perform bounded validation and trivial execution without
spawning a Worker.

If evidence is incomplete, use the recovery rules in
[lifecycle_and_recovery.md](lifecycle_and_recovery.md). Preserve uncertainty and
report `PARTIAL`, `BLOCKED`, or `ERROR` rather than upgrading weak evidence to
success.
