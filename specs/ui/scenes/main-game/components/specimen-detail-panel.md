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
- Primary action button, such as `Guardar`.
- Destructive action button, such as `Descartar`.

## Behavior

- Updates when the player selects a bed cell.
- Store action moves the specimen into an available greenhouse slot.
- Discard action removes the specimen when rules allow it.
- Future delivery/sell actions may appear based on active contract and economy
  rules.

## Accessibility

Destructive actions need clear color, icon, and text. Color alone is not enough.
