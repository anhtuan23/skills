# Skills

Agent skills for Claude Code, Codex, OpenCode, and compatible agents.

## Available Skills

| Skill | Description |
|-------|-------------|
| `git-reconcile` | Reconcile advanced Git merge and rebase conflicts from base, intent, and behavioral evidence |
| `worktree-ship` | Develop in parallel worktrees, ship whole or partial features to main with rebase and --no-ff merge, deploy to production over SSH |
| `commit-msg` | Suggest conventional commit messages for staged changes |
| `complexity-combat` | Scan for over-engineered code, categorize, and ask human which problems are real before simplifying |
| `plan-tracking` | Track implementation plans with structured progress and review artifacts |
| `function-ordering` | Reorder functions within a file for better readability |
| `python-interactive` | Set up Python files for cell-by-cell execution in VS Code's Interactive window |
| `module-refactor` | Split large modules into smaller focused files |
| `project-refactor` | Refactor a project around clear runtime flow and ownership |
| `long-file-refactor` | Refactor long files into manageable pieces |
| `ask-matt` | Find the right skill or workflow |
| `domain-modeling` | Build and sharpen a project's domain model |
| `grill-me` | Interview the user when material choices remain |
| `grill-with-docs` | Interview the user and record durable project decisions |
| `grilling` | Interview the user to stress-test a plan, decision, or idea |

## Install

```bash
npx skills add anhtuan23/skills --skill <name>
```

Install all skills:

```bash
npx skills add anhtuan23/skills --skill '*' -a claude-code codex -y
```

Name both tools, and run this from the project's main checkout:

- `codex` puts the real copies in `.agents/skills`, which Codex, OpenCode, and
  Antigravity read. `claude-code` then adds a link to each in `.claude/skills`.
  Naming only `claude-code` creates separate copies instead.
- `--all` also installs for every other tool the CLI knows, such as Eve's
  `agent/skills` folder.
- Links created from a worktree point through its path, so they break when the
  worktree is removed.

`skills-lock.json` does not record which tools get a skill, so restoring from it
does not recreate the `.claude/skills` links. Name the tools again on a new
machine.

## Update

Update a single skill:

```bash
npx skills update plan-tracking
```

Update all installed skills:

```bash
npx skills update
```

## Usage

Skills are loaded automatically when a task matches their description, or can be invoked explicitly via the skill tool.
