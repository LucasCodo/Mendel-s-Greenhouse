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
256 x 144
```

This gives a widescreen 16:9 canvas that scales cleanly in the browser while staying within a retro pixel-art density.

Asset resolution range:

```text
Minimum: 16 x 16
Maximum: 256 x 256
Preferred high-detail sprite size: 64 x 64 or 128 x 128
Preferred background/tilemap source size: 256 x 144 or 256 x 256
```

Use higher-resolution pixel art within this range when it improves plant readability, especially for plant cards, analyzer previews, and discovery popups.

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
