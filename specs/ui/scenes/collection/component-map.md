---
title: Collection Component Map
tags:
  - ui/scenes/collection
  - ui/components
type: component-map
project: mendels-greenhouse
status: draft
---

# Collection Component Map

This map decomposes the Collection Scene reference into modular Pyxel
components.

## Hierarchy

```text
CollectionScene
|- CollectionBackground
|- CollectionTopBar
|- CollectionHeader
|- CollectionTabs
|- CollectionEntryGrid
|  |- CollectionEntryCard[]
|  `- LockedEntryCard[]
|- CollectionProgressBadge
|- EntryDetailPanel
|  |- EntryPreview
|  `- EntryInfoSection
`- RightNavigationRail
```

## Implementation Notes

- Category tabs should drive the grid contents without changing the overall
  scene layout.
- Discovered cards and locked cards should share dimensions for stable scanning.
- Locked cards must not reveal exact undiscovered details.
- The selected card should receive a bright outline and update the detail panel.
- The Collection button in the navigation rail should show the active state.

## Component Notes

- [[components/collection-top-bar|Collection Top Bar]]
- [[components/collection-header|Collection Header]]
- [[components/collection-tabs|Collection Tabs]]
- [[components/collection-entry-grid|Collection Entry Grid]]
- [[components/collection-entry-card|Collection Entry Card]]
- [[components/locked-entry-card|Locked Entry Card]]
- [[components/collection-progress-badge|Collection Progress Badge]]
- [[components/entry-detail-panel|Entry Detail Panel]]
- [[components/entry-preview|Entry Preview]]
- [[components/entry-info-section|Entry Info Section]]
- [[components/right-navigation-rail|Right Navigation Rail]]
- [[components/collection-background|Collection Background]]

