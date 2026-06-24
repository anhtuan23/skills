## Review

### Scope

Reviewed the new `git-commit-helper` skill content and the supporting reference
file against the stated workflow and convention.

### Findings

- The revised skill stays within the requested boundary: suggest commit message
  text only for the agent's own recent changes, with no staging or commit
  execution steps.
- The convention matches the requested format:
  `type(scope): short subject` with body bullets only for complex changes.
- The allowed type set is restricted to:
  `feat`, `fix`, `refactor`, `chore`, `docs`, `style`, `test`.

### Validation

- `git diff --check`: passed
- Manual read-through of:
  - `commit-msg/SKILL.md`
  - `commit-msg/references/commit-message-conventions.md`

### Notes

- The previous `git-commit-helper/SKILL.md` deletion remains staged in the
  index from pre-existing state. The new `commit-msg` files are worktree
  changes only because the workflow rules say not to alter stage state on the
  user's behalf.
