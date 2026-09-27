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

## Use `_interactive_setup()` as the setup gateway

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
async def _interactive_setup() -> None:
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
await nats_api._interactive_setup()

# %%
from zoneinfo import ZoneInfo

# %%
market_timezone = ZoneInfo("Asia/Ho_Chi_Minh")
db_dates = await nats_api.fetch_db_dates(market_timezone)
db_dates
```

## Organize definitions and function-body exploration

- Put a column-zero `# %%` before each function header and after its body. A
  header on its own is incomplete; executing a complete `def` defines the
  function but does not execute its body.
- Put `# %%` before each independent top-level setup, call, or inspection step.
- If you put a `# %%` inside a function body, place the marker at column zero.
  Python ignores the comment's indentation, while VS Code can recognize the
  cell boundary.
- To step through function logic in the Interactive Window, prepare its inputs
  and required names in the kernel, then move the statement being explored into
  a self-contained top-level cell. You can also extract the step into a helper
  with explicit inputs and outputs and call it from a top-level cell.
- A cell boundary inside a function does not preserve local variables,
  arguments, or control flow across cells. Do not run a function-body fragment
  and assume it is executing inside the function. Use a complete module import
  and function call or the debugger with a breakpoint when local function
  state matters.

There are two useful layouts. In a **callable-function layout**, put markers
only outside a complete function so **Run Cell** defines it as one unit; use
another top-level cell to call it. In a **body-stepping layout**, put inner
markers at the statement boundaries you want to inspect. Those markers split
the definition into cells, so do not use Run Cell or Run Above to define that
partial function. Instead, import the source module from the Interactive
Window; Python parses the entire module and treats `# %%` as comments. To
execute individual body statements, move them to valid top-level cells after
preparing their inputs.

The Python extension also has a **Python: Run Selection/Line in Python
Terminal** command. It removes common leading indentation from a selection,
which can help send a function-body block to a REPL as top-level code. That
command uses the Python terminal, not the Interactive Window kernel; choose it
only when that separate REPL session is appropriate.

## Keep returns at function boundaries

A `return` statement is valid only while executing a function. A cell that
contains just `return result` cannot run as a top-level interactive cell. Keep
the returned value visible before the return and put a `# %%` marker directly
before the final return as a clear source boundary. This inner marker splits
the function across VS Code cells: the preceding partial-definition cell will
not include the return, and the return cell cannot run on its own. To call the
function normally, import the source module from the Interactive Window, so
Python parses the complete function with its return intact. To explore the
body in pieces, run its statements as valid top-level cells and inspect the
named value; do not run the return line by itself.

Prefer one final return when that keeps the logic clear:

This source example stays valid Python. Because it has an inner marker before
`return`, do not use **Run Cell** to define the function; import the containing
module from the Interactive Window so Python reads the complete definition.
The example function stands in for a function defined in the imported module.

```python
# %%
from datetime import date

# %%
def retain_weekdays(dates: list[date]) -> list[date]:
    """Return the supplied dates that fall on weekdays."""
    result = [day for day in dates if day.weekday() < 5]

# %%
    return result

# %%
```

Create the result before the final return. When multiple returns are needed
for clear control flow, put a `# %%` boundary immediately before each return
and keep each branch understandable as part of the complete function. Each
inner marker splits the definition into VS Code cells; import the containing
module to define the whole function. Return cells remain non-runnable on their
own.

```python
# %%
def parse_optional_value(value: str | None) -> str | None:
    if value is None:
# %%
        return None
# %%

    parsed_value = str(value).strip()
# %%
    return parsed_value

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
