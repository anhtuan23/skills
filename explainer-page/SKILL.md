---
name: explainer-page
description: Write a self-contained static HTML page that explains a hard concept behind a plan or doc with diagrams, color, and worked examples. Use when a plan involves a concept that prose explains poorly, such as data flow across services, state machines, timing or races, before/after architecture, or tricky math; or when the user asks for an explainer page.
---

# Explainer Page

An explainer page helps a human understand a concept. It accompanies the
Markdown docs and never replaces them: the Markdown stays the source of truth
that agents read, diff, and edit. The page explains the same facts visually.

## When to Write One

Write a page when a reader would otherwise have to build a mental picture from
several paragraphs, for example:

- data or messages flowing across several services
- a state machine, lifecycle, or retry/recovery path
- timing, ordering, or race conditions
- a before/after change of architecture or ownership
- math or rules with several cases that a worked example makes clear

Skip it for routine plans, small fixes, and anything a short Mermaid diagram in
the Markdown already explains well. Prefer Mermaid first; write a page when one
diagram is not enough.

## Where It Lives

- For a plan: `docs/plans/YYMM/DDHHMM-{name}/explainer.html`.
- For another doc: next to that doc, named `{doc-name}.explainer.html`.
- Link it near the top of the Markdown it explains, for example
  `Explainer: [explainer.html](explainer.html)`.

## How to Build It

- One `.html` file. No build step, no external scripts, fonts, or CDNs, so it
  opens offline in a browser or VS Code's Integrated Browser (right-click the file, Open in Integrated Browser), and diffs stay
  reviewable.
- Draw diagrams as inline SVG. Use plain CSS for layout and color. Small inline
  JavaScript is fine for a toggle or step-through, but the page must make sense
  without it.
- Define colors as CSS variables on `:root` and support dark mode with
  `@media (prefers-color-scheme: dark)`. Use color to carry meaning (one color
  per service, state, or outcome) and say what each color means.
- Readable width (about 60–80 characters of body text), clear headings, and
  labels on every arrow and box.

## Content Order

1. **What and why**: one or two sentences on the problem the concept solves.
2. **Mental model**: the single picture to keep in mind, as a diagram.
3. **Walkthrough**: one concrete example traced step by step, with real names
   from the code (services, NATS subjects, tables, functions).
4. **Edge cases**: the cases that make the concept hard, each with a small
   diagram or table.
5. **Glossary**: only terms the page introduces; link to the project glossary
   for the rest.
6. **Source**: links to the Markdown and code it explains.

Use the project's domain terms. Do not invent facts the Markdown lacks; if the
page reveals a gap, fix the Markdown first.

## Keeping It Current

Update the page in the same change when the concept it explains changes. Do
not track progress on it; status belongs in `progress.md`. Once a plan is done,
leave the page as part of the plan's record.
