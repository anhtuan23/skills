# Skills

Agent skills for OpenCode and compatible agents.

## Available Skills

| Skill | Description |
|-------|-------------|
| `commit-msg` | Suggest conventional commit messages for staged changes |
| `plan-tracking` | Track implementation plans with structured progress and review artifacts |
| `function-ordering` | Reorder functions within a file for better readability |
| `module-refactor` | Split large modules into smaller focused files |
| `long-file-refactor` | Refactor long files into manageable pieces |

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
