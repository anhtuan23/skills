---
name: my-react
description: Coding standards, conventions, architectural patterns, and validation workflows for React and TypeScript development.
---

# React and TypeScript Development Guidelines

This skill defines coding standards, React/TypeScript architectural patterns, preferences, and validation flows for React and TypeScript development.

## Language and Component Rules

- **Function Components**: Prefer React function components over class components. Use modern React patterns (such as Hooks) for state and lifecycle management.
- **Strict TypeScript**: Prefer strict TypeScript configurations. Avoid using `any` types; utilize explicit interfaces and types to ensure type-safety.
- **Type Location**: Keep type definitions close to where they are used. Only move types to shared files or global models when they are genuinely used across multiple features or services.

## Architectural Patterns

- **Separation of Concerns**: Separate view (presentation), state/viewmodel (business logic), and pure data logic when the project or package follows that pattern.
- **Side Effect Isolation**: Keep side effects (such as API calls, subscriptions, and data syncing) in custom hooks or dedicated state modules, not within the presentation/view component code.

## Validation Flow

Every React and TypeScript change must pass validation before completion:
1. **Linting and Type Checking**: Run type checks (e.g., `tsc --noEmit` or equivalent workspace check) and linting commands configured for the package.
2. **Build Verification**: Run production build checks (e.g., `npm run build` or `vite build`) to verify there are no compilation errors.
