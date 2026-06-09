"""Knowledge screen rendering."""

from dataclasses import dataclass

import pyxel

from mendels_greenhouse.ui.components import Rect, draw_panel
from mendels_greenhouse.ui.game_components.shared import (
    DrawContext,
    TextWrapper,
    draw_scene_shell,
)
from mendels_greenhouse.ui.palette import PyxelColor


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


def draw_knowledge_screen(
    context: DrawContext,
    data: KnowledgeScreenData,
) -> None:
    """Draw the knowledge screen."""
    translate = context.translate
    draw_scene_shell(context, "Knowledge", "Learned genetics concepts")
    pyxel.text(
        438,
        86,
        translate(
            "Learned: {learned}/{total}",
            learned=data.learned_count,
            total=data.total_count,
        ),
        PyxelColor.PARCHMENT_LIGHT,
    )

    node_panel = Rect(24, 108, 214, 190)
    detail_panel = Rect(258, 108, 282, 190)
    draw_panel(node_panel)
    draw_panel(detail_panel)
    _draw_knowledge_nodes(context, data)
    _draw_knowledge_details(context, data, detail_panel)


def _draw_knowledge_nodes(
    context: DrawContext,
    data: KnowledgeScreenData,
) -> None:
    translate = context.translate
    index = 0
    for stage in data.stages:
        stage_unlocked = data.analyzer_level >= stage.required_level
        y = 116 + index * 11
        pyxel.text(38, y, translate(stage.title).upper(), PyxelColor.ACCENT)
        index += 1
        for concept in stage.concepts:
            unlocked = data.analyzer_level >= stage.required_level
            selected = concept == data.selected_concept
            rect = Rect(28, 116 + index * 11, 196, 10)
            fill = PyxelColor.ACCENT if selected else PyxelColor.PARCHMENT
            if not unlocked:
                fill = PyxelColor.TEXT_MUTED
            pyxel.rect(rect.x, rect.y, rect.width, rect.height, fill)
            pyxel.rectb(
                rect.x,
                rect.y,
                rect.width,
                rect.height,
                PyxelColor.FRAME,
            )
            label = translate(concept) if unlocked else translate("Locked")
            pyxel.text(
                rect.x + 6,
                rect.y + 3,
                label[:44],
                PyxelColor.UI_DARK,
            )
            if not stage_unlocked:
                pyxel.text(
                    rect.x + 166,
                    rect.y + 3,
                    f"L{stage.required_level}",
                    PyxelColor.UI_DARK,
                )
            index += 1


def _draw_knowledge_details(
    context: DrawContext,
    data: KnowledgeScreenData,
    panel: Rect,
) -> None:
    translate = context.translate
    concept = data.selected_concept
    required_level = _required_level_for(data.stages, concept)
    pyxel.text(
        panel.x + 18,
        panel.y + 18,
        translate("Selected Concept"),
        PyxelColor.UI_DARK,
    )
    if data.analyzer_level < required_level:
        pyxel.text(
            panel.x + 18,
            panel.y + 42,
            translate("Locked"),
            PyxelColor.UI_DARK,
        )
        pyxel.text(
            panel.x + 18,
            panel.y + 58,
            translate("Analyzer L{level} required.", level=required_level),
            PyxelColor.UI_DARK,
        )
        return

    pyxel.text(
        panel.x + 18,
        panel.y + 42,
        translate(concept).upper(),
        PyxelColor.UI_DARK,
    )
    detail = data.detail_texts.get(concept, "")
    for index, line in enumerate(data.wrap_text(translate(detail), 58)[:5]):
        pyxel.text(
            panel.x + 18,
            panel.y + 64 + index * 13,
            line,
            PyxelColor.UI_DARK,
        )
    pyxel.text(
        panel.x + 18,
        panel.y + 154,
        translate("Unlocked by analyzer level {level}.", level=required_level),
        PyxelColor.UI_DARK,
    )


def _required_level_for(
    stages: tuple[KnowledgeStage, ...],
    concept: str,
) -> int:
    for stage in stages:
        if concept in stage.concepts:
            return stage.required_level
    return 1
