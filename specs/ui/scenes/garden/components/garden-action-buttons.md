---
title: Garden Action Buttons
tags:
  - ui/scenes/garden/component
type: component
project: mendels-greenhouse
status: draft
---

# Garden Action Buttons

![[specs/ui/scenes/garden/references/components/garden-component-garden-action-buttons.png]]

## Purpose

Provides direct actions for the selected plant.

## Actions

- Use as Parent A.
- Use as Parent B.
- Analyze.
- Discard.

## Rules

- Parent actions should be enabled only for compatible selectable plants.
- Analyze opens or focuses analyzer information for the selected plant.
- Discard must be disabled for protected founder genotypes.
- Destructive action uses text, icon, and red danger styling.

