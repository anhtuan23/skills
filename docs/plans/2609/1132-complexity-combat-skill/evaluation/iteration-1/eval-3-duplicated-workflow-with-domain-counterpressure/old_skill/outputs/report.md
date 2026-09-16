# Complexity Combat evaluation report

## Scope and mutation boundary

Used the old snapshot at
`docs/plans/2609/1132-complexity-combat-skill/evaluation/skill-snapshot/SKILL.md` and compared only
`module-refactor/SKILL.md` with `project-refactor/SKILL.md`. The review was
read-only except for creating this requested report. Production skills, plan
files, progress files, README files, repository source, and existing worktree
changes were not edited.

The worktree already contained unrelated modifications and evaluation
artifacts before this review; they were left untouched.

## Candidate inventory

| Priority | Candidate | Locations | Initial assessment | Gate status |
| --- | --- | --- | --- | --- |
| 1 | Repeated refactor workflow and unclear routing boundary | `module-refactor/SKILL.md:22-70`; `project-refactor/SKILL.md:8-44` | Plausible medium-impact duplication, but likely intentional scope separation | Presented below; awaiting decision |
| 2 | Repeated cleanup and ownership rules | `module-refactor/SKILL.md:28-38,55-60`; `project-refactor/SKILL.md:20-38` | Plausible maintenance duplication; safety and scope wording differ | Not examined past the first gate |
| 3 | Documentation and comment requirements | `module-refactor/SKILL.md:40-43,61,80-83`; `project-refactor/SKILL.md:40-41,60-61` | Possible over-prescription and an inconsistent comment contract | Not examined past the first gate |
| 4 | Validation and reporting burden | `module-refactor/SKILL.md:68-70,96-106`; `project-refactor/SKILL.md:43-44,58-66` | Possible over-engineering for small changes; project-level obligations may be justified | Not examined past the first gate |
| 5 | Blanket stateless-class rule in the project skill | `project-refactor/SKILL.md:20-23,51` | Concrete over-generalization candidate, but not duplicated guidance | Not examined past the first gate |

## Candidate 1: repeated refactor workflow and unclear routing boundary

### Observed behavior

Both skills describe a behavior-preserving structural cleanup workflow:

- `module-refactor` maps entrypoints, helpers, tests, imports, and local
  ownership; chooses file/API boundaries; moves code; mirrors the production
  layout in tests; and runs focused validation (`module-refactor/SKILL.md:47-70`).
- `project-refactor` traces the complete path from input through decisions,
  persistence, and results; explains it in plain language; preserves safety
  rules; updates production/tests/docs/configuration consistently; and runs
  local plus full validation (`project-refactor/SKILL.md:14-18,20-23,32-44`).
- The goals also overlap: both promise a simpler structure while preserving
  behavior (`module-refactor/SKILL.md:22-24`; `project-refactor/SKILL.md:8-10`).

The repeated principles include feature-oriented organization
(`module-refactor/SKILL.md:30`; `project-refactor/SKILL.md:25-27`), structural
mapping (`module-refactor/SKILL.md:47-49`; `project-refactor/SKILL.md:14-18`),
removal of obsolete indirection (`module-refactor/SKILL.md:34-37,58-59`;
`project-refactor/SKILL.md:20-23,35`), and preserving behavior through tests
and validation (`module-refactor/SKILL.md:62-70`;
`project-refactor/SKILL.md:37-44`).

### Intended purpose and scope counterpressure

The apparent purpose is to provide two entry points for different refactor
sizes:

- The module skill is for one existing code area. It focuses on file splitting,
  local ownership, public-surface narrowing, colocated tests, a conditional
  local README, and focused checks (`module-refactor/SKILL.md:3,31-43,62-70`).
- The project skill is for a project or feature whose runtime path and safety
  boundaries must be understood end to end. It adds data-loss/race/crash
  counterpressure, a plan and approval for major changes, consistency across
  configuration and composition, and full-project testing
  (`project-refactor/SKILL.md:3,14-23,32-44`).

The repository catalog also presents them as different scopes: “split large
modules into smaller focused files” versus “refactor a project around clear
runtime flow and ownership” (`README.md:14-15`). That is evidence for a
deliberate boundary, not proof that the repeated workflow is accidental.

### Complexity and cost

- A user may not know whether a multi-file change is a module refactor or a
  project refactor, especially because both descriptions include “feature” and
  both require mapping, cleanup, tests, and validation.
- The same general principles exist in two maintenance locations and could
  drift. For example, the module skill permits focused validation, while the
  project skill asks for full tests, linters, and type checks.
- If both skills are invoked for one task, the overlapping steps can create
  duplicated planning and reporting rather than additive evidence.

This is an instruction-routing and maintenance cost, not evidence that either
workflow is itself unsafe or that fewer lines would automatically be better.

### Counter-evidence

- The module skill has local structural concerns that do not appear in the
  project skill: splitting long files, deciding which helpers become private,
  placing callers before helpers, and matching tests to production ownership
  (`module-refactor/SKILL.md:31,38-40,50-67`).
- The project skill has broader safety and coordination obligations that do not
  appear in the module skill: preserving rules against data loss, races, and
  crashes; obtaining approval for major cleanups; updating configuration; and
  testing the whole project (`project-refactor/SKILL.md:20-23,32-44`).
- Both skills are standalone documents. Removing the shared principles from
  one could make that skill less usable when invoked without the other.
- No caller, evaluation contract, or observed user failure was found proving
  that the current overlap causes wrong routing. The evidence supports
  “possible duplication with different contracts,” not “merge or delete.”

### Confidence, impact, and smallest safe option

Confidence: medium. Impact: medium. The safest simplification, if approved,
would be a narrow routing clarification: state explicitly that
`module-refactor` owns a bounded code area and `project-refactor` owns
cross-module or end-to-end feature/project changes, while retaining each
skill's local safety and validation contract. A shared third document or
wholesale removal of repeated guidance would need stronger evidence because it
could increase indirection or erase standalone context.

Recommendation before the human gate: defer simplification unless routing
confusion or instruction drift is demonstrated; keep the two scopes separate
if the project intentionally invokes skills independently. If the scopes are
not intentionally distinct, escalate to the skill owner before consolidating
their contracts.

## First decision question

**Candidate 1: repeated refactor workflow and unclear routing boundary**

This guidance addresses: “Let a bounded module refactor preserve local
ownership and focused validation, while a project refactor traces the complete
runtime path and preserves broader safety, approval, configuration, and
full-validation obligations.”

Observed evidence: “The skills repeat mapping, feature grouping, cleanup,
behavior preservation, tests, and validation, but the module skill is local and
focused (`module-refactor/SKILL.md:47-70`) while the project skill is broader
and safety/coordination-oriented (`project-refactor/SKILL.md:14-44`).”

Cost and counter-evidence: “The overlap may cause routing ambiguity and
instruction drift, but the repository catalog names distinct scopes
(`README.md:14-15`), and removing repeated standalone guidance could erase
important local or project-level safeguards.”

Which decision applies?

- **Keep** — the two skills serve intentionally different scopes and safety
  contracts; record that rationale.
- **Simplify** — approve only a narrow routing clarification or other bounded
  follow-up; do not merge contracts yet.
- **Defer** — keep the current split until a concrete routing failure or drift
  trigger appears.
- **Escalate** — route the scope decision to the skill owner or a broader
  workflow-design review.

The evaluation stops here pending this one decision; later candidates have not
been examined past the inventory.
