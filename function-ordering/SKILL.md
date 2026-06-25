---
name: function-ordering
description: Reorder modules so caller-facing functions come first, helper functions follow in execution order, and the public surface is kept as narrow as possible.
---

# Function Ordering

Use this skill when cleaning up a module's function layout, especially after a
refactor or migration where helpers and exported functions have drifted into a
hard-to-read order.

## Rules

- Put the main caller-facing function or public entrypoint first.
- Put helpers after the functions that call them, in execution order.
- Keep low-level utility helpers near the bottom.
- Keep constants and shared types above functions when the whole file uses them.
- Keep the public surface as small as possible.

## Surface Checks

Before reordering, check which functions are actually used outside the module.
If a function is only used inside the same module or package, make it private
unless there is a clear API reason to keep it public.

Practical defaults:

- Go: unexport helpers unless another package imports them.
- Python: use a leading underscore for internal helpers.
- Tests in the same package or module may still exercise private helpers when
  that keeps the production API smaller.

## Editing Pattern

1. Find external call sites first.
2. Shrink the public surface.
3. Reorder functions so readers can follow the file top to bottom.
4. Update tests for renamed private helpers if needed.
5. Run focused formatting and tests for the touched module.

## What Good Looks Like

A reader should be able to open the file, see the main entrypoint near the top,
and follow the control flow downward without jumping back and forth across the
module.
