# Development Tooling

## Purpose

This document defines the initial development tooling for Mendel's Greenhouse.

The goal is to keep the implementation fast to iterate, easy to test, and resistant to low-quality code as the game moves from documentation to MVP.

## Dependency Groups

Use Poetry dependency groups.

Runtime dependencies:

```powershell
poetry add pyxel
```

Initial development dependencies:

```powershell
poetry add --group dev pytest pytest-cov hypothesis ruff poethepoet Babel pyxel-mcp
```

Future browser-test dependencies, added only when a runnable web build exists:

```powershell
poetry add --group dev pytest-playwright
poetry run playwright install
```

Optional later dependencies:

- `pre-commit` if local hooks become useful.
- `pytest-xdist` if the test suite becomes slow.

Do not add `taskipy`; this project uses Poe the Poet for task automation.

## Poe Task Runner

Use Poe the Poet for development tasks in `pyproject.toml`.

Recommended baseline:

```toml
[tool.poe.tasks]
test = "pytest"
test-cov = "pytest --cov=mendels_greenhouse --cov-report=term-missing"
lint = "ruff check ."
lint-fix = "ruff check . --fix"
format = "ruff format ."
check-format = "ruff format --check ."
check = ["lint", "check-format", "test"]
build-assets = "python tools/build_assets.py"
i18n-extract = "pybabel extract -o locale/messages.pot mendels_greenhouse"
i18n-update = "pybabel update -i locale/messages.pot -d mendels_greenhouse/locale -D mendels_greenhouse"
i18n-compile = "pybabel compile -d mendels_greenhouse/locale -D mendels_greenhouse"
```

Rules:

- Use `poe test` for the default test command.
- Use `poe check` before commits that touch implementation code.
- Use `poe build-assets` after changing generated `.pyxres` assets.
- Use `poe i18n-compile` whenever `.po` files change.
- Keep task names short and stable so future agents can run them without guessing.
- Use `poe start` to run the Pyxel game entrypoint.

## Tester Shortcuts

Runtime tester shortcuts are allowed only for local QA and manual playtesting.
They must not be presented as normal player-facing progression.

Current tester code:

| Code | Effect | Purpose |
| ---- | ------ | ------- |
| `MONEYTREE` | Sets credits to `999999` | Lets testers buy unlocks and jump quickly to later progression segments. |

Tester shortcuts should be covered by targeted tests and should remain easy to
remove or disable for a production distribution.

## Pyxel Agent Tooling

The project may use Pyxel-specific agent tooling when available:

- `pyxel-mcp` is the approved MCP server for Pyxel inspection and automation.
- `pyxel-skill` is the approved local Codex skill for Pyxel implementation guidance.

Rules:

- Install `pyxel-mcp` as a development dependency of the `game/` package.
- Prefer project specs over generic skill defaults when they conflict.
- Do not use MCP output as a substitute for tests.
- Use Pyxel/MCP screenshot or validation tools for visual changes when they are exposed to the current agent session.
- If MCP tools are not exposed, fall back to `poe check`, targeted pytest runs, and direct Pyxel runtime checks.
- Configure MCP to use the Poetry-managed `pyxel-mcp` executable instead of adding another global install.
- Use MCP audio tools for Pyxel sounds and music when adding or changing audio assets.

Recommended MCP checks:

| Work Type | MCP Tools |
| --------- | --------- |
| Pyxel code changes | `validate_script`, `run_and_capture`, `inspect_state` |
| Main screen layout | `run_and_capture`, `inspect_layout`, `inspect_palette` |
| Sprite/image-bank changes | `inspect_sprite`, `inspect_bank`, `inspect_palette` |
| Tilemap/background changes | `inspect_tilemap`, `inspect_palette`, `run_and_capture` |
| Animation changes | `capture_frames`, `inspect_animation`, `compare_frames` |
| Music and sound effects | `render_audio` |

Detailed workflow lives in [pyxel-mcp.md](pyxel-mcp.md).

## Ruff

Use Ruff as the primary formatter and linter.

Follow PEP 8 defaults unless the project has a documented reason to diverge.

Rationale:

- Ruff is a Python linter and formatter.
- It supports `pyproject.toml`.
- It replaces several common tools for this project scope, including formatter, import sorting, and many Flake8-style lint rules.
- PEP 8 recommends limiting code lines to 79 characters, so the project should not use wider formatter defaults for normal Python code.

Recommended baseline:

```toml
[tool.ruff]
line-length = 79
target-version = "py311"
src = ["mendels_greenhouse", "tests"]

[tool.ruff.lint]
select = [
  "E",    # pycodestyle errors / PEP 8
  "W",    # pycodestyle warnings / PEP 8
  "F",    # Pyflakes
  "I",    # import sorting
  "N",    # PEP 8 naming
  "UP",   # pyupgrade
  "B",    # flake8-bugbear
  "SIM",  # flake8-simplify
  "C4",   # flake8-comprehensions
  "RET",  # flake8-return
  "PT",   # pytest style
  "PTH",  # pathlib usage
  "RUF",  # Ruff-specific rules
  "ARG",  # unused arguments
  "EM",   # exception message style
  "ERA",  # commented-out code
  "EXE",  # executable file consistency
  "ISC",  # implicit string concatenation
  "PIE",  # unnecessary code patterns
  "PL",   # pragmatic Pylint rules
  "T20",  # print statements
  "YTT",  # sys.version pitfalls
]
ignore = []

fixable = ["ALL"]
unfixable = []

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = [
  "ARG",
  "PLR2004",
]

[tool.ruff.lint.isort]
known-first-party = ["mendels_greenhouse"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "auto"
```

Do not add separate Black, isort, or Flake8 dependencies unless Ruff proves insufficient for a concrete need.

Long string literals, UI copy, and documentation examples should be wrapped or extracted rather than raising the global line length.

Do not enable `D` docstring rules globally during the MVP. Prefer meaningful docstrings on public modules and complex domain functions, but avoid boilerplate comments just to satisfy a linter.

The NSIDC example also includes scientific/data-package rules such as `NPY` and `PD`; do not enable them unless the project later adds NumPy or pandas.

Pre-commit may be added later for local Git hooks, but Poe remains the official project task runner.

## Pytest And Coverage

Use `pyproject.toml` for pytest and coverage configuration.

Recommended baseline:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-ra --strict-markers --strict-config"
markers = [
  "unit: fast deterministic tests for isolated logic",
  "property: property-based tests using generated inputs",
  "integration: tests that combine multiple game systems",
  "browser: web/canvas tests for the future browser target",
  "slow: tests that are too slow for the default local loop",
]

[tool.coverage.run]
branch = true
source = ["mendels_greenhouse"]
omit = [
  "tests/*",
]

[tool.coverage.report]
show_missing = true
skip_covered = true
fail_under = 0
exclude_lines = [
  "pragma: no cover",
  "if TYPE_CHECKING:",
  "if __name__ == .__main__.:",
]
```

Set `fail_under` above `0` only after the first meaningful implementation tests exist.

## I18n Automation

Use Babel's `pybabel` commands through Poe tasks.

The project should not start with a custom Python translation compiler script. Prefer the ecosystem tooling first:

- `poe i18n-extract` extracts messages.
- `poe i18n-update` updates locale catalogs.
- `poe i18n-compile` compiles `.po` files into `.mo` files.

If Babel commands become too repetitive or error-prone, then a small wrapper script may be introduced later, but it must call Babel rather than reimplement message catalog handling.

## Refactoring And Code Quality

Use Refactoring.Guru as a reference when implementation quality starts to drift.

The default response to low-quality code is:

1. Add or preserve tests for the current behavior.
2. Apply small refactorings.
3. Run the relevant Poe task.
4. Avoid changing gameplay rules during refactoring.

Useful refactoring triggers:

- Long methods in scene update/draw code.
- Large scene classes that mix input, state transitions, and drawing.
- Repeated conditional logic for contract or analyzer behavior.
- Primitive obsession around genotype strings, color indexes, or screen names.
- Duplicated UI drawing code.

Preferred corrective patterns:

- Extract Method for long `update()` or `draw()` blocks.
- Extract Class for oversized scenes or services.
- State for scene transitions and screen-specific behavior.
- Strategy for contract validation and analyzer behaviors.
- Command for UI actions that mutate game state.

Patterns should be introduced only when they remove real complexity.

## Readiness Assessment Resolution

The repository contains a non-source-of-truth readiness assessment file with several questions. The official answers are:

| Topic | Decision |
| ----- | -------- |
| Visual assets | Use `.pyxres` as the production asset source; code-generated placeholders are acceptable only for early bootstrapping. |
| MVP save data | Use one autosave slot with local versioned JSON in Pyxel's user data directory. |
| Screen architecture | Use scene management with `Scene` and `SceneManager`. |
| Starting credits | Start with `0` credits unless balance testing proves the tutorial needs a small buffer. |
| I18n automation | Use Babel through Poe tasks. |
| Pyxel colors | Use Pyxel native color constants mapped through human-readable classes. |
| Project initialization | Scaffold with Poetry, Python 3.11, and configure dependencies/tasks before gameplay implementation. |
| First MVP screens | Implement Main Game, Greenhouse, Contracts, and Collection first. |
| Tutorial delivery | Use the first contract as a guided tutorial with minimal popups. |
| Early distribution | Run the Python entrypoint directly for development; use Docker to package `.pyxapp`, export HTML with `app2html`, and serve it with Python's standard `http.server` for the current web build. |
| Documentation site | Postpone until after the first release. |

## References

- [Ruff on PyPI](https://pypi.org/project/ruff/)
- [Adopting pre-commit and Ruff at NSIDC](https://nsidc.github.io/NSIDC-Technical-Blog/posts/pre-commit-and-ruff/index.html)
- [Poe the Poet on PyPI](https://pypi.org/project/poethepoet/)
- [Babel message catalog documentation](https://babel.pocoo.org/en/latest/messages.html)
- [Refactoring.Guru Refactoring](https://refactoring.guru/pt-br/refactoring)
- [Refactoring.Guru Design Patterns](https://refactoring.guru/pt-br/design-patterns)
