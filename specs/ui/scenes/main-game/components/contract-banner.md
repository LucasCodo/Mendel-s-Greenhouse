---
title: Contract Banner
tags:
  - ui/scenes/main-game/component
type: component
project: mendels-greenhouse
status: draft
---

# Contract Banner

![[specs/ui/scenes/main-game/references/components/main-game-component-contract-banner.png]]

## Purpose

Shows the current contract objective and progress during the core loop.

## Elements

- Header label, such as `CONTRATO ATIVO`.
- Objective text.
- Progress bar.
- Numeric progress, such as `0/3`.

## Behavior

- Always visible while in the main scene.
- Updates immediately when a matching Germination Bed specimen is revealed or
  delivered.
- Uses success highlight when complete, but does not automatically claim rewards
  unless the contract rules allow it.

## Accessibility

Progress must include text and numbers, not only bar fill or color.
