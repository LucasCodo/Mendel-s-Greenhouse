---
title: Garden Component Map
tags:
  - ui/scenes/garden
  - ui/components
type: component-map
project: mendels-greenhouse
status: draft
---

# Garden Component Map

This map decomposes the Garden Scene reference into modular Pyxel components.

## Hierarchy

```text
GardenScene
|- GardenBackground
|- GardenTopBar
|  |- LogoPlaque
|  |- CreditsCounter
|  `- CapacityCounter
|- GardenHeader
|- GardenSlotGrid
|  `- PlantSlotCard[]
|- SelectedPlantPanel
|  |- SelectedPlantPreview
|  |- PlantTraitSummary
|  `- GardenActionButtons
`- RightNavigationRail
```

## Implementation Notes

- Keep grid geometry explicit: the reference shows 5 columns and 3 visible rows.
- Slot cards should support occupied, empty, locked, selected, starred, and
  count-badge states.
- The selected plant panel should update from the selected grid slot.
- The same plant data should drive both the slot card and selected detail panel.
- The Garden button in the navigation rail should show the active state.

## Component Notes

- [[components/garden-top-bar|Garden Top Bar]]
- [[components/garden-header|Garden Header]]
- [[components/garden-slot-grid|Garden Slot Grid]]
- [[components/plant-slot-card|Plant Slot Card]]
- [[components/selected-plant-panel|Selected Plant Panel]]
- [[components/selected-plant-preview|Selected Plant Preview]]
- [[components/plant-trait-summary|Plant Trait Summary]]
- [[components/garden-action-buttons|Garden Action Buttons]]
- [[components/right-navigation-rail|Right Navigation Rail]]
- [[components/garden-background|Garden Background]]

