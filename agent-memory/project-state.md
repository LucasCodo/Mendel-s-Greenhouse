---
title: Project State
tags:
  - agent-memory/state
type: state
project: mendels-greenhouse
status: active
updated: 2026-05-30
---

# Project State

Mendel's Greenhouse is an early-stage educational game project about learning Mendelian genetics through plant crossbreeding, contracts, collection, and greenhouse management.

The repository is documentation-first. The approved game engine is Pyxel, the approved art direction is pixel art, and the intended platform is web. Current implementation scope is the game only. NiceGUI is planned later for accounts and save management.

Initial language support: English and Brazilian Portuguese.

Automated testing direction: pytest for the main test suite, Hypothesis for property-based genetics/contract invariants, pytest-cov for coverage, and pytest-playwright later for browser smoke tests once a web build exists.

Future platform direction: saves use versioned JSON, Pyxel packaging uses `.pyxapp` without HTML export during the MVP, NiceGUI integration is revisited after the first release, and initial NiceGUI authentication uses username and password.

Implementation readiness direction: use Python 3.11, Poe for tasks, Ruff for lint/format with PEP 8 line length, Babel for i18n catalog automation, scene management for screens, Pyxel color enums for palette mapping, one autosave slot, and `0` starting credits for the MVP.

Official domains:

- https://mendelsgreenhouse.com
- https://mendelsgreenhouse.com.br

Current structure:

- [[README|README]]: public project overview.
- [[AGENTS|AGENTS]]: instructions for Codex and future agents.
- [[DESIGN|DESIGN]]: global design principles.
- [[CONTRIBUTING|CONTRIBUTING]]: contribution and documentation workflow.
- `specs/`: official source of truth for detailed game rules.

Important specs:

- [[specs/GDD|GDD]]
- [[specs/GBD|GBD]]
- [[specs/mechanics/README|Mechanics Specs]]
- [[specs/mechanics/gameplay|Gameplay Rules]]
- [[specs/content/content-bible|Content Bible]]
- [[specs/mechanics/contracts|Contracts]]
- [[specs/mechanics/progression|Progression]]
- [[specs/UI_FLOW|UI_FLOW]]
- [[specs/SCREEN_SPEC|SCREEN_SPEC]]
- [[specs/mechanics/collection|Collection]]
- [[specs/education/learning-objectives|Learning Objectives]]
- [[specs/mechanics/data-model|Data Model]]
- [[specs/ui/README|UI/UX Specification]]
- [[specs/technical/README|Technical Direction]]
- [[specs/technical/platform-roadmap|Platform Roadmap]]
- [[specs/technical/localization|Localization]]
- [[specs/technical/testing|Testing Strategy]]
- [[specs/technical/future-platform|Future Platform]]
- [[specs/technical/development-tooling|Development Tooling]]
- [[specs/technical/implementation-readiness|Implementation Readiness]]
