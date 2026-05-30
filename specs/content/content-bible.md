# Content Bible

## Purpose

This document defines the official genetic content for Mendel's Greenhouse.

The MVP starts small on purpose: Mendel Pea only, with 2 independent genes. Later species increase gene count without introducing new fundamental mechanics beyond Mendelian inheritance.

## Naming Rules

- Species names are final design names unless later revised by a spec update.
- Genes use uppercase letters for dominant alleles and lowercase letters for recessive alleles.
- Genotypes list genes in alphabetical order.
- MVP implementation should focus on Mendel Pea before expanding to later species.

## Species Progression

| Species | Genes | Objective |
| ------- | ----: | --------- |
| Mendel Pea | 2 | Tutorial |
| Snapdragon | 3 | Intermediate |
| Corn | 4 | Full Mendel's Second Law |
| Tomato | 5 | Advanced planning |
| Orchid | 6 | Endgame and collection |

## Species 1: Mendel Pea

Complexity: 2 genes.

Objective: introduce independent assortment through seed color and seed texture.

Genes:

- `A`: seed color.
- `B`: seed texture.

Starting plants:

- `AABB`
- `aabb`

### Gene A: Seed Color

| Genotype     | Phenotype   |
| ------------ | ----------- |
| `AA` or `Aa` | Yellow seed |
| `aa`         | Green seed  |

### Gene B: Seed Texture

| Genotype     | Phenotype     |
| ------------ | ------------- |
| `BB` or `Bb` | Smooth seed   |
| `bb`         | Wrinkled seed |

### Relevant MVP Genotypes

- `AABB`
- `AABb`
- `AAbb`
- `AaBB`
- `AaBb`
- `Aabb`
- `aaBB`
- `aaBb`
- `aabb`

## Species 2: Snapdragon

Complexity: 3 genes.

Objective: introduce three-gene crosses.

Genes:

- `A`: flower color.
- `B`: plant height.
- `C`: petal shape.

Trait examples:

- Red flower vs white flower.
- Tall plant vs short plant.
- Wide petal vs narrow petal.

Detailed genotype-to-phenotype tables should be finalized when Snapdragon enters implementation scope.

## Species 3: Corn

Complexity: 4 genes.

Objective: represent the full Mendel's Second Law challenge and introduce meaningful combinatorial growth.

Genes:

- `A`: kernel color.
- `B`: ear size.
- `C`: plant height.
- `D`: row count.

Detailed genotype-to-phenotype tables should be finalized when Corn enters implementation scope.

## Species 4: Tomato

Complexity: 5 genes.

Objective: support advanced planning with harder-to-obtain phenotypes.

Genes:

- `A`: fruit color.
- `B`: fruit size.
- `C`: fruit shape.
- `D`: resistance.
- `E`: maturation time.

Detailed genotype-to-phenotype tables should be finalized when Tomato enters implementation scope.

## Species 5: Orchid

Complexity: 6 genes.

Objective: provide endgame collection and advanced breeding goals.

Genes:

- `A`: flower color.
- `B`: flower size.
- `C`: petal count.
- `D`: aroma.
- `E`: flower shape.
- `F`: blooming time.

Detailed genotype-to-phenotype tables should be finalized when Orchid enters implementation scope.

## Content Boundaries

Do not add new genes, species, or phenotype categories without updating:

- [../mechanics/gameplay.md](../mechanics/gameplay.md)
- [../mechanics/contracts.md](../mechanics/contracts.md)
- [../mechanics/progression.md](../mechanics/progression.md)
- [../education/learning-objectives.md](../education/learning-objectives.md)
- [../mechanics/data-model.md](../mechanics/data-model.md)
- [../ui/assets/plants.md](../ui/assets/plants.md)
