---
name: project-refactor
description: Reorganize several modules, a runtime flow, or an ownership boundary while preserving observable behavior. Use for evidence-backed, project-level refactoring; route bounded module, long-file, and complexity-only work to the narrower skill.
---

# Project Refactor

Use this skill for structural change across module boundaries, runtime flows, or
ownership boundaries when the intended behavior must stay the same. The goal is
better change locality and clearer ownership, not a preferred architecture or a
lower line count.

## Scope and routing

Use this skill when the target spans several modules, changes who owns a
responsibility, or requires a project-level dependency and runtime-flow change.

Route instead when the narrower workflow is the real owner:

- `module-refactor`: a bounded package, module, or file cleanup.
- `long-file-refactor`: splitting one long mixed file.
- `complexity-combat`: an open-ended scan for accidental complexity. It reports
  candidates and waits for a human decision; it does not authorize edits.

Feature work, bug fixes, migrations, rewrites, performance optimization, and
security changes need their own explicit behavior and risk scope. Do not call
them behavior-preserving refactors by default.

## Workflow

### 1. Name the target and current behavior

Before choosing a target structure, inspect repository instructions,
conventions, history, configuration, and the canonical commands. State:

- the exact target and the concrete benefit expected;
- the non-goals, especially behavior changes and unrelated cleanup;
- the entrypoints, runtime path, ownership boundaries, and affected contracts;
- observed facts, inferred intent, and unresolved uncertainty separately.

Trace the real flow: inputs, orchestration, decisions, state guards, side
effects, persistence, external boundaries, lifecycle/concurrency behavior, and
outputs. Preserve surprising behavior unless a separately approved behavior
change says otherwise.

Write a compact behavioral contract for the affected boundary. Include inputs
and outputs; errors, codes, and messages that callers may observe; side effects
and ordering; persistence or schema shape; lifecycle and concurrency
guarantees; and performance only when performance is part of the claim.

### 2. Map the exact blast radius

Inventory the references that can make a structural change observable:

- direct and indirect callers, imports, exports, overrides, subclasses,
  factories, registrations, and dependency-injection wiring;
- production and test references, fixtures, snapshots, examples, and docs;
- configuration, generated files, templates, reflection, tags, serialization,
  CLI names, database queries, wire/API contracts, and deployment order when
  relevant.

Distinguish static references from dynamic or external references. Record what
was searched, what was found, and what remains uncertain. A normal reference
search is not proof that a dynamic boundary is safe.

If the boundary is under-tested, establish a characterization baseline before
structural edits. Cover representative success, failure, error paths, and
observable side effects in proportion to risk. Such tests capture current
behavior, including quirks; they do not silently turn a refactor into a bug
fix.

### 3. Design around dependency control

Use these four tests together. Record the current and proposed edges and the
evidence for the decision.

1. **High cohesion, low coupling, and locality.** Keep responsibilities that
   change together for a real reason together, and reduce propagation across
   boundaries. Feature grouping is a useful option, not a universal rule:
   domain, technical, boundary, or lifecycle ownership may be clearer.
2. **Explicit layered dependency direction.** Name the permitted layer or
   package directions. Keep policy independent of replaceable details when the
   project has that boundary, and keep adapters at the edge. If a reverse edge
   is required, make it explicit through a narrow port or composition boundary.
   Do not introduce Clean, Hexagonal, Onion, or other layered schemes without a
   concrete dependency or change-isolation benefit.
3. **Acyclic Dependencies Principle.** Compare the before and after module
   graph and classify runtime/package edges separately from test, build, or
   support edges. Treat an in-scope runtime/package cycle as a defect to
   investigate and break at the smallest meaningful ownership boundary. If
   repository evidence shows an intentional cycle or a non-runtime support
   edge must remain, record the reason and its containment. Do not hide cycles
   in a generic shared package or speculative indirection.
4. **Information hiding.** Keep implementation details private and each
   boundary's public surface small and stable. Expose a contract when it hides
   a volatile implementation behind a stable semantic boundary or has a real
   consumer, variation, compatibility, migration, or test-seam need. Check
   callers before narrowing, renaming, deleting, or bridging a public symbol.

Do not optimize for metrics or architectural vocabulary alone. The plan should
state the intended locality improvement, allowed dependency directions, cycles
removed or retained, and public-surface changes.

### 4. Plan and obtain approval

Choose the smallest structural change that addresses the named problem. For
non-trivial, cross-module, public-surface, deletion, under-tested, or otherwise
high-risk work, write an on-disk plan using the repository's planning workflow
when one exists. It must include:

- target, benefit, non-goals, affected boundaries, and compatibility decisions;
- dependency-ordered slices that can be checked independently;
- entry and exit checks, baseline/contract evidence, and recovery or rollback
  notes;
- validation commands discovered from the repository and known gaps.

Use a diagram only when topology, ownership, or data flow is broad enough that
it materially improves review. When this plan gate applies, do not begin
implementation until the human approves the plan. Approval does not authorize
unrelated bug fixes, feature work, migrations, commits, pushes, or deployment.

### 5. Execute small verified slices

Start from a known, recoverable baseline. For each approved slice:

1. Make one coherent structural move, preferably with mechanical or
   tool-supported moves and renames.
2. Update production code, composition wiring, tests, docs, configuration, and
   dynamic references together when the move requires it.
3. Re-check change locality, allowed dependency direction, cycle status, and
   public surface. A compiling refactor can still worsen ownership or coupling.
4. Run focused checks and inspect the diff before starting the next slice.

Stop and ask for direction if an unexpected behavior, failure, reference,
file, public-surface change, deletion, compatibility concern, or missing
contract evidence appears. Also stop when the work would exceed the approved
target or require an unplanned behavior change. Update the plan before
continuing; do not improvise around the stop condition.

Do not delete old files, compatibility paths, generated artifacts, or public
symbols until callers, dynamic references, deployment/rollback order, history,
and the compatibility decision have been checked. Add comments or README
material only for non-obvious invariants, ordering, side effects, external
contracts, or safety constraints.

### 6. Validate in proportion to risk

Use a focused-to-broad ladder, discovering commands from the repository:

1. focused tests and checks for the changed boundary after each slice;
2. affected package/module checks and characterization tests;
3. repository-wide tests, type checks, linters, builds, smoke tests, or
   benchmarks when exposed by the project and justified by the blast radius.

For dependency claims, compare a before/after graph or repository-native
report, check for new cycles, inspect cross-boundary imports/references, and
review the exported surface. Report structural evidence, not a promise that
future changes can never spread. Preserve error, retry, transaction, cleanup,
lifecycle, and concurrency semantics.

If a check cannot run, report the exact command, failure, and risk as a gap.
Do not claim full validation from partial evidence. Run `git diff --check` when
Git is available.

## Final report

Report:

- the named problem, expected benefit, and before/after ownership and runtime
  flow;
- changed, renamed, removed, or retained paths and compatibility decisions;
- behavioral contract or characterization evidence;
- dependency directions, cycle checks, public-surface findings, and locality
  evidence;
- validation commands and results, exact gaps, unresolved risks, and follow-up;
- a concise suggested commit message. Do not commit automatically.
