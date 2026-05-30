# Progression

## Purpose

This document defines unlock order and progression structure for Mendel's Greenhouse.

## Official Learning Progression

```text
Phenotype
-> Genotype
-> Probability
-> Genetic Planning
```

## First Playable Prototype

The first playable prototype validates the core loop with minimal content.

MVP scope:

- Mendel Pea only.
- 2 independent genes: `A/a` and `B/b`.
- Genetic Analyzer level 1 only.
- Phenotypic contracts only.
- Small greenhouse.
- Functional collection.
- Functional progression.

## Greenhouse

Initial capacity: 4 slots.

Starting plants:

- `AABB`
- `aabb`

Initial free slots: 2.

Maximum capacity: 20 slots.

Final layout: 5 x 4.

Expansion costs are defined in [../GBD.md](../GBD.md).

## Genetic Analyzer

The analyzer is a learning tool with unlimited use. It has:

- No per-use credit cost.
- No time wait.
- No energy cost.

Progression comes from analyzer levels, not usage friction.

### Level 1: Phenotypic Observation

The player sees visible plant traits only.

Unlocks:

- Phenotypic contracts.

Teaches:

- Dominance.
- Recessiveness.

### Level 2: Genetic Sequencing

The player sees full genotypes.

Unlocks:

- Genotypic contracts.

Teaches:

- Genotype.
- Homozygosity.
- Heterozygosity.

### Level 3: Probabilistic Analysis

The player sees expected crossbreeding probabilities.

Unlocks:

- Probabilistic contracts.

Teaches:

- Independent assortment.
- Expected distributions.
- Genetic probability.

### Level 4: Genetic Simulator

The player can simulate and compare crosses before performing them.

Unlocks:

- Advanced optimization.
- Better planning for complex genotypic and probabilistic goals.

Teaches:

- Genetic planning and efficient reasoning.

## Species

```text
Mendel Pea
-> Snapdragon
-> Corn
-> Tomato
-> Orchid
```

Species complexity:

- Mendel Pea: 2 genes.
- Snapdragon: 3 genes.
- Corn: 4 genes.
- Tomato: 5 genes.
- Orchid: 6 genes.

## Contracts

```text
Phenotypic
-> Genotypic
-> Probabilistic
```

Contract types should unlock only when the player can inspect or reason about the required information.

Delivery contracts consume delivered plants. Statistical contracts validate generated batches without automatically consuming plants.
