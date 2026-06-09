---
title: Settings Component Map
tags:
  - ui/scenes/settings
  - ui/components
type: component-map
project: mendels-greenhouse
status: draft
---

# Settings Component Map

## Hierarchy

```text
SettingsOverlay
|- ModalScrim
|- SettingsPanel
|  |- LanguageSelector
|  |- VolumeControl(Music)
|  |- MuteCheckbox(Music)
|  |- VolumeControl(Effects)
|  |- MuteCheckbox(Effects)
|  |- ResetProgressButton
|  `- BackButton
`- ResetConfirmationDialog
   |- DangerCopy
   |- CancelButton
   `- ConfirmResetButton
```

## Implementation Notes

- The overlay draws above the active scene.
- Settings components do not persist changes directly; the scene applies and
  autosaves changes after user actions.
- Reset confirmation must clearly communicate that progression data is erased.
