---
name: python-interactive
description: >-
  Use whenever a user wants to prepare or edit a Python .py file for
  interactive execution in VS Code's Python Interactive window, including
  # %% cells, indented body markers, runtime sys.path setup, interactive setup
  functions (_setup_interactive()), parameter preparation, exploratory plotting,
  or running interactive files via autonomous coding agents.
  Apply this skill even when they describe the workflow as running Python interactively.
---

# Python Interactive in VS Code

Use this skill for Python source files that support both normal module execution
and interactive exploration in VS Code's Python Interactive window. Keep the
module valid Python syntax at all times.

## 1. Runtime Import Roots on `sys.path`

At the very top of files intended for interactive execution, use the standard
workspace path resolution block. This ensures imports resolve when running cells
directly in the Interactive Window without depending on working directory:

```python
# %%
from pathlib import Path
import sys

WORKSPACE_ROOT = Path("/Users/kaestrl/projects/equity")
PROJECT_ROOT = WORKSPACE_ROOT / "<service_dir>"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
```

Follow this immediately with standard imports in the next cell:

```python
# %%
from datetime import date, time
from zoneinfo import ZoneInfo
import polars as pl
...
```

## 2. The `_setup_interactive()` Gateway

Encapsulate environment loading, external connections (such as NATS or databases),
and representative default parameter variables in a standard private function named
`_setup_interactive()`:

- Standard name: `_setup_interactive()` (asynchronous if using async clients like NATS).
- Inside the function, place an indented `# %%` marker before the runnable body statements.
- Tag with `# pragma: no cover` if test coverage reports require it.
- **Representative Parameters & Fixtures**: Define sample parameters (e.g. `user`, `date`, `symbols`, test data paths) directly inside `_setup_interactive()` so executing its body populates kernel variables ready for function-body stepping without polluting global module scope during normal imports.

```python
# %%
async def _setup_interactive() -> None:  # pragma: no cover
    # %%
    common_config.load_environment_files()
    import equity_shared.nats.client as nats_client

    nats_client_ = await nats_client.connect_nats()

    # Representative default parameters for stepping through worker functions
    user = "total"
    period = "annually"
    min_date = date(2025, 1, 1)
    max_date = date(2025, 12, 31)
```

When stepping through code in the Interactive Window, developers execute the body
of `_setup_interactive()` to initialize both the runtime connections and the
parameter variables in the active kernel session.

## 3. Function Structure & Return Isolation (Indented Markers)

`return` statements are only valid inside a function definition. Running a selection
that contains a `return` keyword at the top-level kernel triggers:
`SyntaxError: 'return' outside function`.

### Preferred Pattern: Single Final Return

Prefer structuring functions with **one final `return` statement** at the very end.
Assign intermediate calculations or branch outputs to a result variable. This allows
formatting with the standard **3-boundary pattern**:

1. **Top-level cell marker** before the `def` header: `# %%`
2. **Indented cell marker** immediately after the docstring (or header if no docstring): `    # %%`
3. **Indented cell marker** immediately before the final `return` statement: `    # %%`

```python
# %%
async def get_current_balance_df(
    nats_client_: nats_client.NATSClient,
    user: str,
    *,
    cashflow_nav_cutoff_time: time,
    market_timezone: ZoneInfo,
) -> pl.DataFrame:
    """Calculate the user's current balance combining investment and NAV."""
    # %%
    investment_df = await _get_current_investment(nats_client_)
    nav_df = await _get_current_nav(
        nats_client_,
        cashflow_nav_cutoff_time=cashflow_nav_cutoff_time,
        market_timezone=market_timezone,
    )

    balance_df = investment_df.join(nav_df, on="user", how="inner").filter(
        (pl.col("user") == user)
    )

    # %%
    return balance_df
```

Developers can highlight and run everything between the two indented `# %%` markers
via **Shift+Enter** safely, as no `return` keyword is included in the runnable block.

### Multiple or Early Returns: Isolation Rules

When a function cannot reasonably be refactored to a single final return (e.g. guard
clauses, early exit optimizations, or complex branching), isolate the return
statements using indented `# %%` markers:

1. **Separate Guard Returns from Main Body**:
   Place an indented `# %%` after early guard exits so the downstream computational body
   can still be executed independently:

   ```python
   # %%
   def calculate_metrics(df: pl.DataFrame | None) -> dict[str, float]:
       """Calculate summary metrics for the given DataFrame."""
       if df is None or df.is_empty():
           return {}
       # %%
       total_count = df.height
       mean_value = float(df["value"].mean())
       summary = {"count": total_count, "mean": mean_value}
       # %%
       return summary
   ```

2. **Branch Returns**:
   If branches each contain their own `return`, place indented `# %%` markers around
   the return statements or isolate each branch suite. When stepping through a branch,
   assign the expression to a variable or execute only the assignment/computation line:

   ```python
   # %%
   def evaluate_condition(score: float) -> str:
       """Classify performance tier based on score."""
       # %%
       if score >= 90.0:
           result = "Tier 1"
           # %%
           return result
       # %%
       result = "Standard"
       # %%
       return result
   ```

### Why Indented Markers?

- **Clean Isolation**: Indented `# %%` markers divide the code into runnable computation lines versus non-runnable boundaries (`def` header and `return`).
- **Interactive Execution**: In VS Code, selecting statements between indented `# %%` markers and running them via **Shift+Enter** (Run Selection in Interactive Window/Terminal) works seamlessly.
- **Syntactic Validity**: Python treats `# %%` purely as a comment regardless of indentation level; formatting and linting tools (`ruff`, `flake8`) remain completely valid.

## 4. Exploratory and Diagnostic Functions (`_plot_*`, `_analyze_*`)

In addition to core business logic, modules frequently include private exploratory
or visualization functions designed for ad-hoc inspection and debugging:

- Name them with an explanatory private prefix, e.g. `_plot_journal_index()`, `_create_split_investment_sankey()`, `_analyze_card_expense()`.
- Add `# pragma: no cover` on exploratory functions that do not participate in automated unit tests.
- Keep visualization imports (e.g. `import plotly.express as px`, `import matplotlib.pyplot as plt`) scoped inside the exploratory function if they are only needed during interactive analysis.
- Use interactive display calls like `fig.show()` or detailed table prints.

```python
# %%
async def _plot_journal_index() -> None:  # pragma: no cover
    """Plot the journal index over time for visual inspection."""
    # %%
    import plotly.express as px

    nats_client_ = await nats_client.connect_nats()
    journal_df = await repo.read_journal_index(nats_client_)

    fig = px.line(
        journal_df,
        x="date",
        y="journal_index",
        title="Journal Index Over Time",
    )
    fig.show()
```

## 5. Coding Agent Execution Patterns

While human developers interact via VS Code's GUI (CodeLens "Run Cell", Shift+Enter,
persistent kernel), autonomous coding agents operate in headless terminal shells.
Use these two complementary patterns to allow agents to execute and verify interactive files:

### Pattern A: Self-Executable `__main__` Entrypoint

Add a standard entrypoint block at the bottom of the interactive file:

```python
# %%
if __name__ == "__main__":
    import asyncio

    asyncio.run(_setup_interactive())
```

**How agents use this:**
- An agent can execute `python path/to/module.py` directly in the shell.
- Verifies that imports, `sys.path`, configuration loading, environment files, and service connections succeed without throwing errors.
- Does not affect the module when imported by other services or pytest.

### Pattern B: Ephemeral Scratch Verification Script

When an agent needs to test or verify a specific worker function after making code modifications:

1. The agent writes an ephemeral scratch script in its scratch directory (e.g. `<scratch>/test_worker.py`).
2. The scratch script imports the target module, runs `_setup_interactive()`, calls the function with realistic parameters, and prints results.

```python
# Example scratch script generated by agent
import asyncio
from app.feature.journal.user import balance_worker

async def main():
    nats_client_ = await balance_worker._setup_interactive()
    # Test target function
    df = await balance_worker.get_current_balance_df(
        nats_client_,
        user="total",
        cashflow_nav_cutoff_time=...,
        market_timezone=...,
    )
    print(df)

asyncio.run(main())
```

This provides reliable verification without modifying production code or relying on a GUI window.

## Summary Checklist

- [ ] Path resolution block at top of file with `WORKSPACE_ROOT` / `PROJECT_ROOT` inserting into `sys.path`.
- [ ] Setup gateway named `_setup_interactive()` handling config loading, connections, and representative default parameters.
- [ ] Single final `return` preferred, with indented `# %%` markers placed immediately after docstring and before `return`.
- [ ] If early/multiple returns exist, isolate `return` statements or guard exits with indented `# %%` boundaries.
- [ ] Exploratory visualization or diagnostic helpers named `_plot_*` or `_analyze_*` with `# pragma: no cover`.
- [ ] Headless `if __name__ == "__main__":` entrypoint at bottom calling `_setup_interactive()` for terminal/agent execution.
