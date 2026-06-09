---
title: UI Scene Wiki
tags:
  - ui/scenes
  - obsidian/wiki
type: index
project: mendels-greenhouse
status: active
---

# UI Scene Wiki

This directory organizes each game scene as an Obsidian-friendly module.

Each scene should have its own folder with:

- A scene `README.md`.
- A `visual-target.md` note that defines the official implementation target.
- A `layout-reference.md` note for visual references.
- A `component-map.md` note for composition and hierarchy.
- A `components/` folder with one Markdown note per reusable or scene-specific
  UI element.
- A `references/` folder for images, sketches, and source references.
- A `references/component-sheets/` folder for model-generated component sheets
  used as source art for the component images.

## Naming Pattern

- Scene visual target: `references/<scene>-layout-target.png`.
- Model-generated component sheet:
  `references/component-sheets/<scene>-component-sheet-model.png`.
- Component image: `references/components/<scene>-component-<component>.png`.
- Component note: `components/<component>.md`.
- Component image embeds should use full vault paths. Example pattern:
  `embed specs/ui/scenes/SCENE/references/components/IMAGE.png`.
- Links to project specs should use full vault paths, such as
  `[[specs/ui/screens/main-game-screen|Main Game Screen Spec]]`.

## Scenes

- [[main-game/README|Main Game Scene]]
- [[garden/README|Garden Scene]]
- [[collection/README|Collection Scene]]
- [[knowledge/README|Knowledge Scene]]
- [[contracts/README|Contracts Scene]]
- [[shop/README|Shop Scene]]
- [[settings/README|Settings Overlay]]
- [[overlays/README|Runtime Overlays]]
