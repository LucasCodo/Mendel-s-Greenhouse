"""Top bar for the main game scene."""

from collections.abc import Callable
from dataclasses import dataclass

import pyxel

from mendels_greenhouse.ui.fonts import draw_outlined_text
from mendels_greenhouse.ui.game_components.main_game.chrome import (
    draw_runtime_hud_frame,
    draw_runtime_logo,
)
from mendels_greenhouse.ui.palette import PyxelColor


@dataclass(frozen=True)
class TopBarData:
    """Display data for the main game top bar."""

    credits: int
    greenhouse_used: int
    greenhouse_capacity: int
    active_screen_title: str


def draw_top_bar(
    *,
    data: TopBarData,
    translate: Callable[[str], str],
    display_font: pyxel.Font | None,
) -> None:
    """Draw the main game top bar."""
    draw_runtime_hud_frame(5, 4, 544, 58)
    draw_runtime_logo(16, 10)
    draw_outlined_text(
        24,
        13,
        "MENDEL'S",
        PyxelColor.PEA_GREEN,
        font=display_font,
    )
    draw_outlined_text(
        20,
        24,
        "GREENHOUSE",
        PyxelColor.ACCENT,
        font=display_font,
    )
    _draw_counter(118, "CR", str(data.credits))
    garden = f"{data.greenhouse_used}/{data.greenhouse_capacity}"
    _draw_counter(198, "GDN", garden)
    pyxel.text(
        294,
        41,
        translate(data.active_screen_title).upper()[:18],
        PyxelColor.ACCENT,
    )


def _draw_counter(x: int, icon: str, value: str) -> None:
    pyxel.rect(x, 41, 72, 14, PyxelColor.UI_DARK)
    pyxel.rectb(x, 41, 72, 14, PyxelColor.FRAME)
    pyxel.text(x + 5, 46, icon, PyxelColor.ACCENT)
    pyxel.text(x + 27, 46, value, PyxelColor.TEXT)
