# Content Bible

## Purpose

This document defines the official genetic content for Mendel's Greenhouse.

The baseline MVP starts small on purpose: Mendel Pea only, with 2 independent
genes. The current playable implementation includes the later species listed in
this content bible. Later species increase gene count without introducing new
fundamental mechanics beyond Mendelian inheritance.

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

Trait tables:

| Gene | Dominant phenotype | Recessive phenotype |
| ---- | ------------------ | ------------------- |
| `A` | Red flower | White flower |
| `B` | Tall plant | Short plant |
| `C` | Wide petal | Narrow petal |

## Species 3: Corn

Complexity: 4 genes.

Objective: represent the full Mendel's Second Law challenge and introduce meaningful combinatorial growth.

Genes:

- `A`: kernel color.
- `B`: ear size.
- `C`: plant height.
- `D`: row count.

Trait tables:

| Gene | Dominant phenotype | Recessive phenotype |
| ---- | ------------------ | ------------------- |
| `A` | Purple kernel | Yellow kernel |
| `B` | Large ear | Small ear |
| `C` | Tall plant | Short plant |
| `D` | Many-row ear | Few-row ear |

## Species 4: Tomato

Complexity: 5 genes.

Objective: support advanced planning with harder-to-obtain phenotypes.

Genes:

- `A`: fruit color.
- `B`: fruit size.
- `C`: fruit shape.
- `D`: resistance.
- `E`: maturation time.

Trait tables:

| Gene | Dominant phenotype | Recessive phenotype |
| ---- | ------------------ | ------------------- |
| `A` | Red fruit | Yellow fruit |
| `B` | Large fruit | Small fruit |
| `C` | Round fruit | Pear-shaped fruit |
| `D` | Disease resistant | Disease susceptible |
| `E` | Early maturation | Late maturation |

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

Trait tables:

| Gene | Dominant phenotype | Recessive phenotype |
| ---- | ------------------ | ------------------- |
| `A` | Violet flower | White flower |
| `B` | Large flower | Small flower |
| `C` | Many-petal bloom | Few-petal bloom |
| `D` | Fragrant bloom | Neutral aroma |
| `E` | Star-shaped flower | Round flower |
| `F` | Early blooming | Late blooming |

## Content Boundaries

Do not add new genes, species, or phenotype categories without updating:

- [../mechanics/gameplay.md](../mechanics/gameplay.md)
- [../mechanics/contracts.md](../mechanics/contracts.md)
- [../mechanics/progression.md](../mechanics/progression.md)
- [../education/learning-objectives.md](../education/learning-objectives.md)
- [../mechanics/data-model.md](../mechanics/data-model.md)
- [../ui/assets/plants.md](../ui/assets/plants.md)
