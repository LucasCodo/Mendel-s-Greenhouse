"""Runtime overlay rendering."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import pyxel

from mendels_greenhouse.core.genetics import Plant
from mendels_greenhouse.ui.components import Rect, draw_button, draw_panel
from mendels_greenhouse.ui.fonts import draw_outlined_text
from mendels_greenhouse.ui.game_components.shared import (
    DrawContext,
    draw_modal_scrim,
)
from mendels_greenhouse.ui.palette import PyxelColor

PlantPreview = Callable[[int, int, Plant, bool], None]


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


@dataclass(frozen=True)
class TooltipData:
    """Display data for the hovered plant tooltip."""

    lines: list[str]
    mouse_x: int
    mouse_y: int
    screen_width: int
    screen_height: int


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
                "Pick two parent plants, cross them, then inspect offspring.",
                "Harvest grown plants.",
                "Use 1/2 to reselect starting parents.",
            ],
        ),
    ]
    y = 112
    for title, lines in sections:
        pyxel.text(126, y, translate(title).upper(), PyxelColor.UI_DARK)
        y += 13
        for line in lines:
            pyxel.text(138, y, translate(line), PyxelColor.UI_DARK)
            y += 12
        y += 7
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
    panel = Rect(88, 74, 496, 250)
    draw_panel(panel)
    title = "Select Parent A" if data.target == "a" else "Select Parent B"
    draw_outlined_text(
        116,
        92,
        translate(title).upper(),
        PyxelColor.ACCENT,
        font=context.display_font,
    )
    pyxel.text(118, 112, translate("Garden plants"), PyxelColor.UI_DARK)
    renderers = _ParentPickerRenderers(
        plant_preview,
        visible_genotype,
        trait,
    )
    for index in range(data.capacity):
        _draw_parent_picker_slot(context, data, index, renderers)
    draw_button(data.close_button, translate("BACK"))


def parent_picker_slot_rect(index: int) -> Rect:
    """Return one parent picker slot rectangle."""
    col = index % 5
    row = index // 5
    return Rect(112 + col * 90, 130 + row * 42, 82, 36)


def draw_plant_tooltip(data: TooltipData) -> None:
    """Draw a plant hover tooltip."""
    width = max(len(line) for line in data.lines) * 4 + 16
    height = len(data.lines) * 10 + 12
    x = min(max(data.mouse_x + 10, 8), data.screen_width - width - 8)
    y = min(
        max(data.mouse_y - height - 8, 70),
        data.screen_height - height - 8,
    )
    panel = Rect(x, y, width, height)
    pyxel.rect(
        panel.x + 2,
        panel.y + 2,
        panel.width,
        panel.height,
        PyxelColor.UI_DARK,
    )
    draw_panel(panel)
    for index, line in enumerate(data.lines):
        pyxel.text(
            panel.x + 8,
            panel.y + 8 + index * 10,
            line,
            PyxelColor.UI_DARK,
        )


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
        pyxel.text(
            rect.x + 10,
            rect.y + 26,
            context.translate("Empty slot"),
            PyxelColor.DEEP_GLASS_NAVY,
        )
        return
    renderers.plant_preview(rect.x + 24, rect.y + 47, plant, False)
    pyxel.text(
        rect.x + 48,
        rect.y + 8,
        renderers.visible_genotype(plant),
        PyxelColor.UI_DARK,
    )
    pyxel.text(
        rect.x + 48,
        rect.y + 20,
        renderers.trait(plant.phenotype.primary_trait_value)[:12],
        PyxelColor.UI_DARK,
    )
    pyxel.text(
        rect.x + 48,
        rect.y + 31,
        renderers.trait(plant.phenotype.secondary_trait_value)[:12],
        PyxelColor.UI_DARK,
    )
