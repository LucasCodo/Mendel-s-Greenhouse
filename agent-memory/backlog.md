---
title: Implementation Backlog
tags:
  - agent-memory/todo
type: backlog
project: mendels-greenhouse
status: active
updated: 2026-06-09
---

# Implementation Backlog

Backlog for the first playable implementation of Mendel's Greenhouse.

## Implemented

- [x] Initialize the game package with `poetry new --flat`.
- [x] Make `poetry install` work for the base game package.
- [x] Create the `game/mendels_greenhouse` package.
- [x] Add the root launcher entrypoint for `python game\main.py` and
  `pyxel run game\main.py`.
- [x] Add the package-owned assets directory.
- [x] Add human-readable Pyxel palette enums.
- [x] Implement MVP genotype validation for pea genes `A/a` and `B/b`.
- [x] Implement gamete generation.
- [x] Implement expected crossbreeding distribution calculation.
- [x] Implement shuffled offspring batch generation.
- [x] Implement MVP phenotype mapping for seed color and texture.
- [x] Add unit tests for the initial genetics rules.
- [x] Add a minimal Pyxel screen shell for the first gameplay loop.
- [x] Raise the prototype canvas target to `640 x 360`.
- [x] Update UI specs for the premium pixel-art management layout target.
- [x] Reintroduce Pyxel as a runtime dependency.
- [x] Add `pyxel-mcp` as approved Pyxel agent tooling.
- [x] Add a simple scene manager and Main Game scene.
- [x] Implement `GameState` for plants, credits, active contract, and batch state.
- [x] Implement greenhouse slots with the official initial capacity of 4.
- [x] Add initial plants `AABB` and `aabb` to the greenhouse.
- [x] Implement the first phenotype delivery contract.
- [x] Add automatic contract progress validation during offspring reveal.
- [x] Add rewards for the first completed phenotype contract.
- [x] Add collection registration for discovered species, phenotypes, and genotypes.
- [x] Add mouse-first Main Game controls with keyboard alternatives.
- [x] Add unit tests for state, storage, contracts, and breeding service.

## Next Features

- [x] Add `.pyxres` placeholder assets under `game/mendels_greenhouse/assets/`.
- [x] Create the greenhouse background composition for the `640 x 360` main screen.
- [x] Create initial framed UI pieces for logo, buttons, icons, and the former
  conveyor prototype.
- [x] Create 64 x 64 former conveyor plant sprites for MVP phenotypes.
- [x] Create initial parent-card plant sprites for MVP phenotypes.
- [x] Fix atlas overlap between 64 x 64 plant sprites and UI icons.
- [x] Add click animation states to MVP buttons.
- [x] Add automatic former conveyor reveal/scroll animation.
- [ ] Replace the former conveyor layout with the Germination Bed layout.
- [ ] Regenerate and commit `poetry.lock` when dependency resolution is stable.
- [ ] Configure the active MCP client to expose `pyxel-mcp` tools to Codex sessions.
- [ ] Use `pyxel-mcp` to inspect image banks after adding production sprites.
- [ ] Use `pyxel-mcp` to render and verify sound effects/music after adding audio.
- [x] Create initial Pyxel sound effects for UI clicks, offspring reveal, contract progress, and discovery.
- [x] Create a short loopable greenhouse music track in the `.pyxres` resource.
- [x] Replace code-drawn plant placeholders with Pyxel asset sprites.
- [x] Add an MVP custom BDF display font.
- [ ] Implement Main Game, Greenhouse, Contracts, and Collection scenes.
- [x] Add dedicated Greenhouse, Contracts, and Collection scenes.
- [x] Add clickable parent selection from all stored greenhouse slots.
- [x] Add initial English and Brazilian Portuguese message catalogs.
- [x] Add save data skeleton for the future local autosave slot.
- [x] Add property-based tests for inheritance invariants.
- [x] Add integration tests for crossbreeding plus contract delivery.
- [x] Add species-qualified collection entries and collection rewards.
- [x] Add genotypic and statistical/probabilistic contract support.
- [x] Add level 4 analyzer simulator support for stored-cross planning.
- [x] Split gameplay UI helpers into component modules for visual refinement.
- [x] Require confirmation before resetting progression.
- [x] Add the `MONEYTREE` tester money shortcut for QA.
- [x] Add distinct generated sprites for shop-unlocked species.
- [x] Update specs to match the expanded playable mechanics and QA changes.
