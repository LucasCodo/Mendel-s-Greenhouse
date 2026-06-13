---
title: Genetic Analyzer Panel
tags:
  - ui/scenes/main-game/component
type: component
project: mendels-greenhouse
status: draft
---

# Genetic Analyzer Panel

![[specs/ui/scenes/main-game/references/components/main-game-component-genetic-analyzer-panel.png]]

## Purpose

Displays analyzer-unlocked information for the selected plant or parent pair.

## Elements

- Device frame with glass tube.
- Analyzer title and level badge.
- Selected species or plant summary.
- Phenotype text.
- Genotype section when level allows it.
- Detected genes list.

## Information Visibility

- Level 1: parent phenotype observations.
- Level 2: parent genotypes and allele sequencing.
- Level 3: parent gametes and expected phenotype probabilities.
- Level 4: stored-cross comparison against the active contract.

## Visual Direction

The panel should feel like a botanical lab instrument. Use cool glass, dark
screen surfaces, and green science highlights.

## Current Runtime Treatment

- The analyzer uses a rounded parchment console body with inset shading, corner
  screws, and metal details.
- A side glass tube contains glowing green liquid with procedural rising
  bubbles.
- The dark CRT screen uses a subtle grid, animated scanline, level label, and
  analyzer-unlocked diagnostic text.
- The CRT starts closer to the top edge and occupies the former hardware
  control area.
- The analyzer is slightly wider than the previous treatment; the parent and
  Germination Bed panels are correspondingly narrower while retaining their
  shared right edge.
- The displayed view follows the player's unlocked analyzer level.
- Selecting a parent pair automatically refreshes the experiment report.
- Level 3 probabilities are grouped by visible phenotype from the same
  Mendelian distribution used to generate offspring.
- Level 4 compares compatible stored pairs and reports the pair with the best
  probability of satisfying the active contract.
- Probability-ready and standby states appear in the CRT footer with both a
  label and an indicator.
