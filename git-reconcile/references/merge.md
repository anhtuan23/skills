# Merge workflow

## Before starting a merge

Confirm the direction: the current branch is the branch that will receive the
other branch. From a clean, intended worktree, record:

```text
git status --long --branch
git status --short --branch
git branch --show-current
git rev-parse HEAD
git rev-parse --abbrev-ref --symbolic-full-name @{u}
git merge-base --all HEAD <other>
git log --oneline --graph --decorate --all -n 30
git diff --stat HEAD <other>
```

If `@{u}` is unavailable, record the missing upstream and use only the
explicitly identified merge target.

Record the full pre-merge SHA and, when the merge is material, create or
identify a local recovery ref. Git normally records the current tip in
`ORIG_HEAD`, but do not rely on that alone for a valuable integration.

When available, preview without changing the index or worktree:

```text
git merge-tree --write-tree HEAD <other>
```

The modern form uses Git's merge machinery, including rename and
directory/file handling, and may create temporary tree objects without moving
refs. Check its exit status and conflict records: `0` means clean, `1` means
conflicts, and another status means the preview failed. Do not parse only the
resulting tree or infer logical conflict types from paths alone. The legacy
three-argument form is limited and should not be used as the faithful preview.

If `git merge-base --all HEAD <other>` returns multiple bases, let the normal
merge machinery perform ancestor consolidation; do not feed one arbitrary base
to a preview and call it authoritative.

Run a baseline test or build when practical. Do not begin a new merge with
uncommitted index/worktree changes unless the user has explicitly chosen a
safe handling method. Do not silently use `--autostash`; a later stash conflict
can obscure the actual merge.

Do not start a merge while another merge, rebase, cherry-pick, revert, `am`, or
sequencer operation is active.
For an already halted merge, inspect `MERGE_HEAD`, `ORIG_HEAD`, status, and the
pre-operation record instead of starting over.

## Meaning of the merge sides

In a halted normal merge:

- `HEAD` is the current branch and is Git's merge `ours`.
- `MERGE_HEAD` is the branch being merged and is Git's merge `theirs`.
- the common ancestor set is `git merge-base --all HEAD MERGE_HEAD`; do not
  choose one arbitrarily when Git reports multiple bases.

These names describe Git's mechanics only. Choose a result from the intents and
invariants reconstructed in [conflict-reconciliation.md](conflict-reconciliation.md).
Do not pass `-Xours`, `-Xtheirs`, `git restore --ours`, or `git restore --theirs`
over a whole file unless the exact semantic decision has already been made and
the result is reviewed as a three-way change.

## Conflict shapes

| Shape | Questions to answer |
| --- | --- |
| modify/modify | What did each side change from the base? Are the invariants compatible? |
| modify/delete | Is the deletion architectural or accidental? If behavior survives, where does it belong now? |
| add/add | Are the new files alternatives or complementary additions? Do names, APIs, and registrations collide? |
| rename/modify | Did the modification follow the rename? Check old/new paths, callers, and identity. |
| rename/delete | Is the deletion of the renamed entity intentional? Check references and replacement APIs. |
| rename/rename | Which identity and destination does the repository require? Combine only if both moves are compatible. |
| directory/file movement | Does one side establish a new path model? Move required behavior into that model; do not resurrect obsolete directories. |
| mode, symlink, binary, submodule | Textual editing is unsafe. Use the project's explicit procedure or escalate. |
| generated/lockfile/schema/migration/deployment | Regenerate or obtain domain review; do not hand-edit opaque or order-sensitive output casually. |

Review auto-merged files too when a refactor or contract change changes the
meaning of code without producing markers.

## Resolve and finish

For each path, inspect `git diff --cc`, the three stages where available, both
branch-relative diffs, and relevant callers/tests before editing. Stage only
that path after reviewing its result. Use `git merge --continue` or commit the
merge only when the user's requested scope includes completing the merge.

Preserve the requested history shape. Do not silently turn a requested
no-fast-forward merge into a fast-forward or squash, and do not use the `ours`
merge strategy to hide an unresolved branch. A merge commit may contain small
necessary fixups, but unrelated cleanup belongs in another change.

After resolution, verify unmerged index entries, actual markers, staged diff,
`git diff --cached --check`, focused tests, repository checks, and
`git diff --check`. Confirm the resulting parents and graph match the intended
merge. A clean status alone is not proof.
