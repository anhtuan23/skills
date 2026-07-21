---
name: my-python
description: Coding standards, conventions, interactive workflows, and validation processes for Python development.
---

# Python Development Guidelines

This skill defines the coding standards, language preferences, interactive environment setups, and validation workflows for Python development.

## Language Style and Conventions

- **PEP 8**: Follow standard PEP 8 formatting guidelines.
- **Naming Conventions**: 
  - Use `snake_case` for functions, methods, and variables.
  - Use `PascalCase` for class names.
  - Function names should start with verbs.
  - Boolean variables and properties should prefix with `is_`, `has_`, or `can_`.
- **Private Helper Hierarchy**:
  - Use a single leading underscore for standard internal/private helper functions.
  - When a file has multiple levels of helper functions, use numbered private prefixes to denote helper hierarchy, e.g., `_2_my_helper()`, `_3_nested_helper()`.
- **Built-ins**: Avoid shadowing Python built-in names.
- **Imports**: Prefer explicit module imports over direct imports of functions, classes, or variables (e.g., use `import module` and `module.func()` instead of `from module import func`).
- **Collections**: Prefer using standard built-in collection types (`dict`, `list`, `tuple`) directly instead of importing aliases from the `typing` module (e.g., use `list[str]` instead of `List[str]`).
- **Type Hints**: Always use type hints for all function signatures, variable declarations, and class attributes to ensure clean, type-safe, and self-documenting code.
- **Documentation**: Write descriptive docstrings for every function, method, and class to explain its purpose, parameters, and return values.

## Frameworks and Library Preferences

- **Pydantic**: Use Pydantic for structured data validation and settings management when working on a service that already uses it.
- **Data Processing**:
  - Prefer using vectorized library-backed data processing tools like `polars` or `numpy` for meaningful volumes of data.
  - Use plain Python loops only when simpler and when the data volume is small enough.
  - Always pass an explicit `schema` when creating production-path Polars DataFrames.

## Interactive Mode & Files

- For new Python files, evaluate whether an interactive workflow is beneficial.
- For interactive-friendly files, organize the logic as pure functions.
- Add an `_interactive_setup()` function near the top of the file before other workflow functions so initialization runs first.
- Flank each function header and docstring block with `# %%`.
- Keep each function to a single final `return` statement, returning only simple processed data, and insert `# %%` immediately before the return.

## Validation Flow

Every Python change must pass validation and static analysis before completion:
1. **Testing**: Run tests using `uv run pytest`.
2. **Formatting and Linting**: Run `uv run ruff check .`.
3. **Type Checking**: 
   - Run type check on the entire workspace: `uv run pyright` or `uv run pyright .`.
   - Run type check on a specific service/directory: `uv run pyright <directory>` (e.g., `uv run pyright equity_trader`).
   - All modifications must pass type checking without introducing new errors or warnings.
4. **Sandboxed Cache Directory**: When running checks inside sandboxed environments, configure writable caches such as `UV_CACHE_DIR=/tmp/<project>-uv-cache`.
