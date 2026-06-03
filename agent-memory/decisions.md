---
title: Decisions
tags:
  - agent-memory/decision
type: decision
project: mendels-greenhouse
status: active
updated: 2026-05-31
---

# Decisions

## 2026-05-30: Specs Are Source Of Truth

Detailed game rules belong in `specs/`. Root documentation should stay high-level and point humans and agents to the specs.

## 2026-05-30: Official Genetic Analyzer Progression

The official analyzer progression has exactly 4 levels:

1. Phenotypic Observation
2. Genetic Sequencing
3. Probabilistic Analysis
4. Genetic Simulator

The learning progression is:

```text
Phenotype
->
Genotype
->
Probability
->
Genetic Planning
```

## 2026-05-30: Artifact Naming

Use simple document names. Detailed artifacts live under `specs/`, such as `specs/GDD.md` and `specs/GBD.md`, rather than repeating the project name in filenames.

## 2026-05-30: Keep Agent Memory

Keep `agent-memory/` in the repository as Obsidian-friendly durable memory for agents. It records stable decisions, project state, validated commands, and open questions.

## 2026-05-30: Keep MIT License And .aiignore

The repository uses the MIT License. Keep `LICENSE` as the existing MIT license file.

Keep `.aiignore` in the repository to hide local vault settings, secrets, generated outputs, and dependency folders from agent context.

## 2026-05-30: UI Specs Location

Detailed UI/UX documentation lives in `specs/ui/`. The older `specs/UI_FLOW.md` and `specs/SCREEN_SPEC.md` files are high-level pointers to the detailed UI specs.

## 2026-05-30: MVP Scope And Contract Consumption

The first playable prototype should validate the core loop using Mendel Pea only, 2 independent genes, analyzer level 1, phenotypic contracts, limited greenhouse space, collection, and progression.

Delivery contracts consume delivered plants. Statistical contracts validate the generated batch and do not consume plants automatically.

## 2026-05-30: Analyzer Use Is Free

The genetic analyzer has unlimited use and no per-use credit, time, or energy cost. Progression comes from analyzer levels, not usage friction.

## 2026-05-30: Plant Sale Value

Plant sale values should stay low: common sale should be roughly 5% to 10% of comparable contract value. Selling exists to avoid waste and free storage, not as the main source of income.

## 2026-05-30: Species Naming Progression

The final species naming scheme is:

1. Mendel Pea - 2 genes.
2. Snapdragon - 3 genes.
3. Corn - 4 genes.
4. Tomato - 5 genes.
5. Orchid - 6 genes.

## 2026-05-30: Specs Directory Grouping

Mechanics are grouped under `specs/mechanics/` to make Obsidian navigation and agent context loading more focused.

Related grouping:

- `specs/mechanics/` for gameplay systems.
- `specs/content/` for species, genes, alleles, and phenotypes.
- `specs/education/` for learning objectives.
- `specs/ui/` for interface, assets, and accessibility.

## 2026-05-30: Engine And Art Direction

Mendel's Greenhouse will use Pyxel as its game engine and pixel art as its visual style.

Implementation-specific details such as persistence, packaging, and code architecture remain open until documented in `specs/technical/`.

## 2026-05-30: Web Target And Future NiceGUI Layer

Mendel's Greenhouse is intended to be a web game.

Current scope is only the game implementation. NiceGUI is planned for a future web application layer that manages user accounts and saves.

Do not implement account management, authentication, or hosted save management in the MVP unless future specs explicitly change scope.

## 2026-05-30: Poetry Flat Package And Pyxel Assets

The implementation should be scaffolded with Poetry flat layout using package name `mendels_greenhouse`.

Runtime assets belong inside the game package under `game/mendels_greenhouse/assets/`.

Use Pyxel's native `.pyxres` format, with primary resource file `game/mendels_greenhouse/assets/mendels_greenhouse.pyxres`.

Target internal game resolution is `640 x 360`; the browser view should fill the page, preserve aspect ratio, keep pixel art crisp, and provide fullscreen.

## 2026-05-31: 16:9 Modern Pixel-Art Canvas

The main runtime canvas was raised from the earlier compact prototype target to
`640 x 360`. This preserves a reference-friendly 16:9 composition, gives more
space for modern pixel-art UI density, and still keeps Pyxel asset work
manageable for the MVP.

## 2026-05-31: Expanded Project Palette

The project no longer treats Pyxel's default 16-color palette as a hard visual
limit. Runtime code uses a 32-color named palette to better match the reference
image, reduce orange dominance, and reserve distinct phenotype colors for
future species.

## 2026-05-31: Cozy Scientific Greenhouse Palette

The active 32-color palette should read as a cozy scientific greenhouse rather
than a near-default Pyxel palette. It uses deep slate UI backgrounds, aged paper
panels, warmer less-red wood, brighter botanical greens, gold/yellow phenotype
colors, blue scientific accents, and pink-red danger states. Keep
`specs/ui/color-palette.md`, `mendels_greenhouse/ui/palette.py`, and generated
`.pyxres` assets synchronized when changing these colors.

## 2026-05-31: Mendel Pea Pod Asset Direction

MVP Mendel Pea sprites should appear as vertical or diagonal pea pods, not
horizontal pods, full plants, or potted plants. The pod stays green across
variants, while the visible peas inside the pod carry the seed color and
texture traits. Keep pod colors and seed colors as separate code parameters so
recoloring peas does not recolor the pod.

Sprite blits use `colkey=0`, so palette index `0` is transparent in resource
sprites. Use a non-zero outline color such as `SPRITE_OUTLINE` for visible pod
and seed contours.

Top navigation icons should be stored as 64 x 64 `.pyxres` sprites. HUD frames,
panel backgrounds, button surfaces, and Germination Bed panel shapes should be
generated in runtime code while the layout is still evolving.

## 2026-05-31: Punnett Square Analyzer Behavior

The Genetic Analyzer should expose a read-only Punnett square at level 3 for
selected parent pairs, using the same gamete/genotype logic as breeding
probabilities. Level 4 turns the Punnett square into an interactive simulator
and comparison tool with target highlighting.

## 2026-06-02: Germination Bed Replaces Conveyor

The main offspring layout should abandon the industrial conveyor metaphor and
use a Germination Bed. Generated offspring appear as planted cells with seed,
seedling, and adult phenotype states. This better matches the greenhouse
fantasy, makes Mendelian proportions readable as visual groups, supports direct
specimen selection, and gives contracts a clear match-highlight surface.

The Punnett square remains the analyzer explanation for why outcomes are
possible. The Germination Bed shows the current or representative lot. The two
views must use the same gamete/genotype logic, but the bed is not required to
match Punnett cell positions.

## 2026-05-30: Premium Pixel-Art Interface Target

The UI quality target is a polished pixel-art management screen with dense but
readable information: logo plaque, resource counters, contract panel, parent
cards, probability/Punnett panel, large Germination Bed, bottom stats/help
panels, and icon navigation.

Use larger source sprites for important plant views:

- Germination Bed specimens: prefer `24 x 24` or `32 x 32`.
- Parent card plants: prefer `96 x 96` or `128 x 128`.
- Analyzer and discovery previews: prefer `128 x 128`, maximum `256 x 256`.

## 2026-05-30: AI Contribution Governance

Meaningful AI assistance must be disclosed with an `Assisted-by:` trailer or PR metadata.

AI tools must not be listed as authors, signers, reviewers, approvers, or DCO signers. Human contributors remain responsible for reviewing, understanding, testing, and licensing their contributions.

## 2026-05-30: Initial Localization

Mendel's Greenhouse must support English and Brazilian Portuguese from the initial implementation.

Use Python `gettext` for runtime translations and Babel tooling for extraction/catalog management. Keep localization files inside the game package under `mendels_greenhouse/locale/`.

## 2026-05-30: Testing Strategy

Use `pytest` as the primary automated testing framework.

Core gameplay logic should be testable without launching Pyxel windows. Use `hypothesis` for genetic/property invariants and `pytest-cov` for coverage. Add `pytest-playwright` later only when a runnable web build exists.

## 2026-05-30: Future Platform Decisions

Future save data will use versioned JSON. Local Pyxel saves should live under Pyxel's user data directory. Pyxel `.pyxres` remains for resources, not player saves.

Future packaging follows Pyxel's native flow: run the main Python entrypoint directly during development and package as `.pyxapp` for distribution. The current web build packages the game as `.pyxapp`, exports HTML with Pyxel `app2html`, hardens the generated HTML wrapper with a CSP, and serves it from Docker with `python -m http.server`.

Future NiceGUI integration should replace or wrap the current Docker/app2html delivery artifact when account and save orchestration enter scope. NiceGUI will initially use simple username and password authentication for accounts.

## 2026-05-31: Pyxel Web CSP For Wallet Extensions

The Pyxel web game does not use wallet, Web3, or blockchain APIs. The generated
`app2html` wrapper should be post-processed with a restrictive Content Security
Policy so browser wallet extension scripts such as MetaMask's in-page script
cannot connect inside the game page. Keep `game/tools/harden_web_html.py` in
the Docker build path and verify the game still loads after CSP changes.

## 2026-05-30: Implementation Readiness

Use Poe the Poet for automation, not Taskipy.

Initial development dependencies are `pytest`, `pytest-cov`, `hypothesis`, `ruff`, `poethepoet`, and `Babel`. Add `pytest-playwright` later only when a runnable web build exists.

Configure Ruff to follow PEP 8 line length with `line-length = 79`.

Ruff lint should include PEP 8 style and naming checks (`E`, `W`, `N`), core correctness checks (`F`), import sorting (`I`), modernization (`UP`), and pragmatic quality rules (`B`, `SIM`, `C4`, `RET`, `PT`, `PTH`, `RUF`).

Extend Ruff with the relevant NSIDC-inspired rules `ARG`, `EM`, `ERA`, `EXE`, `ISC`, `PIE`, `PL`, `T20`, and `YTT`. Do not enable scientific/data rules such as `NPY` or `PD` unless those dependencies are added later.

Configure pytest and coverage in `pyproject.toml`; keep coverage `fail_under = 0` until meaningful implementation tests exist.

Use Babel through Poe tasks for i18n extraction, update, and compile.

Use Pyxel palette indexes through human-readable enums and central UI color mappings.

Use scene management for screen architecture. The MVP starts with `0` credits, one autosave slot using local versioned JSON saves, and `.pyxres` as the production asset source.

## 2026-05-30: Pyxel Agent Tooling

`pyxel-mcp` is approved as a development dependency for the `game/` package.

`pyxel-skill` is approved as a local Codex skill for Pyxel implementation guidance, but project specs remain the source of truth when tool defaults conflict.

Pyxel MCP/skill output must support implementation and visual verification; it does not replace pytest or spec updates.

## 2026-05-31: Modern Pixel-Art Direction

The visual target is modern indie pixel art, not bare retro placeholders.

Reference mix:

- Stardew Valley for warm vegetation and farming readability.
- Fields of Mistria for soft modern pixel art and approachable UI.
- Potion Permit for laboratory interiors, lighting, and dense cozy spaces.
- Sun Haven for vibrant analyzer/discovery effects.
- Pokemon GBA for collection/catalog readability.
- Professor Layton for friendly contract/puzzle presentation.
- Papers, Please for readable request/document UI, adapted to a warm tone.

Do not copy assets or compositions from references. Use them only to guide warmth, polish, readability, and UI density.

## 2026-05-31: Pyxel MCP For Assets And Audio

Use `pyxel-mcp` for visual/audio verification when exposed to the session:

- Screens and layout: `run_and_capture`, `inspect_layout`, `inspect_palette`.
- Sprites and image banks: `inspect_sprite`, `inspect_bank`.
- Tilemaps/backgrounds: `inspect_tilemap`.
- Animation: `capture_frames`, `inspect_animation`, `compare_frames`.
- Music and sound effects: `render_audio`.

Production visual/audio resources belong in `game/mendels_greenhouse/assets/mendels_greenhouse.pyxres`.

## 2026-05-31: Mouse-First Interaction

Mendel's Greenhouse is a mouse-first game.

The player should be able to complete the main loop by clicking UI controls,
plant cards, greenhouse slots, Germination Bed specimens, menus, and bed
controls.

Keyboard support is still required for accessibility and power users. Every core mouse action must have a keyboard-reachable equivalent through focus, activation, shortcuts, or explicit controls.

Use Python 3.11 as the local development baseline. The project metadata should use `>=3.11,<4.0`. The first MVP screen set is Main Game, Greenhouse, Contracts, and Collection. Tutorial delivery happens through the first contract with minimal popups.

Do not build a documentation site now; revisit GitHub Pages/MkDocs after the first release.

## 2026-05-31: Specimen Generations And Knowledge Tree

Collection specimen entries record lineage generation labels. Starting or
directly acquired plants display as `P0`; offspring display as `F1`, `F2`, and
later filial generations based on one more than the highest parent generation
depth.

Analyzer level 2 exposes allele breakdowns alongside genotype information.
Analyzer level 3 may show the `9:3:3:1` ratio only for valid independently
assorting, complete-dominance dihybrid crosses such as `AaBb x AaBb`.

The Progression Screen is specified as a Knowledge Tree that stores learned
concepts and shows concept details through hover, focus, or selection without
revealing analyzer-locked information early.
