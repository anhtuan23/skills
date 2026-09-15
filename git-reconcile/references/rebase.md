# Rebase workflow

Rebase replays commits one at a time on a new base. A conflict is therefore a
question about the current commit's historical intent in the new context, not a
single merge between two complete branch tips.

## Before starting or resuming

Record the original branch tip, branch name, upstream, target `--onto` commit,
and a local recovery ref as described in [recovery.md](recovery.md). Establish
a baseline when practical. Confirm the worktree is safe before starting a new
rebase and detect any existing `MERGE_HEAD`, `REBASE_HEAD`, or
`CHERRY_PICK_HEAD` before running another operation.

For an active rebase, inspect all of these before each resolution:

```text
git status --long --branch
git status --short --branch
git branch --show-current
git rev-parse HEAD
git rev-parse REBASE_HEAD
git rebase --show-current-patch
git show --stat --oneline REBASE_HEAD
git show REBASE_HEAD^..REBASE_HEAD
git diff --cc
git ls-files -u
```

Also inspect the Git-resolved operation paths and the effective ref-update
settings before starting or continuing a rewrite:

```text
git rev-parse --git-path rebase-merge
git rev-parse --git-path rebase-apply
git rev-parse --git-path sequencer
git config --show-origin --get rebase.updateRefs
git worktree list --porcelain
```

Check whether those paths exist and whether the rebase was stopped for a
conflict, `edit`, `break`, failed `exec`, or an empty commit. Do not choose a
continuation command from a pseudo-ref alone.

Use the todo list when needed:

```text
git rebase --edit-todo
```

Do not edit the todo merely to bypass a conflict. Preserve the requested commit
order and meaning unless interactive history editing is explicitly in scope.

## The rebase side reversal

Git documents the conflict sides during rebase as follows:

- Git's `ours` is the target/upstream plus commits already replayed so far.
- Git's `theirs` is the working-branch commit currently being replayed.

Thus the labels are reversed from the usual intuition. In the reconciliation
model, call the target context side A and the current replayed commit side B,
then inspect the actual patch and index stages. Never choose a side because it
is called `ours` or `theirs`; a refactor on side A may require porting side B's
feature, while a side-B deletion may be the valid intent.

## Resolve one replayed commit

1. Identify the current commit with `REBASE_HEAD` and read its message, parent,
   full diff, task/PR context, and relevant tests.
2. Compare the target context with the commit's parent and commit. Use stage 1
   when present, but confirm it against `REBASE_HEAD^`; inspect trees directly
   for path and rename conflicts.
3. Apply the shared five-question model and classify each hunk. Preserve the
   commit's intent at the new architecture, including a minimal
   `structural-port` when the original patch no longer applies literally.
4. Stage exact resolved paths, inspect the staged diff, and run focused checks
   before `git rebase --continue`. Include `git diff --cached --check`.
5. If Git stops again, treat the next `REBASE_HEAD` as a new semantic decision.
   Re-read its patch and do not carry a prior side choice forward by habit.

If the patch becomes empty, determine why. It may already be integrated, made
redundant by the new base, intentionally empty, or missing required behavior.
Use `git rebase --skip` only when dropping that specific commit is supported by
the history and requirements, or the user explicitly decides it. Skipping is a
semantic deletion, not a conflict-resolution shortcut. If the behavior is still
required, port it into the current architecture instead.

## Special rebase modes

- `--onto`: identify the old upstream/range, the new base, and the exact commits
  being transplanted. Do not assume the visible branch name describes all three.
  The operation shape is `git rebase --onto <new-base> <old-upstream> <branch>`.
- `--rebase-merges`: the todo can recreate merge commits and branch topology.
  Before starting, inventory original merge commits and merge-only behavior
  with `git log --merges`, `git show --cc --stat <merge>`, and diffs against
  both parents. The todo's `merge -C <original-merge>` entries map original
  merges to recreated ones; inspect each recreated merge's parents, tree, and
  manual resolution even when Git reports no conflict. Preserve topology unless
  the user requested flattening. Do not treat the series as one giant linear
  patch.
- Interactive rebase: review `pick`, `edit`, `reword`, `squash`, `fixup`, and
  `drop` decisions as history semantics. Do not drop or squash a conflicting
  commit just to make the operation finish.

## Compare the rewritten series

Before the rebase, preserve the old base and tip. After it finishes, compare
the old and new commit ranges:

```text
git range-diff --remerge-diff <old-base>..<old-tip> <new-base>..<new-tip>
git log --oneline --graph --decorate <new-base>..<new-tip>
```

Use the recovery ref or reflog for `<old-tip>` if the branch name now points to
the rewritten series. `--remerge-diff` includes merge-commit comparisons on Git
versions that support it; if unavailable, compare every original/recreated
merge's parents and trees directly. Review dropped, reordered, split, empty,
merge-only, and materially changed commits. `range-diff` is evidence about
patch-series preservation, not a substitute for behavioral tests.

Also verify clean status, no unmerged entries or actual markers, and
`git diff --check <new-base>..<new-tip>`. Confirm that every expected ref moved
and no unrelated ref was changed.

Do not publish a rewritten branch without explicit authorization. If publishing
is authorized, record the reviewed remote SHA immediately before pushing and
use an explicit lease and destination, for example:

```text
git ls-remote <remote> refs/heads/<branch>
git push --force-with-lease=refs/heads/<branch>:<reviewed-remote-sha> <remote> HEAD:refs/heads/<branch>
```

A changed remote must make the push fail. Never use an unconditional `--force`
or a bare lease whose expectation can be changed by a background fetch.
