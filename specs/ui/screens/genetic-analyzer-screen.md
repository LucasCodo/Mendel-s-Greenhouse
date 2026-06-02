# Genetic Analyzer Screen

## Purpose

The Genetic Analyzer reveals plant information and planning tools according to the official four-level progression.

## Level 1: Phenotypic Observation

Shows:

```text
Phenotype
```

Wireframe:

```text
+--------------------------------------+
| Genetic Analyzer - Level 1           |
+------------------+-------------------+
| Plant Visual     | Visible Traits    |
|                  | - Red Flower      |
|                  | - Broad Leaf      |
+------------------+-------------------+
| Locked: genotype, alleles, probability |
+--------------------------------------+
```

## Level 2: Genetic Sequencing

Shows:

```text
Phenotype
Genotype
Allele breakdown
```

Wireframe:

```text
+--------------------------------------+
| Genetic Analyzer - Level 2           |
+------------------+-------------------+
| Plant Visual     | Phenotype         |
|                  | Red Flower        |
|                  | Broad Leaf        |
+------------------+-------------------+
| Genotype: AaBb                       |
| Alleles: A/a controls seed color     |
|          B/b controls seed texture   |
+--------------------------------------+
```

Level 2 allele information:

- Show each gene as a pair of alleles.
- Label dominant and recessive allele symbols when the related concept is
  unlocked.
- Explain that one allele in each pair came from each parent when parentage is
  known.
- Do not show probability forecasts until level 3.

## Level 3: Probabilistic Analysis

Shows:

```text
Phenotype
Genotype
Simple probabilities
Read-only Punnett square
Recognized ratio summaries
```

Wireframe:

```text
+------------------------------------------------+
| Genetic Analyzer - Level 3                     |
+----------------------+-------------------------+
| Parent A: AaBb       | Parent B: AABb          |
+----------------------+-------------------------+
| Punnett Square                                 |
|        | AB     | Ab                         |
| AB     | AABB   | AABb                       |
| aB     | AaBB   | AaBb                       |
+------------------------------------------------+
| Expected Results                               |
| AABB 25% | AaBB 25% | AABb 25% | AaBb 25%     |
+------------------------------------------------+
```

## Level 4: Genetic Simulator

Shows:

```text
Phenotype
Genotype
Complete probabilities
Interactive Punnett square
Predictions
```

Wireframe:

```text
+------------------------------------------------------------+
| Genetic Analyzer - Level 4: Simulator                      |
+----------------------+------------------+------------------+
| Target Result        | Suggested Parents| Estimated Chance |
| AABBCCDD             | AaBBCcDD x ...   | 6.25%            |
+----------------------+------------------+------------------+
| Punnett / Distribution View                                |
| +--------+--------+--------+--------+                      |
| | AABB   | AaBB   | AABb   | AaBb   |                      |
| +--------+--------+--------+--------+                      |
+------------------------------------------------------------+
| [Compare Parents] [Simulate Cross] [Use Suggested Parents] |
+------------------------------------------------------------+
```

## Punnett Square

The Punnett square is the analyzer's visual bridge between genotype and
probability.

### Level 3 Behavior

- Show a read-only Punnett square for the selected parent pair.
- Rows and columns represent the gametes each parent can contribute.
- Each cell shows the normalized offspring genotype produced by combining the
  row and column gametes.
- The result summary must aggregate matching cells into percentages.
- When the selected cross satisfies the independent dihybrid conditions, show
  the grouped phenotype ratio `9:3:3:1` and link it to the Independent
  Assortment knowledge node.
- For the MVP two-gene Mendel Pea scope, support up to a `4 x 4` grid when both
  parents can produce four gametes.
- The grid must not allow editing, parent suggestions, or target optimization
  at level 3.

### Level 4 Behavior

- Allow comparing candidate parent pairs.
- Allow simulating expected distributions before performing a cross.
- Highlight cells that match a selected contract target.
- May show grouped phenotype probabilities in addition to genotype cells.
- Must never show impossible gametes or impossible offspring genotypes.

## States

- No plant selected.
- Single plant selected.
- Parent pair selected.
- Target contract selected.
- Simulation result available.
- Punnett square available.

## Rules

- Never reveal information above the current analyzer level.
- Probability views must match [../../GBD.md](../../GBD.md) and [../../mechanics/gameplay.md](../../mechanics/gameplay.md).
- The simulator may suggest options, but it must not create impossible crosses.
- Punnett square cells must be generated from the same genotype/gamete logic as
  the breeding probability model.
