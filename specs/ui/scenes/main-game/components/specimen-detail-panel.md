---
title: Specimen Detail Panel
tags:
  - ui/scenes/main-game/component
type: component
project: mendels-greenhouse
status: draft
---

# Specimen Detail Panel

![[specs/ui/scenes/main-game/references/components/main-game-component-specimen-detail-panel.png]]

## Purpose

Shows details and actions for the selected Germination Bed specimen.

## Elements

- Species header and icon.
- Phenotype section.
- Genotype section when analyzer level allows it.
- Gene explanation section.
- Primary `Store` action.
- Destructive `Discard` action.

## Behavior

- Updates when the player selects a bed cell.
- Store action moves the specimen into an available greenhouse slot.
- Discard removes only the selected unstored offspring, grants no sale value,
  and advances selection to the next available specimen.
- If discarding removes the last remaining specimen, the current bed batch is
  cleared.
- Harvest resolves the grown batch: matching specimens are delivered to the
  active contract first and excess specimens are sold automatically.

## Accessibility

Harvest, store, and discard actions need clear labels and distinct enabled,
disabled, hover, and destructive treatments. Color alone is not enough.
