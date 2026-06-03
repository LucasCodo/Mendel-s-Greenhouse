---
title: Main Game Component Map
tags:
  - ui/scenes/main-game
  - ui/components
type: component-map
project: mendels-greenhouse
status: draft
---

# Main Game Component Map

This map decomposes the main scene reference into modular Pyxel components.

## Hierarchy

```text
MainGameScene
|- GreenhouseBackground
|- TopBar
|  |- LogoPlaque
|  |- ResourceCounters
|  |- CapacityCounter
|  `- ContractBanner
|- GeneticAnalyzerPanel
|- ParentCrossPanel
|  |- ParentCard(A)
|  |- CrossAction
|  `- ParentCard(B)
|- GerminationBed
|  |- BedHeader
|  |- BedCellGrid
|  `- ContractMatchHighlights
|- SpecimenDetailPanel
|- HelpPanel
`- RightNavigationRail
```

## Implementation Notes

- Keep scene-level layout constants in one place before drawing components.
- Draw order should be background, panels, bed cells, plant sprites, highlights,
  text, then modal overlays.
- Components should accept data already filtered by analyzer level; component
  drawing should not reveal locked genotype/probability information by itself.
- The Germination Bed should replace the former conveyor layout in the runtime
  scene.
- The compact Punnett/reference area can live near the Germination Bed or inside
  the analyzer panel once analyzer level 3 is active.

## Component Notes

- [[components/top-bar|Top Bar]]
- [[components/contract-banner|Contract Banner]]
- [[components/genetic-analyzer-panel|Genetic Analyzer Panel]]
- [[components/parent-cross-panel|Parent Cross Panel]]
- [[components/germination-bed|Germination Bed]]
- [[components/specimen-detail-panel|Specimen Detail Panel]]
- [[components/help-panel|Help Panel]]
- [[components/right-navigation-rail|Right Navigation Rail]]
- [[components/greenhouse-background|Greenhouse Background]]

