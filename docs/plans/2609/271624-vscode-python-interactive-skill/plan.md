# Plan: Create a VS Code Python Interactive skill

## Goal

Create a focused, portable skill for preparing Python `.py` files to run in
VS Code's Python Interactive window. Cover cell markers, import roots, a
repeatable `_interactive_setup()` gateway, function-body exploration, and
return-statement boundaries, with examples adapted from
`equity_deviation/app/deviation/api/nats_api.py`.

## Scope

### In scope

- Add `vscode-python-interactive/SKILL.md` with a clear trigger description and
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

- The current `my-python` skill already mentions `_interactive_setup()`,
  function cells, and a final return. A focused companion skill is useful only
  if it owns the detailed VS Code workflow and `my-python` points to it.
- VS Code's official Python Interactive documentation defines `# %%` cells,
  Run Cell/Run Above/Run Below, and interpreter selection:
  <https://code.visualstudio.com/docs/python/jupyter-support-py>
- VS Code runs a cell as a separate unit. A cell delimiter inside an indented
  function does not carry the function's local variables or call context into
  another cell. The skill must distinguish defining a complete function,
  experimenting with dedented body statements in the interactive kernel, and
  invoking the function normally.
- Prefer one final `return` when practical. Create the result before it and put
  `# %%` immediately before the return boundary. If control flow needs multiple
  returns, isolate each return boundary and explain that a `return` cannot be
  executed as a top-level interactive statement; it runs only when the
  function itself is called.
- The import-root example should use an explicit, editable workspace path and
  insert the directory that matches the module's import form. Do not rely on
  the Interactive window's current working directory or `__file__` being
  available in a kernel cell.
- Use the supplied `nats_api.py` pattern to illustrate an async setup that
  loads project configuration and connects dependencies, without copying
  secrets or making the skill depend on the Equity repository.

## Ordered implementation and review

1. Create `vscode-python-interactive/SKILL.md` with the cell workflow,
   `sys.path` setup, `_interactive_setup()` gateway, function/body boundaries,
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
  define and call `_interactive_setup()`, and organize code using `# %%`.
- It explains the limits of executing function-body selections and `return`
  statements as standalone cells without contradicting normal Python function
  execution.
- It covers a single final return, precomputing the returned value, a marker
  before the return, and isolating multiple return boundaries where needed.
- The README and `my-python` handoff agree with the new skill's ownership.
- No Equity source files or unrelated skills are changed.
- Independent review findings are recorded and material findings are resolved
  before final human review.

## Approval gate

This plan is ready for human review. Implementation begins after approval.
