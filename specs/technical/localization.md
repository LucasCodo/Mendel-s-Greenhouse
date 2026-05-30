# Localization Specification

## Purpose

Mendel's Greenhouse must support two initial languages:

- English (`en`)
- Brazilian Portuguese (`pt-BR`)

Localization applies to UI labels, contracts, tutorial text, educational explanations, settings, popups, collection labels, analyzer text, and future account/save UI.

## Recommended Approach

Use Python's `gettext` runtime for translated strings and Babel tooling for extracting and managing message catalogs.

Rationale:

- `gettext` is part of Python's standard library and supports `.mo` message catalogs at runtime.
- Babel builds on gettext catalogs and provides practical tooling for extracting messages from Python projects.
- This keeps the game compatible with Pyxel while leaving room for future NiceGUI web UI localization.

## Locale Policy

### Supported Locales

| Locale | Language |
| ------ | -------- |
| `en` | English |
| `pt-BR` | Brazilian Portuguese |

### Source Language

Use English as the source language for message IDs.

Example:

```python
_("Start Crossbreeding")
```

### Fallback Rule

If a translation is missing, fall back to English.

## Directory Structure

Localization files should live inside the package so they can ship with the game.

Recommended layout:

```text
mendels_greenhouse/
|-- assets/
|   `-- mendels_greenhouse.pyxres
`-- locale/
    |-- en/
    |   `-- LC_MESSAGES/
    |       |-- mendels_greenhouse.po
    |       `-- mendels_greenhouse.mo
    `-- pt_BR/
        `-- LC_MESSAGES/
            |-- mendels_greenhouse.po
            `-- mendels_greenhouse.mo
```

Use `pt-BR` in UI/settings and user-facing documentation. Use `pt_BR` for filesystem paths when required by gettext conventions.

## Translation Domain

Use one gettext domain for the game:

```text
mendels_greenhouse
```

## Runtime API

Create a small localization module:

```text
mendels_greenhouse/core/i18n.py
```

Required responsibilities:

- Load the active locale.
- Provide a translation function.
- Fall back to English.
- Allow changing language from settings without restarting when practical.
- Keep all user-facing text out of gameplay logic when possible.

Suggested API:

```python
set_language("en")
set_language("pt-BR")
t("Start Crossbreeding")
```

Implementation may wrap `gettext.translation(...).gettext`.

## Language Switching

The Settings Screen must expose a language option:

```text
Language: English / Portugues (Brasil)
```

Rules:

- Language can be changed by the player.
- The selected language should affect all visible UI text.
- The MVP may keep the selection in memory until a save/preferences system exists.
- Future NiceGUI save/account layer may persist language preference per user.

## Text Authoring Rules

- Do not hardcode user-facing strings directly in rendering code without passing through the localization function.
- Keep string IDs stable.
- Prefer complete phrases over assembling translated fragments.
- Avoid embedding grammar-sensitive words in code.
- Use placeholders for dynamic values.

Example:

```python
t("Contract progress: {current}/{target}").format(current=3, target=10)
```

## Pixel Art UI Constraints

Localized text must fit the Pyxel UI.

Rules:

- Portuguese strings may be longer than English strings.
- Buttons and panels must reserve extra horizontal space.
- Use compact labels where needed.
- Prefer icons plus short text for repeated actions.
- Avoid long tutorial paragraphs.
- Test both languages in the `256 x 144` internal resolution.

## Initial Glossary

| English | Portuguese |
| ------- | ---------- |
| Greenhouse | Estufa |
| Contract | Contrato |
| Crossbreeding | Cruzamento |
| Genetic Analyzer | Analisador Genetico |
| Phenotype | Fenotipo |
| Genotype | Genotipo |
| Gene | Gene |
| Allele | Alelo |
| Collection | Colecao |
| Credits | Creditos |
| Store | Armazenar |
| Sell | Vender |
| Deliver | Entregar |
| Probability | Probabilidade |
| Discovery | Descoberta |

Use ASCII in source files unless the file explicitly requires translated prose. `.po` files may contain accented Portuguese strings.

## Tooling

Babel manages extraction and catalog workflows. Poe the Poet runs the standard project commands.

Required Poe tasks:

```powershell
poe i18n-extract
poe i18n-update
poe i18n-compile
```

These tasks should call Babel's `pybabel` CLI. Do not start with a custom translation compiler script.

## Acceptance Criteria

- English and Brazilian Portuguese are selectable.
- Core MVP UI text is localized.
- Contract text can render in both languages.
- Tutorial/onboarding text supports both languages.
- Missing translations fall back to English.
- Both languages fit the main game screen at `256 x 144`.
- No gameplay rule depends on the display language.

## References

- [Python gettext documentation](https://docs.python.org/3/library/gettext.html)
- [Babel message catalog documentation](https://babel.pocoo.org/en/latest/messages.html)
