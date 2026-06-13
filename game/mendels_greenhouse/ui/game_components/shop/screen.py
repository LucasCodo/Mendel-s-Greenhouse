"""Shop screen rendering."""

from dataclasses import dataclass

import pyxel

from mendels_greenhouse.ui.components import Rect, draw_button, draw_panel
from mendels_greenhouse.ui.fonts import draw_text
from mendels_greenhouse.ui.game_components.shared import (
    DrawContext,
    draw_scene_shell,
)
from mendels_greenhouse.ui.palette import PyxelColor


@dataclass(frozen=True)
class ShopCardData:
    """Display data for one shop card."""

    item: str
    rect: Rect
    title: str
    cost: str
    status: str


@dataclass(frozen=True)
class ShopScreenData:
    """Display data for the shop screen."""

    credits: int
    selected_item: str
    cards: tuple[ShopCardData, ...]
    details: list[str]
    buy_enabled: bool


def draw_shop_screen(context: DrawContext, data: ShopScreenData) -> None:
    """Draw the shop screen."""
    translate = context.translate
    draw_scene_shell(context, "Shop", "Spend credits on progression")
    draw_text(
        470,
        86,
        f"{translate('Credits')}: {data.credits}",
        PyxelColor.PARCHMENT_LIGHT,
    )
    for card in data.cards:
        _draw_shop_card(
            context,
            card,
            selected=data.selected_item == card.item,
        )

    details_panel = Rect(70, 198, 456, 100)
    draw_panel(details_panel)
    for index, line in enumerate(data.details):
        draw_text(108, 216 + index * 14, translate(line), PyxelColor.UI_DARK)
    draw_button(
        Rect(392, 284, 96, 24),
        translate("BUY"),
        enabled=data.buy_enabled,
    )


def _draw_shop_card(
    context: DrawContext,
    card: ShopCardData,
    *,
    selected: bool,
) -> None:
    translate = context.translate
    rect = card.rect
    fill = PyxelColor.ACCENT if selected else PyxelColor.PARCHMENT
    pyxel.rect(rect.x, rect.y, rect.width, rect.height, fill)
    pyxel.rectb(rect.x, rect.y, rect.width, rect.height, PyxelColor.FRAME)
    draw_text(
        rect.x + 8,
        rect.y + 9,
        translate(card.title),
        PyxelColor.UI_DARK,
    )
    draw_text(rect.x + 8, rect.y + 23, card.cost, PyxelColor.UI_DARK)
    draw_text(
        rect.x + 92,
        rect.y + 23,
        translate(card.status),
        PyxelColor.UI_DARK,
    )
