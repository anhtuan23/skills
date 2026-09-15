# Completion review 01

- Reviewer: Hypatia (`reviewer-complex`)
- Scope: `git-reconcile/`, root catalog entry, and plan artifacts
- Method: adversarial read-only review against the requested merge/rebase
  behavior, current Git documentation, and valuable-repository recovery risks
- Edits/staging performed by reviewer: none

## Findings

### P1 — Recovery ref could move during rebase

The first draft created a backup branch under `refs/heads/`, but
`rebase.updateRefs` can move branches that point into the rewritten series.
That could invalidate the promised recovery point and move unrelated branches.

Required response: use a recovery tag outside `refs/heads/`, inspect effective
`update-refs` behavior, and enumerate affected refs before proceeding.

### P1 — Recreated merges were under-verified

The first draft preserved `--rebase-merges` topology but did not require
inventorying original merge-only resolutions or comparing recreated merge
commits. Plain `range-diff` ignores merge commits.

Required response: map original to recreated merges, inspect merge-only tree
changes, use merge-inclusive range comparison where supported, and add explicit
behavioral verification.

### P1 — Rebase abort could discard resolver edits

The first draft guarded merge abort more clearly than rebase abort. A commit
backup/ref or reflog cannot recover uncommitted conflict edits, untracked files,
or all unmerged index stages.

Required response: preserve current resolver and unrelated work before aborting
either operation; state the limits of patches/stashes and use a complete
worktree preservation method when necessary.

### P1 — Bare force-with-lease was not sufficient

The first draft recommended `--force-with-lease` without an explicit expected
remote SHA. A background fetch can update tracking refs between review and
push, weakening that form of the lease.

Required response: record the reviewed remote SHA and use an explicit lease and
destination ref, only after explicit publication authorization.

### P2 — Merge preview used limited legacy mode

The first draft used the three-argument `git merge-tree` form, which is the
deprecated trivial-merge mode and does not faithfully model rename,
directory/file, or complex merge behavior.

Required response: use modern `git merge-tree --write-tree A B`, explain its
diagnostic/object-writing behavior and exit status, and detect multiple merge
bases.

### P2 — Active-operation detection was incomplete

The first draft relied too heavily on pseudo-refs and `.git` paths. Linked
worktrees, paused interactive states, `am`, revert, cherry-pick, and sequencer
operations need portable `git rev-parse --git-path` inspection and distinct
continuation behavior.

Required response: inspect Git-resolved control paths and `git status`, then
distinguish conflict, edit/break, failed-exec, and other sequencer stops.

## Validation gaps noted

- No disposable merge/rebase scenario was run; this deliverable is a skill
  document, not a live conflict operation.
- `git diff --check` did not include untracked files until they are staged;
  validate the skill's files directly and run cached checks after staging if
  staging is performed.
- The bundled validator could not import `yaml` in this environment.

## Initial review decision

Not ready to trust with a valuable repository until all six findings are
addressed and the resulting instructions are revalidated.

## Response and follow-up review

All six findings were addressed in the skill references:

- Recovery points are tags outside `refs/heads/`; effective
  `rebase.updateRefs`, affected branches, worktrees, and explicit recovery
  paths are inspected.
- `--rebase-merges` now inventories original merges, checks merge-only
  resolutions, uses `range-diff --remerge-diff` where available, and requires
  topology and behavior verification.
- Merge and rebase abort/retry guidance preserves resolver edits, staged
  conflict stages, untracked files, and diagnostics before aborting, while
  documenting patch/snapshot limits.
- Publication guidance records the reviewed remote SHA and uses an explicit
  `--force-with-lease=<ref>:<sha>` destination only after authorization.
- Merge preview uses modern `git merge-tree --write-tree` and explains its
  diagnostic/object-writing behavior and exit statuses; multiple merge bases
  are surfaced.
- Active-operation detection uses Git-resolved control paths and long status,
  including linked-worktree and sequencer states, and distinguishes conflict,
  edit/break, failed-exec, and empty-commit stops.
- The later P3 clarifications distinguish short path inventory from long
  operation diagnosis and distinguish an authorized rebase detachment from an
  unexplained detached `HEAD` or unrelated dirty work.

Validation completed: the bundled skill validator passed; frontmatter,
relative-reference, trailing-whitespace, and `git diff --check` checks passed.
No disposable merge/rebase scenario was run because this deliverable is a
general skill document; that remains a limitation rather than evidence of
runtime Git behavior.

The reviewer confirmed that the P3 findings are resolved and reported no
remaining findings. Ready for final human review.
