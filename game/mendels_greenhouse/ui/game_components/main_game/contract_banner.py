"""Active contract banner for the main game scene."""

from dataclasses import dataclass

import pyxel

from mendels_greenhouse.ui.components import Rect, draw_button, draw_panel
from mendels_greenhouse.ui.fonts import draw_outlined_text
from mendels_greenhouse.ui.game_components.shared import DrawContext
from mendels_greenhouse.ui.palette import PyxelColor


@dataclass(frozen=True)
class ContractBannerData:
    """Display data for the active contract banner."""

    title: str
    progress_label: str
    progress_width: int
    claim_enabled: bool
    claim_button: Rect


def draw_contract_banner(
    context: DrawContext,
    data: ContractBannerData,
) -> None:
    """Draw the compact active-contract banner."""
    rect = Rect(180, 74, 320, 46)
    draw_panel(rect)
    draw_outlined_text(
        286,
        66,
        context.translate("CONTRACT"),
        PyxelColor.ACCENT,
        font=context.display_font,
    )
    pyxel.text(rect.x + 12, rect.y + 12, data.title, PyxelColor.UI_DARK)
    pyxel.rect(rect.x + 12, rect.y + 29, 235, 8, PyxelColor.BAR_EMPTY)
    pyxel.rect(
        rect.x + 12,
        rect.y + 29,
        data.progress_width,
        8,
        PyxelColor.PROGRESS,
    )
    pyxel.text(
        rect.x + 260,
        rect.y + 30,
        data.progress_label,
        PyxelColor.UI_DARK,
    )
    if data.claim_enabled:
        draw_button(data.claim_button, context.translate("CLAIM"))
