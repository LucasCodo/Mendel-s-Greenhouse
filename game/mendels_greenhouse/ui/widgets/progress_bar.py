"""Reusable Progress Bar widget for Pyxel UI."""

from dataclasses import dataclass

import pyxel

from mendels_greenhouse.ui.components import Rect
from mendels_greenhouse.ui.palette import PyxelColor


@dataclass(frozen=True)
class ProgressBar:
    """A progress bar that renders its background and filled progress."""

    rect: Rect
    current_value: float
    target_value: float
    color: int = PyxelColor.PROGRESS
    empty_color: int = PyxelColor.BAR_EMPTY
    border_color: int | None = None

    def draw(self) -> None:
        """Render the progress bar to Pyxel."""
        # Calculate filled width
        if self.target_value <= 0:
            filled_width = 0
        else:
            progress = min(self.current_value / self.target_value, 1.0)
            filled_width = int(self.rect.width * progress)

        # Draw empty background
        pyxel.rect(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height,
            self.empty_color,
        )

        # Draw filled progress
        if filled_width > 0:
            pyxel.rect(
                self.rect.x,
                self.rect.y,
                filled_width,
                self.rect.height,
                self.color,
            )

        # Draw border if configured
        if self.border_color is not None:
            pyxel.rectb(
                self.rect.x,
                self.rect.y,
                self.rect.width,
                self.rect.height,
                self.border_color,
            )
