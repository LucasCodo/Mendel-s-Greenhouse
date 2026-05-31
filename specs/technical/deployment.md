# Deployment

## Purpose

This document defines the current deployment path for Mendel's Greenhouse.

The active scope is the Pyxel game only. Future NiceGUI account and save
management remain outside the current implementation.

## Current Web Artifact

The current web artifact is generated from the Pyxel app:

1. Run asset generation.
2. Stage only runtime game files.
3. Package the staged game with `pyxel package`.
4. Convert the `.pyxapp` with `pyxel app2html`.
5. Serve the resulting `index.html` with Python's standard `http.server`.

The generated `.pyxapp`, HTML output, and `dist/` directory are build
artifacts and must not be committed.

## Browser Extension Noise

The generated Pyxel HTML is served as the Pyxel export produced by
`app2html`. The project does not add wallet, Web3, blockchain, or extension
integration code to the page.

Some browsers inject extension scripts into every page. MetaMask can emit
`Failed to connect to MetaMask` from its own `chrome-extension://` script even
when the page does not use wallet APIs. This is extension-side console noise,
not an application integration point.

Do not add CSP rules, Web3 stubs, wallet detection, or extension integration
code to handle this. If the console message appears during local testing, use a
browser profile without MetaMask or disable MetaMask site access for the local
game URL.

When changing the web delivery path, verify that the game still loads through
the host port assigned to container port `8080` and that Pyxel WebAssembly
starts correctly.

## Docker Compose

The repository root `docker-compose.yml` builds `game/Dockerfile` through the
`game-web` service.

Runtime expectations:

- Container port: `8080`.
- Host port: assigned by Docker or the platform.
- Healthcheck path: `/health.html`.
- Runtime server: `python -m http.server`.
- Base image: `python:3.11-slim`.

## CI/CD

CI runs on pushes and pull requests:

- Install Python 3.11 and Poetry.
- Run `poetry run poe check` in `game/`.
- Build the Docker Compose `game-web` image.

CD is designed for Coolify:

- Run only after CI succeeds on `main`, or through manual dispatch.
- Call the Coolify deploy webhook with `COOLIFY_WEBHOOK`.
- Authenticate the webhook call with `COOLIFY_TOKEN`.

Production environment variables should remain in Coolify, not in the
repository.
