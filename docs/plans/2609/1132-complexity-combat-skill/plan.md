# Plan: Improve complexity-combat skill

## TLDR

Improve `complexity-combat/SKILL.md` so it finds evidence-backed accidental
complexity without mistaking justified domain, safety, boundary, or performance
complexity for a defect. Preserve its portable scan-and-human-gate purpose;
do not turn it into an autonomous refactoring workflow.

## Goal and scope

- Keep the skill name and directory unchanged.
- Sharpen the trigger description and clarify when the skill should defer to a
  more specific refactoring, review, or safety-net workflow.
- Require a named target and repository-context discovery before judging a
  pattern.
- Add an evidence record for each candidate: location, observed behavior,
  callers, purpose, cost, counter-evidence, confidence, and smallest safe
  option.
- Distinguish accidental complexity from complexity that protects a real
  contract, boundary, reliability property, concurrency rule, or measured
  performance need.
- Keep the one-candidate-at-a-time human gate, but make its decisions
  explicit: keep, simplify, defer, or escalate.
- State that scanning and reporting do not authorize edits; implementation
  requires a separately approved scope and behavior-preserving validation.

Out of scope: changing other skills, adding language-specific analyzers,
automatically editing production code, or prescribing numeric complexity
thresholds as universal refactoring rules.

## Research findings

Comparable public skills consistently add safeguards missing from the current
71-line draft:

- `addyosmani/agent-skills` makes exact behavior preservation, local project
  conventions, Chesterton's Fence, incremental changes, and scope control
  explicit.
- `smallnest/goal-workflow` records callers, dependencies, a baseline, and
  counter-pressures against false abstractions before choosing a refactoring;
  it also treats metrics as evidence rather than a substitute for judgment.
- `wilddoc/claude-code-skills-pack` uses characterization tests to capture the
  existing contract, including quirks and error paths, before changing
  under-tested code.
- `testdouble/han` requires a named target, an evidence/YAGNI gate, and a
  reopen trigger for deferred findings instead of silently applying or
  discarding uncertain cleanups.
- `armanzeroeight/fastagent-plugins` provides a useful report shape for
  cyclomatic/cognitive complexity, but its thresholds should remain optional
  signals in a general skill.

## Ordered slices

1. **Research and design** — complete. Inspect the current skill, sibling
   conventions, repository plan format, and comparable public skills.
2. **Revise the entrypoint** — update only `complexity-combat/SKILL.md`, keeping
   it concise and portable.
3. **Validate the skill** — check frontmatter, line count, internal structure,
   `git diff --check`, and three realistic behavior-oriented evaluation prompts
   against the old and revised versions when the evaluation harness is
   available.
4. **Independent review** — review the completed skill for false positives,
   unsafe simplification advice, trigger drift, and unnecessary verbosity;
   write findings here, address material issues, update progress, and return
   the result for final human review.

## Validation criteria

- The frontmatter remains valid and the skill stays below the recommended
  500-line body limit.
- The skill requires evidence before labeling a pattern accidental.
- The report distinguishes observed facts, inferred purpose, risk, and
  recommendation.
- It names common counterexamples: public contracts, dependency inversion,
  test seams, external/untrusted data, transactions, concurrency, lifecycle,
  platform compatibility, and measured hot paths.
- It does not optimize for line count or treat cyclomatic/cognitive thresholds
  as proof that code should change.
- It keeps the human gate one candidate at a time and does not silently edit
  after a scan.
- It defines what happens after keep/simplify/defer/escalate decisions and
  preserves a behavior-validation boundary for any later implementation.
- The final diff contains only approved skill and plan/review artifacts.

## Risks and open questions

- More evidence requirements can make a small scan feel heavy; keep the
  entrypoint short and require deeper tracing only for higher-risk candidates.
- A general skill cannot know whether a boundary or optimization is necessary;
  it must report uncertainty and a concrete reopen trigger.
- Numeric complexity tools differ by language and configuration; use them only
  when available in the project and report their provenance.

## Approval gate

Implementation starts only after human approval of this plan. After approval,
the coordinator will revise the skill, run the planned validation, complete an
independent review, address material findings, and return the skill for final
human review.
