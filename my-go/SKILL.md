---
name: my-go
description: Coding standards, conventions, workspace setup, and validation workflows for Go development.
---

# Go Development Guidelines

This skill defines the coding standards, language preferences, workspace configuration, and validation workflows for Go development.

## Language Style and Conventions

- **Idiomatic and Conservative**: Keep Go code idiomatic, clean, and conservative. Match existing style unless a clear migration is underway.
- **Pattern Reuse**: Reuse existing repository, feature, and model patterns before inventing new structures.
- **Documentation**: Write descriptive documentation comments for every function to explain its purpose, parameters, and return values. Add concise comments for non-obvious behavior, especially diff logic, DB write rules, and lifecycle behavior.

## Validation Flow

Every Go change must pass validation and static analysis before completion:
1. **Formatting**: Format every Go file in the relevant module with `golines -m 100 -w .`, then `gofumpt -w .`. Run these commands from that module's root; `./...` is a Go package pattern, not a formatter path.
2. **Testing**: Run tests using `go test ./...`.
3. **Linting**: Run static analysis using `golangci-lint run ./...`.
4. **Sandboxed Cache Directory**: When running checks inside sandboxed environments, configure writable build caches such as `GOCACHE=/tmp/<project>-go-build-cache`.
