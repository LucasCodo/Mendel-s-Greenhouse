"""Shared rendering contracts for Pyxel UI components."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

import pyxel

from mendels_greenhouse.ui.fonts import draw_outlined_text, draw_text
from mendels_greenhouse.ui.palette import PyxelColor


class Translator(Protocol):
    """Callable translation helper used by UI components."""

    def __call__(self, text: str, **kwargs: object) -> str:
        """Translate a UI string."""


@dataclass(frozen=True)
class DrawContext:
    """Shared drawing dependencies for scene components."""

    translate: Translator
    display_font: pyxel.Font | None


TextWrapper = Callable[[str, int], list[str]]


def draw_scene_shell(
    context: DrawContext,
    title: str,
    subtitle: str,
) -> None:
    """Draw the shared title/subtitle shell for runtime sub-screens."""
    draw_outlined_text(
        24,
        76,
        context.translate(title).upper(),
        PyxelColor.ACCENT,
        font=context.display_font,
    )
    draw_text(
        26,
        91,
        context.translate(subtitle),
        PyxelColor.PARCHMENT_LIGHT,
    )


def draw_modal_scrim(opacity: float) -> None:
    """Draw a full-screen modal scrim using Pyxel dithering."""
    pyxel.dither(opacity)
    pyxel.rect(0, 0, pyxel.width, pyxel.height, PyxelColor.UI_DARK)
    pyxel.dither(1)
