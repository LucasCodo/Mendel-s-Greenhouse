---
title: Top Bar
tags:
  - ui/scenes/main-game/component
type: component
project: mendels-greenhouse
status: draft
---

# Top Bar

![[specs/ui/scenes/main-game/references/components/main-game-component-top-bar.png]]

## Purpose

The Top Bar anchors the scene identity and keeps persistent game state visible.

## Elements

- Logo plaque with `Mendel's Greenhouse`.
- Credits counter.
- Garden capacity counter.
- Active contract banner in the upper center.

## Visual Direction

Use a wood-and-parchment frame with dark inset counters. The logo should remain
large enough to be a first-read brand signal without competing with the active
contract.

## Current Runtime Treatment

- The brand is a centered two-line `MENDEL'S` / `GREENHOUSE` wordmark using
  bold, outlined, letter-spaced pixel text.
- Credits and greenhouse capacity use compact rounded dark capsules with
  resource icons and high-contrast values.
- The wooden status surface ends before the separate active-contract banner so
  the two information groups remain visually distinct.
- Panel corners and borders use stepped pixel rounding, inset highlights, and a
  subtle lower shadow.

## States

- Normal.
- Contract complete highlight.
- Low capacity warning.
