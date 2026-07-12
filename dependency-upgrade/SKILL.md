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

Before executing updates, research the changes between the installed version and the target version. Focus on:

1.  **Security Patches:** Prioritize upgrading packages with known CVEs (e.g., prototype pollution in Axios, memory safety issues, remote code execution).
2.  **Breaking Changes:** Identify removals, API modifications, or major version updates that will break compilation or runtime behavior.
3.  **Deprecations:** Document components, methods, or configurations scheduled for removal in future versions.
4.  **Ecosystem Features:** Identify opportunities to apply new features or best practices introduced by the new versions.

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
