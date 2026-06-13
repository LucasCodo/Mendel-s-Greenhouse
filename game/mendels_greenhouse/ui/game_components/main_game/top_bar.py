"""Top bar for the main game scene."""

from collections.abc import Callable
from dataclasses import dataclass

import pyxel

from mendels_greenhouse.ui.components import Rect, draw_rounded_panel
from mendels_greenhouse.ui.fonts import (
    draw_bold_spaced_text,
    draw_text,
)
from mendels_greenhouse.ui.game_components.main_game.chrome import (
    draw_runtime_hud_frame,
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
    translate: Callable[[str], str],  # noqa: ARG001
    display_font: pyxel.Font | None,
) -> None:
    """Draw the main game top bar."""
    # 1. Main horizontal wooden bar ending before the active contract banner
    # (starts at 286)
    draw_runtime_hud_frame(4, 4, 278, 54)

    # 2. Logo text (centered in logo area, new center = 66)
    extra_sp = 2
    thick = 3

    title_m = "MENDEL'S"
    width_m = len(title_m) * (6 + extra_sp) - extra_sp
    tx_m = 66 - width_m // 2
    draw_bold_spaced_text(
        tx_m,
        19,
        title_m,
        PyxelColor.SUCCESS_LIME,
        extra_spacing=extra_sp,
        bold_thickness=thick,
        font=display_font,
    )

    title_g = "GREENHOUSE"
    width_g = len(title_g) * (6 + extra_sp) - extra_sp
    tx_g = 66 - width_g // 2
    draw_bold_spaced_text(
        tx_g,
        31,
        title_g,
        PyxelColor.ACCENT,
        extra_spacing=extra_sp,
        bold_thickness=thick,
        font=display_font,
    )

    # 3. Draw Credits capsule (x=113, y=19, width=80)
    draw_rounded_panel(
        Rect(113, 19, 80, 24),
        PyxelColor.UI_DARK,
        PyxelColor.FRAME,
        PyxelColor.SOIL_DARK,
    )
    # Large coin icon (scale=0.25 -> 16x16 size, centered vertically)
    pyxel.blt(
        113 + 4 - 24,
        23 - 24,
        0,
        0,
        128,
        64,
        64,
        colkey=0,
        scale=0.25,
    )
    # CR and value text
    draw_text(113 + 22, 28, "CR", PyxelColor.ACCENT, display_font)
    draw_text(113 + 36, 28, str(data.credits), PyxelColor.TEXT, display_font)

    # 4. Draw Capacity capsule (x=201, y=19, width=58)
    draw_rounded_panel(
        Rect(201, 19, 58, 24),
        PyxelColor.UI_DARK,
        PyxelColor.FRAME,
        PyxelColor.SOIL_DARK,
    )
    # Large pot/garden icon (scale=0.25 -> 16x16 size, centered vertically)
    pyxel.blt(
        201 + 4 - 24,
        23 - 24,
        0,
        64,
        64,
        64,
        64,
        colkey=0,
        scale=0.25,
    )
    # Capacity value text
    garden = f"{data.greenhouse_used}/{data.greenhouse_capacity}"
    draw_text(201 + 22, 28, garden, PyxelColor.TEXT, display_font)
