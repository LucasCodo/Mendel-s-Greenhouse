# Asset Generation Guide

## Purpose

This guide defines how AI-generated or human-created visual assets should support Mendel's Greenhouse UI and learning goals.

## Art Style

- Modern 2D pixel art.
- Colorful but comfortable.
- Educational.
- Friendly.
- High legibility.
- Clean silhouettes.
- Low visual noise.
- Limited palette.
- Modern indie-game polish.

Reference direction:

- Stardew Valley for warm vegetation and readable farming spaces.
- Fields of Mistria for soft modern pixel art and friendly UI.
- Potion Permit for laboratory interiors and lighting.
- Sun Haven for vibrant analyzer/discovery effects.
- Pokemon GBA for collection/catalog clarity.

Use these as design references, not as sources to copy.

## Required Visual Rules

Phenotypes must be recognizable without reading text.

Examples:

```text
Flower color:
- Purple
- White
- Red

Height:
- Short
- Medium
- Tall
```

The visual difference must be obvious in small UI cards and in Germination Bed
cells.

## Asset Prompt Pattern

Use this structure for asset generation:

```text
Create a 2D pixel art game asset for Mendel's Greenhouse.
Style: pixel art, friendly educational botanical laboratory, clear silhouette, high readability, limited palette.
Subject: <asset subject>.
Required traits: <phenotype traits>.
Background: transparent or simple neutral.
Avoid: photorealism, painterly rendering, heavy texture, dark lighting, ambiguous traits, clutter.
```

## Native Asset Format

Use Pyxel's native resource format:

```text
.pyxres
```

Primary runtime asset file:

```text
game/mendels_greenhouse/assets/mendels_greenhouse.pyxres
```

Assets should be authored so they can be packed into the `.pyxres` file without losing readability.

## Pyxel MCP Verification

When `pyxel-mcp` tools are available, generated assets must be checked inside Pyxel rather than only as standalone files.

Use:

- `inspect_sprite` for individual plant/icon sprites.
- `inspect_bank` for image-bank overview.
- `inspect_tilemap` for greenhouse backgrounds.
- `inspect_palette` for color/contrast checks.
- `inspect_animation` for animated sprite sheets.
- `render_audio` for sounds and music.

If MCP tools are not available in the current agent session, record that limitation and run `poetry run poe check` plus direct Pyxel smoke checks.

## Resolution Rules

Asset sizes must be large enough for the game to look polished while staying compatible with the Pyxel pixel-art direction.

| Asset Type | Minimum | Preferred | Maximum |
| ---------- | ------: | --------: | ------: |
| Small icons | 16 x 16 | 16 x 16 or 32 x 32 | 64 x 64 |
| UI icons | 16 x 16 | 32 x 32 or 48 x 48 | 64 x 64 |
| Germination Bed specimen sprites | 16 x 16 | 24 x 24 or 32 x 32 | 64 x 64 |
| Parent card plant sprites | 64 x 64 | 96 x 96 or 128 x 128 | 256 x 256 |
| Analyzer plant preview | 96 x 96 | 128 x 128 | 256 x 256 |
| Discovery popup plant | 96 x 96 | 128 x 128 | 256 x 256 |
| Character portrait | 64 x 64 | 64 x 64 or 96 x 96 | 128 x 128 |
| Background tiles | 16 x 16 | 32 x 32 or 64 x 64 | 256 x 256 |
| Background compositions | 256 x 160 | 640 x 360 | 640 x 360 |
| UI panel pieces | 16 x 16 | 32 x 32 or 64 x 64 | 256 x 256 |

Prefer the higher end of the range when readability improves, especially for plant sprites and discovery assets.

For the main game screen, source art should be authored for the `640 x 360` internal canvas. The browser may scale this up, but the base composition must already look complete at native resolution.

## Plant Asset Requirements

- Each phenotype must affect a visible plant part.
- Flower color must be visible at card size.
- Leaf width must change silhouette.
- Stem height must be visible against consistent scale.
- Petal pattern must remain readable without zoom.

## UI Asset Requirements

- Panels should support text readability.
- Buttons should have clear states.
- Icons should be understandable at small sizes.
- Decorative assets must not hide gameplay information.

## Audio Asset Requirements

Audio assets are defined in [assets/audio.md](assets/audio.md).

Use Pyxel sound/music resources for:

- UI clicks.
- Germination Bed growth/reveal.
- Offspring reveal.
- Contract progress.
- Discoveries.
- Analyzer activity.
- Loopable greenhouse music.

## Consistency Rules

- Use the same plant scale within the same screen.
- Use the same trait shape language across species unless the content bible changes it.
- Do not create new genes or traits through art direction.
- Asset names should match the concepts in [../content/content-bible.md](../content/content-bible.md).
- Assets must respect the approved Pyxel direction in [../technical/pyxel.md](../technical/pyxel.md).
