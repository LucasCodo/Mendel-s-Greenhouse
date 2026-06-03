# Pyxel Engine Direction

## Decision

Mendel's Greenhouse will use [Pyxel](https://github.com/kitao/pyxel) as its game engine.

The game art direction is pixel art.

The game is intended for web delivery. Current implementation should focus on the Pyxel game itself; the future web application shell is documented in [platform-roadmap.md](platform-roadmap.md).

## Why Pyxel Fits

Pyxel is a retro game engine for Python focused on pixel-art-style games. Its simple retro-console constraints match the project direction:

- Pixel art visuals.
- Small, readable sprites.
- Limited color thinking.
- Simple screen and input model.
- Lightweight scope suitable for a focused educational MVP.

## Official Constraints To Respect

Use Pyxel's retro constraints as design guidance:

- Treat the palette as intentionally limited.
- Keep sprites small and readable.
- Prefer clear silhouettes over painterly detail.
- Keep UI layouts compact and grid-based.
- Use simple animation loops and concise visual effects.

## Palette Mapping

Use Pyxel's palette indexes through human-readable enums.

Rules:

- UI code must not scatter raw integer color indexes.
- Design-system color roles must map to Pyxel palette indexes in `mendels_greenhouse/ui/palette.py`.
- The MVP uses an expanded project palette instead of limiting itself to the
  default 16 colors.
- If the palette is customized later, update the enum/mapping in one place.
- Background PNGs and `.pyxres` assets must be generated or quantized against
  the same runtime palette.

See [implementation-readiness.md](implementation-readiness.md) and
[../ui/color-palette.md](../ui/color-palette.md).

## Asset Format

Use Pyxel's native resource format:

```text
.pyxres
```

The primary asset file should be:

```text
mendels_greenhouse/assets/mendels_greenhouse.pyxres
```

The `.pyxres` file should contain the production sprites, tilemaps, sounds, and music needed by the Pyxel runtime.

## Resolution Direction

The browser page should display the game scaled to fill the available page area while preserving pixel-art sharpness and the game's aspect ratio.

Recommended internal game resolution:

```text
640 x 360
```

This gives a widescreen 16:9 canvas with enough logical space for a
high-quality management-game interface: persistent resource bar, contract
panel, parent cards, analyzer/probability panels, a large Germination Bed, and
bottom information panels.

The earlier `256 x 144` target is too constrained for the intended visual quality and should only be used for tiny prototypes or isolated UI tests.

Asset resolution range:

```text
Minimum: 16 x 16
Maximum: 256 x 256
Preferred high-detail sprite size: 64 x 64, 96 x 96, or 128 x 128
Preferred background/tilemap source size: 640 x 360, built from reusable tiles and panels
```

Use higher-resolution pixel art within this range when it improves plant readability, especially for plant cards, analyzer previews, and discovery popups.

## Quality Target

The main game screen should aim for the density and polish of a premium pixel-art management interface:

- Decorative greenhouse background with readable foreground UI.
- Framed parchment/wood/metal panels for gameplay information.
- Large parent plant previews.
- A Germination Bed large enough to show representative offspring proportions at
  a glance.
- Distinct icons for credits, premium resource, garden capacity, guide, garden, shop, and settings.
- Bottom panels for generation statistics, last generated plant, educational help, and speed controls.

Do not reduce the UI to plain debug text once production assets exist.

## Browser Display Requirements

The game must:

- Occupy the full browser page area.
- Preserve aspect ratio when scaled.
- Keep pixel art crisp, not blurred.
- Provide a fullscreen option.
- Continue to use the same internal game resolution when entering fullscreen.

## Documentation Boundaries

This document selects the engine and visual direction. It does not define:

- Project architecture.
- Persistence system.
- Save format.
- Packaging workflow.
- Web embedding strategy.
- Account management.
- Code module layout.

Those decisions should be documented later when implementation begins.
