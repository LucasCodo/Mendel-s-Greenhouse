"""Main gameplay scene for the MVP."""

from dataclasses import dataclass
from math import ceil, sqrt

import pyxel

from mendels_greenhouse.core.genetics import Plant, expected_distribution
from mendels_greenhouse.core.i18n import gettext_noop, set_language, t
from mendels_greenhouse.services.breeding_service import BreedingService
from mendels_greenhouse.services.greenhouse_service import GreenhouseService
from mendels_greenhouse.services.save_service import SaveService
from mendels_greenhouse.state.game_state import GameState
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
HARVEST_BUTTON = Rect(432, 322, 122, 24)
PARENT_A_CARD = Rect(166, 120, 128, 68)
PARENT_B_CARD = Rect(346, 120, 128, 68)
INTRO_OK_BUTTON = Rect(272, 294, 96, 24)
CLAIM_CONTRACT_BUTTON = Rect(420, 84, 64, 18)
PARENT_PICKER_CLOSE_BUTTON = Rect(492, 286, 76, 22)
GARDEN_DISCARD_BUTTON = Rect(446, 211, 80, 22)
SETTINGS_BACK_BUTTON = Rect(272, 282, 96, 24)
LANGUAGE_BUTTON = Rect(338, 112, 86, 20)
MUSIC_DOWN_BUTTON = Rect(338, 151, 20, 18)
MUSIC_UP_BUTTON = Rect(404, 151, 20, 18)
SOUND_DOWN_BUTTON = Rect(338, 194, 20, 18)
SOUND_UP_BUTTON = Rect(404, 194, 20, 18)
MUSIC_MUTE_CHECKBOX = Rect(468, 151, 12, 12)
SOUND_MUTE_CHECKBOX = Rect(468, 194, 12, 12)
NAV_RAIL = Rect(558, 70, 76, 276)
NAV_BUTTON_W = 64
NAV_BUTTON_H = 34
NAV_BUTTON_GAP = 4
NAV_BUTTON_X = 564
NAV_BUTTON_Y = 78

PLANT_SPRITES = {
    ("yellow", "smooth"): (0, 0),
    ("yellow", "wrinkled"): (64, 0),
    ("green", "smooth"): (128, 0),
    ("green", "wrinkled"): (192, 0),
}
PLANT_SPRITE_W = 56
PLANT_SPRITE_H = 44
NAV_ICON_SIZE = 64
NAV_ICON_SCALE = 0.25
SCREEN_MAIN = "main"
SCREEN_CONTRACTS = "contracts"
SCREEN_KNOWLEDGE = "knowledge"
SCREEN_COLLECTION = "collection"
SCREEN_GARDEN = "garden"
SCREEN_SHOP = "shop"
NAV_ITEMS = (
    (SCREEN_MAIN, "CROSS PLANTS", (0, 128)),
    (SCREEN_GARDEN, "Garden", (64, 64)),
    (SCREEN_CONTRACTS, "CONTRACT", (128, 128)),
    (SCREEN_KNOWLEDGE, "Knowledge", (0, 64)),
    (SCREEN_SHOP, "Shop", (128, 64)),
    (SCREEN_COLLECTION, "Collection", (64, 128)),
    ("settings", "Settings", (192, 64)),
)
COLLECTION_TABS = ("Species", "Phenotypes", "Genotypes")
KNOWLEDGE_STAGES = (
    ("Phenotype", ("Phenotype", "Dominant allele", "Recessive allele"), 1),
    (
        "Genotype",
        (
            "Allele pair",
            "Genotype",
            "Homozygous",
            "Heterozygous",
            "Allele segregation",
        ),
        2,
    ),
    (
        "Probability",
        (
            "Independent assortment",
            "9:3:3:1 dihybrid ratio",
            "Genetic probability",
        ),
        3,
    ),
    ("Genetic Planning", ("Genetic planning",), 4),
)
KNOWLEDGE_DETAILS = {
    "Phenotype": gettext_noop(
        "Visible traits are what you can observe on a plant.",
    ),
    "Dominant allele": gettext_noop(
        "A dominant allele can shape the visible trait when present.",
    ),
    "Recessive allele": gettext_noop(
        "A recessive allele appears only when no dominant allele masks it.",
    ),
    "Allele pair": gettext_noop(
        "Each gene is represented by two alleles, one from each parent.",
    ),
    "Genotype": gettext_noop(
        "A genotype records the allele pair for each tracked gene.",
    ),
    "Homozygous": gettext_noop(
        "A homozygous gene has two matching alleles.",
    ),
    "Heterozygous": gettext_noop(
        "A heterozygous gene has two different alleles.",
    ),
    "Allele segregation": gettext_noop(
        "Parents pass one allele from each gene to each offspring.",
    ),
    "Independent assortment": gettext_noop(
        "Different genes can be inherited independently.",
    ),
    "9:3:3:1 dihybrid ratio": gettext_noop(
        "AaBb x AaBb can produce four phenotype classes.",
    ),
    "Genetic probability": gettext_noop(
        "Expected percentages help plan before breeding.",
    ),
    "Genetic planning": gettext_noop(
        "Planning compares crosses against a target result.",
    ),
}
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

BUTTON_PRESS_FRAMES = 7
ANALYZER_GENOTYPE_LEVEL = 2
ANALYZER_PROBABILITY_LEVEL = 3
SEED_STAGE_FRAMES = 15
SEEDLING_STAGE_FRAMES = 30
GERMINATION_SETTLE_FRAMES = 90
MAX_BED_CELLS = 20
BED_MAX_COLUMNS = 5
BED_ORIGIN_X = 210
BED_ORIGIN_Y = 184
BED_MAX_W = 220
BED_MAX_H = 72
BED_CELL_W = 34
BED_CELL_H = 15
BED_GAP = 3
MUSIC_CHANNELS = (0, 1, 2)
SOUND_CHANNEL = 3
MAX_VOLUME_STEP = 10

I18N_MARKERS = (
    gettext_noop("Analyzer"),
    gettext_noop("Analyzer upgrades reveal more data."),
    gettext_noop("Analyzer is already maxed."),
    gettext_noop("Analyzer L{level}"),
    gettext_noop("Analyzer upgraded to level {level}."),
    gettext_noop("Adds a {genes}-gene plant species."),
    gettext_noop("All currently specified species are unlocked."),
    gettext_noop("All specified species are unlocked."),
    gettext_noop("Back to game"),
    gettext_noop("Basic controls"),
    gettext_noop("Choose an occupied garden slot."),
    gettext_noop("Collection"),
    gettext_noop("Contract complete. Claim reward."),
    gettext_noop("Contract complete. +{reward} credits."),
    gettext_noop("Contract match. {remaining} left."),
    gettext_noop("Contract matches"),
    gettext_noop("Cost: {cost} credits."),
    gettext_noop("Credits"),
    gettext_noop("Deliver 3 yellow smooth peas"),
    gettext_noop("Discarded plant from slot {slot}."),
    gettext_noop("Discovered genetic records"),
    gettext_noop("DONE"),
    gettext_noop("Each cross shows the expected genetic combinations."),
    gettext_noop("Founder genotypes cannot be discarded."),
    gettext_noop("Garden"),
    gettext_noop("Generating offspring..."),
    gettext_noop("Genetic Analyzer is already fully upgraded."),
    gettext_noop("Genotypes"),
    gettext_noop("Genotypes found: {count}"),
    gettext_noop("Generated offspring register here."),
    gettext_noop("Greenhouse is already at maximum capacity."),
    gettext_noop("Greenhouse is already maxed."),
    gettext_noop("Greenhouse is full."),
    gettext_noop("Greenhouse slot"),
    gettext_noop("Growing"),
    gettext_noop("HARVEST"),
    gettext_noop("Harvest grown plants."),
    gettext_noop("Hidden entries stay unknown."),
    gettext_noop("How to play"),
    gettext_noop("ANALYZER L3 REQUIRED"),
    gettext_noop("Analyzer L{level} required."),
    gettext_noop("Dominant allele"),
    gettext_noop("Genetic Planning"),
    gettext_noop("Genetic planning"),
    gettext_noop("Genetic probability"),
    gettext_noop("Heterozygous"),
    gettext_noop("Homozygous"),
    gettext_noop("Independent assortment"),
    gettext_noop("Knowledge"),
    gettext_noop("Learned genetics concepts"),
    gettext_noop("Learned: {learned}/{total}"),
    gettext_noop("Selected Concept"),
    gettext_noop("Selected specimen"),
    gettext_noop("Select a revealed cell."),
    gettext_noop("SELL"),
    gettext_noop("Sold specimen for {credits} credits."),
    gettext_noop("Upgrade analyzer in Shop."),
    gettext_noop("Unlocked by analyzer level {level}."),
    gettext_noop("Allele pair"),
    gettext_noop("Allele segregation"),
    gettext_noop("9:3:3:1 dihybrid ratio"),
    gettext_noop("LOCK"),
    gettext_noop("Locked"),
    gettext_noop("Matches"),
    gettext_noop("Max capacity"),
    gettext_noop("Max level"),
    gettext_noop("Mendel Pea unlocked."),
    gettext_noop("Missing"),
    gettext_noop("More slots let you store more offspring."),
    gettext_noop("Mouse: click buttons and plant cards."),
    gettext_noop("New discovery registered."),
    gettext_noop("Next species unlock in shop."),
    gettext_noop("No completed contract to claim."),
    gettext_noop("No revealed plant to store."),
    gettext_noop("Not enough credits."),
    gettext_noop("Offspring revealed."),
    gettext_noop("PARENT A"),
    gettext_noop("PARENT B"),
    gettext_noop("Phenotypes"),
    gettext_noop("Phenotypes found: {count}"),
    gettext_noop(
        "Pick two parent plants, cross them, then inspect offspring."
    ),
    gettext_noop("Reward claimed. +{reward} credits. New contract ready."),
    gettext_noop("Seed color + texture."),
    gettext_noop("Select Parent A"),
    gettext_noop("Select Parent B"),
    gettext_noop("Select parents from the same species."),
    gettext_noop("Select parents, then cross plants."),
    gettext_noop("Select two stored parent plants."),
    gettext_noop("Sells after harvest"),
    gettext_noop("Shop"),
    gettext_noop("Slot {slot}"),
    gettext_noop("Species"),
    gettext_noop("Species found: {count}"),
    gettext_noop("Spend credits on progression"),
    gettext_noop("Stored plant in slot {slot}."),
    gettext_noop("Stored plants and parent selection"),
    gettext_noop("Ready to harvest."),
    gettext_noop("The goal"),
    gettext_noop("Unlock {species}."),
    gettext_noop("Unlock greenhouse slot {slot}."),
    gettext_noop("Unlocked {species}."),
    gettext_noop("Unlocked greenhouse slot {slot}."),
    gettext_noop("Unlocks deeper genetic information."),
    gettext_noop("Upgrade to level {level}: {name}."),
    gettext_noop("Use 1/2 to reselect starting parents."),
    gettext_noop(
        "Use contracts to learn how traits pass between generations."
    ),
    gettext_noop("Yellow smooth peas are requested first."),
    gettext_noop("are rescued first."),
    gettext_noop("green"),
    gettext_noop("smooth"),
    gettext_noop("wrinkled"),
    gettext_noop("yellow"),
    gettext_noop("{name} - discovered"),
)


@dataclass
class SettingsState:
    """Runtime-only player preferences for the MVP settings panel."""

    language: str = "pt-BR"
    music_volume: int = 1
    sound_volume: int = 7
    music_muted: bool = False
    sound_muted: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "SettingsState":
        """Restore settings from save data with safe defaults."""
        state = cls()
        language = data.get("language")
        if language in {"en", "pt-BR"}:
            state.language = str(language)
        state.music_volume = _clamp_volume(data.get("music_volume"), 1)
        state.sound_volume = _clamp_volume(data.get("sound_volume"), 7)
        state.music_muted = bool(data.get("music_muted", False))
        state.sound_muted = bool(data.get("sound_muted", False))
        return state

    def to_dict(self) -> dict[str, object]:
        """Serialize settings into the save payload."""
        return {
            "language": self.language,
            "music_volume": self.music_volume,
            "sound_volume": self.sound_volume,
            "music_muted": self.music_muted,
            "sound_muted": self.sound_muted,
        }

    @property
    def music_gain(self) -> float:
        """Return normalized music gain for Pyxel channels."""
        return 0.0 if self.music_muted else self.music_volume / MAX_VOLUME_STEP

    @property
    def sound_gain(self) -> float:
        """Return normalized sound-effect gain for Pyxel channels."""
        return 0.0 if self.sound_muted else self.sound_volume / MAX_VOLUME_STEP


def _clamp_volume(value: object, default: int) -> int:
    if not isinstance(value, int):
        return default
    return min(max(value, 0), MAX_VOLUME_STEP)


@dataclass(frozen=True)
class BedLayout:
    """Computed Germination Bed geometry for the current batch."""

    x: int
    y: int
    columns: int
    rows: int
    cell_count: int

    @property
    def width(self) -> int:
        """Return the pixel width occupied by cells."""
        return self.columns * BED_CELL_W + (self.columns - 1) * BED_GAP

    @property
    def height(self) -> int:
        """Return the pixel height occupied by cells."""
        return self.rows * BED_CELL_H + (self.rows - 1) * BED_GAP


class MainGameScene:
    """Mouse-first main game scene with keyboard alternatives."""

    def __init__(
        self,
        state: GameState,
        *,
        background_image: pyxel.Image | None = None,
        fonts: FontSet | None = None,
        save_service: SaveService | None = None,
        saved_settings: dict[str, object] | None = None,
    ) -> None:
        self.state = state
        self.breeding = BreedingService(state)
        self.greenhouse_service = GreenhouseService(state)
        self.save_service = save_service
        self.background_image = background_image
        self.fonts = fonts
        self.cross_button_timer = 0
        self._reveal_frames = {}
        self.germination_started_frame: int | None = None
        self.intro_open = True
        self.settings_open = False
        self.parent_picker_target: str | None = None
        self.settings = SettingsState.from_dict(saved_settings or {})
        set_language(self.settings.language)
        self.active_screen = SCREEN_MAIN
        self.collection_tab = "Species"
        self.selected_knowledge = "Phenotype"
        self.selected_greenhouse_slot = 0
        self.selected_shop_item = "slot"
        self._apply_audio_settings()

    def update(self) -> None:
        """Handle mouse-first controls and keyboard shortcuts."""
        self._tick_button_timers()
        if not self.intro_open:
            self._update_germination_readiness()
        if self.intro_open:
            self._update_intro_panel()
        elif self.settings_open:
            self._update_settings_panel()
        elif self.parent_picker_target is not None:
            self._update_parent_picker()
        elif self._update_navigation_rail():
            pass
        elif self.active_screen == SCREEN_KNOWLEDGE:
            self._update_knowledge_screen()
        elif self.active_screen == SCREEN_COLLECTION:
            self._update_collection_screen()
        elif self.active_screen == SCREEN_GARDEN:
            self._update_garden_screen()
        elif self.active_screen == SCREEN_CONTRACTS:
            self._update_contracts_screen()
        elif self.active_screen == SCREEN_SHOP:
            self._update_shop_screen()
        else:
            self._update_main_game()

    def _update_main_game(self) -> None:
        """Handle main crossbreeding screen controls."""
        self._handle_breeding_buttons()
        self._update_germination_bed_selection()
        self._track_reveal_frames()

    def _update_germination_readiness(self) -> None:
        if not self.state.current_batch:
            self.germination_started_frame = None
            return
        if self.germination_started_frame is None:
            self.germination_started_frame = pyxel.frame_count
        if (
            self._germination_ready()
            and self.state.status_message == "Generating offspring..."
        ):
            self.state.status_message = "Ready to harvest."

    def _germination_ready(self) -> bool:
        if not self.state.current_batch:
            return False
        if self.germination_started_frame is None:
            return False
        elapsed = pyxel.frame_count - self.germination_started_frame
        return elapsed >= GERMINATION_SETTLE_FRAMES

    def _handle_breeding_buttons(self) -> None:
        if clicked(CROSS_BUTTON) or pyxel.btnp(pyxel.KEY_RETURN):
            self._play_sound(1)
            self.cross_button_timer = BUTTON_PRESS_FRAMES
            if self.breeding.start_crossbreeding():
                self.germination_started_frame = pyxel.frame_count
                self._reveal_frames = dict.fromkeys(
                    range(len(self.state.current_batch)),
                    pyxel.frame_count,
                )
                self._autosave()

        if clicked(CLAIM_CONTRACT_BUTTON) or pyxel.btnp(pyxel.KEY_C):
            self._play_sound(3)
            if self.breeding.claim_contract_reward():
                self._autosave()

        if (
            clicked(HARVEST_BUTTON) or pyxel.btnp(pyxel.KEY_H)
        ) and self._germination_ready():
            self._play_sound(3)
            if self.breeding.harvest_germination_batch():
                self._autosave()
            self._reveal_frames.clear()
            self.germination_started_frame = None

        if clicked(PARENT_A_CARD) or pyxel.btnp(pyxel.KEY_1):
            self._play_sound(0)
            self.parent_picker_target = "a"

        if clicked(PARENT_B_CARD) or pyxel.btnp(pyxel.KEY_2):
            self._play_sound(0)
            self.parent_picker_target = "b"

    def _track_reveal_frames(self) -> None:
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
        if self.active_screen == SCREEN_KNOWLEDGE:
            self._draw_knowledge_screen()
        elif self.active_screen == SCREEN_COLLECTION:
            self._draw_collection_screen()
        elif self.active_screen == SCREEN_GARDEN:
            self._draw_garden_screen()
        elif self.active_screen == SCREEN_CONTRACTS:
            self._draw_contracts_screen()
        elif self.active_screen == SCREEN_SHOP:
            self._draw_shop_screen()
        else:
            self._draw_main_game_screen()
        self._draw_navigation_rail()
        if self.intro_open:
            self._draw_intro_panel()
        if self.parent_picker_target is not None:
            self._draw_parent_picker()
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
            self._t("CROSS PLANTS"),
            enabled=self.state.can_crossbreed and not self.state.current_batch,
            pressed=self.cross_button_timer > 0,
        )
        self._draw_germination_bed()
        self._draw_bottom_panels()
        self._draw_hovered_plant_tooltip()

    def _update_navigation_rail(self) -> bool:
        for screen, _label, _sprite in NAV_ITEMS:
            if clicked(self._nav_button_rect(screen)):
                self._play_sound(0)
                if screen == "settings":
                    self.settings_open = True
                else:
                    self.active_screen = screen
                return True
        return False

    def _update_knowledge_screen(self) -> None:
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self._play_sound(0)
            self.active_screen = SCREEN_MAIN
            return
        index = 0
        for _stage, concepts, _required_level in KNOWLEDGE_STAGES:
            index += 1
            for concept in concepts:
                if clicked(Rect(28, 116 + index * 11, 196, 10)):
                    self._play_sound(0)
                    self.selected_knowledge = concept
                    return
                index += 1

    def _update_collection_screen(self) -> None:
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self._play_sound(0)
            self.active_screen = SCREEN_MAIN
            return
        for index, tab in enumerate(COLLECTION_TABS):
            if clicked(Rect(24, 108 + index * 30, 104, 22)):
                self._play_sound(0)
                self.collection_tab = tab

    def _update_garden_screen(self) -> None:
        if pyxel.btnp(pyxel.KEY_ESCAPE):
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
            if self.greenhouse_service.select_parent(
                "a",
                self.selected_greenhouse_slot,
            ):
                self._autosave()
        if clicked(Rect(392, 211, 96, 22)):
            self._play_sound(0)
            if self.greenhouse_service.select_parent(
                "b",
                self.selected_greenhouse_slot,
            ):
                self._autosave()
        if clicked(GARDEN_DISCARD_BUTTON):
            self._play_sound(4)
            if self.greenhouse_service.discard_plant(
                self.selected_greenhouse_slot
            ):
                self._autosave()

    def _update_contracts_screen(self) -> None:
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self._play_sound(0)
            self.active_screen = SCREEN_MAIN
            return
        if clicked(Rect(408, 250, 96, 24)) or pyxel.btnp(pyxel.KEY_C):
            self._play_sound(3)
            if self.breeding.claim_contract_reward():
                self._autosave()

    def _update_shop_screen(self) -> None:
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self._play_sound(0)
            self.active_screen = SCREEN_MAIN
            return
        for item, rect in [
            ("slot", Rect(34, 120, 154, 42)),
            ("analyzer", Rect(210, 120, 154, 42)),
            ("species", Rect(386, 120, 154, 42)),
        ]:
            if clicked(rect):
                self._play_sound(0)
                self.selected_shop_item = item
                return
        if clicked(Rect(392, 284, 96, 24)) and self._buy_selected_shop_item():
            self._autosave()

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
        self._draw_runtime_hud_frame(5, 4, 544, 58)
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
        screen = self._active_screen_title()
        pyxel.text(294, 41, self._t(screen).upper()[:18], PyxelColor.ACCENT)

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

    def _draw_navigation_rail(self) -> None:
        self._draw_runtime_hud_frame(
            NAV_RAIL.x,
            NAV_RAIL.y,
            NAV_RAIL.width,
            NAV_RAIL.height,
        )
        for screen, label, sprite in NAV_ITEMS:
            self._draw_nav_item(
                self._nav_button_rect(screen),
                label,
                sprite,
                active=screen == self.active_screen
                or (screen == "settings" and self.settings_open),
            )

    def _draw_nav_item(
        self,
        rect: Rect,
        label: str,
        sprite: tuple[int, int],
        *,
        active: bool,
    ) -> None:
        hovering = rect.contains(pyxel.mouse_x, pyxel.mouse_y)
        fill = PyxelColor.ACCENT if active else PyxelColor.DARK_WOOD
        if hovering and not active:
            fill = PyxelColor.WOOD_MIDTONE
        pyxel.rect(rect.x, rect.y, rect.width, rect.height, fill)
        pyxel.rectb(rect.x, rect.y, rect.width, rect.height, PyxelColor.FRAME)
        pyxel.rectb(
            rect.x + 1,
            rect.y + 1,
            rect.width - 2,
            rect.height - 2,
            PyxelColor.UI_DARK,
        )
        u, v = sprite
        pyxel.blt(
            rect.x + 4,
            rect.y + 5,
            0,
            u,
            v,
            NAV_ICON_SIZE,
            NAV_ICON_SIZE,
            colkey=0,
            scale=NAV_ICON_SCALE,
        )
        text = self._t(label).upper()[:10]
        text_x = rect.x + 24
        pyxel.text(text_x + 1, rect.y + 15, text, PyxelColor.SPRITE_OUTLINE)
        pyxel.text(
            text_x,
            rect.y + 14,
            text,
            PyxelColor.UI_DARK if active else PyxelColor.PARCHMENT_LIGHT,
        )

    def _nav_button_rect(self, screen: str) -> Rect:
        index = next(
            (
                item_index
                for item_index, (item_screen, _label, _sprite) in enumerate(
                    NAV_ITEMS,
                )
                if item_screen == screen
            ),
            0,
        )
        return Rect(
            NAV_BUTTON_X,
            NAV_BUTTON_Y + index * (NAV_BUTTON_H + NAV_BUTTON_GAP),
            NAV_BUTTON_W,
            NAV_BUTTON_H,
        )

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
            286,
            66,
            self._t("CONTRACT"),
            PyxelColor.ACCENT,
            font=self._display_font,
        )
        pyxel.text(
            rect.x + 12,
            rect.y + 12,
            self._contract_title(),
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
        if contract.completed and not contract.paid:
            draw_button(CLAIM_CONTRACT_BUTTON, self._t("CLAIM"))

    def _draw_probability_panel(self) -> None:
        rect = Rect(12, 74, 132, 112)
        draw_panel(rect)
        draw_outlined_text(
            18,
            80,
            self._t("PROBABILITIES"),
            PyxelColor.ACCENT,
            font=self._display_font,
        )
        parent_a = self.state.parent_a
        parent_b = self.state.parent_b
        if parent_a is None or parent_b is None:
            pyxel.text(18, 96, self._t("Select parents"), PyxelColor.UI_DARK)
            return
        if self.state.analyzer_level < ANALYZER_PROBABILITY_LEVEL:
            pyxel.text(
                18,
                96,
                self._t("ANALYZER L3 REQUIRED"),
                PyxelColor.UI_DARK,
            )
            pyxel.text(
                18,
                110,
                self._t("Upgrade analyzer in Shop."),
                PyxelColor.UI_DARK,
            )
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
            self._t(title),
            PyxelColor.ACCENT,
            font=self._display_font,
        )
        if plant is None:
            pyxel.text(
                rect.x + 20,
                rect.y + 28,
                self._t("Empty slot"),
                PyxelColor.UI_DARK,
            )
            return

        self._draw_plant_preview(rect.x + 32, rect.y + 64, plant, large=True)
        pyxel.rect(rect.x + 65, rect.y + 25, 46, 15, PyxelColor.FIELD)
        pyxel.rectb(rect.x + 65, rect.y + 25, 46, 15, PyxelColor.FRAME)
        pyxel.text(
            rect.x + 73,
            rect.y + 30,
            self._visible_genotype(plant),
            PyxelColor.UI_DARK,
        )
        phenotype = plant.phenotype
        pyxel.text(
            rect.x + 65,
            rect.y + 47,
            self._trait(phenotype.seed_color),
            PyxelColor.UI_DARK,
        )

    def _draw_germination_bed(self) -> None:
        layout = self._germination_layout()
        frame_x = layout.x - 10
        frame_y = layout.y - 10
        frame_w = layout.width + 20
        frame_h = layout.height + 20
        pyxel.rect(frame_x, frame_y, frame_w, frame_h, PyxelColor.DARK_WOOD)
        pyxel.rectb(frame_x, frame_y, frame_w, frame_h, PyxelColor.FRAME)
        pyxel.rectb(
            frame_x + 2,
            frame_y + 2,
            frame_w - 4,
            frame_h - 4,
            PyxelColor.UI_DARK,
        )
        pyxel.rect(230, 174, 180, 14, PyxelColor.UI_DARK)

        msg = self._status_text(self.state.status_message)[:44]
        text_width = len(msg) * 4
        text_x = 320 - text_width // 2
        pyxel.text(text_x, 179, msg, PyxelColor.ACCENT)

        for index in range(layout.cell_count):
            self._draw_germination_cell(index, layout)

    def _draw_germination_cell(self, index: int, layout: BedLayout) -> None:
        rect = self._germination_cell_rect(index, layout)
        visible = index < self.state.visible_count
        has_specimen = index < len(self.state.current_batch)
        plant = (
            self.state.current_batch[index]
            if visible and has_specimen
            else None
        )
        selected = index == self.state.selected_offspring_index
        matches_contract = (
            plant is not None and self.state.active_contract.matches(plant)
        )

        fill = PyxelColor.SOIL_DARK
        if plant is None and visible:
            fill = PyxelColor.WARM_FLOOR
        pyxel.rect(rect.x, rect.y, rect.width, rect.height, fill)
        border = PyxelColor.ACCENT if selected else PyxelColor.DARK_WOOD
        if matches_contract:
            border = PyxelColor.PROGRESS
        pyxel.rectb(rect.x, rect.y, rect.width, rect.height, border)

        if not visible:
            pyxel.circ(rect.x + 17, rect.y + 8, 2, PyxelColor.WOOD_MIDTONE)
            return
        if plant is None:
            pyxel.text(rect.x + 12, rect.y + 5, "-", PyxelColor.TEXT_MUTED)
            return

        age = pyxel.frame_count - getattr(self, "_reveal_frames", {}).get(
            index,
            pyxel.frame_count,
        )
        center_x = rect.x + rect.width // 2
        center_y = rect.y + rect.height // 2
        if age < SEED_STAGE_FRAMES:
            pyxel.circ(center_x, center_y + 2, 3, PyxelColor.SEED_GOLD)
            pyxel.circb(center_x, center_y + 2, 3, PyxelColor.SPRITE_OUTLINE)
        elif age < SEEDLING_STAGE_FRAMES:
            pyxel.line(
                center_x,
                center_y + 4,
                center_x,
                center_y - 2,
                PyxelColor.LEAF_GREEN,
            )
            pyxel.pset(center_x - 2, center_y, PyxelColor.LEAF_HIGHLIGHT)
            pyxel.pset(center_x + 2, center_y - 1, PyxelColor.LEAF_HIGHLIGHT)
        else:
            self._draw_tiny_plant(center_x, center_y + 5, plant)
        if matches_contract:
            pyxel.text(
                rect.x + rect.width - 7,
                rect.y + 2,
                "+",
                PyxelColor.PROGRESS,
            )

    def _draw_tiny_plant(self, x: int, y: int, plant: Plant) -> None:
        phenotype = plant.phenotype
        seed_color = (
            PyxelColor.PEA_YELLOW
            if phenotype.seed_color == "yellow"
            else PyxelColor.PEA_GREEN
        )
        pyxel.line(x - 5, y - 3, x + 5, y - 8, PyxelColor.POD_BASE)
        pyxel.line(x - 5, y - 2, x + 5, y - 7, PyxelColor.POD_HIGHLIGHT)
        for offset in (-3, 0, 3):
            pyxel.pset(x + offset, y - 5, seed_color)

    def _germination_cell_rect(self, index: int, layout: BedLayout) -> Rect:
        col = index % layout.columns
        row = index // layout.columns
        return Rect(
            layout.x + col * (BED_CELL_W + BED_GAP),
            layout.y + row * (BED_CELL_H + BED_GAP),
            BED_CELL_W,
            BED_CELL_H,
        )

    def _update_germination_bed_selection(self) -> None:
        layout = self._germination_layout()
        for index in range(len(self.state.current_batch)):
            if clicked(self._germination_cell_rect(index, layout)):
                self._play_sound(0)
                self.state.selected_offspring_index = index
                return

    def _germination_layout(self) -> BedLayout:
        cell_count = min(
            max(len(self.state.current_batch), 1),
            MAX_BED_CELLS,
        )
        columns = min(max(ceil(sqrt(cell_count)), 1), BED_MAX_COLUMNS)
        rows = ceil(cell_count / columns)
        while rows * BED_CELL_H + (rows - 1) * BED_GAP > BED_MAX_H:
            columns = min(columns + 1, BED_MAX_COLUMNS)
            rows = ceil(cell_count / columns)
            if columns == BED_MAX_COLUMNS:
                break
        width = columns * BED_CELL_W + (columns - 1) * BED_GAP
        height = rows * BED_CELL_H + (rows - 1) * BED_GAP
        return BedLayout(
            x=BED_ORIGIN_X + (BED_MAX_W - width) // 2,
            y=BED_ORIGIN_Y + (BED_MAX_H - height) // 2,
            columns=columns,
            rows=rows,
            cell_count=cell_count,
        )

    def _draw_bottom_panels(self) -> None:
        self._draw_stats_panel()
        self._draw_last_plant_panel()
        self._draw_help_panel()
        draw_button(
            HARVEST_BUTTON,
            self._t("HARVEST"),
            enabled=self._germination_ready(),
        )

    def _draw_stats_panel(self) -> None:
        rect = Rect(12, 264, 136, 84)
        draw_panel(rect)
        draw_outlined_text(
            18,
            270,
            self._t("Generation").upper(),
            PyxelColor.ACCENT,
            font=self._display_font,
        )
        total = len(self.state.current_batch)
        pyxel.text(
            24,
            286,
            self._t(
                "Generated: {visible}/{total}",
                visible=self.state.visible_count,
                total=total,
            ),
            PyxelColor.UI_DARK,
        )
        contract = self.state.active_contract
        pyxel.text(
            24,
            300,
            f"{self._t('Matches')}: {contract.delivered_count}",
            PyxelColor.UI_DARK,
        )
        pyxel.text(
            24,
            314,
            f"{self._t('Missing')}: {contract.remaining_count}",
            PyxelColor.UI_DARK,
        )

    def _draw_last_plant_panel(self) -> None:
        rect = Rect(160, 264, 150, 84)
        draw_panel(rect)
        draw_outlined_text(
            166,
            270,
            self._t("Selected specimen").upper(),
            PyxelColor.ACCENT,
            font=self._display_font,
        )
        plant = self.state.selected_offspring
        if plant is None:
            pyxel.text(
                178,
                296,
                self._t("Select a revealed cell."),
                PyxelColor.UI_DARK,
            )
            return

        self._draw_plant_preview(190, 334, plant, large=True)
        phenotype = plant.phenotype
        pyxel.text(226, 288, self._visible_genotype(plant), PyxelColor.UI_DARK)
        pyxel.text(
            226,
            302,
            self._trait(phenotype.seed_color),
            PyxelColor.UI_DARK,
        )
        pyxel.text(
            226,
            316,
            self._trait(phenotype.seed_texture),
            PyxelColor.UI_DARK,
        )

    def _draw_help_panel(self) -> None:
        rect = Rect(322, 264, 170, 84)
        draw_panel(rect)
        draw_outlined_text(
            328,
            270,
            self._t("Help").upper(),
            PyxelColor.ACCENT,
            font=self._display_font,
        )
        pyxel.text(334, 284, self._t("Each parent gives"), PyxelColor.UI_DARK)
        pyxel.text(
            334,
            296,
            self._t("one allele per gene."),
            PyxelColor.UI_DARK,
        )
        pyxel.text(
            334,
            308,
            self._t("Contract matches"),
            PyxelColor.UI_DARK,
        )
        pyxel.text(
            334,
            320,
            self._t("are rescued first."),
            PyxelColor.UI_DARK,
        )

    def _draw_hovered_plant_tooltip(self) -> None:
        hover = self._hovered_germination_specimen()
        if hover is None:
            return
        _index, plant = hover
        phenotype = plant.phenotype
        growth_status = (
            self._t("Growing")
            if not self._germination_ready()
            else self._t("DONE")
        )
        lines = [
            growth_status,
            f"Genotype: {self._visible_genotype(plant)}",
            f"Color: {self._trait(phenotype.seed_color)}",
            f"Texture: {self._trait(phenotype.seed_texture)}",
            self._harvest_destination_label(plant),
        ]
        width = max(len(line) for line in lines) * 4 + 16
        height = len(lines) * 10 + 12
        x = min(max(pyxel.mouse_x + 10, 8), WIDTH - width - 8)
        y = min(max(pyxel.mouse_y - height - 8, 70), HEIGHT - height - 8)
        panel = Rect(x, y, width, height)
        pyxel.rect(panel.x + 2, panel.y + 2, panel.width, panel.height, 0)
        draw_panel(panel)
        for index, line in enumerate(lines):
            pyxel.text(
                panel.x + 8,
                panel.y + 8 + index * 10,
                line,
                PyxelColor.UI_DARK,
            )

    def _hovered_germination_specimen(self) -> tuple[int, Plant] | None:
        layout = self._germination_layout()
        visible_cells = min(len(self.state.current_batch), layout.cell_count)
        for index in range(visible_cells):
            if not self._germination_cell_rect(index, layout).contains(
                pyxel.mouse_x,
                pyxel.mouse_y,
            ):
                continue
            plant = self.state.current_batch[index]
            if plant is None:
                return None
            return index, plant
        return None

    def _harvest_destination_label(self, plant: Plant) -> str:
        if (
            not self.state.active_contract.completed
            and self.state.active_contract.matches(plant)
        ):
            return self._t("Contract matches")
        return self._t("Sells after harvest")

    def _draw_collection_screen(self) -> None:
        self._draw_scene_shell("Collection", "Discovered genetic records")
        pyxel.text(
            438,
            86,
            self._t(
                "Discovered: {total}",
                total=self.state.collection.total_entries,
            ),
            PyxelColor.PARCHMENT_LIGHT,
        )
        for index, tab in enumerate(COLLECTION_TABS):
            rect = Rect(24, 108 + index * 30, 104, 22)
            active = self.collection_tab == tab
            draw_button(rect, self._t(tab).upper(), pressed=active)

        list_panel = Rect(148, 108, 220, 178)
        detail_panel = Rect(386, 108, 154, 178)
        draw_panel(list_panel)
        draw_panel(detail_panel)
        entries = self._collection_entries()
        if not entries:
            pyxel.text(
                166,
                132,
                self._t("No discoveries yet."),
                PyxelColor.UI_DARK,
            )
        for index, line in enumerate(entries[:12]):
            y = 122 + index * 12
            pyxel.text(164, y, line[:44], PyxelColor.UI_DARK)

        pyxel.text(
            402,
            126,
            self._t(self.collection_tab).upper(),
            PyxelColor.UI_DARK,
        )
        details = self._collection_details(entries)
        for index, line in enumerate(details):
            pyxel.text(402, 146 + index * 14, line[:32], PyxelColor.UI_DARK)

    def _draw_knowledge_screen(self) -> None:
        self._draw_scene_shell("Knowledge", "Learned genetics concepts")
        total = sum(
            len(concepts) for _stage, concepts, _level in KNOWLEDGE_STAGES
        )
        learned = sum(
            1
            for _stage, concepts, required_level in KNOWLEDGE_STAGES
            for _concept in concepts
            if self.state.analyzer_level >= required_level
        )
        pyxel.text(
            438,
            86,
            self._t(
                "Learned: {learned}/{total}",
                learned=learned,
                total=total,
            ),
            PyxelColor.PARCHMENT_LIGHT,
        )

        node_panel = Rect(24, 108, 214, 190)
        detail_panel = Rect(258, 108, 282, 190)
        draw_panel(node_panel)
        draw_panel(detail_panel)

        index = 0
        for stage, concepts, required_level in KNOWLEDGE_STAGES:
            stage_unlocked = self.state.analyzer_level >= required_level
            y = 116 + index * 11
            pyxel.text(38, y, self._t(stage).upper(), PyxelColor.ACCENT)
            index += 1
            for concept in concepts:
                unlocked = self.state.analyzer_level >= required_level
                selected = concept == self.selected_knowledge
                rect = Rect(28, 116 + index * 11, 196, 10)
                fill = PyxelColor.ACCENT if selected else PyxelColor.PARCHMENT
                if not unlocked:
                    fill = PyxelColor.TEXT_MUTED
                pyxel.rect(rect.x, rect.y, rect.width, rect.height, fill)
                pyxel.rectb(
                    rect.x,
                    rect.y,
                    rect.width,
                    rect.height,
                    PyxelColor.FRAME,
                )
                label = self._t(concept) if unlocked else self._t("Locked")
                pyxel.text(
                    rect.x + 6,
                    rect.y + 3,
                    label[:44],
                    PyxelColor.UI_DARK,
                )
                if not stage_unlocked:
                    pyxel.text(
                        rect.x + 166,
                        rect.y + 3,
                        f"L{required_level}",
                        PyxelColor.UI_DARK,
                    )
                index += 1

        self._draw_knowledge_details(detail_panel)

    def _draw_knowledge_details(self, panel: Rect) -> None:
        concept = self.selected_knowledge
        required_level = self._knowledge_required_level(concept)
        pyxel.text(
            panel.x + 18,
            panel.y + 18,
            self._t("Selected Concept"),
            PyxelColor.UI_DARK,
        )
        if self.state.analyzer_level < required_level:
            pyxel.text(
                panel.x + 18,
                panel.y + 42,
                self._t("Locked"),
                PyxelColor.UI_DARK,
            )
            pyxel.text(
                panel.x + 18,
                panel.y + 58,
                self._t("Analyzer L{level} required.", level=required_level),
                PyxelColor.UI_DARK,
            )
            return

        pyxel.text(
            panel.x + 18,
            panel.y + 42,
            self._t(concept).upper(),
            PyxelColor.UI_DARK,
        )
        detail = KNOWLEDGE_DETAILS.get(concept, "")
        for index, line in enumerate(self._wrap_text(self._t(detail), 58)[:5]):
            pyxel.text(
                panel.x + 18,
                panel.y + 64 + index * 13,
                line,
                PyxelColor.UI_DARK,
            )
        source = self._knowledge_unlock_source(required_level)
        pyxel.text(
            panel.x + 18,
            panel.y + 154,
            self._t(source),
            PyxelColor.UI_DARK,
        )

    def _draw_garden_screen(self) -> None:
        self._draw_scene_shell("Garden", "Stored plants and parent selection")
        pyxel.text(
            476,
            86,
            f"Slots: {self.state.greenhouse.used_slots}/20",
            PyxelColor.PARCHMENT_LIGHT,
        )
        grid_panel = Rect(24, 104, 294, 214)
        detail_panel = Rect(338, 104, 206, 178)
        draw_panel(grid_panel)
        draw_panel(detail_panel)
        for index in range(GREENHOUSE_COLUMNS * GREENHOUSE_ROWS):
            self._draw_greenhouse_slot(index)

        selected = self._selected_greenhouse_plant()
        pyxel.text(354, 122, self._t("SELECTED PLANT"), PyxelColor.UI_DARK)
        if selected is None:
            pyxel.text(
                354,
                146,
                self._t("Empty or locked slot."),
                PyxelColor.UI_DARK,
            )
        else:
            phenotype = selected.phenotype
            self._draw_plant_preview(382, 205, selected, large=True)
            pyxel.text(
                428,
                146,
                f"Genotype: {self._visible_genotype(selected)}",
                PyxelColor.UI_DARK,
            )
            pyxel.text(
                428,
                160,
                f"Color: {self._trait(phenotype.seed_color)}",
                PyxelColor.UI_DARK,
            )
            pyxel.text(
                428,
                174,
                f"Texture: {self._trait(phenotype.seed_texture)}",
                PyxelColor.UI_DARK,
            )
            draw_button(Rect(392, 183, 96, 22), self._t("PARENT A"))
            draw_button(Rect(392, 211, 96, 22), self._t("PARENT B"))
            draw_button(
                GARDEN_DISCARD_BUTTON,
                self._t("DISCARD"),
                enabled=self.state.greenhouse.can_discard(
                    self.selected_greenhouse_slot,
                ),
            )

    def _draw_contracts_screen(self) -> None:
        self._draw_scene_shell(
            "CONTRACT",
            "Use contracts to learn how traits pass between generations.",
        )
        contract = self.state.active_contract
        summary_panel = Rect(34, 112, 506, 74)
        detail_panel = Rect(34, 204, 506, 92)
        draw_panel(summary_panel)
        draw_panel(detail_panel)

        pyxel.text(
            summary_panel.x + 18,
            summary_panel.y + 14,
            self._contract_title(),
            PyxelColor.UI_DARK,
        )
        progress = f"{contract.delivered_count}/{contract.target_count}"
        pyxel.rect(
            summary_panel.x + 18,
            summary_panel.y + 38,
            390,
            12,
            PyxelColor.BAR_EMPTY,
        )
        progress_width = int(
            390 * contract.delivered_count / contract.target_count,
        )
        pyxel.rect(
            summary_panel.x + 18,
            summary_panel.y + 38,
            progress_width,
            12,
            PyxelColor.PROGRESS,
        )
        pyxel.text(
            summary_panel.x + 420,
            summary_panel.y + 40,
            progress,
            PyxelColor.UI_DARK,
        )

        pyxel.text(
            detail_panel.x + 18,
            detail_panel.y + 18,
            self._t("Credits"),
            PyxelColor.UI_DARK,
        )
        pyxel.text(
            detail_panel.x + 94,
            detail_panel.y + 18,
            f"{contract.reward_credits} CR",
            PyxelColor.UI_DARK,
        )
        pyxel.text(
            detail_panel.x + 18,
            detail_panel.y + 40,
            self._t("Yellow smooth peas are requested first."),
            PyxelColor.UI_DARK,
        )
        status = (
            "Contract complete. Claim reward."
            if contract.completed and not contract.paid
            else "Use contracts to learn how traits pass between generations."
        )
        pyxel.text(
            detail_panel.x + 18,
            detail_panel.y + 58,
            self._t(status),
            PyxelColor.UI_DARK,
        )
        draw_button(
            Rect(408, 250, 96, 24),
            self._t("CLAIM"),
            enabled=contract.completed and not contract.paid,
        )

    def _draw_shop_screen(self) -> None:
        self._draw_scene_shell("Shop", "Spend credits on progression")
        pyxel.text(
            510,
            86,
            f"{self._t('Credits')}: {self.state.credits}",
            PyxelColor.PARCHMENT_LIGHT,
        )
        self._draw_shop_card("slot", Rect(34, 120, 154, 42))
        self._draw_shop_card("analyzer", Rect(210, 120, 154, 42))
        self._draw_shop_card("species", Rect(386, 120, 154, 42))

        details_panel = Rect(70, 198, 456, 100)
        draw_panel(details_panel)
        for index, line in enumerate(self._shop_details()):
            pyxel.text(
                108,
                216 + index * 14,
                self._t(line),
                PyxelColor.UI_DARK,
            )
        draw_button(
            Rect(392, 284, 96, 24),
            self._t("BUY"),
            enabled=self._selected_shop_available(),
        )

    def _draw_scene_shell(self, title: str, subtitle: str) -> None:
        draw_outlined_text(
            24,
            76,
            self._t(title).upper(),
            PyxelColor.ACCENT,
            font=self._display_font,
        )
        pyxel.text(26, 91, self._t(subtitle), PyxelColor.PARCHMENT_LIGHT)

    def _update_parent_picker(self) -> None:
        if clicked(PARENT_PICKER_CLOSE_BUTTON) or pyxel.btnp(pyxel.KEY_ESCAPE):
            self._play_sound(0)
            self.parent_picker_target = None
            return

        for index in range(self.state.greenhouse.capacity):
            if clicked(self._parent_picker_slot_rect(index)):
                self._play_sound(0)
                target = self.parent_picker_target
                if target in {"a", "b"}:
                    selected = self.greenhouse_service.select_parent(
                        target,
                        index,
                    )
                    if selected:
                        self._autosave()
                        self.parent_picker_target = None
                return

    def _draw_parent_picker(self) -> None:
        pyxel.dither(0.68)
        pyxel.rect(0, 0, WIDTH, HEIGHT, PyxelColor.UI_DARK)
        pyxel.dither(1)

        panel = Rect(88, 74, 496, 250)
        draw_panel(panel)
        title = (
            "Select Parent A"
            if self.parent_picker_target == "a"
            else "Select Parent B"
        )
        draw_outlined_text(
            116,
            92,
            self._t(title).upper(),
            PyxelColor.ACCENT,
            font=self._display_font,
        )
        pyxel.text(118, 112, self._t("Garden plants"), PyxelColor.UI_DARK)
        for index in range(self.state.greenhouse.capacity):
            self._draw_parent_picker_slot(index)
        draw_button(PARENT_PICKER_CLOSE_BUTTON, self._t("BACK"))

    def _draw_parent_picker_slot(self, index: int) -> None:
        rect = self._parent_picker_slot_rect(index)
        plant = self.state.greenhouse.plant_at(index)
        selected = index in {
            self.state.selected_parent_a,
            self.state.selected_parent_b,
        }
        fill = PyxelColor.ACCENT if selected else PyxelColor.PARCHMENT
        pyxel.rect(rect.x, rect.y, rect.width, rect.height, fill)
        pyxel.rectb(rect.x, rect.y, rect.width, rect.height, PyxelColor.FRAME)
        if plant is None:
            pyxel.text(rect.x + 10, rect.y + 26, self._t("Empty slot"), 1)
            return
        self._draw_plant_preview(rect.x + 24, rect.y + 47, plant)
        pyxel.text(
            rect.x + 48,
            rect.y + 8,
            self._visible_genotype(plant),
            PyxelColor.UI_DARK,
        )
        pyxel.text(
            rect.x + 48,
            rect.y + 20,
            self._trait(plant.phenotype.seed_color),
            PyxelColor.UI_DARK,
        )
        pyxel.text(
            rect.x + 48,
            rect.y + 31,
            self._trait(plant.phenotype.seed_texture),
            PyxelColor.UI_DARK,
        )

    def _parent_picker_slot_rect(self, index: int) -> Rect:
        col = index % 5
        row = index // 5
        return Rect(112 + col * 90, 130 + row * 42, 82, 36)

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
            pyxel.text(
                rect.x + 13,
                rect.y + 19,
                self._t("LOCK"),
                PyxelColor.UI_DARK,
            )
            return
        plant = self.state.greenhouse.slots[index]
        if plant is None:
            pyxel.text(
                rect.x + 14,
                rect.y + 19,
                self._t("Empty slot").upper()[:5],
                PyxelColor.UI_DARK,
            )
            return
        self._draw_plant_preview(rect.x + 22, rect.y + 42, plant)

    def _draw_shop_card(self, item: str, rect: Rect) -> None:
        selected = self.selected_shop_item == item
        fill = PyxelColor.ACCENT if selected else PyxelColor.PARCHMENT
        pyxel.rect(rect.x, rect.y, rect.width, rect.height, fill)
        pyxel.rectb(rect.x, rect.y, rect.width, rect.height, PyxelColor.FRAME)
        title, cost, status = self._shop_card_data(item)
        pyxel.text(rect.x + 8, rect.y + 9, self._t(title), PyxelColor.UI_DARK)
        pyxel.text(rect.x + 8, rect.y + 23, cost, PyxelColor.UI_DARK)
        pyxel.text(
            rect.x + 92,
            rect.y + 23,
            self._t(status),
            PyxelColor.UI_DARK,
        )

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
            return [
                self._t("{name} - discovered", name=name) for name in entries
            ]
        if self.collection_tab == "Phenotypes":
            entries = sorted(collection.phenotypes)
            return [
                f"{self._trait(color)} / {self._trait(texture)}"
                for color, texture in entries
            ]
        return sorted(collection.genotypes)

    def _collection_details(self, entries: list[str]) -> list[str]:
        if self.collection_tab == "Species":
            return [
                self._t("Mendel Pea unlocked."),
                self._t(
                    "Species found: {count}",
                    count=len(self.state.collection.species),
                ),
                self._t("Next species unlock in shop."),
            ]
        if self.collection_tab == "Phenotypes":
            return [
                self._t("Phenotypes found: {count}", count=len(entries)),
                self._t("Seed color + texture."),
                self._t("Hidden entries stay unknown."),
            ]
        return [
            self._t("Genotypes found: {count}", count=len(entries)),
            self._t("Generated offspring register here."),
            self._t("Analyzer upgrades reveal more data."),
        ]

    def _shop_card_data(self, item: str) -> tuple[str, str, str]:
        if item == "slot":
            next_slot = self.state.greenhouse.capacity + 1
            if next_slot not in GREENHOUSE_EXPANSION_COSTS:
                return ("Greenhouse slot", "Max capacity", "DONE")
            cost = GREENHOUSE_EXPANSION_COSTS[next_slot]
            return (
                self._t("Slot {slot}", slot=next_slot),
                f"{cost} CR",
                self._afford_label(cost),
            )
        if item == "analyzer":
            next_level = self.state.analyzer_level + 1
            if next_level not in ANALYZER_UPGRADES:
                return ("Analyzer", "Max level", "DONE")
            _name, cost = ANALYZER_UPGRADES[next_level]
            return (
                self._t("Analyzer L{level}", level=next_level),
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
                return [self._t("Greenhouse is already at maximum capacity.")]
            return [
                self._t("Unlock greenhouse slot {slot}.", slot=next_slot),
                self._t("More slots let you store more offspring."),
                self._t("Cost: {cost} credits.", cost=cost),
            ]
        if self.selected_shop_item == "analyzer":
            next_level = self.state.analyzer_level + 1
            upgrade = ANALYZER_UPGRADES.get(next_level)
            if upgrade is None:
                return [self._t("Genetic Analyzer is already fully upgraded.")]
            name, cost = upgrade
            return [
                self._t(
                    "Upgrade to level {level}: {name}.",
                    level=next_level,
                    name=name,
                ),
                self._t("Unlocks deeper genetic information."),
                self._t("Cost: {cost} credits.", cost=cost),
            ]
        species_name, data = self._next_species_unlock()
        if species_name is None or data is None:
            return [self._t("All currently specified species are unlocked.")]
        genes, cost = data
        return [
            self._t("Unlock {species}.", species=species_name),
            self._t("Adds a {genes}-gene plant species.", genes=genes),
            self._t("Cost: {cost} credits.", cost=cost),
        ]

    def _buy_selected_shop_item(self) -> bool:
        if self.selected_shop_item == "slot":
            return self._buy_greenhouse_slot()

        if self.selected_shop_item == "analyzer":
            return self._buy_analyzer_upgrade()

        return self._buy_species_unlock()

    def _buy_greenhouse_slot(self) -> bool:
        next_slot = self.state.greenhouse.capacity + 1
        cost = GREENHOUSE_EXPANSION_COSTS.get(next_slot)
        if cost is None:
            self.state.status_message = "Greenhouse is already maxed."
            return False
        if not self._spend_credits(cost):
            return False
        self.state.greenhouse.expand()
        self.state.status_message = f"Unlocked greenhouse slot {next_slot}."
        self._play_sound(3)
        return True

    def _buy_analyzer_upgrade(self) -> bool:
        next_level = self.state.analyzer_level + 1
        upgrade = ANALYZER_UPGRADES.get(next_level)
        if upgrade is None:
            self.state.status_message = "Analyzer is already maxed."
            return False
        _name, cost = upgrade
        if not self._spend_credits(cost):
            return False
        self.state.analyzer_level = next_level
        self.state.status_message = f"Analyzer upgraded to level {next_level}."
        self._play_sound(3)
        return True

    def _buy_species_unlock(self) -> bool:
        species_name, data = self._next_species_unlock()
        if species_name is None or data is None:
            self.state.status_message = "All specified species are unlocked."
            return False
        _genes, cost = data
        if not self._spend_credits(cost):
            return False
        self.state.unlocked_species.add(species_name)
        self.state.collection.register_species(species_name)
        self.state.status_message = f"Unlocked {species_name}."
        self._play_sound(3)
        return True

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

    def _update_intro_panel(self) -> None:
        if (
            clicked(INTRO_OK_BUTTON)
            or pyxel.btnp(pyxel.KEY_RETURN)
            or pyxel.btnp(pyxel.KEY_ESCAPE)
        ):
            self._play_sound(0)
            self.intro_open = False

    def _draw_intro_panel(self) -> None:
        pyxel.dither(0.72)
        pyxel.rect(0, 0, WIDTH, HEIGHT, PyxelColor.UI_DARK)
        pyxel.dither(1)

        panel = Rect(92, 56, 456, 272)
        draw_panel(panel)
        draw_outlined_text(
            222,
            78,
            self._t("Before playing").upper(),
            PyxelColor.ACCENT,
            font=self._display_font,
        )

        sections = [
            (
                "The goal",
                [
                    (
                        "Use contracts to learn how traits pass "
                        "between generations."
                    ),
                    "Yellow smooth peas are requested first.",
                ],
            ),
            (
                "How to play",
                [
                    (
                        "Pick two parent plants, cross them, then inspect "
                        "offspring."
                    ),
                    "Each cross shows the expected genetic combinations.",
                ],
            ),
            (
                "Basic controls",
                [
                    "Mouse: click buttons and plant cards.",
                    (
                        "Pick two parent plants, cross them, then inspect "
                        "offspring."
                    ),
                    "Harvest grown plants.",
                    "Use 1/2 to reselect starting parents.",
                ],
            ),
        ]
        y = 112
        for title, lines in sections:
            pyxel.text(126, y, self._t(title).upper(), PyxelColor.UI_DARK)
            y += 13
            for line in lines:
                pyxel.text(138, y, self._t(line), PyxelColor.UI_DARK)
                y += 12
            y += 7

        draw_button(INTRO_OK_BUTTON, self._t("OK"))

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
            set_language(self.settings.language)
            self._autosave()

        if clicked(MUSIC_DOWN_BUTTON):
            self._play_sound(0)
            self.settings.music_volume = max(
                self.settings.music_volume - 1,
                0,
            )
            self._apply_audio_settings()
            self._autosave()
        if clicked(MUSIC_UP_BUTTON):
            self._play_sound(0)
            self.settings.music_volume = min(
                self.settings.music_volume + 1,
                MAX_VOLUME_STEP,
            )
            self._apply_audio_settings()
            self._autosave()
        if clicked(SOUND_DOWN_BUTTON):
            self._play_sound(0)
            self.settings.sound_volume = max(
                self.settings.sound_volume - 1,
                0,
            )
            self._apply_audio_settings()
            self._autosave()
        if clicked(SOUND_UP_BUTTON):
            self._play_sound(0)
            self.settings.sound_volume = min(
                self.settings.sound_volume + 1,
                MAX_VOLUME_STEP,
            )
            self._apply_audio_settings()
            self._autosave()

        if clicked(MUSIC_MUTE_CHECKBOX):
            self.settings.music_muted = not self.settings.music_muted
            self._apply_audio_settings()
            self._play_sound(0)
            self._autosave()
        if clicked(SOUND_MUTE_CHECKBOX):
            self.settings.sound_muted = not self.settings.sound_muted
            self._apply_audio_settings()
            self._play_sound(0)
            self._autosave()

    def _draw_settings_panel(self) -> None:
        pyxel.dither(0.65)
        pyxel.rect(0, 0, WIDTH, HEIGHT, PyxelColor.UI_DARK)
        pyxel.dither(1)

        panel = Rect(100, 70, 440, 242)
        draw_panel(panel)
        draw_outlined_text(
            254,
            84,
            self._t("Settings").upper(),
            PyxelColor.ACCENT,
            font=self._display_font,
        )
        pyxel.text(
            188,
            106,
            self._t("Language"),
            PyxelColor.UI_DARK,
        )
        draw_button(LANGUAGE_BUTTON, self._language_label())

        self._draw_volume_control(
            143,
            self._t("Music volume"),
            self.settings.music_volume,
            (MUSIC_DOWN_BUTTON, MUSIC_UP_BUTTON),
        )
        self._draw_checkbox(
            MUSIC_MUTE_CHECKBOX,
            self.settings.music_muted,
            self._t("Mute music"),
        )

        self._draw_volume_control(
            186,
            self._t("Effects volume"),
            self.settings.sound_volume,
            (SOUND_DOWN_BUTTON, SOUND_UP_BUTTON),
        )
        self._draw_checkbox(
            SOUND_MUTE_CHECKBOX,
            self.settings.sound_muted,
            self._t("Mute sounds"),
        )

        pyxel.text(
            188,
            238,
            self._t("Changes apply immediately."),
            PyxelColor.UI_DARK,
        )
        draw_button(SETTINGS_BACK_BUTTON, self._t("BACK"))

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

    def _active_screen_title(self) -> str:
        for screen, label, _sprite in NAV_ITEMS:
            if screen == self.active_screen:
                return label
        return "CROSS PLANTS"

    def _trait(self, value: str) -> str:
        return self._t(value)

    def _visible_genotype(self, plant: Plant) -> str:
        if self.state.analyzer_level < ANALYZER_GENOTYPE_LEVEL:
            return "????"
        return plant.genotype

    def _knowledge_required_level(self, concept: str) -> int:
        for _stage, concepts, required_level in KNOWLEDGE_STAGES:
            if concept in concepts:
                return required_level
        return 1

    def _knowledge_unlock_source(self, required_level: int) -> str:
        return self._t(
            "Unlocked by analyzer level {level}.",
            level=required_level,
        )

    def _wrap_text(self, text: str, width: int) -> list[str]:
        lines: list[str] = []
        current = ""
        for word in text.split():
            candidate = f"{current} {word}".strip()
            if len(candidate) <= width:
                current = candidate
                continue
            if current:
                lines.append(current)
            current = word
        if current:
            lines.append(current)
        return lines

    def _contract_title(self) -> str:
        contract = self.state.active_contract
        has_phenotype_goal = (
            contract.seed_color is not None
            and contract.seed_texture is not None
        )
        if has_phenotype_goal:
            return self._t(
                "Deliver {target} {color} {texture} peas",
                target=contract.target_count,
                color=self._trait(contract.seed_color),
                texture=self._trait(contract.seed_texture),
            )
        return contract.title

    def _status_text(self, message: str) -> str:
        dynamic_templates = [
            ("Contract complete. +", " credits.", "reward"),
            ("Contract match. ", " left.", "remaining"),
            (
                "Reward claimed. +",
                " credits. New contract ready.",
                "reward",
            ),
            ("Stored plant in slot ", ".", "slot"),
            ("Discarded plant from slot ", ".", "slot"),
            ("Unlocked greenhouse slot ", ".", "slot"),
            ("Analyzer upgraded to level ", ".", "level"),
            ("Sold specimen for ", " credits.", "credits"),
        ]
        for prefix, suffix, key in dynamic_templates:
            if message.startswith(prefix) and message.endswith(suffix):
                value = message.removeprefix(prefix).removesuffix(suffix)
                template = f"{prefix}{{{key}}}{suffix}"
                return self._t(template, **{key: value})
        if message.startswith("Unlocked ") and message.endswith("."):
            species = message.removeprefix("Unlocked ").removesuffix(".")
            return self._t("Unlocked {species}.", species=species)
        return self._t(message)

    def _t(self, text: str, **kwargs: object) -> str:
        return t(text, **kwargs)

    def _autosave(self) -> None:
        if self.save_service is None:
            return
        self.save_service.save(
            self.state,
            language=self.settings.language,
            settings=self.settings.to_dict(),
        )

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
