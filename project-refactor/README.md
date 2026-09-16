# Project Refactor

This skill guides project-level structural refactoring that preserves
observable behavior. Read [`SKILL.md`](SKILL.md) for the workflow; this file is
only a short orientation.

Its organizing lens is dependency control:

- keep related change together and unnecessary coupling low;
- make layered dependency direction explicit without imposing a universal architecture;
- check the module graph before and after for cycles; and
- hide implementation details behind small, stable interfaces.

The workflow maps the runtime contract and exact blast radius, adds a
characterization baseline when evidence is weak, obtains human approval for
non-trivial work, executes small verified slices, and reports validation gaps
honestly. It treats feature folders, class-to-function changes, deletions,
diagrams, comments, and full-suite checks as evidence-based choices.

For narrower work, use `module-refactor` for a bounded module, file, or package;
`long-file-refactor` for one long mixed file; and `complexity-combat` for an
open-ended complexity scan and human disposition.
