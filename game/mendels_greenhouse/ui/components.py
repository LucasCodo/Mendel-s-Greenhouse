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


def draw_button(  # noqa: PLR0915
    rect: Rect,
    label: str,
    *,
    enabled: bool = True,
    pressed: bool = False,
) -> None:
    """Draw an rounded framed pixel-art button."""
    hovering = rect.contains(pyxel.mouse_x, pyxel.mouse_y)
    offset = 1 if pressed else 0
    fill = PyxelColor.ACTION if enabled else PyxelColor.TEXT_MUTED
    if hovering and enabled and not pressed:
        fill = PyxelColor.ACCENT
    text = PyxelColor.TEXT if enabled else PyxelColor.UI_DARK

    # Draw rounded shadow
    sh_x = rect.x + 2
    sh_y = rect.y + 3
    pyxel.rect(sh_x + 4, sh_y, rect.width - 8, 1, PyxelColor.UI_DARK)
    pyxel.rect(sh_x + 2, sh_y + 1, rect.width - 4, 1, PyxelColor.UI_DARK)
    pyxel.rect(sh_x + 1, sh_y + 2, rect.width - 2, 1, PyxelColor.UI_DARK)
    pyxel.rect(sh_x, sh_y + 3, rect.width, rect.height - 6, PyxelColor.UI_DARK)
    pyxel.rect(
        sh_x + 1,
        sh_y + rect.height - 3,
        rect.width - 2,
        1,
        PyxelColor.UI_DARK,
    )
    pyxel.rect(
        sh_x + 2,
        sh_y + rect.height - 2,
        rect.width - 4,
        1,
        PyxelColor.UI_DARK,
    )
    pyxel.rect(
        sh_x + 4,
        sh_y + rect.height - 1,
        rect.width - 8,
        1,
        PyxelColor.UI_DARK,
    )

    # Draw rounded main fill
    rx = rect.x
    ry = rect.y + offset
    w = rect.width
    h = rect.height
    pyxel.rect(rx + 4, ry, w - 8, 1, fill)
    pyxel.rect(rx + 2, ry + 1, w - 4, 1, fill)
    pyxel.rect(rx + 1, ry + 2, w - 2, 1, fill)
    pyxel.rect(rx, ry + 3, w, h - 6, fill)
    pyxel.rect(rx + 1, ry + h - 3, w - 2, 1, fill)
    pyxel.rect(rx + 2, ry + h - 2, w - 4, 1, fill)
    pyxel.rect(rx + 4, ry + h - 1, w - 8, 1, fill)

    # Draw rounded outer border
    border_color = PyxelColor.FRAME
    pyxel.line(rx + 4, ry, rx + w - 5, ry, border_color)
    pyxel.line(rx + 4, ry + h - 1, rx + w - 5, ry + h - 1, border_color)
    pyxel.line(rx, ry + 3, rx, ry + h - 4, border_color)
    pyxel.line(rx + w - 1, ry + 3, rx + w - 1, ry + h - 4, border_color)
    # Corners
    pyxel.line(rx + 2, ry + 1, rx + 3, ry + 1, border_color)
    pyxel.pset(rx + 1, ry + 2, border_color)
    pyxel.line(rx + w - 4, ry + 1, rx + w - 3, ry + 1, border_color)
    pyxel.pset(rx + w - 2, ry + 2, border_color)

    pyxel.line(rx + 2, ry + h - 2, rx + 3, ry + h - 2, border_color)
    pyxel.pset(rx + 1, ry + h - 3, border_color)
    pyxel.line(rx + w - 4, ry + h - 2, rx + w - 3, ry + h - 2, border_color)
    pyxel.pset(rx + w - 2, ry + h - 3, border_color)

    # Draw rounded inner border (radius 3, inset by 1px)
    rx_in = rx + 1
    ry_in = ry + 1
    w_in = w - 2
    h_in = h - 2
    inner_color = PyxelColor.UI_DARK
    pyxel.line(rx_in + 3, ry_in, rx_in + w_in - 4, ry_in, inner_color)
    pyxel.line(
        rx_in + 3,
        ry_in + h_in - 1,
        rx_in + w_in - 4,
        ry_in + h_in - 1,
        inner_color,
    )
    pyxel.line(rx_in, ry_in + 3, rx_in, ry_in + h_in - 4, inner_color)
    pyxel.line(
        rx_in + w_in - 1,
        ry_in + 3,
        rx_in + w_in - 1,
        ry_in + h_in - 4,
        inner_color,
    )
    # Corners
    pyxel.line(rx_in + 1, ry_in + 1, rx_in + 2, ry_in + 1, inner_color)
    pyxel.pset(rx_in, ry_in + 2, inner_color)
    pyxel.line(
        rx_in + w_in - 3,
        ry_in + 1,
        rx_in + w_in - 2,
        ry_in + 1,
        inner_color,
    )
    pyxel.pset(rx_in + w_in - 1, ry_in + 2, inner_color)

    pyxel.line(
        rx_in + 1,
        ry_in + h_in - 2,
        rx_in + 2,
        ry_in + h_in - 2,
        inner_color,
    )
    pyxel.pset(rx_in, ry_in + h_in - 3, inner_color)
    pyxel.line(
        rx_in + w_in - 3,
        ry_in + h_in - 2,
        rx_in + w_in - 2,
        ry_in + h_in - 2,
        inner_color,
    )
    pyxel.pset(rx_in + w_in - 1, ry_in + h_in - 3, inner_color)

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


def draw_rounded_panel(
    rect: Rect,
    fill_color: int,
    border_color: int,
    inner_border_color: int,
) -> None:
    """Draw a rounded panel with border and inner frame."""
    # Fill (radius 4)
    pyxel.rect(rect.x + 4, rect.y, rect.width - 8, 1, fill_color)
    pyxel.rect(rect.x + 2, rect.y + 1, rect.width - 4, 1, fill_color)
    pyxel.rect(rect.x + 1, rect.y + 2, rect.width - 2, 1, fill_color)
    pyxel.rect(rect.x, rect.y + 3, rect.width, rect.height - 6, fill_color)
    pyxel.rect(
        rect.x + 1,
        rect.y + rect.height - 3,
        rect.width - 2,
        1,
        fill_color,
    )
    pyxel.rect(
        rect.x + 2,
        rect.y + rect.height - 2,
        rect.width - 4,
        1,
        fill_color,
    )
    pyxel.rect(
        rect.x + 4,
        rect.y + rect.height - 1,
        rect.width - 8,
        1,
        fill_color,
    )

    # Outer border (radius 4)
    pyxel.line(
        rect.x + 4, rect.y, rect.x + rect.width - 5, rect.y, border_color
    )
    pyxel.line(
        rect.x + 4,
        rect.y + rect.height - 1,
        rect.x + rect.width - 5,
        rect.y + rect.height - 1,
        border_color,
    )
    pyxel.line(
        rect.x, rect.y + 3, rect.x, rect.y + rect.height - 4, border_color
    )
    pyxel.line(
        rect.x + rect.width - 1,
        rect.y + 3,
        rect.x + rect.width - 1,
        rect.y + rect.height - 4,
        border_color,
    )
    # Corners
    pyxel.line(rect.x + 2, rect.y + 1, rect.x + 3, rect.y + 1, border_color)
    pyxel.pset(rect.x + 1, rect.y + 2, border_color)
    pyxel.line(
        rect.x + rect.width - 4,
        rect.y + 1,
        rect.x + rect.width - 3,
        rect.y + 1,
        border_color,
    )
    pyxel.pset(rect.x + rect.width - 2, rect.y + 2, border_color)

    pyxel.line(
        rect.x + 2,
        rect.y + rect.height - 2,
        rect.x + 3,
        rect.y + rect.height - 2,
        border_color,
    )
    pyxel.pset(rect.x + 1, rect.y + rect.height - 3, border_color)
    pyxel.line(
        rect.x + rect.width - 4,
        rect.y + rect.height - 2,
        rect.x + rect.width - 3,
        rect.y + rect.height - 2,
        border_color,
    )
    pyxel.pset(rect.x + rect.width - 2, rect.y + rect.height - 3, border_color)

    # Inner border (rounded inset by 2px)
    rx = rect.x
    ry = rect.y
    w = rect.width
    h = rect.height
    c = inner_border_color

    # Top/Bottom lines
    pyxel.line(rx + 4, ry + 2, rx + w - 5, ry + 2, c)
    pyxel.line(rx + 4, ry + h - 3, rx + w - 5, ry + h - 3, c)

    # Left/Right lines
    pyxel.line(rx + 2, ry + 4, rx + 2, ry + h - 5, c)
    pyxel.line(rx + w - 3, ry + 4, rx + w - 3, ry + h - 5, c)

    # Corners
    # Top-Left
    pyxel.pset(rx + 3, ry + 3, c)
    # Top-Right
    pyxel.pset(rx + w - 4, ry + 3, c)
    # Bottom-Left
    pyxel.pset(rx + 3, ry + h - 4, c)
    # Bottom-Right
    pyxel.pset(rx + w - 4, ry + h - 4, c)


def draw_panel(rect: Rect, title: str | None = None) -> None:
    """Draw a parchment panel with a wood frame."""
    draw_rounded_panel(
        rect, PyxelColor.PARCHMENT, PyxelColor.FRAME, PyxelColor.UI_DARK
    )
    if title is not None:
        pyxel.text(rect.x + 6, rect.y + 6, title, PyxelColor.UI_DARK)
