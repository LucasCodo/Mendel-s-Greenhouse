---
title: Open Questions
tags:
  - agent-memory/question
type: question
project: mendels-greenhouse
status: active
updated: 2026-05-30
---

# Open Questions

## Still Open

- Hosting provider.
- Database technology.
- Final NiceGUI routing structure.
- Exact save synchronization protocol between NiceGUI and the Pyxel game.

## Resolved On 2026-05-30

### Engine And Art Direction

The game will use Pyxel as its engine and pixel art as its visual style.

### Platform Direction

Mendel's Greenhouse is intended to be a web game. For now, implementation focuses only on the game. A future NiceGUI layer is planned for user accounts and save management.

### Initial Localization

The game must support English and Brazilian Portuguese from the initial implementation. Use Python `gettext` for runtime translations and Babel tooling for extraction/catalog management.

### Project Structure And Asset Direction

The implementation should use Poetry flat layout with package name `mendels_greenhouse`. Runtime assets live inside `mendels_greenhouse/assets/` and use Pyxel's native `.pyxres` format.

The game targets internal resolution `640 x 360`, scaled to fill the browser page with crisp pixel art and a fullscreen option.

### First Playable Prototype Scope

The first playable prototype validates the main loop:

1. The player has two parent plants.
2. The player selects two plants for crossbreeding.
3. One offspring batch is generated.
4. Offspring appear on the production conveyor.
5. The player sees produced phenotypes.
6. The system automatically checks contract progress.
7. The player receives rewards.
8. The player can store useful offspring for future crosses.

MVP content:

- Mendel Pea only.
- 2 independent genes: `A/a` and `B/b`.
- Genetic Analyzer level 1 only.
- Phenotypic contracts only.
- Small greenhouse.
- Functional collection.
- Functional progression.

### Contract Consumption

Delivery contracts consume delivered plants. Statistical contracts validate the generated batch and do not consume plants automatically.

### Plant Sale Value

Plant sale values should be intentionally low. Sale exists to prevent waste, not to become the main income source.

Recommended value:

- Contract value: 100%.
- Common sale: 5% to 10%.
- Discard: 0%.

### Genetic Analyzer Use Cost

The genetic analyzer has unlimited use and no per-use cost, wait time, or energy cost. Progression is based on analyzer levels only.

### Final Species Naming Scheme

Species progression:

| Species | Genes | Objective |
| ------- | ----: | --------- |
| Mendel Pea | 2 | Tutorial |
| Snapdragon | 3 | Intermediate |
| Corn | 4 | Full Mendel's Second Law |
| Tomato | 5 | Advanced planning |
| Orchid | 6 | Endgame and collection |

### Future Platform Decisions

Future save data will use versioned JSON. Local Pyxel saves should live under Pyxel's user data directory. Pyxel `.pyxres` remains for resources, not player saves.

Future packaging follows Pyxel's native flow: run the main Python entrypoint directly during development and package as `.pyxapp` for distribution. The current web build exports the `.pyxapp` with Pyxel `app2html`, hardens the generated HTML wrapper, and serves the generated HTML through Docker.

Future code architecture should keep core gameplay logic independent from Pyxel rendering and future NiceGUI infrastructure.

Future NiceGUI integration should replace or wrap the current Docker/app2html delivery artifact when account and save orchestration enter scope. NiceGUI will initially use simple username and password authentication for accounts.

### Implementation Readiness

Use Poe the Poet for automation, not Taskipy.

Initial development dependencies are `pytest`, `pytest-cov`, `hypothesis`, `ruff`, `poethepoet`, and `Babel`. Add `pytest-playwright` later only when a runnable web build exists.

Configure Ruff to follow PEP 8 line length with `line-length = 79`.

Ruff lint should include PEP 8 style and naming checks (`E`, `W`, `N`), core correctness checks (`F`), import sorting (`I`), modernization (`UP`), and pragmatic quality rules (`B`, `SIM`, `C4`, `RET`, `PT`, `PTH`, `RUF`).

Extend Ruff with the relevant NSIDC-inspired rules `ARG`, `EM`, `ERA`, `EXE`, `ISC`, `PIE`, `PL`, `T20`, and `YTT`. Do not enable scientific/data rules such as `NPY` or `PD` unless those dependencies are added later.

Configure pytest and coverage in `pyproject.toml`; keep coverage `fail_under = 0` until meaningful implementation tests exist.

Use Babel through Poe tasks for i18n extraction, update, and compile.

Use Pyxel palette indexes through human-readable enums and central UI color mappings.

Use scene management for screen architecture. The MVP starts with `0` credits, one autosave slot using local versioned JSON saves, and `.pyxres` as the production asset source.

Use Python 3.11 as the local development baseline. The project metadata should use `>=3.11,<4.0`. The first MVP screen set is Main Game, Greenhouse, Contracts, and Collection. Tutorial delivery happens through the first contract with minimal popups.

Do not build a documentation site now; revisit GitHub Pages/MkDocs after the first release.
