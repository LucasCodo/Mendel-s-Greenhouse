# Design Principles

## Philosophy

Mendel's Greenhouse should teach by letting players observe, experiment, and discover.

## Objective

The game should make Mendelian genetics understandable through gameplay. Players should learn because genetic knowledge helps them make better decisions, complete contracts, and manage their greenhouse.

## Visual Direction

Mendel's Greenhouse uses modern pixel art: warm, polished, readable, and rich enough to feel like a contemporary indie management game rather than a minimal retro prototype.

The visual target is a cozy scientific greenhouse: botanical, tactile, slightly magical, but still grounded in clear learning feedback. It should feel like a welcoming plant laboratory, not a realistic clinical lab.

Core references:

- Stardew Valley: warm vegetation, farm readability, environmental detail.
- Fields of Mistria: softer modern pixel art, approachable UI, expressive charm.
- Potion Permit: laboratory mood, dense interiors, lighting and shadows.
- Sun Haven: vibrant special effects for analyzer/discovery moments.
- Pokemon GBA: collection/catalog readability.
- Professor Layton: approachable contracts and puzzle-like requests.
- Papers, Please: readable document/request interfaces, adapted to a friendly tone.

Reference use is directional only. Do not copy compositions, sprites, characters, UI frames, or protected assets from those games.

## Art Principles

- Immediate visual reading comes before decoration.
- Phenotype traits must be recognizable without text.
- Silhouettes should stay strong at conveyor size.
- Use vibrant but comfortable colors.
- Keep environmental detail rich but lower contrast than gameplay objects.
- Use warm greens, yellows, browns, glass blues, and genetics-focused purples.
- UI panels should feel handcrafted: wood, parchment, metal, glass, botanical labels.
- Science should look accessible and playful, not sterile.
- Effects should clarify discoveries, contract progress, and analyzer state.
- Pixel art should use modern polish: controlled clusters, readable lighting, soft atmospheric depth, and intentional contrast.

## Core Visual Areas

### Greenhouse

The greenhouse is the primary fantasy space.

It should include:

- Sunlit glass.
- Plant shelves.
- Botanical clutter.
- Crossbreeding benches.
- Genetic analyzer devices.
- Conveyor machinery.
- Warm wood and metal structure.
- Plants as the clearest foreground objects.

### Genetic Conveyor

The conveyor should feel engineered but friendly.

It should communicate:

- Offspring production.
- Shuffled reveal order.
- Batch progress.
- Contract matches.

Avoid harsh factory aesthetics. The conveyor is a greenhouse tool, not an industrial assembly line.

### Genetic Collection

The collection should borrow the clarity of creature catalogs:

- Plant silhouette.
- Phenotype.
- Genotype when unlocked.
- Discovery state.
- Rarity/probability support when unlocked.

### Analyzer Effects

Analyzer visuals may lean slightly magical or luminous to make abstract genetics visible:

- Soft purple, teal, and gold highlights.
- Lines connecting parents to predicted results.
- Subtle particles for discoveries.
- Clear diagrams over decorative glow.

## Asset Direction

- Small icons: `16 x 16` or `32 x 32`.
- Repeated UI icons: `32 x 32`.
- Conveyor plants: prefer `64 x 64`.
- Parent/analyzer plant views: prefer `96 x 96` or `128 x 128`.
- Discovery plant views: prefer `128 x 128`, up to `256 x 256`.
- Main composition target: `640 x 360`.

Assets should be packed into Pyxel `.pyxres` resources and verified in-game, not judged only as isolated images.

## Audio Direction

Audio should support a cozy science-management loop:

- Soft greenhouse ambience.
- Light mechanical conveyor sounds.
- Gentle UI clicks.
- Warm reward sounds.
- Short discovery stingers.
- Subtle analyzer hums and probability pings.

Music should be calm, loopable, and non-fatiguing. It should support repeated planning rather than demand attention.

## Principles

- Learning happens through experimentation.
- Discovery should be gradual.
- Curiosity should be rewarded.
- Avoid excessive theoretical exposition.
- Every major mechanic should reinforce Mendelian genetics.
- Visual observation should come before numerical explanation.
- Knowledge should be as valuable as currency.
- Complexity should grow only after the player has tools to reason about it.
- Pixel art should reinforce readability, not obscure genetic traits.
- Modern pixel-art polish should support learning rather than compete with it.

## Boundaries

This document defines global design principles only. Detailed rules, systems, values, content, screens, and balance belong in [`specs/`](specs/).
