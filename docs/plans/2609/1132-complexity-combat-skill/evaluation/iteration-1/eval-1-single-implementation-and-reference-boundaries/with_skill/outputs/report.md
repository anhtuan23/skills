# Complexity Combat report

Target: `git-reconcile/`

Scope was read-only. The existing worktree changes outside the target were
left untouched. No production skill, plan, progress, README, or repository
source was edited.

## Candidate inventory

| Priority | Candidate | Location | Initial assessment |
| --- | --- | --- | --- |
| 1 | Duplicated classification contract | `git-reconcile/SKILL.md:73-81`; `git-reconcile/references/conflict-reconciliation.md:92-103` | Plausible accidental complexity; decision required |

The scan found no literal interface, abstract class, factory, or wrapper with a
single implementation in this documentation-only skill. The closest
single-implementation-style concern is the manually duplicated classification
contract above.

## Candidate 1: duplicated classification contract

### Location

- Entrypoint taxonomy: `git-reconcile/SKILL.md:73-81`.
- Detailed taxonomy: `git-reconcile/references/conflict-reconciliation.md:92-103`.
- Entrypoint routes classification work to the reference at
  `git-reconcile/SKILL.md:44-47`.
- The labels are also consumed by the completion-report guidance at
  `git-reconcile/SKILL.md:69-71` and the rebase procedure at
  `git-reconcile/references/rebase.md:74-76`.

### Observed behavior

The same five labels are maintained twice:

`disjoint-intent`, `same-question-different-answer`, `superseded`,
`structural-port`, and `unsafe-or-unresolved`.

The entrypoint table provides a short meaning and default response. The shared
reference provides a test and resolution for the same labels. There is no
generated source, validation step, or other synchronization mechanism; these
are two manually editable representations.

The first four rows are substantively aligned but independently worded. The
`unsafe-or-unresolved` row is less exact across the two locations: the
entrypoint enumerates binary, submodule, generated, schema/migration/deployment
risk, missing intent, and unresolved ambiguity, while the reference summarizes
this as opaque artifacts or insufficient evidence.

### Intended purpose

The entrypoint appears intended to expose the vocabulary during discovery and
completion reporting, while the reference supplies the operational per-hunk
classification procedure. This matches the plan's stated design that
`SKILL.md` contains classification names and references hold command-level
details (`docs/plans/2609/151843-advanced-git-reconciliation/plan.md:31-36`).

### Complexity and cost

- A future taxonomy change must update two tables and keep their meanings
  aligned.
- Different wording creates a drift/authority question: an agent may treat the
  short entrypoint definition or the detailed reference definition as the
  canonical behavior.
- The duplication is small, but it is structural rather than merely repeated
  prose: both tables define the same classification contract.

### Counter-evidence

- The entrypoint is the discovery surface, and its short table may improve
  routing without requiring the agent to open a reference immediately.
- The reference table adds per-hunk tests and resolutions, so it is not a
  byte-for-byte duplicate.
- The four-reference boundary was deliberate: the approved plan explicitly
  calls for four focused references to keep the entrypoint concise
  (`docs/plans/2609/151843-advanced-git-reconciliation/plan.md:5-10`), and the
  review found no blocking issue with that layout
  (`docs/plans/2609/151843-advanced-git-reconciliation/review/plan-01.md:10-18`).
- The current wording is compatible enough that no demonstrated runtime defect
  or user-facing misclassification was found. The risk is maintenance drift,
  not proven behavior failure.

### Confidence and impact

Confidence: medium. Impact: low to medium. The cost is maintenance and
instruction-authority ambiguity; there is no evidence here of a live Git safety
failure.

### Smallest safe option

If simplification is approved, choose one authoritative classification
definition and make the other location a short pointer or compact index. Keep
the five labels discoverable in `SKILL.md`, preserve the detailed tests and
resolutions in `conflict-reconciliation.md`, and validate every reference to
the labels plus the completion-report format. No edit is approved by this
scan.

### Recommendation

**Defer pending human choice** between keeping the intentional discovery
summary and simplifying the duplicated contract. Reopen with a narrow edit if
the taxonomy changes, if the two tables diverge, or if agents show confusion
about which definition governs. The four-reference split itself should remain
deferred rather than treated as accidental until there is evidence that the
reading/routing cost outweighs its deliberate separation.

## First decision question

**Candidate 1: duplicated classification contract**

Observed evidence: “The five classifications are manually defined in both
`git-reconcile/SKILL.md:73-81` and
`git-reconcile/references/conflict-reconciliation.md:92-103`; the wording is
mostly aligned but not identical, and there is no synchronization mechanism.”

It appears to address: “A concise discovery/reporting vocabulary in the
entrypoint plus detailed per-hunk classification tests and resolutions in the
shared reference.”

Cost and counter-evidence: “This creates two maintenance points and a possible
authority/drift problem, especially for `unsafe-or-unresolved`. However, the
plan deliberately assigns classification names to the concise entrypoint and
details to focused references, and no behavior failure has been demonstrated.”

Which decision applies?

- **Keep** — the duplicated summary protects discoverability; record the rationale.
- **Simplify** — approve a narrow follow-up scope before any edit.
- **Defer** — record the missing evidence and a concrete reopen trigger.
- **Escalate** — route the taxonomy/skill-boundary decision to the relevant owner or specialist workflow.

Per the requested evaluation workflow, scanning stops here pending that one
decision.
