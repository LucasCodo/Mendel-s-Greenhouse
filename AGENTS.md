# AGENTS.md

## Project Overview

Mendel's Greenhouse is an educational single-player game about learning Mendelian genetics through plant crossbreeding, contracts, collection, and greenhouse management.

The project is in design phase. The approved game engine is Pyxel and the approved art direction is pixel art. The intended platform is web.

For the current phase, implement only the game. NiceGUI is planned for a future web application layer that manages user accounts and saves.

Do not assume database schema, persistence format, authentication flow, hosting, packaging workflow, or code architecture until those are documented.

## Source Of Truth

The official game rules are in [`specs/`](specs/).

Before implementing or modifying any gameplay system, consult the relevant spec:

- [specs/GDD.md](specs/GDD.md) for overall game design.
- [specs/GBD.md](specs/GBD.md) for balance and economy.
- [specs/mechanics/README.md](specs/mechanics/README.md) for gameplay systems and mechanics.
- [specs/mechanics/gameplay.md](specs/mechanics/gameplay.md) for formal gameplay rules.
- [specs/content/content-bible.md](specs/content/content-bible.md) for species, genes, alleles, and traits.
- [specs/mechanics/contracts.md](specs/mechanics/contracts.md) for procedural contracts.
- [specs/mechanics/progression.md](specs/mechanics/progression.md) for unlocks and pacing.
- [specs/UI_FLOW.md](specs/UI_FLOW.md) and [specs/SCREEN_SPEC.md](specs/SCREEN_SPEC.md) for user flows and screens.
- [specs/ui/README.md](specs/ui/README.md) for detailed UI/UX, components, screens, accessibility, and visual assets.
- [specs/technical/README.md](specs/technical/README.md) for approved implementation direction.
- [specs/technical/platform-roadmap.md](specs/technical/platform-roadmap.md) for web and future NiceGUI scope.
- [specs/technical/localization.md](specs/technical/localization.md) for English and Brazilian Portuguese support.
- [specs/technical/testing.md](specs/technical/testing.md) for pytest-based automated testing expectations.
- [specs/technical/future-platform.md](specs/technical/future-platform.md) for future save, packaging, web delivery, architecture, and NiceGUI decisions.
- [specs/technical/development-tooling.md](specs/technical/development-tooling.md) for dev dependencies, Poe tasks, Ruff, Babel automation, and refactoring policy.
- [specs/technical/implementation-readiness.md](specs/technical/implementation-readiness.md) for resolved MVP readiness decisions.
- [specs/mechanics/collection.md](specs/mechanics/collection.md) for discovery and completion rules.
- [specs/education/learning-objectives.md](specs/education/learning-objectives.md) for educational intent.
- [specs/mechanics/data-model.md](specs/mechanics/data-model.md) for conceptual entities and relationships.

## Approved Developer Tooling

- **pyxel-mcp** ([github.com/kitao/pyxel-mcp](https://github.com/kitao/pyxel-mcp)): Model Context Protocol server for Pyxel, installed as a `game/` development dependency through Poetry.
- **pyxel-skill** ([github.com/kitao/pyxel-skill](https://github.com/kitao/pyxel-skill)): local Codex skill for Pyxel implementation guidance.

Tooling does not override project specs. If a Pyxel tool or skill conflicts with `specs/`, update the relevant spec before following the new behavior.

When Pyxel MCP tools are exposed, use them for Pyxel visual/audio work:

- Validate scripts before running.
- Capture screenshots for screen/layout changes.
- Inspect sprites, banks, tilemaps, palettes, and animations for `.pyxres` work.
- Render audio when changing music or sound effects.

Follow [specs/technical/pyxel-mcp.md](specs/technical/pyxel-mcp.md). If MCP tools are unavailable in the current session, state that and fall back to `poetry run poe check`, targeted pytest tests, and direct Pyxel smoke checks.

## Do Not Invent Rules

Do not create or change species, genes, alleles, phenotypes, genotypes, contracts, progression gates, rewards, analyzer behavior, core mechanics, engine constraints, platform scope, account/save scope, or art direction without checking and updating the related specs.

Do not add user-facing text without considering localization.

Use pytest for automated tests. Keep core gameplay rules testable without launching Pyxel windows.

Keep core gameplay rules independent from Pyxel rendering and future NiceGUI account/save infrastructure.

Use Poe the Poet for automation tasks. Do not introduce Taskipy.

Use human-readable Pyxel color enums instead of raw color indexes in UI code.
Use the expanded palette defined in [specs/ui/color-palette.md](specs/ui/color-palette.md);
do not reintroduce a 16-color-only assumption unless the spec changes.

If a rule is missing, document the proposed rule in the relevant spec before treating it as implementation guidance.

## Documentation Updates

Any change to gameplay rules must update all affected documents. Keep detailed rules in `specs/`; keep root files high-level.

Use the project name **Mendel's Greenhouse** consistently.

## Agent Memory

Keep durable project memory in [`agent-memory/`](agent-memory/). Search it before reconstructing project decisions, validated commands, or open questions.

Do not store chat transcripts, temporary logs, secrets, or speculative implementation details in memory.

## Official Progression

```text
Phenotype
->
Genotype
->
Probability
->
Genetic Planning
```

## Official Genetic Analyzer Levels

```text
Level 1: Phenotypic Observation
Level 2: Genetic Sequencing
Level 3: Probabilistic Analysis
Level 4: Genetic Simulator
```

## Safety And Boundaries

- Do not modify `.obsidian/` unless explicitly requested.
- Do not stage, commit, push, or open pull requests unless explicitly requested.
- Git output, branch names, commit messages, PR titles, and release notes must be written in English.
- Disclose meaningful AI assistance with `Assisted-by:` trailers or PR metadata.
- AI tools must not add `Signed-off-by` trailers, approve changes, merge changes, or claim authorship.
- For documentation changes, verify links and search for stale references before finishing.
