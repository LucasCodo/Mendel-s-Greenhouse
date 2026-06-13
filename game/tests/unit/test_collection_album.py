"""Tests for official collection album slots and scrolling."""

from itertools import pairwise

from mendels_greenhouse.core.collection import official_collection_keys
from mendels_greenhouse.core.content import collection_total_entries
from mendels_greenhouse.ui.game_components.collection import (
    ALBUM_COLUMNS,
    ALBUM_SCROLLBAR,
    ALBUM_VISIBLE_ROWS,
    album_card_rect,
    album_max_scroll_row,
    album_scrollbar_thumb,
)


def test_official_album_slots_match_collection_total() -> None:
    species = official_collection_keys("Species")
    phenotypes = official_collection_keys("Phenotypes")
    genotypes = official_collection_keys("Genotypes")

    assert len(species) == 5
    assert len(phenotypes) == 124
    assert len(genotypes) == 1089
    assert len(species) + len(phenotypes) + len(genotypes) == (
        collection_total_entries()
    )


def test_album_cards_fill_visible_grid_without_overlap() -> None:
    visible_count = ALBUM_COLUMNS * ALBUM_VISIBLE_ROWS
    rects = [album_card_rect(index) for index in range(visible_count)]

    assert len({(rect.x, rect.y) for rect in rects}) == visible_count
    assert all(
        left.x + left.width <= right.x
        for left, right in pairwise(rects)
        if left.y == right.y
    )


def test_album_scrollbar_tracks_first_and_last_rows() -> None:
    entry_count = len(official_collection_keys("Genotypes"))
    max_scroll = album_max_scroll_row(entry_count)
    first_thumb = album_scrollbar_thumb(entry_count, 0)
    last_thumb = album_scrollbar_thumb(entry_count, max_scroll)

    assert first_thumb.y == ALBUM_SCROLLBAR.y
    assert last_thumb.y + last_thumb.height == (
        ALBUM_SCROLLBAR.y + ALBUM_SCROLLBAR.height
    )


def test_album_scrollbar_stays_inside_track_for_small_categories() -> None:
    for entry_count in (0, 5, 12):
        thumb = album_scrollbar_thumb(entry_count, 0)

        assert thumb.y >= ALBUM_SCROLLBAR.y
        assert thumb.height <= ALBUM_SCROLLBAR.height
        assert thumb.y + thumb.height <= (
            ALBUM_SCROLLBAR.y + ALBUM_SCROLLBAR.height
        )
