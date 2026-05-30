# Project Structure

## Purpose

This document defines the initial project structure for implementing Mendel's Greenhouse with Poetry and Pyxel.

## Poetry Scaffolding

When creating the implementation project from scratch, use Poetry with the flat layout:

```powershell
poetry new --flat --name mendels_greenhouse --readme md --license MIT --python ">=3.11,<4.0" --dependency pyxel --no-interaction "Mendel's Greenhouse"
```

Rationale:

- `--flat` keeps the package layout simple for a small game.
- `--name mendels_greenhouse` creates a Python-safe package name.
- `--readme md` matches the repository documentation style.
- `--license MIT` preserves the current project license.
- `--python ">=3.11,<4.0"` matches the local development baseline and Pyxel compatibility.
- `--dependency pyxel` records the selected game engine.
- `--no-interaction` makes the scaffold command repeatable for agents.

If the command is run inside an already initialized repository, verify the generated files before overwriting existing documentation.

After scaffolding, add development dependencies:

```powershell
poetry add --group dev pytest pytest-cov hypothesis ruff poethepoet Babel
```

Use Poe tasks for automation. Do not use Taskipy.

## Package Layout

The game package should own the runtime code, game assets, and localization catalogs.

Recommended structure:

```text
mendels_greenhouse/
|-- __init__.py
|-- __main__.py
|-- app.py
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
mendels_greenhouse/assets/
```

Primary resource file:

```text
mendels_greenhouse/assets/mendels_greenhouse.pyxres
```

Do not place runtime assets only at repository root. Keeping assets inside the package makes imports, packaging, and future web delivery easier to reason about.

## Localization Location

Localization catalogs must live inside the game package:

```text
mendels_greenhouse/locale/
```

Rules are defined in [localization.md](localization.md).

## Save Location

Future local save data should use versioned JSON documents stored under Pyxel's user data directory.

Save format and future NiceGUI boundaries are defined in [future-platform.md](future-platform.md).

## Entrypoint

The package should be runnable as a module:

```powershell
poetry run python -m mendels_greenhouse
```

`__main__.py` should call the game startup entrypoint.

## Test Location

Automated tests must live in the repository-level `tests/` directory.

Testing rules are defined in [testing.md](testing.md).

## Automation

Development automation uses Poe the Poet.

Task definitions are documented in [development-tooling.md](development-tooling.md).

## Current Scope

Implement the game first. NiceGUI account and save integration remains future scope and should not shape the initial package structure beyond keeping game code modular.
