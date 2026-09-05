# Security Policy

## Scope

Security concerns include credential exposure, unsafe command construction, privilege-boundary mistakes, secret-bearing logs, or orchestration behavior that can cause unintended writes outside an authorized task scope.

## Reporting

Do not place API keys, access tokens, private configuration snapshots, or other live credentials in a public issue.

If GitHub private vulnerability reporting is enabled for this repository, use it. Otherwise contact the maintainer privately through the GitHub account associated with this repository and provide only the minimum information needed to reproduce the issue.

If a credential has already been exposed, revoke or rotate it first; repository cleanup is not a substitute for credential rotation.

## Maintainer expectations

Security fixes should preserve provenance, avoid unrelated refactors, and document the affected boundary. Changes involving shell/process execution should prefer structured arguments over interpolated command strings and must not print secrets into logs or task artifacts.
