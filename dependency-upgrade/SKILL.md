---
name: dependency-upgrade
description: Guidelines for checking, researching, updating, and aligning dependencies in a software project safely.
---

# Safe Dependency Upgrades and Alignment Guidelines

Use this skill when checking for newer versions of dependencies, researching their changes, upgrading them, and aligning the codebase to adopt new library features or resolve deprecations.

## 1. Outdated Check (Ecosystem-Specific)

Begin by listing the outdated packages in the workspace or project directory using the relevant package manager command:

### Node.js (npm / yarn / pnpm)
*   **Check:** `npm outdated` (exits with code 1 if packages are outdated, which is expected)
*   **Details:** Run `npm ls <package-name>` to identify transitively nested dependencies.
*   **Update:** `npm install <package>@latest` or `npm install <package>@<version>`.

### Python (uv / pip / poetry)
*   **Check (uv):** `uv pip list --outdated` or `uv tree` to inspect dependency chains.
*   **Check (pip):** `pip list --outdated`
*   **Update:** Update the package version constraints in `pyproject.toml` or `requirements.txt` and run sync (e.g. `uv sync` or `pip install -U`).

### Go
*   **Check:** `go list -u -m all`
*   **Update:** `go get <package>@latest` followed by `go mod tidy` and `go work sync`.

### Flutter & Dart
*   **Check:** `flutter pub outdated` or `dart pub outdated`
*   **Update:** `flutter pub upgrade --major-versions` or `dart pub upgrade --major-versions` (to update constraints), or `flutter pub upgrade` / `dart pub upgrade` (within constraints).

---

## 2. Researching Changelogs

Before executing updates, read the changelogs (or release notes) for every version between the installed version and the target version. Go through **each changelog item one by one** and, for every item, work through three questions:

### For each changelog item

1. **How does this affect the project?**
   - Search the codebase for usages of the changed API, pattern, or configuration.
   - Classify the impact: *breaking* (will fail at compile or runtime), *deprecation* (works now, will fail later), *behavior change* (subtly different output or side-effects), or *no impact* (internal change, unrelated feature, or fix for code we don't use).
   - Note the exact files and lines that are affected.

2. **How must the project be migrated?**
   - If the item is breaking or deprecated, determine the replacement API or pattern.
   - Write a concrete migration step: what to change, where, and to what.
   - If the item changes default behavior (e.g., stricter validation, new option defaults), document what config or code must be added to preserve current behavior or to adopt the new default intentionally.

3. **How can the project improve by using the new feature?**
   - If the item introduces a new API, performance improvement, or best practice, evaluate whether adopting it would benefit this project.
   - Consider: does it simplify existing code, improve performance, remove a workaround, or enable something previously difficult?
   - Only flag adoption opportunities that are concrete and relevant — skip features that don't apply to this codebase.

### Prioritization

After going through all items, group findings by priority:

1.  **Security Patches:** Prioritize upgrading packages with known CVEs (e.g., prototype pollution, memory safety issues, remote code execution).
2.  **Breaking Changes:** Items that will cause compile or runtime failures — must be fixed during the upgrade.
3.  **Deprecations:** Items that work now but will break in a future version — migrate now if practical, otherwise track as follow-up.
4.  **New Feature Adoption:** Concrete opportunities to simplify or improve the codebase — adopt during the upgrade if low-risk, otherwise track as follow-up.

Write all findings into the plan (or a dedicated analysis document) so the upgrade scope is explicit before implementation begins.

---

## 3. Creating the Upgrade Plan

For non-trivial changes, use the `plan-tracking` skill to draft a plan. Structure the upgrades into logical **Slices**:

*   **Slice 1:** Core runtime packages, runtime dependencies, and framework adapters.
*   **Slice 2:** Specialized styling, visualization, or charting components.
*   **Slice 3:** Development tooling, compilers, types, and ESLint configurations.
*   **Slice 4:** Final verification and visual polish.

Include explicitly defined **Validation Criteria** (e.g., `npm run build`, `npm run lint`, `npm run test` must pass clean).

---

## 4. Implementation Workflow

### Step 4.1: Upgrading Packages
*   Update the package file (e.g. `package.json`, `pyproject.toml`, `go.mod`, `pubspec.yaml`) with the target version constraints.
*   Run the installer (e.g. `npm install`, `uv sync`, `go mod tidy`, `flutter pub get`).

### Step 4.2: Applying Best Practices
Review code regions utilizing the updated packages and proactively adapt to modern patterns:
*   Replace deprecated hooks or APIs (e.g., migrating from `useContext` to React 19's `use` hook).
*   Correct deprecated component patterns or configuration parameters.

### Step 4.3: Resolving Strict Linter and Compiler Errors
New devDependencies and language upgrades will often surface new linting rules, deprecation warnings, and type incompatibilities. Address these immediately:
*   **Deprecations:** Migrate to the new APIs or patterns best practices if possible. Document reason for any temporary workarounds.
*   **Configuration Files:** Clean up configuration deprecations.

---

## 5. Validation

Every dependency update must pass a three-tiered validation:

1.  **Compilation Check:** Compile the production assets or binaries (e.g., `npm run build`, `go build`, `pyright`, `flutter build apk` / `flutter build ios` / `dart compile`). Ensure no type checker warnings or compiler deprecation errors occur.
2.  **Linter Check:** Run the project linter (e.g., `npm run lint`, `ruff check`, `golangci-lint`, `flutter analyze` / `dart analyze`). Ensure no styling or rule regressions are introduced.
3.  **Test Suite:** Run unit and integration tests (e.g., `npm run test`, `pytest`, `go test`, `flutter test` / `dart test`). Ensure 100% of existing test suites continue to pass.
