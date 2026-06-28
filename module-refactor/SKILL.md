---
name: module-refactor
description: Refactor an existing code area into a cleaner, easier-to-navigate structure without drifting behavior. Use this when reorganizing files, splitting long modules, adding beginner-friendly documentation, narrowing public surface, removing stale helpers, and updating tests to match the new ownership boundaries.
---

# Module Refactor

Use this skill when the task is to clean up or reorganize existing code rather
than add a new feature.

Typical triggers:

- "refactor this"
- "clean this up"
- "split this file"
- "reorganize this package"
- "make this easier to navigate"
- "remove dead code after migration"

## Goal

Leave the touched area in a simpler end state that is easier to navigate,
easier to follow, and easier for a beginner to read, while preserving the
intended behavior.

## Refactor Rules

- Read the surrounding code first. Match existing local patterns unless the
  task is explicitly migrating away from them.
- Organize by feature responsibility, not generic utility buckets.
- Split long files when they mix multiple responsibilities or are hard to scan.
- Keep project-specific helpers local to the owning feature unless at least two
  real consumers need them.
- Prefer a clean end state over compatibility shims unless compatibility is an
  explicit requirement.
- Remove stale code, bridge code, and dead exports in the touched area instead
  of leaving half-migrated structure behind.
- Keep the public surface as narrow as possible.
- Put caller-facing functions first and helpers later in execution order.
- Add beginner-friendly documentation and comments to all touched functions so
  a new reader can understand purpose, sequence, and important side effects.
- Add or update a local `README.md` when the feature has enough moving parts
  that a short overview improves navigation.

## Workflow

1. Map the current structure.
   - Identify entrypoints, helpers, tests, and external imports.
   - Find which files actually own the behavior.
2. Decide the target shape before editing.
   - Choose folders and file boundaries by responsibility.
   - Decide whether long files should be split.
   - Decide which APIs can become private.
   - Decide which old files should disappear entirely.
3. Refactor in small coherent moves.
   - Move or split code by responsibility.
   - Rename symbols to make ownership and intent clearer.
   - Remove dead helpers, stale adapters, and unused constants while the area is
     open.
   - Add or refresh `README.md` when the area benefits from an overview.
   - Add beginner-friendly function comments in all touched files.
4. Refactor tests to mirror the new structure.
   - Split monolithic tests when production files were split.
   - Keep behavior coverage, but move each test near the responsibility it
     proves.
   - Update tests for newly private helpers only when that keeps the production
     API smaller.
5. Validate the touched area.
   - Run focused formatting, tests, lint, and any repo-specific checks.
   - Call out gaps when validation cannot run.

## Decision Checks

Before finalizing, check these explicitly:

- Is each file easy to name by what it owns?
- Are long files split enough that a reader can scan them quickly?
- Did any helper stay exported only because it used to be exported?
- Did the refactor remove obsolete compatibility code?
- Do tests mirror the new production layout closely enough to navigate quickly?
- Does the area have enough documentation for a beginner to follow it?
- Did function comments explain purpose and important behavior, not just restate
  the code?

## What Good Looks Like

A new reader should be able to:

1. open the feature folder,
2. identify the main entrypoint quickly,
3. use a `README.md` to understand the mental model and file layout,
4. follow the runtime flow top to bottom,
5. find the matching tests without hunting,
6. see little or no dead code left behind.

## Output Expectations

When reporting the work:

- summarize the structural changes,
- mention whether long files were split,
- mention any narrowed public surface,
- mention removed dead code,
- mention README or documentation changes,
- mention how tests were updated,
- list the validation that was run.
