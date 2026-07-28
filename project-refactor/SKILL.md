---
name: project-refactor
description: Refactor an existing project or feature into a clearer, safer end state without changing intended behavior. Use when code is hard to navigate, runtime flow is convoluted, names no longer explain ownership, modules need reorganizing, or a broad cleanup requires an approved plan and full validation.
---

# Refactor Project

## Goal

Make the code easier to follow without flattening safety boundaries that exist
for a real runtime reason.

## Workflow

1. Trace the real path from entrypoint to side effect. Include composition,
   routes or workers, orchestration, state guards, adapters, and audit/output.
2. Explain that path in plain language before proposing structural changes.
3. Separate required complexity from accidental complexity. Keep a boundary when
   it protects concurrency, stale state, external side effects, or ownership.
   Remove wrappers, policies, and branches that add no distinct behavior.
4. Organize by feature responsibility, not technical layers. Keep a feature's
   route, flow, model, persistence, and local helpers together when they serve
   that feature. Create shared infrastructure only after two current features
   genuinely depend on it; do not create generic `services/`, `utils/`, or
   `handlers/` buckets merely because code looks similar.
5. Choose caller-facing names. A reader should be able to identify each
   collaborator's role from its class, parameter, and local-variable names.
6. For a non-trivial change, write a reviewable plan and obtain approval before
   implementation. Do not leave compatibility aliases or empty old modules
   unless compatibility is explicitly required.
7. Apply the refactor consistently: production code, composition wiring, tests,
   docs, and mock names must use the new vocabulary.
8. Add short comments where ordering or a safety rule is not obvious. Explain
   why the step exists, not the syntax.
9. Run focused tests first, then the project's full tests, formatter/linter,
   type checker, and diff check. Record review findings and validation gaps.

## Decision checks

- Is there one obvious public entrypoint for each workflow?
- Can a new reader follow the normal path top-to-bottom without guessing?
- Does each feature own its feature-specific code, rather than scattering it
  across technical-layer folders?
- Does every abstraction have a distinct behavior or safety responsibility?
- Are variable and parameter names as clear as their types?
- Did the refactor remove obsolete code instead of hiding it behind a bridge?
- Do tests mirror the ownership and verify preserved safety behavior?

## Completion report

State the new shape, removed indirection, renamed concepts, documentation and
test changes, validation results, and any remaining risk. Suggest a concise
refactor commit message; do not stage or commit changes.
