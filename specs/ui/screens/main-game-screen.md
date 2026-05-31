# Main Game Screen

## Purpose

The Main Game Screen is the central gameplay workspace. It must support contract tracking, parent selection, crossbreeding, offspring observation, and immediate plant decisions.

## Layout

Top:

```text
Logo | Credits | Special Resource | Garden Capacity | Timer | Guide | Garden | Shop | Settings
```

The screen must be designed for the internal Pyxel resolution defined in [../../technical/pyxel.md](../../technical/pyxel.md), then scaled to fill the browser page.

Upper center:

```text
Current Contract panel | Progress bar | Total generated
```

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

Left side support:

```text
Probabilities | Legend
```

Right side support:

```text
Trait explanation card
```

Footer:

```text
Generation Stats | Last Generated Plant | Genetic Help | Conveyor Controls
```

## ASCII Wireframe

```text
+------------------------------------------------------------------------------------------------+
| LOGO        Credits      Gems      Garden 12/20      Timer        Guide   Garden   Shop   Gear |
+------------------------------------------------------------------------------------------------+
| Probabilities     |        CURRENT CONTRACT: produce 6 purple flowers from 16 offspring       |
| + pie + legend    |        [==================== 3 / 6 ====================] Total: 16       |
|                   +-------------------------------------------------------------------------+
|                   |     Parent Plant A              +              Parent Plant B            |
|                   |   [large plant][AaBb]                        [large plant][AaBb]         |
|                   |   [traits visible]                           [traits visible]            |
|                   |                         [ CROSS PLANTS ]                                  |
+------------------------------------------------------------------------------------------------+
|                              GENETIC CONVEYOR / OFFSPRING BATCH                                |
| [plant] [plant] [plant] [plant] [plant] [plant] [plant] [plant] [plant] [plant] [plant]         |
+------------------------------------------------------------------------------------------------+
| Generation Stats        | Last Generated Plant         | How It Works                 | Cancel / Speed |
+------------------------------------------------------------------------------------------------+
```

## Visual Loop

1. Crossbreeding starts.
2. Offspring batch is generated.
3. Offspring appear on the conveyor in shuffled order.
4. Phenotype is revealed.
5. Contract progress updates if the offspring matches.
6. Visual feedback confirms match, discovery, or invalid delivery.
7. Rewards appear when contract or discovery criteria are met.

## Interaction Model

Primary input is mouse.

Expected mouse interactions:

- Click parent slots or plant cards to select parents.
- Click `Crossbreed` to start the cross.
- Click offspring or the latest plant panel to inspect details.
- Click store, sell, deliver, cancel, and speed controls.
- Click top navigation icons to move between major screens.

Keyboard support is required as an alternative:

- Focus can move through top navigation, parent slots, the crossbreed button, conveyor controls, and bottom-panel actions.
- Focused controls can be activated from the keyboard.
- Cancel/back behavior must be keyboard reachable.
- Repeated reveal/advance actions may have shortcuts, but those shortcuts must mirror visible controls.

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
- `ProbabilityPanel`
- `ResourceCounter`
- `NavigationIconButton`
- `ConveyorControls`

## Browser Display

- The game canvas occupies the full browser page.
- The top menu or settings path must expose a fullscreen option.
- Pixel art must remain crisp when scaled.
- The internal canvas target is `640 x 360`.
- The layout should preserve a 16:9 composition when scaled into the browser.

## Information Visibility

- Analyzer level 1: phenotypes only.
- Analyzer level 2: phenotypes and genotypes.
- Analyzer level 3: parent-pair probability preview available.
- Analyzer level 4: simulator shortcut available.
