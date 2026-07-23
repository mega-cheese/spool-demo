You are working in a small Flask app. Task instructions will tell you which specific file(s) you're authorized to modify for a given task. Stay within that scope. If a complete fix seems to genuinely require touching a file outside your authorized scope, don't make that change — instead, note the limitation clearly in your PR/commit description.

<!-- spool-pr-evidence -->
## Spool PR Evidence

When creating or updating pull requests, follow `.spool/agent_instructions.md` and fill out the Spool sections in the pull request template.

Spool treats agent-written PR sections as claims to verify against the diff, tests, and approved repo decisions. If a task, test result, or decision is unknown, say so explicitly instead of guessing.

## Pull request requirements

When creating a pull request:

1. Branch from the latest `origin/main`.
2. Create the branch directly in `mega-cheese/spool-demo`; do not use a fork.
3. Do not modify `.github/workflows/spool.yml` unless explicitly instructed.
4. Push the branch to `origin`.
5. Open the pull request against `main` using the authenticated GitHub CLI.
6. After creating the PR, verify that the `Spool PR Comment` workflow started.
7. If additional commits are pushed, verify that Spool reruns.
8. Do not merge until the Spool workflow completes successfully.
