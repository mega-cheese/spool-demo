# Spool Agent Instructions

When opening or updating a pull request, fill out the Spool sections in the PR body.

## Required PR sections

- `## Spool Task`
- `## Agent Summary`
- `## Tests Run`
- `## Candidate Decisions`

## Rules

- Restate the user's task in `## Spool Task`.
- Include allowed files/areas if they were provided.
- If the original task is unknown, write `Unknown`.
- Summarize implementation work in `## Agent Summary`.
- List important files changed.
- List exact test commands and results in `## Tests Run`.
- If no tests were run, write `Not run`.
- Candidate decisions are proposed project memory, not a change summary.
- List only durable product, architecture, security, API, policy, or process decisions that future PRs should respect.
- Do not list normal implementation details as candidate decisions.
- Do not list tests, docs, refactors, bug fixes, or file additions as candidate decisions.
- If there are no candidate decisions, write `None`.
- If the PR only implements an already-approved decision, write `None` or explain that no new durable decisions are introduced.
- Do not claim tests passed unless tests or CI actually passed.
- Do not claim a file changed unless it appears in the diff.
- Do not approve candidate decisions yourself.
- Treat the PR body as claims for Spool to verify, not as final truth.
