"""Contracts screen rendering."""

from dataclasses import dataclass

import pyxel

from mendels_greenhouse.ui.components import Rect, draw_button, draw_panel
from mendels_greenhouse.ui.game_components.shared import (
    DrawContext,
    draw_scene_shell,
)
from mendels_greenhouse.ui.palette import PyxelColor
from mendels_greenhouse.ui.widgets.progress_bar import ProgressBar


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
        "CONTRACT",
        "Use contracts to learn how traits pass between generations.",
    )
    summary_panel = Rect(34, 112, 506, 74)
    detail_panel = Rect(34, 204, 506, 92)
    draw_panel(summary_panel)
    draw_panel(detail_panel)

    pyxel.text(
        summary_panel.x + 18,
        summary_panel.y + 14,
        data.title,
        PyxelColor.UI_DARK,
    )

    # Draw progress using the modular ProgressBar widget
    ProgressBar(
        rect=Rect(summary_panel.x + 18, summary_panel.y + 38, 390, 12),
        current_value=data.progress_width,
        target_value=390,
    ).draw()
    pyxel.text(
        summary_panel.x + 420,
        summary_panel.y + 40,
        data.progress_label,
        PyxelColor.UI_DARK,
    )

    pyxel.text(
        detail_panel.x + 18,
        detail_panel.y + 18,
        translate("Credits"),
        PyxelColor.UI_DARK,
    )
    pyxel.text(
        detail_panel.x + 94,
        detail_panel.y + 18,
        f"{data.reward_credits} CR",
        PyxelColor.UI_DARK,
    )
    pyxel.text(
        detail_panel.x + 18,
        detail_panel.y + 40,
        data.instruction,
        PyxelColor.UI_DARK,
    )
    status = (
        "Contract complete. Claim reward."
        if data.claim_enabled
        else "Use contracts to learn how traits pass between generations."
    )
    pyxel.text(
        detail_panel.x + 18,
        detail_panel.y + 58,
        translate(status),
        PyxelColor.UI_DARK,
    )
    draw_button(
        Rect(408, 250, 96, 24),
        translate("CLAIM"),
        enabled=data.claim_enabled,
    )
