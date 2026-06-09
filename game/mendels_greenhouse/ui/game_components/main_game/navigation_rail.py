"""Right-side navigation rail for the main game scene."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import pyxel

from mendels_greenhouse.ui.components import Rect
from mendels_greenhouse.ui.game_components.main_game.chrome import (
    draw_runtime_hud_frame,
)
from mendels_greenhouse.ui.palette import PyxelColor

NavItem = tuple[str, str, tuple[int, int]]


@dataclass(frozen=True)
class NavigationRailConfig:
    """Layout constants for the right navigation rail."""

    rail_rect: Rect
    button_x: int
    button_y: int
    button_width: int
    button_height: int
    button_gap: int
    icon_size: int
    icon_scale: float


def nav_button_rect(
    screen: str,
    nav_items: Sequence[NavItem],
    config: NavigationRailConfig,
) -> Rect:
    """Return the clickable rectangle for one navigation item."""
    index = next(
        (
            item_index
            for item_index, (item_screen, _label, _sprite) in enumerate(
                nav_items,
            )
            if item_screen == screen
        ),
        0,
    )
    return Rect(
        config.button_x,
        config.button_y + index * (config.button_height + config.button_gap),
        config.button_width,
        config.button_height,
    )


def draw_navigation_rail(
    config: NavigationRailConfig,
    nav_items: Sequence[NavItem],
    *,
    active_screen: str,
    settings_open: bool,
    translate: Callable[[str], str],
) -> None:
    """Draw the right navigation rail."""
    draw_runtime_hud_frame(
        config.rail_rect.x,
        config.rail_rect.y,
        config.rail_rect.width,
        config.rail_rect.height,
    )
    for item in nav_items:
        screen, _label, _sprite = item
        rect = nav_button_rect(
            screen,
            nav_items,
            config,
        )
        _draw_nav_item(
            rect,
            item,
            active=screen == active_screen
            or (screen == "settings" and settings_open),
            translate=translate,
            config=config,
        )


def _draw_nav_item(
    rect: Rect,
    item: NavItem,
    *,
    active: bool,
    translate: Callable[[str], str],
    config: NavigationRailConfig,
) -> None:
    _screen, label, sprite = item
    hovering = rect.contains(pyxel.mouse_x, pyxel.mouse_y)
    fill = PyxelColor.ACCENT if active else PyxelColor.DARK_WOOD
    if hovering and not active:
        fill = PyxelColor.WOOD_MIDTONE
    pyxel.rect(rect.x, rect.y, rect.width, rect.height, fill)
    pyxel.rectb(rect.x, rect.y, rect.width, rect.height, PyxelColor.FRAME)
    pyxel.rectb(
        rect.x + 1,
        rect.y + 1,
        rect.width - 2,
        rect.height - 2,
        PyxelColor.UI_DARK,
    )
    u, v = sprite
    pyxel.blt(
        rect.x + 4,
        rect.y + 5,
        0,
        u,
        v,
        config.icon_size,
        config.icon_size,
        colkey=0,
        scale=config.icon_scale,
    )
    text = translate(label).upper()[:10]
    text_x = rect.x + 24
    pyxel.text(text_x + 1, rect.y + 15, text, PyxelColor.SPRITE_OUTLINE)
    pyxel.text(
        text_x,
        rect.y + 14,
        text,
        PyxelColor.UI_DARK if active else PyxelColor.PARCHMENT_LIGHT,
    )
