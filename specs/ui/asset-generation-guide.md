# Asset Generation Guide

## Purpose

This guide defines how AI-generated or human-created visual assets should support Mendel's Greenhouse UI and learning goals.

## Art Style

- 2D pixel art.
- Colorful.
- Educational.
- Friendly.
- High legibility.
- Clean silhouettes.
- Low visual noise.
- Limited palette.
- Retro game readability.

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

The visual difference must be obvious in small UI cards and in the production conveyor.

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
mendels_greenhouse/assets/mendels_greenhouse.pyxres
```

Assets should be authored so they can be packed into the `.pyxres` file without losing readability.

## Resolution Rules

Asset sizes must be large enough for the game to look polished while staying compatible with the Pyxel pixel-art direction.

| Asset Type | Minimum | Preferred | Maximum |
| ---------- | ------: | --------: | ------: |
| Small icons | 16 x 16 | 16 x 16 or 32 x 32 | 64 x 64 |
| UI icons | 16 x 16 | 32 x 32 | 64 x 64 |
| Plant sprites | 32 x 32 | 64 x 64 or 128 x 128 | 256 x 256 |
| Analyzer plant preview | 64 x 64 | 128 x 128 | 256 x 256 |
| Discovery popup plant | 64 x 64 | 128 x 128 | 256 x 256 |
| Background panels | 128 x 128 | 256 x 144 or 256 x 256 | 256 x 256 |

Prefer the higher end of the range when readability improves, especially for plant sprites and discovery assets.

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

## Consistency Rules

- Use the same plant scale within the same screen.
- Use the same trait shape language across species unless the content bible changes it.
- Do not create new genes or traits through art direction.
- Asset names should match the concepts in [../content/content-bible.md](../content/content-bible.md).
- Assets must respect the approved Pyxel direction in [../technical/pyxel.md](../technical/pyxel.md).
