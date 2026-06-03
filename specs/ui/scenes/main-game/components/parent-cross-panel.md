---
title: Parent Cross Panel
tags:
  - ui/scenes/main-game/component
type: component
project: mendels-greenhouse
status: draft
---

# Parent Cross Panel

![[specs/ui/scenes/main-game/references/components/main-game-component-parent-cross-panel.png]]

## Purpose

Lets the player inspect and confirm the selected parent pair before generating
offspring.

## Elements

- `Parental A` card.
- `Parental B` card.
- Cross symbol between parents.
- Central `Cross` action button.
- Helper status line.

## Data

Each parent card should show:

- Plant/pod preview.
- Genotype label when analyzer level allows it.
- Phenotype labels.
- Selection state.
- Species compatibility state.

## Behavior

- Clicking either parent opens the parent picker from garden specimens.
- Cross action is enabled only when both selected parents are valid and
  compatible.
- If parent species differ, selecting one parent should repair or request a
  compatible second parent according to gameplay rules.
