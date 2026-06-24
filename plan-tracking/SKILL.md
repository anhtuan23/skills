---
name: plan-tracking
description: Track implementation plans with structured progress and review artifacts for multi-step work.
---

# Plan Tracking

Use this skill when starting non-trivial, multi-step, or risky work that needs
a plan, progress tracking, and structured reviews.

## Plan Structure

Store all artifacts under `docs/plans/YYMMDD-HHMM-{short_descriptive_name}/`:
use local time and a concise lowercase hyphenated name.

Required files:

```text
docs/plans/YYMMDD-HHMM-{name}/
├── plan.md          # source of truth
├── progress.md      # current status for resumption
└── review/
    ├── 00-plan-review.md
    ├── {NN}-slice-{name}.md
    └── 99-completion-review.md
```

## Plan Creation

1. Create the plan folder with the timestamped name.
2. Write `plan.md` with:
   - Goal and scope
   - Assumptions and constraints
   - Ordered implementation steps (slices)
   - Validation criteria for each slice
   - Known risks or open questions
3. Write `progress.md` with:
   - Current status (not started / in progress / blocked / done)
   - Active slice number and name
   - Next intended step
   - Blockers or notes for resumption

Keep `plan.md` as the source of truth. Update it when scope or sequence changes.
Keep `progress.md` current so future agents can resume.

## Review Types

### Plan Review

Review `plan.md` before implementation starts.

- Create as `review/00-plan-review.md`
- Cover: feasibility, risks, sequencing, missing assumptions, spec alignment
- Include: reviewer identity, method, findings by severity, overall go/no-go

### Slice Review

Review a specific implementation commit after each slice is done.

- Create as `review/{NN}-slice-{name}.md` (e.g. `review/01-slice-1-signing.md`)
- Include:
  - Commit hash
  - Scope coverage table
  - Validation run results
  - Technical correctness notes against specs
  - Findings by severity
  - Overall opinion

### Review Response

Documents how findings from a slice review were addressed.

- Append to the same slice review file after the overall opinion
- Include:
  - Which findings were addressed and how
  - Validation results for the fixes
  - Any deferred items

### Completion Review

Review the full implementation after all slices are done.

- Create as `review/99-completion-review.md`
- Cover: end-to-end coherence across slices, remaining legacy artifacts, operational readiness
- Include: final go/no-go for production cutover

## Workflow

1. Before starting, check if a plan folder already exists for this work.
2. If no plan exists, create one and ask the human to review before implementing.
3. For large plans, work in small reviewable, logical commit-sized steps.
4. Complete one step, report it, announce the next intended step, then wait
   for the human to approve or edit before continuing.
5. When the plan is complete, say so explicitly and include validation gaps
   or known follow-up work.

## Decision Rules

- Skip the plan for trivial changes (single file, obvious fix, no risk).
- Use plan review only for non-trivial, risky, multi-step, or explicitly
  review-gated work.
- Skip slice reviews for low-risk changes; use plan review + completion review.
- Always write a completion review when the plan had 3+ slices.
