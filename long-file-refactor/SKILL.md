---
name: long-file-refactor
description: Split a long code file into smaller, domain-organized files. Covers domain type splitting, responsibility splitting, feature splitting, and test mirroring. Use when a file exceeds 300+ lines and mixes multiple concerns.
version: 1.1.0
tags:
  - refactoring
  - go
  - python
  - file-organization
  - domain-models
---

# Long File Refactor

Split a long file into smaller files organized by domain concept or responsibility.
Tests mirror the new code structure.

## When to Use

- File exceeds 300 lines and mixes multiple concerns
- 3+ distinct groups of types, functions, or responsibilities
- You scroll past unrelated code to find what you need

## When NOT to Use

- Large but single-responsibility (e.g. a linear pipeline)
- Types are tightly coupled and always change together
- Splitting would force awkward exports of private helpers

## Split Strategies

### 1. Domain Type Split

**Use when:** File holds multiple unrelated types (structs, dataclasses, schemas).

One file per type. Shared helpers in their own file.

```
model/
  quote.go          Quote struct + methods
  trade.go          Trade struct + methods
  market_index.go   MarketIndex struct + methods
  decode_json.go    shared decoder helpers
```

### 2. Responsibility Split

**Use when:** File mixes layers (I/O + logic + persistence).

Original becomes thin orchestrator. Each responsibility gets its own file.

```
worker.py           thin orchestrator
fetch.py            network I/O
normalize.py        data cleaning
merge.py            business logic
```

### 3. Feature Split

**Use when:** File handles multiple related but distinct features.

One subfolder per feature. Cross-cutting code stays at root.

```
service/
  common.py         shared types
  auction.py        auction logic
  continuous.py     continuous-session logic
```

### 4. Test Mirror Split

**Use when:** Single test file covers multiple domains.

One test file per production file. Cross-cutting tests in shared file.

```
model_test.go       cross-cutting contract tests
quote_test.go       TestQuote_Parse
trade_test.go       TestTrade_Parse
```

## Subpackage vs Same-Package

**Subpackage** (`parent/child/`): types are self-contained, clean import
boundaries desired, parent package already has many files.

**Same package**: split code is tightly integrated with parent logic, moving
would require exporting many internal helpers, parent is small.

## Workflow

1. **Map** the file. Catalog types, functions, helpers, tests, external consumers. Identify seams (domain, responsibility, feature).
2. **Design** the target layout before editing.
3. **Move** types/functions to target files. Export helpers crossing package boundaries.
4. **Update** imports in all consumers. Delete original or gut to thin orchestrator.
5. **Split** tests to mirror production code.
6. **Verify**: build, test, lint all affected packages.

## Output

Report: new file structure with line counts, deleted files, import changes,
renamed exports, test results, suggested commit message.
