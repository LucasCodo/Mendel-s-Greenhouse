"""Small Pyxel UI helpers for the MVP screens."""

from dataclasses import dataclass

import pyxel

from mendels_greenhouse.ui.palette import PyxelColor


@dataclass(frozen=True)
class Rect:
    """Clickable rectangle."""

    x: int
    y: int
    width: int
    height: int

    def contains(self, x: int, y: int) -> bool:
        """Return whether a point is inside the rectangle."""
        return (
            self.x <= x < self.x + self.width
            and self.y <= y < self.y + self.height
        )


def clicked(rect: Rect) -> bool:
    """Return whether the mouse clicked inside a rectangle."""
    return pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and rect.contains(
        pyxel.mouse_x, pyxel.mouse_y
    )


def draw_button(
    rect: Rect,
    label: str,
    *,
    enabled: bool = True,
    pressed: bool = False,
) -> None:
    """Draw an animated framed pixel-art button."""
    hovering = rect.contains(pyxel.mouse_x, pyxel.mouse_y)
    offset = 1 if pressed else 0
    fill = PyxelColor.ACTION if enabled else PyxelColor.TEXT_MUTED
    if hovering and enabled and not pressed:
        fill = PyxelColor.ACCENT
    text = PyxelColor.TEXT if enabled else PyxelColor.UI_DARK
    pyxel.rect(
        rect.x + 2,
        rect.y + 3,
        rect.width,
        rect.height,
        PyxelColor.UI_DARK,
    )
    pyxel.rect(rect.x, rect.y + offset, rect.width, rect.height, fill)
    pyxel.rectb(
        rect.x,
        rect.y + offset,
        rect.width,
        rect.height,
        PyxelColor.FRAME,
    )
    pyxel.rectb(
        rect.x + 1,
        rect.y + 1 + offset,
        rect.width - 2,
        rect.height - 2,
        PyxelColor.UI_DARK,
    )
    if enabled and not pressed:
        pyxel.line(
            rect.x + 3,
            rect.y + 3,
            rect.x + rect.width - 4,
            rect.y + 3,
            PyxelColor.PARCHMENT,
        )
    text_x = rect.x + max((rect.width - len(label) * 4) // 2, 2)
    text_y = rect.y + offset + rect.height // 2 - 2
    pyxel.text(text_x + 1, text_y + 1, label, PyxelColor.UI_DARK)
    pyxel.text(text_x, text_y, label, text)


def draw_panel(rect: Rect, title: str | None = None) -> None:
    """Draw a parchment panel with a wood frame."""
    pyxel.rect(rect.x, rect.y, rect.width, rect.height, PyxelColor.PARCHMENT)
    pyxel.rectb(rect.x, rect.y, rect.width, rect.height, PyxelColor.FRAME)
    pyxel.rectb(
        rect.x + 1,
        rect.y + 1,
        rect.width - 2,
        rect.height - 2,
        PyxelColor.UI_DARK,
    )
    if title is not None:
        pyxel.text(rect.x + 6, rect.y + 6, title, PyxelColor.UI_DARK)
