# Project Structure

## Purpose

This document defines the initial project structure for implementing Mendel's Greenhouse with Poetry and Pyxel.

## Poetry Scaffolding

When creating the game package from scratch, use Poetry with the flat layout inside a dedicated `game/` directory:

```powershell
poetry new --flat --name mendels_greenhouse --readme md --license MIT --python ">=3.11,<4.0" --dependency pyxel --no-interaction game
```

Rationale:

- `--flat` keeps the package layout simple for a small game.
- `--name mendels_greenhouse` creates a Python-safe package name.
- `game/` keeps the Pyxel game package separate from the future NiceGUI site package.
- `--readme md` matches the repository documentation style.
- `--license MIT` preserves the current project license.
- `--python ">=3.11,<4.0"` matches the local development baseline and Pyxel compatibility.
- `--dependency pyxel` records the selected game engine.
- `--no-interaction` makes the scaffold command repeatable for agents.

Do not run `poetry init` at the repository root for the game package. The root remains documentation and repository governance space, while implementation packages live in dedicated directories.

After scaffolding, add development dependencies:

```powershell
poetry add --group dev pytest pytest-cov hypothesis ruff poethepoet Babel pyxel-mcp
```

Use Poe tasks for automation. Do not use Taskipy.

Local bootstrap note:

- If `poetry install` fails because local HTTPS inspection prevents Poetry from validating `files.pythonhosted.org`, keep the first `pyproject.toml` installable with no external dependencies and reintroduce Pyxel/dev dependencies after the certificate chain is fixed.
- Do not solve this by committing machine-specific certificate bundles.

## Package Layout

The game package should own the runtime code, game assets, and localization catalogs.

Recommended structure:

```text
game/
|-- pyproject.toml
|-- poetry.lock
|-- README.md
|-- main.py
|-- mendels_greenhouse/
|-- __init__.py
|-- main.py
|-- assets/
|   |-- mendels_greenhouse.pyxres
|   `-- README.md
|-- locale/
|   |-- en/
|   |   `-- LC_MESSAGES/
|   `-- pt_BR/
|       `-- LC_MESSAGES/
|-- core/
|   |-- genetics.py
|   |-- contracts.py
|   |-- greenhouse.py
|   |-- collection.py
|   |-- progression.py
|   |-- save_data.py
|   `-- i18n.py
|-- state/
|   |-- game_state.py
|   |-- settings.py
|   `-- session.py
|-- services/
|   |-- breeding_service.py
|   |-- contract_service.py
|   |-- collection_service.py
|   `-- save_service.py
|-- scenes/
|   |-- main_game.py
|   |-- contracts.py
|   |-- greenhouse.py
|   |-- analyzer.py
|   `-- collection.py
`-- ui/
    |-- components.py
    |-- game_components/
    |   |-- __init__.py
    |   |-- contract_summary.py
    |   |-- germination_bed.py
    |   `-- plant_info.py
    |-- layout.py
    `-- palette.py
tests/
|-- conftest.py
|-- unit/
|-- property/
|-- integration/
`-- browser/
```

## Asset Location

All Pyxel-native assets must live inside the game package:

```text
game/mendels_greenhouse/assets/
```

Primary resource file:

```text
game/mendels_greenhouse/assets/mendels_greenhouse.pyxres
```

Do not place runtime assets only at repository root. Keeping assets inside the package makes imports, packaging, and future web delivery easier to reason about.

## Localization Location

Localization catalogs must live inside the game package:

```text
game/mendels_greenhouse/locale/
```

Rules are defined in [localization.md](localization.md).

## Save Location

Future local save data should use versioned JSON documents stored under Pyxel's user data directory.

Save format and future NiceGUI boundaries are defined in [future-platform.md](future-platform.md).

## Entrypoint

The game should be started from the root-level launcher:

```powershell
python game\main.py
```

Pyxel's runner can also execute the same launcher:

```powershell
pyxel run game\main.py
```

`game/main.py` calls the game startup entrypoint. Do not add
`mendels_greenhouse/__main__.py`; the package is not the CLI entrypoint.

## Test Location

Automated tests must live in the repository-level `tests/` directory.

Testing rules are defined in [testing.md](testing.md).

## Automation

Development automation uses Poe the Poet.

Task definitions are documented in [development-tooling.md](development-tooling.md).

## Current Scope

Implement the game first. NiceGUI account and save integration remains future scope and should not shape the initial package structure beyond keeping game code modular.

Gameplay-specific UI helper modules may live under
`mendels_greenhouse/ui/game_components/`. This package is intended for
component-by-component visual refinement of Pyxel UI surfaces while keeping core
gameplay rules independent from rendering code.
