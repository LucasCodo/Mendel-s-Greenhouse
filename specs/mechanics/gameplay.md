# Gameplay Specification

## Purpose

This is the formal gameplay rules document for Mendel's Greenhouse. If implementation requires a rule, check this document first.

## Crossbreeding

The player selects two parent plants from available stored specimens.

Requirements:

- Both parent slots must contain valid plants.
- Parent plants must belong to the same species unless a future spec explicitly allows hybrid species.
- The crossbreeding action generates one offspring batch.
- The displayed offspring batch size follows the number of genetic outcome
  combinations for the selected parents when that count fits on screen.
- If the number of genetic combinations is too large for the main screen, the
  Germination Bed uses a capped representative batch that preserves the active
  cross distribution as well as possible without overflowing the UI.

## Allele Inheritance

Each gene has two alleles in the parent genotype.

For each offspring:

1. Select one allele from Parent A for each gene.
2. Select one allele from Parent B for each gene.
3. Combine selected alleles into the offspring genotype.
4. Normalize allele display using dominant allele first when applicable, such as `Aa` instead of `aA`.

## Genotype Formation

A genotype is the complete ordered set of gene pairs for a plant.

Examples:

- Mendel Pea: `AABB`, `AaBb`, `aabb`
- Snapdragon: `AABBCC`, `AaBbCc`
- Corn: `AABBCCDD`, `AaBbCcDd`
- Tomato: `AABBCCDDEE`, `AaBbCcDdEe`
- Orchid: `AABBCCDDEEFF`, `AaBbCcDdEeFf`

## Phenotype Formation

Phenotypes are derived from genotype rules defined in [../content/content-bible.md](../content/content-bible.md).

General MVP rule:

- At least one dominant allele expresses the dominant phenotype.
- Two recessive alleles express the recessive phenotype.

Example:

```text
AA or Aa -> dominant phenotype
aa -> recessive phenotype
```

## Offspring Generation

The system must calculate genetically valid offspring before displaying results.

Rules:

- Every offspring must be possible from the selected parents.
- Expected combinations and probabilities must be mathematically valid.
- Offspring display order must be shuffled.
- Shuffled display order must not reveal probability order.

## Germination Bed

The Germination Bed displays the generated offspring batch as a readable
planting grid instead of an industrial production conveyor.

The bed reinforces the greenhouse fantasy, makes Mendelian proportions visible
as spatial patterns, and gives each offspring a concrete specimen slot the
player can inspect.

Rules:

- Each visible bed cell represents one generated offspring specimen.
- The bed should use a representative grid for the active cross instead of an
  arbitrary fixed visual count.
- The bed dimensions are variable and are derived from the current displayed
  batch size.
- The bed must never grow beyond the available main-screen area.
- For simple equal-probability crosses, the visual bed may show one specimen per
  distinct expected outcome.
- For crosses with more possible combinations than can fit on the main screen,
  the bed uses the maximum supported representative cell count instead of
  drawing every possible combination.
- For percentage-based contracts, the bed may expand to enough cells to make the
  target proportion readable, such as a `4 x 4` bed for 75% / 25% patterns.
- Offspring display order may still be shuffled, but the final bed must preserve
  the generated batch contents and contract validation data.
- Contract-matching plants should receive a clear non-color-only highlight.
- During the MVP loop, generated specimens appear in the bed simultaneously as
  seeds and grow over a short timed animation.
- When the growth animation completes, the player can press the harvest button
  to resolve the grown batch.
- Harvesting rescues delivery-contract matches into the active contract until
  its remaining requirement is satisfied.
- Harvesting sells specimens that do not count toward the active delivery
  contract at the current common sale value.
- The player can select a growing bed cell to inspect it while the batch is
  visible.
- Hovering a growing bed cell shows a floating information panel with the
  plant information currently unlocked by the analyzer level.
- The bed should show only information unlocked by the current analyzer level.

Examples:

- Level 1: visible phenotypes only.
- Level 2: full genotypes may be inspected.
- Level 3: expected probabilities may be shown for selected crosses.
- Level 4: simulated results may be previewed before spending the cross.

### Punnett Square Relationship

The Genetic Analyzer's Punnett square and the Germination Bed must use the same
gamete and genotype calculation source.

The Punnett square explains why the outcomes are possible; the Germination Bed
shows what the current lot produced or represents.

Rules:

- At analyzer level 3, the main screen may show a compact read-only Punnett
  summary beside the bed.
- Punnett cells should aggregate into phenotype/genotype groups that map to bed
  highlights and legends.
- A bed cell is not required to occupy the same position as a Punnett cell. The
  bed is a garden layout, not a genetics matrix.
- When the generated or representative bed is shuffled, the Punnett summary
  remains the stable explanatory reference.
- Selecting a bed specimen may highlight the corresponding Punnett outcome group
  when that information is unlocked.

## Contract Resolution

Contracts define required delivery criteria.

### Delivery Contracts

Delivery contracts consume matching plants.

Examples:

- Deliver 5 yellow peas.
- Deliver 3 yellow and smooth peas.

Rules:

- A plant must match the contract requirement to count.
- Delivered plants are removed from greenhouse storage or from the current
  Germination Bed batch when they are rescued directly after growth.
- Partial delivery is not complete unless the contract explicitly supports partial progress.
- Invalid plants cannot be delivered to a contract.

### Statistical Contracts

Statistical contracts evaluate the whole generated batch instead of consuming plants.

Examples:

- Produce a batch containing at least 25% red flowers.
- Produce a batch matching a 9:3:3:1 ratio.
- Generate a batch with 75% probability for trait X.

Rules:

- The generated batch is validated.
- No plant is consumed automatically.
- The player chooses whether to store, sell, or discard descendants afterward.

## Storage

Plants occupy greenhouse slots.

Rules:

- A slot can hold one plant.
- The starting greenhouse has 4 slots.
- The maximum greenhouse has 20 slots.
- Initial plants are `AABB` and `aabb`.
- Two initial slots are empty.

## Sale

The player may sell stored plants to free space.

Rules:

- Sold plants are removed from storage.
- Sold plants remain registered in the collection if already discovered.
- Sale values are intentionally low.
- Common sale should pay 5% to 10% of comparable contract value.
- Discard value is 0%.
- Selling exists to avoid waste and free storage, not as the main income source.

## Discoveries

A discovery occurs the first time the player obtains or registers a new species, phenotype, or genotype.

Rules:

- Discoveries are permanent.
- Discoveries can trigger rewards defined in [../GBD.md](../GBD.md).
- Discovery status is independent from whether the specimen remains in storage.

## Impossibility Rules

The game must never generate impossible contracts.

A contract is impossible if:

- It asks for an undiscovered phenotype when the relevant contract type requires discovered content.
- It asks for a genotype not available in the unlocked species.
- It asks for a probability that no available parent combination can produce.
- It requires a species not yet unlocked.
- It requires analyzer knowledge the player has not unlocked.

When in doubt, contract generation must reject the contract candidate.
