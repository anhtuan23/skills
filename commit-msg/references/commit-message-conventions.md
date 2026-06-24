# Commit Message Conventions

This reference explains the conventions used by `commit-msg`.

## Core Format

- Use a Conventional Commits style prefix:
  `type(scope): short subject`
- Scope is optional and should be short, stable, and codebase-oriented.
- Keep the subject under 60 characters for scanability in logs and review
  tools.
- Write the subject in imperative mood such as `add`, `fix`, `refactor`,
  `update`, or `remove`.
- Do not end the subject with a period.

## Allowed Types

- `feat`: adds a user-facing or developer-facing feature
- `fix`: corrects a bug or incorrect behavior
- `refactor`: restructures code without intended behavior change
- `chore`: maintenance work that does not fit the other allowed types
- `docs`: documentation-only changes, including explanatory comments
- `style`: formatting or presentational cleanup without behavior change
- `test`: adds or updates tests

## Body Guidance

Use a body only when the changes are complex and the extra context improves
reviewability.

Preferred shape:

```text
- bullet of what changed
- bullet of why
```

Guidelines:

- Keep bullets factual and concise.
- Focus on intent and impact, not line-by-line mechanics.
- Avoid repeating the subject in different words.
- Omit the body for small or obvious changes.

## Source Basis

These rules are based on:

- Conventional Commits 1.0.0 for the prefix/body/footer structure
- Chris Beams' guidance for short imperative subjects and meaningful bodies
- Tim Pope's guidance for blank-line separation and readable body formatting
