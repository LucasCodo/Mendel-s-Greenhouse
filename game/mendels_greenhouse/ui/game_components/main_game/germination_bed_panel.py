"""Germination Bed and action bar for the main game scene."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import pyxel

from mendels_greenhouse.core.genetics import Plant
from mendels_greenhouse.ui.components import Rect, draw_button
from mendels_greenhouse.ui.game_components.germination_bed import BedLayout
from mendels_greenhouse.ui.game_components.shared import DrawContext
from mendels_greenhouse.ui.palette import PyxelColor


@dataclass(frozen=True)
class GerminationBedPanelData:
    """Display data for the Germination Bed."""

    layout: BedLayout
    current_batch: Sequence[Plant | None]
    visible_count: int
    selected_index: int | None
    status_message: str
    reveal_frames: dict[int, int]
    frame_count: int
    seed_stage_frames: int
    seedling_stage_frames: int
    store_button: Rect
    harvest_button: Rect
    can_store: bool
    can_harvest: bool
    contract_progress_count: int
    contract_remaining_count: int


def draw_germination_bed_panel(
    context: DrawContext,
    data: GerminationBedPanelData,
    *,
    status_text: Callable[[str], str],
    matches_contract: Callable[[Plant], bool],
) -> None:
    """Draw the Germination Bed and its action bar."""
    _draw_germination_bed(
        data,
        status_text=status_text,
        matches_contract=matches_contract,
    )
    _draw_bed_action_bar(context, data)


def _draw_germination_bed(
    data: GerminationBedPanelData,
    *,
    status_text: Callable[[str], str],
    matches_contract: Callable[[Plant], bool],
) -> None:
    layout = data.layout
    frame_x = layout.x - 10
    frame_y = layout.y - 10
    frame_w = layout.width + 20
    frame_h = layout.height + 20
    pyxel.rect(frame_x, frame_y, frame_w, frame_h, PyxelColor.DARK_WOOD)
    pyxel.rectb(frame_x, frame_y, frame_w, frame_h, PyxelColor.FRAME)
    pyxel.rectb(
        frame_x + 2,
        frame_y + 2,
        frame_w - 4,
        frame_h - 4,
        PyxelColor.UI_DARK,
    )
    pyxel.rect(230, 174, 180, 14, PyxelColor.UI_DARK)

    msg = status_text(data.status_message)[:44]
    text_x = 320 - len(msg) * 4 // 2
    pyxel.text(text_x, 179, msg, PyxelColor.ACCENT)

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
    pyxel.rect(rect.x, rect.y, rect.width, rect.height, fill)
    border = PyxelColor.ACCENT if selected else PyxelColor.DARK_WOOD
    if matches:
        border = PyxelColor.PROGRESS
    pyxel.rectb(rect.x, rect.y, rect.width, rect.height, border)

    if not visible:
        pyxel.circ(rect.x + 17, rect.y + 8, 2, PyxelColor.WOOD_MIDTONE)
        return
    if plant is None:
        pyxel.text(rect.x + 12, rect.y + 5, "-", PyxelColor.TEXT_MUTED)
        return

    age = data.frame_count - data.reveal_frames.get(index, data.frame_count)
    center_x = rect.x + rect.width // 2
    center_y = rect.y + rect.height // 2
    if age < data.seed_stage_frames:
        pyxel.circ(center_x, center_y + 2, 3, PyxelColor.SEED_GOLD)
        pyxel.circb(center_x, center_y + 2, 3, PyxelColor.SPRITE_OUTLINE)
    elif age < data.seedling_stage_frames:
        pyxel.line(
            center_x,
            center_y + 4,
            center_x,
            center_y - 2,
            PyxelColor.LEAF_GREEN,
        )
        pyxel.pset(center_x - 2, center_y, PyxelColor.LEAF_HIGHLIGHT)
        pyxel.pset(center_x + 2, center_y - 1, PyxelColor.LEAF_HIGHLIGHT)
    else:
        _draw_tiny_plant(center_x, center_y + 5, plant)
    if matches:
        pyxel.text(
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
    translate = context.translate
    pyxel.rect(140, 306, 240, 42, PyxelColor.DARK_WOOD)
    pyxel.rectb(140, 306, 240, 42, PyxelColor.FRAME)
    pyxel.rectb(142, 308, 236, 38, PyxelColor.UI_DARK)
    progress = translate(
        "Generated: {visible}/{total}",
        visible=data.visible_count,
        total=len(data.current_batch),
    )
    contract_text = (
        f"{translate('Matches')}: {data.contract_progress_count}  "
        f"{translate('Missing')}: {data.contract_remaining_count}"
    )
    pyxel.text(150, 312, progress[:36], PyxelColor.PARCHMENT_LIGHT)
    pyxel.text(150, 324, contract_text[:44], PyxelColor.PARCHMENT_LIGHT)
    draw_button(data.store_button, translate("STORE"), enabled=data.can_store)
    draw_button(
        data.harvest_button,
        translate("HARVEST"),
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
