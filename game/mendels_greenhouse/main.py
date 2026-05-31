"""Pyxel application entrypoint for Mendel's Greenhouse."""

from pathlib import Path

import pyxel

from mendels_greenhouse.scenes.base import SceneManager
from mendels_greenhouse.scenes.main_game import HEIGHT, WIDTH, MainGameScene
from mendels_greenhouse.state.game_state import GameState
from mendels_greenhouse.ui.fonts import FontSet
from mendels_greenhouse.ui.palette import apply_project_palette

TITLE = "Mendel's Greenhouse"


class Game:
    """Pyxel runtime shell with scene management."""

    def __init__(self) -> None:
        pyxel.init(WIDTH, HEIGHT, title=TITLE, display_scale=2)
        pyxel.mouse(True)
        self._load_assets()
        apply_project_palette()
        self.assets_dir = Path(__file__).resolve().parent / "assets"
        self.fonts = FontSet(self.assets_dir)
        self.background_image = self._load_background_image()
        self.state = GameState.create_initial()
        self.scenes = SceneManager()
        self.scenes.switch_to(
            MainGameScene(
                self.state,
                background_image=self.background_image,
                fonts=self.fonts,
            ),
        )
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        """Update the active scene."""
        current_scene = self.scenes.current
        settings_open = bool(
            getattr(current_scene, "settings_open", False),
        )
        active_screen = getattr(current_scene, "active_screen", "main")
        sub_screen_open = active_screen != "main"
        if pyxel.btnp(pyxel.KEY_ESCAPE) and not (
            settings_open or sub_screen_open
        ):
            pyxel.quit()
        self.scenes.update()

    def draw(self) -> None:
        """Draw the active scene."""
        self.scenes.draw()

    def _load_assets(self) -> None:
        assets_dir = Path(__file__).resolve().parent / "assets"
        pyxres_path = assets_dir / "mendels_greenhouse.pyxres"
        if pyxres_path.exists():
            pyxel.load(str(pyxres_path))

    def _load_background_image(self) -> pyxel.Image | None:
        background_path = self.assets_dir / "greenhouse_background_640x360.png"
        if not background_path.exists():
            return None

        image = pyxel.Image(WIDTH, HEIGHT)
        image.load(0, 0, str(background_path))
        return image


def run() -> None:
    """Start the game."""
    Game()


if __name__ == "__main__":
    run()
