---
name: vectorize
description: Use when implementing or refactoring batched data transformations and a vectorized or DataFrame approach may improve clarity or performance, especially in Python projects using Polars or Dataframely.
---

# Vectorize

Prefer column-oriented transformations when the data is naturally tabular. The main benefit may be clearer code as well as less per-row Python work; do not vectorize code when it makes the flow harder to understand.

## Workflow

1. Trace the full data path from input through transformation to output and side effects. Identify row ordering, null behavior, duplicate-key assumptions, cursor or state updates, and the boundary where another system consumes the result.
2. Decide whether tabular or array operations fit the whole transformation. Prefer the project's existing dataframe or numerical library. In Python projects that already use Polars, keep data in Polars through filters, joins, grouping, derived columns, and state-frame updates where those operations are naturally column-based.
3. Convert between representations at clear boundaries. Avoid repeated `iter_rows()`, `to_dicts()`, or per-row `apply`/`map_elements` for logic that can be expressed with dataframe operations. A small loop can remain clearer for inherently sequential work, external side effects, or tiny scalar inputs.
4. Use the project's dataframe schema library at meaningful frame boundaries when it adds useful guarantees. In projects using Dataframely, define feature-local schemas for required columns, dtypes, nullability, and keys; validate input frames rather than silently filtering malformed rows. Keep external API or RPC contracts in their existing contract layer, and avoid maintaining duplicate schemas without a clear reason.
5. Preserve behavior while changing representation. In particular, check null versus missing rows, NaN and infinity handling, timestamp zones, duplicate keys, ordering, and when state is advanced relative to writes or other side effects. Do not let a cast or schema validator silently change accepted inputs.
6. Compare the resulting flow end to end. Keep vectorized stages together when that improves readability, but leave orchestration and side effects explicit. Explain any remaining row-wise step and why it is inherently sequential or clearer that way.

## Review checklist

- Is the transformation naturally column-oriented, or is vectorization being forced?
- Does the full pipeline stay in the dataframe or array representation until a real boundary?
- Are schema checks at input boundaries clear about invalid rows and casts?
- Are ordering, nulls, duplicate keys, and state-update timing preserved?
- Are conversions to Python objects limited to a boundary such as serialization?
- Is the result easier to read, not just different?

Follow the repository's own library choices, typing, and validation instructions. Do not introduce Polars or Dataframely into a project that does not need them.
