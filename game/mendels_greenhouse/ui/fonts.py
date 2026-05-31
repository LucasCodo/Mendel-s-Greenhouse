"""Font loading and text helpers."""

from pathlib import Path

import pyxel

from mendels_greenhouse.ui.palette import PyxelColor


class FontSet:
    """Project font bundle."""

    def __init__(self, assets_dir: Path) -> None:
        font_path = assets_dir / "mendel_5x7.bdf"
        self.display = (
            pyxel.Font(str(font_path)) if font_path.exists() else None
        )


def draw_text(
    x: int,
    y: int,
    text: str,
    color: int,
    *,
    font: pyxel.Font | None = None,
) -> None:
    """Draw text with the project font when provided."""
    pyxel.text(x, y, text, color, font)


def draw_shadow_text(
    x: int,
    y: int,
    text: str,
    color: int,
    *,
    font: pyxel.Font | None = None,
) -> None:
    """Draw text with a one-pixel dark shadow."""
    pyxel.text(x + 1, y + 1, text, PyxelColor.UI_DARK, font)
    draw_text(x, y, text, color, font=font)


def draw_outlined_text(
    x: int,
    y: int,
    text: str,
    color: int,
    *,
    font: pyxel.Font | None = None,
) -> None:
    """Draw text with a 1-pixel dark outline."""
    outline = PyxelColor.UI_DARK
    pyxel.text(x - 1, y, text, outline, font)
    pyxel.text(x + 1, y, text, outline, font)
    pyxel.text(x, y - 1, text, outline, font)
    pyxel.text(x, y + 1, text, outline, font)
    draw_text(x, y, text, color, font=font)
