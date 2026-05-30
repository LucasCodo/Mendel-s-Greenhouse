# Breeding History Screen

## Purpose

The Breeding History Screen records past crossbreeding attempts so players can learn from observed outcomes.

## Layout

```text
+------------------------------------------------------------+
| Breeding History        Filters: Species / Genotype / Date |
+--------------------------+---------------------------------+
| Cross List               | Cross Details                   |
| AABB x aabb              | Parents                         |
| AaBb x AaBb              | Offspring summary               |
|                          | Discoveries                     |
+--------------------------+---------------------------------+
```

## Filters

- Species.
- Genotype.
- Phenotype.
- Date.
- Contract relevance.

## Entry Data

Each history entry should include:

- Parent A.
- Parent B.
- Species.
- Offspring count.
- Notable phenotypes.
- Notable genotypes if known.
- Discoveries produced.
- Contract progress caused.

## States

- No history yet.
- Filtered list empty.
- Entry selected.
- Entry contains new discovery.

## Educational Role

This screen supports pattern recognition and reinforces probability learning by showing repeated attempts and observed distributions.
