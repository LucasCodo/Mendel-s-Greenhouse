import string

from tools.build_assets import GLYPHS, ICONS

from mendels_greenhouse.ui.fonts import FontSet, fit_text


def test_display_font_covers_runtime_characters() -> None:
    runtime_characters = (
        string.ascii_letters + string.digits + " !%()*+,-./:<=>?'"
    )

    assert set(runtime_characters) <= GLYPHS.keys()


def test_fit_text_respects_pixel_width() -> None:
    FontSet.active_display = None

    assert fit_text("ABCDEFGHIJ", 40) == "ABCDEFGHIJ"
    assert fit_text("ABCDEFGHIJ", 28) == "ABCD..."


def test_contract_navigation_icon_uses_expected_atlas_slot() -> None:
    assert ICONS["contract"] == (128, 128)
