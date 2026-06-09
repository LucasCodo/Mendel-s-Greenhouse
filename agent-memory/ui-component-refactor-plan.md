---
title: UI Component Refactor Plan
tags:
  - agent-memory/todo
  - ui/components
type: session-log
project: mendels-greenhouse
status: resolved
updated: 2026-06-09
---

# UI Component Refactor Plan

## Context

Runtime UI drawing is currently concentrated in
`game/mendels_greenhouse/scenes/main_game.py`, with smaller helper modules under
`game/mendels_greenhouse/ui/game_components/`. The UI specs already define
component maps for Main Game, Garden, and Collection scenes, so extraction
should follow those documented boundaries instead of creating a separate
taxonomy.

Relevant specs:

- [[specs/ui/component-library|Component Library]]
- [[specs/ui/scenes/main-game/component-map|Main Game Component Map]]
- [[specs/ui/scenes/garden/component-map|Garden Component Map]]
- [[specs/ui/scenes/collection/component-map|Collection Component Map]]
- [[specs/technical/project-structure|Project Structure]]

## Goals

- Reduce merge conflicts by moving large screen-specific drawing blocks out of
  `MainGameScene`.
- Keep gameplay rules, state mutation, and rendering concerns separated.
- Make each visual component easier to test, screenshot, and refine
  independently.
- Preserve analyzer-level information visibility and localization rules.
- Avoid introducing new gameplay rules during UI extraction.

## Non-Goals

- Do not redesign gameplay, progression, contracts, genes, alleles, species, or
  analyzer behavior.
- Do not introduce NiceGUI, persistence architecture, authentication, or
  packaging changes.
- Do not move business logic into UI components.
- Do not extract every method in one large change.

## Proposed Structure

Create runtime Pyxel UI modules under:

```text
game/mendels_greenhouse/ui/game_components/
|-- layout.py
|-- main_game/
|   |-- __init__.py
|   |-- top_bar.py
|   |-- navigation_rail.py
|   |-- greenhouse_background.py
|   |-- contract_banner.py
|   |-- genetic_analyzer_panel.py
|   |-- parent_cross_panel.py
|   |-- germination_bed_panel.py
|   |-- specimen_detail_panel.py
|   `-- help_panel.py
|-- garden/
|   |-- __init__.py
|   |-- garden_background.py
|   |-- garden_top_bar.py
|   |-- garden_slot_grid.py
|   `-- selected_plant_panel.py
`-- collection/
    |-- __init__.py
    |-- collection_header.py
    |-- collection_tabs.py
    |-- collection_entry_grid.py
    `-- entry_detail_panel.py
```

Each component should expose small functions or classes with explicit inputs.
Prefer stateless drawing functions first; add component classes only when the
component owns local animation or interaction state.

## Component Contract

Components should receive:

- A `Rect` or explicit coordinates.
- Already-filtered display data.
- The active language/translator callback when text is needed.
- The active analyzer level only when the component must choose a visible state.
- Existing palette names from `mendels_greenhouse.ui.palette`.

Components should return:

- Draw-only components return `None`.
- Interactive components may return a small action value, such as selected slot,
  selected tab, or button action.

Components must not:

- Mutate `GameState` directly.
- Spend credits, generate offspring, claim contracts, or unlock progression.
- Reveal hidden genotype/probability data before the relevant analyzer level.
- Use raw Pyxel color indexes where named palette constants exist.

## Extraction Order

1. Extract low-risk shared layout and drawing primitives.
   Move repeated frame, title, counter, button, and text wrapping helpers into
   `ui/components.py` or `ui/game_components/layout.py` only when reuse is clear.

2. Extract passive Main Game visual surfaces.
   Start with `GreenhouseBackground`, `TopBar`, and `RightNavigationRail`.
   These have visible impact but limited gameplay coupling.

3. Extract Main Game data panels.
   Move `ContractBanner`, `ParentCrossPanel`, `GeneticAnalyzerPanel`, and
   `SpecimenDetailPanel` after defining display DTOs or dictionaries in
   `MainGameScene`.

4. Extract `GerminationBed`.
   Keep geometry helpers close to `germination_bed.py`, but move rendering and
   selection-hit testing behind a narrow API. This is higher risk because it is
   tied to offspring reveal, harvest actions, and contract highlights.

5. Extract secondary screens one at a time.
   Recommended order: Shop, Garden, Collection, Contracts, Knowledge, Settings.
   Garden and Collection should follow their existing component maps.

6. Convert root prototypes into references or remove them after parity.
   `experiment_analyzer.py` and `experiment_analyzer_panel.py` are useful visual
   references, but runtime code should live inside the game package.

## Verification For Each Step

- Run targeted pytest tests for affected pure helpers when available.
- Run `poetry run poe check` when the change touches shared runtime code.
- For Pyxel visual changes, use `pyxel-mcp` screenshots and inspections when
  exposed; otherwise run a direct Pyxel smoke check and report the fallback.
- Manually verify analyzer-level visibility for levels 1 through 4 whenever
  analyzer, parent, specimen, or probability UI changes.

## Implemented Runtime Slices

Implemented on 2026-06-09:

- Added runtime component modules for Main Game, Collection, Garden, Contracts,
  Knowledge, Shop, Settings, and overlays under
  `game/mendels_greenhouse/ui/game_components/`.
- Reduced `MainGameScene` to state orchestration, update handling, data assembly,
  service calls, autosave, and thin draw delegation.
- Added component maps for runtime scenes that did not yet have scene-level
  component specs: Contracts, Knowledge, Shop, Settings, and Runtime Overlays.
- Preserved current gameplay behavior and avoided changing rules, economy,
  progression, contracts, species, or analyzer visibility thresholds.

Validation:

- `poetry run poe check`: passed with 48 tests.
- `mcp__pyxel.validate_script` on `game/mendels_greenhouse/main.py`: completed
  with the existing warning that the shell `draw()` does not call `pyxel.cls()`
  directly.

Known verification limit:

- Pyxel MCP screenshot/layout capture timed out earlier against the normal game
  loop, so this refactor was verified by project checks and script validation
  rather than by a captured visual diff.
