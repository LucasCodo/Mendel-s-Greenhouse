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

## Boundaries

Do not define the NiceGUI architecture yet.

Open future decisions:

- How Pyxel will be embedded or delivered in the future NiceGUI web shell.
- Save data format.
- Account model.
- Authentication flow.
- Deployment and hosting.
- Integration boundary between the Pyxel game and the NiceGUI application shell.
