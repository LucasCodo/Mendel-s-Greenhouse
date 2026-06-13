"""Parent cards and cross action for the main game scene."""

from collections.abc import Callable
from dataclasses import dataclass

import pyxel

from mendels_greenhouse.core.genetics import Plant
from mendels_greenhouse.ui.components import Rect, draw_button, draw_panel
from mendels_greenhouse.ui.fonts import (
    draw_outlined_text,
    draw_text,
    fit_text,
    text_width,
)
from mendels_greenhouse.ui.game_components.shared import DrawContext
from mendels_greenhouse.ui.palette import PyxelColor

PlantPreview = Callable[[int, int, Plant, bool], None]

PARENT_CROSS_PANEL = Rect(188, 60, 362, 114)
PARENT_A_CARD = Rect(198, 60, 128, 86)
PARENT_B_CARD = Rect(412, 60, 128, 86)
CROSS_BUTTON = Rect(316, 126, 106, 22)


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
    """Draw the parent cards and cross button in a single unified panel."""
    panel_rect = PARENT_CROSS_PANEL
    draw_panel(panel_rect)

    left = panel_rect.x
    right = panel_rect.x + panel_rect.width
    top_y = panel_rect.y

    # 1. Parental A section (Left Side)
    title_a = context.translate("PARENT A")
    tx_a = (left + 78) - text_width(title_a) // 2
    draw_outlined_text(
        tx_a,
        top_y + 6,
        title_a,
        PyxelColor.ACCENT,
        font=context.display_font,
    )

    if data.parent_a is not None:
        plant_preview(left + 44, top_y + 66, data.parent_a, True)

        # Genotype rounded textbox
        pyxel.rect(left + 84, top_y + 20, 54, 15, PyxelColor.FIELD)
        pyxel.rectb(left + 84, top_y + 20, 54, 15, PyxelColor.FRAME)
        draw_text(
            left + 92,
            top_y + 25,
            visible_genotype(data.parent_a),
            PyxelColor.UI_DARK,
        )

        # Phenotype stacked labels
        t1 = fit_text(
            trait(data.parent_a.phenotype.primary_trait_value),
            54,
        )
        draw_text(left + 84, top_y + 40, t1, PyxelColor.UI_DARK)
        t_keys = list(data.parent_a.phenotype.traits.values())
        if len(t_keys) > 1:
            t2 = fit_text(trait(t_keys[1]), 54)
            draw_text(left + 84, top_y + 50, t2, PyxelColor.UI_DARK)
    else:
        draw_text(
            left + 44,
            top_y + 28,
            context.translate("Empty slot"),
            PyxelColor.UI_DARK,
        )

    # 2. Cross "X" Symbol (Center)
    cx, cy = left + panel_rect.width // 2, top_y + 40
    # Draw outline shadow for contrast
    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
        (-1, -1),
        (1, -1),
        (-1, 1),
        (1, 1),
    ]
    for dx, dy in directions:
        pyxel.line(
            cx - 4 + dx,
            cy - 4 + dy,
            cx + 4 + dx,
            cy + 4 + dy,
            PyxelColor.UI_DARK,
        )
        pyxel.line(
            cx - 4 + dx,
            cy + 4 + dy,
            cx + 4 + dx,
            cy - 4 + dy,
            PyxelColor.UI_DARK,
        )
    # Draw red cross body
    pyxel.line(cx - 4, cy - 4, cx + 4, cy + 4, PyxelColor.TOMATO_RED)
    pyxel.line(cx - 4, cy + 4, cx + 4, cy - 4, PyxelColor.TOMATO_RED)

    # 3. Parental B section (Right Side)
    title_b = context.translate("PARENT B")
    tx_b = (right - 78) - text_width(title_b) // 2
    draw_outlined_text(
        tx_b,
        top_y + 6,
        title_b,
        PyxelColor.ACCENT,
        font=context.display_font,
    )

    if data.parent_b is not None:
        plant_preview(right - 44, top_y + 66, data.parent_b, True)

        # Genotype rounded textbox
        pyxel.rect(right - 138, top_y + 20, 54, 15, PyxelColor.FIELD)
        pyxel.rectb(right - 138, top_y + 20, 54, 15, PyxelColor.FRAME)
        draw_text(
            right - 130,
            top_y + 25,
            visible_genotype(data.parent_b),
            PyxelColor.UI_DARK,
        )

        # Phenotype stacked labels
        tb1 = fit_text(
            trait(data.parent_b.phenotype.primary_trait_value),
            54,
        )
        draw_text(right - 138, top_y + 40, tb1, PyxelColor.UI_DARK)
        tb_keys = list(data.parent_b.phenotype.traits.values())
        if len(tb_keys) > 1:
            tb2 = fit_text(trait(tb_keys[1]), 54)
            draw_text(right - 138, top_y + 50, tb2, PyxelColor.UI_DARK)
    else:
        draw_text(
            right - 132,
            top_y + 28,
            context.translate("Empty slot"),
            PyxelColor.UI_DARK,
        )

    # 4. CROSS button ("CRUZAR")
    draw_button(
        data.cross_button,
        context.translate("CROSS PLANTS"),
        enabled=data.can_crossbreed and not data.has_current_batch,
        pressed=data.cross_pressed,
    )

    # 5. Center Bottom instructions note
    note = context.translate("Select parents, then cross plants.")
    nx = panel_rect.x + (panel_rect.width - text_width(note)) // 2
    draw_text(nx, top_y + 98, note, PyxelColor.UI_DARK)
