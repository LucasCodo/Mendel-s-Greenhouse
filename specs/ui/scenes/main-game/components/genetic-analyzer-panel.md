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

- Device frame with glass tube and lab controls.
- Analyzer title and level badge.
- Selected species or plant summary.
- Phenotype text.
- Genotype section when level allows it.
- Detected genes list.

## Information Visibility

- Level 1: phenotype only.
- Level 2: genotype and allele breakdown.
- Level 3: probability and compact Punnett summary access.
- Level 4: simulator shortcut or expanded planning view.

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
- A circular directional pad cycles through generated offspring.
- A green leaf button triggers a short screen flash as tactile feedback.
- A vertical roller selects a view level from the analyzer levels already
  unlocked; it cannot preview locked information.
- The status light distinguishes probability-ready and standby states with
  both a label and an indicator.

The temporary view-level selector changes presentation only. It does not grant
analyzer progression or reveal information above the player's unlocked level.
