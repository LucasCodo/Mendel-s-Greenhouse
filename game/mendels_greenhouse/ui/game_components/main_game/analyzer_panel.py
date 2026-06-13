"""Analyzer/probability panel for the main game scene."""

from dataclasses import dataclass

import pyxel

from mendels_greenhouse.ui.components import Rect
from mendels_greenhouse.ui.fonts import draw_text, fit_text
from mendels_greenhouse.ui.game_components.shared import DrawContext
from mendels_greenhouse.ui.palette import PyxelColor

ANALYZER_PANEL = Rect(10, 68, 170, 280)
ANALYZER_SCREEN = Rect(34, 82, 138, 252)


@dataclass(frozen=True)
class AnalyzerPanelData:
    """Display data for the analyzer probability panel."""

    has_parent_pair: bool
    analyzer_level: int
    genotype_level: int
    probability_level: int
    simulator_level: int
    phenotype_lines: list[str]
    genotype_lines: list[str]
    gamete_lines: list[str]
    probability_lines: list[str]
    best_cross: str | None
    max_probability_y: int
    view_level: int


def draw_analyzer_panel(
    context: DrawContext,
    data: AnalyzerPanelData,
) -> None:
    """Draw the left analyzer probability panel as a handheld console."""
    rect = ANALYZER_PANEL
    _draw_console_bezel(rect)
    _draw_glass_tube(ANALYZER_SCREEN)
    _draw_crt_screen(rect, context, data)


def _draw_rounded_fill_r10(x: int, y: int, w: int, h: int, color: int) -> None:
    # Fill rows symmetrically from top and bottom
    pyxel.rect(x + 10, y, w - 20, 1, color)
    pyxel.rect(x + 10, y + h - 1, w - 20, 1, color)

    pyxel.rect(x + 6, y + 1, w - 12, 1, color)
    pyxel.rect(x + 6, y + h - 2, w - 12, 1, color)

    pyxel.rect(x + 4, y + 2, w - 8, 1, color)
    pyxel.rect(x + 4, y + h - 3, w - 8, 1, color)

    pyxel.rect(x + 3, y + 3, w - 6, 1, color)
    pyxel.rect(x + 3, y + h - 4, w - 6, 1, color)

    pyxel.rect(x + 2, y + 4, w - 4, 1, color)
    pyxel.rect(x + 2, y + h - 5, w - 4, 1, color)

    pyxel.rect(x + 2, y + 5, w - 4, 1, color)
    pyxel.rect(x + 2, y + h - 6, w - 4, 1, color)

    for r_y in range(y + 6, y + 10):
        pyxel.rect(x + 1, r_y, w - 2, 1, color)
    for r_y in range(y + h - 10, y + h - 6):
        pyxel.rect(x + 1, r_y, w - 2, 1, color)

    pyxel.rect(x, y + 10, w, h - 20, color)


def _draw_rounded_border_r10(
    x: int, y: int, w: int, h: int, color: int
) -> None:
    # Outer lines
    pyxel.line(x + 10, y, x + w - 11, y, color)
    pyxel.line(x + 10, y + h - 1, x + w - 11, y + h - 1, color)
    pyxel.line(x, y + 10, x, y + h - 11, color)
    pyxel.line(x + w - 1, y + 10, x + w - 1, y + h - 11, color)

    # Top-Left Corner
    pyxel.line(x + 6, y + 1, x + 9, y + 1, color)
    pyxel.line(x + 4, y + 2, x + 5, y + 2, color)
    pyxel.pset(x + 3, y + 3, color)
    pyxel.line(x + 2, y + 4, x + 2, y + 5, color)
    pyxel.line(x + 1, y + 6, x + 1, y + 9, color)

    # Top-Right Corner
    pyxel.line(x + w - 10, y + 1, x + w - 7, y + 1, color)
    pyxel.line(x + w - 6, y + 2, x + w - 5, y + 2, color)
    pyxel.pset(x + w - 4, y + 3, color)
    pyxel.line(x + w - 3, y + 4, x + w - 3, y + 5, color)
    pyxel.line(x + w - 2, y + 6, x + w - 2, y + 9, color)

    # Bottom-Left Corner
    pyxel.line(x + 6, y + h - 2, x + 9, y + h - 2, color)
    pyxel.line(x + 4, y + h - 3, x + 5, y + h - 3, color)
    pyxel.pset(x + 3, y + h - 4, color)
    pyxel.line(x + 2, y + h - 6, x + 2, y + h - 5, color)
    pyxel.line(x + 1, y + h - 10, x + 1, y + h - 7, color)

    # Bottom-Right Corner
    pyxel.line(x + w - 10, y + h - 2, x + w - 7, y + h - 2, color)
    pyxel.line(x + w - 6, y + h - 3, x + w - 5, y + h - 3, color)
    pyxel.pset(x + w - 4, y + h - 4, color)
    pyxel.line(x + w - 3, y + h - 6, x + w - 3, y + h - 5, color)
    pyxel.line(x + w - 2, y + h - 10, x + w - 2, y + h - 7, color)


def _draw_console_bezel(rect: Rect) -> None:
    """Draw the console body case and corner screw rivets."""
    # Draw dark wood outer frame and shadow
    _draw_rounded_border_r10(
        rect.x, rect.y, rect.width, rect.height, PyxelColor.FRAME
    )
    _draw_rounded_border_r10(
        rect.x + 1,
        rect.y + 1,
        rect.width - 2,
        rect.height - 2,
        PyxelColor.UI_DARK,
    )

    # Fill console body base (parchment beige)
    _draw_rounded_fill_r10(
        rect.x + 2,
        rect.y + 2,
        rect.width - 4,
        rect.height - 4,
        PyxelColor.PARCHMENT_BASE,
    )

    # Casing 3D border shadows & highlights
    pyxel.line(
        rect.x + 10,
        rect.y + 2,
        rect.x + rect.width - 11,
        rect.y + 2,
        PyxelColor.PARCHMENT_LIGHT,
    )
    pyxel.line(
        rect.x + 2,
        rect.y + 10,
        rect.x + 2,
        rect.y + rect.height - 11,
        PyxelColor.PARCHMENT_LIGHT,
    )
    pyxel.line(
        rect.x + rect.width - 3,
        rect.y + 10,
        rect.x + rect.width - 3,
        rect.y + rect.height - 11,
        PyxelColor.WOOD_MIDTONE,
    )
    pyxel.line(
        rect.x + 10,
        rect.y + rect.height - 3,
        rect.x + rect.width - 11,
        rect.y + rect.height - 3,
        PyxelColor.SOIL_DARK,
    )

    # Bezel Corner Screws
    def draw_screw(sx: int, sy: int) -> None:
        pyxel.pset(sx, sy, PyxelColor.METAL_LIGHT)
        pyxel.pset(sx + 1, sy, PyxelColor.SOIL_DARK)
        pyxel.pset(sx, sy + 1, PyxelColor.SOIL_DARK)

    draw_screw(rect.x + 12, rect.y + 12)
    draw_screw(rect.x + rect.width - 14, rect.y + 12)
    draw_screw(rect.x + 12, rect.y + rect.height - 14)
    draw_screw(rect.x + rect.width - 14, rect.y + rect.height - 14)


def _draw_glass_tube(screen: Rect) -> None:
    """Draw the glass tube with glowing liquid and procedural bubbles."""
    tx, ty, tw, th = screen.x - 17, screen.y, 10, screen.height
    # Dark shadow background of tube
    pyxel.rect(tx, ty, tw, th, PyxelColor.INK_SHADOW)

    # Fluid height meniscus (fill ~70%)
    fluid_lvl_y = ty + 25
    if fluid_lvl_y < ty + th - 2:
        pyxel.rect(
            tx + 1,
            fluid_lvl_y,
            tw - 2,
            (ty + th - 2) - fluid_lvl_y,
            PyxelColor.LEAF_GREEN,
        )
        # 3D fluid shading columns
        pyxel.line(
            tx + 1, fluid_lvl_y, tx + 1, ty + th - 2, PyxelColor.LEAF_SHADOW
        )
        pyxel.line(
            tx + tw - 2,
            fluid_lvl_y,
            tx + tw - 2,
            ty + th - 2,
            PyxelColor.LEAF_SHADOW,
        )
        for cx in range(tx + 2, tx + tw - 2):
            pyxel.line(
                cx, fluid_lvl_y, cx, ty + th - 2, PyxelColor.LEAF_HIGHLIGHT
            )

    # Procedural rising bubbles inside fluid (using frame_count)
    for i in range(2):
        bubble_speed = 1.0 + i * 0.2
        phase = int((pyxel.frame_count * bubble_speed + i * 25) % (th - 27))
        by = ty + th - 3 - phase
        bx = tx + 2 + (i * 3 + pyxel.frame_count // 8) % (tw - 4)
        if fluid_lvl_y <= by <= ty + th - 2:
            pyxel.pset(bx, by, PyxelColor.WHITE_PETAL)

    # Tube highlights & shine
    pyxel.line(tx + 2, ty + 1, tx + 2, ty + th - 2, PyxelColor.GLASS_HIGHLIGHT)
    pyxel.line(
        tx + tw - 2,
        ty + 1,
        tx + tw - 2,
        ty + th - 2,
        PyxelColor.PARCHMENT_LIGHT,
    )

    # Metal endcaps
    pyxel.rect(tx - 1, ty - 2, tw + 2, 3, PyxelColor.METAL_DARK)
    pyxel.rectb(tx - 1, ty - 2, tw + 2, 3, PyxelColor.SOIL_DARK)
    pyxel.rect(tx - 1, ty + th - 1, tw + 2, 3, PyxelColor.METAL_DARK)
    pyxel.rectb(tx - 1, ty + th - 1, tw + 2, 3, PyxelColor.SOIL_DARK)


def _draw_crt_screen(
    _rect: Rect,
    context: DrawContext,
    data: AnalyzerPanelData,
) -> None:
    """Draw the green CRT screen, scanlines, and diagnostic text."""
    translate = context.translate
    sx = ANALYZER_SCREEN.x
    sy = ANALYZER_SCREEN.y
    sw = ANALYZER_SCREEN.width
    sh = ANALYZER_SCREEN.height

    # Screen background and bezel borders
    pyxel.rect(sx, sy, sw, sh, PyxelColor.INK_SHADOW)
    pyxel.rectb(sx, sy, sw, sh, PyxelColor.METAL_DARK)
    pyxel.rectb(sx + 1, sy + 1, sw - 2, sh - 2, PyxelColor.DEEP_GLASS_NAVY)

    # Screen green grid mesh
    for gx in range(sx + 6, sx + sw - 2, 12):
        for gy in range(sy + 6, sy + sh - 2, 12):
            pyxel.pset(gx, gy, PyxelColor.LEAF_SHADOW)

    # CRT Scanline animation
    scanline_y = sy + 2 + (pyxel.frame_count // 2) % (sh - 4)
    pyxel.line(
        sx + 2,
        scanline_y,
        sx + sw - 3,
        scanline_y,
        PyxelColor.DEEP_GLASS_NAVY,
    )

    # Screen Title Header
    header = translate("Analyzer").upper()
    draw_text(
        sx + 6,
        sy + 5,
        fit_text(f"{header} L{data.view_level}", sw - 12),
        PyxelColor.ACCENT,
    )
    pyxel.line(sx + 4, sy + 13, sx + sw - 5, sy + 13, PyxelColor.LEAF_SHADOW)

    # Screen Display Logic
    if not data.has_parent_pair:
        draw_text(
            sx + 6,
            sy + 22,
            fit_text(translate("Select parents"), sw - 12),
            PyxelColor.LEAF_HIGHLIGHT,
        )
    else:
        y = sy + 20
        y = _draw_report_section(
            Rect(sx, y, sw, 0),
            translate("Phenotype"),
            data.phenotype_lines,
        )
        if data.view_level >= data.genotype_level:
            y = _draw_report_section(
                Rect(sx, y + 2, sw, 0),
                translate("Genotype"),
                data.genotype_lines,
            )
        if data.view_level >= data.probability_level:
            y = _draw_report_section(
                Rect(sx, y + 2, sw, 0),
                translate("Gametes"),
                data.gamete_lines,
            )
            _draw_report_section(
                Rect(sx, y + 2, sw, 0),
                translate("Expected outcomes"),
                data.probability_lines,
                max_lines=6,
            )

        # Level 4 Simulator preview
        if data.view_level >= data.simulator_level:
            summary_y = sy + sh - 54
            pyxel.line(
                sx + 4,
                summary_y,
                sx + sw - 5,
                summary_y,
                PyxelColor.LEAF_SHADOW,
            )
            draw_text(
                sx + 6,
                summary_y + 5,
                fit_text(translate("Best stored cross"), sw - 12),
                PyxelColor.ACCENT,
            )
            best = (
                data.best_cross
                if data.best_cross is not None
                else translate("No valid stored cross found.")
            )
            draw_text(
                sx + 6,
                summary_y + 17,
                fit_text(best, sw - 12),
                PyxelColor.WHITE_PETAL,
            )
    online = data.analyzer_level >= data.probability_level
    status = translate("ONLINE") if online else translate("STANDBY")
    status_color = (
        PyxelColor.SUCCESS_LIME if online else PyxelColor.TOMATO_ORANGE
    )
    status_y = sy + sh - 12
    pyxel.line(
        sx + 4,
        status_y - 4,
        sx + sw - 5,
        status_y - 4,
        PyxelColor.LEAF_SHADOW,
    )
    draw_text(sx + 6, status_y, status, status_color)
    pyxel.circ(sx + sw - 9, status_y + 3, 2, status_color)


def _draw_report_section(
    rect: Rect,
    title: str,
    lines: list[str],
    *,
    max_lines: int = 2,
) -> int:
    draw_text(
        rect.x + 6,
        rect.y,
        fit_text(title.upper(), rect.width - 12),
        PyxelColor.ACCENT,
    )
    y = rect.y + 10
    for line in lines[:max_lines]:
        draw_text(
            rect.x + 6,
            y,
            fit_text(line, rect.width - 12),
            PyxelColor.SUCCESS_LIME,
        )
        y += 9
    return y
