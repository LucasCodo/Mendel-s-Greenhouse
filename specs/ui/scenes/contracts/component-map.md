---
title: Contracts Component Map
tags:
  - ui/scenes/contracts
  - ui/components
type: component-map
project: mendels-greenhouse
status: draft
---

# Contracts Component Map

## Hierarchy

```text
ContractsScene
|- SceneShell
|- ContractSummaryPanel
|  |- ContractTitle
|  `- ContractProgressBar
|- ContractDetailPanel
|  |- RewardSummary
|  |- ContractInstruction
|  |- ContractStatusMessage
|  `- ClaimButton
`- RightNavigationRail
```

## Implementation Notes

- Progress values come from the contract model and summary helpers.
- Claim availability is a display state only; the scene owns reward payment.
- Contract text must remain localizable.
