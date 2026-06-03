---
title: Greenhouse Background
tags:
  - ui/scenes/main-game/component
type: component
project: mendels-greenhouse
status: draft
---

# Greenhouse Background

![[specs/ui/scenes/main-game/references/components/main-game-component-greenhouse-background.png]]

## Purpose

Sets the greenhouse fantasy behind the gameplay panels.

## Visual Direction

- Glass walls and greenhouse beams.
- Botanical clutter and shelves.
- Warm floor perspective.
- Darker corners to keep foreground panels readable.
- No decorative element should obscure text or plant cells.

## Implementation Notes

The current runtime already uses a greenhouse background asset. Future layout
work should crop or mask it so the central Germination Bed, analyzer panel, and
right navigation rail remain readable at `640 x 360`.
