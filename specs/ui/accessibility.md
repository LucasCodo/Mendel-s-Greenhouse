# Accessibility

## Goals

Mendel's Greenhouse should be readable, teachable, and playable by a broad audience, including students encountering genetics for the first time.

## Visual Accessibility

- Do not rely on color alone to communicate phenotype, rarity, contract state, or validity.
- Pair color with shape, icon, label, or pattern.
- Keep genotype strings legible and fixed-width.
- Keep small UI text optional, not the only way to understand a trait.
- Maintain strong contrast between text and panels.

## Cognitive Accessibility

- Introduce one new genetic information layer at a time.
- Keep tutorial text short.
- Prefer examples over definitions.
- Use repeated visual patterns for recurring actions.
- Avoid showing locked advanced data too early.

## Interaction Accessibility

- The primary interaction mode is mouse-first, but every core action must also be reachable by keyboard.
- Important actions must have clear labels or recognizable icons.
- Destructive actions, such as selling plants, require confirmation or undo support.
- Contract requirements should remain visible during planning.
- Hover-only information must also be accessible through selection or focus.
- Focus states must be visible on all keyboard-reachable controls.
- Keyboard navigation order should follow the visual reading order of each screen.
- Keyboard shortcuts may accelerate repeated play, but they must not be the only way to complete an action.

## Input Requirements

Mouse:

- Primary input for normal play.
- Used for selecting plants, buttons, tabs, cards, slots, bed cells, and bed
  controls.
- Hover may reveal tooltips, but the same information must be available through click/selection or focus.

Keyboard:

- Secondary input path.
- Must support navigation, activation, cancellation, and repeated core actions.
- Should be documented in settings or help once controls are implemented.
- Must not require memorizing shortcuts to understand the game.

## Feedback Accessibility

- Success, warning, and error feedback must use color plus text/icon.
- Discovery feedback should not block rapid play longer than necessary.
- Failed actions should explain what is missing.

## Minimum UI Checks

- Phenotypes remain recognizable in plant cards.
- Contract progress can be read without color.
- Analyzer level restrictions are obvious.
- Stored, selected, reserved, and deliverable plant states are visually distinct.
