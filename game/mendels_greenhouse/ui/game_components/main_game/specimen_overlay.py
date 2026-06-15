"""Selected specimen overlay for the main game scene."""

from collections.abc import Callable
from dataclasses import dataclass

import pyxel

from mendels_greenhouse.core.genetics import Plant
from mendels_greenhouse.ui.components import (
    Rect,
    draw_button,
    draw_panel,
    draw_rounded_panel,
)
from mendels_greenhouse.ui.fonts import draw_text, fit_text, text_width
from mendels_greenhouse.ui.game_components.shared import (
    DrawContext,
    draw_modal_scrim,
)
from mendels_greenhouse.ui.palette import PyxelColor

PlantPreview = Callable[[int, int, Plant, bool], None]


@dataclass(frozen=True)
class SpecimenOverlayData:
    """Display data for the selected specimen overlay."""

    panel: Rect
    store_button: Rect
    discard_button: Rect
    close_button: Rect
    plant: Plant
    can_store: bool
    visible_genotype: str
    trait_lines: list[str]


def draw_specimen_overlay(
    context: DrawContext,
    data: SpecimenOverlayData,
    *,
    plant_preview: PlantPreview,
) -> None:
    """Draw an inspection card over the current gameplay screen."""
    translate = context.translate
    draw_modal_scrim(0.58)
    draw_panel(data.panel)

    header = Rect(
        data.panel.x + 4,
        data.panel.y + 4,
        data.panel.width - 8,
        24,
    )
    draw_rounded_panel(
        header,
        PyxelColor.UI_DARK,
        PyxelColor.FRAME,
        PyxelColor.WOOD_MIDTONE,
    )
    species = translate(data.plant.species).upper()
    draw_text(
        header.x + 12,
        header.y + 8,
        fit_text(species, header.width - 48),
        PyxelColor.ACCENT,
    )
    draw_button(data.close_button, "X")

    preview = Rect(data.panel.x + 16, data.panel.y + 40, 132, 172)
    draw_rounded_panel(
        preview,
        PyxelColor.DEEP_GLASS_NAVY,
        PyxelColor.FRAME,
        PyxelColor.LEAF_SHADOW,
    )
    _draw_preview_atmosphere(preview)
    plant_preview(
        preview.x + preview.width // 2,
        preview.y + 124,
        data.plant,
        True,
    )

    details_x = data.panel.x + 166
    details_width = data.panel.width - 182
    next_detail_y = _draw_detail_row(
        details_x,
        data.panel.y + 48,
        translate("Phenotype"),
        data.trait_lines,
        details_width,
        PyxelColor.LEAF_HIGHLIGHT,
    )
    next_detail_y = _draw_detail_row(
        details_x,
        next_detail_y,
        translate("Genotype"),
        [data.visible_genotype],
        details_width,
        PyxelColor.UI_DARK,
    )
    _draw_detail_row(
        details_x,
        next_detail_y,
        translate("Generation"),
        [data.plant.generation_label],
        details_width,
        PyxelColor.UI_DARK,
    )

    draw_button(
        data.store_button,
        translate("STORE"),
        enabled=data.can_store,
    )
    _draw_discard_button(data.discard_button, translate("DISCARD"))


def _draw_preview_atmosphere(rect: Rect) -> None:
    for x, y in (
        (rect.x + 14, rect.y + 18),
        (rect.x + 112, rect.y + 28),
        (rect.x + 20, rect.y + 144),
        (rect.x + 104, rect.y + 150),
    ):
        draw_text(x, y, "+", PyxelColor.LEAF_HIGHLIGHT)
    pyxel.line(
        rect.x + 14,
        rect.y + 154,
        rect.x + rect.width - 15,
        rect.y + 154,
        PyxelColor.LEAF_SHADOW,
    )


def _draw_detail_row(  # noqa: PLR0913
    x: int,
    y: int,
    label: str,
    values: list[str],
    width: int,
    value_color: int,
) -> int:
    draw_text(x, y, f"{label}:", PyxelColor.UI_DARK)
    for index, value in enumerate(values):
        draw_text(
            x,
            y + 13 + index * 11,
            fit_text(value, width),
            value_color,
        )
    separator_y = y + 17 + len(values) * 11
    pyxel.line(x, separator_y, x + width, separator_y, PyxelColor.WOOD_MIDTONE)
    return separator_y + 8


def _draw_discard_button(rect: Rect, label: str) -> None:
    hovering = rect.contains(pyxel.mouse_x, pyxel.mouse_y)
    fill = PyxelColor.TOMATO_ORANGE if hovering else PyxelColor.TOMATO_RED
    draw_rounded_panel(
        rect,
        fill,
        PyxelColor.FRAME,
        PyxelColor.UI_DARK,
    )
    fitted_label = fit_text(label, rect.width - 16)
    text_x = rect.x + (rect.width - text_width(fitted_label)) // 2
    text_y = rect.y + (rect.height - 8) // 2
    draw_text(text_x + 1, text_y + 1, fitted_label, PyxelColor.UI_DARK)
    draw_text(text_x, text_y, fitted_label, PyxelColor.PARCHMENT_LIGHT)
