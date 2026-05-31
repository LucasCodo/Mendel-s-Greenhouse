# Platform Roadmap

## Decision

Mendel's Greenhouse is intended to be a web game.

For the current phase, implementation should focus only on the game itself using Pyxel. User accounts, cloud saves, account management, and save orchestration are future scope.

## Current Scope

Build the game loop first:

- Pyxel game runtime.
- Pixel art presentation.
- Local gameplay systems.
- MVP crossbreeding, contracts, collection, and progression.
- Full-page browser display for the game canvas.
- Fullscreen option for the game view.

Do not implement user accounts or hosted save management in the MVP unless a future spec explicitly changes the scope.

## Future Scope

NiceGUI is the planned future framework for:

- User account management.
- Save management.
- Player profile screens.
- Web application shell around the Pyxel game.

The initial future account model will use simple username and password authentication.

The current web delivery uses Pyxel's documented `.pyxapp` to `app2html`
flow inside Docker, hardens the generated HTML wrapper, and serves the
generated HTML with `python -m http.server`. The future NiceGUI shell should
replace or wrap this delivery path when account and save orchestration enter
scope.

## Boundaries

Do not implement NiceGUI in the MVP.

Resolved future direction:

- Save data format: versioned JSON.
- Local Pyxel save location: Pyxel user data directory.
- Packaging: Pyxel `.pyxapp`.
- Early execution: main Python entrypoint.
- HTML export: enabled for the temporary Docker-hosted Pyxel web build.
- Future web shell: NiceGUI custom component around Pyxel web delivery.
- Authentication: simple username and password initially.

Still open:

- Hosting provider.
- Database technology.
- Deployment workflow.
- Final NiceGUI routing structure.
- Exact save synchronization protocol between NiceGUI and the Pyxel game.

See [future-platform.md](future-platform.md).
