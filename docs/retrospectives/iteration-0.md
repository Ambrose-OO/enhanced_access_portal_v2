# Iteration 0 retrospective

Date: 2026-08-13

Iteration goal: establish the DevOps pipeline against the inherited IEAP codebase

Outcome: pipeline operational and enforced; five gates running on every push
and pull request

| What went well? | What went less well? | What do we want to try next? | What puzzles us? |
| --- | --- | --- | --- |
| A gated CI pipeline was delivered and merged, running build, static analysis, security and test gates on every push and pull request. | The Python version in the local environment had drifted from the project target, which caused three separate failures before it was identified and resolved. | Harden the settings module by reading the debug flag and allowed hosts from the environment, as ADR-0005 records for the secret key. | Whether the project can remain on Django 3.1.5 for the duration, given that pip-audit reports twenty known vulnerabilities and the count can only grow. |
| Each gate failure was diagnosed and resolved, and the reasoning behind each decision was recorded as an architecture decision record. | The pipeline was built before a working local environment existed, so early failures were only visible through CI, which slowed each attempt to several minutes. | Run the gates locally before pushing, now that the environment matches the target, so failures are found in seconds rather than minutes. | |
| The security gate found a hardcoded secret key in a public repository, a genuine and exploitable defect in inherited code. | Two decisions were deferred rather than resolved, being the unused import findings and the dependency vulnerabilities, both accepted on time grounds. | | |

## Improvement actions carried into Iteration 1

1. Verify all gates locally before pushing, using the commands recorded in the
   README.
2. Harden the settings module for the debug flag and allowed hosts, ahead of
   the Render deployment.

## Deferred to the backlog

1. Remove unused imports and delete the F401 entry from the ruff ignore list
   (ADR-0003).
2. Raise the coverage threshold above