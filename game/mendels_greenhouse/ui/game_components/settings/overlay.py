"""Settings overlay rendering."""

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
    text_width,
)
from mendels_greenhouse.ui.game_components.shared import (
    DrawContext,
    draw_modal_scrim,
)
from mendels_greenhouse.ui.palette import PyxelColor

SETTINGS_PANEL = Rect(140, 28, 360, 304)
SETTINGS_PREFERENCES_PANEL = Rect(158, 68, 324, 160)
LANGUAGE_BUTTON = Rect(348, 76, 118, 24)
MUSIC_DOWN_BUTTON = Rect(326, 112, 24, 22)
MUSIC_UP_BUTTON = Rect(442, 112, 24, 22)
MUSIC_MUTE_CHECKBOX = Rect(326, 140, 14, 14)
SOUND_DOWN_BUTTON = Rect(326, 174, 24, 22)
SOUND_UP_BUTTON = Rect(442, 174, 24, 22)
SOUND_MUTE_CHECKBOX = Rect(326, 202, 14, 14)
RESET_PROGRESS_BUTTON = Rect(184, 250, 272, 22)
SETTINGS_BACK_BUTTON = Rect(252, 286, 136, 24)
RESET_CONFIRM_BUTTON = Rect(324, 250, 92, 22)
RESET_CANCEL_BUTTON = Rect(224, 250, 92, 22)


@dataclass(frozen=True)
class VolumeControlData:
    """Display data for a volume control row."""

    y: int
    label: str
    value: int
    down_button: Rect
    up_button: Rect


@dataclass(frozen=True)
class SettingsOverlayData:
    """Display data for the settings overlay."""

    language_label: str
    language_button: Rect
    music: VolumeControlData
    sound: VolumeControlData
    music_mute_checkbox: Rect
    sound_mute_checkbox: Rect
    music_muted: bool
    sound_muted: bool
    reset_button: Rect
    back_button: Rect
    reset_confirmation_open: bool
    reset_cancel_button: Rect
    reset_confirm_button: Rect


def draw_settings_overlay(
    context: DrawContext,
    data: SettingsOverlayData,
) -> None:
    """Draw the settings overlay."""
    translate = context.translate
    draw_modal_scrim(0.65)
    draw_panel(SETTINGS_PANEL)
    title = translate("Settings").upper()
    draw_outlined_text(
        SETTINGS_PANEL.x
        + (SETTINGS_PANEL.width - text_width(title, context.display_font))
        // 2,
        SETTINGS_PANEL.y + 16,
        title,
        PyxelColor.ACCENT,
        font=context.display_font,
    )
    draw_rounded_panel(
        SETTINGS_PREFERENCES_PANEL,
        PyxelColor.PARCHMENT,
        PyxelColor.FRAME,
        PyxelColor.WOOD_MIDTONE,
    )
    draw_text(174, 84, translate("Language"), PyxelColor.UI_DARK)
    draw_button(data.language_button, data.language_label)
    pyxel.line(170, 104, 470, 104, PyxelColor.WOOD_MIDTONE)
    _draw_volume_control(data.music)
    _draw_checkbox(
        data.music_mute_checkbox,
        data.music_muted,
        translate("Mute music"),
    )
    _draw_volume_control(data.sound)
    _draw_checkbox(
        data.sound_mute_checkbox,
        data.sound_muted,
        translate("Mute sounds"),
    )
    draw_text(
        184,
        232,
        translate("Changes apply immediately."),
        PyxelColor.TEXT_MUTED,
    )
    draw_button(data.reset_button, translate("Reset game progression"))
    draw_button(data.back_button, translate("BACK"))
    if data.reset_confirmation_open:
        draw_reset_confirmation(context, data)


def draw_reset_confirmation(
    context: DrawContext,
    data: SettingsOverlayData,
) -> None:
    """Draw the reset confirmation dialog."""
    translate = context.translate
    draw_modal_scrim(0.82)
    panel = Rect(176, 100, 288, 182)
    draw_panel(panel)
    draw_outlined_text(
        panel.x + 76,
        panel.y + 18,
        translate("Dangerous action").upper(),
        PyxelColor.ERROR_EMBER,
        font=context.display_font,
    )
    lines = [
        "This will erase all progression data.",
        "Contracts, credits, discoveries, and plants will reset.",
        "This cannot be undone.",
    ]
    for index, line in enumerate(lines):
        draw_text(
            panel.x + 24,
            panel.y + 58 + index * 18,
            translate(line),
            PyxelColor.UI_DARK,
        )
    draw_button(data.reset_cancel_button, translate("CANCEL"))
    draw_button(data.reset_confirm_button, translate("CONFIRM RESET"))


def _draw_volume_control(data: VolumeControlData) -> None:
    label_y = data.y + 7
    draw_text(174, label_y, data.label, PyxelColor.UI_DARK)
    draw_text(
        274,
        label_y,
        f"{data.value * 10:3d}%",
        PyxelColor.UI_DARK,
    )
    draw_button(data.down_button, "-")
    bar_x = data.down_button.x + data.down_button.width + 8
    bar_width = data.up_button.x - bar_x - 8
    bar_y = data.y + 8
    fill_width = round(bar_width * data.value / 10)
    pyxel.rect(bar_x, bar_y, bar_width, 6, PyxelColor.BAR_EMPTY)
    pyxel.rect(bar_x, bar_y, fill_width, 6, PyxelColor.PROGRESS)
    pyxel.rectb(
        bar_x,
        bar_y,
        bar_width,
        6,
        PyxelColor.UI_DARK,
    )
    draw_button(data.up_button, "+")


def _draw_checkbox(rect: Rect, checked: bool, label: str) -> None:
    pyxel.rect(rect.x, rect.y, rect.width, rect.height, PyxelColor.FIELD)
    pyxel.rectb(rect.x, rect.y, rect.width, rect.height, PyxelColor.UI_DARK)
    if checked:
        pyxel.line(
            rect.x + 2,
            rect.y + 6,
            rect.x + 5,
            rect.y + 9,
            PyxelColor.PROGRESS,
        )
        pyxel.line(
            rect.x + 5,
            rect.y + 9,
            rect.x + 10,
            rect.y + 2,
            PyxelColor.PROGRESS,
        )
    draw_text(rect.x + 18, rect.y + 3, label, PyxelColor.UI_DARK)
