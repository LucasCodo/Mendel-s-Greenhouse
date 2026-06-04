# Contract Generation

## Purpose

Contracts provide goals, rewards, and learning pressure. They must be generated from valid unlocked content only.

## Contract Types

### Phenotypic Contracts

The client requests visible traits.

Example:

```text
Deliver 10 plants with red flowers.
```

Rules:

- Available from analyzer level 1.
- Based on discovered phenotypes.
- Does not require genotype knowledge.
- Assigned primarily to Common Customers.
- Usually resolved as delivery contracts in the early game.

### Genotypic Contracts

The client requests exact genotypes.

Example:

```text
Deliver 5 plants with genotype AaBb.
```

Rules:

- Available from analyzer level 2.
- Based on registered genotypes.
- Requires full genotype visibility.
- Assigned primarily to Specialist Customers.

### Probabilistic Contracts

The client requests a probability or population distribution.

Examples:

```text
Produce a population where 75% of plants have red flowers.
Generate a cross with 25% chance to produce the rare phenotype.
```

Rules:

- Available from analyzer level 3.
- Based on observed or analyzable combinations.
- Requires probability analysis.
- Assigned primarily to Scientific Customers.
- Usually resolved as statistical contracts that validate a generated batch without consuming plants automatically.
- Contracts that require the `9:3:3:1` ratio are valid only for independently
  assorting two-gene, complete-dominance crosses such as `AaBb x AaBb`.

## Resolution Modes

### Delivery Contracts

Delivery contracts consume plants submitted to the contract.

Examples:

- Deliver 5 yellow peas.
- Deliver 3 yellow and smooth peas.

### Statistical Contracts

Statistical contracts validate the generated batch.

Examples:

- Produce a batch containing at least 25% of a phenotype.
- Produce a batch matching the 9:3:3:1 ratio.
- Generate a batch with a 75% probability for a target trait.

Rules:

- The batch is evaluated.
- Plants are not consumed automatically.
- The player chooses what to store before harvest.
- Harvesting resolves matching specimens into the active contract and sells
  excess specimens automatically.

## Customer Types

| Customer | Request Focus |
| -------- | ------------- |
| Common Customer | Phenotypes |
| Specialist Customer | Genotypes |
| Scientific Customer | Probabilities |

## Scaling Rules

Contract complexity scales with:

- Analyzer level.
- Unlocked species.
- Discovered content.
- Greenhouse capacity.
- Previous contract success.

## Validity Criteria

A generated contract is valid only if:

- The required species is unlocked.
- The required phenotype or genotype is discovered when required.
- The player has the analyzer level needed to verify completion.
- At least one available or reasonably reachable parent combination can satisfy it.
- The objective quantity is feasible within the current production and storage rules.
- Ratio objectives such as `9:3:3:1` match the biological conditions documented
  in [progression.md](progression.md).

## Impossibility Prevention

Never generate impossible contracts.

The generator must reject candidates that require:

- Locked species.
- Unknown analyzer capabilities.
- Undiscovered required content.
- Impossible genotype outcomes.
- Probability thresholds no valid cross can meet.

## Progression Mix

The official contract progression is:

```text
Phenotypic
->
Genotypic
->
Probabilistic
```

Detailed percentages are defined in [../GBD.md](../GBD.md).
