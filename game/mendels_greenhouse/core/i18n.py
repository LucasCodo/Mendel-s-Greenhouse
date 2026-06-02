"""Runtime localization helpers for Mendel's Greenhouse."""

import gettext
from pathlib import Path

DOMAIN = "mendels_greenhouse"
DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ("en", "pt-BR")
LOCALE_DIR = Path(__file__).resolve().parents[1] / "locale"

_state = {
    "language": DEFAULT_LANGUAGE,
    "translation": gettext.NullTranslations(),
}


def set_language(language: str) -> None:
    """Set the active runtime language."""
    normalized = _normalize_language(language)
    active_language = (
        language if language in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
    )
    _state["language"] = active_language
    _state["translation"] = gettext.translation(
        DOMAIN,
        localedir=LOCALE_DIR,
        languages=[normalized],
        fallback=True,
    )


def get_language() -> str:
    """Return the active user-facing language code."""
    return str(_state["language"])


def t(message: str, **kwargs: object) -> str:
    """Translate a message and apply optional format placeholders."""
    translation = _state["translation"]
    translated = translation.gettext(message)
    if kwargs:
        return translated.format(**kwargs)
    return translated


def gettext_noop(message: str) -> str:
    """Mark a message for extraction without translating it."""
    return message


def _normalize_language(language: str) -> str:
    if language == "pt-BR":
        return "pt_BR"
    if language in SUPPORTED_LANGUAGES:
        return language
    return DEFAULT_LANGUAGE


set_language(DEFAULT_LANGUAGE)
