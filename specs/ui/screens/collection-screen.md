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
|                |                   | First discovered      |
+----------------+-------------------+-----------------------+
```

## Entry Data

Each discovered specimen or entry may show:

- Phenotype.
- Genotype.
- Discovery date.
- Plant of origin.
- Rarity.
- Species.

## Tabs

- Species.
- Phenotypes.
- Genotypes.

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
