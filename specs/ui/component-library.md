# Component Library

## Component Rules

Reusable components must:

- Respect analyzer-level information visibility.
- Use consistent phenotype, genotype, rarity, and contract colors.
- Provide readable states.
- Avoid creating new gameplay rules.

## PlantCard

Purpose: represent one plant specimen.

Properties:

- Plant visual.
- Species.
- Known phenotype summary.
- Known genotype if analyzer level allows it.
- Rarity.
- Slot status.

States:

- Empty.
- Unknown details.
- Selected as parent.
- Reserved for contract.
- Deliverable.
- Sold or unavailable.

Behavior:

- Selects plant when clicked.
- Opens inspection details when requested.
- Shows locked data as `Unknown`.

Example:

```text
+------------------+
| Red Flower       |
| Broad Leaf       |
| Genotype: AaBb   |
| [Select Parent]  |
+------------------+
```

## TraitBadge

Purpose: show one visible phenotype.

Properties:

- Trait icon.
- Trait label.
- Trait color.

States:

- Discovered.
- Newly discovered.
- Contract-required.

Behavior:

- Tooltip explains trait source only if known.

## GenotypeLabel

Purpose: display genotype strings clearly.

Properties:

- Genotype text.
- Species gene count.
- Unknown marker.

States:

- Hidden.
- Partial unknown.
- Fully visible.
- Contract target.

Behavior:

- Uses fixed-width visual treatment.
- Never shown before analyzer level 2.

## PhenotypeCard

Purpose: show collection or contract phenotype details.

Properties:

- Trait name.
- Visual example.
- Related gene if discovered.
- Discovery status.

States:

- Hidden.
- Discovered.
- Required by contract.

## ContractCard

Purpose: represent available, active, completed, or failed contracts.

Properties:

- Customer type.
- Contract type.
- Objective.
- Progress.
- Reward.
- Difficulty.

States:

- Available.
- Active.
- Complete.
- Locked.
- Expired or failed if such rules are later defined.

Behavior:

- Opens contract details.
- Accept action available only for valid contracts.

## AnalyzerPanel

Purpose: show analyzer output based on level.

Properties:

- Analyzer level.
- Selected plant or parent pair.
- Revealed data.
- Predictions.

States:

- No selection.
- Plant selected.
- Parent pair selected.
- Simulation available.

Behavior:

- Level 1: phenotype only.
- Level 2: phenotype, genotype, and allele breakdown.
- Level 3: simple probabilities, read-only Punnett square, and recognized ratio
  summaries such as `9:3:3:1` when valid.
- Level 4: full predictions and simulator outputs.

## KnowledgeNode

Purpose: show one learned genetics concept in the knowledge tree.

Properties:

- Concept name.
- Unlock state.
- Prerequisites.
- Short explanation.
- Optional related specimen, cross, contract, or collection entry.

States:

- Locked.
- Available.
- Newly learned.
- Selected.

Behavior:

- Reveals details on hover, focus, or click selection.
- Does not reveal information above the current analyzer level.
- Uses localizable educational text.

## ConveyorBelt

Purpose: display offspring generation.

Properties:

- Offspring queue.
- Current offspring.
- Generation status.
- Speed state.

States:

- Idle.
- Crossbreeding.
- Revealing offspring.
- Paused.
- Complete.

Behavior:

- Shows offspring in shuffled order.
- Triggers discovery and contract feedback.

## RewardPopup

Purpose: show rewards after contracts, discoveries, and milestones.

Properties:

- Reward source.
- Credits gained.
- Unlocks.

States:

- Contract reward.
- Discovery reward.
- Milestone reward.

## DiscoveryPopup

Purpose: celebrate first-time discoveries.

Properties:

- Discovery type.
- Plant visual.
- Phenotype or genotype.
- Collection destination.

States:

- New phenotype.
- New genotype.
- New species.

## ProgressBar

Purpose: show progress toward a target.

Properties:

- Current value.
- Target value.
- Label.
- Color role.

States:

- Empty.
- In progress.
- Complete.

## GeneticTag

Purpose: compact display of genetic information.

Types:

- Phenotype.
- Genotype.
- Probability.
- Rarity.

Behavior:

- Uses consistent color roles from [design-system.md](design-system.md).
