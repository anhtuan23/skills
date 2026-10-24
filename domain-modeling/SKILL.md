---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing domain terminology, updating the project's designated context with domain language, or recording or editing an ADR.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and recording resolved language and decisions as they crystallise. (Merely reading the project's context documentation for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## Find the project's context conventions

Before editing durable domain knowledge, read the applicable `AGENTS.md`, project context maps, and existing context and ADR files. Follow the repository's declared locations and formats. This includes conventions such as `AI_CONTEXT.md`, `CONTEXT.md`, or files under `docs/ai_context/`. Update those canonical files in place; do not create a parallel `GLOSSARY.md` or glossary map when the project already has a context system.

Use the following glossary layout only when the repository has no context-file convention:

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `GLOSSARY-MAP.md` exists at the root, the repo has multiple glossary contexts. The map points to where each one lives:

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

Create fallback files lazily: only when you have something to write. If no project context convention exists, create `GLOSSARY.md` when the first term is resolved. Follow the project's ADR location if it declares one; otherwise use `docs/adr/`, creating it when the first ADR is needed.

## During the session

### Challenge the project's domain language

When the user uses a term that conflicts with the project's existing context documentation, call it out immediately. "The project context defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update the canonical context inline

When a term is resolved, update the project's designated context file right there. Don't batch these up: capture them as they happen, matching the existing structure and format. If the project explicitly uses `GLOSSARY.md`, use the format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md). If it has no context convention, use that format for the fallback `GLOSSARY.md`.

When updating a glossary, keep it devoid of implementation details. Do not treat a glossary as a spec, scratch pad, or repository for implementation decisions. If the project uses a broader context document, preserve its purpose and keep domain language in the relevant section.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Follow the repository's ADR format and location if declared; otherwise use [ADR-FORMAT.md](./ADR-FORMAT.md) under `docs/adr/`.
