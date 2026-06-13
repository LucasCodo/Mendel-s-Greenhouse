"""Font loading and text helpers."""

from pathlib import Path

import pyxel

from mendels_greenhouse.ui.palette import PyxelColor

DISPLAY_GLYPH_WIDTH = 6
DISPLAY_GLYPH_HEIGHT = 8


class FontSet:
    """Project font bundle."""

    active_display: pyxel.Font | None = None

    def __init__(self, assets_dir: Path) -> None:
        font_path = assets_dir / "mendel_5x7.bdf"
        self.display = (
            pyxel.Font(str(font_path)) if font_path.exists() else None
        )
        FontSet.active_display = self.display


def _resolve_font(font: pyxel.Font | None) -> pyxel.Font | None:
    return font or FontSet.active_display


def draw_text(
    x: int,
    y: int,
    text: str,
    color: int,
    font: pyxel.Font | None = None,
) -> None:
    """Draw text with the project font when provided."""
    pyxel.text(x, y, text, color, _resolve_font(font))


def text_width(text: str, font: pyxel.Font | None = None) -> int:
    """Return rendered text width for the active project font."""
    active_font = _resolve_font(font)
    if active_font is not None:
        return active_font.text_width(text)
    return len(text) * pyxel.FONT_WIDTH


def fit_text(
    text: str,
    max_width: int,
    font: pyxel.Font | None = None,
) -> str:
    """Truncate text with an ellipsis so it fits a pixel width."""
    if text_width(text, font) <= max_width:
        return text

    ellipsis = "..."
    available_width = max_width - text_width(ellipsis, font)
    if available_width <= 0:
        return ""

    fitted = ""
    for character in text:
        candidate = fitted + character
        if text_width(candidate, font) > available_width:
            break
        fitted = candidate
    return fitted.rstrip() + ellipsis


def draw_shadow_text(
    x: int,
    y: int,
    text: str,
    color: int,
    *,
    font: pyxel.Font | None = None,
) -> None:
    """Draw text with a one-pixel dark shadow."""
    pyxel.text(
        x + 1,
        y + 1,
        text,
        PyxelColor.UI_DARK,
        _resolve_font(font),
    )
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
    active_font = _resolve_font(font)
    pyxel.text(x - 1, y, text, outline, active_font)
    pyxel.text(x + 1, y, text, outline, active_font)
    pyxel.text(x, y - 1, text, outline, active_font)
    pyxel.text(x, y + 1, text, outline, active_font)
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
    active_font = _resolve_font(font)
    # Outline around the bold footprint (x-1 to x+2, y-1 to y+1)
    for dx in [-1, 0, 1, 2]:
        for dy in [-1, 1]:
            pyxel.text(x + dx, y + dy, text, outline, active_font)
    pyxel.text(x - 1, y, text, outline, active_font)
    pyxel.text(x + 2, y, text, outline, active_font)

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
    active_font = _resolve_font(font)
    current_x = x
    for char in text:
        # Draw outline around the bold footprint for this character
        # The bold body spans from dx = 0 to dx = bold_thickness - 1
        # Therefore, the outline spans dx from -1 to bold_thickness,
        # and dy from -1 to 1.
        for dx in range(-1, bold_thickness + 1):
            for dy in [-1, 1]:
                pyxel.text(
                    current_x + dx,
                    y + dy,
                    char,
                    outline,
                    active_font,
                )
        # Left and right side outlines at dy = 0
        pyxel.text(current_x - 1, y, char, outline, active_font)
        pyxel.text(
            current_x + bold_thickness,
            y,
            char,
            outline,
            active_font,
        )

        # Draw bold body
        for dx in range(bold_thickness):
            pyxel.text(current_x + dx, y, char, color, active_font)

        # Advance current_x by character width (6px) + extra_spacing
        current_x += 6 + extra_spacing
