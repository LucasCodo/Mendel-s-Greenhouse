# UI/UX Specification Index

This directory is the source of truth for Mendel's Greenhouse interface, navigation, reusable UI components, accessibility, and visual asset requirements.

Use these documents with the gameplay specs:

- [../GDD.md](../GDD.md)
- [../GBD.md](../GBD.md)
- [../mechanics/gameplay.md](../mechanics/gameplay.md)
- [../mechanics/progression.md](../mechanics/progression.md)

## Reading Order

1. [design-system.md](design-system.md)
2. [navigation-flow.md](navigation-flow.md)
3. [component-library.md](component-library.md)
4. [accessibility.md](accessibility.md)
5. [asset-generation-guide.md](asset-generation-guide.md)
6. [screens/main-game-screen.md](screens/main-game-screen.md)
7. [screens/contract-screen.md](screens/contract-screen.md)
8. [screens/genetic-analyzer-screen.md](screens/genetic-analyzer-screen.md)
9. [screens/greenhouse-screen.md](screens/greenhouse-screen.md)
10. [screens/collection-screen.md](screens/collection-screen.md)
11. [screens/breeding-history-screen.md](screens/breeding-history-screen.md)
12. [screens/shop-screen.md](screens/shop-screen.md)
13. [screens/tutorial-screen.md](screens/tutorial-screen.md)
14. [screens/settings-screen.md](screens/settings-screen.md)
15. [screens/game-overlays.md](screens/game-overlays.md)
16. [assets/plants.md](assets/plants.md)
17. [assets/ui-elements.md](assets/ui-elements.md)
18. [assets/icons.md](assets/icons.md)
19. [assets/backgrounds.md](assets/backgrounds.md)
20. [assets/animations.md](assets/animations.md)
21. [assets/visual-effects.md](assets/visual-effects.md)

## Implementation Rule

Agents implementing UI must not invent new gameplay rules. If a screen needs gameplay behavior not defined here, check the relevant `specs/` document and update the appropriate spec before implementation.

## Interface Priorities

- Make phenotypes recognizable without reading text.
- Keep contract progress visible during the main loop.
- Reveal genetic information only when unlocked by the analyzer level.
- Prefer clear visual feedback over decorative complexity.
- Follow the approved pixel art direction and Pyxel constraints in [../technical/pyxel.md](../technical/pyxel.md).
