"""Collection screen rendering."""

from dataclasses import dataclass

import pyxel

from mendels_greenhouse.ui.components import Rect, draw_button, draw_panel
from mendels_greenhouse.ui.game_components.shared import (
    DrawContext,
    draw_scene_shell,
)
from mendels_greenhouse.ui.palette import PyxelColor


@dataclass(frozen=True)
class CollectionScreenData:
    """Display data for the collection screen."""

    total_entries: int
    tabs: tuple[str, ...]
    active_tab: str
    entries: list[str]
    details: list[str]


def draw_collection_screen(
    context: DrawContext,
    data: CollectionScreenData,
) -> None:
    """Draw the collection screen."""
    translate = context.translate
    draw_scene_shell(context, "Collection", "Discovered genetic records")
    pyxel.text(
        438,
        86,
        translate("Discovered: {total}", total=data.total_entries),
        PyxelColor.PARCHMENT_LIGHT,
    )
    for index, tab in enumerate(data.tabs):
        rect = Rect(24, 108 + index * 30, 104, 22)
        active = data.active_tab == tab
        draw_button(rect, translate(tab).upper(), pressed=active)

    list_panel = Rect(148, 108, 220, 178)
    detail_panel = Rect(386, 108, 154, 178)
    draw_panel(list_panel)
    draw_panel(detail_panel)
    if not data.entries:
        pyxel.text(
            166,
            132,
            translate("No discoveries yet."),
            PyxelColor.UI_DARK,
        )
    for index, line in enumerate(data.entries[:12]):
        pyxel.text(164, 122 + index * 12, line[:44], PyxelColor.UI_DARK)

    pyxel.text(
        402,
        126,
        translate(data.active_tab).upper(),
        PyxelColor.UI_DARK,
    )
    for index, line in enumerate(data.details):
        pyxel.text(402, 146 + index * 14, line[:32], PyxelColor.UI_DARK)
