# Complexity Combat self-review report

## Scope and mutation boundary

Reviewed only the old snapshot at
`docs/plans/2609/1132-complexity-combat-skill/evaluation/skill-snapshot/SKILL.md` (71 lines). The review
was read-only except for creating this requested report. The production skill,
plan, progress file, README, repository source, and existing worktree changes
were not edited.

No executable caller for the old snapshot was found. The repository does have
current textual contracts for the skill's human gate:

- `README.md:11` catalogs `complexity-combat` as asking the human which
  problems are real before simplifying.
- `docs/plans/2609/1132-complexity-combat-skill/plan.md:23` requires retaining
  a one-candidate-at-a-time human gate.
- `docs/plans/2609/1132-complexity-combat-skill/evaluation/evals/evals.json:14-15` expects a report with a
  one-candidate human gate and explicitly rejects line-count optimization as
  the basis for simplification.

## Candidate inventory

| Candidate | Location | Initial assessment |
| --- | --- | --- |
| 1. Human-gate control split across two sections | `SKILL.md:52-71` | Plausible low-impact structural duplication; decision required |

## Candidate 1: human-gate control split across two sections

### Observed behavior

The `Reality Check (Human Gate)` section tells the agent to ask about
candidates one at a time, use the problem statement in the question, offer
three outcomes, wait for the response, and accept a confirmed real problem
(`SKILL.md:52-64`). The separate `Decision Rules` section repeats part of that
control flow and adds the disputed-answer behavior, rationale recording, and a
fallback to ask when uncertain (`SKILL.md:66-71`).

This is not a mere repeated sentence. It is one behavioral gate described in
two adjacent structures: the first presents and sequences the question; the
second handles post-answer exceptions and persistence of the decision.

### Intended protection and current contract

The split protects against silently simplifying code, batching human
decisions, accepting an unsupported finding after disagreement, or losing the
human's rationale. Those are the safety properties of the skill's approval
boundary.

There is no code-level caller to prove that each rule is independently
consumed. However, the README, active plan, and evaluation contract above are
current textual callers/constraints for the combined behavior. In particular,
removing the `Decision Rules` section wholesale would weaken the explicit
pushback and rationale-recording behavior; removing the `Reality Check` section
would weaken the one-at-a-time presentation and wait boundary.

### Complexity and cost

- A future change to the human-gate behavior must keep two sections aligned.
- The authority boundary is slightly unclear: the workflow says to accept a
  real problem and move on, while the decision rules add a pushback branch for
  cases where the agent disagrees with the human.
- This is an instruction-maintenance and interpretation cost, not a line-count
  problem and not a demonstrated runtime defect.

### Counter-evidence

- The sections serve different phases and are complementary rather than
  identical: presentation/sequencing versus response handling.
- The one-candidate gate is explicitly required by current project planning
  and evaluation material, so simplification must preserve it exactly.
- The old skill's three response choices do not fully express the pushback and
  rationale-recording rules; consolidating them carelessly could erase a
  safety behavior.
- No observed user or agent failure shows that the split currently causes
  confusion.

### Confidence and impact

Confidence: medium. Impact: low. The candidate is plausible because it has two
maintenance points, but the protected contract is real and the likely failure
is instruction drift rather than unsafe code execution.

### Smallest safe option

If simplification is approved, consolidate only the control-flow wording into
one canonical human-gate sequence while retaining the separate requirements to
ask one candidate at a time, wait, push back with concrete risk when needed,
and record the final rationale. Do not remove the gate or infer that fewer
lines is itself a benefit. Any edit would require a separately approved scope
and a check against the README, plan, and evaluation contract.

### Recommendation

Keep or defer pending the human decision. The evidence does not justify
calling the two sections accidental merely because they are adjacent or
partially repetitive.

## First decision question

**Candidate 1: human-gate control split across two sections**

This code addresses: “Preserve a one-candidate-at-a-time human approval
boundary, including explicit handling of disagreement and recording the
decision rationale.”

Observed evidence: “`SKILL.md:52-64` defines how to present and wait for each
candidate; `SKILL.md:66-71` defines pushback, acceptance after pushback,
rationale recording, and asking when uncertain.”

Cost and counter-evidence: “The same behavioral gate has two maintenance
locations, but the sections cover different phases and are backed by current
README, plan, and evaluation contracts. No behavior failure has been shown.”

Which decision applies?

- **Keep** — the two sections protect distinct phases of a required human gate.
- **Simplify** — approve a narrow consolidation while preserving every listed
  gate behavior.
- **Defer** — keep the skill unchanged until instruction drift or user/agent
  confusion provides stronger evidence.

The review stops here pending this one decision; no later candidate is
examined.
