"""Parent cards and cross action for the main game scene."""

from collections.abc import Callable
from dataclasses import dataclass

import pyxel

from mendels_greenhouse.core.genetics import Plant
from mendels_greenhouse.ui.components import Rect, draw_button, draw_panel
from mendels_greenhouse.ui.fonts import draw_outlined_text, draw_shadow_text
from mendels_greenhouse.ui.game_components.shared import DrawContext
from mendels_greenhouse.ui.palette import PyxelColor

PlantPreview = Callable[[int, int, Plant, bool], None]


@dataclass(frozen=True)
class _ParentCardData:
    """Internal parent card drawing data."""

    rect: Rect
    title: str
    plant: Plant | None


@dataclass(frozen=True)
class _ParentCardRenderers:
    """Callbacks needed to render a parent card."""

    plant_preview: PlantPreview
    visible_genotype: Callable[[Plant], str]
    trait: Callable[[str], str]


@dataclass(frozen=True)
class ParentCrossPanelData:
    """Display data for parent cards and cross action."""

    parent_a_card: Rect
    parent_b_card: Rect
    parent_a: Plant | None
    parent_b: Plant | None
    cross_button: Rect
    can_crossbreed: bool
    has_current_batch: bool
    cross_pressed: bool


def draw_parent_cross_panel(
    context: DrawContext,
    data: ParentCrossPanelData,
    *,
    plant_preview: PlantPreview,
    visible_genotype: Callable[[Plant], str],
    trait: Callable[[str], str],
) -> None:
    """Draw the parent cards and cross button."""
    renderers = _ParentCardRenderers(
        plant_preview,
        visible_genotype,
        trait,
    )
    _draw_parent_card(
        context,
        _ParentCardData(data.parent_a_card, "PARENT A", data.parent_a),
        renderers,
    )
    _draw_parent_card(
        context,
        _ParentCardData(data.parent_b_card, "PARENT B", data.parent_b),
        renderers,
    )
    draw_shadow_text(
        316,
        112,
        "+",
        PyxelColor.ACCENT,
        font=context.display_font,
    )
    draw_button(
        data.cross_button,
        context.translate("CROSS PLANTS"),
        enabled=data.can_crossbreed and not data.has_current_batch,
        pressed=data.cross_pressed,
    )


def _draw_parent_card(
    context: DrawContext,
    data: _ParentCardData,
    renderers: _ParentCardRenderers,
) -> None:
    rect = data.rect
    draw_panel(rect)
    draw_outlined_text(
        rect.x + 32,
        rect.y + 7,
        context.translate(data.title),
        PyxelColor.ACCENT,
        font=context.display_font,
    )
    plant = data.plant
    if plant is None:
        pyxel.text(
            rect.x + 20,
            rect.y + 28,
            context.translate("Empty slot"),
            PyxelColor.UI_DARK,
        )
        return

    renderers.plant_preview(rect.x + 32, rect.y + 64, plant, True)
    pyxel.rect(rect.x + 65, rect.y + 25, 46, 15, PyxelColor.FIELD)
    pyxel.rectb(rect.x + 65, rect.y + 25, 46, 15, PyxelColor.FRAME)
    pyxel.text(
        rect.x + 73,
        rect.y + 30,
        renderers.visible_genotype(plant),
        PyxelColor.UI_DARK,
    )
    pyxel.text(
        rect.x + 65,
        rect.y + 47,
        renderers.trait(plant.phenotype.primary_trait_value)[:14],
        PyxelColor.UI_DARK,
    )
