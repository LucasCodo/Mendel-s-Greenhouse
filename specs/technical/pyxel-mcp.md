# Pyxel MCP Workflow

## Purpose

This document defines how Mendel's Greenhouse should use `pyxel-mcp` during implementation.

`pyxel-mcp` is a development tool for validating Pyxel code, screenshots, sprites, palettes, tilemaps, animations, and audio. It supports implementation quality but does not define gameplay rules.

## Source Of Truth

Project specs remain the source of truth:

- Gameplay rules live in `specs/mechanics/`.
- Visual direction lives in `DESIGN.md` and `specs/ui/`.
- Technical direction lives in `specs/technical/`.

If `pyxel-mcp` output suggests a change that affects rules, layout, art direction, or asset requirements, update the relevant spec before treating the change as accepted.

## Installation

The project uses `pyxel-mcp` as a `game/` development dependency:

```powershell
cd game
poetry add --group dev pyxel-mcp
```

The package exposes the MCP command:

```text
pyxel-mcp
```

Preferred MCP server configuration for clients that read JSON MCP config:

```json
{
  "mcpServers": {
    "pyxel": {
      "type": "stdio",
      "command": "pyxel-mcp"
    }
  }
}
```

When possible, point the MCP client at the Poetry-managed executable from `game/.venv/Scripts/pyxel-mcp.exe` on Windows to avoid a separate global install.

## Official Tool Capabilities

Use the MCP server for these categories.

### Run And Capture

- `run_and_capture`: run a Pyxel script and capture a screenshot after selected frames.
- `capture_frames`: capture multiple frames to verify animation timing.
- `play_and_capture`: simulate input and capture resulting frames.

Use for:

- Main game screen visual checks.
- Conveyor reveal flow.
- Fullscreen/page framing checks when available.
- Regression screenshots after UI changes.

### Inspect And Debug

- `validate_script`: validate Pyxel scripts without running them.
- `inspect_state`: inspect game object attributes at specific frames.
- `inspect_screen`: capture compact screen color-index grids.
- `compare_frames`: compare screenshots for pixel differences.

Use for:

- Catching Pyxel API misuse.
- Checking screen state after input.
- Detecting blank screens.
- Validating that reveal/progress states change.

### Visual Analysis

- `inspect_sprite`: inspect sprite pixel data in image banks.
- `inspect_layout`: analyze text alignment and visual balance.
- `inspect_palette`: analyze color usage and contrast.
- `inspect_bank`: visualize a whole image bank.
- `inspect_tilemap`: inspect tilemap content and tile usage.
- `inspect_animation`: check sprite sheet consistency across animation frames.

Use for:

- Verifying `.pyxres` sprite banks.
- Checking plant phenotype readability.
- Checking UI contrast.
- Checking modern pixel-art asset consistency.
- Auditing tilemaps/backgrounds for clutter.

### Audio

- `render_audio`: render Pyxel sound or music to WAV and return waveform analysis.

Use for:

- Sound-effect sanity checks.
- Loopable music checks.
- Confirming discovery/reward/conveyor sounds are present and not silent.

## Required Workflow For Visual Changes

When MCP tools are available:

1. Update code or `.pyxres` assets.
2. Run `validate_script`.
3. Run `run_and_capture` for the affected screen.
4. Use `inspect_layout` for UI-heavy changes.
5. Use `inspect_palette` when changing colors.
6. Use `inspect_sprite`, `inspect_bank`, or `inspect_tilemap` when changing assets.
7. Use `inspect_animation` when adding animation frames.
8. Use `render_audio` when adding sounds or music.
9. Run `poetry run poe check`.

When MCP tools are not available:

1. Run `poetry run poe check`.
2. Run targeted pytest tests.
3. Run direct Pyxel smoke checks where possible.
4. Record that MCP visual/audio validation was not available.

## Asset Generation And Verification

Generated assets must be packed into:

```text
game/mendels_greenhouse/assets/mendels_greenhouse.pyxres
```

Rules:

- Do not keep production assets only as loose external images.
- Use AI image generation only as source material or concept support unless the output is converted into Pyxel-ready pixel art.
- Verify sprites inside Pyxel image banks with MCP inspection tools.
- Verify palettes against the approved visual direction.
- Verify phenotype readability at the actual in-game size.

## Music And Sound Verification

Sound and music should be authored in Pyxel resources when possible.

Required checks:

- Sounds are not silent.
- Reward/discovery sounds are short and readable.
- Conveyor sounds do not become fatiguing.
- Music loops cleanly.
- Audio supports the cozy greenhouse/laboratory mood.

Use `render_audio` when available.

## Acceptance Criteria

A Pyxel visual/audio contribution is ready when:

- `poetry run poe check` passes.
- The game screen is nonblank.
- Main UI text is readable.
- Plant phenotypes are visually distinguishable.
- `.pyxres` banks contain the expected sprites/sounds/music.
- MCP validation was run, or the reason it was unavailable is documented.
