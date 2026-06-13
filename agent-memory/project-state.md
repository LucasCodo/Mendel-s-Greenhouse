---
title: Project State
tags:
  - agent-memory/state
type: state
project: mendels-greenhouse
status: active
updated: 2026-06-13
---

# Project State

Mendel's Greenhouse is an early-stage educational game project about learning Mendelian genetics through plant crossbreeding, contracts, collection, and greenhouse management.

The repository is moving from documentation-first into an initial Pyxel game package. The approved game engine is Pyxel, the approved art direction is polished pixel art, and the intended platform is web. Current implementation scope is the game only. NiceGUI is planned later for accounts and save management.

Initial language support: English and Brazilian Portuguese.

Automated testing direction: pytest for the main test suite, Hypothesis for property-based genetics/contract invariants, pytest-cov for coverage, and pytest-playwright later for browser smoke tests once a web build exists.

Future platform direction: saves use versioned JSON, local development runs the Pyxel Python entrypoint, and the current web build packages `.pyxapp`, exports HTML with Pyxel `app2html`, hardens the generated wrapper with a CSP, and serves it through Docker with `python -m http.server`. NiceGUI integration is revisited later for account and save orchestration, and initial NiceGUI authentication uses username and password.

Implementation readiness direction: use Python 3.11, Poe for tasks, Ruff for lint/format with PEP 8 line length, Babel for i18n catalog automation, scene management for screens, Pyxel color enums for palette mapping, one autosave slot, and `0` starting credits for the MVP.

UI target: `640 x 360` internal Pyxel canvas, full-page/browser-scaled display, fullscreen option, and premium pixel-art management layout with rich framed panels and readable high-detail plant sprites.

Pyxel agent tooling: `pyxel-mcp` is installed as a game-package dev dependency, and a local `pyxel-skill` exists in Codex. MCP tools were not exposed through `tool_search` in the current session, so fallback validation used Poe/Ruff/pytest and direct Pyxel load checks.

Design direction: modern polished pixel art inspired by contemporary farming/life-sim and cozy laboratory games. Assets, animations, sounds, and music should be packed into the Pyxel `.pyxres` file and verified with `pyxel-mcp` when tools are exposed.

Interaction model: mouse-first, with keyboard support required as an
alternative path for all core actions.

Current settings implementation: clicking the top-bar gear opens a runtime
settings panel with language selection, music volume, sound-effect volume,
music mute, sound mute, a reset progression control, and a Back button. Reset
progression opens a dangerous-action confirmation dialog before clearing
progress. Music gain is applied to Pyxel channels `0` and `1`; sound effects
use channel `3`. The overlay uses a centered `360 x 304` panel with a framed
preferences card and grouped footer actions; clickable geometry is owned by
the settings component so rendering and interaction stay aligned.

Current playable implementation: the Pyxel game package has an MVP Main Game
scene at `640 x 360`, a scene manager, initial `GameState`, greenhouse slots,
starting plants `AABB` and `aabb`, phenotype, genotype, and statistical
contract support, offspring generation/reveal, Germination Bed harvest
resolution, contract rewards, discovery rewards, collection milestones, and
collection registration for species-qualified genotypes and phenotypes.

The top navigation currently opens runtime sub-scenes for Collection, Garden,
Contracts, Knowledge, Shop, and Settings. Collection shows discovered species,
phenotypes, and genotypes. Garden shows stored plants and locked slots, and can
assign stored plants as Parent A or Parent B. Shop can buy greenhouse slots,
analyzer levels, and all specified species unlocks when the player has enough
credits and required empty slots.

Navigation labels use compact localized names so they remain on one line in
the right rail: `Contract`/`Contrato`, `Learn`/`Saber`, and `Config.` in both
languages. Multiword labels may wrap only at spaces; single long words are
truncated with an ellipsis instead of being split mid-word.

The Shop screen uses three large illustrated progression cards for greenhouse
capacity, analyzer research, and the next species unlock. Cards reuse original
`.pyxres` icons and species sprites, show selected/affordable/locked/completed
states, and feed a structured details panel. The Shop does not repeat the
credit balance because the persistent top bar already displays it. Pressing Buy
opens a centered confirmation overlay with the selected item, price, projected
remaining balance, Cancel, and Confirm actions. Credits are spent only after
explicit confirmation; Escape cancels the overlay.

The Knowledge screen presents the official four-stage learning progression as
a horizontal path: Phenotype, Genotype, Probability, and Genetic Planning. The
active stage shows its concepts as large selectable rows, while the detail panel
uses a stage-specific illustration, learned/locked status, concise explanation,
and analyzer unlock source. Locked stages expose only the broad stage and
required analyzer level; their internal concept names remain hidden. Mouse
hover/click and keyboard arrows share the same component-owned geometry.
The Genotype stage illustration uses the same procedural DNA language as the
analyzer experiment: rotating sine-wave strands, colored allele nodes, connected
rungs, depth-aware highlights, a moving scanline, and pulsing endpoint lights.

The Collection screen is a sticker album rather than a text list. Each category
shows every official numbered slot, including undiscovered placeholders, in a
four-column grid with three visible rows. The album scrolls with the mouse
wheel, Up/Down, Page Up/Page Down, or clicks on the vertical scrollbar. Official
content currently produces 5 species, 124 phenotype, and 1089 genotype slots.

Current QA shortcut: entering tester code `MONEYTREE` sets credits to `999999`
so testers can quickly buy species and analyzer unlocks and reach later game
segments.

UI component direction: gameplay-specific component helpers now live under
`game/mendels_greenhouse/ui/game_components/`, split into contract summary,
Germination Bed geometry, and plant information formatting modules so future
visual refinement can proceed component by component.

Main-game layout alignment: the wider analyzer uses `170 px`; the Parent Cross
panel and Germination Bed share the remaining horizontal bounds (`x=188`,
width `362`). Parent click targets and the Cross button are exported by the
Parent Cross component so interaction geometry remains aligned with rendering.

Current asset implementation: `poetry run poe build-assets` regenerates
`game/mendels_greenhouse/assets/mendels_greenhouse.pyxres` with MVP plant
sprites, 64 x 64 top-navigation/resource icons, initial sound effects, and a
short loopable music pattern. HUD frames, panels, button surfaces, and
Germination Bed panel shapes are generated by runtime drawing code rather than
packed into `.pyxres`. The build task also generates the MVP custom display
font `mendel_5x7.bdf`.

Current typography implementation: all runtime UI text is rendered through
`game/mendels_greenhouse/ui/fonts.py` using the generated `mendel_5x7.bdf`
font. Components must use `draw_text`, `text_width`, and `fit_text` instead of
calling `pyxel.text` directly or assuming the default 4-pixel glyph width.

Current localization safeguards: Babel extraction includes literal
`translate(...)` calls in addition to `_t`, `t`, and `gettext_noop`.
Project-style AST tests reject alphabetic text drawn directly by UI helpers
except approved technical symbols, and require literal `status_message`
values to be registered with `gettext_noop`. Run `poetry run poe
i18n-extract`, `poetry run poe i18n-update`, and `poetry run poe
i18n-compile` when user-facing text changes.

Current specimen inspection behavior: only clicking a visible Germination Bed
specimen opens the centered specimen inspection overlay. Hover has no effect.
The main screen does not reserve a permanent specimen side panel. Store and
discard actions live inside the overlay, which closes through its close button,
`Escape`, or a successful action.

Runtime entrypoint: `game/main.py` is the root-level launcher. The package must
not define `mendels_greenhouse/__main__.py`; `poetry run poe start` runs
the same launcher. Canonical root commands are `python game\main.py` and
`pyxel run game\main.py`.

Current visual refinement: Mendel Pea sprites use 64 x 64 atlas cells and show
pea pods instead of full plants or potted plants. Pod colors are separate from
seed colors so code can recolor visible peas without recoloring the pod. The
asset atlas reserves separate rows for plant resources and icons to avoid
sprite corruption. Snapdragon, Corn, Tomato, and Orchid also have distinct
64 x 64 species sprites in the generated asset atlas so shop-unlocked species
do not display as Mendel Pea.

Current palette direction: the project uses an expanded Pyxel palette with 32
named color indexes. The palette is documented in `specs/ui/color-palette.md`
and now targets a cozy scientific greenhouse look with slate UI backgrounds,
aged paper panels, warm brown wood, brighter botanical greens, yellow phenotype
colors, blue scientific accents, and clear danger states.

Current Main Game visual refinement: runtime panels and buttons use stepped
rounded pixel frames, inset highlights, and shadows. The top bar has a bold
two-line wordmark, icon resource capsules, and a compact contract banner. The
left analyzer is a tactile console with animated glass details and one tall
CRT that occupies the former hardware-control area. Its experiment report
shows parent phenotypes at level 1, genotypes at level 2, gametes and expected
phenotype probabilities at level 3, and the best stored cross for the active
contract at level 4. Parent selection is unified in one panel, the Germination
Bed uses five growth phases and a persistent twenty-cell workspace,
the specimen inspection overlay exposes Store and zero-value Discard actions,
and the full-height right navigation rail uses larger icon buttons.

Official domains:

- https://mendelsgreenhouse.com
- https://mendelsgreenhouse.com.br

Current structure:

- [[README|README]]: public project overview.
- [[AGENTS|AGENTS]]: instructions for Codex and future agents.
- [[DESIGN|DESIGN]]: global design principles.
- [[CONTRIBUTING|CONTRIBUTING]]: contribution and documentation workflow.
- `specs/`: official source of truth for detailed game rules.
- `game/`: Poetry-managed Pyxel game package created with `poetry new`.
- [[agent-memory/backlog|Implementation Backlog]]: feature checklist for the first playable implementation.

Important specs:

- [[specs/GDD|GDD]]
- [[specs/GBD|GBD]]
- [[specs/mechanics/README|Mechanics Specs]]
- [[specs/mechanics/gameplay|Gameplay Rules]]
- [[specs/content/content-bible|Content Bible]]
- [[specs/mechanics/contracts|Contracts]]
- [[specs/mechanics/progression|Progression]]
- [[specs/UI_FLOW|UI_FLOW]]
- [[specs/SCREEN_SPEC|SCREEN_SPEC]]
- [[specs/mechanics/collection|Collection]]
- [[specs/education/learning-objectives|Learning Objectives]]
- [[specs/mechanics/data-model|Data Model]]
- [[specs/ui/README|UI/UX Specification]]
- [[specs/technical/README|Technical Direction]]
- [[specs/technical/platform-roadmap|Platform Roadmap]]
- [[specs/technical/localization|Localization]]
- [[specs/technical/testing|Testing Strategy]]
- [[specs/technical/future-platform|Future Platform]]
- [[specs/technical/development-tooling|Development Tooling]]
- [[specs/technical/implementation-readiness|Implementation Readiness]]
- [[specs/technical/pyxel-mcp|Pyxel MCP Workflow]]
