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

Pyxel encourages retro limited-palette thinking. These color roles define intent; implementation should map them to the final Pyxel palette during production.

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

## Screen Resolution And Scaling

Target internal game resolution:

```text
256 x 144
```

Display requirements:

- The game canvas fills the browser page.
- Scaling preserves the internal aspect ratio.
- Pixel art remains crisp.
- A fullscreen action is available from the game UI.
- UI must remain readable at the internal resolution before browser scaling.

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

### Buttons

- Primary: green fill for main actions.
- Secondary: neutral surface with border.
- Danger: red only for destructive actions.
- Disabled: desaturated and non-interactive.

### Progress Bars

- Use for contract progress, collection completion, and analyzer upgrade progress.
- Always include readable numeric status, such as `3/10`.

### Tooltips

- Explain actions or unfamiliar icons.
- Avoid teaching full genetics concepts in tooltips.
- Prefer one short sentence.

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
