---
title: Right Navigation Rail
tags:
  - ui/scenes/main-game/component
type: component
project: mendels-greenhouse
status: draft
---

# Right Navigation Rail

![[specs/ui/scenes/main-game/references/components/main-game-component-right-navigation-rail.png]]

## Purpose

Provides large, always-visible navigation buttons for major scenes.

## Buttons In Reference

- Crossbreeding.
- Garden.
- Contracts.
- Shop.
- Collection.
- Settings.

## Visual Direction

Use stacked icon buttons on a warm wood panel. Each button needs a large icon and
short label. The active scene should have a brighter frame.

## Behavior

- Clicking opens the corresponding scene or sub-scene.
- Keyboard focus moves top-to-bottom.
- Disabled destinations should show a locked state only when progression rules
  require it.
