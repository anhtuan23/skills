# Plan: Improve project-refactor skill

## TLDR

Strengthen `project-refactor` as a project-level, behavior-preserving workflow
organized around dependency control: high cohesion and low coupling, explicit
dependency direction, acyclic module graphs, and small stable interfaces that
hide implementation details. The revised skill will map the real runtime flow
and blast radius, establish a behavioral baseline when coverage is weak, require
an approved on-disk plan for non-trivial restructuring, and execute small
independently verified slices. It will replace universal style rules with
evidence-based decisions and make the boundaries with `module-refactor`,
`long-file-refactor`, and `complexity-combat` explicit.

## Goal and scope

### In scope

- Revise `project-refactor/SKILL.md` while keeping its name and directory.
- Define the skill's ownership: cross-module or project-level restructuring,
  runtime-flow cleanup, and ownership-boundary changes.
- Make dependency control the primary design lens: high cohesion/low coupling,
  explicit dependency direction, the Acyclic Dependencies Principle, and
  information hiding through small stable interfaces.
- Add routing rules for bounded module work, long-file splitting, complexity
  diagnosis, feature work, bug fixes, migrations, and security-sensitive work.
- Require evidence before changing structure: target, intended benefit, runtime
  path, callers/dependencies, contracts, tests, history/configuration, and
  relevant external or dynamic references.
- Add a characterization or equivalent baseline path for under-tested behavior,
  including error paths and observable side effects.
- Require an approved plan with non-goals, dependency-ordered slices,
  entry/exit checks, rollback or recovery notes, and risk-based validation.
- Replace absolute rules about feature folders, stateless classes, deletion,
  diagrams, comments, and full-suite testing with conditional guidance.
- Align `project-refactor/README.md` so it does not advertise superseded
  mandatory rules; keep it a concise companion, not a second workflow.

### Out of scope

- Changes to production source code, tests, configuration, or other skills.
- Language-specific refactoring commands or universal complexity thresholds.
- Autonomous implementation of a project refactor.
- Automatic commits, pushes, deployment, or public API/migration decisions.
- Rewriting the broader plan-tracking system.

The revised skill and README should remain portable, concise, and below the
skill-creator recommendation of 500 lines for the main skill body.

## Findings from the current repository

The current `project-refactor/SKILL.md` has useful behavior-preservation intent,
but its latest form is more prescriptive than its earlier version:

- It says every project should be organized by feature and that technical
  layers such as `services/`, `utils/`, and `handlers/` should be avoided.
- It directs agents to replace all stateless classes with standalone functions.
- It requires a Mermaid diagram for every major cleanup and full project tests,
  linters, and type checks without requiring the commands to be discovered.
- It does not define a behavioral contract, characterization-test path, exact
  blast-radius inventory, per-slice stop rules, or an honest way to report
  validation gaps.
- It has no explicit routing boundary with the existing `module-refactor`,
  `long-file-refactor`, and `complexity-combat` skills.
- Its companion README duplicates the same universal folder, class, and diagram
  rules, so changing only the skill would leave contradictory guidance.

The local sibling skills support a more conditional design: bounded module
work belongs to `module-refactor`; long-file splitting belongs to
`long-file-refactor`; and complexity candidates should be evidence-backed and
human-decided under `complexity-combat`. The user's dependency-control notes
will be the organizing theory for the revised workflow rather than an
additional checklist at the end.

## Online research findings

Comparable public skills and workflows suggest these additions:

- [Characterization testing skill](https://github.com/moogah/claude_skills/blob/main/characterization-testing/SKILL.md)
  captures what the system does now, including edge cases, and runs the
  baseline before structural changes. It also treats characterization tests as
  temporary scaffolding rather than a replacement for a proper specification.
- [Refactor safety net](https://github.com/wilddoc/claude-code-skills-pack/blob/main/skills/refactor-safety-net/SKILL.md)
  defines the exact boundary whose external behavior must remain stable,
  includes exception/error behavior, and says not to edit a failing
  characterization test merely to make a refactor pass.
- [Goal-workflow refactor](https://github.com/smallnest/goal-workflow/blob/master/skills/refactor/SKILL.md)
  requires a named problem, evidence, expected impact, smallest refactoring,
  baseline, and counter-pressure checks against false abstractions. It treats
  metrics as signals rather than proof and recommends skipping refactoring with
  no clear benefit.
- [Blast-radius analyzer](https://github.com/event4u-app/agent-config/blob/main/src/skills/blast-radius-analyzer/SKILL.md)
  pins the exact symbol or contract first, then inventories callers, overrides,
  tests, factories, database/configuration references, and documentation.
- [Architectural refactor](https://github.com/petekp/agent-skills/blob/main/skills/architectural-refactor/SKILL.md)
  externalizes an ordered plan, gives each chunk entry/exit criteria, and
  stops when execution drifts from the approved plan. This supports the local
  plan/progress artifact convention without requiring a heavy manifest in the
  portable skill.
- [Go refactoring workflow](https://github.com/samber/cc-skills-golang/blob/main/skills/golang-refactoring/SKILL.md)
  reinforces small tool-driven steps, separation of structural and behavioral
  changes, human sign-off for cross-package moves/API changes/deletion, and
  checks for reflection or tags that ordinary reference search misses. These
  ideas will be generalized rather than made Go-specific.

## Proposed workflow changes

### 1. Scope and routing

Add a clear `When to use` / `When not to use` section:

- Use this skill when several modules, a runtime flow, or an ownership boundary
  must be reorganized while preserving observable behavior.
- Route a bounded package/file cleanup to `module-refactor`, a long mixed file
  to `long-file-refactor`, and an open-ended complexity scan to
  `complexity-combat`.
- Do not treat a feature addition, bug fix, migration, rewrite, security
  change, or performance optimization as a behavior-preserving refactor unless
  the separate workflow and scope are explicit.

### 2. Understand the current system

Before proposing a target shape:

- Read repository instructions, local conventions, relevant history, and the
  canonical build/test/lint/type-check commands.
- Name the exact target and the concrete benefit expected from restructuring.
- Trace entrypoints, orchestration, state guards, side effects, persistence,
  external boundaries, lifecycle/concurrency behavior, and outputs.
- Map the relevant dependency graph: modules/packages, runtime versus test/build
  edges, permitted dependency directions, existing cycles, and the public
  interfaces that cross each boundary.
- Inventory direct and indirect callers, tests, configuration, docs, generated
  files, reflection/tag/template references, and wire/API contracts where
  relevant.
- Separate observed facts from inferred purpose and unresolved uncertainty.

Write a compact behavioral contract for the affected boundary: inputs and
outputs, errors/codes/messages where callers may depend on them, side effects
and ordering, persistence or schema shape, lifecycle/concurrency guarantees,
and performance only when performance is part of the claim. If coverage is
insufficient, add characterization tests or another explicit baseline before
changing the structure. Record surprising behavior as behavior to preserve,
not as an implicit bug fix.

### 3. Dependency-control design lens

Use these four questions to judge the proposed structure:

1. **Cohesion and locality** — Do related responsibilities change together for
   a real reason, and will a normal change stay within a small boundary? Do not
   group code by feature name alone if ownership, lifecycle, or change coupling
   says another boundary is clearer.
2. **Dependency direction** — Which layers or packages may depend on which
   others? Keep policy and domain decisions independent of replaceable
   implementation details when the project has that boundary. Put adapters at
   the edge, but do not introduce Clean/Hexagonal/Onion layers without a real
   dependency or change-isolation benefit.
3. **Acyclic graph** — Does the target preserve or improve an acyclic module
   graph? Identify every new edge and any cycle it creates. Break cycles at the
   smallest meaningful ownership boundary rather than hiding them in a generic
   shared package or adding speculative indirection.
4. **Information hiding** — Is each boundary's public surface as small and
   stable as practical? Keep implementation details private, expose contracts
   rather than concrete details, and verify that an interface or compatibility
   bridge has a real consumer, variation, or migration need.

Record the baseline and target graph, the allowed edge directions, the cycles
removed or intentionally retained, and the public-surface changes in the plan.

### 4. Design and approval gate

Choose the smallest structural change that addresses the named problem. Test
each proposed abstraction, feature grouping, layer, class-to-function change,
compatibility bridge, and deletion against current callers, ownership,
framework/protocol requirements, lifecycle, safety, likely change coupling,
dependency direction, cycle risk, and interface size. Feature organization is
a useful default, not a universal law; retain a technical, domain, boundary, or
lifecycle structure when it improves cohesion or reduces coupling.

For non-trivial, cross-module, public-surface, deletion, untested, or
high-risk work, write an approved plan through `plan-tracking`. The plan must
name the target and non-goals, list affected boundaries, order independently
verifiable slices, state entry/exit checks and recovery options, and call out
compatibility decisions. Use a diagram only when the topology, ownership, or
data flow is broad enough that it materially helps review.

Do not begin implementation until the human approves that plan. A plan is not
permission to mix in unrelated bug fixes, feature work, or opportunistic
cleanup.

### 5. Execute in verified slices

- Start from a known, recoverable baseline according to repository policy.
- Make one coherent structural change at a time, preferably with mechanical or
  tool-supported renames/moves where available.
- Keep the public behavior and the recorded contract stable. Update production
  code, composition wiring, tests, docs, configuration, and dynamic references
  together.
- After each structural slice, re-check dependency direction, cycle status,
  change locality, and the boundary's public surface; a compiling refactor can
  still make ownership or dependency propagation worse.
- After each slice, run the focused checks and inspect the diff. Stop on an
  unexpected failure, reference, file, or behavior change; update the plan and
  ask for direction rather than improvising.
- Do not delete old files, compatibility paths, generated artifacts, or public
  symbols until callers, deployment/rollback order, history, and dynamic
  references have been checked and the compatibility decision is explicit.
- Add comments or README material only for non-obvious invariants, side
  effects, ordering, external contracts, or safety constraints; do not restate
  obvious code.

### 6. Validate and report honestly

Use a validation ladder appropriate to the repository and risk:

1. Focused tests/checks for the changed boundary after every slice.
2. Affected package/module checks and characterization tests.
3. Repository-wide tests, type checks, linters, builds, smoke tests, or
   benchmarks when the project exposes them and the risk warrants them.

For dependency-control claims, compare the before/after graph or an equivalent
repository-native report, check for new cycles, inspect imports/references that
cross the boundary, and review the exported/public surface. Report improvement
as structural evidence (for example, fewer cross-boundary edges or a removed
cycle), not as a promise that future changes can never spread.

Discover commands from the repository; never invent a command. Preserve the
existing error, retry, transaction, cleanup, lifecycle, and concurrency
semantics. If a check cannot run, report the exact gap and its risk instead of
claiming full validation. Run `git diff --check` when Git is available.

The final report should state the named problem and benefit, before/after
ownership and runtime flow, changed/removed/renamed paths, compatibility
decisions, contract evidence, validation results, unresolved risks, and a
concise suggested commit message. Do not commit automatically.

## Ordered implementation slices

1. **Revise `SKILL.md`** — make dependency control the primary design lens,
   replace the universal rules with the scoped workflow above, add routing/stop
   rules, and keep the skill concise and portable.
2. **Align `README.md`** — reduce duplicated prescriptions and point readers to
   the revised workflow; preserve only a short orientation and example where it
   remains accurate.
3. **Validate the documentation** — check frontmatter, line count, internal
   references, Markdown rendering/link targets where tooling exists, and
   `git diff --check`. Run old-versus-revised behavior-oriented prompts for
   project-level refactor, bounded-module routing, under-tested behavior,
   public/dynamic reference changes, and out-of-scope feature/bugfix requests.
4. **Independent review** — review for trigger drift, unsafe universal advice,
   overlap with sibling skills, missing approval/stop gates, and unnecessary
   verbosity. Write findings into this plan folder, address material findings,
   update progress, and return the result for final human review.

## Validation criteria

- Frontmatter remains valid and the main skill body is below 500 lines.
- The description identifies project-level, behavior-preserving restructuring
  and does not over-trigger for local module or complexity-only work.
- The skill names a target, intended benefit, non-goals, and evidence required
  before choosing a structure.
- It treats high cohesion/low coupling, dependency direction, ADP, and
  information hiding as design tests grounded in the repository's actual graph,
  not slogans or mandatory Clean Architecture adoption.
- It defines the observable contract and a characterization/baseline path when
  tests are inadequate.
- It inventories cross-module and dynamic/external references when relevant.
- It records dependency edges, permitted directions, cycle status, and public
  surface changes for relevant project-level work.
- It distinguishes runtime/package cycles from test/build/support edges and
  requires any retained intentional cycle to be documented and contained.
- It does not require feature folders, pure functions, diagrams, comments, or
  full-suite checks in cases where evidence does not justify them.
- It requires human approval for non-trivial changes and stops on drift,
  unexpected failures, public-surface changes, deletion risk, or missing
  contract evidence.
- It validates in focused-to-broad order using discovered project commands and
  reports gaps honestly.
- The README and SKILL agree, and sibling skill boundaries are clear.
- The final diff contains only the approved skill/docs/plan artifacts and any
  explicitly retained evaluation artifacts.

## Risks and open questions

- A project-level workflow can become too heavy for a small change. Keep the
  evidence and planning depth proportional to blast radius and risk.
- “Project-level” is repository-dependent. Use affected boundaries and change
  coupling, not a file-count threshold, to decide scope.
- Characterization tests capture current behavior, including undesirable quirks;
  a separate approved behavior change is needed to correct them.
- Dynamic dispatch, generated code, deployment sequencing, and public consumers
  may remain invisible to ordinary static search. The skill should surface the
  uncertainty and escalate rather than imply proof.

## Approval gate

Research and planning are complete. Implementation starts only after human
approval of this plan. After approval, the coordinator will revise the skill
and README, run the documented validation, perform the independent review,
address material findings, update `progress.md`, and return the result for
final human review.
