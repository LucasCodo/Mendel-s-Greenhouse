"""Germination Bed and action bar for the main game scene."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import pyxel

from mendels_greenhouse.core.genetics import Plant
from mendels_greenhouse.ui.components import (
    Rect,
    draw_button,
    draw_rounded_panel,
    draw_rounded_rect,
)
from mendels_greenhouse.ui.fonts import draw_text, text_width
from mendels_greenhouse.ui.game_components.germination_bed import BedLayout
from mendels_greenhouse.ui.game_components.shared import DrawContext
from mendels_greenhouse.ui.palette import PyxelColor


@dataclass(frozen=True)
class GerminationBedPanelData:
    """Display data for the Germination Bed."""

    rect: Rect
    layout: BedLayout
    current_batch: Sequence[Plant | None]
    visible_count: int
    selected_index: int | None
    status_message: str
    reveal_frames: dict[int, int]
    frame_count: int
    seed_stage_frames: int
    seedling_stage_frames: int
    harvest_button: Rect
    can_harvest: bool
    contract_progress_count: int
    contract_remaining_count: int


def draw_germination_bed_panel(
    context: DrawContext,
    data: GerminationBedPanelData,
    *,
    status_text: Callable[[str], str],  # noqa: ARG001
    matches_contract: Callable[[Plant], bool],
) -> None:
    """Draw the Germination Bed and its action bar."""
    _draw_germination_bed(
        context,
        data,
        matches_contract=matches_contract,
    )
    _draw_bed_action_bar(context, data)


def _draw_germination_bed(
    context: DrawContext,
    data: GerminationBedPanelData,
    *,
    matches_contract: Callable[[Plant], bool],
) -> None:
    translate = context.translate
    rect = data.rect

    # Unified frame for the germination bed
    draw_rounded_panel(
        rect,
        PyxelColor.DARK_WOOD,
        PyxelColor.FRAME,
        PyxelColor.UI_DARK,
    )

    # Header bar
    pyxel.rect(rect.x + 2, rect.y + 2, rect.width - 4, 14, PyxelColor.UI_DARK)

    # Header title with count
    count_suffix = (
        f" ({data.visible_count}/{len(data.current_batch)})"
        if data.current_batch
        else f" (0/{data.layout.cell_count})"
    )
    msg = translate("Descendants").upper() + count_suffix
    text_x = rect.x + (rect.width - text_width(msg)) // 2
    draw_text(text_x, rect.y + 6, msg, PyxelColor.ACCENT)

    layout = data.layout
    for index in range(layout.cell_count):
        _draw_germination_cell(
            data,
            index,
            matches_contract=matches_contract,
        )


def _draw_germination_cell(
    data: GerminationBedPanelData,
    index: int,
    *,
    matches_contract: Callable[[Plant], bool],
) -> None:
    rect = _cell_rect(index, data.layout)
    visible = index < data.visible_count
    has_specimen = index < len(data.current_batch)
    plant = data.current_batch[index] if visible and has_specimen else None
    selected = index == data.selected_index
    matches = plant is not None and matches_contract(plant)

    fill = PyxelColor.SOIL_DARK
    if plant is None and visible:
        fill = PyxelColor.WARM_FLOOR
    border = PyxelColor.ACCENT if selected else PyxelColor.DARK_WOOD
    if matches:
        border = PyxelColor.PROGRESS
    draw_rounded_rect(rect, fill, border)

    if not visible:
        pyxel.circ(
            rect.x + rect.width // 2,
            rect.y + rect.height // 2,
            2,
            PyxelColor.WOOD_MIDTONE,
        )
        return
    if plant is None:
        draw_text(
            rect.x + rect.width // 2 - 2,
            rect.y + rect.height // 2 - 3,
            "-",
            PyxelColor.TEXT_MUTED,
        )
        return

    age = data.frame_count - data.reveal_frames.get(index, data.frame_count)
    center_x = rect.x + rect.width // 2
    center_y = rect.y + rect.height // 2

    _draw_growing_specimen(
        center_x=center_x,
        center_y=center_y,
        age=age,
        data=data,
        plant=plant,
        index=index,
        rect=rect,
        matches=matches,
    )


def _draw_growing_specimen(  # noqa: PLR0913
    center_x: int,
    center_y: int,
    age: int,
    data: GerminationBedPanelData,
    plant: Plant,
    index: int,
    rect: Rect,
    *,
    matches: bool,
) -> None:
    # Gentle desynchronized sway for fully grown plants
    sway = 0
    if age >= data.seedling_stage_frames:
        phase = ((data.frame_count + index * 8) // 12) % 4
        phase_sway_right = 1
        phase_sway_left = 3
        if phase == phase_sway_right:
            sway = 1
        elif phase == phase_sway_left:
            sway = -1

    seed_stage = data.seed_stage_frames
    seedling_stage = data.seedling_stage_frames
    sprout_stage = seed_stage // 2
    mid_seedling = seed_stage + (seedling_stage - seed_stage) // 2

    if age < sprout_stage:
        # Stage 0: Gold Seed nestled in the dirt
        pyxel.circ(center_x, center_y + 3, 2, PyxelColor.SEED_GOLD)
        pyxel.circb(center_x, center_y + 3, 2, PyxelColor.SPRITE_OUTLINE)
    elif age < seed_stage:
        # Stage 1: Sprout breaking through
        pyxel.circ(center_x, center_y + 4, 2, PyxelColor.SEED_GOLD)
        pyxel.circb(center_x, center_y + 4, 2, PyxelColor.SPRITE_OUTLINE)
        # Sprout grows from length 1 to 3
        progress = (age - sprout_stage) / (seed_stage - sprout_stage)
        sprout_h = int(1 + progress * 2)
        pyxel.line(
            center_x,
            center_y + 2,
            center_x,
            center_y + 2 - sprout_h,
            PyxelColor.LEAF_GREEN,
        )
    elif age < mid_seedling:
        # Stage 2: Small seedling with baby leaves
        pyxel.line(
            center_x,
            center_y + 4,
            center_x,
            center_y - 1,
            PyxelColor.LEAF_GREEN,
        )
        progress = (age - seed_stage) / (mid_seedling - seed_stage)
        leaf_spread = int(1 + progress * 2)
        pyxel.pset(
            center_x - leaf_spread,
            center_y + 1,
            PyxelColor.LEAF_HIGHLIGHT,
        )
        pyxel.pset(
            center_x + leaf_spread,
            center_y,
            PyxelColor.LEAF_HIGHLIGHT,
        )
    elif age < seedling_stage:
        # Stage 3: Medium seedling growing to full height
        pyxel.line(
            center_x,
            center_y + 5,
            center_x,
            center_y - 2,
            PyxelColor.LEAF_GREEN,
        )
        pyxel.line(
            center_x,
            center_y,
            center_x - 3,
            center_y - 2,
            PyxelColor.LEAF_HIGHLIGHT,
        )
        pyxel.line(
            center_x,
            center_y - 1,
            center_x + 3,
            center_y - 3,
            PyxelColor.LEAF_HIGHLIGHT,
        )
    else:
        # Stage 4: Fully grown adult plant (with gentle wind sway)
        _draw_tiny_plant(center_x + sway, center_y + 5, plant)
    if matches:
        draw_text(
            rect.x + rect.width - 7,
            rect.y + 2,
            "+",
            PyxelColor.PROGRESS,
        )


def _draw_tiny_plant(x: int, y: int, plant: Plant) -> None:
    phenotype = plant.phenotype
    colorful_traits = {"yellow", "red", "purple", "violet"}
    seed_color = (
        PyxelColor.PEA_YELLOW
        if phenotype.primary_trait_value in colorful_traits
        else PyxelColor.PEA_GREEN
    )
    pyxel.line(x - 5, y - 3, x + 5, y - 8, PyxelColor.POD_BASE)
    pyxel.line(x - 5, y - 2, x + 5, y - 7, PyxelColor.POD_HIGHLIGHT)
    for offset in (-3, 0, 3):
        pyxel.pset(x + offset, y - 5, seed_color)


def _draw_bed_action_bar(
    context: DrawContext,
    data: GerminationBedPanelData,
) -> None:
    # Draw Harvest button centered at the bottom of the bed panel
    draw_button(
        data.harvest_button,
        context.translate("HARVEST"),
        enabled=data.can_harvest,
    )


def _cell_rect(index: int, layout: BedLayout) -> Rect:
    col = index % layout.columns
    row = index // layout.columns
    return Rect(
        layout.x + col * (layout.cell_width + layout.gap),
        layout.y + row * (layout.cell_height + layout.gap),
        layout.cell_width,
        layout.cell_height,
    )
