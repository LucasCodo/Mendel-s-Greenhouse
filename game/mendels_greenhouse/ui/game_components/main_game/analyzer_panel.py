"""Analyzer/probability panel for the main game scene."""

from dataclasses import dataclass

import pyxel

from mendels_greenhouse.ui.components import Rect, draw_panel
from mendels_greenhouse.ui.fonts import draw_outlined_text
from mendels_greenhouse.ui.game_components.shared import DrawContext
from mendels_greenhouse.ui.palette import PyxelColor


@dataclass(frozen=True)
class AnalyzerPanelData:
    """Display data for the analyzer probability panel."""

    has_parent_pair: bool
    analyzer_level: int
    probability_level: int
    simulator_level: int
    probability_lines: list[str]
    best_cross: str | None
    max_probability_y: int


def draw_analyzer_panel(
    context: DrawContext,
    data: AnalyzerPanelData,
) -> None:
    """Draw the left analyzer probability panel."""
    translate = context.translate
    rect = Rect(12, 74, 132, 112)
    draw_panel(rect)
    draw_outlined_text(
        18,
        80,
        translate("PROBABILITIES"),
        PyxelColor.ACCENT,
        font=context.display_font,
    )
    if not data.has_parent_pair:
        pyxel.text(18, 96, translate("Select parents"), PyxelColor.UI_DARK)
        return
    if data.analyzer_level < data.probability_level:
        pyxel.text(
            18,
            96,
            translate("ANALYZER L3 REQUIRED"),
            PyxelColor.UI_DARK,
        )
        pyxel.text(
            18,
            110,
            translate("Upgrade analyzer in Shop."),
            PyxelColor.UI_DARK,
        )
        return

    y = 94
    for line in data.probability_lines:
        pyxel.text(18, y, line, PyxelColor.UI_DARK)
        y += 10
        if y > data.max_probability_y:
            break
    if data.analyzer_level >= data.simulator_level:
        pyxel.text(
            18,
            168,
            translate("Best stored cross"),
            PyxelColor.UI_DARK,
        )
        pyxel.text(
            18,
            178,
            data.best_cross
            if data.best_cross is not None
            else translate("No valid stored cross found."),
            PyxelColor.UI_DARK,
        )
