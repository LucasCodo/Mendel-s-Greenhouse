# UI Elements

## Purpose

This document lists reusable UI art assets and layout elements required for the interface.

| Asset | Purpose | Recommended Variations |
| ----- | ------- | ---------------------- |
| Plant card frame | Holds plant data | normal, selected, reserved, deliverable, locked |
| Contract panel | Shows contract objective | phenotypic, genotypic, probabilistic |
| Analyzer panel | Displays genetic data | level 1, level 2, level 3, level 4 |
| Conveyor belt | Shows offspring generation | idle, moving, paused |
| Greenhouse slot | Stores plants | empty, occupied, locked, highlighted |
| Progress bar | Shows completion | contract, collection, upgrade |
| Reward popup frame | Displays rewards | small, large |
| Discovery popup frame | Displays discoveries | phenotype, genotype, species |
| Tooltip panel | Context help | short text, icon + text |
| Modal panel | Confirmation | confirm, warning, reward |

## Resolution Guidance

Pyxel is the selected engine, and runtime assets should be packed into `.pyxres`.

Minimum practical sizes:

- Icons: square source, readable at small UI size.
- Plant cards: vertical card-friendly composition.
- Panels: scalable 9-slice-friendly shapes.
- Backgrounds: wide layouts that can crop safely.

Recommended size range:

```text
16 x 16 minimum
256 x 256 maximum
```

Prefer 64 x 64 or 128 x 128 for important visual elements when it improves readability.

## Style Rules

- Edges should be clean.
- Text-bearing areas need low visual noise.
- Important states must be visible without relying only on color.
- UI elements should feel botanical-lab, not medieval fantasy or pure sci-fi.
