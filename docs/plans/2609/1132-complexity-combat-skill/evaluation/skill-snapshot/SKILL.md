---
name: complexity-combat
description: Scan for over-engineered code and ask human which problems are real.
version: 1.0.0
tags:
  - refactoring
  - simplification
  - code-quality
---

# Complexity Combat

Scan a codebase for over-engineered code. For each candidate, identify what problem the code is trying to solve, then ask the human: "Is this a real problem that needs solving?"

## When to Use

- Code feels harder than it needs to be
- More infrastructure than business logic
- Asked to simplify or reduce complexity

## When NOT to Use

- Complexity matches the problem domain
- Performance-critical code justified by benchmarks
- Stable code that is rarely touched

## Scan For

Look for these patterns:

- **Unnecessary abstraction** — interface/abstract class with one implementation, factory that always returns the same type, wrapper that adds no behavior
- **Premature generalization** — generic code for hypothetical futures, config options never changed from defaults, plugin points with no plugins
- **Excessive indirection** — function that just calls another function, middleware that does trivial work, event bus for a single synchronous consumer
- **Over-engineered error handling** — catching exceptions that cannot be thrown, defensive null checks on guaranteed non-null values, re-checking invariants the type system already enforces
- **Unnecessary state** — caching cheap computations, state machine for a linear sequence, shared mutable state that could be local immutable

## Workflow

### 1. Scan and Present

Walk the target directory. For each candidate, figure out what problem the code is trying to solve — not just what pattern it uses, but the actual concern it addresses (e.g. "allow swapping database backends", "handle future multi-tenant support", "protect against null from external API").

Record for each candidate:

- File path and line range
- What problem it is trying to solve (one sentence)
- Why it is over-engineered for that problem (one sentence)
- Estimated impact: low / medium / high

Present as a table, then detail each candidate.

### 2. Reality Check (Human Gate)

**Ask the human about each candidate, one by one:**

> **Candidate N: [name]**
> This code addresses: "[the problem it is trying to solve]"
>
> Is this a real problem for your project?
> - **Yes** — keep the code
> - **No** — simplify or remove it
> - **Maybe, but overblown** — simplify with care

Wait for each response before moving to the next. Do not batch. If the human says the problem is real, accept it and move on.

## Decision Rules

- If the human says a problem is not real but you think it is, push back — explain why the concern is legitimate, what could go wrong, or what scenario makes it real. Let them convince you otherwise.
- If the human confirms after pushback, accept and move on.
- Record kept candidates with the human's reasoning.
- When in doubt, ask.
