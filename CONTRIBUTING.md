# Contributing

Contributions are welcome when they preserve the core separation of responsibilities: Brain plans and judges, Workers execute bounded contracts, and the native Codex runtime owns agent lifecycle.

## Before changing runtime policy

1. Read `SKILL.md` and all files under `references/`.
2. State which behavior is being changed and why.
3. Distinguish host-specific observations from portable policy.
4. Avoid hard-coding local paths, credentials, private endpoints, or one maintainer's provider configuration unless the text is explicitly labeled as an environment-specific observation.
5. Do not introduce a custom scheduler, watchdog, heartbeat loop, completion database, or polling-based worker manager.

## Validation

Run the repository-local structural audit:

```bash
python scripts/audit_policy.py
```

If changing result-packet semantics, also exercise:

```bash
python scripts/lint_result_packet.py <packet-file>
```

When a change depends on a specific Codex/runtime version or provider, record the exact environment and treat the result as compatibility evidence rather than a universal guarantee.

## Pull requests

Keep changes scoped. A useful pull request should explain:

- problem and motivation;
- affected policy section(s);
- behavioral impact;
- validation performed;
- compatibility limitations or unresolved risks.

Do not include credentials, secret-bearing logs, private config snapshots, or unrelated machine-specific state.
