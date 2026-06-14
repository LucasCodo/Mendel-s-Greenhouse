"""Garden screen rendering."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import pyxel

from mendels_greenhouse.core.genetics import Plant
from mendels_greenhouse.ui.components import Rect, draw_button, draw_panel
from mendels_greenhouse.ui.fonts import draw_text, fit_text
from mendels_greenhouse.ui.game_components.shared import (
    DrawContext,
    draw_scene_shell,
)
from mendels_greenhouse.ui.palette import PyxelColor

PlantPreview = Callable[[int, int, Plant], None]
PlantPreviewLarge = Callable[[int, int, Plant, bool], None]

GARDEN_PARENT_A_BUTTON = Rect(392, 238, 96, 22)
GARDEN_PARENT_B_BUTTON = Rect(392, 264, 96, 22)
GARDEN_DISCARD_BUTTON = Rect(392, 290, 96, 22)


@dataclass(frozen=True)
class GardenScreenData:
    """Display data for the garden screen."""

    slots: Sequence[Plant | None]
    capacity: int
    used_slots: int
    selected_slot: int
    selected_plant: Plant | None
    can_discard_selected: bool
    discard_button: Rect


def draw_garden_screen(
    context: DrawContext,
    data: GardenScreenData,
    *,
    plant_preview: PlantPreviewLarge,
    visible_genotype: Callable[[Plant], str],
    trait_lines: Callable[[Plant], list[str]],
) -> None:
    """Draw the garden screen."""
    translate = context.translate
    draw_scene_shell(context, "Garden", "Stored plants and parent selection")
    draw_text(
        476,
        86,
        translate(
            "Slots: {used}/{capacity}",
            used=data.used_slots,
            capacity=data.capacity,
        ),
        PyxelColor.PARCHMENT_LIGHT,
    )
    grid_panel = Rect(24, 104, 294, 214)
    detail_panel = Rect(338, 104, 206, 214)
    draw_panel(grid_panel)
    draw_panel(detail_panel)
    for index in range(20):
        _draw_greenhouse_slot(context, data, index, plant_preview)

    draw_text(354, 122, translate("SELECTED PLANT"), PyxelColor.UI_DARK)
    selected = data.selected_plant
    if selected is None:
        draw_text(
            354,
            146,
            translate("Empty or locked slot."),
            PyxelColor.UI_DARK,
        )
        return

    plant_preview(382, 174, selected, True)
    draw_text(
        420,
        132,
        translate(
            "Generation: {generation}",
            generation=selected.generation_label,
        ),
        PyxelColor.UI_DARK,
    )
    draw_text(
        420,
        146,
        translate(
            "Genotype: {genotype}",
            genotype=visible_genotype(selected),
        ),
        PyxelColor.UI_DARK,
    )
    for line_index, line in enumerate(trait_lines(selected)):
        draw_text(
            354,
            184 + line_index * 9,
            fit_text(line, detail_panel.width - 32),
            PyxelColor.UI_DARK,
        )
    draw_button(GARDEN_PARENT_A_BUTTON, translate("PARENT A"))
    draw_button(GARDEN_PARENT_B_BUTTON, translate("PARENT B"))
    draw_button(
        data.discard_button,
        translate("DISCARD"),
        enabled=data.can_discard_selected,
    )


def greenhouse_slot_rect(
    index: int,
    *,
    columns: int,
    slot_size: int,
) -> Rect:
    """Return the garden slot rectangle for an index."""
    col = index % columns
    row = index // columns
    return Rect(38 + col * 54, 118 + row * 46, slot_size, slot_size)


def _draw_greenhouse_slot(
    context: DrawContext,
    data: GardenScreenData,
    index: int,
    plant_preview: PlantPreviewLarge,
) -> None:
    rect = greenhouse_slot_rect(index, columns=5, slot_size=44)
    unlocked = index < data.capacity
    selected = index == data.selected_slot
    fill = PyxelColor.PARCHMENT if unlocked else PyxelColor.TEXT_MUTED
    if selected:
        fill = PyxelColor.ACCENT
    pyxel.rect(rect.x, rect.y, rect.width, rect.height, fill)
    pyxel.rectb(rect.x, rect.y, rect.width, rect.height, PyxelColor.FRAME)
    pyxel.rectb(
        rect.x + 1,
        rect.y + 1,
        rect.width - 2,
        rect.height - 2,
        PyxelColor.UI_DARK,
    )
    translate = context.translate
    if not unlocked:
        draw_text(
            rect.x + 13,
            rect.y + 19,
            translate("LOCK"),
            PyxelColor.UI_DARK,
        )
        return
    plant = data.slots[index] if index < len(data.slots) else None
    if plant is None:
        draw_text(
            rect.x + 14,
            rect.y + 19,
            translate("Empty slot").upper()[:5],
            PyxelColor.UI_DARK,
        )
        return
    plant_preview(rect.x + 22, rect.y + 42, plant, False)
