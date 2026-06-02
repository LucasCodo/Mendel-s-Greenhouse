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
7. [screens/main-game-screen.md](screens/main-game-screen.md)
8. [screens/contract-screen.md](screens/contract-screen.md)
9. [screens/genetic-analyzer-screen.md](screens/genetic-analyzer-screen.md)
10. [screens/greenhouse-screen.md](screens/greenhouse-screen.md)
11. [screens/collection-screen.md](screens/collection-screen.md)
12. [screens/knowledge-tree-screen.md](screens/knowledge-tree-screen.md)
13. [screens/breeding-history-screen.md](screens/breeding-history-screen.md)
14. [screens/shop-screen.md](screens/shop-screen.md)
15. [screens/tutorial-screen.md](screens/tutorial-screen.md)
16. [screens/settings-screen.md](screens/settings-screen.md)
17. [screens/game-overlays.md](screens/game-overlays.md)
18. [assets/plants.md](assets/plants.md)
19. [assets/ui-elements.md](assets/ui-elements.md)
20. [assets/icons.md](assets/icons.md)
21. [assets/backgrounds.md](assets/backgrounds.md)
22. [assets/animations.md](assets/animations.md)
23. [assets/visual-effects.md](assets/visual-effects.md)
24. [assets/audio.md](assets/audio.md)

## Implementation Rule

Agents implementing UI must not invent new gameplay rules. If a screen needs gameplay behavior not defined here, check the relevant `specs/` document and update the appropriate spec before implementation.

## Interface Priorities

- Make phenotypes recognizable without reading text.
- Keep contract progress visible during the main loop.
- Reveal genetic information only when unlocked by the analyzer level.
- Prefer clear visual feedback over decorative complexity.
- Follow the approved pixel art direction and Pyxel constraints in [../technical/pyxel.md](../technical/pyxel.md).
