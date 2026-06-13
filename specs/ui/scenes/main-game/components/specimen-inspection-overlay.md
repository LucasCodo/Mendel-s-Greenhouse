---
title: Specimen Inspection Overlay
tags:
  - ui/scenes/main-game/component
type: component
project: mendels-greenhouse
status: draft
---

# Specimen Inspection Overlay

## Purpose

Shows details and actions for a Germination Bed specimen after the player
clicks its visible cell. The overlay appears above the current screen and does
not reserve permanent layout space.

## Elements

- Species header and close button.
- Large plant preview.
- Phenotype section.
- Genotype section when analyzer level allows it.
- Generation section.
- Primary `Store` action.
- Destructive `Discard` action.

## Behavior

- Opens only when the player clicks a visible, occupied bed cell.
- Hovering does not open the overlay or change the selected specimen.
- The close button and `Escape` dismiss the overlay without changing the batch.
- Store action moves the specimen into an available greenhouse slot.
- Discard removes only the selected unstored offspring, grants no sale value,
  and closes the overlay.
- If discarding removes the last remaining specimen, the current bed batch is
  cleared.
- Harvest resolves the grown batch: matching specimens are delivered to the
  active contract first and excess specimens are sold automatically.

## Accessibility

Store, discard, and close actions need clear labels and distinct enabled,
disabled, hover, and destructive treatments. Color alone is not enough. The
overlay must trap gameplay interaction until dismissed.
