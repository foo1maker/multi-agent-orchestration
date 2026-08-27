# Brain-Authored Task Contracts

Brain must understand and compress the assignment before delegation. Never
raw-forward the user's original long prompt to a Worker.

Use this schema as a flexible template, not a hard runtime gate:

```text
OBJECTIVE
TASK_MODE: EXECUTION | ANALYSIS | REVIEW
SCOPE & TARGETS
INPUTS / CONTEXT_REFS
EXECUTION
DELIVERABLES
CONSTRAINTS
ACCEPTANCE
```

Omit empty or ceremonial sections for trivial contracts. `TASK_MODE` is
recommended, not mandatory. Do not invent execution steps for an open-ended
analysis task.

## Task Modes

**EXECUTION** covers code changes, file processing, data transforms, commands,
artifact generation, tests, and deterministic queries. Once the next concrete
action is clear, execute it. If a new scientific, architectural, or permission
decision is required, return a structured `BLOCKED` result to Brain.

**ANALYSIS** covers source understanding, scientific judgment, literature
comparison, architecture, and complex reasoning. Deliver key results, evidence,
and limitations without expanding scope.

**REVIEW** is read-only unless Brain explicitly authorizes edits. Reviewers and
inspectors do not modify the object they are assessing by default.

## Contract Rules

- Name the files, paths, inputs, and permissions the Worker may use.
- State the expected deliverable and observable acceptance evidence.
- Give the Worker only the context it needs.
- Do not let the Worker become a second Brain or choose a new workflow round.
- If required input is absent, the Worker may settle with:

```text
RESULT_PACKET
STATUS: BLOCKED
ISSUES: <specific missing input or decision>
```

This `BLOCKED` value is a text protocol status, not a native child lifecycle.
