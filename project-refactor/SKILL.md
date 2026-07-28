---
name: project-refactor
description: Clean up and restructure a project or feature so it is easy to read and maintain, without changing how it works. Use when code is hard to follow, files are messy, names are confusing, or major cleanup needs a clear plan and full testing.
---

# Project Refactor

## Goal

Make the codebase clean, simple, and easy to understand, while keeping all important safety checks and rules intact.

## Step-by-Step Guide

1. **Map out how the code works**
   Follow the complete path from start to finish: see how user input enters, how decisions are made, how data is saved, and how results are sent back.

2. **Explain the process in plain language**
   Describe how the feature works in simple words before making any structural changes.

3. **Keep essential safety, remove unnecessary clutter**
   - Keep rules that protect against data loss, race conditions, or system crashes.
   - Delete middleman code, empty wrappers, and extra steps that do not add real value.
   - Avoid creating classes that don't store any data (stateless classes). Replace them with simple, standalone functions that take an input and return an output directly.

4. **Group code by feature, not by technical layer**
   - Put all code for a single feature together (its paths, logic, data storage, and helpers).
   - Avoid creating vague dumping grounds like `utils/`, `services/`, or `handlers/` unless multiple features actually share the exact same code.

5. **Use simple, clear names**
   Name files, functions, and variables so that anyone reading them immediately understands their job without having to guess.

6. **Create a plan before making big changes**
   - For major cleanups, write down a clear plan and get approval before changing code.
   - Include a visual diagram (such as a Mermaid flowchart) showing the proposed code structure so reviewers can easily visualize the changes.
   - Delete old, unused files completely rather than leaving empty placeholders or temporary workarounds behind.

7. **Update everything to match**
   Make sure production code, tests, documentation, and configuration files all use the new names and folder layout consistently.

8. **Explain *why*, not *what*, in comments**
   Add brief notes only when a step has a non-obvious safety rule or specific sequence, explaining *why* it is necessary rather than repeating what the code syntax does.

9. **Test thoroughly**
   Run local tests first, followed by full project tests, linters, and type checks to confirm everything runs smoothly without unexpected breaks.

## Cleanup Checklist

- Is there one obvious starting point for each workflow?
- Can a new team member read the code from top to bottom without getting confused?
- Is code organized by feature rather than split across generic technical folders?
- Were unnecessary stateless classes replaced with simple, direct functions?
- Does every file and function serve a clear, distinct purpose?
- Are variable and function names self-explanatory?
- Was obsolete code completely removed instead of being hidden?
- Is a visual diagram provided to help reviewers understand the structural changes?
- Do all tests pass and confirm that the original behavior is preserved?

## Final Summary Report

When finished, summarize:
- What the new code structure looks like (with a Mermaid diagram for reviewers).
- What clutter or extra steps were removed.
- What files or concepts were renamed.
- Test and validation results.
- Any remaining risks or follow-up items.
- A concise summary line for the change (do not commit changes automatically).


