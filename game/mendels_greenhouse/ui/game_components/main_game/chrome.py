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
    pyxel.rect(x, y, width, height, PyxelColor.PANEL_DARK)
    pyxel.rectb(x, y, width, height, PyxelColor.SPRITE_OUTLINE)
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
