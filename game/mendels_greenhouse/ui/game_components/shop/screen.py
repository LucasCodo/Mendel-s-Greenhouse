"""Shop screen rendering."""

from dataclasses import dataclass

import pyxel

from mendels_greenhouse.ui.components import (
    Rect,
    draw_button,
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
    draw_modal_scrim,
    draw_scene_shell,
)
from mendels_greenhouse.ui.palette import PyxelColor

SHOP_CARD_RECTS = (
    Rect(24, 112, 164, 118),
    Rect(202, 112, 164, 118),
    Rect(380, 112, 164, 118),
)
SHOP_DETAILS_PANEL = Rect(24, 240, 520, 94)
SHOP_BUY_BUTTON = Rect(414, 298, 112, 24)
SHOP_CONFIRM_PANEL = Rect(140, 76, 360, 216)
SHOP_CONFIRM_CANCEL_BUTTON = Rect(218, 250, 96, 24)
SHOP_CONFIRM_BUY_BUTTON = Rect(326, 250, 96, 24)


@dataclass(frozen=True)
class ShopCardData:
    """Display data for one shop card."""

    item: str
    rect: Rect
    title: str
    cost: str
    status: str
    artwork: str
    sprite: tuple[int, int] | None = None


@dataclass(frozen=True)
class ShopScreenData:
    """Display data for the shop screen."""

    credits: int
    selected_item: str
    cards: tuple[ShopCardData, ...]
    details: list[str]
    buy_enabled: bool


@dataclass(frozen=True)
class ShopConfirmationData:
    """Display data for the purchase confirmation overlay."""

    title: str
    cost: str
    credits_after: int
    artwork: str
    sprite: tuple[int, int] | None


def draw_shop_screen(context: DrawContext, data: ShopScreenData) -> None:
    """Draw the shop screen."""
    draw_scene_shell(context, "Shop", "Spend credits on progression")
    for card in data.cards:
        _draw_shop_card(
            context,
            card,
            selected=data.selected_item == card.item,
        )

    selected_card = next(
        card for card in data.cards if card.item == data.selected_item
    )
    _draw_details_panel(context, data, selected_card)


def draw_shop_confirmation(
    context: DrawContext,
    data: ShopConfirmationData,
) -> None:
    """Draw the purchase confirmation overlay."""
    translate = context.translate
    draw_modal_scrim(0.78)
    draw_panel(SHOP_CONFIRM_PANEL)
    title = translate("Confirm purchase").upper()
    draw_outlined_text(
        SHOP_CONFIRM_PANEL.x
        + (SHOP_CONFIRM_PANEL.width - text_width(title, context.display_font))
        // 2,
        SHOP_CONFIRM_PANEL.y + 16,
        title,
        PyxelColor.ACCENT,
        font=context.display_font,
    )

    preview = Rect(
        SHOP_CONFIRM_PANEL.x + 24,
        SHOP_CONFIRM_PANEL.y + 50,
        82,
        82,
    )
    draw_rounded_panel(
        preview,
        PyxelColor.DEEP_GLASS_NAVY,
        PyxelColor.FRAME,
        PyxelColor.BLUE_GLASS,
    )
    _draw_card_artwork(data.artwork, preview, data.sprite)

    text_x = SHOP_CONFIRM_PANEL.x + 126
    draw_text(
        text_x,
        SHOP_CONFIRM_PANEL.y + 56,
        fit_text(translate(data.title), 190),
        PyxelColor.UI_DARK,
    )
    draw_text(
        text_x,
        SHOP_CONFIRM_PANEL.y + 78,
        translate("Purchase price"),
        PyxelColor.TEXT_MUTED,
    )
    draw_text(
        text_x,
        SHOP_CONFIRM_PANEL.y + 92,
        data.cost,
        PyxelColor.UI_DARK,
    )
    draw_text(
        text_x,
        SHOP_CONFIRM_PANEL.y + 116,
        translate("Balance after purchase"),
        PyxelColor.TEXT_MUTED,
    )
    draw_text(
        text_x,
        SHOP_CONFIRM_PANEL.y + 130,
        f"{data.credits_after} CR",
        PyxelColor.LEAF_SHADOW,
    )
    draw_text(
        SHOP_CONFIRM_PANEL.x + 24,
        SHOP_CONFIRM_PANEL.y + 166,
        translate("The upgrade will be applied immediately."),
        PyxelColor.UI_DARK,
    )
    draw_button(
        SHOP_CONFIRM_CANCEL_BUTTON,
        translate("CANCEL"),
    )
    draw_button(
        SHOP_CONFIRM_BUY_BUTTON,
        translate("CONFIRM"),
    )


def _draw_shop_card(
    context: DrawContext,
    card: ShopCardData,
    *,
    selected: bool,
) -> None:
    translate = context.translate
    rect = card.rect
    hovering = rect.contains(pyxel.mouse_x, pyxel.mouse_y)
    fill = PyxelColor.PARCHMENT_LIGHT
    border = PyxelColor.ACCENT if selected else PyxelColor.FRAME
    if hovering and not selected:
        fill = PyxelColor.PARCHMENT
        border = PyxelColor.CYAN_SCIENCE
    draw_rounded_panel(rect, fill, border, PyxelColor.WOOD_MIDTONE)

    if selected:
        pyxel.rect(
            rect.x + 8,
            rect.y + 7,
            rect.width - 16,
            3,
            PyxelColor.ACCENT,
        )

    art_rect = Rect(rect.x + 10, rect.y + 18, 68, 70)
    draw_rounded_panel(
        art_rect,
        PyxelColor.DEEP_GLASS_NAVY,
        PyxelColor.FRAME,
        PyxelColor.BLUE_GLASS,
    )
    _draw_card_artwork(card.artwork, art_rect, card.sprite)

    title = fit_text(translate(card.title), rect.width - 92)
    draw_text(rect.x + 88, rect.y + 23, title, PyxelColor.UI_DARK)
    draw_text(
        rect.x + 88,
        rect.y + 43,
        card.cost,
        PyxelColor.LEAF_SHADOW,
    )
    _draw_status_badge(context, rect, card.status)

    if card.artwork == "slot":
        category = translate("CAPACITY")
    elif card.artwork == "analyzer":
        category = translate("RESEARCH")
    else:
        category = translate("SPECIES")
    draw_text(
        rect.x + 12,
        rect.y + 98,
        category,
        PyxelColor.TEXT_MUTED,
    )
    marker = ">" if selected else "+"
    draw_text(
        rect.x + rect.width - 18,
        rect.y + 97,
        marker,
        border,
    )


def _draw_status_badge(
    context: DrawContext,
    rect: Rect,
    status: str,
) -> None:
    translated = context.translate(status)
    badge_width = min(max(text_width(translated) + 12, 48), 70)
    badge = Rect(rect.x + 86, rect.y + 61, badge_width, 18)
    if status == "BUY":
        fill = PyxelColor.LEAF_GREEN
        text_color = PyxelColor.UI_DARK
    elif status == "DONE":
        fill = PyxelColor.CYAN_SCIENCE
        text_color = PyxelColor.UI_DARK
    else:
        fill = PyxelColor.METAL_DARK
        text_color = PyxelColor.PARCHMENT_LIGHT
    draw_rounded_panel(badge, fill, PyxelColor.UI_DARK, fill)
    draw_text(
        badge.x + (badge.width - text_width(translated)) // 2,
        badge.y + 5,
        translated,
        text_color,
    )


def _draw_details_panel(
    context: DrawContext,
    data: ShopScreenData,
    card: ShopCardData,
) -> None:
    translate = context.translate
    draw_panel(SHOP_DETAILS_PANEL)
    draw_text(
        SHOP_DETAILS_PANEL.x + 16,
        SHOP_DETAILS_PANEL.y + 12,
        translate("SELECTED UPGRADE"),
        PyxelColor.LEAF_SHADOW,
    )
    draw_text(
        SHOP_DETAILS_PANEL.x + 16,
        SHOP_DETAILS_PANEL.y + 29,
        fit_text(translate(card.title), 340),
        PyxelColor.UI_DARK,
    )
    for index, line in enumerate(data.details[:3]):
        draw_text(
            SHOP_DETAILS_PANEL.x + 16,
            SHOP_DETAILS_PANEL.y + 46 + index * 12,
            fit_text(translate(line), 360),
            PyxelColor.UI_DARK,
        )
    draw_text(
        SHOP_BUY_BUTTON.x + 3,
        SHOP_BUY_BUTTON.y - 13,
        card.cost,
        PyxelColor.UI_DARK,
    )
    draw_button(
        SHOP_BUY_BUTTON,
        translate("BUY"),
        enabled=data.buy_enabled,
    )


def _draw_card_artwork(
    artwork: str,
    rect: Rect,
    sprite: tuple[int, int] | None,
) -> None:
    if artwork == "slot":
        _draw_slot_artwork(rect)
    elif artwork == "analyzer":
        _draw_analyzer_artwork(rect)
    else:
        _draw_species_artwork(rect, sprite)


def _draw_slot_artwork(rect: Rect) -> None:
    pyxel.blt(
        rect.x + 2,
        rect.y + 2,
        0,
        64,
        64,
        64,
        64,
        colkey=0,
        scale=1,
    )
    pyxel.rect(
        rect.x + 12,
        rect.y + rect.height - 15,
        rect.width - 24,
        6,
        PyxelColor.SOIL_DARK,
    )
    pyxel.line(
        rect.x + 15,
        rect.y + rect.height - 17,
        rect.x + rect.width - 16,
        rect.y + rect.height - 17,
        PyxelColor.LEAF_HIGHLIGHT,
    )


def _draw_analyzer_artwork(rect: Rect) -> None:
    machine = Rect(rect.x + 11, rect.y + 10, rect.width - 22, rect.height - 22)
    draw_rounded_panel(
        machine,
        PyxelColor.METAL_DARK,
        PyxelColor.UI_DARK,
        PyxelColor.METAL_LIGHT,
    )
    screen = Rect(machine.x + 7, machine.y + 7, machine.width - 14, 25)
    pyxel.rect(
        screen.x,
        screen.y,
        screen.width,
        screen.height,
        PyxelColor.DEEP_GLASS_NAVY,
    )
    pyxel.rectb(
        screen.x,
        screen.y,
        screen.width,
        screen.height,
        PyxelColor.CYAN_SCIENCE,
    )
    pulse = pyxel.frame_count // 10 % max(screen.width - 8, 1)
    pyxel.line(
        screen.x + 4,
        screen.y + 17,
        screen.x + 4 + pulse,
        screen.y + 9,
        PyxelColor.CYAN_SCIENCE,
    )
    pyxel.circ(machine.x + 12, machine.y + 40, 3, PyxelColor.LEAF_GREEN)
    pyxel.circ(machine.x + 24, machine.y + 40, 3, PyxelColor.SEED_GOLD)
    pyxel.line(
        machine.x + machine.width - 13,
        machine.y + 38,
        machine.x + machine.width - 7,
        machine.y + 38,
        PyxelColor.METAL_LIGHT,
    )


def _draw_species_artwork(
    rect: Rect,
    sprite: tuple[int, int] | None,
) -> None:
    if sprite is None:
        pyxel.blt(
            rect.x + 2,
            rect.y + 2,
            0,
            128,
            64,
            64,
            64,
            colkey=0,
        )
        return
    u, v = sprite
    pyxel.blt(
        rect.x + 2,
        rect.y + 2,
        0,
        u,
        v,
        64,
        64,
        colkey=0,
    )
