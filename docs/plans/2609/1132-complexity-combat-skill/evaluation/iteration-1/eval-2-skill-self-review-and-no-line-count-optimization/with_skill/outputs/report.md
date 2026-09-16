# Complexity Combat self-review report

Target: `complexity-combat/SKILL.md`

Scope was read-only. No production skill, plan, progress, README, or
repository source was edited. The only output created by this evaluation is
this report.

## Candidate inventory

| Priority | Candidate | Location | Initial assessment |
| --- | --- | --- | --- |
| 1 | Overlapping anti-metric guidance | `complexity-combat/SKILL.md:51-53` and `:79-80` | Possible documentation redundancy, but currently protects an explicit contract; low confidence that it should change |

No line-count reduction is being proposed merely because the skill contains
overlapping prose. The candidate is being reported because the two passages
may express related safeguards, not because fewer lines are inherently better.

## Candidate 1: overlapping anti-metric guidance

### Location

- `complexity-combat/SKILL.md:51-53`: tells the agent not to optimize for line
  count, remove a one-implementation abstraction solely for that reason, or
  treat cyclomatic/cognitive-complexity thresholds as universal refactoring
  rules.
- `complexity-combat/SKILL.md:79-80`: says metrics and code shape are evidence
  only, and uncertainty must be stated when purpose, cost, or contract cannot
  be established.

### Observed behavior

The first passage is an explicit prohibition against metric- or shape-driven
refactoring. The second is an evidence rule used during the workflow: metrics
and code shape may inform a candidate, but cannot establish accidental
complexity without purpose, cost, and contract evidence.

They overlap around the idea that measurements and code shape are not proof,
but they are not identical. The first names concrete failure modes, including
line-count optimization and universal complexity thresholds; the second
governs how evidence must be weighed and how uncertainty is reported.

### Intended purpose and current caller/contract

The apparent purpose is to prevent a complexity scan from becoming an
automated code-golf or threshold-enforcement workflow while still allowing
metrics to be useful signals.

This protection has a current contract and caller:

- The skill's own workflow at `:84-100` requires observed behavior, intended
  purpose, cost, counter-evidence, confidence, and a recommendation before a
  candidate can be called accidental.
- The local improvement plan requires that the skill not optimize for line
  count or treat cyclomatic/cognitive thresholds as proof
  (`docs/plans/2609/1132-complexity-combat-skill/plan.md:76-80`).
- This evaluation request explicitly requires “no line count optimization,”
  making the anti-line-count rule a live evaluation contract, not unused
  prose.
- There is no runtime caller: this is an instruction contract consumed by an
  agent during a review. The repository README identifies the skill as a
  pre-simplification, human-gated workflow, which is consistent with that
  contract.

### Complexity and cost

Maintaining two nearby safeguards costs a small amount of reading and creates
a possible future wording-drift question. A later editor could wonder whether
the concrete prohibition at `:51-53` or the general evidence rule at `:79-80`
is authoritative.

The observed cost is documentation overlap only. There is no evidence of a
conflicting instruction, an active caller that is confused, or a validation
failure caused by the two passages.

### Counter-evidence

- Removing `:51-53` would weaken the explicit protection against the exact
  failure mode under evaluation: optimizing merely for fewer lines or applying
  complexity thresholds as universal rules.
- Removing `:79-80` would weaken the broader workflow requirement that all
  metrics and code shape remain subordinate to purpose, cost, and contract
  evidence.
- The local plan treats both behaviors as acceptance criteria, so the apparent
  duplication currently has a documented contract behind it.
- The two passages operate at different levels: one is a concrete “do not”
  guardrail, and one is a general evidence standard.

### Confidence and impact

Confidence that there is textual overlap: medium-high.

Confidence that the overlap is accidental: low.

Impact if simplified incorrectly: medium, because the skill could drift toward
line-count optimization or threshold-based refactoring despite its intended
human-gated evidence standard.

### Smallest safe option

Keep both passages unless a later edit can preserve both contracts in one
shorter rule and validate the three concrete protections: no line-count
optimization, no universal cyclomatic/cognitive thresholds, and no candidate
label without purpose/cost/contract evidence. No edit is approved by this
scan.

### Recommendation

**Keep pending human decision.** The overlap is real but currently justified by
two related safety contracts with different scope. Reopen a simplification only
if the wording is consolidated without losing the concrete anti-line-count and
anti-threshold examples, or if a future evaluation demonstrates that agents
misread the two passages as conflicting or duplicative requirements.

## First decision question

**Candidate 1: overlapping anti-metric guidance**

Observed evidence: “`SKILL.md:51-53` explicitly prohibits line-count and
universal-threshold optimization, while `:79-80` makes metrics and code shape
evidence only. They overlap, but the first gives concrete prohibitions and the
second states the general evidence standard.”

It appears to protect: “An evidence-backed, human-gated review workflow that
does not turn line count or complexity metrics into automatic refactoring
criteria. This protection is a current contract in the local plan and in this
evaluation request; it has no runtime caller.”

Cost and counter-evidence: “The two passages add a small maintenance and
authority question, but no conflicting behavior or current confusion was
found. Removing either passage could weaken a distinct part of the contract,
especially the explicit no-line-count requirement.”

Which decision applies?

- **Keep** — the two-level guardrails protect real review behavior; record the rationale.
- **Simplify** — approve a narrow wording-consolidation scope before any edit.
- **Defer** — record the missing evidence and a concrete reopen trigger.
- **Escalate** — route the contract/wording decision to the skill owner or review workflow.

Per the requested evaluation workflow, scanning stops here pending this one
decision.
