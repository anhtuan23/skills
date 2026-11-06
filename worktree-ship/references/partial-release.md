# Partial release

Goal: ship selected commits of `<feature>` while the rest keeps developing.

## Prepare the history

1. Back up: `git branch backup/<feature>-<date> <feature>`.
2. List commits: `git log --oneline main..<feature>`. Classify each as ship,
   keep, or mixed. Ask the user to confirm the split when it is not obvious.
3. A commit that mixes shipped and kept changes must be split first
   (`git rebase -i` with `edit`, then `git reset HEAD^` and re-commit in
   pieces) in the worktree. Interactive editors are unavailable to agents;
   use `GIT_SEQUENCE_EDITOR` with a prepared todo, or build the release
   branch by cherry-picking with `-n` and staging selectively.
4. Check dependency: a shipped commit must not need a kept commit. Verify by
   building/testing the release branch alone.

## Ship

1. `git worktree add ~/projects/<repo>-worktrees/<feature>-release -b <feature>-release origin/main`
   (after fetching and fast-forwarding `main`).
2. `git cherry-pick <shipped SHAs in original order>`. Conflicts: `git-reconcile`.
3. Run tests on this branch alone; this is the code production will run.
4. Merge `<feature>-release` into `main` with `--no-ff`, then `git push origin main`.

## Realign the remainder

1. In the feature worktree: `git rebase main`. Git drops cherry-picked commits
   that are patch-identical; if one survives as a duplicate, skip it, after
   confirming the content already exists on `main`.
2. Conflicts: `git-reconcile`. Re-run tests.
3. Remove the release worktree and `<feature>-release` branch once merged.
   Keep the backup ref until the user says otherwise.

## Pitfalls

- Cherry-pick changes SHAs; never reuse the feature branch's old SHAs in
  reports for what landed on `main`.
- Do not merge the whole feature branch "temporarily" and revert parts.
- If the split is not clean, ask the user whether to introduce a feature flag
  (a config switch that merges unfinished code but keeps it off in production)
  instead of contorting history.
