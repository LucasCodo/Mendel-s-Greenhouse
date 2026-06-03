---
title: Selected Plant Panel
tags:
  - ui/scenes/garden/component
type: component
project: mendels-greenhouse
status: draft
---

# Selected Plant Panel

![[specs/ui/scenes/garden/references/components/garden-component-selected-plant-panel.png]]

## Purpose

Shows the selected plant at high detail and exposes all actions available from
the Garden.

## Elements

- Header `PLANTA SELECIONADA`.
- Plant ID badge.
- Large plant preview.
- Trait summary.
- Action button group.

## Behavior

- Updates from the selected grid slot.
- Hides genotype details until analyzer level allows them.
- Disables discard for protected founder genotypes.

