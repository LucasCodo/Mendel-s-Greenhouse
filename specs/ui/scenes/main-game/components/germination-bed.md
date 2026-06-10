---
title: Germination Bed
tags:
  - ui/scenes/main-game/component
type: component
project: mendels-greenhouse
status: draft
aliases:
  - Canteiro de Germinação
---

# Germination Bed

![[specs/ui/scenes/main-game/references/components/main-game-component-germination-bed.png]]

## Purpose

The Germination Bed is the main offspring observation surface. It replaces the
former conveyor metaphor with a greenhouse-native planting grid.

## Elements

- Header with `DESCENDENTES` and visible/total count.
- Wooden or terracotta bed frame.
- Soil cells or pot cells.
- Seed, seedling, and adult plant states.
- Contract-match highlights.
- Selected-cell highlight.

## Grid Guidance

- Use a representative cell count for the active cross.
- Use compact grids for simple distributions.
- Use `4 x 4` when a proportion such as 75% / 25% should be visually obvious.
- Later progression may expand to larger beds such as `3 x 4` or `4 x 5`.

## Punnett Relationship

The bed is not a cell-for-cell Punnett square. It is a planted lot. The compact
Punnett summary explains expected genetic combinations, while the bed shows the
generated or representative specimens.

Selecting a bed cell may highlight the corresponding Punnett outcome group when
analyzer level allows it.

## Behavior

- Crossbreeding creates seed cells.
- Reveal animation uses five readable phases: seed, emerging sprout, small
  seedling, medium seedling, and adult phenotype.
- Fully grown specimens may use a subtle desynchronized one-pixel sway.
- Clicking a cell selects the specimen and updates the detail panel.
- Matching contract specimens receive a visible icon and outline.
- Empty idle beds retain the supported cell grid so the workspace does not
  collapse before the first cross.
- The header shows `Descendants` with a visible/total count.
- The centered `Harvest` action remains inside the bed workspace and is enabled
  only when the batch can be resolved.

## Current Runtime Treatment

The bed uses one large rounded wood frame with a dark title strip, larger soil
cells, centered growth sprites, and a persistent grid of up to twenty cells.
The separate lower statistics bar has been removed from the main composition;
contract progress remains in the top banner and specimen actions remain in the
adjacent detail panel.
