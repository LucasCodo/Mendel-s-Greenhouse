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
- Panels: generated in runtime with Pyxel drawing primitives unless a future
  spec explicitly requires a fixed decorative panel asset.
- Backgrounds: wide layouts that can crop safely.

Recommended size range:

```text
16 x 16 minimum
256 x 256 maximum
```

Prefer 64 x 64 or 128 x 128 for important visual elements when it improves readability.

Main screen composition target:

```text
640 x 360 internal canvas
```

Required high-polish UI asset groups:

| Asset Group | Recommended Source Size | Notes |
| ----------- | ----------------------: | ----- |
| Logo plaque | 96 x 48 | Botanical frame, readable title |
| Resource frame | 80 x 24 | Supports icon + number |
| Top navigation icon | 64 x 64 | Guide, Garden, Shop, Settings |
| Contract panel | Runtime generated | Parchment surface, progress bar area |
| Parent panel | 128 x 96 | Plant preview plus trait fields |
| Probability panel | 96 x 128 | Pie chart and allele legend |
| Conveyor body | Runtime generated | Metal belt with modular ends |
| Bottom info panel | Runtime generated | Stats, last plant, help |
| Speed controls | 96 x 64 | Pause, play, fast-forward |

## Style Rules

- Edges should be clean.
- Text-bearing areas need low visual noise.
- Important states must be visible without relying only on color.
- UI elements should feel botanical-lab, not medieval fantasy or pure sci-fi.
- Do not pack HUD panel backgrounds into `.pyxres` while the layout is still
  changing. Generate HUD frames, bars, and panel surfaces in runtime code.
