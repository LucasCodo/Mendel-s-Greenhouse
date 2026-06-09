---
title: Shop Component Map
tags:
  - ui/scenes/shop
  - ui/components
type: component-map
project: mendels-greenhouse
status: draft
---

# Shop Component Map

## Hierarchy

```text
ShopScene
|- SceneShell
|- CreditsSummary
|- ShopCardGrid
|  |- ShopCard(Greenhouse Slot)
|  |- ShopCard(Analyzer Upgrade)
|  `- ShopCard(Species Unlock)
|- ShopDetailsPanel
`- BuyButton
```

## Implementation Notes

- Shop cards display title, price, and availability calculated by the scene.
- Buying remains a scene/service action.
- Species unlock text must follow the content bible and progression specs.
