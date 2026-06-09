# Collection

## Purpose

The collection records the player's discovered genetic knowledge and supports long-term goals.

## Collection Categories

### Specimens

Registers individual discovered or preserved plant specimens when the game needs
to show lineage history for a concrete plant.

Specimen entries should show:

- Species identifier.
- Phenotype summary.
- Genotype when the analyzer level allows it.
- Generation label, such as `P0`, `F1`, or `F2`.
- Generation depth, meaning how many crossbreeding steps were required to obtain
  the specimen.
- Parent summary when known and useful.
- Discovery status.

Generation rules:

- Starting or directly acquired plants are generation depth `0` and display as
  `P0`.
- Offspring produced by one cross from `P0` parents display as `F1`.
- Offspring produced from a lineage that required two crossbreeding steps display
  as `F2`.
- For mixed-generation parents, offspring generation depth is one more than the
  highest parent generation depth.
- Generation labels are informational. They do not change genetic probability,
  contract validity, phenotype expression, or genotype formation.

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

- Species identifier.
- Trait name.
- Related gene when known.
- Species availability.
- Discovery status.

Phenotype discovery keys are species-qualified. A yellow, smooth Mendel Pea and
an equivalent dominant-trait pattern in another species are separate collection
entries.

### Genotypes

Registers genetic combinations discovered through generated specimens.

Genotype entries should show:

- Genotype string.
- Related species.
- Derived phenotype summary.
- Discovery status.

Genotype discovery keys are species-qualified. The same allele string is not
treated as the same collection entry across different species because each
species has its own gene count, trait mapping, and unlock context.

## Discovery Rules

A discovery is recorded the first time the player obtains a valid plant, phenotype, genotype, or species entry.

Rules:

- Discovery remains registered even if the plant is sold or delivered.
- Hidden entries should not reveal exact undiscovered details unless intentionally designed.
- Discovery rewards are granted once.
- Collection milestone rewards are granted once and tracked independently from
  regular discovery rewards.
- The first specimen record for a discovered plant stores its generation label.
- Later specimens with the same genotype may update observed lineage history but
  do not grant duplicate genotype discovery rewards.

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
