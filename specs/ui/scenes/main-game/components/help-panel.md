---
title: Help Panel
tags:
  - ui/scenes/main-game/component
type: component
project: mendels-greenhouse
status: draft
---

# Help Panel

![[specs/ui/scenes/main-game/references/components/main-game-component-help-panel.png]]

## Purpose

Provides short contextual teaching text without interrupting the main loop.

## Content Rules

- Keep text short.
- Use the current action context.
- Do not reveal locked analyzer information.
- Prefer one concrete genetics idea at a time.

## Example

```text
Cada planta fornece
um alelo por gene.
```

## Placement

The reference places this panel below the analyzer on the lower left. It should
not compete with the contract banner or Germination Bed.
