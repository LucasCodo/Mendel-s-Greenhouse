"""Runtime overlay rendering."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import pyxel

from mendels_greenhouse.core.genetics import Plant
from mendels_greenhouse.ui.components import Rect, draw_button, draw_panel
from mendels_greenhouse.ui.fonts import (
    draw_outlined_text,
    draw_text,
    fit_text,
)
from mendels_greenhouse.ui.game_components.plant_info import (
    localized_trait_name,
)
from mendels_greenhouse.ui.game_components.shared import (
    DrawContext,
    draw_modal_scrim,
)
from mendels_greenhouse.ui.palette import PyxelColor

PlantPreview = Callable[[int, int, Plant, bool], None]

PARENT_PICKER_PANEL = Rect(72, 48, 512, 288)
PARENT_PICKER_DETAIL_PANEL = Rect(452, 106, 116, 190)


@dataclass(frozen=True)
class _ParentPickerRenderers:
    """Callbacks needed to draw parent picker slots."""

    plant_preview: PlantPreview
    visible_genotype: Callable[[Plant], str]
    trait: Callable[[str], str]


@dataclass(frozen=True)
class ParentPickerData:
    """Display data for the parent picker overlay."""

    target: str | None
    slots: Sequence[Plant | None]
    capacity: int
    selected_parent_a: int | None
    selected_parent_b: int | None
    close_button: Rect


def draw_intro_panel(context: DrawContext, ok_button: Rect) -> None:
    """Draw the first-run introduction panel."""
    translate = context.translate
    draw_modal_scrim(0.72)
    panel = Rect(92, 56, 456, 272)
    draw_panel(panel)
    draw_outlined_text(
        222,
        78,
        translate("Before playing").upper(),
        PyxelColor.ACCENT,
        font=context.display_font,
    )
    sections = [
        (
            "The goal",
            [
                "Use contracts to learn how traits pass between generations.",
                "Yellow smooth peas are requested first.",
            ],
        ),
        (
            "How to play",
            [
                "Pick two parent plants, cross them, then inspect offspring.",
                "Each cross shows the expected genetic combinations.",
            ],
        ),
        (
            "Basic controls",
            [
                "Mouse: click buttons and plant cards.",
                "Harvest grown plants.",
                "Use 1/2 to reselect starting parents.",
            ],
        ),
    ]
    y = 108
    for title, lines in sections:
        draw_text(
            126,
            y,
            translate(title).upper(),
            PyxelColor.UI_DARK,
            context.display_font,
        )
        y += 14
        for line in lines:
            draw_text(
                138,
                y,
                translate(line),
                PyxelColor.UI_DARK,
                context.display_font,
            )
            y += 14
        y += 4
    draw_button(ok_button, translate("OK"))


def draw_parent_picker(
    context: DrawContext,
    data: ParentPickerData,
    *,
    plant_preview: PlantPreview,
    visible_genotype: Callable[[Plant], str],
    trait: Callable[[str], str],
) -> None:
    """Draw the parent picker overlay."""
    translate = context.translate
    draw_modal_scrim(0.68)
    panel = PARENT_PICKER_PANEL
    draw_panel(panel)
    title = "Select Parent A" if data.target == "a" else "Select Parent B"
    draw_outlined_text(
        92,
        66,
        translate(title).upper(),
        PyxelColor.ACCENT,
        font=context.display_font,
    )
    draw_text(92, 88, translate("Garden plants"), PyxelColor.UI_DARK)
    renderers = _ParentPickerRenderers(
        plant_preview,
        visible_genotype,
        trait,
    )
    for index in range(data.capacity):
        _draw_parent_picker_slot(context, data, index, renderers)
    _draw_parent_picker_details(context, data, renderers)
    draw_button(data.close_button, translate("BACK"))


def parent_picker_slot_rect(index: int) -> Rect:
    """Return one parent picker slot rectangle."""
    col = index % 4
    row = index // 4
    return Rect(88 + col * 90, 106 + row * 42, 82, 36)


def _draw_parent_picker_slot(
    context: DrawContext,
    data: ParentPickerData,
    index: int,
    renderers: _ParentPickerRenderers,
) -> None:
    rect = parent_picker_slot_rect(index)
    plant = data.slots[index]
    selected = index in {
        data.selected_parent_a,
        data.selected_parent_b,
    }
    fill = PyxelColor.ACCENT if selected else PyxelColor.PARCHMENT
    pyxel.rect(rect.x, rect.y, rect.width, rect.height, fill)
    pyxel.rectb(rect.x, rect.y, rect.width, rect.height, PyxelColor.FRAME)
    if plant is None:
        draw_text(
            rect.x + 10,
            rect.y + 26,
            context.translate("Empty slot"),
            PyxelColor.DEEP_GLASS_NAVY,
        )
        return
    renderers.plant_preview(rect.x + 24, rect.y + 47, plant, False)
    draw_text(
        rect.x + 48,
        rect.y + 8,
        fit_text(
            renderers.visible_genotype(plant),
            rect.width - 52,
        ),
        PyxelColor.UI_DARK,
    )
    draw_text(
        rect.x + 48,
        rect.y + 22,
        context.translate(plant.species),
        PyxelColor.UI_DARK,
    )


def _draw_parent_picker_details(
    context: DrawContext,
    data: ParentPickerData,
    renderers: _ParentPickerRenderers,
) -> None:
    plant = _parent_picker_detail_plant(data)
    draw_panel(PARENT_PICKER_DETAIL_PANEL)
    x = PARENT_PICKER_DETAIL_PANEL.x + 8
    width = PARENT_PICKER_DETAIL_PANEL.width - 16
    draw_text(
        x,
        PARENT_PICKER_DETAIL_PANEL.y + 8,
        context.translate("Phenotype").upper(),
        PyxelColor.UI_DARK,
    )
    if plant is None:
        draw_text(
            x,
            PARENT_PICKER_DETAIL_PANEL.y + 28,
            context.translate("Select a plant"),
            PyxelColor.TEXT_MUTED,
        )
        return

    draw_text(
        x,
        PARENT_PICKER_DETAIL_PANEL.y + 22,
        fit_text(context.translate(plant.species), width),
        PyxelColor.ACCENT,
    )
    draw_text(
        x,
        PARENT_PICKER_DETAIL_PANEL.y + 34,
        fit_text(renderers.visible_genotype(plant), width),
        PyxelColor.UI_DARK,
    )
    y = PARENT_PICKER_DETAIL_PANEL.y + 50
    for name, value in plant.phenotype.traits.items():
        draw_text(
            x,
            y,
            fit_text(localized_trait_name(name, context.translate), width),
            PyxelColor.UI_DARK,
        )
        draw_text(
            x + 6,
            y + 9,
            fit_text(renderers.trait(value), width - 6),
            PyxelColor.LEAF_SHADOW,
        )
        y += 22


def _parent_picker_detail_plant(data: ParentPickerData) -> Plant | None:
    for index in range(data.capacity):
        if parent_picker_slot_rect(index).contains(
            pyxel.mouse_x,
            pyxel.mouse_y,
        ):
            return data.slots[index]
    selected_index = (
        data.selected_parent_a
        if data.target == "a"
        else data.selected_parent_b
    )
    if selected_index is None or selected_index >= len(data.slots):
        return None
    return data.slots[selected_index]
