---
title: Open Questions
tags:
  - agent-memory/question
type: question
project: mendels-greenhouse
status: active
updated: 2026-05-30
---

# Open Questions

## Still Open

- What save data format will be used later?
- What packaging and distribution workflow will be used later?
- What code architecture and module layout will be used later?
- How will Pyxel be embedded or delivered in the future web experience?
- What account/authentication model will NiceGUI use later?

## Resolved On 2026-05-30

### Engine And Art Direction

The game will use Pyxel as its engine and pixel art as its visual style.

### Platform Direction

Mendel's Greenhouse is intended to be a web game. For now, implementation focuses only on the game. A future NiceGUI layer is planned for user accounts and save management.

### Project Structure And Asset Direction

The implementation should use Poetry flat layout with package name `mendels_greenhouse`. Runtime assets live inside `mendels_greenhouse/assets/` and use Pyxel's native `.pyxres` format.

The game targets internal resolution `256 x 144`, scaled to fill the browser page with crisp pixel art and a fullscreen option.

### First Playable Prototype Scope

The first playable prototype validates the main loop:

1. The player has two parent plants.
2. The player selects two plants for crossbreeding.
3. One offspring batch is generated.
4. Offspring appear on the production conveyor.
5. The player sees produced phenotypes.
6. The system automatically checks contract progress.
7. The player receives rewards.
8. The player can store useful offspring for future crosses.

MVP content:

- Mendel Pea only.
- 2 independent genes: `A/a` and `B/b`.
- Genetic Analyzer level 1 only.
- Phenotypic contracts only.
- Small greenhouse.
- Functional collection.
- Functional progression.

### Contract Consumption

Delivery contracts consume delivered plants. Statistical contracts validate the generated batch and do not consume plants automatically.

### Plant Sale Value

Plant sale values should be intentionally low. Sale exists to prevent waste, not to become the main income source.

Recommended value:

- Contract value: 100%.
- Common sale: 5% to 10%.
- Discard: 0%.

### Genetic Analyzer Use Cost

The genetic analyzer has unlimited use and no per-use cost, wait time, or energy cost. Progression is based on analyzer levels only.

### Final Species Naming Scheme

Species progression:

| Species | Genes | Objective |
| ------- | ----: | --------- |
| Mendel Pea | 2 | Tutorial |
| Snapdragon | 3 | Intermediate |
| Corn | 4 | Full Mendel's Second Law |
| Tomato | 5 | Advanced planning |
| Orchid | 6 | Endgame and collection |
