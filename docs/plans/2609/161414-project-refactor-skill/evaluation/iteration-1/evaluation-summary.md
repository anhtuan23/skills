# Project-refactor evaluation — iteration 1

## Method

Compared the pre-change snapshot in `../skill-snapshot/SKILL.md` with the
revised `project-refactor/SKILL.md` on five prompts. The executor runs were
read-only and were instructed not to invent repository-specific evidence or
edit files. This is a qualitative comparison; native subagent timing/token
metrics were not available, so no quantitative benchmark is claimed.

## Results

### 1. Cross-module dependency boundaries

Revised behavior:

- refused to claim a runtime map without a target repository;
- required a behavioral contract, dependency graph, callers, dynamic
  references, and characterization coverage where needed;
- used the direction `callers → reporting/application contract → implementation
  details` and stopped before implementation pending approval.

Old behavior:

- proposed a feature-folder structure and a mandatory Mermaid diagram;
- prescribed a full test suite, linters, and type checks without first defining
  repository-specific commands.

Assessment: improved evidence and dependency-boundary discipline.

### 2. Acyclic package graph

Revised behavior:

- classified `orders → billing` as a likely runtime edge and
  `billing → orders` as a shared-type/ownership edge;
- avoided automatically creating a generic `shared` package;
- proposed moving the contract to its owning boundary or inverting orchestration
  at composition, then checking the graph and public surface before/after;
- preserved behavior and stopped for approval.

Old behavior:

- extracted the type to a neutral `contracts` module by default;
- used Mermaid diagrams and unconditional broad validation.

Assessment: improved ownership reasoning and reduced speculative abstraction.

### 3. Information hiding and stable interface

Revised behavior:

- named non-goals for outputs, ordering, errors, side effects, transactions,
  and performance;
- mapped five callers and proposed a narrow reporting interface justified by
  real consumers;
- kept query builders, models, joins, and schema mappings private;
- required graph, cycle, import, export, and characterization checks.

Old behavior:

- also recognized the need for a small interface and hidden database details,
  but still prescribed feature naming, a Mermaid diagram, and full-suite checks.

Assessment: revised skill gives the boundary a stronger contract and
dependency-control rationale without requiring a generic abstraction.

### 4. Local long-file cleanup

Both versions routed a single 500-line file to `module-refactor` or
`long-file-refactor`. The result is non-discriminating, but the revised skill
does so explicitly from its routing section and no longer adds unnecessary
project-level architecture work.

### 5. Mixed behavior change and public deletion

Both versions separated the retry behavior change from public adapter deletion.
The revised response was more explicit about compatibility, external callers,
dynamic references, separate approval, and separate validation. The old
response still required a Mermaid diagram and broad checks.

## Qualitative conclusion

The revised skill better expresses the requested dependency-control principles:
it treats cohesion, coupling, direction, cycles, and information hiding as
evidence-backed design checks. It also reduces false certainty by routing
narrow work away and refusing to claim repository facts without inspection.
The local-file routing case should remain a regression test even though it is
not strongly discriminating between versions.
