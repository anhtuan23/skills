# Plan: Create advanced Git reconciliation skill

## TLDR

Create a portable `git-reconcile` skill for merge and rebase
conflicts. It will preserve Hermes Agent's intent-reconciliation model, add
real Git state and recovery safeguards, and teach agents to port behavior into
the surviving architecture when a refactor makes a branch's original diff
stale. The skill will be concise in `SKILL.md` and use four focused reference
files for merge, rebase, reconciliation, and recovery details.

## Goal and scope

- Add a reusable, general Agent Skills-compatible skill under
  `git-reconcile/`.
- Cover merge, rebase, repeated rebase conflicts, interactive rebase,
  `--onto`, `--rebase-merges`, rerere, range-diff, and recovery.
- Require base/history/intent reconstruction before non-trivial resolutions.
- Fail closed when intent, authorization, repository state, or verification is
  insufficient.
- Permit the smallest additional implementation needed to preserve an intent
  after refactoring or path/API movement, while prohibiting unrelated cleanup.
- Preserve attribution to Nous Research Hermes Agent without copying its skill
  verbatim or retaining Hermes-only commands.
- Update the root skill catalog after the skill is complete.

Out of scope: implementing Git automation scripts, changing Git configuration,
performing a real repository merge/rebase, pushing branches, or adding
client-specific UI metadata that would reduce portability across agents.

## Design

The entrypoint will contain discovery boundaries, the safety gate, the shared
workflow, classification names, reference routing, and the required report.
References will hold the command-level details so the entrypoint stays easy to
load.

The classifications will be:

- `disjoint-intent`: compatible requirements; preserve both.
- `same-question-different-answer`: incompatible answers; choose from evidence
  or escalate, never blend by reflex.
- `superseded`: one premise no longer applies; preserve surviving behavior and
  port any still-valid intent.
- `structural-port`: an intent survives, but its original patch must be
  reimplemented in the other side's refactored architecture.
- `unsafe-or-unresolved`: binary/generated/schema/deployment or ambiguous
  cases requiring regeneration, domain review, or explicit human direction.

## Ordered slices

1. **Research and design** — complete. Inspect Hermes, local skill conventions,
   Agent Skills/Codex layout, Git's merge/rebase documentation, and comparable
   conflict workflows.
2. **Write the skill** — create `SKILL.md` and the four routed references:
   `conflict-reconciliation.md`, `merge.md`, `rebase.md`, and `recovery.md`.
3. **Integrate and validate** — add the catalog row, run the skill validator,
   check frontmatter/reference links, inspect for duplication and unsafe
   instructions, and verify the worktree diff.
4. **Independent final review** — review the completed skill as if it could
   operate on a valuable repository; record findings in this plan folder,
   address material findings, and update progress.

## Validation criteria

- The skill directory has valid lowercase naming and required frontmatter.
- `SKILL.md` is concise, routes every reference, and contains no scaffold
  placeholders or client-specific assumptions.
- The references cover all requested Git modes and conflict shapes without
  duplicating the same rule unnecessarily.
- The instructions distinguish merge `ours`/`theirs` from rebase labels and
  never use those labels as semantic authority.
- Safety rules preserve dirty work, detect existing operations, record a
  recovery point, prohibit casual destructive commands, and require explicit
  authorization for publication/history rewriting.
- Final validation requires unmerged-index checks, marker review,
  `git diff --check`, focused/full behavioral verification, and range-diff or
  equivalent history comparison after rewriting.
- The final diff contains only the planned skill, catalog, and plan/review
  artifacts.

## Risks and open questions

- The skill cannot infer product intent that is absent from repository evidence;
  it must report an ambiguity rather than invent one.
- Tests may pass while semantics are wrong, so the report must connect
  invariants to evidence rather than treating green tests as proof by
  themselves.
- Git metadata and command behavior vary across versions; references will use
  stable porcelain commands and explain when a command is only diagnostic.
- A general skill cannot safely authorize a push or shared-history rewrite;
  those remain explicit user decisions.

## Approval gate

Implementation starts only after human approval of this plan. After approval,
the coordinator will create the skill, run validation, obtain an independent
review, address material findings, and return the files plus limitations for
final human review. The approved skill name is `git-reconcile`.
