## Objective

Create a new or replacement skill in this repository that suggests a Git commit
message for changes the agent has just made, matching the typical
`~/projects/equity/AGENTS.md` workflow of offering one descriptive commit
message after changes are complete.

## Current State

- The repository currently tracks `git-commit-helper/SKILL.md`, but the user
  wants the skill renamed to `commit-msg`.
- The committed version is minimal and only instructs the agent to inspect staged changes and emit a Conventional Commits message.
- The workspace otherwise has no visible project files beyond `.git`, so this task will establish the needed project structure.
- The user wants a narrower convention than generic "best possible" guidance:
  `type(scope): short subject`, subject under 60 chars, and body bullets only
  when the change is complex.

## Research Basis

- Conventional Commits v1.0.0 defines the canonical structure, optional scope, body, and footer/trailer handling.
- Chris Beams' commit-message guidance reinforces subject/body separation, short subjects, imperative mood, and body content focused on why.
- Tim Pope's guidance reinforces 50-character summary, 72-character body wrapping, blank-line separation, and imperative wording.
- Git's trailer docs confirm footer/trailer formatting conventions and support structured metadata such as `Refs:` or `Signed-off-by:`.
- `equity/AGENTS.md` requires the final workflow to suggest one descriptive commit message per logical change and to avoid staging/committing on the user's behalf.

## Proposed Deliverables

1. Create `commit-msg/` in the worktree.
2. Replace `SKILL.md` with a more complete skill that:
   - is used after the agent has made changes,
   - suggests commit text only,
   - chooses from `feat`, `fix`, `refactor`, `chore`, `docs`, `style`, `test`,
   - formats the message as `type(scope): short subject`,
   - keeps the subject under 60 characters,
   - adds bullets for what changed and why only when the changes are complex,
   - returns the message as a suggestion without approval flow.
3. Add optional `references/commit-message-conventions.md` to keep SKILL.md concise while preserving the researched decision rules.
4. Update `progress.md` during implementation and validation.
5. Record review notes in `review.md` after implementation.

## Validation Plan

- Re-read the created files for instruction quality and internal consistency.
- Run `git diff --check`.
- Inspect `git status --short` to confirm the expected new files and the restored/replaced skill path.

## Risks

- Over-prescribing one team's exact style instead of a broadly useful convention.
- Duplicating too much guidance into `SKILL.md` rather than using progressive disclosure.
- Drifting into staged-change inspection instead of summarizing the agent's own
  recent changes.
- Letting the skill drift from "suggest a message" into commit execution workflow.
