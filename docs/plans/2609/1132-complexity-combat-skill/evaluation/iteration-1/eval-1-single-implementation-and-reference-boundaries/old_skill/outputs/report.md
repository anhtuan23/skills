# Complexity Combat evaluation report

## Scope and scan status

Scanned `/Users/kaestrl/projects/skills/git-reconcile` read-only. It contains one
98-line entrypoint and four reference files totaling 647 lines:

- `SKILL.md`
- `references/conflict-reconciliation.md`
- `references/merge.md`
- `references/rebase.md`
- `references/recovery.md`

No literal interface, abstract class, factory, or wrapper with a single
implementation was found. The closest abstraction is the fixed five-label
classification taxonomy; it is used in the entrypoint and shared conflict
reference, rather than being a code-level single-implementation abstraction.

The initial scan identified these possible candidates:

| Candidate | Scope | Impact | Gate status |
| --- | --- | --- | --- |
| 1. Reference boundary split and repeated guidance | Four references, with overlapping preflight and classification material | Medium | Presented below; awaiting decision |
| 2. Fixed classification taxonomy | Five labels and repeated taxonomy presentation | Low/medium | Not examined past the first gate |
| 3. Single-implementation abstraction | No concrete instance found | None | Not a candidate |

## Candidate 1: Reference boundary split and repeated guidance

### Problem this is trying to solve

Provide one portable entrypoint for semantically different merge, rebase, and
history-recovery situations while keeping operation-specific instructions and
safety guidance focused.

### Evidence that it may be accidental complexity

- The entrypoint requires a sequence of four reads: the shared reconciliation
  reference, one or both operation references, and the recovery reference
  (`SKILL.md:42-50`). The instruction to read both operation references when the
  target is unclear increases routing and reading cost.
- The same repository-state/preflight concerns recur across the shared,
  merge, rebase, and recovery references: status, branch/HEAD, upstream or
  target, active operation state, and recovery information
  (`references/conflict-reconciliation.md:32-49`, `references/merge.md:3-24`,
  `references/rebase.md:7-43`, `references/recovery.md:7-78`).
- The classification taxonomy is defined in the entrypoint
  (`SKILL.md:73-81`) and substantially repeated in the shared reference
  (`references/conflict-reconciliation.md:92-114`). The labels are then
  referenced again in the operation guidance (`SKILL.md:56-59`,
  `references/rebase.md:67-87`). This creates multiple maintenance locations
  for one conceptual model.
- The directory is 647 lines for a single skill, and the split requires the
  reader to reconstruct the complete workflow across documents before acting.

### Counter-evidence

- Merge and rebase are not interchangeable workflows. Their side labels differ
  materially (`references/merge.md:53-66`, `references/rebase.md:54-65`), and
  rebase has replay, empty-commit, interactive, `--onto`, and
  `--rebase-merges` concerns that do not belong in a generic merge section
  (`references/rebase.md:67-104`).
- Recovery is a safety boundary with abort/quit/skip, uncommitted-work
  preservation, rerere, and publication guidance; separating it makes the
  highest-risk instructions easier to locate (`references/recovery.md:80-162`).
- The entrypoint itself is short and routes to focused references rather than
  duplicating every procedure. The repeated classification table may be
  intentional discoverability for readers who open the shared reference
  directly.
- The classification labels encode materially different actions, especially
  `structural-port` versus `superseded` and `unsafe-or-unresolved`; collapsing
  them could cause incorrect conflict decisions.

### Assessment

This is a plausible medium-impact complexity candidate, but the evidence does
not establish that the four-file boundary is wrong. The strongest concrete
concern is duplicated preflight/taxonomy guidance and the resulting maintenance
burden, not the existence of operation-specific references itself.

## Required first decision

**Candidate 1: Reference boundary split and repeated guidance**

This code addresses: “Provide one portable entrypoint for semantically
different merge, rebase, and history-recovery situations while keeping
operation-specific instructions and safety guidance focused.”

Is this a real problem for your project?

- **Yes** — keep the code
- **No** — simplify or remove it
- **Maybe, but overblown** — simplify with care

Per the evaluation workflow, no later candidate will be examined until this
decision is answered.
