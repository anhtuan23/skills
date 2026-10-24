# Skills

Agent skills for Codex, OpenCode, and compatible agents.

## Available Skills

| Skill | Description |
|-------|-------------|
| `git-reconcile` | Reconcile advanced Git merge and rebase conflicts from base, intent, and behavioral evidence |
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
npx skills add anhtuan23/skills --all
```

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
