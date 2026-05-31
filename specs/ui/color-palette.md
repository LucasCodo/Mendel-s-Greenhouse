# Color Palette Specification

## Purpose

Mendel's Greenhouse uses an expanded Pyxel palette to reach a modern
pixel-art look without making the whole game feel orange.

The palette must support:

- Greenhouse backgrounds.
- Botanical foliage.
- Parchment UI surfaces.
- Wood and terracotta accents.
- Glass and scientific equipment.
- Multiple plant species and phenotype colors.
- Contract, rarity, and feedback states.

## Pyxel Palette Policy

Pyxel starts from a small retro-console palette, but the project may extend the
color list because Pyxel supports user-extensible colors, channels, and banks.

Rules:

- Do not treat 16 colors as a hard project limit.
- Treat palette index `0` as transparent for sprite blits that use
  `colkey=0`; do not use it for visible sprite outlines.
- Keep the first 16 indexes stable for core UI and MVP sprites.
- Use indexes 16+ for additional phenotype, rarity, glass, metal, and future
  species colors.
- Do not scatter raw color indexes in gameplay or UI code.
- All color indexes must be exposed through human-readable names in
  `mendels_greenhouse/ui/palette.py`.
- Background PNGs and `.pyxres` assets must be quantized against the same
  runtime palette.

## Visual Reference Direction

The current palette is inspired by warm modern pixel-art farming and cozy
laboratory games while preserving Pyxel's indexed-color workflow. The intended
screen read is:

- Near-black blue-gray outlines and shadows.
- Deep slate-blue greenhouse and UI backgrounds.
- Botanical greens that stand clearly apart from panels and wood.
- Aged paper panels with warm but readable contrast.
- Warm brown wood frames with orange highlights used sparingly.
- Gold and yellow for seeds, rewards, and recessive pea color.
- Purple/blue scientific accents for genetics, analyzer, and rarity feedback.

Orange and brown must not dominate the full screen. They are structural accents,
not the main mood.

## Palette Groups

### Core 0-15

These indexes are used by the MVP runtime, generated `.pyxres`, text, frames,
and the background quantization pipeline.

| Index | Name | Hex | Primary Use |
| ----: | ---- | --- | ----------- |
| 0 | Ink Shadow | `#111827` | Outlines, deep shadows |
| 1 | Deep Glass Navy | `#1E293B` | Dark greenhouse glass, night UI |
| 2 | Genetic Purple | `#7C3AED` | Purple flowers, genetics accent |
| 3 | Leaf Shadow | `#2D9D78` | Deep foliage and green pea base |
| 4 | Dark Wood | `#7C4F2C` | Frames, wood structure |
| 5 | Blue Glass | `#4F6FAF` | Secondary blue UI and lab glass |
| 6 | Glass Highlight | `#C7DDFB` | Windows, cool highlights |
| 7 | Parchment Light | `#F8F4E8` | Text-bearing panel highlights |
| 8 | Tomato Red | `#D94B6A` | Warnings, tomato phenotype, cancel |
| 9 | Terracotta | `#D88B3A` | Pots, wood highlights, small warm accents |
| 10 | Seed Gold | `#F2C94C` | Yellow pea seed, coins, reward highlight |
| 11 | Leaf Green | `#6BCB77` | Main foliage and positive feedback |
| 12 | Wood Midtone | `#B89A72` | Secondary wood, progress track, panel depth |
| 13 | Warm Floor | `#334155` | Background medium and restrained dark surfaces |
| 14 | Sunlit Cream | `#F7D96E` | Bright yellow and warm highlights |
| 15 | Parchment Base | `#E8D3B0` | Main parchment panels |

### Extended 16-31

These colors are reserved for richer future content. Use them when a phenotype
would become ambiguous with the core palette.

| Index | Name | Hex | Primary Use |
| ----: | ---- | --- | ----------- |
| 16 | Leaf Highlight | `#A7E48A` | Young leaves, healthy growth |
| 17 | Cyan Science | `#86C8AA` | Analyzer lines, probability UI |
| 18 | Blue Flower | `#7AA2F7` | Future flower phenotype |
| 19 | Pink Flower | `#F7A8B8` | Snapdragon/orchid phenotype |
| 20 | White Petal | `#F8F4E8` | White flowers/petals |
| 21 | Orchid Violet | `#9B58D6` | Orchid/purple rarity variant |
| 22 | Corn Yellow | `#F7D96E` | Corn kernels, high-value yellow |
| 23 | Corn Husk | `#A7E48A` | Corn leaves/husks |
| 24 | Tomato Orange | `#D88B3A` | Tomato fruit transition |
| 25 | Tomato Red Bright | `#D94B6A` | Tomato fruit dominant color |
| 26 | Soil Dark | `#3A2A20` | Soil, pot interior |
| 27 | Metal Dark | `#334155` | Conveyor body, machine panels |
| 28 | Metal Light | `#9CA3AF` | Bolts, rails, mechanical highlights |
| 29 | Rare Gem | `#A35CFF` | Premium/rare resource |
| 30 | Success Lime | `#6BCB77` | Contract success, completion tick |
| 31 | Error Ember | `#D94B6A` | Invalid action, danger accent |

## Phenotype Color Rules

### Mendel Pea

- Seed color:
  - Yellow: `Seed Gold` or `Corn Yellow`.
  - Green: `Leaf Highlight` over a darker green pod.
- Texture:
  - Smooth: rounded highlight using `Parchment Light`.
  - Wrinkled: internal lines using `Dark Wood` or `Soil Dark`.

### Snapdragon

- Flower color:
  - Red: `Tomato Red` or `Tomato Red Bright`.
  - White: `White Petal` with `Parchment Light`.
- Height:
  - Tall: longer stem silhouette.
  - Short: compressed stem silhouette.
- Petal shape:
  - Wide: broad petal clusters.
  - Narrow: slim petal clusters.

### Corn

- Kernel color:
  - Yellow: `Corn Yellow`.
  - Pale/white: `White Petal`.
- Ear size:
  - Large: bigger ear silhouette.
  - Small: shorter ear silhouette.
- Row count:
  - Many rows: patterned kernel lines.
  - Few rows: simpler kernel groups.

### Tomato

- Fruit color:
  - Red: `Tomato Red Bright`.
  - Orange/yellow: `Tomato Orange` or `Seed Gold`.
- Resistance:
  - Healthy: `Success Lime` or `Leaf Highlight`.
  - Vulnerable: muted `Leaf Shadow` plus visible spots.

### Orchid

- Flower color:
  - Purple/violet: `Orchid Violet`.
  - Pink: `Pink Flower`.
  - White: `White Petal`.
- Aroma/bloom traits should use particle/effect color, not only flower color,
  to avoid ambiguity.

## UI Color Rules

- Top bars and machine frames use `Ink Shadow`, `Deep Glass Navy`, and
  `Warm Floor`.
- Text panels use `Parchment Base`, `Parchment Light`, and `Sunlit Cream`.
- Primary action buttons use `Leaf Green`/`Success Lime`, not orange.
- Destructive/cancel actions use `Tomato Red`/`Error Ember`.
- Progress bars use `Wood Midtone` for the empty track and `Success Lime` for
  completion. Use phenotype-specific color only when the bar communicates a
  phenotype directly.
- Analyzer UI should prefer `Cyan Science`, `Blue Glass`, `Rare Gem`, and
  `Genetic Purple`.

## Background Balance

Backgrounds should reserve visual contrast for the UI and plants.

Target balance:

- 35-45% cool/dark greenhouse tones.
- 25-35% foliage greens.
- 15-25% parchment/cream UI surfaces.
- 5-15% warm wood/terracotta.
- 5-10% high-saturation phenotype/accent colors.

If a screenshot reads primarily orange/brown, revise the palette or background
quantization before adding more UI.

## Asset Workflow

When changing the palette:

1. Update this document.
2. Update `PROJECT_PALETTE` and `PyxelColor` in
   `mendels_greenhouse/ui/palette.py`.
3. Re-quantize PNG backgrounds against the updated palette.
4. Regenerate `.pyxres` with `poetry run poe build-assets`.
5. Validate with `poetry run poe check`.
6. Use Pyxel MCP visual/palette inspection when available.
