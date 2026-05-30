# Specifications Index

The `specs/` directory is the official source of truth for Mendel's Greenhouse game rules, content, balance, progression, user flows, learning objectives, and conceptual models.

Read the documents in this order:

1. [GDD.md](GDD.md) - Game vision, player fantasy, systems, screens, progression, and completion goals.
2. [GBD.md](GBD.md) - Costs, rewards, economy, rarities, multipliers, and expected pacing.
3. [mechanics/README.md](mechanics/README.md) - Gameplay mechanics, contracts, progression, collection, and conceptual model.
4. [content/README.md](content/README.md) - Species, genes, alleles, phenotypes, and MVP genetic content.
5. [education/README.md](education/README.md) - Genetics concepts mapped to systems and learning progression.
6. [UI_FLOW.md](UI_FLOW.md) - High-level pointer to navigation flow.
7. [SCREEN_SPEC.md](SCREEN_SPEC.md) - High-level pointer to screen specifications.
8. [ui/README.md](ui/README.md) - Detailed UI/UX, component, screen, accessibility, and asset specifications.
9. [technical/README.md](technical/README.md) - Approved engine, web target, and future platform direction.

## Documentation Rules

- Root files stay high-level.
- Detailed gameplay rules stay in `specs/`.
- Mechanics live in `specs/mechanics/`.
- Game content lives in `specs/content/`.
- Learning objectives live in `specs/education/`.
- Detailed interface rules stay in `specs/ui/`.
- Approved implementation direction lives in `specs/technical/`.
- Localization rules live in `specs/technical/localization.md`.
- Automated testing rules live in `specs/technical/testing.md`.
- Future platform decisions live in `specs/technical/future-platform.md`.
- Development tooling lives in `specs/technical/development-tooling.md`.
- MVP readiness decisions live in `specs/technical/implementation-readiness.md`.
- If documents disagree, update them before implementation.
