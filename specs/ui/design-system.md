# UI Design System

## Visual Theme

Mendel's Greenhouse combines:

- Educational game clarity.
- Scientific greenhouse atmosphere.
- Mendelian genetics symbolism.
- Botanical laboratory organization.
- Modern casual management readability.
- Pixel art readability.

Reference tone:

- Plant Tycoon for plant-care management.
- Plant Crossing for approachable plant variation.
- Two Point Campus for readable management UI.
- Potion Craft for tactile experimentation.
- Mini Motorways for low-noise information design.
- Cozy management games for friendly pacing and warmth.

## Visual Principles

- Clarity above realism.
- Pixel art above painterly illustration.
- Phenotypes must be identified instantly.
- Interface should be friendly for students.
- Feedback should be constant and readable.
- Cognitive load should stay low.
- Genetic complexity should be staged through disclosure.
- Numbers should support observation, not replace it.

## Color Palette

Use the expanded project palette defined in
[color-palette.md](color-palette.md). Pyxel supports extending the color list,
so the project does not treat 16 colors as a hard limit.

These roles summarize intent; the authoritative hex values and palette indexes
live in the color palette spec and `mendels_greenhouse/ui/palette.py`.

### Primary Colors

| Role | Color | Usage |
| ---- | ----- | ----- |
| Greenhouse Green | `#4F8F4A` | Primary actions, growth, valid plant states |
| Lab Teal | `#2F8F8A` | Analyzer, scientific panels, probability tools |
| Warm Cream | `#F4E9D2` | Main background surfaces |
| Deep Ink | `#263238` | Primary text |

### Secondary Colors

| Role | Color | Usage |
| ---- | ----- | ----- |
| Soil Brown | `#8B6A4E` | Greenhouse structure, slot borders |
| Glass Blue | `#A7D8DE` | Glass panels and cool highlights |
| Seed Yellow | `#F2C94C` | Rewards, discovery moments |
| Lavender Note | `#9B7EDE` | rare or special educational emphasis |

### Feedback Colors

| Role | Color | Usage |
| ---- | ----- | ----- |
| Success | `#49A65F` | Valid delivery, completed contract |
| Warning | `#E6A23C` | Low space, unmet requirement |
| Error | `#D9534F` | Invalid delivery, impossible action |
| Info | `#3B82C4` | Tutorial, analyzer explanation |

### Phenotype Colors

| Phenotype Category | Color Rule |
| ------------------ | ---------- |
| Flower color | Must visibly alter flower petals |
| Leaf width | Must visibly alter leaf silhouette |
| Stem height | Must visibly alter plant height |
| Petal pattern | Must visibly alter petal markings |

Text labels may support recognition, but visual traits must remain identifiable without labels.

Orange and brown are allowed for terracotta pots, wood, floor light, and warm
small accents. They must not dominate the full screen.

### Rarity Colors

| Rarity | Color |
| ------ | ----- |
| Common | `#9AA3A8` |
| Uncommon | `#4F8F4A` |
| Rare | `#3B82C4` |
| Very Rare | `#9B7EDE` |

### Contract Colors

| Contract Type | Color |
| ------------- | ----- |
| Phenotypic | `#4F8F4A` |
| Genotypic | `#2F8F8A` |
| Probabilistic | `#9B7EDE` |

## Typography

| Text Type | Intent |
| --------- | ------ |
| Titles | Short, confident, screen-level labels |
| Subtitles | Section labels and panel headings |
| Panel text | Compact readable instructions and values |
| Educational text | One or two sentence explanations, never dense paragraphs |
| Tooltips | Action-focused and contextual |
| Genotype text | Monospace or fixed-width style for allele alignment |

The runtime may use bold, outlined, letter-spaced display text for the game
logo and other short brand labels. Dense panel content should continue using
the compact display font without extra letter spacing.

## Spacing And Grid

Use an 8-unit spacing system:

| Token | Size | Usage |
| ----- | ---: | ----- |
| `xs` | 4 | tight icon spacing |
| `sm` | 8 | component internal spacing |
| `md` | 16 | panel padding |
| `lg` | 24 | screen section spacing |
| `xl` | 32 | major layout separation |

Main screens should use a stable grid:

- Top bar: contract, progress, resources.
- Side zones: parent slots or navigation panels.
- Center zone: core activity.
- Bottom zone: recent results, help, and contextual actions.

## Interaction Model

The primary interaction mode is mouse-first.

Players should be able to complete the core loop by pointing and clicking:

- Select parent plants.
- Start crossbreeding.
- Inspect offspring.
- Store selected specimens or harvest a batch into contract delivery and
  automatic excess sale.
- Navigate to contracts, greenhouse, analyzer, collection, shop, and settings.
- Select Germination Bed specimens and control bed reveal/clear actions.
- Confirm or cancel modal actions.

Keyboard support is required as an alternative input path, not as the primary UX assumption.

Keyboard controls should support:

- Focus navigation between interactive elements.
- Activation of focused controls.
- Common shortcuts for repeated actions.
- Cancel/back behavior.
- Accessibility for users who cannot or prefer not to use a mouse.

Every mouse-only affordance must have a keyboard-accessible equivalent.

## Screen Resolution And Scaling

Target internal game resolution:

```text
640 x 360
```

Display requirements:

- The game canvas fills the browser page.
- Scaling preserves the internal aspect ratio.
- Pixel art remains crisp.
- A fullscreen action is available from the game UI.
- UI must remain readable at the internal resolution before browser scaling.
- UI must fit both English and Brazilian Portuguese labels.
- The main game screen should support a premium pixel-art management layout with
  a persistent top bar, central contract panel, parent cards,
  probability/Punnett support, a large Germination Bed, and bottom information
  panels.

The old `256 x 144` target is no longer sufficient for the desired interface density.

## Quality Target Reference

Production UI should trend toward:

- Rich greenhouse/laboratory pixel-art background.
- Wood, parchment, metal, and botanical UI framing.
- Large, readable plant sprites.
- Icon-first navigation.
- High-contrast text surfaces.
- Decorative detail around panels that never competes with gameplay data.
- A dense but organized management-game layout.

## Base Visual Components

### Cards

- Rounded rectangle with 8px or smaller radius.
- Clear title zone.
- Trait badges near plant visuals.
- Locked information hidden or shown as unknown placeholders.

### Panels

- Slightly raised surfaces.
- Use consistent padding.
- Avoid nested card-heavy layouts.
- Use borders to clarify grouping.
- Runtime-drawn panel chrome may use stepped pixel corners, an outer shadow,
  and an inset highlight to create rounded, tactile surfaces without
  anti-aliasing.

### Buttons

- Primary: green fill for main actions.
- Secondary: neutral surface with border.
- Danger: red only for destructive actions.
- Disabled: desaturated and non-interactive.
- Main runtime buttons use stepped rounded corners, a visible lower shadow,
  outer and inner borders, centered labels, and a one-pixel pressed offset.
- Hover, pressed, disabled, and destructive states must remain distinguishable
  through shape, contrast, label, and color together.

### Progress Bars

- Use for contract progress, collection completion, and analyzer upgrade progress.
- Always include readable numeric status, such as `3/10`.

### Tooltips

- Explain actions or unfamiliar icons.
- Avoid teaching full genetics concepts in tooltips.
- Prefer one short sentence.

Knowledge tree concept details are not tooltips for this rule. They may contain
short educational explanations because they remain available through selection
and focus.

### Modals

- Use for confirmation, discoveries, rewards, and important unlocks.
- Must not block repeated core actions unnecessarily.

### Popups

- Use for transient feedback, such as new discovery or reward gained.
- Should be dismissible or auto-dismiss after a readable duration.

### Genetic Tags

- Phenotype tags: friendly labels with trait icon.
- Genotype tags: fixed-width allele text.
- Probability tags: percent value plus contract/probability color.
