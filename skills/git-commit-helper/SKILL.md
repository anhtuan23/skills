---
name: git-commit-helper
description: Generate semantic and structured Git commit messages from staged changes.
---

# Git Commit Helper

Use this skill when preparing or staging changes to automatically draft a commit message.

## Instructions
1. Get the list of changes by running `git diff --cached`. Do NOT look at unstaged files.
2. If there are no staged changes, ask the user to stage files first.
3. Write a commit message following the **Conventional Commits** standard:
   - Structure: `<type>(<optional scope>): <description>`
   - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
   - Length: The subject line must be under 50 characters, written in lowercase, present tense.
4. If the changes are complex, add a blank line followed by a paragraph or bullet points explaining the motivation and reasoning behind the change.
5. Present the proposed commit message to the user for approval.
