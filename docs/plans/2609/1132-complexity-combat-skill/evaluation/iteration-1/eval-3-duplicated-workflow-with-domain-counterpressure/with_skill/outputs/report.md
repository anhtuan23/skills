# Evaluation: `module-refactor` vs `project-refactor`

## Scope and evidence

Compared the complete `SKILL.md` files and their companion READMEs, checked the
repository catalog, and inspected the Git history for both skills. No edits were
made to either skill or to repository source.

The skills are presented as separate capabilities in `README.md:14-15`:
`module-refactor` focuses on splitting and navigating a local code area, while
`project-refactor` addresses a project or feature's complete runtime path. The
history also shows separate origins: `module-refactor` was added on 2026-06-28;
`project-refactor` was added and then substantially updated on 2026-07-28.

## Prioritized candidate table

| Priority | Candidate | Evidence | Assessment | Recommendation |
|---|---|---|---|---|
| 1 | Blanket stateless-class removal | `project-refactor/SKILL.md:20-23,50-51` | Overly broad rule: absence of stored fields does not prove absence of behavior, a test seam, polymorphism, lifecycle, or safety responsibility. | Simplify, subject to human approval |
| 2 | Mandatory and repeated Mermaid diagrams | `project-refactor/SKILL.md:32-35,55,61`; `project-refactor/README.md:16-49` | A project-level topology diagram can justify itself, but requiring it for every “major cleanup” and repeating it in plan/checklist/final output adds an unclear artifact contract. | Simplify, subject to human approval |
| 3 | Beginner-comment requirement versus safety-only comments | `module-refactor/SKILL.md:40-41,61,81-83`; `project-refactor/SKILL.md:40-41` | The module skill requires comments on all touched functions; the project skill limits comments to non-obvious order/safety. The overlap is not exact, but the module rule can create comment churn and contradict its own “not just restate the code” check. | Simplify or keep for the narrower beginner-reader scope |
| 4 | Shared refactor workflow guidance | `module-refactor/SKILL.md:47-70`; `project-refactor/SKILL.md:14-44` | Both map behavior, choose ownership, update tests, and validate. This is expected workflow overlap, not proof of duplication: module scope is local file/API/test layout; project scope includes entrypoint-to-side-effect tracing, safety boundaries, approval, and full-project checks. | Keep unless a concrete maintenance cost is demonstrated |

## Candidate details

### 1. Blanket stateless-class removal — high priority

- **Location:** `project-refactor/SKILL.md:20-23,50-51`.
- **Observed behavior:** The skill instructs the user to avoid classes that do not
  store data and replace them with standalone input/output functions; the same
  prescription is repeated in the cleanup checklist.
- **Intended purpose:** Remove empty wrappers and simplify indirection during a
  broad project cleanup.
- **Complexity and cost:** It turns a useful smell into a shape-based rule. A
  stateless class may still provide a deliberate interface, dependency-injection
  seam, polymorphic collaborator, lifecycle boundary, or policy owner. Applying
  the rule mechanically can increase coupling or erase a safety boundary.
- **Counter-evidence:** The project skill explicitly says to preserve important
  safety checks and rules (`project-refactor/SKILL.md:10,20-23`), and a project-
  level refactor may encounter genuinely empty wrappers. However, no evidence in
  this repository establishes that stateless classes are always accidental.
- **Confidence and impact:** High confidence that the wording is over-broad;
  high potential impact if followed literally.
- **Smallest safe option:** Limit removal to classes that add no distinct
  behavior, safety responsibility, ownership, interface/test seam, or lifecycle;
  remove the duplicate checklist item or make it a conditional smell.
- **Recommendation:** Simplify after a human decision. If a concrete language or
  framework contract is involved, escalate that instance to its domain owner.

### 2. Mandatory and repeated Mermaid diagrams — medium-high priority

- **Location:** `project-refactor/SKILL.md:32-35,55,61` and
  `project-refactor/README.md:16-49`.
- **Observed behavior:** Major cleanups must include a Mermaid diagram in the
  plan; the checklist asks for one again; the final summary must include one.
  The companion README supplies two example diagrams and repeats the usage rule.
- **Intended purpose:** Make a project-level structural change and data flow easy
  for reviewers to see before approval.
- **Complexity and cost:** The artifact requirement is repeated across workflow,
  checklist, final output, and README. “Major cleanup” has no operational
  threshold, and a diagram can become stale or add little value for a small
  ownership-preserving cleanup.
- **Counter-evidence:** Unlike the module skill, project refactors can cross
  routes/workers, orchestration, persistence, and side effects; a topology diagram
  can expose safety and ownership changes. That is a valid domain counterweight,
  so this is not evidence that diagrams should be removed entirely.
- **Confidence and impact:** Medium-high confidence of over-specification;
  medium impact on workflow cost and review noise.
- **Smallest safe option:** Require one diagram only when the refactor materially
  changes runtime topology, ownership, or data flow; place it in the approved
  plan and summarize changes later without requiring a second copy.
- **Recommendation:** Simplify after a human decision, preserving the conditional
  project-level diagram use.

### 3. Beginner-comment requirement versus safety-only comments — medium priority

- **Location:** `module-refactor/SKILL.md:40-41,61,81-83` versus
  `project-refactor/SKILL.md:40-41`.
- **Observed behavior:** `module-refactor` asks for beginner-friendly comments
  on all touched functions and checks that comments explain purpose and behavior.
  `project-refactor` asks for brief comments only where ordering or a safety rule
  is non-obvious and explicitly explains why rather than syntax.
- **Intended purpose:** The module skill optimizes for navigation by a beginner;
  the project skill optimizes for preserving and explaining cross-cutting safety
  constraints.
- **Complexity and cost:** “All touched functions” can produce redundant
  comments, increase maintenance burden, and conflict with the project skill's
  narrower comment discipline when both are considered for a feature.
- **Counter-evidence:** This is partly a deliberate scope difference. A module
  refactor may reasonably add a local overview or targeted explanation even when
  a project refactor does not require broad documentation. The module skill also
  says comments must not merely restate code.
- **Confidence and impact:** Medium confidence; low-to-medium impact.
- **Smallest safe option:** Replace the blanket module requirement with comments
  for non-obvious purpose, sequence, side effects, or public contracts, plus a
  local README only when it materially improves navigation.
- **Recommendation:** Simplify if the intended documentation contract is shared;
  otherwise keep the module-specific beginner-reader goal and clarify its limit.

### 4. Shared refactor workflow guidance — low priority / screened as justified

- **Location:** `module-refactor/SKILL.md:47-70` versus
  `project-refactor/SKILL.md:14-44`.
- **Observed behavior:** Both skills tell the user to understand the current
  structure or runtime path, choose a clearer ownership shape, update tests, and
  validate the result.
- **Intended purpose:** These are the minimum behavior-preserving phases of any
  refactor. The module skill adds file/API/test-layout guidance; the project skill
  adds complete path tracing, safety checks, approval for major changes, and
  project-wide validation.
- **Complexity and cost:** Maintaining two versions of common workflow language
  can drift. However, deleting the shared guidance from either skill would make
  standalone use less safe and would force the user to infer the scope boundary.
- **Counter-evidence:** The different target scopes and safety contracts explain
  the overlap. `module-refactor` is local and focused; `project-refactor` is
  cross-cutting and runtime-oriented. The repository catalog also intentionally
  lists them separately.
- **Confidence and impact:** High confidence that the overlap is justified;
  low impact from the duplication.
- **Smallest safe option:** Keep both workflows, but if maintenance drift appears,
  extract only a short shared principle and retain scope-specific obligations in
  each skill. No current evidence requires that extraction.
- **Recommendation:** Keep.

## Overlap not currently treated as a candidate

Feature-based organization and avoiding generic buckets appear in both skills
(`module-refactor/SKILL.md:30-33`; `project-refactor/SKILL.md:25-27`), as do
dead/obsolete-code removal (`module-refactor/SKILL.md:34-37,58-59`;
`project-refactor/SKILL.md:35,54`). The module versions apply to the touched area;
the project versions apply to cross-project ownership and compatibility. Those
scope differences, plus the need to preserve safety and external contracts, are
enough counter-evidence to avoid calling either overlap accidental.

## First decision — stop here

**Candidate 1: Blanket stateless-class removal**

Observed evidence: `project-refactor/SKILL.md:20-23,50-51` directs users to replace
classes without stored data with standalone functions and repeats that rule in
the checklist.

It appears to address: removing empty wrappers and unnecessary indirection in a
project-wide cleanup.

Cost and counter-evidence: the rule conflates “no fields” with “no distinct
responsibility.” Stateless classes can still preserve interfaces, dependency
injection, polymorphism, lifecycle, testing seams, or safety policy. The
project-level safety goal is a reason to narrow the rule, not proof that every
such class should be removed.

Which decision applies?

- **Keep** — the complexity protects a real need; record the rationale.
- **Simplify** — approve the narrow follow-up scope: remove only classes with no
  distinct behavior, safety responsibility, ownership, interface/test seam, or
  lifecycle, and make the checklist conditional.
- **Defer** — record the owner, missing evidence, and concrete reopen trigger.
- **Escalate** — route language/framework-specific class-shape decisions to the
  relevant domain owner or specialist workflow.

