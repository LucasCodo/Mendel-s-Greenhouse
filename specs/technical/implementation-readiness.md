# Implementation Readiness Decisions

## Purpose

This document closes the practical implementation questions raised before starting the first playable prototype.

It is based on the current specs, the repository readiness assessment, Pyxel documentation, Python ecosystem tooling, and the project owner's latest decisions.

## Readiness Assessment Notes

The temporary readiness checklist has been resolved and removed.

Use this document as the official readiness source of truth.

## Decisions

### Visual Asset Strategy

Production runtime assets must use Pyxel's `.pyxres` format.

Rules:

- The primary resource file remains `mendels_greenhouse/assets/mendels_greenhouse.pyxres`.
- The MVP may generate simple placeholder sprites in code only for Mendel Pea plants and minimal UI icons.
- Placeholder generation must not become the long-term asset pipeline.
- When a `.pyxres` asset exists, runtime code should load it instead of redrawing equivalent sprites procedurally.

### Save Persistence For MVP

The MVP should support local persistence using versioned JSON.

Rules:

- Save files live under Pyxel's user data directory.
- The MVP uses one autosave slot.
- Save data uses explicit schema versions.
- Game state must be serializable without Pyxel objects.
- NiceGUI-hosted saves remain future scope.

### Scene Architecture

Use scene management.

Required concepts:

- `Scene` protocol or abstract base with `update()` and `draw()`.
- `SceneManager` responsible for switching scenes.
- Each screen owns its own scene class.
- Scenes call services for game mutations instead of embedding core rules directly.

Avoid one large `App` class with screen-wide `if/else` branches.

### First MVP Screen Set

The first implementation slice includes:

- Main Game.
- Greenhouse.
- Contracts.
- Collection.

Other screens remain future slices unless required to complete the core loop.

### Tutorial Delivery

Use the first contract as a guided tutorial with minimal popups.

Tutorial guidance should stay contextual and should not interrupt repeated core actions unnecessarily.

### Starting Credits

The MVP starts the player with `0` credits.

Rationale:

- It reinforces the first tutorial contract as the first economic action.
- It prevents early purchases from bypassing the intended first learning loop.
- It keeps the economy simple for initial balance testing.

If playtesting shows that `0` credits blocks comprehension, the value may be revisited in the GBD.

### I18n Compilation

Use Babel through Poe tasks.

Do not create a custom `scripts/compile_locales.py` at the start.

Required tasks:

- `poe i18n-extract`
- `poe i18n-update`
- `poe i18n-compile`

### Pyxel Palette Mapping

Use the project palette indexes through human-readable classes.

Rules:

- Do not scatter raw integer color indexes across UI code.
- Keep design-system color roles mapped to named indexes in one place.
- Keep `PROJECT_PALETTE`, `PyxelColor`, and `specs/ui/color-palette.md`
  synchronized.
- Do not assume Pyxel's default 16-color palette is the project visual limit.

Recommended module:

```text
mendels_greenhouse/ui/palette.py
```

Recommended shape:

```python
PROJECT_PALETTE = [
    0x111827,  # 0 ink shadow
    0x1E293B,  # 1 deep glass navy
    # ...
]


class PyxelColor:
    GREENHOUSE_BG = 1
    UI_DARK = 0
    PARCHMENT = 15
    ACTION = 11
    PROGRESS = 30
```

Names may be adjusted after checking the final Pyxel palette, but the principle
is fixed.

### Development Dependencies

Initial development dependencies:

- `pytest`
- `pytest-cov`
- `hypothesis`
- `ruff`
- `poethepoet`
- `Babel`
- `pyxel-mcp`

Future-only:

- `pytest-playwright`

Do not add `taskipy`.

`pyxel-mcp` is an implementation aid for Pyxel validation and screenshots. It does not replace pytest or the source-of-truth specs.

### Python Version

Use Python `3.11` as the local development baseline.

The project metadata should use:

```text
>=3.11,<4.0
```

### Packaging And Execution Timing

Approved execution/distribution options for the early implementation:

- Run the main Python entrypoint directly with `python game\main.py`
  from the repository root.
- Run the same launcher with `pyxel run game\main.py` from the
  repository root.
- Package the game as a Pyxel `.pyxapp`.
- Export the staged `.pyxapp` with Pyxel `app2html` for the current Docker
  web build.
- Serve the generated HTML without rewriting it.

Documentation-site work remains postponed until after the first release.

## Acceptance Criteria

- The implementation can start without choosing between competing architecture options.
- Dev commands are automated with Poe.
- Localization compile workflow uses Babel.
- Color indexes are readable and centralized.
- The first MVP has a clear save strategy.
- Future refactoring guidance is documented before code quality degrades.
- No unresolved readiness checklist remains outside the official specs.
