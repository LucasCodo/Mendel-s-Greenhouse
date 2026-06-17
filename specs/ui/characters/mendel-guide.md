# Mendel Guide Character

## Purpose

The Mendel Guide is a friendly pixel-art mentor character who delivers short
tutorial instructions, contextual hints, and feedback while the player learns
the core greenhouse loop.

The character supports the educational experience without changing genetics,
contracts, rewards, progression gates, analyzer behavior, or the main
mouse-first interaction model.

## Design Goals

- Make tutorial guidance feel present and personal.
- Keep onboarding light, visual, and action-oriented.
- Reinforce the official learning progression:
  phenotype, genotype, probability, and genetic planning.
- Help players recover from mistakes without exposing locked analyzer
  information early.
- Add personality to the greenhouse while preserving the scientific-botanical
  tone.

## Character Concept

The guide is inspired by Gregor Mendel as an approachable greenhouse mentor,
not as a strict historical simulation.

Visual direction:

- Elder scientist and gardener silhouette.
- Monk-like coat or apron, simplified for pixel-art readability.
- Warm, scholarly expression.
- Botanical or notebook accessory, such as a pea pod, small journal, or hand
  lens.
- Palette aligned with [../color-palette.md](../color-palette.md), avoiding
  colors reserved for critical gameplay states.

The character must not imply fantasy powers or non-Mendelian mechanics.

## Tutorial Role

The Mendel Guide may appear during:

- First contract onboarding.
- First parent selection.
- First cross.
- First offspring reveal.
- First contract delivery.
- First analyzer use at each unlocked analyzer level.
- First discovery or collection milestone.
- Recovery moments when an attempted action fails because a prerequisite is
  missing.

Guidance must remain contextual. The guide should point to the next useful
action instead of explaining unrelated systems.

## Interaction Model

The guide is a UI helper, not a controllable character.

Allowed presentation patterns:

- Small portrait beside a help panel.
- Speech bubble attached to the bottom help zone.
- Short overlay prompt during tutorial-only steps.
- Optional icon in the help panel to reopen the current hint.

Interaction rules:

- The player must be able to dismiss or advance guide messages.
- Tutorial prompts must not block repeated experimentation longer than needed.
- Core actions must stay mouse-first and keyboard-reachable.
- Hover-only guide content is not allowed; the same content must be available
  through click, focus, or the help panel.
- The guide must not cover contract progress, selected parents, analyzer output,
  or the Germination Bed during active play.

## Writing Rules

Guide text must follow the localization rules in
[../../technical/localization.md](../../technical/localization.md).

Content rules:

- Use short sentences.
- Teach one idea at a time.
- Prefer action prompts over definitions.
- Use official content from
  [../../content/content-bible.md](../../content/content-bible.md).
- Do not reveal genotype, probability, or simulator concepts before the
  corresponding analyzer level is unlocked.
- Do not introduce new lore that changes the game premise.

Tone:

- Encouraging but concise.
- Curious and scientific.
- Clear enough for first-time genetics learners.

Example message length target:

```text
Each parent gives one allele per gene. Choose two peas and cross them.
```

## Visual Asset Requirements

Concept references for voting live in
[references/README.md](references/README.md). They are not production sprites
until one direction is selected and normalized for Pyxel.

Required sprite set:

| Asset | Recommended Source Size | Use |
| ----- | ----------------------: | --- |
| Portrait neutral | 64 x 64 or 96 x 96 | Help panel and tutorial prompts |
| Portrait pointing | 64 x 64 or 96 x 96 | Action-directed hint |
| Portrait pleased | 64 x 64 or 96 x 96 | Success, discovery, completion |
| Portrait concerned | 64 x 64 or 96 x 96 | Invalid action or missing prerequisite |
| Small guide icon | 32 x 32 or 48 x 48 | Help button, guide recall control |

Animation requirements:

- Keep portrait animation subtle.
- Use blinking, slight head movement, or small hand gesture loops only.
- Avoid animation that distracts from reading contract or analyzer data.
- Provide a static fallback frame for every pose.

Asset constraints:

- Transparent background.
- Clean silhouette at native Pyxel resolution.
- Readable face and accessory at help-panel size.
- No photorealistic or painterly rendering.
- No copied likeness from specific copyrighted artwork.

## UI Placement

Primary placement is the existing contextual help area described in
[../scenes/main-game/components/help-panel.md](../scenes/main-game/components/help-panel.md).

The portrait should sit inside or directly beside the help panel. Speech text
should use the same readable panel treatment as other tutorial text.

During tutorial-only steps, a larger prompt may appear if it does not obscure
the required interaction target. When possible, the prompt should visually point
to the target area instead of covering it.

## Progression And State

The guide may track whether a player has already seen a hint, but that state is
only tutorial/help state. It must not affect:

- Genetic outcomes.
- Contract generation.
- Rewards or costs.
- Analyzer unlocks.
- Collection completion.
- Greenhouse storage rules.

Settings should support resetting tutorial prompts as defined in
[../screens/settings-screen.md](../screens/settings-screen.md).

## Non-Goals

- No dialogue tree system for the MVP.
- No autonomous NPC movement in the greenhouse for the MVP.
- No voice acting requirement.
- No historical biography screen requirement.
- No new tutorial economy, reward, or progression rule.

## Acceptance Criteria

- The first playable tutorial can show Mendel Guide prompts without requiring
  long reading.
- Guide prompts respect analyzer information locks.
- Guide UI is dismissible, keyboard-reachable, and does not hide core game
  state.
- Guide assets follow the approved pixel-art direction and expanded palette.
- All guide text is localizable in English and Brazilian Portuguese.
