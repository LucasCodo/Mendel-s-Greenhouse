"""Scene abstractions for the Pyxel runtime."""

from typing import Protocol


class Scene(Protocol):
    """A Pyxel screen with update and draw hooks."""

    def update(self) -> None:
        """Advance scene state."""

    def draw(self) -> None:
        """Render the scene."""


class SceneManager:
    """Hold and switch the active scene."""

    def __init__(self) -> None:
        self.current: Scene | None = None

    def switch_to(self, scene: Scene) -> None:
        """Switch to another scene."""
        self.current = scene

    def update(self) -> None:
        """Update the current scene."""
        if self.current is not None:
            self.current.update()

    def draw(self) -> None:
        """Draw the current scene."""
        if self.current is not None:
            self.current.draw()
