"""Knowledge screen rendering."""

import math
from dataclasses import dataclass

import pyxel

from mendels_greenhouse.ui.components import (
    Rect,
    draw_panel,
    draw_rounded_panel,
)
from mendels_greenhouse.ui.fonts import (
    draw_outlined_text,
    draw_text,
    fit_text,
    text_width,
)
from mendels_greenhouse.ui.game_components.shared import (
    DrawContext,
    TextWrapper,
    draw_scene_shell,
)
from mendels_greenhouse.ui.palette import PyxelColor

KNOWLEDGE_STAGE_Y = 106
KNOWLEDGE_STAGE_HEIGHT = 42
KNOWLEDGE_STAGE_GAP = 6
KNOWLEDGE_STAGE_WIDTH = 126
KNOWLEDGE_STAGE_X = 24
KNOWLEDGE_NODE_PANEL = Rect(24, 158, 220, 176)
KNOWLEDGE_DETAIL_PANEL = Rect(254, 158, 290, 176)
KNOWLEDGE_NODE_X = KNOWLEDGE_NODE_PANEL.x + 12
KNOWLEDGE_NODE_Y = KNOWLEDGE_NODE_PANEL.y + 42
KNOWLEDGE_NODE_WIDTH = KNOWLEDGE_NODE_PANEL.width - 24
KNOWLEDGE_NODE_HEIGHT = 22
KNOWLEDGE_NODE_GAP = 6
PHENOTYPE_LEVEL = 1
GENOTYPE_LEVEL = 2
PROBABILITY_LEVEL = 3
HELIX_FRONT_THRESHOLD = 0.5
HELIX_GLOW_THRESHOLD = 0.55


@dataclass(frozen=True)
class KnowledgeStage:
    """One stage in the learning progression."""

    title: str
    concepts: tuple[str, ...]
    required_level: int


@dataclass(frozen=True)
class KnowledgeScreenData:
    """Display data for the knowledge screen."""

    stages: tuple[KnowledgeStage, ...]
    analyzer_level: int
    selected_concept: str
    detail_texts: dict[str, str]
    learned_count: int
    total_count: int
    wrap_text: TextWrapper


def knowledge_stage_rect(index: int) -> Rect:
    """Return one progression stage rectangle."""
    return Rect(
        KNOWLEDGE_STAGE_X
        + index * (KNOWLEDGE_STAGE_WIDTH + KNOWLEDGE_STAGE_GAP),
        KNOWLEDGE_STAGE_Y,
        KNOWLEDGE_STAGE_WIDTH,
        KNOWLEDGE_STAGE_HEIGHT,
    )


def knowledge_concept_rect(index: int) -> Rect:
    """Return one visible concept rectangle."""
    return Rect(
        KNOWLEDGE_NODE_X,
        KNOWLEDGE_NODE_Y
        + index * (KNOWLEDGE_NODE_HEIGHT + KNOWLEDGE_NODE_GAP),
        KNOWLEDGE_NODE_WIDTH,
        KNOWLEDGE_NODE_HEIGHT,
    )


def selected_knowledge_stage(
    stages: tuple[KnowledgeStage, ...],
    concept: str,
) -> KnowledgeStage:
    """Return the stage containing the selected concept."""
    for stage in stages:
        if concept in stage.concepts:
            return stage
    return stages[0]


def draw_knowledge_screen(
    context: DrawContext,
    data: KnowledgeScreenData,
) -> None:
    """Draw the knowledge screen."""
    draw_scene_shell(context, "Knowledge", "Learned genetics concepts")
    _draw_progress_summary(context, data)
    active_stage = selected_knowledge_stage(
        data.stages,
        data.selected_concept,
    )
    _draw_learning_path(context, data, active_stage)
    _draw_knowledge_nodes(context, data, active_stage)
    _draw_knowledge_details(context, data, active_stage)


def _draw_progress_summary(
    context: DrawContext,
    data: KnowledgeScreenData,
) -> None:
    rect = Rect(394, 74, 150, 26)
    draw_rounded_panel(
        rect,
        PyxelColor.DEEP_GLASS_NAVY,
        PyxelColor.FRAME,
        PyxelColor.BLUE_GLASS,
    )
    label = context.translate(
        "Learned: {learned}/{total}",
        learned=data.learned_count,
        total=data.total_count,
    )
    draw_text(
        rect.x + 9,
        rect.y + 5,
        fit_text(label, rect.width - 18),
        PyxelColor.PARCHMENT_LIGHT,
    )
    bar = Rect(rect.x + 9, rect.y + 17, rect.width - 18, 4)
    pyxel.rect(bar.x, bar.y, bar.width, bar.height, PyxelColor.BAR_EMPTY)
    fill = (
        0
        if data.total_count == 0
        else bar.width * data.learned_count // data.total_count
    )
    pyxel.rect(bar.x, bar.y, fill, bar.height, PyxelColor.PROGRESS)


def _draw_learning_path(
    context: DrawContext,
    data: KnowledgeScreenData,
    active_stage: KnowledgeStage,
) -> None:
    for index, stage in enumerate(data.stages):
        rect = knowledge_stage_rect(index)
        unlocked = data.analyzer_level >= stage.required_level
        active = stage == active_stage
        _draw_stage_card(
            context,
            rect,
            stage,
            unlocked=unlocked,
            active=active,
            final=index == len(data.stages) - 1,
        )


def _draw_stage_card(  # noqa: PLR0913
    context: DrawContext,
    rect: Rect,
    stage: KnowledgeStage,
    *,
    unlocked: bool,
    active: bool,
    final: bool,
) -> None:
    hovering = rect.contains(pyxel.mouse_x, pyxel.mouse_y)
    fill = PyxelColor.PARCHMENT if unlocked else PyxelColor.METAL_DARK
    border = PyxelColor.ACCENT if active else PyxelColor.FRAME
    if hovering and not active:
        border = PyxelColor.CYAN_SCIENCE
    draw_rounded_panel(rect, fill, border, PyxelColor.UI_DARK)
    _draw_stage_emblem(
        rect.x + 10,
        rect.y + 10,
        stage.required_level,
        unlocked,
    )
    title = context.translate(stage.title)
    title_color = (
        PyxelColor.UI_DARK if unlocked else PyxelColor.PARCHMENT_LIGHT
    )
    draw_text(
        rect.x + 35,
        rect.y + 9,
        fit_text(title.upper(), rect.width - 42),
        title_color,
    )
    level = context.translate(
        "Analyzer L{level}",
        level=stage.required_level,
    )
    draw_text(
        rect.x + 35,
        rect.y + 24,
        fit_text(level, rect.width - 42),
        PyxelColor.LEAF_SHADOW if unlocked else PyxelColor.TEXT_MUTED,
    )
    if not final:
        arrow_x = rect.x + rect.width + 1
        arrow_y = rect.y + rect.height // 2
        pyxel.line(
            arrow_x,
            arrow_y,
            arrow_x + KNOWLEDGE_STAGE_GAP - 2,
            arrow_y,
            PyxelColor.ACCENT if unlocked else PyxelColor.TEXT_MUTED,
        )
        pyxel.pset(
            arrow_x + KNOWLEDGE_STAGE_GAP - 3,
            arrow_y - 1,
            PyxelColor.ACCENT if unlocked else PyxelColor.TEXT_MUTED,
        )
        pyxel.pset(
            arrow_x + KNOWLEDGE_STAGE_GAP - 3,
            arrow_y + 1,
            PyxelColor.ACCENT if unlocked else PyxelColor.TEXT_MUTED,
        )


def _draw_knowledge_nodes(
    context: DrawContext,
    data: KnowledgeScreenData,
    stage: KnowledgeStage,
) -> None:
    translate = context.translate
    draw_panel(KNOWLEDGE_NODE_PANEL)
    draw_outlined_text(
        KNOWLEDGE_NODE_PANEL.x + 13,
        KNOWLEDGE_NODE_PANEL.y + 12,
        translate("CONCEPTS"),
        PyxelColor.ACCENT,
        font=context.display_font,
    )
    stage_unlocked = data.analyzer_level >= stage.required_level
    for index, concept in enumerate(stage.concepts):
        rect = knowledge_concept_rect(index)
        selected = concept == data.selected_concept
        hovering = rect.contains(pyxel.mouse_x, pyxel.mouse_y)
        fill = PyxelColor.PARCHMENT_LIGHT
        border = PyxelColor.FRAME
        if selected:
            fill = PyxelColor.SUNLIT_CREAM
            border = PyxelColor.ACCENT
        elif hovering:
            border = PyxelColor.CYAN_SCIENCE
        if not stage_unlocked:
            fill = PyxelColor.METAL_DARK
            border = PyxelColor.UI_DARK
        draw_rounded_panel(rect, fill, border, PyxelColor.WOOD_MIDTONE)

        _draw_node_marker(rect, selected, stage_unlocked)
        label = (
            translate(concept)
            if stage_unlocked
            else translate("Locked concept")
        )
        color = (
            PyxelColor.UI_DARK
            if stage_unlocked
            else PyxelColor.PARCHMENT_LIGHT
        )
        draw_text(
            rect.x + 25,
            rect.y + 7,
            fit_text(label, rect.width - 34),
            color,
        )


def _draw_knowledge_details(
    context: DrawContext,
    data: KnowledgeScreenData,
    stage: KnowledgeStage,
) -> None:
    translate = context.translate
    panel = KNOWLEDGE_DETAIL_PANEL
    draw_panel(panel)
    concept = data.selected_concept
    required_level = stage.required_level
    unlocked = data.analyzer_level >= required_level
    _draw_detail_illustration(
        Rect(panel.x + 16, panel.y + 16, 72, 72),
        required_level,
        unlocked,
    )
    draw_text(
        panel.x + 102,
        panel.y + 18,
        translate("Selected Concept").upper(),
        PyxelColor.LEAF_SHADOW,
    )
    title = translate(concept) if unlocked else translate(stage.title)
    draw_text(
        panel.x + 102,
        panel.y + 37,
        fit_text(title.upper(), panel.width - 118),
        PyxelColor.UI_DARK,
    )
    _draw_detail_status(
        context,
        Rect(panel.x + 102, panel.y + 57, 118, 18),
        required_level,
        unlocked,
    )

    if unlocked:
        detail = data.detail_texts.get(concept, "")
        lines = data.wrap_text(translate(detail), 42)[:4]
        for index, line in enumerate(lines):
            draw_text(
                panel.x + 16,
                panel.y + 100 + index * 13,
                fit_text(line, panel.width - 32),
                PyxelColor.UI_DARK,
            )
        footer = translate(
            "Unlocked by analyzer level {level}.",
            level=required_level,
        )
    else:
        lines = [
            translate("This concept is still locked."),
            translate(
                "Upgrade the analyzer to level {level}.",
                level=required_level,
            ),
        ]
        for index, line in enumerate(lines):
            draw_text(
                panel.x + 16,
                panel.y + 104 + index * 15,
                fit_text(line, panel.width - 32),
                PyxelColor.UI_DARK,
            )
        footer = translate("Progress without revealing future details.")

    draw_text(
        panel.x + 16,
        panel.y + panel.height - 18,
        fit_text(footer, panel.width - 32),
        PyxelColor.TEXT_MUTED,
    )


def _draw_stage_emblem(
    x: int,
    y: int,
    level: int,
    unlocked: bool,
) -> None:
    color = PyxelColor.ACCENT if unlocked else PyxelColor.TEXT_MUTED
    pyxel.circ(x + 7, y + 7, 8, PyxelColor.DEEP_GLASS_NAVY)
    pyxel.circb(x + 7, y + 7, 8, PyxelColor.UI_DARK)
    if unlocked:
        draw_text(x + 5, y + 4, str(level), color)
        return
    pyxel.rect(x + 4, y + 7, 7, 6, color)
    pyxel.circb(x + 7, y + 7, 4, color)


def _draw_node_marker(rect: Rect, selected: bool, unlocked: bool) -> None:
    x = rect.x + 12
    y = rect.y + rect.height // 2
    color = (
        PyxelColor.ACCENT
        if selected
        else PyxelColor.LEAF_GREEN
        if unlocked
        else PyxelColor.TEXT_MUTED
    )
    pyxel.circ(x, y, 4, PyxelColor.DEEP_GLASS_NAVY)
    pyxel.circb(x, y, 4, PyxelColor.UI_DARK)
    if unlocked:
        pyxel.pset(x, y, color)
        pyxel.pset(x + 1, y, color)
    else:
        pyxel.rect(x - 2, y, 5, 4, color)
        pyxel.circb(x, y, 3, color)


def _draw_detail_status(
    context: DrawContext,
    rect: Rect,
    level: int,
    unlocked: bool,
) -> None:
    fill = PyxelColor.LEAF_GREEN if unlocked else PyxelColor.METAL_DARK
    draw_rounded_panel(rect, fill, PyxelColor.UI_DARK, fill)
    label = (
        context.translate("LEARNED")
        if unlocked
        else context.translate("ANALYZER L{level} REQUIRED", level=level)
    )
    label = fit_text(label, rect.width - 8)
    draw_text(
        rect.x + (rect.width - text_width(label)) // 2,
        rect.y + 5,
        label,
        PyxelColor.UI_DARK if unlocked else PyxelColor.PARCHMENT_LIGHT,
    )


def _draw_detail_illustration(
    rect: Rect,
    level: int,
    unlocked: bool,
) -> None:
    draw_rounded_panel(
        rect,
        PyxelColor.DEEP_GLASS_NAVY,
        PyxelColor.FRAME,
        PyxelColor.BLUE_GLASS,
    )
    if not unlocked:
        _draw_large_lock(rect)
    elif level == PHENOTYPE_LEVEL:
        _draw_phenotype_icon(rect)
    elif level == GENOTYPE_LEVEL:
        _draw_genotype_icon(rect)
    elif level == PROBABILITY_LEVEL:
        _draw_probability_icon(rect)
    else:
        _draw_planning_icon(rect)


def _draw_large_lock(rect: Rect) -> None:
    x = rect.x + rect.width // 2
    y = rect.y + rect.height // 2
    pyxel.circb(x, y - 9, 13, PyxelColor.METAL_LIGHT)
    pyxel.rect(x - 15, y - 7, 30, 25, PyxelColor.METAL_DARK)
    pyxel.rectb(x - 15, y - 7, 30, 25, PyxelColor.METAL_LIGHT)
    pyxel.circ(x, y + 3, 3, PyxelColor.ACCENT)
    pyxel.line(x, y + 6, x, y + 11, PyxelColor.ACCENT)


def _draw_phenotype_icon(rect: Rect) -> None:
    x = rect.x + rect.width // 2
    y = rect.y + rect.height // 2
    pyxel.line(x, y + 22, x, y - 8, PyxelColor.LEAF_GREEN)
    pyxel.elli(x - 20, y - 3, 20, 11, PyxelColor.LEAF_HIGHLIGHT)
    pyxel.elli(x, y + 2, 20, 11, PyxelColor.LEAF_GREEN)
    pyxel.circ(x, y - 16, 8, PyxelColor.SEED_GOLD)
    pyxel.circ(x - 8, y - 13, 6, PyxelColor.SUNLIT_CREAM)
    pyxel.circ(x + 8, y - 13, 6, PyxelColor.SUNLIT_CREAM)
    pyxel.rect(x - 12, y + 21, 24, 4, PyxelColor.TERRACOTTA)


def _draw_genotype_icon(rect: Rect) -> None:
    center_x = rect.x + rect.width // 2
    center_y = rect.y + rect.height // 2
    amplitude = min(15, rect.width // 4)
    half_height = rect.height // 2 - 9
    phase = pyxel.frame_count * 0.09

    for vertical_offset in range(-half_height, half_height + 1, 4):
        angle = vertical_offset * 0.2 + phase
        strand_a = math.sin(angle) * amplitude
        strand_b = math.sin(angle + math.pi) * amplitude
        x_a = int(center_x + strand_a)
        x_b = int(center_x + strand_b)
        y = center_y + vertical_offset
        depth = (math.sin(angle) + 1.0) * 0.5

        rung_color = (
            PyxelColor.CYAN_SCIENCE
            if vertical_offset % 8 == 0
            else PyxelColor.GENETIC_PURPLE
        )
        pyxel.line(
            x_a,
            y,
            x_b,
            y,
            PyxelColor.METAL_DARK,
        )
        if vertical_offset % 8 == 0:
            pyxel.line(
                min(x_a, x_b) + 2,
                y,
                max(x_a, x_b) - 2,
                y,
                rung_color,
            )

        strand_a_front = depth >= HELIX_FRONT_THRESHOLD
        front_x = x_a if strand_a_front else x_b
        back_x = x_b if strand_a_front else x_a
        front_color = (
            PyxelColor.CYAN_SCIENCE
            if strand_a_front
            else PyxelColor.GENETIC_PURPLE
        )
        back_color = (
            PyxelColor.GENETIC_PURPLE
            if strand_a_front
            else PyxelColor.CYAN_SCIENCE
        )
        pyxel.circ(back_x, y, 1, back_color)
        pyxel.circ(front_x, y, 2, front_color)
        pyxel.pset(front_x - 1, y - 1, PyxelColor.GLASS_HIGHLIGHT)

    scan_y = rect.y + 5 + (pyxel.frame_count // 2) % max(rect.height - 10, 1)
    pyxel.dither(0.45)
    pyxel.line(
        rect.x + 6,
        scan_y,
        rect.x + rect.width - 7,
        scan_y,
        PyxelColor.CYAN_SCIENCE,
    )
    pyxel.dither(1)

    pulse = (math.sin(pyxel.frame_count * 0.16) + 1.0) * 0.5
    glow_color = (
        PyxelColor.GLASS_HIGHLIGHT
        if pulse > HELIX_GLOW_THRESHOLD
        else PyxelColor.CYAN_SCIENCE
    )
    pyxel.pset(center_x, rect.y + 5, glow_color)
    pyxel.pset(center_x, rect.y + rect.height - 6, glow_color)


def _draw_probability_icon(rect: Rect) -> None:
    grid_x = rect.x + 17
    grid_y = rect.y + 17
    cell = 18
    colors = (
        PyxelColor.LEAF_GREEN,
        PyxelColor.CYAN_SCIENCE,
        PyxelColor.SEED_GOLD,
        PyxelColor.ORCHID_VIOLET,
    )
    for row in range(2):
        for column in range(2):
            color = colors[row * 2 + column]
            pyxel.rect(
                grid_x + column * cell,
                grid_y + row * cell,
                cell - 2,
                cell - 2,
                color,
            )
            pyxel.rectb(
                grid_x + column * cell,
                grid_y + row * cell,
                cell - 2,
                cell - 2,
                PyxelColor.UI_DARK,
            )
    pyxel.line(
        grid_x,
        grid_y + 45,
        grid_x + 34,
        grid_y + 45,
        PyxelColor.GLASS_HIGHLIGHT,
    )


def _draw_planning_icon(rect: Rect) -> None:
    start_x = rect.x + 15
    mid_x = rect.x + rect.width // 2
    end_x = rect.x + rect.width - 15
    center_y = rect.y + rect.height // 2
    pyxel.line(
        start_x,
        center_y - 16,
        mid_x,
        center_y,
        PyxelColor.CYAN_SCIENCE,
    )
    pyxel.line(
        start_x,
        center_y + 16,
        mid_x,
        center_y,
        PyxelColor.CYAN_SCIENCE,
    )
    pyxel.line(
        mid_x,
        center_y,
        end_x,
        center_y,
        PyxelColor.ACCENT,
    )
    for x, y, color in (
        (start_x, center_y - 16, PyxelColor.LEAF_GREEN),
        (start_x, center_y + 16, PyxelColor.ORCHID_VIOLET),
        (mid_x, center_y, PyxelColor.CYAN_SCIENCE),
        (end_x, center_y, PyxelColor.SEED_GOLD),
    ):
        pyxel.circ(x, y, 6, color)
        pyxel.circb(x, y, 6, PyxelColor.UI_DARK)
