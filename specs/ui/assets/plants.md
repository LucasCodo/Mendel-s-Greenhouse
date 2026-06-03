# Plant Assets

## Purpose

Plant assets must make genetic phenotypes visually readable at small sizes in
plant cards and Germination Bed cells.

## Global Rules

- Phenotypes must be recognizable without text.
- Each gene maps to a clear visual feature.
- Visual priority favors contract-relevant traits.
- Plant silhouettes must stay readable in `PlantCard` and Germination Bed states.

## Gene Visual Mapping

| Gene | MVP / Example Trait Axis | Dominant Visual | Recessive Visual | Priority |
| ---- | ------------------------ | --------------- | ---------------- | -------- |
| A | Seed or flower color | Yellow seed / red flower | Green seed / white flower | High |
| B | Texture or size | Smooth seed / large form | Wrinkled seed / small form | High |
| C | Height or shape | Tall / wide | Short / narrow | Medium |
| D | Pattern or rows | Spotted / many rows | Plain / few rows | Medium |
| E | Timing or resistance | Early / resistant | Late / vulnerable | Medium |
| F | Aroma or blooming | Fragrant / fast bloom | Mild / slow bloom | Medium |

## Species 1: Mendel Pea

Genes:

- `A`
- `B`

Required plant variants:

- Yellow seed + smooth seed.
- Yellow seed + wrinkled seed.
- Green seed + smooth seed.
- Green seed + wrinkled seed.

Reference images:

- [references/plants/mendel-pea/README.md](references/plants/mendel-pea/README.md)
- [references/plants/mendel-pea/mendel-pea-variants-sheet.png](references/plants/mendel-pea/mendel-pea-variants-sheet.png)

MVP Mendel Pea assets should be shown as vertical or diagonal pea pods, not as
a horizontal pod, full plant, or plant in a pot. The pod remains green across
variants; the visible peas inside the pod carry the seed color trait. Keep pod
colors and seed colors as separate asset parameters so code can change seed
color without recoloring the pod.

Texture must be readable on the peas themselves:

- Smooth seeds: round, glossy peas with a clean highlight.
- Wrinkled seeds: irregular pea silhouette with visible crease lines.

## Species 2: Snapdragon

Genes:

- `A`
- `B`
- `C`

Adds:

- Flower color.
- Plant height.
- Petal shape.

## Species 3: Corn

Genes:

- `A`
- `B`
- `C`
- `D`

Adds:

- Kernel color.
- Ear size.
- Plant height.
- Row count.

## Species 4: Tomato

Genes:

- `A`
- `B`
- `C`
- `D`
- `E`

Adds advanced planning traits:

- Fruit color.
- Fruit size.
- Fruit shape.
- Resistance.
- Maturation time.

## Species 5: Orchid

Genes:

- `A`
- `B`
- `C`
- `D`
- `E`
- `F`

Adds endgame collection traits:

- Color.
- Size.
- Petal count.
- Aroma.
- Shape.
- Blooming time.

## Asset States

Each plant visual may need:

- Normal.
- Newly discovered glow.
- Contract match highlight.
- Selected as parent.
- Reserved for delivery.
- Disabled or unavailable.

## Scale Requirements

| Context | Requirement |
| ------- | ----------- |
| PlantCard | Trait readable at small card size |
| Germination Bed | Trait readable in grid cells |
| Analyzer | Larger view for inspection |
| Collection | Clean reference pose |

## Resolution Requirements

| Plant Asset Use | Minimum | Preferred | Maximum |
| --------------- | ------: | --------: | ------: |
| Germination Bed specimen | 16 x 16 | 24 x 24 or 32 x 32 | 64 x 64 |
| PlantCard sprite | 64 x 64 | 96 x 96 or 128 x 128 | 256 x 256 |
| Analyzer preview | 96 x 96 | 128 x 128 | 256 x 256 |
| Discovery popup | 96 x 96 | 128 x 128 | 256 x 256 |

Use higher-resolution pixel art when phenotype readability improves.

The visual target is polished pixel art rather than minimal retro placeholders.
Parent cards and analyzer views should use larger sprites than Germination Bed
items so flower color, stem height, leaf shape, and pot silhouette are obvious
without text.

## Prohibited Ambiguity

Do not make:

- Red and purple too similar.
- Broad and narrow leaves differ only slightly.
- Tall and short stems depend on camera angle.
- Spotted and plain petals differ only by subtle texture.
