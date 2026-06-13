---
title: Commands
tags:
  - agent-memory/command
type: command
project: mendels-greenhouse
status: active
updated: 2026-06-13
---

# Commands

The implementation package now lives under `game/`.

Validated documentation checks:

- `git status --short` checks the worktree before staging or commits.
- `rg -n "<term>" README.md AGENTS.md DESIGN.md CONTRIBUTING.md specs` searches for stale references across documentation.
- `Get-ChildItem specs -File | Sort-Object Name | Select-Object -ExpandProperty Name` verifies the specs directory contents on Windows PowerShell.
- A PowerShell Markdown-link scan can validate relative links after moving docs by scanning Markdown link syntax and checking local targets with `Test-Path`.
- `git diff --check` validates staged or unstaged documentation edits for whitespace errors.
- `python --version` confirmed the local Python baseline as Python 3.11.1.
- GitHub CLI was used successfully to make the repository public, add branch protection, and verify final settings.
- `poetry new --flat --name mendels_greenhouse --readme md --license MIT --python ">=3.11,<4.0" --dependency pyxel --no-interaction game` created the Pyxel game package.
- `poetry add --group dev pytest pytest-cov hypothesis ruff poethepoet Babel` initially failed when Poetry could not validate the Kaspersky-reissued certificate chain for `files.pythonhosted.org`.
- Antigravity later restored Pyxel/dev dependencies and installed `pyxel-mcp`; the generated lock was stale and should be regenerated only when dependency resolution is stable.
- `poetry check` validates the current `game/pyproject.toml`.
- `poetry run poe check` runs Ruff, format check, and pytest for the game package.
- From the repository root, run the game with `python game\main.py`.
- From the repository root, Pyxel can run the same launcher with
  `pyxel run game\main.py`.
- From `game/`, `poetry run poe start` is the convenience task for the same
  launcher.
- 2026-05-31: `poetry run poe check` passed with 15 tests after adding
  MVP state, contracts, greenhouse, collection, breeding service, and the
  Pyxel Main Game scene.
- 2026-05-31: `poetry run poe build-assets` generated the MVP
  `mendels_greenhouse.pyxres` and `mendel_5x7.bdf` assets. Direct Pyxel smoke
  checks validated sprite pixels, custom font loading, and non-silent sound
  banks because MCP tools were still unavailable in the active session.
- 2026-05-31: after updating the project palette to the cozy scientific
  greenhouse direction, `poetry run poe build-assets` regenerated
  `game/mendels_greenhouse/assets/mendels_greenhouse.pyxres` and
  `mendel_5x7.bdf`; `poetry run poe check` passed with Ruff, format check, and
  15 pytest tests.
- 2026-05-31: after replacing Mendel Pea plant-in-pot sprites with pea pod
  sprites, `poetry run poe build-assets` regenerated the `.pyxres` asset file
  and `poetry run poe check` passed with Ruff, format check, and 15 pytest
  tests.
- 2026-05-31: after moving visible pea pod contours away from transparent
  palette index `0`, `poetry run poe build-assets` regenerated the `.pyxres`
  asset file and `poetry run poe check` passed with Ruff, format check, and 15
  pytest tests.
- 2026-05-31: after tightening the pea pod sprite visible area and recoloring
  the settings gear icon, `poetry run poe build-assets` regenerated the
  `.pyxres` asset file and `poetry run poe check` passed with Ruff, format
  check, and 15 pytest tests.
- 2026-05-31: after moving top-navigation icons to 64 x 64 `.pyxres` sprites
  and generating HUD frames in runtime code, `poetry run poe build-assets`
  regenerated the `.pyxres` asset file and `poetry run poe check` passed with
  Ruff, format check, and 15 pytest tests. A small smoke command confirmed
  `pyxel.blt(..., scale=0.5)` works in the installed Pyxel version.
- 2026-05-31: after adding the runtime settings panel and routing sound
  effects to Pyxel channel `3`, `poetry run poe check` passed with Ruff, format
  check, and 15 pytest tests.
- 2026-05-31: after adding Collection, Garden, and Shop runtime sub-scenes,
  `poetry run poe check` passed with Ruff, format check, and 15 pytest tests.
  Pyxel MCP `run_and_capture` still timed out at 30 seconds in the active
  session; `validate_script` only reported the known delegated-draw warning.
- 2026-05-31: `sh game/scripts/build-web.sh` is the Linux/Docker web build path.
  It runs `poetry run poe build-assets`, stages the game package under
  `game/dist/web-build/mendels-greenhouse`, packages it with
  `poetry run pyxel package mendels-greenhouse mendels-greenhouse/main.py`,
  converts it with `poetry run pyxel app2html mendels-greenhouse.pyxapp`,
  hardens the generated HTML wrapper with `tools/harden_web_html.py`, and
  writes `game/dist/web/index.html`.
- 2026-05-31: `docker compose up --build` builds the Pyxel app2html artifact
  in a Python/Poetry builder image and serves it on `http://localhost:8080`
  with `python -m http.server` from a Python runtime image. The Dockerfile
  lives at `game/Dockerfile`, and the Compose build context is `./game`.
- 2026-05-31: `docker compose build game-web` and
  `docker compose up -d game-web` validated the Python/http.server container
  path. `Invoke-WebRequest -UseBasicParsing http://localhost:8080/health.html`
  returned `200 ok`, and the root page returned `200`.
- 2026-05-31: local cleanup commands for generated files were blocked by the
  safety hook. Repository sanitization relies on `.gitignore`, `.dockerignore`,
  and selective staging; generated local artifacts must not be committed.
- `poetry run python -c "from mendels_greenhouse.core.genetics import Plant, crossbreed; offspring = crossbreed(Plant('AABB'), Plant('aabb'), count=20); assert {p.genotype for p in offspring} == {'AaBb'}; print('poetry core smoke check passed')"` validates the current core genetics implementation.
- `pyxel-mcp` official package docs list tools for `run_and_capture`, `capture_frames`, `play_and_capture`, `validate_script`, `inspect_state`, `inspect_screen`, `compare_frames`, `inspect_sprite`, `inspect_layout`, `inspect_palette`, `inspect_bank`, `inspect_tilemap`, `inspect_animation`, `render_audio`, and `pyxel_info`.
- 2026-06-13: `poetry run poe check` passed with Ruff, format checking, and
  71 pytest tests after the typography, localization, analyzer, specimen
  overlay, navigation, settings, layout, and collection-album refinements.
  Pyxel MCP script validation passed, while screenshot capture continued to
  time out in the active session.
- 2026-05-31: local Codex MCP config was updated in
  `C:\Users\luss1\.codex\config.toml` with `[mcp_servers.pyxel]` pointing to
  `C:\Users\luss1\Documents\GitHub\Mendel's Greenhouse\game\.venv\Scripts\pyxel-mcp.EXE`.
  The TOML file was validated with Python `tomllib`; restart/reload Codex for
  the server to appear as tools in a new session.
