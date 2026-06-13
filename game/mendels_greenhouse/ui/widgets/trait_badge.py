"""Reusable Trait Badge widget for Pyxel UI."""

from dataclasses import dataclass

import pyxel

from mendels_greenhouse.ui.components import Rect
from mendels_greenhouse.ui.fonts import (
    DISPLAY_GLYPH_HEIGHT,
    draw_text,
    text_width,
)
from mendels_greenhouse.ui.palette import PyxelColor


@dataclass(frozen=True)
class TraitBadge:
    """A visual badge displaying a phenotype trait and its status."""

    rect: Rect
    label: str
    discovered: bool = True
    newly_discovered: bool = False
    contract_required: bool = False

    def draw(self) -> None:
        """Render the trait badge."""
        # Determine background and border colors based on states
        if not self.discovered:
            bg_color = PyxelColor.BAR_EMPTY
            border_color = PyxelColor.FRAME
            text_color = PyxelColor.TEXT_MUTED
            display_label = "???"
        elif self.newly_discovered:
            bg_color = PyxelColor.ACCENT
            border_color = PyxelColor.SUCCESS_LIME
            text_color = PyxelColor.UI_DARK
            display_label = self.label
        elif self.contract_required:
            bg_color = PyxelColor.FIELD
            border_color = PyxelColor.SUCCESS_LIME
            text_color = PyxelColor.UI_DARK
            # Star prefix indicates contract requirement
            display_label = f"* {self.label}"
        else:
            bg_color = PyxelColor.FIELD
            border_color = PyxelColor.FRAME
            text_color = PyxelColor.UI_DARK
            display_label = self.label

        # Draw badge background
        pyxel.rect(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height,
            bg_color,
        )

        # Draw badge border
        pyxel.rectb(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height,
            border_color,
        )

        # Draw inner detail line for newly discovered/special badges
        if self.newly_discovered or self.contract_required:
            pyxel.rectb(
                self.rect.x + 1,
                self.rect.y + 1,
                self.rect.width - 2,
                self.rect.height - 2,
                PyxelColor.UI_DARK,
            )

        # Center text inside the badge
        label_width = text_width(display_label)
        text_x = self.rect.x + max((self.rect.width - label_width) // 2, 2)
        text_y = self.rect.y + (self.rect.height - DISPLAY_GLYPH_HEIGHT) // 2
        draw_text(text_x, text_y, display_label, text_color)
