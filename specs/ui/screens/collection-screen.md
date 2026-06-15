# Collection Screen

## Purpose

The Collection Screen is the genetic Pokedex of Mendel's Greenhouse.

Detailed scene decomposition and the official visual target live in
[../scenes/collection/README.md](../scenes/collection/README.md).

## Layout

```text
+------------------------------------------------------------+
| Collection                         Discovered: X/Y         |
+----------------+-------------------+-----------------------+
| Species        | Sticker Album Grid                 | |
| Phenotypes     | [Card][????][Card][????]       [|] | |
| Genotypes      | [????][Card][????][Card]       [|] | |
| Specimens      | [Card][????][????][Card]       [|] | |
|                |                          Scroll [|] | |
+----------------+-------------------+-----------------------+
```

The active category uses a fixed card grid that includes every official slot,
whether discovered or hidden. A vertical scrollbar on the right side of the
album supports mouse-wheel scrolling, scrollbar clicks, and keyboard
navigation. Hidden slots preserve their numbered position but do not reveal
their exact genetic content.

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
