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
+--------------------------------------+
```

## Level 3: Probabilistic Analysis

Shows:

```text
Phenotype
Genotype
Simple probabilities
```

Wireframe:

```text
+------------------------------------------------+
| Genetic Analyzer - Level 3                     |
+----------------------+-------------------------+
| Parent A: AaBb       | Parent B: AABb          |
+----------------------+-------------------------+
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
Punnett square
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

## States

- No plant selected.
- Single plant selected.
- Parent pair selected.
- Target contract selected.
- Simulation result available.

## Rules

- Never reveal information above the current analyzer level.
- Probability views must match [../../GBD.md](../../GBD.md) and [../../mechanics/gameplay.md](../../mechanics/gameplay.md).
- The simulator may suggest options, but it must not create impossible crosses.
