"""Greenhouse background for the main game scene."""

import pyxel

from mendels_greenhouse.ui.palette import PyxelColor


def draw_greenhouse_background(
    *,
    background_image: pyxel.Image | None,
    width: int,
    height: int,
) -> None:
    """Draw the main greenhouse background."""
    if background_image is not None:
        pyxel.blt(0, 0, background_image, 0, 0, width, height)
        return

    pyxel.cls(PyxelColor.GREENHOUSE_BG)
    for x in range(0, width, 32):
        pyxel.line(x, 30, x - 40, 180, PyxelColor.TEXT_MUTED)
        pyxel.line(x, 30, x + 40, 180, PyxelColor.FIELD)

    pyxel.rect(0, 258, width, 102, PyxelColor.PANEL_DARK)
    for x in range(0, width, 16):
        pyxel.line(x, 258, x + 8, height, PyxelColor.FRAME)
