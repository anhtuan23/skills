---
name: python-interactive
description: >-
  Use whenever a user wants to prepare or edit a Python .py file for
  cell-by-cell execution in VS Code's Python Interactive window, including
  # %% cells, runtime import paths, setup code, or stepping through function
  logic. Apply this skill even when they describe the workflow as running
  Python interactively rather than naming the Interactive window.
---

# Python Interactive in VS Code

Use this skill for Python source files that should support both normal module
execution and focused exploration in VS Code's Python Interactive window.
Keep the source module valid Python. Put IPython-only syntax, such as a
top-level `await`, in cells sent to the Interactive Window rather than in a
module that must also be imported or run as a normal Python file.

## Run cells

Assume VS Code's Python/Jupyter support and the project interpreter are already
configured. Check those one-time prerequisites only when cell commands are
missing, the kernel will not start, or project imports fail.

1. Save the source as a `.py` file.
2. Start with complete, runnable top-level cells. Put `# %%` at column zero on
   its own line before each cell. Use the **Run Cell** CodeLens or the
   Interactive Window command to execute cells.
3. Treat the Interactive Window as a persistent kernel: names and initialized
   resources remain between cells. Re-run setup after restarting the kernel,
   and restart it when stale state makes results confusing.

VS Code documents `# %%` cells, Run Cell/Run Above/Run Below, and interpreter
selection in its [Python Interactive window guide](https://code.visualstudio.com/docs/python/jupyter-support-py).
The Jupyter extension's default marker pattern is anchored at the start of a
line, so an indented `    # %%` is not recognized as a cell boundary; see its
[marker definition](https://github.com/microsoft/vscode-jupyter/blob/main/src/platform/common/constants.ts).

## Check setup when execution fails

- If **Run Cell** is missing, confirm the file is saved as `.py`, the Python
  and Jupyter VS Code extensions are enabled, and each `# %%` marker starts at
  column zero.
- If the kernel will not start or imports fail, use **Python: Select
  Interpreter** to choose the project environment, then check that it contains
  the `jupyter` package and the project's dependencies.

## Put runtime import roots on `sys.path`

Add the directory that contains the package you want to import, before importing
that package. For example, `app.common` needs the service root that contains
`app/`; a repository-local `equity_shared` package needs the repository root.
These roots are different from paths used only by editor autocomplete.

Use an explicit checkout path in an early cell. Replace it for the current
machine; do not assume the Interactive Window's working directory or
`__file__` points at the source file.

```python
# %%
from pathlib import Path
import sys

WORKSPACE_ROOT = Path("/Users/kaestrl/projects/equity")
SERVICE_ROOT = WORKSPACE_ROOT / "equity_deviation"

for import_root in (SERVICE_ROOT, WORKSPACE_ROOT):
    import_root_text = str(import_root)
    if import_root_text not in sys.path:
        sys.path.insert(0, import_root_text)
```

Run that cell before imports that depend on those roots. Keep only roots the
module actually needs, and make their precedence explicit if package names
could collide. Do not paste credentials into cells; load project configuration
through its existing environment or settings mechanism.

## Use `_setup_interactive()` as the setup gateway

Keep environment loading and resource initialization in one clearly named
function. Make setup safe to repeat where practical, and keep it separate from
the data-processing steps being explored. Keep the function definition in the
source module between top-level cell markers. Move environment-sensitive
imports inside setup after loading configuration. The example reuses an
existing client in the same kernel instead of opening a second connection;
use the project's close/reset path before clearing and recreating a stale
resource.

```python
# %%
from app.common import config as common_config

# %%
async def _setup_interactive() -> None:
    """Load local configuration and initialize the interactive client."""
    global nats_client_

    common_config.load_environment_files()
    import equity_shared.nats.client as nats_client

    if "nats_client_" not in globals():
        nats_client_ = await nats_client.connect_nats()

# %%
```

Import the module after the path cell, then call setup from separate
Interactive Window input cells. Keep the top-level `await` out of the
importable source module:

```python
# %%
from app.deviation.api import nats_api

# %%
await nats_api._setup_interactive()

# %%
from zoneinfo import ZoneInfo

# %%
market_timezone = ZoneInfo("Asia/Ho_Chi_Minh")
db_dates = await nats_api.fetch_db_dates(market_timezone)
db_dates
```

## Organize definitions and function-body exploration

- In the callable-function layout, keep each complete function definition,
  including its docstring and body, between top-level `# %%` markers. The cell
  defines the function; call it from another cell to execute it.
- Put `# %%` before each independent top-level setup, call, or inspection step.
- In the body-stepping layout, put column-zero `# %%` markers between the
  function header/docstring and body statements you want to explore. Prepare
  the required local values as kernel variables and dedent selected body
  statements before running them as top-level code. Keep each runnable branch
  with its complete `if`/`elif`/`else` suite. A cell marker does not preserve
  the function's local variables, arguments, or control flow; use the debugger
  when those need to stay intact.
- Prefer body cells without `return`. If a branch cell needs a visible
  statement to be useful, assign or print/log the intermediate value in that
  branch so the cell is valid without a `return`.
- If an early `return` must stay with its branch, put the entire branch and its
  `return` statement(s) in one cell labeled `[ignore]`. Never split
  the branch header from its suite or separate the return from its branch.
  That label is a reminder, not a VS Code execution guard. To execute the
  function normally, import the complete module or run a complete function
  definition cell, then call the function.

Use the callable-function layout when normal function calls are the goal:
place markers outside the complete definition so **Run Cell** defines it as
one unit, then use another top-level cell to call it. Use body-stepping cells
only for statements that can be run with prepared inputs after dedenting.

The Python extension also has a **Python: Run Selection/Line in Python
Terminal** command. It removes common leading indentation from a selection;
use it only for code that becomes valid top-level Python after dedenting, with
any required local values prepared. It uses the Python terminal, not the
Interactive Window kernel; choose it only when that separate REPL session is
appropriate.

## Keep returns at function boundaries

A `return` statement is valid only inside a function. Prepare function-body
cells in this order:

1. First, redesign the function to use one final `return` when that keeps the
   logic clear. Let each branch assign the value that the final return will
   produce.
2. For branch cells you want to run interactively, omit `return`. Keep the
   branch and its full suite together, and add an assignment or `print`/log
   statement so the cell is valid and its result is visible.
3. If the function must keep an early return, put the entire branch together
   with its `return` statement(s) in one `[ignore]` cell. Never split
   an `if` header from its suite or a return branch from its return. Define and
   call the complete function normally to execute that path.

The first example refactors the function to one final return. Prepare `value`
in the kernel. The assignment and branch cells can be selected, dedented, and
run independently; the branch prints what it computed. The partial definition
and final return cells are marked `[ignore]`. Import the complete module or
run the complete definition to call the function normally. Treat the `print`
calls as temporary exploration output; use the project's logger or remove
them if normal calls should remain quiet.

```python
# %%
value = "  example  "

# %% [ignore: partial function definition]
def parse_optional_value(value: str | None) -> str | None:
    """Return a stripped value, or None for missing input."""
# %%
    parsed_value = None

# %%
    if value is None:
        print(f"Parsed value: {parsed_value!r}")
    else:
        parsed_value = str(value).strip()
        print(f"Parsed value: {parsed_value!r}")

# %% [ignore: return requires function context]
    return parsed_value

# %%
```

Create the returned value before the final return when that makes it easier to
inspect or debug. When an early return must be preserved, keep the whole branch
with its returns in one ignored cell:

```python
# %% [ignore: partial function definition]
def parse_optional_value_with_early_return(value: str | None) -> str | None:
    """Return a stripped value, or None for missing input."""
# %% [ignore: keep full branch and returns together]
    if value is None:
        return None
    else:
        return str(value).strip()

# %%
```

## Finish the interactive workflow

1. Run the path cell after selecting the intended interpreter.
2. Import the source module in the Interactive Window, then run its setup
   gateway.
3. Call functions with representative inputs and inspect returned values in
   separate cells. Keep calls with network, file,
   database, or other side effects explicit so they are not triggered by
   re-running unrelated cells.
4. After editing an imported module, reload it or restart the kernel, then
   repeat the path and setup steps. This avoids testing stale function objects
   or old initialized resources.

Use VS Code's debugger for stepping through a function while preserving its
real arguments and local variables. Use cells for independent top-level steps
and repeatable setup; a cell marker does not turn a function body into a
standalone function frame.
