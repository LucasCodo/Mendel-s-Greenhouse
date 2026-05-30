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
- `--python ">=3.11,<4.0"` defines a modern Python range.
- `--dependency pyxel` records the selected game engine.
- `--no-interaction` makes the scaffold command repeatable for agents.

If the command is run inside an already initialized repository, verify the generated files before overwriting existing documentation.

## Package Layout

The game package should own the runtime code and game assets.

Recommended structure:

```text
mendels_greenhouse/
├── __init__.py
├── __main__.py
├── app.py
├── assets/
│   ├── mendels_greenhouse.pyxres
│   └── README.md
├── core/
│   ├── genetics.py
│   ├── contracts.py
│   ├── greenhouse.py
│   └── progression.py
├── scenes/
│   ├── main_game.py
│   ├── contracts.py
│   ├── greenhouse.py
│   ├── analyzer.py
│   └── collection.py
└── ui/
    ├── components.py
    ├── layout.py
    └── palette.py
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

## Entrypoint

The package should be runnable as a module:

```powershell
poetry run python -m mendels_greenhouse
```

`__main__.py` should call the game startup entrypoint.

## Current Scope

Implement the game first. NiceGUI account and save integration remains future scope and should not shape the initial package structure beyond keeping game code modular.
