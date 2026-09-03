# Iteration 2 retrospective

Date: 2026-09-02
Iteration window: 2026-08-25 to 2026-09-02 (`iteration-2/feature-fixes`, merged into `l6_dev_ops_main` via PR #58, plus follow-on commits after merge)

Iteration goal: fix application features, optimise and enhance areas of weakness.

Outcome: feature bugs found during self and SE&A testing were fixed, validation and usability messaging coverage was brought up to brief requirements, a deployed-only performance defect was diagnosed and fixed, CI and CD both pass, and live manual deployment tests worked out well.

| What went well? | What went less well? | What do we want to try next? | What puzzles us? |
| --- | --- | --- | --- |
| CD is now operational end to end: a merge to `l6_dev_ops_main` runs the CI gates, triggers a Render deploy through a deploy hook, and verifies the live site with a post-deploy smoke test. | Code modularisation is still at file level rather than package level — `resource_dashboard/views.py` remains one large file. Some cleanup did happen this iteration (shared validation helpers, a `throttle_action` decorator, JS split across `projects_shared.js`/`projects_admin.js`/`group_shared.js` by responsibility), so this is better described as partial/acceptable rather than not attempted. | Split `resource_dashboard/views.py` into logical modules (projects, groups, VMs, statistics) now that the validation and throttling helpers give it a natural seam to split along. | Why the ERR_INSUFFICIENT_RESOURCES defect was completely invisible locally. Same code, same database, same browser — the only difference was Render's single shared worker being slow enough for seven independent polling loops to actually overlap. It took Chrome's own Network tab, not our code or Render's logs, to make the defect visible at all. |
| Validation coverage and usability messaging were both weak points named directly in the brief and by SE&A; both were worked through this iteration (see rubric summary below). | Had to defer several nice-to-have features (account deletion, group renaming, password reset, communication features) due to time limitations and the fact that none are required by the brief. | Structured logging (5.5) — currently the app relies on scattered `print()` calls (as detailed below). | |
| A deployed-only performance defect (`ERR_INSUFFICIENT_RESOURCES` on the resource dashboard) was diagnosed from first principles — comparing local vs deployed behaviour and reading browser Network timings rather than guessing — and fixed without a full redesign. | | Revisit the combined-dashboard-endpoint idea if the dashboard is still sluggish after the interval/self-scheduling fixes below — deliberately not done this iteration (see Observations). | |
| Server-side query optimisation (the VM group add/remove flow specifically) measurably improved response times once it was confirmed the interval fix alone wasn't enough there. | | | |
| Pytest test coverage was added for the new validation, throttling, and the bugs fixed this iteration, wired into the existing CI coverage gate. | | | |

## Rubric self-assessment summary

Status colours below reflect the SE&A review, with team notes added where our own view differs slightly.

| # | Item | Status | Notes |
| --- | --- | --- | --- |
| 5.1 | Code cleaning | Amber (reviewed Red) | Genuine modularisation happened this iteration — validation logic and rate-limiting were pulled into shared, reusable functions (`is_blank_or_whitespace`, `name_length_error`, `throttle_action`) rather than repeated per view, and the JS was already split by responsibility across files. It has not reached package-level modularisation (see 5.1.1), which is the fair basis for the Red rating, but "no work done" would be inaccurate. |
| 5.1.1 | Code modularisation | Red | `resource_dashboard/views.py` is still one file covering projects, groups, VMs and statistics. Carried into Iteration 3 below. |
| 5.1.2 | Code readability & quality | Green | Naming conventions, shared constants (`PROJECT_NAME_MIN_LENGTH`, `BASE_POLL_TIME`, etc.), and de-duplicated validation logic across client and server. |
| 5.2.1–5.2.2 | Admin vs regular user capabilities | Green | Admin-only actions (remove project member, delete project, create/manage projects) are gated server-side by `user_type`; the corresponding UI controls are now also never rendered for a `USER` session rather than just hidden, closing off the affordance for regular users entirely. |
| 5.3.3 | Usability — success/failure messaging and delete confirmation | Green | `confirmation_prompt_user` is used before every delete; `prompt_user` now surfaces both application-level failures and network-level failures (previously several `.catch()` blocks only logged to the console, leaving the user with a stuck button and no message). |
| 5.3 | Database | Green | SQLite with sample records, appropriate types, and FK relationships kept deliberately simple per the brief — no restructuring attempted mid-project. |
| 5.4 | Validation | Green | Both invalid actions and non-conformant field data are now covered: blank/whitespace-only names, minimum and maximum length bounds, and duplicate names are rejected server-side (the authority) and mirrored client-side for instant feedback, on project creation, project rename, and group creation. |
| 5.5 | Error logging | Red | Still `print()`-based. Carried into Iteration 3 below. |
| 5.6 | Code testing | Green | Coverage gate already existed; this iteration added the first real `resource_dashboard` test suite (validation rules, throttling, and regression tests for the bugs described below) on top of the existing `login_page` test. |
| 6 | Operate & monitor | Withheld | No metrics/alerting tooling this iteration, by scope decision, not oversight — see Observations for what stood in for it. |

## Improvement actions carried into Iteration 3

1. Replace the hardcoded cross site request forgery token in the login page
   template with a token generated per request.
2. Review the remaining production settings for further disclosure or
   misconfiguration risks, as part of the OWASP work.
3. Split `resource_dashboard/views.py` into logical modules (projects,
   groups, VMs, statistics) now that shared validation/throttling helpers
   give it a natural seam.
4. Introduce structured logging (Python `logging`, with severity levels) in
   place of the remaining `print()` calls, starting with the views touched
   by this iteration's debugging work.

## Deferred to the backlog

1. Deeper levels of code modularisation beyond the Iteration 3 split above.
2. Monitoring and alerting, so that the Operate and Monitor stage of the
   lifecycle is evidenced rather than described.
3. Structured application logs (see Iteration 3 item 4).
4. Combining the resource dashboard's polling endpoints into a single
   endpoint returning all panel data in one response. Identified as a real
   improvement during the performance investigation below, but deliberately
   not implemented this iteration: the self-scheduling and interval changes
   already remove the failure mode it would solve, and it is a larger,
   riskier change touching every panel's JavaScript at once.

## Observations for the report

### Feature audit before this iteration's fixes

Before starting feature work, we treated "does it actually work" as
something to confirm rather than assume, given SE&A feedback had flagged
login as broken on the deployed site. The two items that turned out to be
real, brief-relevant defects were:

- **Admin add-member/add-VM visual bugs.** `ADMIN_PROMPT_add_user` was
  passing the full array of projects returned by the server straight into
  `update_project_display_with_project_data`, a function that expects a
  single project object and immediately iterates
  `project.project_vms_details` — throwing `TypeError: ... is not
  iterable` in the browser console and leaving the project detail panel
  stuck. Fixed by finding the matching project in the array first, the
  same pattern the sibling add/remove-VM handlers already used correctly.
- **Validation coverage and usability messaging**, named directly in the
  brief and weighted heavily in the rubric (5.4, 5.3.3). Addressed
  iteration-wide: see the rubric summary above.

Nice-to-have features (account deletion, group renaming, password reset,
communication features) were scoped out deliberately. As none are required
by the brief, and each adds validation and security surface area for no
rubric benefit.

### The ERR_INSUFFICIENT_RESOURCES investigation

Server-side response times were noticeably slower on the deployed Render
instance than locally, with no errors surfacing in the Render logs. The
first hypothesis — Render's free-tier single shared CPU and single
gunicorn worker being inherently slower than a local machine — was a
reasonable starting point but didn't fully explain what was being
observed, so it was tested rather than assumed: comparing a cold request
against an immediate repeat (to rule out container spin-up), and comparing
local `runserver` timings against the same action on Render (to isolate
host from code).

The actual defect was found through the browser, not the server: Chrome's
Network tab showed `net::ERR_INSUFFICIENT_RESOURCES` against a large
number of pending requests, a browser-side refusal to open more
connections, not a server error. Since the refused requests never left
the browser, nothing appeared in the Render logs, which is why the server
had looked innocent up to that point.

The root cause, once counted directly in the Network tab: the resource
dashboard ran seven independent polling loops (`update_all_vms`,
`update_statistics`, `update_groups_content`,
`update_available_group_vms_content`, `update_projects_content`,
`update_available_project_vms`, `update_available_project_users`), each
using `setInterval` on a fixed 1–3 second timer. `setInterval` fires
regardless of whether the previous request has completed. On a host where
a single request could take up to ~30 seconds under load, one slow
response was enough for a loop firing every second to queue roughly
30 outstanding requests before it — across seven loops, easily over a
hundred — until the browser's own connection limit refused further
requests. Locally, requests return in milliseconds, so the loops never
overlap and the failure mode simply never appears — which is what made
this invisible in local testing and only surface under deployed
conditions.

**What was fixed, and in that order:**

1. **Self-scheduling instead of fixed-interval polling.** Every loop was
   converted from `setInterval` to a pattern where the loop's own
   `.finally()` schedules the *next* call only once the current request has
   settled (commit `b9862af` introduced the pattern and the shared
   `BASE_POLL_TIME` constant; extended to the remaining loops in
   `2e36850`, `fb420d2`, `119245d`, and others). This is a scheduling fix
   with no behavioural change, and it is what actually stops requests from
   ever overlapping, which was the mechanical cause of the browser refusing
   connections. Verified by confirming the errors stopped before any
   further change was made.
2. **User-visible failure feedback.** Several fetch chains ended in
   `.catch(error => console.error(...))` only — a dropped or failed
   request left a button stuck (e.g. "Adding vm...") with nothing shown to
   the user. This is the usability messaging requirement in the brief, not
   just cleanup, so it was treated as equally high priority: failure paths
   now call `prompt_user` and reset the control, and a client-side network
   timeout (`AbortController`, 10s) was added so a request that never
   returns still eventually reaches the failure path instead of leaving
   the loop silently stuck.
3. **Interval, not redesign.** Rather than rearchitecting how the dashboard
   refreshes, the polling intervals were simply lengthened via the shared
   `BASE_POLL_TIME` constant (from 1–3 seconds to 15 seconds) — panels
   already refresh themselves immediately after the action that changes
   their data, so the interval is a safety net rather than the primary
   update path. Low effort, large effect on request volume.
4. **Query optimisation, applied narrowly.** Combining all three of the
   above drops request volume by roughly 95%, at which point most of the
   N+1 query patterns in `views.py` stopped mattering in practice. One
   endpoint still measured as slow on Render afterwards: adding/removing a
   VM from a VM group, whose `fetch_available_vms_for_group` helper was
   doing an O(VMs × groups) nested query (plus a repeated user lookup per
   inner iteration). This was fixed specifically for that flow (commit
   `fb420d2`, plus a duplicate-membership check that was a no-op
   comparison rather than an assignment, commit `9142765`), rather than
   applied speculatively across every view.
5. **Combining the polling endpoints into one** was identified as a valid
   further improvement but deliberately not implemented — see the backlog
   item above.

This is a useful example for the Operate & Monitor section even without
dedicated monitoring tooling this iteration: the defect was invisible
locally, only emerged under the deployed environment's real constraints,
and was diagnosed by comparing environments and reading browser-side
timing evidence rather than by guessing or by reading server logs (which
had nothing to show, since the failed requests never reached the server).
That is the same evidence-based diagnosis discipline the withheld
monitoring/alerting work (6.2–6.3) would formalise with real tooling —
here it was done manually, once, for a specific incident.
