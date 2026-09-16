---
name: complexity-combat
description: Scan for accidental or over-engineered code, distinguish justified complexity from needless complexity, and ask a human which candidates are real. Use when code feels harder than necessary, abstraction or indirection is growing, or a user asks to simplify code; defer to a specific refactoring, review, testing, or safety workflow when one is already required.
version: 1.1.0
tags:
  - refactoring
  - simplification
  - code-quality
---

# Complexity Combat

Find evidence-backed accidental complexity without treating justified domain,
safety, boundary, reliability, concurrency, or performance complexity as a
defect. Report candidates and obtain a human decision before any edit.

## When to Use

- Code feels harder than it needs to be
- More infrastructure than business logic
- Asked to simplify or reduce complexity

## When NOT to Use

- A specific refactoring, code-review, characterization-test, security, or
  migration workflow is the better owner; use it or coordinate with it.
- The request is only to measure complexity or enforce a project-specific
  metric; use the project's measurement workflow.
- The apparent complexity is already explained by a known domain contract,
  external boundary, reliability property, concurrency rule, lifecycle, or
  measured hot path. Do not label it accidental without contrary evidence.

## Boundary

Scanning, tracing, and reporting never authorize edits. Do not change
production code, tests, configuration, or documentation during this workflow.
If the human chooses **simplify**, stop at a separately approved scope and
validation plan; implementation is a later task that must preserve observed
behavior, including important error paths and compatibility quirks.

## Scan For

Look for these patterns:

- **Unnecessary abstraction** — interface/abstract class with one implementation, factory that always returns the same type, wrapper that adds no behavior
- **Premature generalization** — generic code for hypothetical futures, config options never changed from defaults, plugin points with no plugins
- **Excessive indirection** — function that just calls another function, middleware that does trivial work, event bus for a single synchronous consumer
- **Over-engineered error handling** — catching exceptions that cannot be thrown, defensive null checks on guaranteed non-null values, re-checking invariants the type system already enforces
- **Unnecessary state** — caching cheap computations, state machine for a linear sequence, shared mutable state that could be local immutable

Treat these as leads, not proof. Do not optimize for line count, remove an
abstraction merely because it has one implementation, or use cyclomatic or
cognitive-complexity thresholds as universal refactoring rules.

## Workflow

### 1. Establish scope and evidence

Name a bounded target directory, module, or symbol and its intended behavior.
If the request is unbounded, ask the human to narrow it or approve a small
representative slice; do not sweep an entire repository by default. Inspect the
repository's conventions and relevant history/configuration before judging a
pattern. Trace callers, data flow, dependencies, tests, interfaces, and
external boundaries as risk requires. Record observed facts separately from
inferences. For higher-risk candidates, first establish a baseline or
characterization of success, failure, and compatibility behavior.

Check both sides of the case:

- **Intentional complexity:** public or stable contracts, dependency-injection
  or test seams, external/untrusted data, transactions, retries, concurrency,
  lifecycle/state transitions, platform compatibility, security boundaries,
  or a measured performance need.
- **Accidental-complexity signals:** no active caller or variation, duplicated
  paths, indirection that adds no policy, configuration that cannot vary,
  defensive work contradicted by the contract, or cost without a demonstrated
  benefit.

Metrics and code shape are evidence only. State uncertainty when the purpose,
cost, or contract cannot be established.

### 2. Present a concrete candidate report

Walk the named target and report candidates, not edits. Start with a compact
table, then detail candidates in priority order. Use this record for every
candidate:

| Field | Record |
|---|---|
| Location | File, symbol, and line range |
| Observed behavior | What the code actually does, with callers/tests or other evidence |
| Intended purpose | The problem or contract it appears to address |
| Complexity and cost | The indirection, state, cognitive, operational, or performance cost |
| Counter-evidence | Why it may be intentional, including missing evidence and risk |
| Confidence and impact | Confidence in the diagnosis; low/medium/high impact |
| Smallest safe option | The narrowest possible simplification, or why none is known |
| Recommendation | Keep, simplify, defer, or escalate, with a reopen/validation trigger |

Do not call a candidate accidental until the report explains both the observed
cost and why the counter-evidence does not justify it.

### 3. Reality check: one candidate at a time

Ask about exactly one candidate at a time; do not batch decisions:

> **Candidate N: [name]**
> Observed evidence: "[behavior and evidence]"
>
> It appears to address: "[purpose or contract]"
>
> Cost and counter-evidence: "[why it may be accidental, and what remains uncertain]"
>
> Which decision applies?
> - **Keep** — the complexity protects a real need; record the rationale.
> - **Simplify** — approve a narrow follow-up scope before any edit.
> - **Defer** — record the owner, missing evidence, and concrete reopen trigger.
> - **Escalate** — route to the relevant domain owner or specialist workflow.

Wait for the decision before moving to the next candidate. If the human's
answer conflicts with the evidence, explain the specific risk or missing fact
and ask whether to keep, simplify, defer, or escalate; do not silently decide
for them.

## Decision Rules

- **Keep:** record the human's rationale and leave the code unchanged.
- **Simplify:** record the approved candidate and constraints, then end this
  workflow. A later implementation must have separately approved scope and
  behavior-preserving validation.
- **Defer:** record what evidence is missing and a concrete event or condition
  that should reopen the candidate; do not silently discard it.
- **Escalate:** identify the owner or narrower workflow and preserve the report
  for handoff.
- When evidence is insufficient or risk is high, prefer defer or escalate over
  a confident simplification.

## Completion report

After the workflow ends, summarize every candidate considered so far, its
disposition, the human's rationale, deferred evidence and reopen triggers,
escalations, and any approved follow-up scope. If the workflow stopped before
later candidates were considered, mark them unreviewed rather than inferring a
decision. If no candidate survives the evidence check, say so and explain what
was inspected.
