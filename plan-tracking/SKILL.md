---
name: plan-tracking
description: Track implementation plans with structured progress and review artifacts for multi-step work.
---

# Plan Tracking

Use this skill when starting non-trivial, multi-step, or risky work that needs
a plan, progress tracking, and structured reviews.

## Plan Structure

Store all artifacts under `docs/plans/YYMM/DDHHMM-{short_descriptive_name}/`:
use local time and a concise lowercase hyphenated name.

The `YYMM` sub-folder (e.g. `2607/` for July 2026) groups plans by year-month
so the top-level `docs/plans/` stays browsable.  The folder name itself uses
`DDHHMM` since the year and month are already in the parent path.

Required files:

```text
docs/plans/YYMM/DDHHMM-{name}/
├── plan.md              # source of truth
├── progress.md          # current status for resumption
├── review/
│   ├── plan-01.md       # first plan review
│   ├── plan-02.md       # second plan review (if needed)
│   ├── slice-01-{name}.md
│   ├── slice-02-{name}.md
│   ├── completion-01.md # first completion review
│   └── completion-02.md # second completion review (if needed)
└── sub-plans/
    └── DDHHMM-{sub-name}/  # same structure as main plan
```

## Subplans

During execution, new work may surface that should be done after the main plan
completes.  Capture these as sub plans under a `sub-plans/` folder inside the main
plan directory.

- Name each sub plan folder `DDHHMM-{name}/` using the timestamp when it was
  created (no `YYMM` subdivision — the parent plan already provides context).
- Each sub plan contains the same files as the main plan: `plan.md`,
  `progress.md`, and a `review/` folder with its own review rounds.
- Create the `sub-plans/` folder only when the first sub plan is identified.

```text
docs/plans/YYMM/DDHHMM-{name}/
└── sub-plans/
    ├── DDHHMM-{sub-1}/
    │   ├── plan.md
    │   ├── progress.md
    │   └── review/
    └── DDHHMM-{sub-2}/
        ├── plan.md
        ├── progress.md
        └── review/
```

Sub plans are independent units — each tracks its own progress and reviews.
When the main plan references a sub plan, note it in `plan.md` with a link to
the sub plan folder.

## Writing Style

Write all plan artifacts in clear, easy-to-understand language. Avoid jargon,
ambiguous pronouns, and dense technical prose. Prefer short sentences, concrete
examples, and explicit names over vague references. A future agent (or human)
resuming work after days away should understand every line without needing to
decode it.

## Plan Creation

1. Create the plan folder with the timestamped name.
2. Write `plan.md` with:
   - Goal and scope — stated plainly so a newcomer can follow
   - A simple overview — explain the end-to-end approach in 3–6 short steps,
     including what happens now, what will change, and how the change fixes the
     problem. Keep this understandable without reading the detailed slices.
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

When presenting a new or revised plan to the human, include the same simple
overview in the response. Lead with the expected outcome, then summarize the
flow in plain language before linking to the detailed plan artifacts.

## Review Types

### Plan Review

Review `plan.md` before implementation starts.

- Create as `review/plan-{NN}.md` (start with `plan-01.md`)
- If the plan is revised after review, create a new round (`plan-02.md`, etc.)
- Cover: feasibility, risks, sequencing, missing assumptions, spec alignment
- Include: reviewer identity, method, findings by severity, overall go/no-go
- Write findings in plain language — state the problem, why it matters, and what to do about it

### Slice Review

Review a specific implementation commit after each slice is done.

- Create as `review/slice-{NN}-{name}.md` (e.g. `review/slice-01-signing.md`)
- Include:
  - Commit hash
  - Scope coverage table
  - Validation run results
  - Technical correctness notes against specs
  - Findings by severity — describe each issue plainly so someone unfamiliar with the code can understand it
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

- Create as `review/completion-{NN}.md` (start with `completion-01.md`)
- If the implementation is revised after review, create a new round (`completion-02.md`, etc.)
- Cover: end-to-end coherence across slices, remaining legacy artifacts, operational readiness
- Include: final go/no-go for production cutover
- State conclusions plainly — avoid hedging language that obscures the recommendation

## Workflow

1. Before starting, check if a plan folder already exists for this work.
   Look under `docs/plans/YYMM/` for the current month and recent months.
2. If no plan exists, create the `YYMM` sub-folder (if it doesn't exist yet)
   and a `DDHHMM-{name}` folder inside it. Ask the human to review before implementing.
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
- Create a sub plan when new work surfaces during execution that should follow
  the main plan, not interrupt it.
