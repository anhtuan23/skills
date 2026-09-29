# Plan: Create a VS Code Python Interactive skill

## Goal

Create a focused, portable skill for preparing Python `.py` files to run in
VS Code's Python Interactive window. Cover cell markers, import roots, a
repeatable `_setup_interactive()` gateway, function-body exploration, and
return-statement boundaries, with examples adapted from
`equity_deviation/app/deviation/api/nats_api.py`.

## Scope

### In scope

- Add `python-interactive/SKILL.md` with a clear trigger description and
  step-by-step workflow.
- Update `my-python/SKILL.md` to route VS Code cell-based workflows to the new
  skill and avoid maintaining two overlapping sets of detailed instructions.
- Add the new skill to the root `README.md` skills table.
- Record implementation progress and review findings in this plan folder.

### Out of scope

- Editing the Equity example module or its project configuration.
- Changing general Python coding conventions beyond the interactive-workflow
  handoff in `my-python`.
- Adding or running automated tests/evals, modifying unrelated skills, or
  making commits.

## Research findings and design decisions

- The current `my-python` skill already mentions an interactive setup gateway,
  function cells, and a final return. A focused companion skill is useful only
  if it owns the detailed VS Code workflow and `my-python` points to it.
- VS Code's official Python Interactive documentation defines `# %%` cells,
  Run Cell/Run Above/Run Below, and interpreter selection:
  <https://code.visualstudio.com/docs/python/jupyter-support-py>
- The Jupyter extension's default cell marker regex is anchored at column zero.
  Body markers must start at the left edge; Python still ignores their
  indentation as comments. The implementation source is
  <https://github.com/microsoft/vscode-jupyter/blob/main/src/platform/common/constants.ts>.
- VS Code runs a cell as a separate unit. A cell delimiter inside an indented
  function does not carry the function's local variables or call context into
  another cell. The skill must distinguish defining a complete function,
  experimenting with dedented body statements in the interactive kernel, and
  invoking the function normally.
- Top-level `await` is Interactive Window input, not valid in an ordinary
  Python module. Keep async setup invocation cells separate from importable
  source code.
- For body stepping, first refactor return paths to one final return when
  clear. Make runnable branch cells complete and free of `return`, using
  assignments and print/log output as needed. If early returns must remain,
  keep each whole branch and its returns together in an ignored cell.
- The import-root example should use an explicit, editable workspace path and
  insert the directory that matches the module's import form. Do not rely on
  the Interactive window's current working directory or `__file__` being
  available in a kernel cell.
- Use the supplied `nats_api.py` pattern to illustrate an async setup that
  loads project configuration and connects dependencies, without copying
  secrets or making the skill depend on the Equity repository.

## Ordered implementation and review

1. Create `python-interactive/SKILL.md` with the cell workflow,
   `sys.path` setup, `_setup_interactive()` gateway, function/body boundaries,
   return rules, and a complete annotated example.
2. Add a short routing note to `my-python/SKILL.md` and list the new skill in
   `README.md`.
3. Review the authored Markdown against the scope and official VS Code behavior;
   inspect the diff and `git diff --check`. Do not run tests or evals because
   this request is for documentation and does not ask for testing.
4. Have an independent reviewer check accuracy, portability, trigger overlap,
   and whether the function/return example can be followed as written. Write
   findings under `review/`, address material findings, and update
   `progress.md`.
5. Return the finished skill for final human review.

## Acceptance criteria

- The new skill is a valid skill directory with `SKILL.md` frontmatter
  containing `name` and `description`.
- Its description clearly triggers for VS Code Python Interactive setup and
  cell-based Python editing, including when the user does not say “skill.”
- The example shows how to put the correct project import root on `sys.path`,
  define and call `_setup_interactive()`, and organize code using `# %%`.
- Cell markers start at column zero. Support both complete function cells for
  normal calls and body-stepping cells whose runnable statements remain
  complete after dedenting; label return-bearing fragments as ignored.
- It explains the limits of executing function-body selections and `return`
  statements as standalone cells without contradicting normal Python function
  execution.
- It follows the return-resolution order: refactor to one final return, make
  runnable branch cells complete without returns, or group an unavoidable
  branch and its returns in one ignored cell.
- The README and `my-python` handoff agree with the new skill's ownership.
- No Equity source files or unrelated skills are changed.
- Independent review findings are recorded and material findings are resolved
  before final human review.

## Approval gate

Approved by the user on 2026-09-27, with the skill name changed from
`vscode-python-interactive` to `python-interactive`. Implementation may begin.

## Follow-up decisions

- The user requested `_setup_interactive()` as the verb-first setup function
  name. Use this name in the skill and its handoff.
- The user noted that examples need a `# %%` boundary between each function
  header and its executable body. Put it after a function docstring when there
  is one, and directly after the header when there is none. Retain boundaries
  before body returns.
- The user identified that a cell split inside a multiple-return function left
  an `if` header without its suite, making the cell invalid to run alone.
  Keep the whole branch and its returns together in one ignored cell, and
  make executable branch exploration complete without returns. This supersedes
  the earlier example that split an `if` header from its suite.
- The user specified the return resolution order: try one final return first;
  add assignment/print/log statements to make runnable branch cells valid
  without returns; if that cannot preserve behavior, group the whole branch
  and returns in an ignored cell.
