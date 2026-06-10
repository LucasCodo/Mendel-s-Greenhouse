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
- While incomplete, shows the objective above a compact progress bar and
  numeric ratio.
- When complete and unpaid, the progress treatment is replaced by a visible
  `Claim` action.

## Current Runtime Treatment

The banner is a compact parchment panel integrated into the upper status row.
Its `Active Contract` heading is centered above the panel, while objective,
progress, and claim states remain inside the framed surface.

## Accessibility

Progress must include text and numbers, not only bar fill or color.
