"""Garden screen rendering."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import pyxel

from mendels_greenhouse.core.genetics import Plant
from mendels_greenhouse.ui.components import Rect, draw_button, draw_panel
from mendels_greenhouse.ui.game_components.shared import (
    DrawContext,
    draw_scene_shell,
)
from mendels_greenhouse.ui.palette import PyxelColor

PlantPreview = Callable[[int, int, Plant], None]
PlantPreviewLarge = Callable[[int, int, Plant, bool], None]


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
    pyxel.text(
        476,
        86,
        f"Slots: {data.used_slots}/20",
        PyxelColor.PARCHMENT_LIGHT,
    )
    grid_panel = Rect(24, 104, 294, 214)
    detail_panel = Rect(338, 104, 206, 178)
    draw_panel(grid_panel)
    draw_panel(detail_panel)
    for index in range(20):
        _draw_greenhouse_slot(context, data, index, plant_preview)

    pyxel.text(354, 122, translate("SELECTED PLANT"), PyxelColor.UI_DARK)
    selected = data.selected_plant
    if selected is None:
        pyxel.text(
            354,
            146,
            translate("Empty or locked slot."),
            PyxelColor.UI_DARK,
        )
        return

    plant_preview(382, 205, selected, True)
    pyxel.text(
        428,
        146,
        translate(
            "Generation: {generation}",
            generation=selected.generation_label,
        ),
        PyxelColor.UI_DARK,
    )
    pyxel.text(
        428,
        160,
        f"Genotype: {visible_genotype(selected)}",
        PyxelColor.UI_DARK,
    )
    for line_index, line in enumerate(trait_lines(selected)):
        pyxel.text(428, 174 + line_index * 14, line, PyxelColor.UI_DARK)
    draw_button(Rect(392, 201, 96, 22), translate("PARENT A"))
    draw_button(Rect(392, 229, 96, 22), translate("PARENT B"))
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
        pyxel.text(
            rect.x + 13,
            rect.y + 19,
            translate("LOCK"),
            PyxelColor.UI_DARK,
        )
        return
    plant = data.slots[index] if index < len(data.slots) else None
    if plant is None:
        pyxel.text(
            rect.x + 14,
            rect.y + 19,
            translate("Empty slot").upper()[:5],
            PyxelColor.UI_DARK,
        )
        return
    plant_preview(rect.x + 22, rect.y + 42, plant, False)
