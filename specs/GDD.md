# Game Design Document

## Overview

Mendel's Greenhouse is an educational single-player game focused on Mendel's Second Law, the Law of Independent Assortment.

The player manages a genetic greenhouse, crossbreeds plants, observes offspring, completes contracts, expands the greenhouse, and builds a permanent collection of discovered species, phenotypes, and genotypes.

The game teaches genetics through interaction, not exposition. Players learn by forming hypotheses, running crosses, observing patterns, and applying discoveries to practical goals.

## Player Fantasy

The player is a greenhouse geneticist responsible for producing plants with requested traits. Clients submit contracts, and the player must use available plants, genetic analysis, storage space, and experimentation to fulfill those requests.

## Goals

### Short-Term Goals

- Accept and complete active contracts.
- Produce plants with requested visible traits.
- Learn which parent combinations create useful offspring.
- Decide which specimens to keep, sell, or deliver.

### Mid-Term Goals

- Expand greenhouse capacity.
- Unlock deeper genetic analysis.
- Preserve useful hybrids.
- Unlock new species with more genes.

### Long-Term Goals

- Complete the genetic collection.
- Discover all available phenotypes and genotypes.
- Unlock all species.
- Use probability and planning to solve complex contracts.

## First Playable Prototype

The first playable prototype validates the core loop:

1. The player has two parent plants.
2. The player selects two plants for crossbreeding.
3. One offspring batch is generated.
4. Offspring germinate in the Germination Bed.
5. The player sees produced phenotypes.
6. The system automatically checks contract progress.
7. The player receives rewards.
8. The player can store useful offspring for future crosses.

MVP content:

- Mendel Pea only.
- 2 independent genes: `A/a` and `B/b`.
- Genetic Analyzer level 1 only.
- Phenotypic contracts only.
- Small greenhouse.
- Functional collection.
- Functional progression.

The MVP objective is to teach the Second Law of Mendel without introducing excessive complexity.

## Core Gameplay Loop

1. Accept a contract.
2. Select parent plants.
3. Perform a crossbreeding process.
4. Observe offspring in the Germination Bed.
5. Analyze results.
6. Store useful specimens.
7. Deliver valid plants or validate statistical goals.
8. Receive rewards.
9. Upgrade the greenhouse or analyzer.
10. Repeat with harder goals.

## Core Systems

### Plants

Each plant belongs to a species and has genes, alleles, a genotype, and one or more phenotypes.

### Crossbreeding

Crossbreeding combines alleles from two parent plants to create offspring. The system calculates valid genetic combinations before displaying offspring in shuffled order.

### Genetic Analyzer

The analyzer controls what the player can know:

```text
Level 1: Phenotypic Observation
Level 2: Genetic Sequencing
Level 3: Probabilistic Analysis
Level 4: Genetic Simulator
```

The analyzer has unlimited use. It does not consume credits, time, energy, or any other per-use resource.

### Contracts

Contracts provide goals and progression pressure.

Contract progression:

```text
Phenotypic
-> Genotypic
-> Probabilistic
```

Delivery contracts consume delivered plants. Statistical contracts validate the generated batch and do not consume plants automatically.

### Greenhouse

The greenhouse is the player's plant inventory. Limited space creates strategic decisions about storage, sale, future breeding, and delivery.

### Collection

The collection records discovered species, phenotypes, and genotypes. It gives long-term structure to experimentation.

### Genetic Encyclopedia

The encyclopedia exposes discovered knowledge, observed frequencies, and crossbreeding history. It grows through exploration.

The knowledge tree presents unlocked genetics concepts, including allele
definitions, independent assortment conditions, and the `9:3:3:1` dihybrid
ratio, using hover, focus, or selection details.

## Screens

Minimum planned screens:

- Main Screen
- Greenhouse Screen
- Contracts Screen
- Genetic Analyzer Screen
- Collection Screen
- Progression Screen
- Knowledge Tree Screen

Detailed screen rules are defined in [SCREEN_SPEC.md](SCREEN_SPEC.md) and [ui/README.md](ui/README.md).

## Progression

The official learning and tool progression is:

```text
Phenotype
-> Genotype
-> Probability
-> Genetic Planning
```

Species progression increases genetic complexity:

```text
Mendel Pea: 2 genes
-> Snapdragon: 3 genes
-> Corn: 4 genes
-> Tomato: 5 genes
-> Orchid: 6 genes
```

Detailed progression rules are defined in [mechanics/progression.md](mechanics/progression.md).

## Completion Conditions

The game may continue indefinitely, but completion goals include:

- All species unlocked.
- All planned phenotypes discovered.
- All planned genotypes discovered.
- Genetic analyzer fully upgraded.
- Greenhouse fully expanded.
- Genetic encyclopedia completed.

## Design Principles

- Learn by observing.
- Let genetics emerge from gameplay.
- Require hypothesis and experimentation.
- Increase complexity gradually.
- Reward curiosity and discovery.
- Make knowledge as valuable as currency.
