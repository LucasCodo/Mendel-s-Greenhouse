"""Shared main game chrome drawing helpers."""

import pyxel

from mendels_greenhouse.ui.palette import PyxelColor


def draw_runtime_hud_frame(
    x: int,
    y: int,
    width: int,
    height: int,
) -> None:
    """Draw the framed runtime HUD surface used by top and side chrome."""
    # Draw rounded filled panel background (radius 4)
    pyxel.rect(x + 4, y, width - 8, 1, PyxelColor.PANEL_DARK)
    pyxel.rect(x + 2, y + 1, width - 4, 1, PyxelColor.PANEL_DARK)
    pyxel.rect(x + 1, y + 2, width - 2, 1, PyxelColor.PANEL_DARK)
    pyxel.rect(x, y + 3, width, height - 6, PyxelColor.PANEL_DARK)
    pyxel.rect(x + 1, y + height - 3, width - 2, 1, PyxelColor.PANEL_DARK)
    pyxel.rect(x + 2, y + height - 2, width - 4, 1, PyxelColor.PANEL_DARK)
    pyxel.rect(x + 4, y + height - 1, width - 8, 1, PyxelColor.PANEL_DARK)

    # Draw rounded outer border (radius 4)
    pyxel.line(x + 4, y, x + width - 5, y, PyxelColor.SPRITE_OUTLINE)
    pyxel.line(
        x + 4,
        y + height - 1,
        x + width - 5,
        y + height - 1,
        PyxelColor.SPRITE_OUTLINE,
    )
    pyxel.line(x, y + 3, x, y + height - 4, PyxelColor.SPRITE_OUTLINE)
    pyxel.line(
        x + width - 1,
        y + 3,
        x + width - 1,
        y + height - 4,
        PyxelColor.SPRITE_OUTLINE,
    )
    # Corner borders
    pyxel.line(x + 2, y + 1, x + 3, y + 1, PyxelColor.SPRITE_OUTLINE)
    pyxel.pset(x + 1, y + 2, PyxelColor.SPRITE_OUTLINE)
    pyxel.line(
        x + width - 4,
        y + 1,
        x + width - 3,
        y + 1,
        PyxelColor.SPRITE_OUTLINE,
    )
    pyxel.pset(x + width - 2, y + 2, PyxelColor.SPRITE_OUTLINE)

    pyxel.line(
        x + 2,
        y + height - 2,
        x + 3,
        y + height - 2,
        PyxelColor.SPRITE_OUTLINE,
    )
    pyxel.pset(x + 1, y + height - 3, PyxelColor.SPRITE_OUTLINE)
    pyxel.line(
        x + width - 4,
        y + height - 2,
        x + width - 3,
        y + height - 2,
        PyxelColor.SPRITE_OUTLINE,
    )
    pyxel.pset(x + width - 2, y + height - 3, PyxelColor.SPRITE_OUTLINE)

    # Inner highlight frame
    pyxel.rectb(x + 2, y + 2, width - 4, height - 4, PyxelColor.FRAME)

    for line_y in range(y + 10, y + height - 6, 9):
        pyxel.line(
            x + 4,
            line_y,
            x + width - 5,
            line_y,
            PyxelColor.DARK_WOOD,
        )
    for corner_x in [x + 3, x + width - 4]:
        pyxel.pset(corner_x, y + 3, PyxelColor.ACCENT)
        pyxel.pset(corner_x, y + height - 4, PyxelColor.ACCENT)


def draw_runtime_logo(x: int, y: int) -> None:
    """Draw the compact Mendel's Greenhouse logo plaque."""
    pyxel.rect(x, y + 2, 34, 30, PyxelColor.DARK_WOOD)
    pyxel.rectb(x, y + 2, 34, 30, PyxelColor.SPRITE_OUTLINE)
    pyxel.line(x + 5, y + 8, x + 18, y + 4, PyxelColor.POD_HIGHLIGHT)
    pyxel.line(x + 5, y + 22, x + 18, y + 29, PyxelColor.POD_SHADOW)
    pyxel.circ(x + 12, y + 17, 7, PyxelColor.SEED_GOLD)
    pyxel.circb(x + 12, y + 17, 7, PyxelColor.SPRITE_OUTLINE)
    pyxel.circ(x + 23, y + 16, 7, PyxelColor.PEA_GREEN)
    pyxel.circb(x + 23, y + 16, 7, PyxelColor.SPRITE_OUTLINE)
