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

PARENT_CROSS_PANEL = Rect(188, 60, 362, 132)
PARENT_A_CARD = Rect(198, 60, 146, 94)
PARENT_B_CARD = Rect(394, 60, 146, 94)
CROSS_BUTTON = Rect(316, 154, 106, 22)

GENOTYPE_FIELD_WIDTH = 82
GENOTYPE_TEXT_INSET = 4
PHENOTYPE_LABEL_WIDTH = 70
PHENOTYPE_LINE_HEIGHT = 9


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


def phenotype_labels(
    plant: Plant,
    *,
    trait: Callable[[str], str],
    max_width: int = PHENOTYPE_LABEL_WIDTH,
) -> tuple[str, ...]:
    """Return one fitted phenotype label for each tracked gene."""
    return tuple(
        fit_text(trait(value), max_width)
        for value in plant.phenotype.traits.values()
    )


def genotype_label(
    plant: Plant,
    *,
    visible_genotype: Callable[[Plant], str],
) -> str:
    """Return the complete analyzer-visible genotype text."""
    return visible_genotype(plant)


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
        pyxel.rect(
            left + 84,
            top_y + 20,
            GENOTYPE_FIELD_WIDTH,
            15,
            PyxelColor.FIELD,
        )
        pyxel.rectb(
            left + 84,
            top_y + 20,
            GENOTYPE_FIELD_WIDTH,
            15,
            PyxelColor.FRAME,
        )
        draw_text(
            left + 84 + GENOTYPE_TEXT_INSET,
            top_y + 25,
            genotype_label(
                data.parent_a,
                visible_genotype=visible_genotype,
            ),
            PyxelColor.UI_DARK,
        )

        # Phenotype labels: one visible characteristic per allele pair.
        for index, label in enumerate(
            phenotype_labels(data.parent_a, trait=trait),
        ):
            draw_text(
                left + 84,
                top_y + 40 + index * PHENOTYPE_LINE_HEIGHT,
                label,
                PyxelColor.UI_DARK,
            )
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
        pyxel.rect(
            right - 84 - GENOTYPE_FIELD_WIDTH,
            top_y + 20,
            GENOTYPE_FIELD_WIDTH,
            15,
            PyxelColor.FIELD,
        )
        pyxel.rectb(
            right - 84 - GENOTYPE_FIELD_WIDTH,
            top_y + 20,
            GENOTYPE_FIELD_WIDTH,
            15,
            PyxelColor.FRAME,
        )
        draw_text(
            right - 84 - GENOTYPE_FIELD_WIDTH + GENOTYPE_TEXT_INSET,
            top_y + 25,
            genotype_label(
                data.parent_b,
                visible_genotype=visible_genotype,
            ),
            PyxelColor.UI_DARK,
        )

        # Phenotype labels: one visible characteristic per allele pair.
        for index, label in enumerate(
            phenotype_labels(data.parent_b, trait=trait),
        ):
            draw_text(
                right - 154,
                top_y + 40 + index * PHENOTYPE_LINE_HEIGHT,
                label,
                PyxelColor.UI_DARK,
            )
    else:
        draw_text(
            right - 148,
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
    draw_text(nx, top_y + 119, note, PyxelColor.UI_DARK)
