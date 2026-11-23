---
name: commit-msg
description: Write Conventional Commits messages for changes the agent just made, one per logical change, following the repository's own commit conventions. Use when suggesting a commit message, or when committing your own work.
---

# Commit Msg

Use this skill when the agent has finished one or more logical changes and
needs a commit message for each: to suggest it to the user, or to commit
directly when the project's rules allow agent commits.

## Workflow

1. **Learn the repo's conventions.** Read the project's agent rules
   (`AGENTS.md`, `CLAUDE.md`, or similar) for commit rules, then run
   `git log --format=%s -20` on the current branch. Check for a commitlint or
   similar config. These win over the defaults below: allowed types, scope
   names (package, service, or folder), subject length, and required trailers.
2. **Split into logical changes.** Group the changes the agent made by
   purpose. Each group gets its own message, and its own commit when
   committing. Commit only your own changes; leave other work in the tree
   untouched.
3. **Pick the type** by the main purpose of the change (see Decision Rules).
   Default set: `feat`, `fix`, `refactor`, `chore`, `docs`, `style`, `test`,
   extended by any types the repo's history or config uses, such as `build`,
   `ci`, or `perf`.
4. **Pick the scope.** Use one when a single area dominates, spelled as the repo
   spells it in its history (for example the package or service name). Omit it
   when the change spans unrelated areas.
5. **Write the subject:** `type(scope): short subject`, or `type: short subject`
   with no scope. Imperative mood, under about 60 characters, no trailing
   period. Mark breaking changes with `!` before the colon:
   `feat(api)!: remove deprecated endpoint`.
6. **Add a body only when the change is complex:** 1–3 bullets for what
   changed, why, and optionally the impact. Small or obvious changes get the
   subject only.
7. **Add trailers** the environment requires, such as a `Co-Authored-By` line,
   after a blank line at the end.

## Output Format

When suggesting, return one copy-ready block per logical change:

```text
type(scope): short subject

- what changed
- why
- (optional) impact or scope
```

When committing, use the same text as the commit message, and report each
commit's SHA and subject.

## Decision Rules

- Prefer `refactor` over `fix` when behavior is intended to stay the same.
- Prefer `docs` for comments, READMEs, plans, and other documentation-only
  edits.
- Prefer `style` only for formatting or non-behavioral polish.
- Prefer `chore` for maintenance that fits no other type, such as tooling,
  lockfiles, or board updates.
- When one change truly mixes concerns that cannot be split (for example a
  single edited file), say it would be cleaner as separate commits, then give
  the best single message.

For the rationale behind these conventions, read
`references/commit-message-conventions.md`.
