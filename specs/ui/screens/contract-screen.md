# Contract Screen

## Purpose

The Contract Screen lets players review available, active, completed, and historical contracts.

## Layout

```text
+--------------------------------------------------------------+
| Contracts                         Filters: All / Type / Client |
+----------------------+---------------------------------------+
| Available Contracts  | Contract Details                      |
| - ContractCard       | Objective                             |
| - ContractCard       | Reward                                |
| - ContractCard       | Requirements                          |
|                      | [Accept] [Track]                      |
+----------------------+---------------------------------------+
| Active | Completed | History                               |
+--------------------------------------------------------------+
```

## Sections

### Available Contracts

Shows contracts the player can accept now.

Each card shows:

- Client type.
- Contract type.
- Objective.
- Reward.
- Difficulty.
- Requirements.

### Active Contracts

Shows accepted contracts and current progress.

### Completed Contracts

Shows completed contracts and rewards earned.

### History

Shows past contracts for review and learning.

## States

- Empty list.
- Available contract selected.
- Active contract selected.
- Contract complete.
- Contract locked by analyzer level.

## Contract Type Visuals

- Phenotypic: green.
- Genotypic: teal.
- Probabilistic: lavender.

## Required Actions

- Accept contract.
- Track active contract.
- Review requirements.
- Deliver eligible plants when available.

## Validity Feedback

Invalid or locked contracts must explain the blocker, such as:

- Analyzer level too low.
- Required species locked.
- Missing discovered content.
