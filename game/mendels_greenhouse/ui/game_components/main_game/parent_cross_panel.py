"""Parent cards and cross action for the main game scene."""

from collections.abc import Callable
from dataclasses import dataclass

import pyxel

from mendels_greenhouse.core.genetics import Plant
from mendels_greenhouse.ui.components import Rect, draw_button, draw_panel
from mendels_greenhouse.ui.fonts import draw_outlined_text
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
    """Draw the parent cards and cross button in a single unified panel."""
    # Redraw a single wood-framed panel
    panel_rect = Rect(164, 60, 286, 114)
    draw_panel(panel_rect)

    left = panel_rect.x
    right = panel_rect.x + panel_rect.width
    top_y = panel_rect.y

    # 1. Parental A section (Left Side)
    title_a = context.translate("PARENT A")
    tx_a = (left + 59) - (len(title_a) * 4) // 2
    draw_outlined_text(
        tx_a,
        top_y + 6,
        title_a,
        PyxelColor.ACCENT,
        font=context.display_font,
    )

    if data.parent_a is not None:
        plant_preview(left + 34, top_y + 66, data.parent_a, True)

        # Genotype rounded textbox
        pyxel.rect(left + 66, top_y + 20, 46, 15, PyxelColor.FIELD)
        pyxel.rectb(left + 66, top_y + 20, 46, 15, PyxelColor.FRAME)
        pyxel.text(
            left + 74,
            top_y + 25,
            visible_genotype(data.parent_a),
            PyxelColor.UI_DARK,
        )

        # Phenotype stacked labels
        t1 = trait(data.parent_a.phenotype.primary_trait_value)[:12]
        pyxel.text(left + 66, top_y + 40, t1, PyxelColor.UI_DARK)
        t_keys = list(data.parent_a.phenotype.traits.values())
        if len(t_keys) > 1:
            t2 = trait(t_keys[1])[:12]
            pyxel.text(left + 66, top_y + 50, t2, PyxelColor.UI_DARK)
    else:
        pyxel.text(
            left + 24,
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
    tx_b = (right - 59) - (len(title_b) * 4) // 2
    draw_outlined_text(
        tx_b,
        top_y + 6,
        title_b,
        PyxelColor.ACCENT,
        font=context.display_font,
    )

    if data.parent_b is not None:
        plant_preview(right - 34, top_y + 66, data.parent_b, True)

        # Genotype rounded textbox
        pyxel.rect(right - 112, top_y + 20, 46, 15, PyxelColor.FIELD)
        pyxel.rectb(right - 112, top_y + 20, 46, 15, PyxelColor.FRAME)
        pyxel.text(
            right - 104,
            top_y + 25,
            visible_genotype(data.parent_b),
            PyxelColor.UI_DARK,
        )

        # Phenotype stacked labels
        tb1 = trait(data.parent_b.phenotype.primary_trait_value)[:12]
        pyxel.text(right - 112, top_y + 40, tb1, PyxelColor.UI_DARK)
        tb_keys = list(data.parent_b.phenotype.traits.values())
        if len(tb_keys) > 1:
            tb2 = trait(tb_keys[1])[:12]
            pyxel.text(right - 112, top_y + 50, tb2, PyxelColor.UI_DARK)
    else:
        pyxel.text(
            right - 100,
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
    nx = panel_rect.x + (panel_rect.width - len(note) * 4) // 2
    pyxel.text(nx, top_y + 98, note, PyxelColor.UI_DARK)
