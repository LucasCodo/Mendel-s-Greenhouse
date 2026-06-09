# Conceptual Data Model

## Purpose

This document defines conceptual entities for Mendel's Greenhouse. The approved engine is Pyxel, but this document does not define database tables, storage technology, code architecture, or module layout.

## Plant

Responsibility: represents an individual specimen.

Relationships:

- Belongs to one Species.
- Has one Genotype.
- Expresses one or more Phenotypes.
- May occupy one GreenhouseSlot.
- May reference parent Plants when produced through crossbreeding.

Rules:

- A plant can be stored, sold, delivered, inspected, or used as a parent.
- A plant records generation depth, meaning the number of crossbreeding steps
  needed to produce that specimen from a starting or directly acquired plant.
- Starting or directly acquired plants use generation depth `0` and display as
  `P0`.
- Offspring generation depth is `max(parent_a.generation_depth,
  parent_b.generation_depth) + 1`.
- Offspring display generation depth as filial labels such as `F1`, `F2`, and
  `F3`.

## Species

Responsibility: defines a plant group's genetic complexity.

Relationships:

- Contains Genes.
- Defines valid genotype length.
- Groups collection entries.

Rules:

- Mendel Pea has 2 genes.
- Snapdragon has 3 genes.
- Corn has 4 genes.
- Tomato has 5 genes.
- Orchid has 6 genes.

## Gene

Responsibility: defines one inheritable trait axis.

Relationships:

- Contains possible Alleles.
- Contributes to Genotype.
- Maps to Phenotype rules.

Rules:

- MVP genes use dominant and recessive alleles.

## Allele

Responsibility: represents one inherited variant of a gene.

Relationships:

- Belongs to one Gene.
- Combines with another allele to form a gene pair.

Rules:

- One allele per gene is inherited from each parent.

## Genotype

Responsibility: represents the complete genetic code of a plant.

Relationships:

- Belongs to a Plant.
- Is composed of gene pairs.
- Determines Phenotypes through content rules.

Rules:

- Gene order is consistent and alphabetical in display.

## Phenotype

Responsibility: represents visible expressed traits.

Relationships:

- Derived from Genotype.
- Registered in CollectionEntry when discovered.

Rules:

- Visible from analyzer level 1.

## Contract

Responsibility: defines a player objective.

Relationships:

- Belongs to a Customer type.
- References required Phenotypes, Genotypes, or probabilities.
- Grants rewards when completed.

Rules:

- Must be possible.
- Must match player progression.
- Delivery contracts consume submitted plants.
- Statistical contracts validate generated batches and do not consume plants automatically.

## Customer

Responsibility: defines contract request style.

Relationships:

- Generates or owns Contracts.

Rules:

- Common Customer requests phenotypes.
- Specialist Customer requests genotypes.
- Scientific Customer requests probabilities.

## GeneticAnalyzer

Responsibility: controls what genetic information and planning tools are visible.

Relationships:

- Reads Plants and parent pairs.
- Unlocks contract types.

Rules:

- Has exactly 4 levels.
- Level 1: Phenotypic Observation.
- Level 2: Genetic Sequencing.
- Level 3: Probabilistic Analysis.
- Level 4: Genetic Simulator.

## GreenhouseSlot

Responsibility: stores one plant or remains empty.

Relationships:

- May contain one Plant.

Rules:

- Storage accepts at most one plant for each genotype.
- Initial capacity is 4 slots.
- Maximum capacity is 20 slots.

## CollectionEntry

Responsibility: records permanent discovery state.

Relationships:

- May reference Species, Phenotype, or Genotype.
- May reference a discovered Plant specimen record when preserving lineage
  history.

Rules:

- Discovery persists after sale or delivery.
- Rewards are granted once.
- Specimen collection entries store the specimen generation label and generation
  depth.

## CrossbreedingResult

Responsibility: represents a generated batch of offspring.

Relationships:

- Has two parent Plants.
- Contains generated offspring Plants.
- May include expected probabilities.

Rules:

- Contains displayed offspring generated for the active cross.
- The displayed count follows the number of genetic outcome combinations when
  that count fits on screen.
- Larger future crosses may use a capped representative count.
- Display order is shuffled after valid combinations are generated.
