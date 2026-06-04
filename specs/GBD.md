# Game Balance Document

## Purpose

This document defines balance values for Mendel's Greenhouse. It covers costs, rewards, economy, rarity, multipliers, and expected progression pacing.

## Currency

Credits are the main currency.

Initial player credits:

```text
0
```

The first tutorial contract should provide the player's first credits.

Sources:

- Contracts
- First-time discoveries
- Collection milestones

Uses:

- Greenhouse expansion
- Genetic analyzer upgrades
- Species unlocks

## Greenhouse Expansion Costs

Initial capacity: 4 slots.

Maximum capacity: 20 slots.

Only one plant of each genotype may be stored in the greenhouse. Duplicate
genotypes must be sold, delivered to contracts, or left out of storage instead
of occupying another slot.

Final layout: 5 x 4.

| Slot | Cost |
| ---- | ---: |
| 5 | 50 |
| 6 | 75 |
| 7 | 100 |
| 8 | 125 |
| 9 | 150 |
| 10 | 200 |
| 11 | 250 |
| 12 | 300 |
| 13 | 400 |
| 14 | 500 |
| 15 | 600 |
| 16 | 700 |
| 17 | 850 |
| 18 | 1000 |
| 19 | 1200 |
| 20 | 1500 |

## Genetic Analyzer Costs

| Level | Name | Cost | Unlock |
| ----- | ---- | ---: | ------ |
| 1 | Phenotypic Observation | 0 | Phenotypic contracts |
| 2 | Genetic Sequencing | 500 | Genotypic contracts |
| 3 | Probabilistic Analysis | 2000 | Probabilistic contracts |
| 4 | Genetic Simulator | 5000 | Advanced optimization |

Analyzer use is unlimited after a level is unlocked. It has no per-use credit cost, time wait, energy cost, or other resource cost.

## Species Unlock Costs

| Species | Gene Count | Cost |
| ------- | ---------: | ---: |
| Mendel Pea | 2 | 0 |
| Snapdragon | 3 | 3000 |
| Corn | 4 | 10000 |
| Tomato | 5 | TBD |
| Orchid | 6 | TBD |

The player must have two empty greenhouse slots before buying a species unlock.
Those slots are immediately occupied by the new species' fully dominant and
fully recessive founder plants. If fewer than two slots are free, the unlock is
blocked even when the player has enough credits.

## Offspring Production

Each crossbreeding process displays a batch sized from the active cross's
genetic outcome combinations when that count fits on screen. If the combination
count is too large, the Germination Bed uses a capped representative batch.

Balance intent:

- Large enough for visible statistical patterns when probabilities matter.
- Small enough to keep results readable.
- Variable enough that simple crosses do not add visual noise.
- Compatible with greenhouse storage pressure.
- Useful for contract fulfillment without removing strategic scarcity.

## Contract Rewards

### Phenotypic Contracts

| Difficulty | Objective | Reward |
| ---------- | --------- | -----: |
| Easy | 3 plants | 50 |
| Medium | 5 plants | 100 |
| Hard | 10 plants | 250 |

### Genotypic Contracts

| Difficulty | Objective | Reward |
| ---------- | --------- | -----: |
| Easy | 2 specimens | 300 |
| Medium | 4 specimens | 600 |
| Hard | 8 specimens | 1000 |

### Probabilistic Contracts

| Difficulty | Reward |
| ---------- | -----: |
| Easy | 1500 |
| Medium | 3000 |
| Hard | 5000 |

## Plant Sale Values

Plant sale values are intentionally low. In the MVP, sale happens
automatically during harvest for grown specimens that are not delivered to the
active contract. Sale exists to avoid waste, not to become the main income
source.

| Destination | Relative Value |
| ----------- | -------------: |
| Contract | 100% |
| Common sale | 5% to 10% |
| Discard | 0% |

Example:

```text
If a contract pays 100 credits for a comparable plant, common sale should pay about 5 to 10 credits.
```

## Discovery Rewards

| Discovery | Reward |
| --------- | -----: |
| New phenotype | 20 |
| New genotype | 50 |
| New species registered | 200 |

## Collection Milestones

| Completion | Reward |
| ---------- | -----: |
| 25% | 250 |
| 50% | 500 |
| 75% | 1000 |
| 100% | 5000 |

## Customer Distribution

Base distribution after all contract types exist:

| Customer | Request Type | Probability |
| -------- | ------------ | ----------: |
| Common Customer | Phenotypes | 60% |
| Specialist Customer | Genotypes | 30% |
| Scientific Customer | Probabilities | 10% |

## Contract Mix By Progress

| Progress State | Phenotypic | Genotypic | Probabilistic |
| -------------- | ---------: | --------: | -------------: |
| Start | 100% | 0% | 0% |
| Analyzer Level 2 | 80% | 20% | 0% |
| Analyzer Level 3 | 50% | 40% | 10% |
| Analyzer Level 4 | 20% | 40% | 40% |

Level 4 does not create a new contract type. It improves planning for complex genotypic and probabilistic contracts.

## Genotype Rarity

| Rarity | Probability | Multiplier |
| ------ | ----------- | ----------: |
| Common | >= 25% | x1 |
| Uncommon | >= 12.5% | x1.5 |
| Rare | >= 6.25% | x2 |
| Very Rare | < 6.25% | x3 |

## Reward Formula

```text
Final Reward = Base Reward x Rarity Multiplier x Species Complexity
```

Species complexity:

| Species | Complexity |
| ------- | ---------: |
| Mendel Pea | 1 |
| Snapdragon | 2 |
| Corn | 3 |
| Tomato | 4 |
| Orchid | 5 |

Example:

```text
100 credits x rare genotype (x2) x Corn (x3) = 600 credits
```

## Expected Progression Pace

| Time | Expected Goal |
| ---- | ------------- |
| First hour | Understand basic crosses and buy up to 8 slots |
| Second hour | Buy analyzer level 2 |
| Third hour | Buy analyzer level 3 |
| Fourth hour | Unlock Snapdragon |
| Sixth hour | Buy analyzer level 4 |
| Eighth hour | Start Corn |

## Expected Campaign Length

| Player Type | Duration |
| ----------- | -------- |
| Casual | 10 to 15 hours |
| Completionist | 20 to 30 hours |

## Balance Validation

Playtests should verify:

- The player can reach 8 slots during the first hour.
- Variable representative bed sizes make patterns visible without overflowing
  the main screen.
- The initial 4-slot greenhouse creates decisions without frustration.
- Analyzer level 2 arrives before phenotypic contracts feel repetitive.
- Probabilistic contracts appear only after players understand genotypes.
- The genetic simulator reduces endgame repetition without solving the game automatically.
