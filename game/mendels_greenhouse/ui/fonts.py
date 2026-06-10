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


def draw_bold_outlined_text(
    x: int,
    y: int,
    text: str,
    color: int,
    *,
    font: pyxel.Font | None = None,
) -> None:
    """Draw bold text with a 1-pixel dark outline."""
    outline = PyxelColor.UI_DARK
    # Outline around the bold footprint (x-1 to x+2, y-1 to y+1)
    for dx in [-1, 0, 1, 2]:
        for dy in [-1, 1]:
            pyxel.text(x + dx, y + dy, text, outline, font)
    pyxel.text(x - 1, y, text, outline, font)
    pyxel.text(x + 2, y, text, outline, font)

    # Bold body
    draw_text(x, y, text, color, font=font)
    draw_text(x + 1, y, text, color, font=font)


def draw_bold_spaced_text(  # noqa: PLR0913
    x: int,
    y: int,
    text: str,
    color: int,
    *,
    extra_spacing: int = 2,
    bold_thickness: int = 3,
    font: pyxel.Font | None = None,
) -> None:
    """Draw bold outlined text with letter spacing and custom thickness.

    The text is outlined by a 1-pixel dark border.
    """
    outline = PyxelColor.UI_DARK
    current_x = x
    for char in text:
        # Draw outline around the bold footprint for this character
        # The bold body spans from dx = 0 to dx = bold_thickness - 1
        # Therefore, the outline spans dx from -1 to bold_thickness,
        # and dy from -1 to 1.
        for dx in range(-1, bold_thickness + 1):
            for dy in [-1, 1]:
                pyxel.text(current_x + dx, y + dy, char, outline, font)
        # Left and right side outlines at dy = 0
        pyxel.text(current_x - 1, y, char, outline, font)
        pyxel.text(current_x + bold_thickness, y, char, outline, font)

        # Draw bold body
        for dx in range(bold_thickness):
            pyxel.text(current_x + dx, y, char, color, font)

        # Advance current_x by character width (6px) + extra_spacing
        current_x += 6 + extra_spacing
