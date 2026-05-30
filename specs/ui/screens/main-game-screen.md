# Main Game Screen

## Purpose

The Main Game Screen is the central gameplay workspace. It must support contract tracking, parent selection, crossbreeding, offspring observation, and immediate plant decisions.

## Layout

Top:

```text
Current Contract | Progress | Credits | Menu
```

The screen must be designed for the internal Pyxel resolution defined in [../../technical/pyxel.md](../../technical/pyxel.md), then scaled to fill the browser page.

Center:

```text
Parent Plant A + Parent Plant B
```

Center bottom:

```text
[Crossbreed]
```

Main area:

```text
Genetic Conveyor
```

Footer:

```text
Last Generated Plant | Quick Stats | Genetic Help
```

## ASCII Wireframe

```text
+--------------------------------------------------------------------------------+
| Contract: Red Flowers 3/10      Credits: 250      Analyzer Lv. 2      Menu     |
+----------------------+--------------------------------------+------------------+
| Parent A             |          Genetic Conveyor            | Parent B         |
| +------------------+ |  [ ] -> [ ] -> [ ] -> [Current]      | +--------------+ |
| | PlantCard        | |                                      | | PlantCard    | |
| | Phenotype        | |  Offspring reveal area               | | Phenotype    | |
| | Genotype if ok   | |                                      | | Genotype if | |
| +------------------+ |                                      | | ok          | |
|                      |              [Crossbreed]            | +--------------+ |
+----------------------+--------------------------------------+------------------+
| Last Plant: Red/Broad | Stats: 20 offspring | Help: Aa x Aa can reveal recessive |
+--------------------------------------------------------------------------------+
```

## Visual Loop

1. Crossbreeding starts.
2. Offspring batch is generated.
3. Offspring appear on the conveyor in shuffled order.
4. Phenotype is revealed.
5. Contract progress updates if the offspring matches.
6. Visual feedback confirms match, discovery, or invalid delivery.
7. Rewards appear when contract or discovery criteria are met.

## Screen States

### Idle

- No active generation.
- Parent slots may be empty or selected.
- Crossbreed button disabled until both valid parents are selected.

### Crossbreeding

- Parent slots locked.
- Conveyor animation starts.
- Crossbreed button becomes disabled or changes to current status.

### Revealing Offspring

- Offspring enter the conveyor one by one.
- Newly visible traits animate lightly.
- New discoveries trigger a non-destructive overlay.

### Contract Complete

- Contract progress reaches target.
- Completion overlay appears.
- Reward is shown.

### New Discovery

- Discovery popup appears.
- Collection entry is updated.
- Player can continue after acknowledgement or short auto-dismiss.

### Contract Failed

Only used if failure rules are later defined. If no failure rule exists, the state should not appear.

## Required Components

- `PlantCard`
- `ContractCard` compact variant
- `ConveyorBelt`
- `TraitBadge`
- `GenotypeLabel`
- `RewardPopup`
- `DiscoveryPopup`

## Browser Display

- The game canvas occupies the full browser page.
- The top menu or settings path must expose a fullscreen option.
- Pixel art must remain crisp when scaled.

## Information Visibility

- Analyzer level 1: phenotypes only.
- Analyzer level 2: phenotypes and genotypes.
- Analyzer level 3: parent-pair probability preview available.
- Analyzer level 4: simulator shortcut available.
