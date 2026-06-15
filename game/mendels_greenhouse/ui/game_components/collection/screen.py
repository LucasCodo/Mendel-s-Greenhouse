"""Collection album screen rendering."""

from dataclasses import dataclass

import pyxel

from mendels_greenhouse.ui.components import (
    Rect,
    draw_button,
    draw_panel,
    draw_rounded_panel,
)
from mendels_greenhouse.ui.fonts import draw_text, fit_text, text_width
from mendels_greenhouse.ui.game_components.shared import (
    DrawContext,
    draw_scene_shell,
)
from mendels_greenhouse.ui.palette import PyxelColor

ALBUM_GRID_RECT = Rect(148, 108, 392, 218)
ALBUM_COLUMNS = 4
ALBUM_VISIBLE_ROWS = 3
ALBUM_CARD_WIDTH = 82
ALBUM_CARD_HEIGHT = 48
ALBUM_CARD_GAP_X = 6
ALBUM_CARD_GAP_Y = 8
ALBUM_CARDS_X = 158
ALBUM_CARDS_Y = 142
ALBUM_SCROLLBAR = Rect(516, 140, 10, 160)
ALBUM_DETAIL_RECT = Rect(24, 204, 104, 96)


@dataclass(frozen=True)
class CollectionAlbumEntry:
    """One discovered sticker or hidden album slot."""

    title: str
    subtitle: str
    discovered: bool


@dataclass(frozen=True)
class CollectionScreenData:
    """Display data for the collection album."""

    total_entries: int
    total_slots: int
    tabs: tuple[str, ...]
    active_tab: str
    entries: tuple[CollectionAlbumEntry, ...]
    discovered_count: int
    scroll_row: int
    selected_index: int


def album_card_rect(visible_index: int) -> Rect:
    """Return one visible album card rectangle."""
    column = visible_index % ALBUM_COLUMNS
    row = visible_index // ALBUM_COLUMNS
    return Rect(
        ALBUM_CARDS_X + column * (ALBUM_CARD_WIDTH + ALBUM_CARD_GAP_X),
        ALBUM_CARDS_Y + row * (ALBUM_CARD_HEIGHT + ALBUM_CARD_GAP_Y),
        ALBUM_CARD_WIDTH,
        ALBUM_CARD_HEIGHT,
    )


def album_max_scroll_row(entry_count: int) -> int:
    """Return the last valid top row for the collection album."""
    total_rows = (entry_count + ALBUM_COLUMNS - 1) // ALBUM_COLUMNS
    return max(total_rows - ALBUM_VISIBLE_ROWS, 0)


def album_scrollbar_thumb(entry_count: int, scroll_row: int) -> Rect:
    """Return scrollbar thumb geometry for the current album position."""
    total_rows = max(
        (entry_count + ALBUM_COLUMNS - 1) // ALBUM_COLUMNS,
        1,
    )
    max_scroll = album_max_scroll_row(entry_count)
    thumb_height = min(
        max(
            ALBUM_SCROLLBAR.height * ALBUM_VISIBLE_ROWS // total_rows,
            18,
        ),
        ALBUM_SCROLLBAR.height,
    )
    travel = ALBUM_SCROLLBAR.height - thumb_height
    thumb_y = ALBUM_SCROLLBAR.y
    if max_scroll:
        thumb_y += travel * min(scroll_row, max_scroll) // max_scroll
    return Rect(
        ALBUM_SCROLLBAR.x + 1,
        thumb_y,
        ALBUM_SCROLLBAR.width - 2,
        thumb_height,
    )


def draw_collection_screen(
    context: DrawContext,
    data: CollectionScreenData,
) -> None:
    """Draw the collection as a scrollable sticker album."""
    translate = context.translate
    draw_scene_shell(context, "Collection", "Discovered genetic records")
    total_label = translate(
        "Discovered: {found}/{total}",
        found=data.total_entries,
        total=data.total_slots,
    )
    draw_text(
        ALBUM_GRID_RECT.x + ALBUM_GRID_RECT.width - text_width(total_label),
        86,
        total_label,
        PyxelColor.PARCHMENT_LIGHT,
    )
    for index, tab in enumerate(data.tabs):
        rect = Rect(24, 108 + index * 30, 104, 22)
        draw_button(
            rect,
            translate(tab).upper(),
            pressed=data.active_tab == tab,
        )

    draw_panel(ALBUM_GRID_RECT)
    _draw_album_header(context, data)
    _draw_album_cards(context, data)
    _draw_scrollbar(data)
    _draw_selected_entry(context, data)


def _draw_album_header(
    context: DrawContext,
    data: CollectionScreenData,
) -> None:
    translate = context.translate
    title = translate(data.active_tab).upper()
    draw_text(160, 120, title, PyxelColor.UI_DARK)
    progress = translate(
        "{found}/{total} found",
        found=data.discovered_count,
        total=len(data.entries),
    )
    draw_text(
        504 - text_width(progress),
        120,
        progress,
        PyxelColor.UI_DARK,
    )
    bar_x = 160
    bar_y = 132
    bar_width = 344
    pyxel.rect(bar_x, bar_y, bar_width, 4, PyxelColor.BAR_EMPTY)
    if data.entries:
        fill = bar_width * data.discovered_count // len(data.entries)
        pyxel.rect(bar_x, bar_y, fill, 4, PyxelColor.PROGRESS)


def _draw_album_cards(
    context: DrawContext,
    data: CollectionScreenData,
) -> None:
    first_index = data.scroll_row * ALBUM_COLUMNS
    visible_count = ALBUM_COLUMNS * ALBUM_VISIBLE_ROWS
    for visible_index, entry in enumerate(
        data.entries[first_index : first_index + visible_count]
    ):
        absolute_index = first_index + visible_index
        _draw_album_card(
            context,
            album_card_rect(visible_index),
            entry,
            number=absolute_index + 1,
            selected=absolute_index == data.selected_index,
        )


def _draw_album_card(
    context: DrawContext,
    rect: Rect,
    entry: CollectionAlbumEntry,
    *,
    number: int,
    selected: bool,
) -> None:
    translate = context.translate
    fill = (
        PyxelColor.PARCHMENT_LIGHT
        if entry.discovered
        else PyxelColor.WOOD_MIDTONE
    )
    border = PyxelColor.ACCENT if selected else PyxelColor.FRAME
    draw_rounded_panel(rect, fill, border, PyxelColor.UI_DARK)
    number_label = f"#{number:03d}"
    draw_text(rect.x + 5, rect.y + 5, number_label, PyxelColor.UI_DARK)

    if entry.discovered:
        title = fit_text(entry.title, rect.width - 10)
        subtitle = fit_text(entry.subtitle, rect.width - 10)
        draw_text(rect.x + 5, rect.y + 19, title, PyxelColor.UI_DARK)
        draw_text(
            rect.x + 5,
            rect.y + 31,
            subtitle,
            PyxelColor.LEAF_SHADOW,
        )
        return

    mystery = "?"
    draw_text(
        rect.x + (rect.width - text_width(mystery)) // 2,
        rect.y + 17,
        mystery,
        PyxelColor.UI_DARK,
    )
    hidden = fit_text(translate("Undiscovered"), rect.width - 10)
    draw_text(
        rect.x + (rect.width - text_width(hidden)) // 2,
        rect.y + 32,
        hidden,
        PyxelColor.UI_DARK,
    )


def _draw_scrollbar(data: CollectionScreenData) -> None:
    pyxel.rect(
        ALBUM_SCROLLBAR.x,
        ALBUM_SCROLLBAR.y,
        ALBUM_SCROLLBAR.width,
        ALBUM_SCROLLBAR.height,
        PyxelColor.UI_DARK,
    )
    pyxel.rect(
        ALBUM_SCROLLBAR.x + 2,
        ALBUM_SCROLLBAR.y + 2,
        ALBUM_SCROLLBAR.width - 4,
        ALBUM_SCROLLBAR.height - 4,
        PyxelColor.BAR_EMPTY,
    )
    thumb = album_scrollbar_thumb(len(data.entries), data.scroll_row)
    pyxel.rect(
        thumb.x,
        thumb.y,
        thumb.width,
        thumb.height,
        PyxelColor.ACTION,
    )
    pyxel.line(
        thumb.x + 1,
        thumb.y + 1,
        thumb.x + thumb.width - 2,
        thumb.y + 1,
        PyxelColor.PARCHMENT_LIGHT,
    )


def _draw_selected_entry(
    context: DrawContext,
    data: CollectionScreenData,
) -> None:
    draw_panel(ALBUM_DETAIL_RECT)
    translate = context.translate
    draw_text(
        ALBUM_DETAIL_RECT.x + 8,
        ALBUM_DETAIL_RECT.y + 10,
        translate("Selected"),
        PyxelColor.UI_DARK,
    )
    if not data.entries:
        return
    index = min(max(data.selected_index, 0), len(data.entries) - 1)
    entry = data.entries[index]
    draw_text(
        ALBUM_DETAIL_RECT.x + 8,
        ALBUM_DETAIL_RECT.y + 28,
        f"#{index + 1:03d}",
        PyxelColor.UI_DARK,
    )
    if not entry.discovered:
        draw_text(
            ALBUM_DETAIL_RECT.x + 8,
            ALBUM_DETAIL_RECT.y + 46,
            fit_text(translate("Undiscovered"), ALBUM_DETAIL_RECT.width - 16),
            PyxelColor.UI_DARK,
        )
        return
    draw_text(
        ALBUM_DETAIL_RECT.x + 8,
        ALBUM_DETAIL_RECT.y + 46,
        fit_text(entry.title, ALBUM_DETAIL_RECT.width - 16),
        PyxelColor.UI_DARK,
    )
    draw_text(
        ALBUM_DETAIL_RECT.x + 8,
        ALBUM_DETAIL_RECT.y + 62,
        fit_text(entry.subtitle, ALBUM_DETAIL_RECT.width - 16),
        PyxelColor.LEAF_SHADOW,
    )
