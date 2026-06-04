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

- Alleles.
- Genotype.
- Homozygosity.
- Heterozygosity.
- Allele segregation.

### Level 3: Probabilistic Analysis

The player sees expected crossbreeding probabilities.

Unlocks:

- Probabilistic contracts.

Teaches:

- Independent assortment.
- Expected distributions.
- Genetic probability.
- Canonical dihybrid ratios such as `9:3:3:1` when the selected cross satisfies
  the biological conditions.

The `9:3:3:1` phenotype ratio should be introduced only when all of these are
true:

- The species has at least two genes under analysis.
- The analyzed traits are controlled by different genes.
- The genes assort independently according to the content rules.
- Both parents are heterozygous for the two analyzed genes, such as
  `AaBb x AaBb`.
- The phenotype rules use complete dominance for both genes.

### Level 4: Genetic Simulator

The player can simulate and compare crosses before performing them.

Unlocks:

- Advanced optimization.
- Better planning for complex genotypic and probabilistic goals.

Teaches:

- Genetic planning and efficient reasoning.

## Knowledge Tree

The Progression Screen includes a knowledge tree that records what the player
has learned.

Rules:

- Knowledge nodes unlock from analyzer levels, discovered concepts, and relevant
  contract milestones.
- Hover, focus, or selection shows concise educational information for the node.
- The same information must be reachable without hover for accessibility.
- Nodes may reference examples from the player's own discovered specimens,
  crosses, and collection entries.
- The knowledge tree explains concepts but does not reveal locked genotype,
  allele, or probability data before the relevant analyzer level.

Initial knowledge nodes:

- Phenotype.
- Dominant allele.
- Recessive allele.
- Allele pair.
- Genotype.
- Homozygous.
- Heterozygous.
- Allele segregation.
- Independent assortment.
- `9:3:3:1` dihybrid ratio.
- Genetic probability.
- Genetic planning.

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

Unlocking a new species requires two empty greenhouse slots. The unlock places
two founder specimens into those slots: the fully dominant genotype and the
fully recessive genotype for that species gene count, such as `AABBCC` and
`aabbcc` for Snapdragon.

## Contracts

```text
Phenotypic
-> Genotypic
-> Probabilistic
```

Contract types should unlock only when the player can inspect or reason about the required information.

Delivery contracts consume delivered plants. Statistical contracts validate generated batches without automatically consuming plants.
