# Deploy to production (air-m1)

Deploy only `origin/main`, only after it has been pushed. The agent may SSH to
`air-m1` (directly from `air-m5` or `mac-mini`).

## Configuration

Deployment steps are project-specific. Read them from `AGENTS.md` or README
(a "Deploy" section with the restart rules and health check). The repo path is the
same on all machines (`~/projects/<repo>`). If the command is missing, ask the
user and suggest recording it there. Do not invent one.

## Steps

1. Confirm with the user for this run: "Deploy `<short SHA>` to air-m1?" A
   previous approval does not carry over.
2. Inspect production (read-only):
   `ssh air-m1 'cd <path> && git status --short --branch && git rev-parse HEAD'`.
   Stop and report if the main checkout is dirty, on a branch other than
   `main`, or has an active merge/rebase. Do not clean it up. Feature work on
   `air-m1` belongs in its worktrees, so the main checkout should be clean.
3. `ssh air-m1 'cd <path> && git fetch origin && git pull --ff-only origin main'`.
   A non-fast-forward means production diverged: stop and report. Never reset,
   stash, or force.
4. The SHA from step 2 is the rollback point; keep it for the report.
5. Work out which services changed (`git diff --name-only <old>..<new>`). Per
   the project's deploy section, restart only what changed. Prefer single
   services. A whole-fleet restart is allowed only inside the pane where the
   fleet already runs: SSH to the machine (herdr runs per machine; prepend
   `PATH=/opt/homebrew/bin:$PATH` for non-interactive SSH), locate the pane
   with `herdr pane list` and `pane read`, then drive it with
   `pane send-keys` and `pane run`. Never start
   a second fleet from a separate SSH shell, `nohup`, or a service manager. If
   herdr is unreachable, the fleet pane is not found or is
   ambiguous, or the pane is not at a clean shell prompt after stopping, stop
   and ask the user.
6. Verify with the project's health check if documented; otherwise report the
   deployed SHA and command output.

## Failure

On restart or health failure, report output and the previous SHA. Do not roll back
automatically; propose `git revert -m 1 <merge SHA>` on `main` (new ship) or
checking out the previous SHA on `air-m1` and let the user choose.

## Safety

- Non-interactive SSH only; if a password/host-key prompt appears, stop.
- Never run commands on `air-m1` beyond status, fetch, ff-only pull, single
  service restarts, herdr pane control of the existing fleet pane, and the
  configured health commands.
