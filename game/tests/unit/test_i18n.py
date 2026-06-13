"""Tests for gettext-backed runtime localization."""

from mendels_greenhouse.core.i18n import get_language, set_language, t


def test_portuguese_catalog_translates_runtime_text() -> None:
    set_language("pt-BR")

    assert t("CROSS PLANTS") == "CRUZAR"
    assert t("Contract") == "Contrato"
    assert t("Learn") == "Saber"
    assert t("Config.") == "Config."
    assert t("Undiscovered") == "Nao descoberta"
    assert t("{found}/{total} found", found=3, total=9) == ("3/9 encontradas")
    assert t("Generation") == "Geracao"
    assert t("Gametes") == "Gametas"
    assert t("Expected outcomes") == "Resultados esperados"
    assert t("ONLINE") == "ATIVO"
    assert t("Slots: {used}/{capacity}", used=3, capacity=12) == (
        "Espacos: 3/12"
    )
    assert t("yellow") == "amarela"


def test_unknown_language_falls_back_to_english() -> None:
    set_language("fr")

    assert get_language() == "en"
    assert t("CROSS PLANTS") == "CROSS PLANTS"
