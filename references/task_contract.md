# Brain-Authored Task Contracts

Brain must understand the objective well enough to compress it into a bounded
Task Contract before delegation. This is contract-level understanding, not
execution-level reconnaissance: Brain does not need to locate every input,
inspect schemas, audit manifests, or read project data before the first spawn.
Unknown execution facts should become a bounded `DISCOVERY` contract rather
than a Brain-side reconnaissance phase. Never raw-forward the user's original
long prompt to a Worker.

Use this schema. For any Worker that will search, read, or write more than a
handful of already-named files, `OBJECTIVE`, `SCOPE & TARGETS`, `DELIVERABLES`,
`STOP`, and `ACCEPTANCE` are required. `DISCOVERY ROOTS` is required for
`TASK_MODE: DISCOVERY`. Omit only empty ceremonial sections.

```text
OBJECTIVE
TASK_MODE: EXECUTION | DISCOVERY | ANALYSIS | REVIEW
EXECUTION_KIND: IMPLEMENT | EXECUTE
SCOPE & TARGETS
DISCOVERY ROOTS
INPUTS / CONTEXT_REFS
EXECUTION
DELIVERABLES
CONSTRAINTS
STOP
ACCEPTANCE
```

Omit empty or ceremonial sections for trivial contracts. `TASK_MODE` is
recommended except that discovery work must explicitly use `TASK_MODE:
DISCOVERY`. Do not invent execution steps for an open-ended analysis task.
`EXECUTION_KIND` is required when `TASK_MODE` is `EXECUTION` and the work both
changes code and runs a live expensive backend.

## Task Modes

**EXECUTION** covers code changes, file processing, data transforms, commands,
artifact generation, tests, and deterministic queries. Once the next concrete
action is clear, execute it. If a new scientific, architectural, or permission
decision is required, return a structured `BLOCKED` result to Brain. When the
work mixes new or changed code with a live expensive backend, split it as
specified below instead of one combined EXECUTION contract.

**DISCOVERY** covers bounded reconnaissance needed to convert unresolved
execution facts into named inputs for later contracts. Typical work includes
locating authority/status files, manifests, schemas, package entries, existing
results, or other concrete inputs within explicitly named `DISCOVERY ROOTS`.
The Worker returns a named discovery manifest or report and stops; it does not
execute the downstream task, widen the search roots, or make project-level
scientific decisions. An unknown target path is allowed only in DISCOVERY, and
only when the contract gives concrete existing search roots, closed target
criteria, a named deliverable, and closed acceptance criteria.

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
- EXECUTION / ANALYSIS / REVIEW: a required named path is missing → settle BLOCKED. Do not broaden into an unnamed repository search.
- DISCOVERY: a named DISCOVERY ROOT is missing, or the target cannot be resolved inside the named roots under the contract criteria → settle BLOCKED. Never broaden the roots.
- Recursive content scanning is forbidden. DISCOVERY may recursively list names and metadata only inside named DISCOVERY ROOTS; other modes may list only directories explicitly named in SCOPE & TARGETS.
- Same failing hypothesis 2 attempts → write a minimal failing test, fix it, re-run that test. No further probes. (EXECUTION)
- Do not debug by loading the production entrypoint via importlib, exec_module, or an equivalent whole-program REPL. (EXECUTION)
```

These are Worker self-stop rules that produce a settled `BLOCKED` packet. They
are not Brain watchdogs and do not weaken Running Worker Immunity.

## Contract Rules

- For EXECUTION, ANALYSIS, and REVIEW, `SCOPE & TARGETS` must list concrete
  existing paths. If a required target path is unknown, use a separate
  DISCOVERY contract first rather than making Brain discover it or letting a
  downstream Worker broaden scope.
- For DISCOVERY, final target paths may be unknown, but `DISCOVERY ROOTS` must
  list concrete existing directories or repositories that bound the search.
  The contract must state exactly what is being located, what evidence
  distinguishes an authoritative or relevant target, and what resolved facts
  must be written to the deliverable. "Locate" or "discover" is valid only in
  this bounded DISCOVERY mode.
- A directory in non-DISCOVERY SCOPE is a listing bound (names and sizes only).
  Reading, hashing, or row-counting file contents is allowed only for files
  listed by full path. Do not write "inspect this package recursively" when a
  manifest, hash list, or summary file can answer ACCEPTANCE.
- A DISCOVERY Worker may recursively inspect names and metadata only inside the
  named DISCOVERY ROOTS. It may read candidate files after discovery only when
  their names, locations, or metadata plausibly match the contract's target
  criteria and only as needed to resolve the requested path/schema/authority
  facts. It must not bulk-read file contents, hash or row-count an entire
  package, or broaden to another root unless the contract explicitly names that
  operation and root.
- Name the files, paths, inputs, and permissions the Worker may use. For
  DISCOVERY, name the search roots and target criteria instead of inventing an
  unresolved target path. Put those facts in the contract text; do not assume
  the Worker can see parent history.
- `DELIVERABLES` names one output file, or a short explicit list. Writing it
  is settlement.
- `ACCEPTANCE` is a closed checklist. For non-DISCOVERY work it names the facts
  to verify from the scoped inputs; for DISCOVERY it names the target identities,
  paths, schema facts, authority markers, or other bounded facts that must be
  resolved. Never use "enough evidence to proceed" as acceptance.
- Give the Worker only the context it needs.
- Do not let the Worker become a second Brain or choose a new workflow round.
- If required input is absent, or a STOP rule fires, the Worker may settle with:

```text
RESULT_PACKET
STATUS: BLOCKED
ISSUES: <specific missing input, decision, or stop condition>
```

This `BLOCKED` value is a text protocol status, not a native child lifecycle.
