# Iteration 1 retrospective

Date: 2026-08-20

Iteration goal: deliver the application to a hosted environment and gate that
delivery behind the CI pipeline

Outcome: application deployed to Render and reachable publicly; deployment now
occurs only after all quality gates pass, followed by an automated smoke test

| What went well? | What went less well? | What do we want to try next? | What puzzles us? |
| --- | --- | --- | --- |
| The continuous delivery half of the lifecycle is now operational. A merge to the deployment branch runs the gates, triggers a Render deploy through a deploy hook, and verifies the live site with a post-deploy smoke test. | Three separate failures were caused by configuration that was correct locally but wrong in the target environment: the Render root directory, the production dependencies missing from the requirements file, and the workflow working directory applying to a job that performs no checkout. | Address the OWASP security requirements of the brief, beginning with the cross site request forgery token finding surfaced by the smoke test output. | Whether the fixed ninety second wait before the smoke test will remain sufficient, given that build duration and cold start time both vary. |
| Settings were hardened for production, with the debug flag and allowed hosts read from the environment, so error pages no longer disclose internal detail on the public site. | The manifest static file storage was applied unconditionally, which broke the test gate in CI because no static files had been collected there. It was resolved by applying that storage only when the debug flag is off. | Add monitoring and alerting, so that the Operate and Monitor stage of the lifecycle is evidenced rather than described. | |
| Auto-deploy was disabled in favour of a pipeline triggered deploy hook, which makes the continuous delivery claim accurate rather than aspirational. | The smoke test output printed the entire page body to the workflow log, making the run difficult to read. Resolved by discarding the response body. | | |

## Improvement actions carried into Iteration 2

1. Replace the hardcoded cross site request forgery token in the login page
   template with a token generated per request.
2. Review the remaining production settings for further disclosure or
   misconfiguration risks, as part of the OWASP work.

## Deferred to the backlog

1. Replace the fixed wait before the smoke test with a check against the Render
   API, so the pipeline responds to actual deploy completion.
2. Add a staging service, so that validation occurs against a deployed
   environment before production release.
3. Items carried forward from Iteration 0 remain open, the coverage threshold, the favicon URL pattern, and dependency
   vulnerabilities.

## Observations for the report

Every failure in this iteration shared a cause, which is that a configuration
assumption held on the developer machine did not hold elsewhere. The
requirements file omitted two packages that were installed locally; the static
storage setting depended on a directory that existed locally; the workflow
default assumed a checked out repository. None would have been found by reading
the code, and all were found within minutes by the pipeline or the host. This
is a concrete illustration of why environment parity is pursued through pinned
manifests and automated deployment rather than through documentation.

The distinction between deployment and release is also now demonstrable. The
deploy hook approach means the pipeline decides when code reaches the server,
and the gates decide whether the pipeline gets that far.