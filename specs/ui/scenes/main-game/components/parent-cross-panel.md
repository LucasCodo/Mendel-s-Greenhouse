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

## Current Runtime Treatment

- Both parent summaries share one unified parchment-and-wood panel.
- Parent A and Parent B use mirrored layouts with plant preview, genotype field,
  and stacked phenotype labels.
- Locked genotype information remains shown as an unknown placeholder.
- A high-contrast cross symbol separates the parents.
- The primary cross button is centered below the parent pair, followed by one
  short helper line.
