---
title: Runtime Overlays Component Map
tags:
  - ui/scenes/overlays
  - ui/components
type: component-map
project: mendels-greenhouse
status: draft
---

# Runtime Overlays Component Map

## Hierarchy

```text
RuntimeOverlays
|- IntroPanel
|- ParentPickerOverlay
|  |- ParentPickerSlot[]
|  `- BackButton
|- HoveredPlantTooltip
`- ModalScrim
```

## Implementation Notes

- Overlays must not mutate gameplay state directly.
- Parent picker slots can expose selected, empty, genotype, and trait display
  states; assigning parents remains scene-owned behavior.
- Hover tooltips must respect analyzer-level information visibility.
