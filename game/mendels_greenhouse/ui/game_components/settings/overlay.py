"""Settings overlay rendering."""

from dataclasses import dataclass

import pyxel

from mendels_greenhouse.ui.components import Rect, draw_button, draw_panel
from mendels_greenhouse.ui.fonts import draw_outlined_text
from mendels_greenhouse.ui.game_components.shared import (
    DrawContext,
    draw_modal_scrim,
)
from mendels_greenhouse.ui.palette import PyxelColor


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
    panel = Rect(100, 70, 440, 242)
    draw_panel(panel)
    draw_outlined_text(
        254,
        84,
        translate("Settings").upper(),
        PyxelColor.ACCENT,
        font=context.display_font,
    )
    pyxel.text(188, 106, translate("Language"), PyxelColor.UI_DARK)
    draw_button(data.language_button, data.language_label)
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
    pyxel.text(
        188,
        232,
        translate("Changes apply immediately."),
        PyxelColor.UI_DARK,
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
        pyxel.text(
            panel.x + 24,
            panel.y + 58 + index * 18,
            translate(line),
            PyxelColor.UI_DARK,
        )
    draw_button(data.reset_cancel_button, translate("CANCEL"))
    draw_button(data.reset_confirm_button, translate("CONFIRM RESET"))


def _draw_volume_control(data: VolumeControlData) -> None:
    x = 188
    pyxel.text(x, data.y, data.label, PyxelColor.UI_DARK)
    draw_button(data.down_button, "-")
    pyxel.rect(x + 176, data.y + 11, 40, 6, PyxelColor.BAR_EMPTY)
    pyxel.rect(x + 176, data.y + 11, data.value * 4, 6, PyxelColor.PROGRESS)
    pyxel.rectb(x + 176, data.y + 11, 40, 6, PyxelColor.UI_DARK)
    pyxel.text(
        x + 224,
        data.y + 9,
        f"{data.value * 10:3d}%",
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
    pyxel.text(rect.x + 18, rect.y + 3, label, PyxelColor.UI_DARK)
