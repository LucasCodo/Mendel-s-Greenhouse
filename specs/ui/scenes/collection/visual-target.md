---
title: Collection Visual Target
tags:
  - ui/scenes/collection
  - ui/visual-target
type: visual-target
project: mendels-greenhouse
status: active
---

# Collection Visual Target

This is the official visual target for the Collection Scene. Runtime UI
implementation should approach this reference as closely as Pyxel constraints
allow.

![[specs/ui/scenes/collection/references/collection-layout-target.png]]

## Target Standard

The implementation should preserve:

- A full-screen greenhouse archive background.
- A wide top bar with logo, credits, and garden capacity.
- A left scene title block with `COLEÇÃO` and a short subtitle.
- Left vertical category tabs for species, phenotypes, and genotypes.
- A central entry grid with discovered and locked cards.
- A progress badge such as `Descobertos: 5/20`.
- A right entry detail panel with large preview art and trait information.
- A close/return affordance on the detail panel when needed.
- A vertical right navigation rail with Collection as the active destination.

## Implementation Rule

When layout tradeoffs are necessary, preserve the functional hierarchy:

```text
Category tabs
-> entry grid
-> selected entry details
-> discovery progress
-> navigation
-> resources/capacity
```

## Image Source Note

The stored `collection-layout-target.png` is the official scene target.
Component reference images are generated from bitmap model art and stored under
`references/components/`, with the source sheet preserved at
`references/component-sheets/collection-component-sheet-model.png`.
