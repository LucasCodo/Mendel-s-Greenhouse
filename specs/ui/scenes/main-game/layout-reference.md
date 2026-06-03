---
title: Main Game Layout Reference
tags:
  - ui/scenes/main-game
  - ui/reference
type: reference
project: mendels-greenhouse
status: active
---

# Main Game Layout Reference

This note records the user-provided main scene reference image from the chat.
The image depicts the desired direction for the primary gameplay scene:
a polished pixel-art greenhouse interface with a central parent-crossing panel,
a Germination Bed, a left genetic analyzer device, a right specimen/action
panel, top contract progress, and a vertical right navigation rail.

> [!important] Visual Target
> The main game interface should approach [[visual-target|Main Game Visual
> Target]] as closely as Pyxel allows.

> [!note] Image File
> The chat attachment was not available as a filesystem file, so this repository
> stores generated target/reference PNGs based on the provided image. Replace
> `references/main-game-layout-target.png` with the original exported image when
> available.

## Image

![[specs/ui/scenes/main-game/references/main-game-layout-target.png]]

## Scene Read

The composition should read as a greenhouse workbench rather than a factory.
The player's attention flows from the active contract, to the parent pair, to
the Germination Bed, then to the selected specimen actions.

## Layout Zones

```text
+----------------------------------------------------------------------------------+
| Top Bar: logo, resources, capacity, active contract                               |
+--------------------------+-------------------------------------+-----------------+
| Genetic Analyzer Panel   | Parent Cross Panel                  | Right Nav Rail  |
|                          +-------------------------------------+                 |
| Help Panel               | Germination Bed + Specimen Panel    |                 |
+--------------------------+-------------------------------------+-----------------+
```

## Visual Priorities

- The active contract is always visible at the top center.
- Parent A and Parent B are shown as large plant/pod previews with genotype and
  phenotype labels.
- The Germination Bed is the largest play surface and displays offspring as
  planted cells.
- The selected specimen panel sits close to the bed so plant actions feel
  immediate.
- The left analyzer panel feels like a botanical lab device and shows only
  analyzer-unlocked information.
- The right navigation rail uses large icon buttons with text labels.

## Portuguese Labels Seen In Reference

- `CONTRATO ATIVO`
- `Entregue 3 ervilhas amarelas lisa`
- `ANALISADOR GENETICO`
- `NIVEL 2`
- `PARENTAL A`
- `PARENTAL B`
- `CRUZAR`
- `DESCENDENTES`
- `ERVILHA`
- `GUARDAR`
- `DESCARTAR`
- `AJUDA`
- `CRUZAMENTO`
- `JARDIM`
- `CONTRATOS`
- `LOJA`
- `COLECAO`
- `CONFIGURACOES`
