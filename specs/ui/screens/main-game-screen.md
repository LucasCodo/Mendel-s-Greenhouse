# Main Game Screen

## Purpose

The Main Game Screen is the central gameplay workspace. It must support contract
tracking, parent selection, crossbreeding, offspring observation in the
Germination Bed, and immediate plant decisions.

Detailed scene decomposition and the official visual target live in
[../scenes/main-game/README.md](../scenes/main-game/README.md).

## Layout

Top:

```text
Logo | Credits | Garden Capacity | Active Contract | Right Navigation Rail
```

The screen must be designed for the internal Pyxel resolution defined in [../../technical/pyxel.md](../../technical/pyxel.md), then scaled to fill the browser page.

Upper center:

```text
Parent A | Cross Action | Parent B
```

Main workspace:

```text
Genetic Analyzer | Germination Bed | Selected Specimen
```

Primary actions:

```text
[Cross Plants] | [Harvest] | [Store] | [Discard]
```

Left side support:

```text
Analyzer level | Phenotype/genotype visibility | Probabilities | Simulator hint
```

Right side support:

```text
Selected specimen details | Store | Discard | Scene navigation
```

## ASCII Wireframe

```text
+----------------------------------------------------------------------------------+
| LOGO | Credits | Capacity | ACTIVE CONTRACT + progress | Navigation Rail         |
+----------------------+-----------------------------------+-----------------------+
| Genetic Analyzer     | Parent A | Cross | Parent B       | Navigation buttons    |
| glass + CRT + input  +-----------------------------------+                       |
| controls             | Germination Bed | Specimen Detail |                       |
|                      | growth grid      | Store / Discard |                       |
+----------------------+-----------------------------------+-----------------------+
```

## Visual Loop

1. Crossbreeding starts.
2. Offspring batch is generated.
3. Seeds appear in the Germination Bed.
4. A short growth animation reveals seedlings or adult phenotype sprites.
5. All cells grow simultaneously over a short timed animation.
6. The player clicks `Harvest` after the growth animation completes.
7. Contract progress updates when matching grown specimens are rescued by the
   active contract.
8. Non-contract specimens are sold during harvest.
9. Rewards appear when contract or discovery criteria are met.

## Interaction Model

Primary input is mouse.

Expected mouse interactions:

- Click parent slots or plant cards to select parents.
- Click `Crossbreed` to start the cross.
- Hover over a growing bed specimen to inspect details in a floating panel.
- Click a bed specimen or the selected specimen panel as a non-hover fallback.
- Click analyzer hardware controls to cycle specimens, trigger tactile feedback,
  or choose among already unlocked information levels.
- Click `Store` to preserve a selected specimen or `Discard` to remove it with
  no sale value.
- Click `Harvest` to resolve the grown batch into contract rescues and sales.
- Click top navigation icons to move between major screens.

Keyboard support is required as an alternative:

- Focus can move through top navigation, parent slots, the crossbreed button,
  bed cells, bed controls, and bottom-panel actions.
- Focused controls can be activated from the keyboard.
- Cancel/back behavior must be keyboard reachable.
- Batch growth is automatic after crossbreeding; contract/sale resolution
  requires the visible harvest button.

## Screen States

### Idle

- No active generation.
- Parent slots may be empty or selected.
- Crossbreed button disabled until both valid parents are selected.

### Crossbreeding

- Parent slots locked.
- Germination Bed enters seeded state.
- Crossbreed button becomes disabled or changes to current status.

### Revealing Offspring

- Bed cells reveal seedlings or adult phenotype sprites in a readable sequence.
- Newly visible traits animate lightly through grow-in, bloom, or highlight
  states.
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
- `GerminationBed`
- `PunnettSummary`
- `TraitBadge`
- `GenotypeLabel`
- `RewardPopup`
- `DiscoveryPopup`
- `ProbabilityPanel`
- `ResourceCounter`
- `NavigationIconButton`
- `BedControls`

## Browser Display

- The game canvas occupies the full browser page.
- The top menu or settings path must expose a fullscreen option.
- Pixel art must remain crisp when scaled.
- The internal canvas target is `640 x 360`.
- The layout should preserve a 16:9 composition when scaled into the browser.

## Information Visibility

- Analyzer level 1: phenotypes only.
- Analyzer level 2: phenotypes, genotypes, and allele breakdown.
- Analyzer level 3: parent-pair probability preview available.
- Analyzer level 4: simulator shortcut available.
