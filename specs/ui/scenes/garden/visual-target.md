---
title: Garden Visual Target
tags:
  - ui/scenes/garden
  - ui/visual-target
type: visual-target
project: mendels-greenhouse
status: active
---

# Garden Visual Target

This is the official visual target for the Garden Scene. Runtime UI
implementation should approach this reference as closely as Pyxel constraints
allow.

![[specs/ui/scenes/garden/references/garden-layout-target.png]]

## Target Standard

The implementation should preserve:

- A full-screen greenhouse garden background.
- A wide top bar with logo, credits, and garden capacity.
- A left scene title block with `JARDIM` and a short subtitle.
- A large wood-framed stored-plant grid.
- A clear selected-slot highlight.
- Locked/empty slots represented with plus symbols or muted cards.
- A right selected plant details panel with large plant art.
- Phenotype, genotype, color, and texture summaries.
- Four primary actions: use as Parent A, use as Parent B, analyze, discard.
- A vertical right navigation rail with the Garden button highlighted.

## Implementation Rule

When layout tradeoffs are necessary, preserve the functional hierarchy:

```text
Stored plant grid
-> selected plant details
-> parent assignment actions
-> analyzer/discard actions
-> navigation
-> resources/capacity
```

## Image Source Note

The stored `garden-layout-target.png` is the official scene target. Component
reference images are generated from bitmap model art and stored under
`references/components/`, with the source sheet preserved at
`references/component-sheets/garden-component-sheet-model.png`.
