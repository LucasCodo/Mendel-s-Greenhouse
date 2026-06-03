---
title: Garden Layout Reference
tags:
  - ui/scenes/garden
  - ui/reference
type: reference
project: mendels-greenhouse
status: active
---

# Garden Layout Reference

This note records the user-provided Garden Scene reference image from the chat.
The image depicts the desired direction for the stored-plant management scene:
a polished pixel-art greenhouse interface with a large inventory grid, a
selected plant detail panel, parent-selection actions, and a vertical right
navigation rail.

> [!important] Visual Target
> The Garden interface should approach [[visual-target|Garden Visual Target]] as
> closely as Pyxel allows.

> [!note] Image File
> The chat attachment was not available as a filesystem file, so this repository
> stores a generated target PNG based on the provided image. Replace
> `references/garden-layout-target.png` with the original exported image when
> available.

## Image

![[specs/ui/scenes/garden/references/garden-layout-target.png]]

## Scene Read

The composition should read as the player's stored greenhouse collection. The
player's attention flows from the plant grid, to the selected plant details, to
the action buttons.

## Layout Zones

```text
+----------------------------------------------------------------------------------+
| Top Bar: logo, credits, capacity                                                  |
+-----------------------------------------------------------+----------------------+
| Scene Header: JARDIM                                      | Right Nav Rail       |
| Stored Plant Grid                 | Selected Plant Panel  |                      |
| 5 columns x 3 visible rows        | Preview + traits      |                      |
|                                   | Actions               |                      |
+----------------------------------------------------------------------------------+
```

## Portuguese Labels Seen In Reference

- `JARDIM`
- `Plantas guardadas e seleção de pais.`
- `Slots: 5/24`
- `PLANTA SELECIONADA`
- `ID: 001`
- `Fenótipo`
- `Genótipo`
- `Cor`
- `Textura`
- `AÇÕES`
- `USAR COMO PAI A`
- `USAR COMO PAI B`
- `ANALISAR`
- `DESCARTAR`
- `CRUZAMENTO`
- `CONTRATOS`
- `LOJA`
- `COLEÇÃO`
- `CONFIGURAÇÕES`

