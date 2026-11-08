# Deploy to production

Deploy only `origin/main`, only after it has been pushed.

## Configuration

Deployment is project-specific. Read the "Deploy" section of `AGENTS.md`, or the
doc it links to, for the production machine, when an agent may act, the restart
rules, and the health check. The repo path is the same on all machines
(`~/projects/<repo>`). If any of this is missing, ask the user and suggest
recording it there. Do not invent it.

## Steps

1. Follow the project's permission rule. If it has none, confirm with the user
   for this run: "Deploy `<short SHA>`?" A previous approval does not carry over.
2. Inspect production (read-only):
   `git status --short --branch && git rev-parse HEAD`, over SSH if you are on
   another machine. Stop and report if the main checkout is dirty, on a branch
   other than `main`, or has an active merge/rebase. Do not clean it up. Feature
   work on that machine belongs in its worktrees.
3. `git fetch origin && git pull --ff-only origin main`. A non-fast-forward
   means production diverged: stop and report. Never reset, stash, or force.
4. The SHA from step 2 is the rollback point; keep it for the report.
5. Work out which services changed (`git diff --name-only <old>..<new>`), and
   restart the smallest set the project's rules allow. Follow the project's
   restart procedure exactly. If it cannot be followed, stop and ask the user.
6. Verify with the project's health check if documented; otherwise report the
   deployed SHA and command output.

## Failure

On restart or health failure, report output and the previous SHA. Do not roll back
automatically; propose the project's rollback, or `git revert -m 1 <merge SHA>`
on `main` (new ship), and let the user choose.

## Safety

- Non-interactive SSH only; if a password/host-key prompt appears, stop.
- On the production machine, run only status, fetch, ff-only pull, the project's
  restart procedure, and its health checks.
