---
title: Collection Layout Reference
tags:
  - ui/scenes/collection
  - ui/reference
type: reference
project: mendels-greenhouse
status: active
---

# Collection Layout Reference

This note records the user-provided Collection Scene reference image from the
chat. The image depicts a genetic records screen with category tabs, a central
discovery grid, locked silhouettes, detailed selected-entry information, and the
shared right navigation rail.

> [!important] Visual Target
> The Collection interface should approach [[visual-target|Collection Visual
> Target]] as closely as Pyxel allows.

> [!note] Image File
> The chat attachment was not available as a filesystem file, so this repository
> stores a generated target PNG based on the provided image. Replace
> `references/collection-layout-target.png` with the original exported image
> when available.

## Image

![[specs/ui/scenes/collection/references/collection-layout-target.png]]

## Scene Read

The composition should read as the player's genetic archive. The player first
chooses a record type, scans discovered and hidden cards, then reads details for
the selected entry.

## Layout Zones

```text
+----------------------------------------------------------------------------------+
| Top Bar: logo, credits, capacity                                                  |
+------------------+--------------------------------------+------------------------+
| Collection Header| Entry Grid + Progress Badge           | Right Nav Rail         |
| Category Tabs    | Discovered + locked cards             |                        |
|                  |                                      | Entry Detail Panel     |
+----------------------------------------------------------------------------------+
```

## Portuguese Labels Seen In Reference

- `COLEÇÃO`
- `Registros genéticos descobertos.`
- `ESPÉCIES`
- `FENÓTIPOS`
- `GENÓTIPOS`
- `Descobertos: 5/20`
- `ERVILHA DE MENDEL`
- `Fenótipo`
- `Genótipo`
- `Cor`
- `Textura`
- `INFORMAÇÕES`
- `Tipo`
- `Genes conhecidos`
- `Fenótipos descobertos`
- `Descoberta em`
- `Não descoberta`
- `CRUZAMENTO`
- `JARDIM`
- `CONTRATOS`
- `LOJA`
- `CONFIGURAÇÕES`

