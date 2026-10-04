---
name: python-interactive
description: >-
  Use whenever a user wants to prepare or edit a Python .py file for
  interactive execution in VS Code's Python Interactive window, including
  # %% cells, indented body markers, runtime sys.path setup, interactive setup
  functions (_setup_interactive()), default parameter cells, or exploratory plotting.
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

## 2. Top-Level Default Inputs Cell

To enable stepping through function bodies interactively without having to invoke
the function with arguments, define representative default parameter variables at
the module level inside a dedicated interactive cell:

```python
# %%
user = "total"
period = "annually"
min_date = date(2025, 1, 1)
max_date = date(2025, 12, 31)
```

When evaluating the function body interactively, these module-level variables
serve as the input arguments in the kernel session.

## 3. The `_setup_interactive()` Gateway

Encapsulate environment loading, external connections (such as NATS or databases),
and mock data initialization in a standard private function named `_setup_interactive()`:

- Standard name: `_setup_interactive()` (asynchronous if using async clients like NATS).
- Inside the function, place an indented `# %%` marker before the runnable body statements.
- Tag with `# pragma: no cover` if test coverage reports require it.

```python
# %%
async def _setup_interactive() -> None:  # pragma: no cover
    # %%
    common_config.load_environment_files()
    import equity_shared.nats.client as nats_client

    nats_client_ = await nats_client.connect_nats()
    return nats_client_
```

To run this in the Interactive Window or notebook interface:
```python
# %%
nats_client_ = await _setup_interactive()
```

## 4. Standard 3-Boundary Function Structure (Indented Markers)

To step through function logic easily while keeping standard Python syntax and
clean git diffs, format callable functions using the standard 3-boundary pattern
with **indented `# %%` markers**:

1. **Top-level cell marker** before the `def` header: `# %%`
2. **Indented cell marker** immediately after the docstring (or header if no docstring): `    # %%`
3. **Indented cell marker** immediately before the `return` statement: `    # %%`

### Pattern

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

### Why Indented Markers?

- **Clean Isolation**: The indented `# %%` markers cleanly divide the function into three clear regions:
  1. Function signature and documentation
  2. Executable calculation logic (which uses the kernel variables or default inputs defined in Step 2)
  3. Return statement
- **Interactive Execution**: In VS Code, developers select the statements between the indented `# %%` markers and execute them directly via **Shift+Enter** (Run Selection in Interactive Window/Terminal) or run cells directly.
- **Syntactic Validity**: Python treats `# %%` purely as a comment regardless of its indentation, so function definition and linting remain 100% compliant.
- **Return Safety**: Isolating `return` after the second indented `# %%` prevents `SyntaxError: 'return' outside function` when sending the core body lines to the interactive kernel.

## 5. Exploratory and Diagnostic Functions (`_plot_*`, `_analyze_*`)

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

    nats_client_ = await _setup_interactive()
    journal_df = await repo.read_journal_index(nats_client_)

    fig = px.line(
        journal_df,
        x="date",
        y="journal_index",
        title="Journal Index Over Time",
    )
    fig.show()
```

## Summary Checklist

- [ ] Path resolution block at top of file with `WORKSPACE_ROOT` / `PROJECT_ROOT` inserting into `sys.path`.
- [ ] Top-level `# %%` cells defining representative test parameters (`user`, `dates`, etc.).
- [ ] Setup gateway named `_setup_interactive()` handling config loading and connection management.
- [ ] Indented `# %%` markers placed immediately after function docstring and immediately before `return`.
- [ ] Exploratory visualization or diagnostic helpers named `_plot_*` or `_analyze_*` with `# pragma: no cover`.
