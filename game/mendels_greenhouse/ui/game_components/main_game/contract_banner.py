"""Active contract banner for the main game scene."""

from dataclasses import dataclass

import pyxel

from mendels_greenhouse.ui.components import Rect, draw_button, draw_panel
from mendels_greenhouse.ui.fonts import draw_outlined_text
from mendels_greenhouse.ui.game_components.shared import DrawContext
from mendels_greenhouse.ui.palette import PyxelColor
from mendels_greenhouse.ui.widgets.progress_bar import ProgressBar


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
    """Draw the compact active-contract banner next to the status counters."""
    rect = Rect(286, 12, 266, 34)
    draw_panel(rect)

    # Redraw active contract title centered above the panel
    header = context.translate("ACTIVE CONTRACT").upper()
    hx = rect.x + (rect.width - len(header) * 4) // 2
    draw_outlined_text(
        hx,
        4,
        header,
        PyxelColor.ACCENT,
        font=context.display_font,
    )

    # Contract Goal text
    pyxel.text(rect.x + 8, rect.y + 6, data.title, PyxelColor.UI_DARK)

    if data.claim_enabled:
        # Draw CLAIM button on the right side of the panel
        draw_button(data.claim_button, context.translate("CLAIM"))
    else:
        # Draw progress bar and ratio text
        ProgressBar(
            rect=Rect(rect.x + 8, rect.y + 18, 200, 8),
            current_value=data.progress_width,
            target_value=200,
        ).draw()

        pyxel.text(
            rect.x + 214,
            rect.y + 19,
            data.progress_label,
            PyxelColor.UI_DARK,
        )
