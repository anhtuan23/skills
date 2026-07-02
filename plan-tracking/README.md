# Plan Tracking

Track implementation plans with structured progress and review artifacts.

## Overview

This skill provides a standardized workflow for managing multi-step implementation
plans. It ensures plans are documented, progress is trackable, and reviews happen
at the right checkpoints.

## When to Use

- Non-trivial features or refactors
- Risky changes (migrations, data integrity, auth/security)
- Multi-step work that needs human approval gates
- Work where resumption by other agents matters

## Structure

```
docs/plans/YYMM/DDHHMM-{name}/
├── plan.md              # source of truth
├── progress.md          # current status
├── review/
│   ├── plan-01.md       # plan review rounds
│   ├── slice-01-{name}.md
│   ├── completion-01.md # completion review rounds
│   └── completion-02.md
└── sub-plans/
    └── DDHHMM-{sub-name}/  # same structure as main plan
```

The `YYMM` sub-folder (e.g. `2607/` for July 2026) keeps `docs/plans/` browsable
as plans accumulate over time.  The folder name uses `DDHHMM` since year-month
is already in the parent path.

## Subplans

Work that surfaces during execution but belongs after the main plan goes into
`sub-plans/DDHHMM-{name}/`.  Each sub plan has its own `plan.md`, `progress.md`,
and `review/` — fully independent tracking.  Create the `sub-plans/` folder only
when the first sub plan is identified.

## Reviews

| Review | When | File |
|--------|------|------|
| Plan review | Before implementation | `plan-{NN}.md` (supports multiple rounds) |
| Slice review | After each slice | `slice-{NN}-{name}.md` |
| Review response | After addressing findings | Appended to slice review |
| Completion review | After all slices done | `completion-{NN}.md` (supports multiple rounds) |

## Quick Start

1. Create plan folder: `docs/plans/YYMM/DDHHMM-{descriptive-name}/`
   (create the `YYMM` sub-folder first if it doesn't exist)
2. Write `plan.md` with goal, steps, and validation criteria
3. Write `progress.md` with current status
4. Get plan review before implementing
5. Work slice by slice, reviewing each one
6. Write completion review when done
