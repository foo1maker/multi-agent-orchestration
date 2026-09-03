# Brain-Authored Task Contracts

Brain must understand and compress the assignment before delegation. Never
raw-forward the user's original long prompt to a Worker.

Use this schema. For any Worker that will search, read, or write more than a
handful of already-named files, `OBJECTIVE`, `SCOPE & TARGETS`, `DELIVERABLES`,
`STOP`, and `ACCEPTANCE` are required. Omit only empty ceremonial sections.

```text
OBJECTIVE
TASK_MODE: EXECUTION | ANALYSIS | REVIEW
EXECUTION_KIND: IMPLEMENT | EXECUTE
SCOPE & TARGETS
INPUTS / CONTEXT_REFS
EXECUTION
DELIVERABLES
CONSTRAINTS
STOP
ACCEPTANCE
```

Omit empty or ceremonial sections for trivial contracts. `TASK_MODE` is
recommended, not mandatory. Do not invent execution steps for an open-ended
analysis task. `EXECUTION_KIND` is required when `TASK_MODE` is `EXECUTION`
and the work both changes code and runs a live expensive backend.

## Task Modes

**EXECUTION** covers code changes, file processing, data transforms, commands,
artifact generation, tests, and deterministic queries. Once the next concrete
action is clear, execute it. If a new scientific, architectural, or permission
decision is required, return a structured `BLOCKED` result to Brain. When the
work mixes new or changed code with a live expensive backend, split it as
specified below instead of one combined EXECUTION contract.

**ANALYSIS** covers source understanding, literature comparison, data exploration,
and local analytical reasoning. The Worker delivers key results, evidence, and
limitations; project-level scientific judgment and final ranking remain with Brain.

**REVIEW** is read-only unless Brain explicitly authorizes edits. Reviewers and
inspectors do not modify the object they are assessing by default.

## Deliverable-first

The named `DELIVERABLES` file is the work. Gathering is only to fill it.

As soon as the Worker has the facts `ACCEPTANCE` requires, the next action is
write that file and settle. Remaining unchecked items go in `ISSUES`. Do not
start another verification pass, hash pass, or full-table scan after those
facts are in hand.

A successful command is not a reason to run it again. If the same executable
and purpose already returned, use that result or settle `BLOCKED`.

## IMPLEMENT vs EXECUTE

A live expensive backend is any real model, oracle, GPU job, full benchmark,
or long production pipeline that is not a fake, stub, or recorded fixture.

If the assignment needs both new or changed code and a live expensive backend,
Brain writes two contracts, never one:

- **IMPLEMENT**: change code and prove it with cheap tests that use a fake,
  stub, or recorded fixture. Acceptance is those tests green. The Worker must
  not call the live expensive backend.
- **EXECUTE**: run the live backend only after IMPLEMENT settled `SUCCESS`.
  Acceptance is the named run artifacts. The Worker must not change search,
  scoring, or algorithm code. Fail closed with `BLOCKED` or `ERROR`.

A single EXECUTION contract is allowed only when there is no such mix: a pure
run of existing code, or a pure edit with no live expensive backend.

## Stop conditions

Brain must paste this `STOP` block into every contract. Workers follow it
even if Brain omits it. The last two bullets apply only to `TASK_MODE:
EXECUTION`.

```text
STOP
- Same command 3 times (same executable and purpose; ignore print-only diffs) → settle BLOCKED with that command.
- ACCEPTANCE facts already in hand and the named deliverable is still unwritten → write it now or settle BLOCKED. No further probes.
- 5 minutes with no named contract deliverable on disk → settle BLOCKED with evidence in hand.
- A required named path is missing → settle BLOCKED. Do not broaden into an unnamed repository search.
- Recursive listing or scanning of the project root, or of any directory not named in SCOPE & TARGETS, → settle BLOCKED.
- Same failing hypothesis 2 attempts → write a minimal failing test, fix it, re-run that test. No further probes. (EXECUTION)
- Do not debug by loading the production entrypoint via importlib, exec_module, or an equivalent whole-program REPL. (EXECUTION)
```

These are Worker self-stop rules that produce a settled `BLOCKED` packet. They
are not Brain watchdogs and do not weaken Running Worker Immunity.

## Contract Rules

- `SCOPE & TARGETS` must list concrete existing paths, or say that a required
  path is unknown and the Worker must settle `BLOCKED`. "Locate", "discover",
  or "live-read authority files" without those paths is not a SCOPE.
- A directory in SCOPE is a listing bound (names and sizes only). Reading,
  hashing, or row-counting file contents is allowed only for files listed by
  full path. Do not write "inspect this package recursively" when a manifest,
  hash list, or summary file can answer ACCEPTANCE.
- Name the files, paths, inputs, and permissions the Worker may use. Put those
  facts in the contract text; do not assume the Worker can see parent history.
- `DELIVERABLES` names one output file, or a short explicit list. Writing it
  is settlement.
- `ACCEPTANCE` is a closed checklist of named facts (paths, counts, hashes
  already stored in SCOPE files), not "enough evidence to proceed".
- Give the Worker only the context it needs.
- Do not let the Worker become a second Brain or choose a new workflow round.
- If required input is absent, or a STOP rule fires, the Worker may settle with:

```text
RESULT_PACKET
STATUS: BLOCKED
ISSUES: <specific missing input, decision, or stop condition>
```

This `BLOCKED` value is a text protocol status, not a native child lifecycle.
