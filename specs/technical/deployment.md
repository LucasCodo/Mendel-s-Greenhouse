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
5. Harden the generated HTML wrapper.
6. Serve the resulting `index.html` with `python -m http.server`.

The generated `.pyxapp`, HTML output, and `dist/` directory are build
artifacts and must not be committed.

## MetaMask Extension Isolation

The generated Pyxel HTML does not use wallet, Web3, or blockchain APIs.

Some browsers inject the MetaMask in-page script into every page. To avoid
extension-origin scripts trying to connect inside the game page, the build
post-processes the generated HTML and adds a Content Security Policy that
allows only the game page, Pyxel's CDN script, and required browser primitives
for the Pyxel WebAssembly runtime.

If the CSP is changed, verify that:

- The game still loads from `http://localhost:8080`.
- Browser console output does not contain MetaMask connection attempts from
  `chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn`.
- Pyxel WebAssembly still starts correctly.

## Docker Compose

The repository root `docker-compose.yml` builds `game/Dockerfile` through the
`game-web` service.

Runtime expectations:

- Container port: `8080`.
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
