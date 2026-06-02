# Knowledge Tree Screen

## Purpose

The Knowledge Tree Screen records genetics concepts the player has already
encountered and gives concise explanations tied to progression.

It is the detailed version of the Progression Screen referenced by the GDD.

## Layout

```text
+------------------------------------------------------------+
| Knowledge Tree                         Learned: X/Y        |
+----------------------+-------------------------------------+
| Concept Nodes        | Selected Concept                    |
| Phenotype -> Allele  | Independent Assortment              |
| Genotype -> Ratio    | Conditions, example, related cross  |
| Probability -> Plan  |                                     |
+----------------------+-------------------------------------+
```

## Node Behavior

- Hover, keyboard focus, or click selection shows the concept explanation.
- Hover-only information is not allowed; the selected panel must expose the same
  content.
- Locked nodes show a silhouette, broad category, or prerequisite without
  revealing locked genotype, allele, or probability details.
- Unlocked nodes may cite examples from discovered specimens, breeding history,
  contracts, or collection entries.

## Initial Nodes

- Phenotype.
- Dominant allele.
- Recessive allele.
- Allele pair.
- Genotype.
- Homozygous.
- Heterozygous.
- Allele segregation.
- Independent assortment.
- `9:3:3:1` dihybrid ratio.
- Genetic probability.
- Genetic planning.

## 9:3:3:1 Node

Unlock source: analyzer level 3 plus a valid independent dihybrid probability
view or equivalent Scientific Customer contract.

Explanation content:

- The ratio describes four phenotype classes expected from a complete-dominance
  dihybrid cross.
- The canonical example is `AaBb x AaBb`.
- It depends on the genes being different, independently assorting, and governed
  by complete dominance.
- It does not apply to linked genes, incomplete dominance, codominance, or traits
  controlled by the same gene unless a future content spec explicitly defines
  compatible rules.

## Accessibility

- Every node must be reachable by keyboard or controller-equivalent navigation.
- The selected concept panel must be readable without timed hover.
- Educational text must be localizable.
