# Settings Screen

## Purpose

The Settings Screen controls player preferences without defining implementation technology.

## Layout

```text
+--------------------------------------------+
| Settings                                   |
+----------------------+---------------------+
| Audio                | Volume controls      |
| Visual               | Motion, effects      |
| Accessibility        | Text, color support  |
| Gameplay             | Tutorial/progression |
+----------------------+---------------------+
| [Apply] [Reset Defaults] [Back]            |
+--------------------------------------------+
```

## Settings Categories

### Audio

- Master volume.
- Music volume.
- Effects volume.
- Mute music toggle.
- Mute effects toggle.

### Visual

- Animation intensity.
- Visual effects intensity.
- Interface scale if supported.
- Fullscreen toggle.

### Accessibility

- Color-support mode.
- Larger text option.
- Reduced motion.
- Tooltip persistence.

### Gameplay

- Reset tutorial prompts.
- Reset progression control.

Reset progression is a dangerous action. Activating the reset progression
control must open a confirmation dialog instead of resetting immediately.

Confirmation dialog requirements:

- Clearly warn that the action is dangerous.
- State that all user progression data will be erased.
- Require an explicit confirm action before deleting progress.
- Provide a cancel action that closes the dialog without changing data.
- Closing the dialog with Back, Escape, or an equivalent dismissal action must
  behave like cancel.

After confirmation, reset progression returns the save-relevant game state to
the initial playable state, including credits, contracts, discoveries,
greenhouse contents, unlocked species, analyzer level, collection milestones,
and current batch data.

### Language

- English.
- Portugues (Brasil).

Language changes should update visible UI text. Persistence can wait until the
future save/preferences system exists.

## Rules

- Settings must not change game rules.
- Accessibility settings must preserve phenotype readability.
