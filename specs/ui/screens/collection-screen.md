# Collection Screen

## Purpose

The Collection Screen is the genetic Pokedex of Mendel's Greenhouse.

## Layout

```text
+------------------------------------------------------------+
| Collection                         Discovered: X/Y         |
+----------------+-------------------+-----------------------+
| Species        | Entry Grid        | Entry Details         |
| Phenotypes     | [Card][Card]      | Phenotype             |
| Genotypes      | [????][Card]      | Genotype              |
| Specimens      |                   | Generation: F2        |
|                |                   | First discovered      |
+----------------+-------------------+-----------------------+
```

## Entry Data

Each discovered specimen or entry may show:

- Phenotype.
- Genotype.
- Generation label, such as `P0`, `F1`, or `F2`.
- Generation depth, meaning how many crossbreeding steps were needed to produce
  that specimen.
- Parent summary when known.
- Discovery date.
- Plant of origin.
- Rarity.
- Species.

## Tabs

- Species.
- Phenotypes.
- Genotypes.
- Specimens.

## Progress Display

```text
Discovered: X/Y
```

Use progress bars for:

- Species completion.
- Phenotype completion.
- Genotype completion.

## Hidden Entries

Undiscovered entries should show:

- Mystery silhouette or placeholder.
- Broad category if appropriate.
- No exact genotype unless already discovered.

## States

- Empty category.
- New entry highlighted.
- Filtered results.
- Milestone reached.

## Required Components

- `PhenotypeCard`
- `GenotypeLabel`
- `TraitBadge`
- `ProgressBar`
- `DiscoveryPopup`
