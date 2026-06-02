"""Tests for gettext-backed runtime localization."""

from mendels_greenhouse.core.i18n import get_language, set_language, t


def test_portuguese_catalog_translates_runtime_text() -> None:
    set_language("pt-BR")

    assert t("CROSS PLANTS") == "CRUZAR"
    assert t("yellow") == "amarela"


def test_unknown_language_falls_back_to_english() -> None:
    set_language("fr")

    assert get_language() == "en"
    assert t("CROSS PLANTS") == "CROSS PLANTS"
