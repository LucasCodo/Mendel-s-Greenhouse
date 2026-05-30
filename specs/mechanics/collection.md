# Collection

## Purpose

The collection records the player's discovered genetic knowledge and supports long-term goals.

## Collection Categories

### Species

Registers each unlocked species.

Species entries should show:

- Species identifier.
- Gene count.
- Known genes.
- Completion progress.

### Phenotypes

Registers visible traits discovered through play.

Phenotype entries should show:

- Trait name.
- Related gene when known.
- Species availability.
- Discovery status.

### Genotypes

Registers genetic combinations discovered through generated specimens.

Genotype entries should show:

- Genotype string.
- Related species.
- Derived phenotype summary.
- Discovery status.

## Discovery Rules

A discovery is recorded the first time the player obtains a valid plant, phenotype, genotype, or species entry.

Rules:

- Discovery remains registered even if the plant is sold or delivered.
- Hidden entries should not reveal exact undiscovered details unless intentionally designed.
- Discovery rewards are granted once.

## Rewards

Discovery rewards are defined in [../GBD.md](../GBD.md):

- New phenotype.
- New genotype.
- New species registered.

## Milestones

Collection milestones are based on completion percentage:

- 25%
- 50%
- 75%
- 100%

Milestone rewards are defined in [../GBD.md](../GBD.md).

## Completion Criteria

Collection completion requires:

- All planned species registered.
- All planned phenotypes discovered.
- All planned genotypes discovered for the official content set.

Exact content scope is defined in [../content/content-bible.md](../content/content-bible.md).
