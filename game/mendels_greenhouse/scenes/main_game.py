"""Main gameplay scene for the MVP."""

from dataclasses import dataclass

import pyxel

from mendels_greenhouse.core.genetics import Plant, expected_distribution
from mendels_greenhouse.services.breeding_service import BreedingService
from mendels_greenhouse.state.game_state import BATCH_SIZE, GameState
from mendels_greenhouse.ui.components import (
    Rect,
    clicked,
    draw_button,
    draw_panel,
)
from mendels_greenhouse.ui.fonts import (
    FontSet,
    draw_outlined_text,
    draw_shadow_text,
)
from mendels_greenhouse.ui.palette import PyxelColor

WIDTH = 640
HEIGHT = 360
TOP_BAR_H = 66
PROBABILITY_PANEL_MAX_Y = 166

CROSS_BUTTON = Rect(267, 158, 106, 22)
REVEAL_BUTTON = Rect(506, 322, 58, 24)
STORE_BUTTON = Rect(570, 322, 58, 24)
PARENT_A_CARD = Rect(166, 120, 128, 68)
PARENT_B_CARD = Rect(346, 120, 128, 68)
COLLECTION_NAV_BUTTON = Rect(350, 5, 60, 56)
GARDEN_NAV_BUTTON = Rect(420, 5, 60, 56)
SHOP_NAV_BUTTON = Rect(490, 5, 60, 56)
SETTINGS_NAV_BUTTON = Rect(560, 5, 60, 56)
SETTINGS_BACK_BUTTON = Rect(272, 282, 96, 24)
SCENE_BACK_BUTTON = Rect(516, 318, 92, 24)
LANGUAGE_BUTTON = Rect(338, 112, 86, 20)
MUSIC_DOWN_BUTTON = Rect(338, 151, 20, 18)
MUSIC_UP_BUTTON = Rect(404, 151, 20, 18)
SOUND_DOWN_BUTTON = Rect(338, 194, 20, 18)
SOUND_UP_BUTTON = Rect(404, 194, 20, 18)
MUSIC_MUTE_CHECKBOX = Rect(468, 151, 12, 12)
SOUND_MUTE_CHECKBOX = Rect(468, 194, 12, 12)

PLANT_SPRITES = {
    ("yellow", "smooth"): (0, 0),
    ("yellow", "wrinkled"): (64, 0),
    ("green", "smooth"): (128, 0),
    ("green", "wrinkled"): (192, 0),
}
PLANT_SPRITE_W = 56
PLANT_SPRITE_H = 44
NAV_ICON_SIZE = 64
NAV_ICON_SCALE = 0.5
NAV_ICONS = {
    "COLECAO": (0, 64),
    "JARDIM": (64, 64),
    "LOJA": (128, 64),
    "CONFIG.": (192, 64),
}
SCREEN_MAIN = "main"
SCREEN_COLLECTION = "collection"
SCREEN_GARDEN = "garden"
SCREEN_SHOP = "shop"
COLLECTION_TABS = ("Species", "Phenotypes", "Genotypes")
GREENHOUSE_COLUMNS = 5
GREENHOUSE_ROWS = 4
GREENHOUSE_SLOT_SIZE = 44
GREENHOUSE_EXPANSION_COSTS = {
    5: 50,
    6: 75,
    7: 100,
    8: 125,
    9: 150,
    10: 200,
    11: 250,
    12: 300,
    13: 400,
    14: 500,
    15: 600,
    16: 700,
    17: 850,
    18: 1000,
    19: 1200,
    20: 1500,
}
ANALYZER_UPGRADES = {
    2: ("Genetic Sequencing", 500),
    3: ("Probabilistic Analysis", 2000),
    4: ("Genetic Simulator", 5000),
}
SPECIES_UNLOCKS = {
    "Snapdragon": (3, 3000),
    "Corn": (4, 10000),
}

AUTO_REVEAL_INTERVAL = 18
BUTTON_PRESS_FRAMES = 7
CONVEYOR_START_X = 68
CONVEYOR_SLOT_WIDTH = 38
CONVEYOR_ENTRANCE_X = 44
CONVEYOR_BELT_SPEED = 3
MUSIC_CHANNELS = (0, 1)
SOUND_CHANNEL = 3
MAX_VOLUME_STEP = 10


@dataclass
class SettingsState:
    """Runtime-only player preferences for the MVP settings panel."""

    language: str = "pt-BR"
    music_volume: int = 7
    sound_volume: int = 7
    music_muted: bool = False
    sound_muted: bool = False

    @property
    def music_gain(self) -> float:
        """Return normalized music gain for Pyxel channels."""
        return 0.0 if self.music_muted else self.music_volume / MAX_VOLUME_STEP

    @property
    def sound_gain(self) -> float:
        """Return normalized sound-effect gain for Pyxel channels."""
        return 0.0 if self.sound_muted else self.sound_volume / MAX_VOLUME_STEP


class MainGameScene:
    """Mouse-first main game scene with keyboard alternatives."""

    def __init__(
        self,
        state: GameState,
        *,
        background_image: pyxel.Image | None = None,
        fonts: FontSet | None = None,
    ) -> None:
        self.state = state
        self.breeding = BreedingService(state)
        self.background_image = background_image
        self.fonts = fonts
        self.cross_button_timer = 0
        self.reveal_button_timer = 0
        self.store_button_timer = 0
        self._reveal_frames = {}
        self.settings_open = False
        self.settings = SettingsState()
        self.active_screen = SCREEN_MAIN
        self.collection_tab = "Species"
        self.selected_greenhouse_slot = 0
        self.selected_shop_item = "slot"
        self._apply_audio_settings()

    def update(self) -> None:
        """Handle mouse-first controls and keyboard shortcuts."""
        self._tick_button_timers()
        if self.settings_open:
            self._update_settings_panel()
            return

        if self._update_top_navigation():
            return

        if self.active_screen == SCREEN_COLLECTION:
            self._update_collection_screen()
            return
        if self.active_screen == SCREEN_GARDEN:
            self._update_garden_screen()
            return
        if self.active_screen == SCREEN_SHOP:
            self._update_shop_screen()
            return

        self._update_main_game()

    def _update_main_game(self) -> None:
        """Handle main crossbreeding screen controls."""
        if clicked(SETTINGS_NAV_BUTTON):
            self._play_sound(0)
            self.settings_open = True
            return

        should_auto_reveal = (
            self.state.current_batch
            and pyxel.frame_count % AUTO_REVEAL_INTERVAL == 0
        )
        if should_auto_reveal:
            self.breeding.reveal_next()

        if clicked(CROSS_BUTTON) or pyxel.btnp(pyxel.KEY_RETURN):
            self._play_sound(1)
            self.cross_button_timer = BUTTON_PRESS_FRAMES
            self.breeding.start_crossbreeding()

        if clicked(REVEAL_BUTTON) or pyxel.btnp(pyxel.KEY_SPACE):
            self._play_sound(2)
            self.reveal_button_timer = BUTTON_PRESS_FRAMES
            self.breeding.reveal_next()

        if clicked(STORE_BUTTON) or pyxel.btnp(pyxel.KEY_S):
            self._play_sound(0)
            self.store_button_timer = BUTTON_PRESS_FRAMES
            self.breeding.store_last_revealed()

        if clicked(PARENT_A_CARD) or pyxel.btnp(pyxel.KEY_1):
            self._play_sound(0)
            self.state.selected_parent_a = 0
            self.state.status_message = "Parent A selected from slot 1."

        if clicked(PARENT_B_CARD) or pyxel.btnp(pyxel.KEY_2):
            self._play_sound(0)
            self.state.selected_parent_b = 1
            self.state.status_message = "Parent B selected from slot 2."

        # Track when each plant index is revealed
        if not hasattr(self, "_reveal_frames"):
            self._reveal_frames = {}
        current_visible = self.state.visible_count
        if current_visible < len(self._reveal_frames):
            self._reveal_frames.clear()
        for index in range(current_visible):
            if index not in self._reveal_frames:
                self._reveal_frames[index] = pyxel.frame_count

    def draw(self) -> None:
        """Draw the main game screen."""
        self._draw_greenhouse_background()
        self._draw_top_bar()
        if self.active_screen == SCREEN_COLLECTION:
            self._draw_collection_screen()
        elif self.active_screen == SCREEN_GARDEN:
            self._draw_garden_screen()
        elif self.active_screen == SCREEN_SHOP:
            self._draw_shop_screen()
        else:
            self._draw_main_game_screen()
        if self.settings_open:
            self._draw_settings_panel()

    def _draw_main_game_screen(self) -> None:
        self._draw_contract_panel()
        self._draw_probability_panel()
        self._draw_parent_card(PARENT_A_CARD, "PARENT A", self.state.parent_a)
        self._draw_parent_card(PARENT_B_CARD, "PARENT B", self.state.parent_b)
        draw_shadow_text(
            316,
            112,
            "+",
            PyxelColor.ACCENT,
            font=self._display_font,
        )
        draw_button(
            CROSS_BUTTON,
            "CROSS PLANTS",
            enabled=self.state.can_crossbreed,
            pressed=self.cross_button_timer > 0,
        )
        self._draw_conveyor()
        self._draw_bottom_panels()

    def _update_top_navigation(self) -> bool:
        if clicked(COLLECTION_NAV_BUTTON):
            self._play_sound(0)
            self.active_screen = SCREEN_COLLECTION
            return True
        if clicked(GARDEN_NAV_BUTTON):
            self._play_sound(0)
            self.active_screen = SCREEN_GARDEN
            return True
        if clicked(SHOP_NAV_BUTTON):
            self._play_sound(0)
            self.active_screen = SCREEN_SHOP
            return True
        if clicked(SETTINGS_NAV_BUTTON):
            self._play_sound(0)
            self.settings_open = True
            return True
        return False

    def _update_collection_screen(self) -> None:
        if clicked(SCENE_BACK_BUTTON) or pyxel.btnp(pyxel.KEY_ESCAPE):
            self._play_sound(0)
            self.active_screen = SCREEN_MAIN
            return
        for index, tab in enumerate(COLLECTION_TABS):
            if clicked(Rect(24, 108 + index * 30, 104, 22)):
                self._play_sound(0)
                self.collection_tab = tab

    def _update_garden_screen(self) -> None:
        if clicked(SCENE_BACK_BUTTON) or pyxel.btnp(pyxel.KEY_ESCAPE):
            self._play_sound(0)
            self.active_screen = SCREEN_MAIN
            return
        for index in range(GREENHOUSE_COLUMNS * GREENHOUSE_ROWS):
            slot_rect = self._greenhouse_slot_rect(index)
            if clicked(slot_rect):
                self._play_sound(0)
                self.selected_greenhouse_slot = index
                return

        selected = self._selected_greenhouse_plant()
        if selected is None:
            return
        if clicked(Rect(392, 183, 96, 22)):
            self._play_sound(0)
            self.state.selected_parent_a = self.selected_greenhouse_slot
            self.state.status_message = "Parent A selected from garden."
        if clicked(Rect(392, 211, 96, 22)):
            self._play_sound(0)
            self.state.selected_parent_b = self.selected_greenhouse_slot
            self.state.status_message = "Parent B selected from garden."

    def _update_shop_screen(self) -> None:
        if clicked(SCENE_BACK_BUTTON) or pyxel.btnp(pyxel.KEY_ESCAPE):
            self._play_sound(0)
            self.active_screen = SCREEN_MAIN
            return
        for item, rect in [
            ("slot", Rect(36, 120, 170, 42)),
            ("analyzer", Rect(234, 120, 170, 42)),
            ("species", Rect(432, 120, 170, 42)),
        ]:
            if clicked(rect):
                self._play_sound(0)
                self.selected_shop_item = item
                return
        if clicked(Rect(392, 284, 96, 24)):
            self._buy_selected_shop_item()

    def _draw_greenhouse_background(self) -> None:
        if self.background_image is not None:
            pyxel.blt(0, 0, self.background_image, 0, 0, WIDTH, HEIGHT)
            return

        pyxel.cls(PyxelColor.GREENHOUSE_BG)
        for x in range(0, WIDTH, 32):
            pyxel.line(x, 30, x - 40, 180, PyxelColor.TEXT_MUTED)
            pyxel.line(x, 30, x + 40, 180, PyxelColor.FIELD)

        pyxel.rect(0, 258, WIDTH, 102, PyxelColor.PANEL_DARK)
        for x in range(0, WIDTH, 16):
            pyxel.line(x, 258, x + 8, HEIGHT, PyxelColor.FRAME)

    def _draw_top_bar(self) -> None:
        self._draw_runtime_hud_frame(5, 4, 430, 58)
        self._draw_runtime_logo(16, 10)
        draw_outlined_text(
            24,
            13,
            "MENDEL'S",
            PyxelColor.PEA_GREEN,
            font=self._display_font,
        )
        draw_outlined_text(
            20,
            24,
            "GREENHOUSE",
            PyxelColor.ACCENT,
            font=self._display_font,
        )
        self._draw_counter(118, "CR", str(self.state.credits))
        garden = f"{self.state.greenhouse.used_slots}/"
        garden += f"{self.state.greenhouse.capacity}"
        self._draw_counter(198, "GDN", garden)

        nav_x = 350
        self._draw_runtime_hud_frame(nav_x - 7, 4, 290, 58)
        for index, (label, sprite) in enumerate(NAV_ICONS.items()):
            self._draw_nav_item(nav_x + index * 70, 9, label, sprite)

    def _draw_runtime_hud_frame(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> None:
        pyxel.rect(x, y, width, height, PyxelColor.PANEL_DARK)
        pyxel.rectb(x, y, width, height, PyxelColor.SPRITE_OUTLINE)
        pyxel.rectb(x + 2, y + 2, width - 4, height - 4, PyxelColor.FRAME)
        for line_y in range(y + 10, y + height - 6, 9):
            pyxel.line(
                x + 4,
                line_y,
                x + width - 5,
                line_y,
                PyxelColor.DARK_WOOD,
            )
        for corner_x in [x + 3, x + width - 4]:
            pyxel.pset(corner_x, y + 3, PyxelColor.ACCENT)
            pyxel.pset(corner_x, y + height - 4, PyxelColor.ACCENT)

    def _draw_runtime_logo(self, x: int, y: int) -> None:
        pyxel.rect(x, y + 2, 34, 30, PyxelColor.DARK_WOOD)
        pyxel.rectb(x, y + 2, 34, 30, PyxelColor.SPRITE_OUTLINE)
        pyxel.line(x + 5, y + 8, x + 18, y + 4, PyxelColor.POD_HIGHLIGHT)
        pyxel.line(x + 5, y + 22, x + 18, y + 29, PyxelColor.POD_SHADOW)
        pyxel.circ(x + 12, y + 17, 7, PyxelColor.SEED_GOLD)
        pyxel.circb(x + 12, y + 17, 7, PyxelColor.SPRITE_OUTLINE)
        pyxel.circ(x + 23, y + 16, 7, PyxelColor.PEA_GREEN)
        pyxel.circb(x + 23, y + 16, 7, PyxelColor.SPRITE_OUTLINE)

    def _draw_nav_item(
        self,
        x: int,
        y: int,
        label: str,
        sprite: tuple[int, int],
    ) -> None:
        u, v = sprite
        pyxel.blt(
            x + 14,
            y,
            0,
            u,
            v,
            NAV_ICON_SIZE,
            NAV_ICON_SIZE,
            colkey=0,
            scale=NAV_ICON_SCALE,
        )
        text_x = x + 30 - len(label) * 2
        pyxel.text(text_x + 1, y + 40, label, PyxelColor.SPRITE_OUTLINE)
        pyxel.text(text_x, y + 39, label, PyxelColor.PARCHMENT_LIGHT)

    def _draw_counter(self, x: int, icon: str, value: str) -> None:
        pyxel.rect(x, 41, 72, 14, PyxelColor.UI_DARK)
        pyxel.rectb(x, 41, 72, 14, PyxelColor.FRAME)
        pyxel.text(x + 5, 46, icon, PyxelColor.ACCENT)
        pyxel.text(x + 27, 46, value, PyxelColor.TEXT)

    def _draw_contract_panel(self) -> None:
        contract = self.state.active_contract
        rect = Rect(180, 74, 320, 46)
        draw_panel(rect)
        draw_outlined_text(
            272,
            66,
            "CURRENT CONTRACT",
            PyxelColor.ACCENT,
            font=self._display_font,
        )
        pyxel.text(
            rect.x + 12,
            rect.y + 12,
            contract.title,
            PyxelColor.UI_DARK,
        )
        pyxel.rect(rect.x + 12, rect.y + 29, 235, 8, PyxelColor.BAR_EMPTY)
        progress_width = int(
            235 * contract.delivered_count / contract.target_count,
        )
        pyxel.rect(
            rect.x + 12,
            rect.y + 29,
            progress_width,
            8,
            PyxelColor.PROGRESS,
        )
        progress = f"{contract.delivered_count}/{contract.target_count}"
        pyxel.text(rect.x + 260, rect.y + 30, progress, PyxelColor.UI_DARK)

    def _draw_probability_panel(self) -> None:
        rect = Rect(12, 74, 132, 112)
        draw_panel(rect)
        draw_outlined_text(
            18,
            80,
            "PROBABILITIES",
            PyxelColor.ACCENT,
            font=self._display_font,
        )
        parent_a = self.state.parent_a
        parent_b = self.state.parent_b
        if parent_a is None or parent_b is None:
            pyxel.text(18, 96, "Select parents", PyxelColor.UI_DARK)
            return

        distribution = expected_distribution(parent_a, parent_b)
        y = 94
        for genotype, probability in distribution.probabilities.items():
            chance = int(probability * 100)
            pyxel.text(18, y, f"{genotype}: {chance}%", PyxelColor.UI_DARK)
            y += 10
            if y > PROBABILITY_PANEL_MAX_Y:
                break

    def _draw_parent_card(
        self,
        rect: Rect,
        title: str,
        plant: Plant | None,
    ) -> None:
        draw_panel(rect)
        draw_outlined_text(
            rect.x + 32,
            rect.y + 7,
            title,
            PyxelColor.ACCENT,
            font=self._display_font,
        )
        if plant is None:
            pyxel.text(
                rect.x + 20,
                rect.y + 28,
                "Empty slot",
                PyxelColor.UI_DARK,
            )
            return

        self._draw_plant_preview(rect.x + 32, rect.y + 64, plant, large=True)
        pyxel.rect(rect.x + 65, rect.y + 25, 46, 15, PyxelColor.FIELD)
        pyxel.rectb(rect.x + 65, rect.y + 25, 46, 15, PyxelColor.FRAME)
        pyxel.text(
            rect.x + 73,
            rect.y + 30,
            plant.genotype,
            PyxelColor.UI_DARK,
        )
        phenotype = plant.phenotype
        pyxel.text(
            rect.x + 65,
            rect.y + 47,
            phenotype.seed_color,
            PyxelColor.UI_DARK,
        )

    def _draw_conveyor(self) -> None:
        pyxel.rect(44, 194, 552, 58, PyxelColor.CONVEYOR)
        pyxel.rectb(44, 194, 552, 58, PyxelColor.FRAME)
        pyxel.rectb(45, 195, 550, 56, PyxelColor.UI_DARK)
        pyxel.rect(230, 182, 180, 14, PyxelColor.UI_DARK)

        # Center status message dynamically inside the status box
        msg = self.state.status_message[:44]
        text_width = len(msg) * 4
        text_x = 320 - text_width // 2
        pyxel.text(text_x, 187, msg, PyxelColor.ACCENT)
        # Conveyor belt itself moves to the RIGHT (from left to right)
        belt_offset = (pyxel.frame_count * CONVEYOR_BELT_SPEED) % 16
        for x in range(52 + belt_offset, 592, 16):
            pyxel.line(x, 248, x + 8, 248, PyxelColor.TEXT_MUTED)
            pyxel.circ(x + 4, 250, 3, PyxelColor.UI_DARK)
            pyxel.circb(x + 4, 250, 3, PyxelColor.TEXT_MUTED)

        # Draw visible plants, sliding them smoothly from the left entrance
        visible = self.state.current_batch[: self.state.visible_count]
        reveal_frames = getattr(self, "_reveal_frames", {})
        for index, plant in enumerate(visible[:14]):
            reveal_frame = reveal_frames.get(index, 0)
            age = pyxel.frame_count - reveal_frame
            final_x = CONVEYOR_START_X + index * CONVEYOR_SLOT_WIDTH

            if reveal_frame > 0:
                # Travel at the same speed as the conveyor belt
                conveyor_x = min(
                    final_x,
                    CONVEYOR_ENTRANCE_X + age * CONVEYOR_BELT_SPEED,
                )
            else:
                conveyor_x = final_x

            self._draw_plant_preview(conveyor_x, 238, plant)

    def _draw_bottom_panels(self) -> None:
        self._draw_stats_panel()
        self._draw_last_plant_panel()
        self._draw_help_panel()
        draw_button(
            REVEAL_BUTTON,
            "REVEAL",
            pressed=self.reveal_button_timer > 0,
        )
        draw_button(
            STORE_BUTTON,
            "STORE",
            pressed=self.store_button_timer > 0,
        )

    def _draw_stats_panel(self) -> None:
        rect = Rect(12, 264, 136, 84)
        draw_panel(rect)
        draw_outlined_text(
            18,
            270,
            "GENERATION",
            PyxelColor.ACCENT,
            font=self._display_font,
        )
        pyxel.text(
            24,
            286,
            f"Generated: {self.state.visible_count}/{BATCH_SIZE}",
            PyxelColor.UI_DARK,
        )
        contract = self.state.active_contract
        pyxel.text(
            24,
            300,
            f"Matches: {contract.delivered_count}",
            PyxelColor.UI_DARK,
        )
        pyxel.text(
            24,
            314,
            f"Missing: {contract.remaining_count}",
            PyxelColor.UI_DARK,
        )

    def _draw_last_plant_panel(self) -> None:
        rect = Rect(160, 264, 150, 84)
        draw_panel(rect)
        draw_outlined_text(
            166,
            270,
            "LAST PLANT",
            PyxelColor.ACCENT,
            font=self._display_font,
        )
        plant = self.state.last_visible_plant
        if plant is None:
            pyxel.text(178, 296, "Reveal offspring", PyxelColor.UI_DARK)
            return

        self._draw_plant_preview(190, 334, plant, large=True)
        phenotype = plant.phenotype
        pyxel.text(226, 288, plant.genotype, PyxelColor.UI_DARK)
        pyxel.text(226, 302, phenotype.seed_color, PyxelColor.UI_DARK)
        pyxel.text(226, 316, phenotype.seed_texture, PyxelColor.UI_DARK)

    def _draw_help_panel(self) -> None:
        rect = Rect(322, 264, 170, 84)
        draw_panel(rect)
        draw_outlined_text(
            328,
            270,
            "HOW IT WORKS",
            PyxelColor.ACCENT,
            font=self._display_font,
        )
        pyxel.text(334, 284, "Each parent gives", PyxelColor.UI_DARK)
        pyxel.text(334, 296, "one allele per gene.", PyxelColor.UI_DARK)
        pyxel.text(334, 308, "Results are shuffled", PyxelColor.UI_DARK)
        pyxel.text(334, 320, "before the conveyor.", PyxelColor.UI_DARK)

    def _draw_collection_screen(self) -> None:
        self._draw_scene_shell("COLLECTION", "Discovered genetic records")
        pyxel.text(
            470,
            86,
            f"Discovered: {self.state.collection.total_entries}",
            PyxelColor.PARCHMENT_LIGHT,
        )
        for index, tab in enumerate(COLLECTION_TABS):
            rect = Rect(24, 108 + index * 30, 104, 22)
            active = self.collection_tab == tab
            draw_button(rect, tab.upper(), pressed=active)

        list_panel = Rect(148, 108, 220, 178)
        detail_panel = Rect(386, 108, 222, 178)
        draw_panel(list_panel)
        draw_panel(detail_panel)
        entries = self._collection_entries()
        if not entries:
            pyxel.text(166, 132, "No discoveries yet.", PyxelColor.UI_DARK)
        for index, line in enumerate(entries[:12]):
            y = 122 + index * 12
            pyxel.text(164, y, line[:44], PyxelColor.UI_DARK)

        pyxel.text(402, 126, self.collection_tab.upper(), PyxelColor.UI_DARK)
        details = self._collection_details(entries)
        for index, line in enumerate(details):
            pyxel.text(402, 146 + index * 14, line, PyxelColor.UI_DARK)
        self._draw_scene_back_button()

    def _draw_garden_screen(self) -> None:
        self._draw_scene_shell("GARDEN", "Stored plants and parent selection")
        pyxel.text(
            476,
            86,
            f"Slots: {self.state.greenhouse.used_slots}/20",
            PyxelColor.PARCHMENT_LIGHT,
        )
        grid_panel = Rect(24, 104, 294, 214)
        detail_panel = Rect(338, 104, 270, 178)
        draw_panel(grid_panel)
        draw_panel(detail_panel)
        for index in range(GREENHOUSE_COLUMNS * GREENHOUSE_ROWS):
            self._draw_greenhouse_slot(index)

        selected = self._selected_greenhouse_plant()
        pyxel.text(354, 122, "SELECTED PLANT", PyxelColor.UI_DARK)
        if selected is None:
            pyxel.text(354, 146, "Empty or locked slot.", PyxelColor.UI_DARK)
        else:
            phenotype = selected.phenotype
            self._draw_plant_preview(382, 205, selected, large=True)
            pyxel.text(
                428,
                146,
                f"Genotype: {selected.genotype}",
                PyxelColor.UI_DARK,
            )
            pyxel.text(
                428,
                160,
                f"Color: {phenotype.seed_color}",
                PyxelColor.UI_DARK,
            )
            pyxel.text(
                428,
                174,
                f"Texture: {phenotype.seed_texture}",
                PyxelColor.UI_DARK,
            )
            draw_button(Rect(392, 183, 96, 22), "PARENT A")
            draw_button(Rect(392, 211, 96, 22), "PARENT B")
        self._draw_scene_back_button()

    def _draw_shop_screen(self) -> None:
        self._draw_scene_shell("SHOP", "Spend credits on progression")
        pyxel.text(
            510,
            86,
            f"Credits: {self.state.credits}",
            PyxelColor.PARCHMENT_LIGHT,
        )
        self._draw_shop_card("slot", Rect(36, 120, 170, 42))
        self._draw_shop_card("analyzer", Rect(234, 120, 170, 42))
        self._draw_shop_card("species", Rect(432, 120, 170, 42))

        details_panel = Rect(88, 198, 464, 100)
        draw_panel(details_panel)
        for index, line in enumerate(self._shop_details()):
            pyxel.text(108, 216 + index * 14, line, PyxelColor.UI_DARK)
        draw_button(
            Rect(392, 284, 96, 24),
            "BUY",
            enabled=self._selected_shop_available(),
        )
        self._draw_scene_back_button()

    def _draw_scene_shell(self, title: str, subtitle: str) -> None:
        draw_outlined_text(
            24,
            76,
            title,
            PyxelColor.ACCENT,
            font=self._display_font,
        )
        pyxel.text(26, 91, subtitle, PyxelColor.PARCHMENT_LIGHT)

    def _draw_scene_back_button(self) -> None:
        draw_button(SCENE_BACK_BUTTON, "BACK")

    def _draw_greenhouse_slot(self, index: int) -> None:
        rect = self._greenhouse_slot_rect(index)
        unlocked = index < self.state.greenhouse.capacity
        selected = index == self.selected_greenhouse_slot
        fill = PyxelColor.PARCHMENT if unlocked else PyxelColor.TEXT_MUTED
        if selected:
            fill = PyxelColor.ACCENT
        pyxel.rect(rect.x, rect.y, rect.width, rect.height, fill)
        pyxel.rectb(rect.x, rect.y, rect.width, rect.height, PyxelColor.FRAME)
        pyxel.rectb(
            rect.x + 1,
            rect.y + 1,
            rect.width - 2,
            rect.height - 2,
            PyxelColor.UI_DARK,
        )
        if not unlocked:
            pyxel.text(rect.x + 13, rect.y + 19, "LOCK", PyxelColor.UI_DARK)
            return
        plant = self.state.greenhouse.slots[index]
        if plant is None:
            pyxel.text(rect.x + 14, rect.y + 19, "EMPTY", PyxelColor.UI_DARK)
            return
        self._draw_plant_preview(rect.x + 22, rect.y + 42, plant)

    def _draw_shop_card(self, item: str, rect: Rect) -> None:
        selected = self.selected_shop_item == item
        fill = PyxelColor.ACCENT if selected else PyxelColor.PARCHMENT
        pyxel.rect(rect.x, rect.y, rect.width, rect.height, fill)
        pyxel.rectb(rect.x, rect.y, rect.width, rect.height, PyxelColor.FRAME)
        title, cost, status = self._shop_card_data(item)
        pyxel.text(rect.x + 8, rect.y + 9, title, PyxelColor.UI_DARK)
        pyxel.text(rect.x + 8, rect.y + 23, cost, PyxelColor.UI_DARK)
        pyxel.text(rect.x + 92, rect.y + 23, status, PyxelColor.UI_DARK)

    def _greenhouse_slot_rect(self, index: int) -> Rect:
        col = index % GREENHOUSE_COLUMNS
        row = index // GREENHOUSE_COLUMNS
        return Rect(
            38 + col * 54,
            118 + row * 46,
            GREENHOUSE_SLOT_SIZE,
            GREENHOUSE_SLOT_SIZE,
        )

    def _selected_greenhouse_plant(self) -> Plant | None:
        if self.selected_greenhouse_slot >= self.state.greenhouse.capacity:
            return None
        return self.state.greenhouse.plant_at(self.selected_greenhouse_slot)

    def _collection_entries(self) -> list[str]:
        collection = self.state.collection
        if self.collection_tab == "Species":
            entries = sorted(collection.species)
            return [f"{name} - discovered" for name in entries]
        if self.collection_tab == "Phenotypes":
            entries = sorted(collection.phenotypes)
            return [f"{color} / {texture}" for color, texture in entries]
        return sorted(collection.genotypes)

    def _collection_details(self, entries: list[str]) -> list[str]:
        if self.collection_tab == "Species":
            return [
                "Mendel Pea unlocked.",
                f"Species found: {len(self.state.collection.species)}",
                "Next species unlock in shop.",
            ]
        if self.collection_tab == "Phenotypes":
            return [
                f"Phenotypes found: {len(entries)}",
                "Seed color + texture.",
                "Hidden entries stay unknown.",
            ]
        return [
            f"Genotypes found: {len(entries)}",
            "Generated offspring register here.",
            "Analyzer upgrades reveal more data.",
        ]

    def _shop_card_data(self, item: str) -> tuple[str, str, str]:
        if item == "slot":
            next_slot = self.state.greenhouse.capacity + 1
            if next_slot not in GREENHOUSE_EXPANSION_COSTS:
                return ("Greenhouse slot", "Max capacity", "DONE")
            cost = GREENHOUSE_EXPANSION_COSTS[next_slot]
            return (
                f"Slot {next_slot}",
                f"{cost} CR",
                self._afford_label(cost),
            )
        if item == "analyzer":
            next_level = self.state.analyzer_level + 1
            if next_level not in ANALYZER_UPGRADES:
                return ("Analyzer", "Max level", "DONE")
            _name, cost = ANALYZER_UPGRADES[next_level]
            return (
                f"Analyzer L{next_level}",
                f"{cost} CR",
                self._afford_label(cost),
            )

        species_name, (_genes, cost) = self._next_species_unlock()
        if species_name is None:
            return ("Species", "All unlocked", "DONE")
        return (species_name, f"{cost} CR", self._afford_label(cost))

    def _shop_details(self) -> list[str]:
        if self.selected_shop_item == "slot":
            next_slot = self.state.greenhouse.capacity + 1
            cost = GREENHOUSE_EXPANSION_COSTS.get(next_slot)
            if cost is None:
                return ["Greenhouse is already at maximum capacity."]
            return [
                f"Unlock greenhouse slot {next_slot}.",
                "More slots let you store more offspring.",
                f"Cost: {cost} credits.",
            ]
        if self.selected_shop_item == "analyzer":
            next_level = self.state.analyzer_level + 1
            upgrade = ANALYZER_UPGRADES.get(next_level)
            if upgrade is None:
                return ["Genetic Analyzer is already fully upgraded."]
            name, cost = upgrade
            return [
                f"Upgrade to level {next_level}: {name}.",
                "Unlocks deeper genetic information.",
                f"Cost: {cost} credits.",
            ]
        species_name, data = self._next_species_unlock()
        if species_name is None or data is None:
            return ["All currently specified species are unlocked."]
        genes, cost = data
        return [
            f"Unlock {species_name}.",
            f"Adds a {genes}-gene plant species.",
            f"Cost: {cost} credits.",
        ]

    def _buy_selected_shop_item(self) -> None:
        if self.selected_shop_item == "slot":
            self._buy_greenhouse_slot()
            return

        if self.selected_shop_item == "analyzer":
            self._buy_analyzer_upgrade()
            return

        self._buy_species_unlock()

    def _buy_greenhouse_slot(self) -> None:
        next_slot = self.state.greenhouse.capacity + 1
        cost = GREENHOUSE_EXPANSION_COSTS.get(next_slot)
        if cost is None:
            self.state.status_message = "Greenhouse is already maxed."
            return
        if not self._spend_credits(cost):
            return
        self.state.greenhouse.expand()
        self.state.status_message = f"Unlocked greenhouse slot {next_slot}."
        self._play_sound(3)

    def _buy_analyzer_upgrade(self) -> None:
        next_level = self.state.analyzer_level + 1
        upgrade = ANALYZER_UPGRADES.get(next_level)
        if upgrade is None:
            self.state.status_message = "Analyzer is already maxed."
            return
        _name, cost = upgrade
        if not self._spend_credits(cost):
            return
        self.state.analyzer_level = next_level
        self.state.status_message = f"Analyzer upgraded to level {next_level}."
        self._play_sound(3)

    def _buy_species_unlock(self) -> None:
        species_name, data = self._next_species_unlock()
        if species_name is None or data is None:
            self.state.status_message = "All specified species are unlocked."
            return
        _genes, cost = data
        if not self._spend_credits(cost):
            return
        self.state.unlocked_species.add(species_name)
        self.state.collection.register_species(species_name)
        self.state.status_message = f"Unlocked {species_name}."
        self._play_sound(3)

    def _selected_shop_available(self) -> bool:
        _title, cost_text, status = self._shop_card_data(
            self.selected_shop_item,
        )
        return status == "BUY" and cost_text.endswith("CR")

    def _spend_credits(self, cost: int) -> bool:
        if self.state.credits < cost:
            self.state.status_message = "Not enough credits."
            self._play_sound(4)
            return False
        self.state.credits -= cost
        return True

    def _afford_label(self, cost: int) -> str:
        return "BUY" if self.state.credits >= cost else "LOCK"

    def _next_species_unlock(
        self,
    ) -> tuple[str | None, tuple[int, int] | None]:
        for species_name, data in SPECIES_UNLOCKS.items():
            if species_name not in self.state.unlocked_species:
                return species_name, data
        return None, None

    def _draw_plant_preview(
        self,
        x: int,
        y: int,
        plant: Plant,
        *,
        large: bool = False,
    ) -> None:
        phenotype = plant.phenotype
        u, v = PLANT_SPRITES[(phenotype.seed_color, phenotype.seed_texture)]
        vertical_nudge = 2 if large else 0
        pyxel.blt(
            x - PLANT_SPRITE_W // 2,
            y - PLANT_SPRITE_H - vertical_nudge,
            0,
            u,
            v,
            PLANT_SPRITE_W,
            PLANT_SPRITE_H,
            colkey=0,
        )

    def _update_settings_panel(self) -> None:
        if clicked(SETTINGS_BACK_BUTTON) or pyxel.btnp(pyxel.KEY_ESCAPE):
            self._play_sound(0)
            self.settings_open = False
            return

        if clicked(LANGUAGE_BUTTON):
            self._play_sound(0)
            self.settings.language = (
                "en" if self.settings.language == "pt-BR" else "pt-BR"
            )

        if clicked(MUSIC_DOWN_BUTTON):
            self._play_sound(0)
            self.settings.music_volume = max(
                self.settings.music_volume - 1,
                0,
            )
            self._apply_audio_settings()
        if clicked(MUSIC_UP_BUTTON):
            self._play_sound(0)
            self.settings.music_volume = min(
                self.settings.music_volume + 1,
                MAX_VOLUME_STEP,
            )
            self._apply_audio_settings()
        if clicked(SOUND_DOWN_BUTTON):
            self._play_sound(0)
            self.settings.sound_volume = max(
                self.settings.sound_volume - 1,
                0,
            )
            self._apply_audio_settings()
        if clicked(SOUND_UP_BUTTON):
            self._play_sound(0)
            self.settings.sound_volume = min(
                self.settings.sound_volume + 1,
                MAX_VOLUME_STEP,
            )
            self._apply_audio_settings()

        if clicked(MUSIC_MUTE_CHECKBOX):
            self.settings.music_muted = not self.settings.music_muted
            self._apply_audio_settings()
            self._play_sound(0)
        if clicked(SOUND_MUTE_CHECKBOX):
            self.settings.sound_muted = not self.settings.sound_muted
            self._apply_audio_settings()
            self._play_sound(0)

    def _draw_settings_panel(self) -> None:
        pyxel.dither(0.65)
        pyxel.rect(0, 0, WIDTH, HEIGHT, PyxelColor.UI_DARK)
        pyxel.dither(1)

        panel = Rect(160, 70, 320, 242)
        draw_panel(panel)
        draw_outlined_text(
            254,
            84,
            self._settings_text("SETTINGS", "CONFIGURACOES"),
            PyxelColor.ACCENT,
            font=self._display_font,
        )
        pyxel.text(
            188,
            106,
            self._settings_text("Language", "Idioma"),
            PyxelColor.UI_DARK,
        )
        draw_button(LANGUAGE_BUTTON, self._language_label())

        self._draw_volume_control(
            143,
            self._settings_text("Music volume", "Volume musica"),
            self.settings.music_volume,
            (MUSIC_DOWN_BUTTON, MUSIC_UP_BUTTON),
        )
        self._draw_checkbox(
            MUSIC_MUTE_CHECKBOX,
            self.settings.music_muted,
            self._settings_text("Mute music", "Mutar musica"),
        )

        self._draw_volume_control(
            186,
            self._settings_text("Sound volume", "Volume sons"),
            self.settings.sound_volume,
            (SOUND_DOWN_BUTTON, SOUND_UP_BUTTON),
        )
        self._draw_checkbox(
            SOUND_MUTE_CHECKBOX,
            self.settings.sound_muted,
            self._settings_text("Mute sounds", "Mutar sons"),
        )

        pyxel.text(
            188,
            238,
            self._settings_text(
                "Changes apply immediately.",
                "Alteracoes aplicam na hora.",
            ),
            PyxelColor.UI_DARK,
        )
        draw_button(
            SETTINGS_BACK_BUTTON,
            self._settings_text("BACK", "VOLTAR"),
        )

    def _draw_volume_control(
        self,
        y: int,
        label: str,
        value: int,
        buttons: tuple[Rect, Rect],
    ) -> None:
        x = 188
        down_button, up_button = buttons
        pyxel.text(x, y, label, PyxelColor.UI_DARK)
        draw_button(down_button, "-")
        pyxel.rect(x + 176, y + 11, 40, 6, PyxelColor.BAR_EMPTY)
        pyxel.rect(x + 176, y + 11, value * 4, 6, PyxelColor.PROGRESS)
        pyxel.rectb(x + 176, y + 11, 40, 6, PyxelColor.UI_DARK)
        pyxel.text(x + 224, y + 9, f"{value * 10:3d}%", PyxelColor.UI_DARK)
        draw_button(up_button, "+")

    def _draw_checkbox(self, rect: Rect, checked: bool, label: str) -> None:
        pyxel.rect(rect.x, rect.y, rect.width, rect.height, PyxelColor.FIELD)
        pyxel.rectb(
            rect.x,
            rect.y,
            rect.width,
            rect.height,
            PyxelColor.UI_DARK,
        )
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

    def _language_label(self) -> str:
        if self.settings.language == "pt-BR":
            return "PT-BR"
        return "EN"

    def _settings_text(self, english: str, portuguese: str) -> str:
        if self.settings.language == "pt-BR":
            return portuguese
        return english

    def _apply_audio_settings(self) -> None:
        for channel in MUSIC_CHANNELS:
            pyxel.channels[channel].gain = self.settings.music_gain
        pyxel.channels[SOUND_CHANNEL].gain = self.settings.sound_gain

    def _play_sound(self, sound_index: int) -> None:
        if self.settings.sound_muted:
            return
        pyxel.play(SOUND_CHANNEL, sound_index)

    @property
    def _display_font(self) -> pyxel.Font | None:
        if self.fonts is None:
            return None
        return self.fonts.display

    def _tick_button_timers(self) -> None:
        self.cross_button_timer = max(self.cross_button_timer - 1, 0)
        self.reveal_button_timer = max(self.reveal_button_timer - 1, 0)
        self.store_button_timer = max(self.store_button_timer - 1, 0)
