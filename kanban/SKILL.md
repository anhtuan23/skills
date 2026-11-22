---
name: kanban
description: Create, update, move, complete, and archive items on the repo's shared `kanban.md` task board, then commit and push it so other machines see the change. Use when starting or finishing a task, recording a deferred bug, risk, or follow-up, choosing what to work on next, or tidying the board at the start of a month.
---

# Kanban

`kanban.md` at the repo root is the one task board shared by every machine and
worktree. Other agents read it to learn what is active, where it runs, and how
to resume it. Every item must make sense to an agent that has none of your
context.

## Board Layout

```text
kanban.md
├── ## 🚧 In Progress   tasks someone is working on now
├── ## 📋 To Do         tasks waiting to start, including deferred findings
└── ## ✅ Done          tasks completed this month
docs/kanban/YYYY-MM.md  completed tasks from earlier months
```

Edit `kanban.md` in the main checkout of the repo, not in a worktree. The board
lives on `main`, and a worktree copy goes stale.

## Item Format

```markdown
- [owner] One-sentence summary of the task. (created YYYY-MM-DD HH:MM ICT on <machine>, <context>)
  - Why or evidence: what prompted it, with file paths, commits, or research notes.
  - Status (YYYY-MM-DD HH:MM ICT): current state and the next step.
  - Where: machine `<machine>`, branch `<branch>`, worktree `<path>`.
  - Resume: `cd <path> && cat docs/plans/YYMM/DDHHMM-<name>/progress.md`.
```

- **Owner tag:** the service or area, in square brackets, such as `[trader]`,
  `[fetch]`, or `[deploy]`.
- **Summary:** state the task or the problem, not the activity. "Auction
  writes pay DNS+TCP+TLS on almost every order" is better than "look at
  latency".
- **Origin:** the created stamp also names the machine (from `hostname`) and
  the context: the branch or worktree, plus the task or plan that turned up
  the item. Example:
  `(created 2026-11-22 10:15 ICT on air-m1, worktree auction-profit-tiers, while planning the profit-tier buffer)`.
- **Timestamps:** use `YYYY-MM-DD HH:MM ICT`. Get it with
  `TZ=Asia/Ho_Chi_Minh date '+%Y-%m-%d %H:%M ICT'`. Add `started`, `updated`,
  and `completed` to the same parentheses as they happen, so the stamps stay
  together.
- **To Do items** need the summary, origin, and enough context to act on later.
  `Where` and `Resume` are optional until work starts.
- **In Progress items** must have `Where` and `Resume`. Link the plan folder
  when one exists (see the `plan-tracking` skill).

## Lifecycle

```mermaid
stateDiagram-v2
    [*] --> ToDo: create (deferred finding or new task)
    [*] --> InProgress: create and start now
    ToDo --> InProgress: start
    InProgress --> InProgress: status update
    InProgress --> ToDo: pause
    InProgress --> Done: complete
    ToDo --> Done: cancel, with the reason
    Done --> Archive: next month
```

1. **Create.** When you find work outside the current task, such as a bug, a
   risk, or a follow-up you are deferring, add it to To Do without asking.
   Name it in your final response.
2. **Start.** Move the item to In Progress, add `started`, `Where`, and
   `Resume`. Any task you work on needs an In Progress item, even one you
   created a minute ago.
3. **Update.** When the state changes, such as a plan written, waiting on the
   human, merged, or deployed, edit the item's `Status` line in place and bump
   `updated`. Keep only the current status plus the facts a resumer needs.
   History belongs in the plan's `progress.md` and in git.
4. **Pause.** If you stop without finishing, keep `Resume` exact and say what
   it waits on.
5. **Complete.** Move the item to the top of Done. Shrink it to a summary of
   the outcome: what shipped (merge SHA), whether it is deployed, and the plan
   link. Add `completed`. A cancelled item says why it was not worth doing.

## Choosing What to Do Next

Run `hostname`, then read the Machines section of
`docs/ai_context/operations.md` to learn what this machine usually does.
Prefer To Do items that fit it, and items other items depend on.

## Commit and Push

Commit and push the board as soon as task state changes, so other machines see
it. Agents may push `kanban.md` to `main` without asking. Commit nothing else
in the same commit.

```bash
cd <main checkout>
git pull --rebase=merges origin main
# edit kanban.md
git add kanban.md
git commit -m "chore(kanban): <start|update|complete|add> <short item name>"
git push origin main
```

If the push is rejected, run `git pull --rebase=merges origin main` and push
again. If the rebase conflicts in `kanban.md`, keep both sides' items and
re-sort them; never drop another agent's item.

## Monthly Archive

On the first board edit of a new month, move every Done item completed in an
earlier month to `docs/kanban/YYYY-MM.md` for the month it completed, creating
the file if needed. Newest first, as on the board. Commit this as its own
`chore(kanban): archive YYYY-MM` commit.
