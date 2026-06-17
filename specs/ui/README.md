# UI/UX Specification Index

This directory is the source of truth for Mendel's Greenhouse interface, navigation, reusable UI components, accessibility, and visual asset requirements.

Use these documents with the gameplay specs:

- [../GDD.md](../GDD.md)
- [../GBD.md](../GBD.md)
- [../mechanics/gameplay.md](../mechanics/gameplay.md)
- [../mechanics/progression.md](../mechanics/progression.md)

## Reading Order

1. [design-system.md](design-system.md)
2. [color-palette.md](color-palette.md)
3. [navigation-flow.md](navigation-flow.md)
4. [component-library.md](component-library.md)
5. [accessibility.md](accessibility.md)
6. [asset-generation-guide.md](asset-generation-guide.md)
7. [characters/mendel-guide.md](characters/mendel-guide.md)
8. [scenes/README.md](scenes/README.md)
9. [screens/main-game-screen.md](screens/main-game-screen.md)
10. [screens/contract-screen.md](screens/contract-screen.md)
11. [screens/genetic-analyzer-screen.md](screens/genetic-analyzer-screen.md)
12. [screens/greenhouse-screen.md](screens/greenhouse-screen.md)
13. [screens/collection-screen.md](screens/collection-screen.md)
14. [screens/knowledge-tree-screen.md](screens/knowledge-tree-screen.md)
15. [screens/breeding-history-screen.md](screens/breeding-history-screen.md)
16. [screens/shop-screen.md](screens/shop-screen.md)
17. [screens/tutorial-screen.md](screens/tutorial-screen.md)
18. [screens/settings-screen.md](screens/settings-screen.md)
19. [screens/game-overlays.md](screens/game-overlays.md)
20. [assets/plants.md](assets/plants.md)
21. [assets/ui-elements.md](assets/ui-elements.md)
22. [assets/icons.md](assets/icons.md)
23. [assets/backgrounds.md](assets/backgrounds.md)
24. [assets/animations.md](assets/animations.md)
25. [assets/visual-effects.md](assets/visual-effects.md)
26. [assets/audio.md](assets/audio.md)

## Scene Wiki

Detailed Obsidian-friendly scene decomposition lives in
[scenes/README.md](scenes/README.md). Use it to break reference images into
implementation-sized components without bloating the formal screen specs.

Current scene targets:

- [scenes/main-game/visual-target.md](scenes/main-game/visual-target.md)
- [scenes/garden/visual-target.md](scenes/garden/visual-target.md)
- [scenes/collection/visual-target.md](scenes/collection/visual-target.md)

## Implementation Rule

Agents implementing UI must not invent new gameplay rules. If a screen needs gameplay behavior not defined here, check the relevant `specs/` document and update the appropriate spec before implementation.

## Interface Priorities

- Make phenotypes recognizable without reading text.
- Keep contract progress visible during the main loop.
- Reveal genetic information only when unlocked by the analyzer level.
- Prefer clear visual feedback over decorative complexity.
- Follow the approved pixel art direction and Pyxel constraints in [../technical/pyxel.md](../technical/pyxel.md).
