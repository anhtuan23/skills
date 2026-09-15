# Safety and recovery

Use this reference before a new history rewrite and before aborting or retrying
an active operation. A recovery path is part of correctness, not an optional
cleanup step.

## Pre-operation snapshot

Inspect without mutation:

```text
git status --long --branch
git status --short --branch
git branch --show-current
git rev-parse HEAD
git rev-parse --abbrev-ref --symbolic-full-name @{u}
git log --oneline --graph --decorate --all -n 30
git reflog -n 10 HEAD
git rev-parse --git-path MERGE_HEAD
git rev-parse --git-path REBASE_HEAD
git rev-parse --git-path CHERRY_PICK_HEAD
git rev-parse --git-path REVERT_HEAD
git rev-parse --git-path rebase-merge
git rev-parse --git-path rebase-apply
git rev-parse --git-path sequencer
git worktree list --porcelain
```

If `@{u}` is unavailable, record the missing upstream rather than guessing a
remote or branch.

Check whether the returned paths exist. `git status` remains the primary
operation report, including for linked worktrees; the paths also cover paused
interactive rebases, `git am`, cherry-pick/revert, and other sequencer states.
Distinguish a conflict from an `edit`, `break`, failed `exec`, or an operation
that has already finished its current patch before choosing `--continue`,
`--skip`, `--quit`, or `--abort`.

Record the full pre-operation SHA, branch, upstream, operation, target/base,
and dirty/untracked paths. Before a rebase or other history rewrite, create a
unique local recovery tag outside `refs/heads/` if no reliable one already
exists:

```text
git tag git-reconcile/recovery-<timestamp> <pre-operation-sha>
git show-ref --verify refs/tags/git-reconcile/recovery-<timestamp>
```

Keep the ref until the user is satisfied; never delete it automatically. A
recovery tag is not one of the local branches targeted by `rebase.updateRefs`
and is more reliable than relying only on reflog retention. Inspect the
effective `rebase.updateRefs` configuration and whether `--update-refs` was
requested; enumerate any local branches that may move and obtain authorization
for those updates. A linked worktree can also prevent some branch updates, so
inspect `git worktree list --porcelain` rather than guessing.

If `git branch --show-current` is empty, `HEAD` is detached. This can be
normal during an identified, authorized rebase; use the recorded rebase
metadata and original branch to confirm it. Stop before moving a branch ref
when the detached state is unexplained or the target/authorization is missing.

Use the branch list to identify refs in the rebased range before proceeding:

```text
git for-each-ref refs/heads --format='%(refname:short) %(objectname)'
```

When starting a new operation, stop by default if the worktree is dirty.
During an active operation, distinguish expected resolver edits from unrelated
work and preserve both before aborting, quitting, or retrying. Commit, stash,
export a patch, or use an isolated worktree only after the user chooses that
handling. Do not assume `--abort` can reconstruct overlapping uncommitted
changes.

For an operation already in progress, identify its control paths from the
Git-resolved commands above and its refs from `git status`, `ORIG_HEAD`,
`MERGE_HEAD`, and `REBASE_HEAD`. Do not overwrite an active operation with a
new one.

## Abort, quit, continue, and skip

| Command | Meaning and guard |
| --- | --- |
| `git merge --abort` | Try to return to the pre-merge state; safest after a clean preflight. Preserve and verify current resolver/unrelated work first if it must be retained. |
| `git rebase --abort` | Stop and return the branch to its original pre-rebase state. Preserve and verify current resolver/unrelated work first; then verify the branch and worktree afterward. |
| `git rebase --quit` | Stop the rebase machinery but leave `HEAD`, index, and worktree as they are; it is not an undo. |
| `git rebase --skip` | Drop the current replayed commit. Use only after proving it is redundant or after an explicit decision. |
| `git merge --continue` / `git rebase --continue` | Use only after exact paths are staged, no unmerged entries remain, and checks support the result. |

Do not use `git reset --hard` or `git clean` as routine conflict cleanup. If a
known-good ref must be restored, first preserve the current state, verify the
exact target SHA, check for unrelated changes, and obtain explicit authorization
for the history-moving command.

Before aborting, quitting, or retrying either operation, preserve any current
resolver edits and unrelated work. A commit/tag protects committed objects only;
it does not preserve uncommitted file contents, untracked files, or all unmerged
index stages. At minimum, save and verify an external copy of the worktree and
these diagnostics:

```text
git diff --binary > <safe-path>/worktree.patch
git diff --cached --binary > <safe-path>/index.patch
git diff --cc --binary > <safe-path>/conflict.patch
git ls-files --others --exclude-standard > <safe-path>/untracked.txt
```

Patches may be incomplete for unmerged stages, binary files, ignored files, or
untracked content. Use a complete worktree/filesystem snapshot or stop for
human assistance when those contents matter. Verify preservation before running
`--abort` or any retry.

## If the result is wrong

Stop publication. Preserve the current tip and inspect the reflog and backup:

```text
git reflog show --date=local <branch>
git show <recovery-ref>
git diff <recovery-ref>..<current-tip>
git log --oneline --graph --decorate <recovery-ref>..<current-tip>
```

Compare trees and tests before deciding whether to retry, abort, or restore.
Move a local branch back only with a confirmed target and explicit authorization;
do not overwrite a remote branch as part of recovery. If uncommitted work was
present, recover it from the saved patch/stash or original worktree record
before changing refs.

## Rerere

`rerere` can reuse a previously recorded textual resolution, which is useful
for repeated conflicts but can repeat a bad semantic choice. Use it only when
the repository/user wants it:

```text
git rerere status
git rerere diff
git rerere remaining
git rerere forget <path>
```

Review every reused resolution against the current base and intent. Prefer
`--no-rerere-autoupdate` while checking a merge or rebase so Git does not stage
the reused result before inspection. Do not treat rerere as proof or enable it
silently as part of an unrelated resolution.

## Publication boundary

A local merge/rebase result is distinct from a pushed or deployed result. Push,
force-push, PR comments, and remote branch updates require separate explicit
authorization. Before an authorized force update, inspect the remote tip
immediately before pushing and use an explicit lease and destination:

```text
git ls-remote <remote> refs/heads/<branch>
git push --force-with-lease=refs/heads/<branch>:<reviewed-remote-sha> <remote> HEAD:refs/heads/<branch>
```

If the remote moves or the reviewed SHA is unclear, the explicit lease must fail
or the operation must stop. Never use a bare lease whose expectation can be
silently changed by a background fetch.

Final recovery evidence should include the pre-operation SHA, backup ref,
operation/target, resulting ref and SHA, reflog or range-diff comparison, tests,
and anything intentionally skipped or not published.
