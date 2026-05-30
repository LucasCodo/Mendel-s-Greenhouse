---
title: Decisions
tags:
  - agent-memory/decision
type: decision
project: mendels-greenhouse
status: active
updated: 2026-05-30
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

Runtime assets belong inside the package under `mendels_greenhouse/assets/`.

Use Pyxel's native `.pyxres` format, with primary resource file `mendels_greenhouse/assets/mendels_greenhouse.pyxres`.

Target internal game resolution is `256 x 144`; the browser view should fill the page, preserve aspect ratio, keep pixel art crisp, and provide fullscreen.

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

Future packaging follows Pyxel's native flow: run the main Python entrypoint directly during development and package as `.pyxapp` for distribution. Do not export HTML during the MVP implementation phase.

Future NiceGUI integration should wrap the selected Pyxel delivery artifact after the first release. NiceGUI will initially use simple username and password authentication for accounts.

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

Use Python 3.11 as the local development baseline. The project metadata should use `>=3.11,<4.0`. The first MVP screen set is Main Game, Greenhouse, Contracts, and Collection. Tutorial delivery happens through the first contract with minimal popups.

Do not build a documentation site now; revisit GitHub Pages/MkDocs after the first release.
