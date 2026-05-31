# Future Platform And Architecture Decisions

## Purpose

This document records future implementation decisions for save data, packaging, web delivery, code architecture, and the later NiceGUI application shell.

Current implementation scope remains the Pyxel game only. NiceGUI account and save management are future scope.

## Save Data Format

### Decision

Future save data should use a versioned JSON document.

Pyxel's `.pyxres` format is reserved for game resources such as images, tilemaps, sounds, and music. It should not be used as the player save format.

### Local Pyxel Save Location

When running as a standalone Pyxel game, save files should live under Pyxel's user data directory.

Recommended conceptual path:

```text
pyxel.user_data_dir("LucasCodo", "MendelsGreenhouse")/
`-- saves/
    `-- slot-1.json
```

The exact application and author strings should be finalized during implementation.

For the MVP, local JSON persistence is enabled. The player starts with `0` credits unless balance testing changes the GBD.

### Save Schema

Every save file must include:

```json
{
  "schema_version": 1,
  "language": "en",
  "created_at": "ISO-8601 timestamp",
  "updated_at": "ISO-8601 timestamp",
  "profile": {},
  "greenhouse": {},
  "collection": {},
  "progression": {},
  "contracts": {},
  "settings": {}
}
```

Rules:

- Saves must be explicit JSON, not Python pickles.
- Saves must be schema-versioned from the first implementation.
- Save migration must be handled by schema version, not by guessing fields.
- Gameplay logic must not depend on the save storage backend.
- Future NiceGUI storage should preserve the same conceptual save payload.

### NiceGUI Future Storage

When NiceGUI is introduced, user saves may move from local files to an application-managed backend. The game should still read and write through a save service boundary so the payload remains portable.

## Packaging And Distribution Workflow

### Decision

Use Pyxel's native packaging flow for the game:

1. Develop and run the Python package locally.
2. Package the game as a `.pyxapp`.
3. Convert the `.pyxapp` to HTML with Pyxel `app2html` for the current web
   delivery.
4. Harden the generated HTML wrapper.
5. Serve the generated HTML with `python -m http.server` from the Docker
   runtime image.

This is a temporary web delivery path for the Pyxel game only. NiceGUI
account and save orchestration remain future scope.

### Local Development

The package remains runnable through Poetry:

```powershell
python game\main.py
```

Pyxel's runner can also execute the same launcher:

```powershell
pyxel run game\main.py
```

### Pyxel Packaging

Future packaging should follow Pyxel's documented flow:

```powershell
pyxel package mendels-greenhouse mendels-greenhouse/main.py
pyxel app2html mendels-greenhouse.pyxapp
```

The resulting `.pyxapp` is the intermediate Pyxel artifact. The generated HTML
is the current browser-delivered artifact.

### Early Execution

Early development should run the main Python entrypoint directly:

```powershell
python game\main.py
```

Pyxel runner execution is also valid:

```powershell
pyxel run game\main.py
```

The `.pyxapp` package remains the approved intermediate Pyxel distribution
artifact before the first release.

HTML export is part of the current Docker-hosted web build.

## Code Architecture And Module Layout

### Decision

Use a small layered architecture that keeps gameplay rules independent from Pyxel rendering.

Screen flow uses scene management with a `Scene` abstraction and a `SceneManager`.

Goals:

- Make genetics, contracts, progression, and saves testable with `pytest`.
- Keep Pyxel calls at the outer runtime/scenes layer.
- Make future NiceGUI integration possible without rewriting the game rules.

### Module Responsibilities

Recommended package layout:

```text
mendels_greenhouse/
|-- main.py
|-- assets/
|-- locale/
|-- content/
|   |-- species.py
|   |-- traits.py
|   `-- contracts.py
|-- core/
|   |-- genetics.py
|   |-- contracts.py
|   |-- greenhouse.py
|   |-- collection.py
|   |-- progression.py
|   |-- save_data.py
|   `-- i18n.py
|-- state/
|   |-- game_state.py
|   |-- settings.py
|   `-- session.py
|-- services/
|   |-- breeding_service.py
|   |-- contract_service.py
|   |-- collection_service.py
|   `-- save_service.py
|-- scenes/
|-- ui/
`-- web/
    `-- future_nicegui_shell.md
```

### Layer Rules

- `content/` defines static game content.
- `core/` contains deterministic domain rules.
- `state/` contains mutable game state structures.
- `services/` coordinates multi-step gameplay actions.
- `scenes/` owns Pyxel scene flow and input handling.
- `ui/` owns reusable Pyxel UI drawing helpers.
- `web/` remains future scope until NiceGUI integration starts.

Core modules must not import Pyxel.

If code quality degrades, use the refactoring policy in [development-tooling.md](development-tooling.md).

## Pyxel Web Delivery And Future NiceGUI

### Decision

The current repository includes a minimal Docker web delivery path:

- Build assets.
- Stage the Pyxel game package.
- Package the staged game as `.pyxapp`.
- Convert the `.pyxapp` with Pyxel `app2html`.
- Harden the generated HTML wrapper to isolate browser wallet extensions.
- Serve the generated `index.html` with `python -m http.server`.

The future NiceGUI application should replace or wrap this selected Pyxel web
artifact when account and save management enter scope.

### NiceGUI Integration Direction

When the NiceGUI shell is implemented:

- Prefer the Docker/app2html web artifact unless a later spec selects a
  different Pyxel delivery method.
- Create a small custom NiceGUI component for the game container.
- Keep account/profile/save UI outside the Pyxel canvas.
- Keep the game canvas full-page or fullscreen-capable.
- Use a narrow JavaScript bridge only when needed for save import/export, language selection, or session handoff.

### Custom Component Boundary

The NiceGUI custom component should be responsible for:

- Mounting the Pyxel web game.
- Controlling fullscreen.
- Passing initial configuration to the game.
- Reporting lifecycle events back to the NiceGUI shell.

The custom component should not implement gameplay rules.

## Future Account And Authentication Model

### Decision

The initial NiceGUI account model will use simple username and password authentication.

This is future scope and must not be implemented in the Pyxel MVP.

### Account Rules

Initial account model:

- Username.
- Password.
- One or more save slots per user.
- User-selected language preference.

Security requirements for future implementation:

- Never store plain-text passwords.
- Use password hashing.
- Use authenticated sessions.
- Keep save ownership tied to the authenticated user.
- Do not expose another user's save data through client-side state.

## Boundaries

Still not defined:

- Hosting provider.
- Database technology.
- Deployment workflow.
- Final NiceGUI routing structure.
- Exact save synchronization protocol between NiceGUI and the Pyxel game.

These decisions must be documented before implementation.

## References

- [Pyxel README](https://github.com/kitao/pyxel)
- [Pyxel user guide](https://kitao.github.io/pyxel/web/user-guide/)
- [Pyxel API reference](https://kitao.github.io/pyxel/web/api-reference/)
- [NiceGUI documentation](https://nicegui.io/documentation)
- [NiceGUI GitHub repository](https://github.com/zauberzeug/nicegui)
