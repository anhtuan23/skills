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
docs/plans/YYMMDD-HHMM-{name}/
├── plan.md          # source of truth
├── progress.md      # current status
└── review/
    ├── 00-plan-review.md
    ├── {NN}-slice-{name}.md
    └── 99-completion-review.md
```

## Reviews

| Review | When | File |
|--------|------|------|
| Plan review | Before implementation | `00-plan-review.md` |
| Slice review | After each slice | `{NN}-slice-{name}.md` |
| Review response | After addressing findings | Appended to slice review |
| Completion review | After all slices done | `99-completion-review.md` |

## Quick Start

1. Create plan folder: `docs/plans/YYMMDD-HHMM-{descriptive-name}/`
2. Write `plan.md` with goal, steps, and validation criteria
3. Write `progress.md` with current status
4. Get plan review before implementing
5. Work slice by slice, reviewing each one
6. Write completion review when done
