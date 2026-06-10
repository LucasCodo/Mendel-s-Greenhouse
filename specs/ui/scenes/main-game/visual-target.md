---
title: Main Game Visual Target
tags:
  - ui/scenes/main-game
  - ui/visual-target
type: visual-target
project: mendels-greenhouse
status: active
---

# Main Game Visual Target

This is the official visual target for the Main Game Scene. Runtime UI
implementation should approach this reference as closely as Pyxel constraints
allow.

![[specs/ui/scenes/main-game/references/main-game-layout-target.png]]

## Target Standard

The implementation should preserve:

- A full-screen polished pixel-art greenhouse background.
- A wide wooden top bar with the game logo, resource counters, capacity, and
  active contract.
- A left-side genetic analyzer device with a tactile lab-instrument frame.
- A central parchment parent-crossing panel.
- A large Germination Bed as the main offspring result surface.
- A right-side selected specimen action panel attached visually to the bed.
- A vertical right navigation rail with large icon buttons.
- Warm wood, parchment, dark lab panels, green growth highlights, and crisp
  high-contrast pixel text.

## Implementation Rule

When layout tradeoffs are necessary, preserve the functional hierarchy:

```text
Contract visibility
-> parent selection
-> Germination Bed readability
-> selected specimen actions
-> analyzer details
-> navigation
```

## Current Runtime Refinement

The current Pyxel implementation establishes the following production
direction:

- Stepped rounded frames, inset highlights, and lower shadows replace plain
  rectangular panel and button surfaces.
- The top bar uses a bold two-line wordmark, icon-backed resource capsules, and
  a compact active-contract banner.
- The analyzer is rendered as a tactile handheld botanical console with a glass
  tube, animated liquid bubbles, CRT scanline, hardware controls, and status
  light.
- Parent selection is grouped into one parchment work panel with mirrored
  parent summaries and a central cross action.
- The Germination Bed and selected specimen panel form one continuous lower
  workspace.
- The right navigation rail uses larger icons and labels in full-height stacked
  buttons.

These refinements are the baseline for future visual work on the Main Game
Scene. Exact pixel coordinates remain implementation details.

## Image Source Note

The stored `main-game-layout-target.png` is the official scene target. Component
reference images are generated from bitmap model art and stored under
`references/components/`, with the source sheet preserved at
`references/component-sheets/main-game-component-sheet-model.png`.
