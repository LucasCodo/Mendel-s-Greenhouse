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

The panel may include the
[Mendel Guide character](../../../characters/mendel-guide.md) as a portrait or
small guide icon when the prompt is part of onboarding or contextual teaching.

## Content Rules

- Keep text short.
- Use the current action context.
- Do not reveal locked analyzer information.
- Prefer one concrete genetics idea at a time.
- Keep guide messages dismissible and available through click or keyboard
  focus, not hover only.

## Example

```text
Cada planta fornece
um alelo por gene.
```

## Placement

The reference places this panel below the analyzer on the lower left. It should
not compete with the contract banner or Germination Bed.
