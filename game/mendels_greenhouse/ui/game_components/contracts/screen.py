"""Contracts screen rendering."""

from dataclasses import dataclass

from mendels_greenhouse.ui.components import Rect, draw_button, draw_panel
from mendels_greenhouse.ui.fonts import draw_text, fit_text
from mendels_greenhouse.ui.game_components.shared import (
    DrawContext,
    draw_scene_shell,
)
from mendels_greenhouse.ui.palette import PyxelColor
from mendels_greenhouse.ui.widgets.progress_bar import ProgressBar

CLAIM_TEXT_MAX_WIDTH = 340


@dataclass(frozen=True)
class ContractsScreenData:
    """Display data for the contracts screen."""

    title: str
    progress_label: str
    progress_width: int
    reward_credits: int
    instruction: str
    claim_enabled: bool


def draw_contracts_screen(
    context: DrawContext,
    data: ContractsScreenData,
) -> None:
    """Draw the contracts screen."""
    translate = context.translate
    draw_scene_shell(
        context,
        "Contract",
        "Use contracts to learn how traits pass between generations.",
    )
    summary_panel = Rect(34, 112, 506, 74)
    detail_panel = Rect(34, 204, 506, 92)
    draw_panel(summary_panel)
    draw_panel(detail_panel)

    draw_text(
        summary_panel.x + 18,
        summary_panel.y + 14,
        fit_text(data.title, summary_panel.width - 36),
        PyxelColor.UI_DARK,
    )

    # Draw progress using the modular ProgressBar widget
    ProgressBar(
        rect=Rect(summary_panel.x + 18, summary_panel.y + 38, 390, 12),
        current_value=data.progress_width,
        target_value=390,
    ).draw()
    draw_text(
        summary_panel.x + 420,
        summary_panel.y + 40,
        data.progress_label,
        PyxelColor.UI_DARK,
    )

    draw_text(
        detail_panel.x + 18,
        detail_panel.y + 18,
        translate("Credits"),
        PyxelColor.UI_DARK,
    )
    draw_text(
        detail_panel.x + 94,
        detail_panel.y + 18,
        f"{data.reward_credits} CR",
        PyxelColor.UI_DARK,
    )
    draw_text(
        detail_panel.x + 18,
        detail_panel.y + 40,
        fit_text(data.instruction, detail_panel.width - 36),
        PyxelColor.UI_DARK,
    )
    status = (
        "Contract complete. Claim reward."
        if data.claim_enabled
        else "Use contracts to learn how traits pass between generations."
    )
    draw_text(
        detail_panel.x + 18,
        detail_panel.y + 58,
        fit_text(
            translate(status),
            CLAIM_TEXT_MAX_WIDTH,
        ),
        PyxelColor.UI_DARK,
    )
    draw_button(
        Rect(408, 250, 96, 24),
        translate("CLAIM"),
        enabled=data.claim_enabled,
    )
