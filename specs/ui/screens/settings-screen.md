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
| Gameplay             | Tutorial reset       |
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

### Language

- English.
- Portugues (Brasil).

Language changes should update visible UI text. Persistence can wait until the
future save/preferences system exists.

## Rules

- Settings must not change game rules.
- Accessibility settings must preserve phenotype readability.
