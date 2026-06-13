"""Main gameplay scene for the MVP."""

from dataclasses import dataclass

import pyxel

from mendels_greenhouse.core.collection import official_collection_keys
from mendels_greenhouse.core.content import (
    ANALYZER_UPGRADES,
    DISCOVERY_REWARDS,
    GREENHOUSE_EXPANSION_COSTS,
    SPECIES_DEFINITIONS,
    SPECIES_UNLOCK_ORDER,
    SPECIES_UNLOCK_REQUIRED_FREE_SLOTS,
    collection_total_entries,
    species_definition,
)
from mendels_greenhouse.core.genetics import (
    Plant,
    expected_distribution,
    expected_phenotype_probabilities,
    founder_genotypes,
    gametes,
)
from mendels_greenhouse.core.i18n import gettext_noop, set_language, t
from mendels_greenhouse.services.breeding_service import BreedingService
from mendels_greenhouse.services.greenhouse_service import GreenhouseService
from mendels_greenhouse.services.save_service import SaveService
from mendels_greenhouse.state.game_state import GameState
from mendels_greenhouse.ui.components import (
    Rect,
    clicked,
)
from mendels_greenhouse.ui.fonts import (
    FontSet,
)
from mendels_greenhouse.ui.game_components import (
    BedGeometry,
    BedLayout,
    contract_progress_label,
    contract_progress_width,
    germination_cell_rect,
    germination_layout,
    plant_trait_lines,
)
from mendels_greenhouse.ui.game_components.collection import (
    ALBUM_COLUMNS,
    ALBUM_GRID_RECT,
    ALBUM_SCROLLBAR,
    ALBUM_VISIBLE_ROWS,
    CollectionAlbumEntry,
    CollectionScreenData,
    album_card_rect,
    album_max_scroll_row,
    draw_collection_screen,
)
from mendels_greenhouse.ui.game_components.contracts import (
    ContractsScreenData,
    draw_contracts_screen,
)
from mendels_greenhouse.ui.game_components.garden import (
    GardenScreenData,
    draw_garden_screen,
    greenhouse_slot_rect,
)
from mendels_greenhouse.ui.game_components.knowledge import (
    KnowledgeScreenData,
    KnowledgeStage,
    draw_knowledge_screen,
    knowledge_concept_rect,
    knowledge_stage_rect,
    selected_knowledge_stage,
)
from mendels_greenhouse.ui.game_components.main_game import (
    CROSS_BUTTON,
    PARENT_A_CARD,
    PARENT_B_CARD,
    AnalyzerPanelData,
    ContractBannerData,
    GerminationBedPanelData,
    NavigationRailConfig,
    ParentCrossPanelData,
    SpecimenOverlayData,
    TopBarData,
    draw_analyzer_panel,
    draw_contract_banner,
    draw_germination_bed_panel,
    draw_greenhouse_background,
    draw_navigation_rail,
    draw_parent_cross_panel,
    draw_specimen_overlay,
    draw_top_bar,
    nav_button_rect,
)
from mendels_greenhouse.ui.game_components.overlays import (
    ParentPickerData,
    draw_intro_panel,
    draw_parent_picker,
    parent_picker_slot_rect,
)
from mendels_greenhouse.ui.game_components.settings import (
    LANGUAGE_BUTTON,
    MUSIC_DOWN_BUTTON,
    MUSIC_MUTE_CHECKBOX,
    MUSIC_UP_BUTTON,
    RESET_CANCEL_BUTTON,
    RESET_CONFIRM_BUTTON,
    RESET_PROGRESS_BUTTON,
    SETTINGS_BACK_BUTTON,
    SOUND_DOWN_BUTTON,
    SOUND_MUTE_CHECKBOX,
    SOUND_UP_BUTTON,
    SettingsOverlayData,
    VolumeControlData,
    draw_settings_overlay,
)
from mendels_greenhouse.ui.game_components.shared import (
    DrawContext,
    draw_scene_shell,
)
from mendels_greenhouse.ui.game_components.shop import (
    SHOP_BUY_BUTTON,
    SHOP_CARD_RECTS,
    SHOP_CONFIRM_BUY_BUTTON,
    SHOP_CONFIRM_CANCEL_BUTTON,
    ShopCardData,
    ShopConfirmationData,
    ShopScreenData,
    draw_shop_confirmation,
    draw_shop_screen,
)

WIDTH = 640
HEIGHT = 360
TOP_BAR_H = 66
PROBABILITY_PANEL_MAX_Y = 166

SPECIMEN_PANEL = Rect(158, 16, 324, 328)
SPECIMEN_CLOSE_BUTTON = Rect(446, 22, 24, 18)
STORE_BUTTON = Rect(178, 270, 284, 30)
DISCARD_BUTTON = Rect(178, 306, 284, 30)
HARVEST_BUTTON = Rect(309, 318, 120, 24)
INTRO_OK_BUTTON = Rect(272, 294, 96, 24)
CLAIM_CONTRACT_BUTTON = Rect(480, 20, 64, 18)
PARENT_PICKER_CLOSE_BUTTON = Rect(492, 286, 76, 22)
GARDEN_DISCARD_BUTTON = Rect(392, 257, 96, 22)
NAV_RAIL = Rect(558, 0, 82, 360)
NAV_BUTTON_W = 70
NAV_BUTTON_H = 48
NAV_BUTTON_GAP = 2
NAV_BUTTON_X = 564
NAV_BUTTON_Y = 6

PLANT_SPRITES = {
    ("yellow", "smooth"): (0, 0),
    ("yellow", "wrinkled"): (64, 0),
    ("green", "smooth"): (128, 0),
    ("green", "wrinkled"): (192, 0),
}
SPECIES_PLANT_SPRITES = {
    "Snapdragon": (0, 192),
    "Corn": (64, 192),
    "Tomato": (128, 192),
    "Orchid": (192, 192),
}
PLANT_SPRITE_W = 56
PLANT_SPRITE_H = 44
NAV_ICON_SIZE = 64
NAV_ICON_SCALE = 0.5
NAV_RAIL_CONFIG = NavigationRailConfig(
    rail_rect=NAV_RAIL,
    button_x=NAV_BUTTON_X,
    button_y=NAV_BUTTON_Y,
    button_width=NAV_BUTTON_W,
    button_height=NAV_BUTTON_H,
    button_gap=NAV_BUTTON_GAP,
    icon_size=NAV_ICON_SIZE,
    icon_scale=NAV_ICON_SCALE,
)
SCREEN_MAIN = "main"
SCREEN_CONTRACTS = "contracts"
SCREEN_KNOWLEDGE = "knowledge"
SCREEN_COLLECTION = "collection"
SCREEN_GARDEN = "garden"
SCREEN_SHOP = "shop"
NAV_ITEMS = (
    (SCREEN_MAIN, "CROSS PLANTS", (0, 128)),
    (SCREEN_GARDEN, "Garden", (64, 64)),
    (SCREEN_CONTRACTS, "Contract", (128, 128)),
    (SCREEN_KNOWLEDGE, "Learn", (0, 64)),
    (SCREEN_SHOP, "Shop", (128, 64)),
    (SCREEN_COLLECTION, "Collection", (64, 128)),
    ("settings", "Config.", (192, 64)),
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
BUTTON_PRESS_FRAMES = 7
ANALYZER_GENOTYPE_LEVEL = 2
ANALYZER_PROBABILITY_LEVEL = 3
ANALYZER_SIMULATOR_LEVEL = 4
ANALYZER_FULL_GAMETE_LIMIT = 4
ANALYZER_COMPACT_GAMETE_COUNT = 2
SEED_STAGE_FRAMES = 15
SEEDLING_STAGE_FRAMES = 30
GERMINATION_SETTLE_FRAMES = 90
MAX_BED_CELLS = 20
BED_MAX_COLUMNS = 5
BED_ORIGIN_X = 369
BED_ORIGIN_Y = 196
BED_CELL_W = 46
BED_CELL_H = 26
BED_GAP = 4
BED_GEOMETRY = BedGeometry(
    origin_x=BED_ORIGIN_X,
    origin_y=BED_ORIGIN_Y,
    max_columns=BED_MAX_COLUMNS,
    cell_width=BED_CELL_W,
    cell_height=BED_CELL_H,
    gap=BED_GAP,
)
MUSIC_CHANNELS = (0, 1, 2)
SOUND_CHANNEL = 3
MAX_VOLUME_STEP = 10
TESTER_MONEY_CODE = "MONEYTREE"
TESTER_MONEY_CREDITS = 999_999
TESTER_CODE_KEYS = {
    "A": pyxel.KEY_A,
    "B": pyxel.KEY_B,
    "C": pyxel.KEY_C,
    "D": pyxel.KEY_D,
    "E": pyxel.KEY_E,
    "F": pyxel.KEY_F,
    "G": pyxel.KEY_G,
    "H": pyxel.KEY_H,
    "I": pyxel.KEY_I,
    "J": pyxel.KEY_J,
    "K": pyxel.KEY_K,
    "L": pyxel.KEY_L,
    "M": pyxel.KEY_M,
    "N": pyxel.KEY_N,
    "O": pyxel.KEY_O,
    "P": pyxel.KEY_P,
    "Q": pyxel.KEY_Q,
    "R": pyxel.KEY_R,
    "S": pyxel.KEY_S,
    "T": pyxel.KEY_T,
    "U": pyxel.KEY_U,
    "V": pyxel.KEY_V,
    "W": pyxel.KEY_W,
    "X": pyxel.KEY_X,
    "Y": pyxel.KEY_Y,
    "Z": pyxel.KEY_Z,
}

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
    gettext_noop("Config."),
    gettext_noop("Contract"),
    gettext_noop("Contract complete. Claim reward."),
    gettext_noop("Contract complete. +{reward} credits."),
    gettext_noop("Contract match. {remaining} left."),
    gettext_noop("Contract matches"),
    gettext_noop("Cost: {cost} credits."),
    gettext_noop("Credits"),
    gettext_noop("Deliver 3 yellow smooth peas"),
    gettext_noop("Deliver {target} {genotype} {species}"),
    gettext_noop("Deliver {target} {traits} {species}"),
    gettext_noop("Discarded plant from slot {slot}."),
    gettext_noop("Discovery rewards. +{credits} credits."),
    gettext_noop("Discovered genetic records"),
    gettext_noop("Discovered: {found}/{total}"),
    gettext_noop("DONE"),
    gettext_noop("Each cross shows the expected genetic combinations."),
    gettext_noop("Founder genotypes cannot be discarded."),
    gettext_noop("Garden"),
    gettext_noop("Generating offspring..."),
    gettext_noop("Genotype already stored."),
    gettext_noop("Genetic Analyzer is already fully upgraded."),
    gettext_noop("Genotypes"),
    gettext_noop("Genotypes found: {count}"),
    gettext_noop("Generated offspring register here."),
    gettext_noop("Greenhouse is already at maximum capacity."),
    gettext_noop("Greenhouse is already maxed."),
    gettext_noop("Greenhouse is full."),
    gettext_noop("Greenhouse slot"),
    gettext_noop("Requires two empty garden slots."),
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
    gettext_noop("Learn"),
    gettext_noop("Learned genetics concepts"),
    gettext_noop("Learned: {learned}/{total}"),
    gettext_noop("Selected Concept"),
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
    gettext_noop("No selected specimen to store."),
    gettext_noop("No specimens to harvest."),
    gettext_noop("Not enough credits."),
    gettext_noop("Offspring discarded."),
    gettext_noop("Offspring revealed."),
    gettext_noop("Parent A selected from garden."),
    gettext_noop("Parent B selected from garden."),
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
    gettext_noop("Adds dominant and recessive founders."),
    gettext_noop("Sells after harvest"),
    gettext_noop("Shop"),
    gettext_noop("Slot {slot}"),
    gettext_noop("Species"),
    gettext_noop("Species found: {count}"),
    gettext_noop("Species unlock is not priced."),
    gettext_noop("Spend credits on progression"),
    gettext_noop("Stored plant in slot {slot}."),
    gettext_noop("Stored plant in slot {slot}. +{credits} credits."),
    gettext_noop("Statistical contract complete."),
    gettext_noop("Stored plants and parent selection"),
    gettext_noop("Ready to harvest."),
    gettext_noop("Reset game progression"),
    gettext_noop("Reset requires confirmation."),
    gettext_noop("Progress reset."),
    gettext_noop("Dangerous action"),
    gettext_noop("This will erase all progression data."),
    gettext_noop("Contracts, credits, discoveries, and plants will reset."),
    gettext_noop("This cannot be undone."),
    gettext_noop("CONFIRM RESET"),
    gettext_noop("CANCEL"),
    gettext_noop("Tester money code enabled."),
    gettext_noop("The goal"),
    gettext_noop("Unlock {species}."),
    gettext_noop("Unlock greenhouse slot {slot}."),
    gettext_noop("Unlocked {species}."),
    gettext_noop("Unlocked greenhouse slot {slot}."),
    gettext_noop("Unlocks deeper genetic information."),
    gettext_noop("Upgrade to level {level}: {name}."),
    gettext_noop("Undiscovered"),
    gettext_noop("Use 1/2 to reselect starting parents."),
    gettext_noop(
        "Use contracts to learn how traits pass between generations."
    ),
    gettext_noop("Yellow smooth peas are requested first."),
    gettext_noop("Analyzer level 2 reveals exact genotypes."),
    gettext_noop("Best stored cross"),
    gettext_noop("are rescued first."),
    gettext_noop("Matching harvest specimens are rescued first."),
    gettext_noop("Validate the whole generated batch."),
    gettext_noop("No valid stored cross found."),
    gettext_noop("green"),
    gettext_noop("smooth"),
    gettext_noop("wrinkled"),
    gettext_noop("yellow"),
    gettext_noop("{name} - discovered"),
    gettext_noop("{found}/{total} found"),
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
        self.reset_confirmation_open = False
        self.shop_confirmation_open = False
        self.parent_picker_target: str | None = None
        self.specimen_overlay_open = False
        self.settings = SettingsState.from_dict(saved_settings or {})
        set_language(self.settings.language)
        self.active_screen = SCREEN_MAIN
        self.collection_tab = "Species"
        self.collection_scroll_row = 0
        self.selected_collection_entry = 0
        self.selected_knowledge = "Phenotype"
        self.selected_greenhouse_slot = 0
        self.selected_shop_item = "slot"
        self.tester_code_buffer = ""
        self._apply_audio_settings()

    def update(self) -> None:  # noqa: PLR0912
        """Handle mouse-first controls and keyboard shortcuts."""
        self._tick_button_timers()
        self._update_tester_code()
        if not self.intro_open:
            self._update_germination_readiness()
        if self.intro_open:
            self._update_intro_panel()
        elif self.settings_open:
            self._update_settings_panel()
        elif self.parent_picker_target is not None:
            self._update_parent_picker()
        elif self.specimen_overlay_open:
            self._update_specimen_overlay()
        elif self.shop_confirmation_open:
            self._update_shop_purchase_confirmation()
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

    def _update_tester_code(self) -> None:
        for character, key in TESTER_CODE_KEYS.items():
            if pyxel.btnp(key):
                self._handle_tester_code_character(character)
                return

    def _handle_tester_code_character(self, character: str) -> None:
        self.tester_code_buffer = (self.tester_code_buffer + character)[
            -len(TESTER_MONEY_CODE) :
        ]
        if self.tester_code_buffer != TESTER_MONEY_CODE:
            return
        self.state.credits = max(self.state.credits, TESTER_MONEY_CREDITS)
        self.state.status_message = "Tester money code enabled."
        self.tester_code_buffer = ""
        self._play_sound(3)
        self._autosave()

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
        if not any(plant is not None for plant in self.state.current_batch):
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
        if self.shop_confirmation_open:
            self._draw_shop_purchase_confirmation()
        if self.specimen_overlay_open:
            self._draw_specimen_overlay()
        if self.intro_open:
            self._draw_intro_panel()
        if self.parent_picker_target is not None:
            self._draw_parent_picker()
        if self.settings_open:
            self._draw_settings_panel()

    def _draw_main_game_screen(self) -> None:
        contract = self.state.active_contract
        draw_contract_banner(
            self._draw_context(),
            ContractBannerData(
                title=self._contract_title(),
                progress_label=contract_progress_label(contract),
                progress_width=contract_progress_width(contract, 200),
                claim_enabled=contract.completed and not contract.paid,
                claim_button=CLAIM_CONTRACT_BUTTON,
            ),
        )
        draw_analyzer_panel(
            self._draw_context(),
            AnalyzerPanelData(
                has_parent_pair=(
                    self.state.parent_a is not None
                    and self.state.parent_b is not None
                ),
                analyzer_level=self.state.analyzer_level,
                genotype_level=ANALYZER_GENOTYPE_LEVEL,
                probability_level=ANALYZER_PROBABILITY_LEVEL,
                simulator_level=ANALYZER_SIMULATOR_LEVEL,
                phenotype_lines=self._analyzer_phenotype_lines(),
                genotype_lines=self._analyzer_genotype_lines(),
                gamete_lines=self._analyzer_gamete_lines(),
                probability_lines=self._probability_lines(),
                best_cross=self._best_contract_cross(),
                max_probability_y=PROBABILITY_PANEL_MAX_Y,
                view_level=self.state.analyzer_level,
            ),
        )
        draw_parent_cross_panel(
            self._draw_context(),
            ParentCrossPanelData(
                parent_a_card=PARENT_A_CARD,
                parent_b_card=PARENT_B_CARD,
                parent_a=self.state.parent_a,
                parent_b=self.state.parent_b,
                cross_button=CROSS_BUTTON,
                can_crossbreed=self.state.can_crossbreed,
                has_current_batch=bool(self.state.current_batch),
                cross_pressed=self.cross_button_timer > 0,
            ),
            plant_preview=self._draw_component_plant_preview,
            visible_genotype=self._visible_genotype,
            trait=self._trait,
        )
        self._draw_germination_bed()

    def _draw_specimen_overlay(self) -> None:
        plant = self.state.selected_offspring
        if plant is None:
            return
        can_store = (
            not self.state.greenhouse.has_genotype(plant.genotype)
            and self.state.greenhouse.free_slots > 0
        )
        draw_specimen_overlay(
            self._draw_context(),
            SpecimenOverlayData(
                panel=SPECIMEN_PANEL,
                store_button=STORE_BUTTON,
                discard_button=DISCARD_BUTTON,
                close_button=SPECIMEN_CLOSE_BUTTON,
                plant=plant,
                can_store=can_store,
                visible_genotype=self._visible_genotype(plant),
                trait_lines=self._plant_trait_lines(plant, limit=2),
            ),
            plant_preview=self._draw_overlay_plant_preview,
        )

    def _draw_context(self) -> DrawContext:
        return DrawContext(
            translate=self._t,
            display_font=self._display_font,
        )

    def _draw_component_plant_preview(
        self,
        x: int,
        y: int,
        plant: Plant,
        large: bool,
    ) -> None:
        self._draw_plant_preview(x, y, plant, large=large)

    def _draw_overlay_plant_preview(
        self,
        x: int,
        y: int,
        plant: Plant,
        _large: bool,
    ) -> None:
        u, v = self._plant_sprite_coords(plant)
        scale = 2
        pyxel.blt(
            x - PLANT_SPRITE_W * scale // 2,
            y - PLANT_SPRITE_H * scale,
            0,
            u,
            v,
            PLANT_SPRITE_W,
            PLANT_SPRITE_H,
            colkey=0,
            scale=scale,
        )

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
        stages = self._knowledge_stage_data()
        active_stage = selected_knowledge_stage(
            stages,
            self.selected_knowledge,
        )
        active_stage_index = stages.index(active_stage)

        for index, stage in enumerate(stages):
            if clicked(knowledge_stage_rect(index)):
                self._play_sound(0)
                self.selected_knowledge = stage.concepts[0]
                return

        for index, concept in enumerate(active_stage.concepts):
            rect = knowledge_concept_rect(index)
            if rect.contains(pyxel.mouse_x, pyxel.mouse_y):
                self.selected_knowledge = concept
            if clicked(rect):
                self._play_sound(0)
                return

        stage_delta = 0
        if pyxel.btnp(pyxel.KEY_LEFT):
            stage_delta = -1
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            stage_delta = 1
        if stage_delta:
            next_index = min(
                max(active_stage_index + stage_delta, 0),
                len(stages) - 1,
            )
            self._play_sound(0)
            self.selected_knowledge = stages[next_index].concepts[0]
            return

        concept_index = active_stage.concepts.index(self.selected_knowledge)
        concept_delta = 0
        if pyxel.btnp(pyxel.KEY_UP):
            concept_delta = -1
        elif pyxel.btnp(pyxel.KEY_DOWN):
            concept_delta = 1
        if concept_delta:
            next_index = min(
                max(concept_index + concept_delta, 0),
                len(active_stage.concepts) - 1,
            )
            self._play_sound(0)
            self.selected_knowledge = active_stage.concepts[next_index]

    def _update_collection_screen(self) -> None:
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self._play_sound(0)
            self.active_screen = SCREEN_MAIN
            return
        for index, tab in enumerate(COLLECTION_TABS):
            if clicked(Rect(24, 108 + index * 30, 104, 22)):
                self._play_sound(0)
                self.collection_tab = tab
                self.collection_scroll_row = 0
                self.selected_collection_entry = 0
                return

        entries = self._collection_album_entries()
        max_scroll = album_max_scroll_row(len(entries))
        scroll_delta = 0
        if ALBUM_GRID_RECT.contains(pyxel.mouse_x, pyxel.mouse_y):
            scroll_delta -= pyxel.mouse_wheel
        if pyxel.btnp(pyxel.KEY_UP):
            scroll_delta -= 1
        if pyxel.btnp(pyxel.KEY_DOWN):
            scroll_delta += 1
        if pyxel.btnp(pyxel.KEY_PAGEUP):
            scroll_delta -= ALBUM_VISIBLE_ROWS
        if pyxel.btnp(pyxel.KEY_PAGEDOWN):
            scroll_delta += ALBUM_VISIBLE_ROWS
        if scroll_delta:
            self.collection_scroll_row = min(
                max(self.collection_scroll_row + scroll_delta, 0),
                max_scroll,
            )

        first_index = self.collection_scroll_row * ALBUM_COLUMNS
        visible_count = ALBUM_COLUMNS * ALBUM_VISIBLE_ROWS
        for visible_index in range(
            min(visible_count, len(entries) - first_index)
        ):
            if clicked(album_card_rect(visible_index)):
                self._play_sound(0)
                self.selected_collection_entry = first_index + visible_index
                return

        if clicked(ALBUM_SCROLLBAR) and max_scroll:
            relative_y = pyxel.mouse_y - ALBUM_SCROLLBAR.y
            self.collection_scroll_row = min(
                max_scroll * relative_y // ALBUM_SCROLLBAR.height,
                max_scroll,
            )

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
        if clicked(Rect(392, 201, 96, 22)):
            self._play_sound(0)
            if self.greenhouse_service.select_parent(
                "a",
                self.selected_greenhouse_slot,
            ):
                self._autosave()
        if clicked(Rect(392, 229, 96, 22)):
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
        for item, rect in zip(
            ("slot", "analyzer", "species"),
            SHOP_CARD_RECTS,
            strict=True,
        ):
            if clicked(rect):
                self._play_sound(0)
                self.selected_shop_item = item
                return
        if (
            clicked(SHOP_BUY_BUTTON) or pyxel.btnp(pyxel.KEY_RETURN)
        ) and self._selected_shop_available():
            self._request_shop_purchase()

    def _update_shop_purchase_confirmation(self) -> None:
        if clicked(SHOP_CONFIRM_CANCEL_BUTTON) or pyxel.btnp(pyxel.KEY_ESCAPE):
            self._play_sound(0)
            self.shop_confirmation_open = False
            return
        if clicked(SHOP_CONFIRM_BUY_BUTTON) or pyxel.btnp(pyxel.KEY_RETURN):
            self._confirm_shop_purchase()

    def _request_shop_purchase(self) -> None:
        if not self._selected_shop_available():
            return
        self._play_sound(0)
        self.shop_confirmation_open = True

    def _confirm_shop_purchase(self) -> bool:
        if not self.shop_confirmation_open:
            return False
        if not self._buy_selected_shop_item():
            return False
        self.shop_confirmation_open = False
        self._autosave()
        return True

    def _draw_greenhouse_background(self) -> None:
        draw_greenhouse_background(
            background_image=self.background_image,
            width=WIDTH,
            height=HEIGHT,
        )

    def _draw_top_bar(self) -> None:
        draw_top_bar(
            data=TopBarData(
                credits=self.state.credits,
                greenhouse_used=self.state.greenhouse.used_slots,
                greenhouse_capacity=self.state.greenhouse.capacity,
                active_screen_title=self._active_screen_title(),
            ),
            translate=self._t,
            display_font=self._display_font,
        )

    def _draw_navigation_rail(self) -> None:
        draw_navigation_rail(
            NAV_RAIL_CONFIG,
            NAV_ITEMS,
            active_screen=self.active_screen,
            settings_open=self.settings_open,
            translate=self._t,
        )

    def _nav_button_rect(self, screen: str) -> Rect:
        return nav_button_rect(
            screen,
            NAV_ITEMS,
            NAV_RAIL_CONFIG,
        )

    def _probability_lines(self) -> list[str]:
        parent_a = self.state.parent_a
        parent_b = self.state.parent_b
        if parent_a is None or parent_b is None:
            return []
        view_level = self.state.analyzer_level
        if view_level < ANALYZER_PROBABILITY_LEVEL:
            return []

        probabilities = expected_phenotype_probabilities(parent_a, parent_b)
        return [
            f"{' / '.join(self._trait(value) for value in traits)}: "
            f"{round(probability * 100)}%"
            for traits, probability in sorted(
                probabilities.items(),
                key=lambda item: (-item[1], item[0]),
            )
        ]

    def _analyzer_phenotype_lines(self) -> list[str]:
        parent_a = self.state.parent_a
        parent_b = self.state.parent_b
        if parent_a is None or parent_b is None:
            return []
        return [
            "A: "
            + " / ".join(
                self._trait(value)
                for value in parent_a.phenotype.traits.values()
            ),
            "B: "
            + " / ".join(
                self._trait(value)
                for value in parent_b.phenotype.traits.values()
            ),
        ]

    def _analyzer_genotype_lines(self) -> list[str]:
        parent_a = self.state.parent_a
        parent_b = self.state.parent_b
        if parent_a is None or parent_b is None:
            return []
        return [
            f"A: {parent_a.genotype}",
            f"B: {parent_b.genotype}",
        ]

    def _analyzer_gamete_lines(self) -> list[str]:
        parent_a = self.state.parent_a
        parent_b = self.state.parent_b
        if parent_a is None or parent_b is None:
            return []
        return [
            f"A: {self._compact_gametes(gametes(parent_a))}",
            f"B: {self._compact_gametes(gametes(parent_b))}",
        ]

    @staticmethod
    def _compact_gametes(values: tuple[str, ...]) -> str:
        if len(values) <= ANALYZER_FULL_GAMETE_LIMIT:
            return " ".join(values)
        visible = " ".join(values[:ANALYZER_COMPACT_GAMETE_COUNT])
        remaining = len(values) - ANALYZER_COMPACT_GAMETE_COUNT
        return f"{visible} +{remaining}"

    def _best_contract_cross(self) -> str | None:
        """Return the stored parent pair with the best active-contract odds."""
        stored = [
            (index, plant)
            for index, plant in enumerate(self.state.greenhouse.slots)
            if plant is not None
        ]
        best_label: str | None = None
        best_score = -1.0
        for index_a, parent_a in stored:
            for index_b, parent_b in stored:
                if index_a >= index_b or parent_a.species != parent_b.species:
                    continue
                score = self._contract_cross_score(parent_a, parent_b)
                if score <= best_score:
                    continue
                best_score = score
                best_label = (
                    f"{index_a + 1} x {index_b + 1}: {int(score * 100)}%"
                )
        return best_label

    def _contract_cross_score(self, parent_a: Plant, parent_b: Plant) -> float:
        contract = self.state.active_contract
        distribution = expected_distribution(parent_a, parent_b)
        if contract.ratio is not None:
            phenotype_counts = {}
            for genotype, count in distribution.genotype_counts.items():
                plant = Plant(genotype, species=parent_a.species)
                key = tuple(sorted(plant.phenotype.traits.items()))
                phenotype_counts[key] = phenotype_counts.get(key, 0) + count
            observed = tuple(sorted(phenotype_counts.values(), reverse=True))
            return 1.0 if observed == contract.ratio else 0.0
        matches = 0
        for genotype, count in distribution.genotype_counts.items():
            plant = Plant(genotype, species=parent_a.species)
            if contract.matches(plant):
                matches += count
        return matches / distribution.total_combinations

    def _draw_germination_bed(self) -> None:
        contract = self.state.active_contract
        draw_germination_bed_panel(
            self._draw_context(),
            GerminationBedPanelData(
                rect=Rect(188, 178, 362, 170),
                layout=self._germination_layout(),
                current_batch=self.state.current_batch,
                visible_count=self.state.visible_count,
                selected_index=(
                    self.state.selected_offspring_index
                    if self.specimen_overlay_open
                    else None
                ),
                status_message=self.state.status_message,
                reveal_frames=getattr(self, "_reveal_frames", {}),
                frame_count=pyxel.frame_count,
                seed_stage_frames=SEED_STAGE_FRAMES,
                seedling_stage_frames=SEEDLING_STAGE_FRAMES,
                harvest_button=HARVEST_BUTTON,
                can_harvest=self._germination_ready(),
                contract_progress_count=contract.progress_count,
                contract_remaining_count=contract.remaining_count,
            ),
            status_text=self._status_text,
            matches_contract=contract.matches,
        )

    def _germination_cell_rect(self, index: int, layout: BedLayout) -> Rect:
        return germination_cell_rect(index, layout)

    def _update_germination_bed_selection(self) -> None:
        layout = self._germination_layout()
        visible_cells = min(
            self.state.visible_count,
            len(self.state.current_batch),
            layout.cell_count,
        )
        for index in range(visible_cells):
            if self.state.current_batch[index] is None:
                continue
            if clicked(self._germination_cell_rect(index, layout)):
                self._play_sound(0)
                self.state.selected_offspring_index = index
                self.specimen_overlay_open = True
                return

    def _germination_layout(self) -> BedLayout:
        return germination_layout(
            batch_size=min(len(self.state.current_batch), MAX_BED_CELLS),
            fallback_cells=20,
            geometry=BED_GEOMETRY,
        )

    def _update_specimen_overlay(self) -> None:
        if clicked(SPECIMEN_CLOSE_BUTTON) or pyxel.btnp(pyxel.KEY_ESCAPE):
            self._play_sound(0)
            self.specimen_overlay_open = False
            return

        if clicked(STORE_BUTTON) or pyxel.btnp(pyxel.KEY_S):
            if self.breeding.store_selected_offspring():
                self._play_sound(3)
                self.specimen_overlay_open = False
                if not self.state.current_batch:
                    self._reveal_frames.clear()
                    self.germination_started_frame = None
                self._autosave()
            else:
                self._play_sound(4)
            return

        if clicked(DISCARD_BUTTON) or pyxel.btnp(pyxel.KEY_D):
            if self.breeding.discard_selected_offspring():
                self._play_sound(3)
                self.specimen_overlay_open = False
                if not self.state.current_batch:
                    self._reveal_frames.clear()
                    self.germination_started_frame = None
                self._autosave()
            else:
                self._play_sound(4)

    def _draw_collection_screen(self) -> None:
        entries = self._collection_album_entries()
        draw_collection_screen(
            self._draw_context(),
            CollectionScreenData(
                total_entries=self.state.collection.total_entries,
                total_slots=collection_total_entries(),
                tabs=COLLECTION_TABS,
                active_tab=self.collection_tab,
                entries=entries,
                discovered_count=sum(entry.discovered for entry in entries),
                scroll_row=self.collection_scroll_row,
                selected_index=self.selected_collection_entry,
            ),
        )

    def _draw_knowledge_screen(self) -> None:
        total = sum(
            len(concepts) for _stage, concepts, _level in KNOWLEDGE_STAGES
        )
        learned = sum(
            1
            for _stage, concepts, required_level in KNOWLEDGE_STAGES
            for _concept in concepts
            if self.state.analyzer_level >= required_level
        )
        draw_knowledge_screen(
            self._draw_context(),
            KnowledgeScreenData(
                stages=self._knowledge_stage_data(),
                analyzer_level=self.state.analyzer_level,
                selected_concept=self.selected_knowledge,
                detail_texts=KNOWLEDGE_DETAILS,
                learned_count=learned,
                total_count=total,
                wrap_text=self._wrap_text,
            ),
        )

    def _knowledge_stage_data(self) -> tuple[KnowledgeStage, ...]:
        return tuple(
            KnowledgeStage(stage, concepts, required_level)
            for stage, concepts, required_level in KNOWLEDGE_STAGES
        )

    def _draw_garden_screen(self) -> None:
        draw_garden_screen(
            self._draw_context(),
            GardenScreenData(
                slots=self.state.greenhouse.slots,
                capacity=self.state.greenhouse.capacity,
                used_slots=self.state.greenhouse.used_slots,
                selected_slot=self.selected_greenhouse_slot,
                selected_plant=self._selected_greenhouse_plant(),
                can_discard_selected=self.state.greenhouse.can_discard(
                    self.selected_greenhouse_slot,
                ),
                discard_button=GARDEN_DISCARD_BUTTON,
            ),
            plant_preview=self._draw_component_plant_preview,
            visible_genotype=self._visible_genotype,
            trait_lines=lambda plant: self._plant_trait_lines(plant, limit=2),
        )

    def _draw_contracts_screen(self) -> None:
        contract = self.state.active_contract
        draw_contracts_screen(
            self._draw_context(),
            ContractsScreenData(
                title=self._contract_title(),
                progress_label=contract_progress_label(contract),
                progress_width=contract_progress_width(contract, 390),
                reward_credits=contract.reward_credits,
                instruction=self._contract_instruction(),
                claim_enabled=contract.completed and not contract.paid,
            ),
        )

    def _draw_shop_screen(self) -> None:
        draw_shop_screen(
            self._draw_context(),
            ShopScreenData(
                credits=self.state.credits,
                selected_item=self.selected_shop_item,
                cards=(
                    self._shop_card_display_data(
                        "slot",
                        SHOP_CARD_RECTS[0],
                    ),
                    self._shop_card_display_data(
                        "analyzer",
                        SHOP_CARD_RECTS[1],
                    ),
                    self._shop_card_display_data(
                        "species",
                        SHOP_CARD_RECTS[2],
                    ),
                ),
                details=self._shop_details(),
                buy_enabled=self._selected_shop_available(),
            ),
        )

    def _draw_shop_purchase_confirmation(self) -> None:
        cost = self._selected_shop_cost()
        card = self._shop_card_display_data(
            self.selected_shop_item,
            SHOP_CARD_RECTS[
                ("slot", "analyzer", "species").index(self.selected_shop_item)
            ],
        )
        draw_shop_confirmation(
            self._draw_context(),
            ShopConfirmationData(
                title=card.title,
                cost=card.cost,
                credits_after=max(self.state.credits - cost, 0),
                artwork=card.artwork,
                sprite=card.sprite,
            ),
        )

    def _draw_scene_shell(self, title: str, subtitle: str) -> None:
        draw_scene_shell(self._draw_context(), title, subtitle)

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
        draw_parent_picker(
            self._draw_context(),
            ParentPickerData(
                target=self.parent_picker_target,
                slots=self.state.greenhouse.slots,
                capacity=self.state.greenhouse.capacity,
                selected_parent_a=self.state.selected_parent_a,
                selected_parent_b=self.state.selected_parent_b,
                close_button=PARENT_PICKER_CLOSE_BUTTON,
            ),
            plant_preview=self._draw_component_plant_preview,
            visible_genotype=self._visible_genotype,
            trait=self._trait,
        )

    def _parent_picker_slot_rect(self, index: int) -> Rect:
        return parent_picker_slot_rect(index)

    def _greenhouse_slot_rect(self, index: int) -> Rect:
        return greenhouse_slot_rect(
            index,
            columns=GREENHOUSE_COLUMNS,
            slot_size=GREENHOUSE_SLOT_SIZE,
        )

    def _selected_greenhouse_plant(self) -> Plant | None:
        if self.selected_greenhouse_slot >= self.state.greenhouse.capacity:
            return None
        return self.state.greenhouse.plant_at(self.selected_greenhouse_slot)

    def _collection_album_entries(
        self,
    ) -> tuple[CollectionAlbumEntry, ...]:
        collection = self.state.collection
        if self.collection_tab == "Species":
            return tuple(
                CollectionAlbumEntry(
                    title=self._t(species),
                    subtitle=self._t("Species"),
                    discovered=species in collection.species,
                )
                for species in official_collection_keys("Species")
            )
        if self.collection_tab == "Phenotypes":
            return tuple(
                CollectionAlbumEntry(
                    title=" / ".join(
                        self._trait(value) for _name, value in traits
                    ),
                    subtitle=self._t(species),
                    discovered=(species, traits) in collection.phenotypes,
                )
                for species, traits in official_collection_keys("Phenotypes")
            )
        return tuple(
            CollectionAlbumEntry(
                title=genotype,
                subtitle=self._t(species),
                discovered=(species, genotype) in collection.genotypes,
            )
            for species, genotype in official_collection_keys("Genotypes")
        )

    def _shop_card_data(self, item: str) -> tuple[str, str, str]:
        if item == "slot":
            return self._greenhouse_slot_card_data()
        if item == "analyzer":
            return self._analyzer_card_data()
        return self._species_card_data()

    def _shop_card_display_data(self, item: str, rect: Rect) -> ShopCardData:
        title, cost, status = self._shop_card_data(item)
        return ShopCardData(
            item=item,
            rect=rect,
            title=title,
            cost=cost,
            status=status,
            artwork=item,
            sprite=self._shop_artwork_sprite(item),
        )

    def _shop_artwork_sprite(
        self,
        item: str,
    ) -> tuple[int, int] | None:
        if item != "species":
            return None
        species_name, _data = self._next_species_unlock()
        if species_name is None:
            return None
        return SPECIES_PLANT_SPRITES.get(species_name)

    def _greenhouse_slot_card_data(self) -> tuple[str, str, str]:
        next_slot = self.state.greenhouse.capacity + 1
        if next_slot not in GREENHOUSE_EXPANSION_COSTS:
            return ("Greenhouse slot", "Max capacity", "DONE")
        cost = GREENHOUSE_EXPANSION_COSTS[next_slot]
        return (
            self._t("Slot {slot}", slot=next_slot),
            f"{cost} CR",
            self._afford_label(cost),
        )

    def _analyzer_card_data(self) -> tuple[str, str, str]:
        next_level = self.state.analyzer_level + 1
        if next_level not in ANALYZER_UPGRADES:
            return ("Analyzer", "Max level", "DONE")
        _name, cost = ANALYZER_UPGRADES[next_level]
        return (
            self._t("Analyzer L{level}", level=next_level),
            f"{cost} CR",
            self._afford_label(cost),
        )

    def _species_card_data(self) -> tuple[str, str, str]:
        species_name, data = self._next_species_unlock()
        if species_name is None or data is None:
            return ("Species", "All unlocked", "DONE")
        _genes, cost = data
        if cost is None:
            return (species_name, "TBD", "LOCK")
        if (
            self.state.greenhouse.free_slots
            < SPECIES_UNLOCK_REQUIRED_FREE_SLOTS
        ):
            return (species_name, f"{cost} CR", "LOCK")
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
        cost_label = "TBD" if cost is None else cost
        return [
            self._t("Unlock {species}.", species=species_name),
            self._t("Adds a {genes}-gene plant species.", genes=genes),
            self._t("Adds dominant and recessive founders."),
            self._t("Requires two empty garden slots."),
            self._t("Cost: {cost} credits.", cost=cost_label),
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
        genes, cost = data
        if cost is None:
            self.state.status_message = "Species unlock is not priced."
            return False
        if (
            self.state.greenhouse.free_slots
            < SPECIES_UNLOCK_REQUIRED_FREE_SLOTS
        ):
            self.state.status_message = "Requires two empty garden slots."
            self._play_sound(4)
            return False
        if not self._spend_credits(cost):
            return False
        self.state.unlocked_species.add(species_name)
        if self.state.collection.register_species(species_name):
            self.state.credits += DISCOVERY_REWARDS["species"]
        dominant, recessive = founder_genotypes(genes)
        self.state.greenhouse.store(
            Plant(dominant, species=species_name),
        )
        self.state.greenhouse.store(
            Plant(recessive, species=species_name),
        )
        self.state.status_message = f"Unlocked {species_name}."
        self._play_sound(3)
        return True

    def _selected_shop_available(self) -> bool:
        _title, cost_text, status = self._shop_card_data(
            self.selected_shop_item,
        )
        return status == "BUY" and cost_text.endswith("CR")

    def _selected_shop_cost(self) -> int:
        if self.selected_shop_item == "slot":
            next_slot = self.state.greenhouse.capacity + 1
            return GREENHOUSE_EXPANSION_COSTS.get(next_slot, 0)
        if self.selected_shop_item == "analyzer":
            next_level = self.state.analyzer_level + 1
            upgrade = ANALYZER_UPGRADES.get(next_level)
            return 0 if upgrade is None else upgrade[1]
        _species_name, data = self._next_species_unlock()
        if data is None or data[1] is None:
            return 0
        return data[1]

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
    ) -> tuple[str | None, tuple[int, int | None] | None]:
        for species_name in SPECIES_UNLOCK_ORDER:
            if species_name not in SPECIES_DEFINITIONS:
                continue
            if species_name not in self.state.unlocked_species:
                definition = species_definition(species_name)
                return (
                    species_name,
                    (definition.gene_count, definition.unlock_cost),
                )
        return None, None

    def _draw_plant_preview(
        self,
        x: int,
        y: int,
        plant: Plant,
        *,
        large: bool = False,
    ) -> None:
        u, v = self._plant_sprite_coords(plant)
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

    def _plant_sprite_coords(self, plant: Plant) -> tuple[int, int]:
        if plant.species in SPECIES_PLANT_SPRITES:
            return SPECIES_PLANT_SPRITES[plant.species]
        phenotype = plant.phenotype
        sprite_key = (phenotype.seed_color, phenotype.seed_texture)
        return PLANT_SPRITES.get(
            sprite_key,
            PLANT_SPRITES[("yellow", "smooth")],
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
        draw_intro_panel(self._draw_context(), INTRO_OK_BUTTON)

    def _update_settings_panel(self) -> None:
        if self.reset_confirmation_open:
            self._update_reset_confirmation()
            return

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

        if clicked(RESET_PROGRESS_BUTTON):
            self._request_progress_reset()

    def _update_reset_confirmation(self) -> None:
        if clicked(RESET_CANCEL_BUTTON) or pyxel.btnp(pyxel.KEY_ESCAPE):
            self._play_sound(0)
            self.reset_confirmation_open = False
            return
        if clicked(RESET_CONFIRM_BUTTON):
            self._play_sound(3)
            self._confirm_progress_reset()

    def _draw_settings_panel(self) -> None:
        draw_settings_overlay(
            self._draw_context(),
            self._settings_overlay_data(),
        )

    def _draw_reset_confirmation(self) -> None:
        draw_settings_overlay(
            self._draw_context(),
            self._settings_overlay_data(),
        )

    def _settings_overlay_data(self) -> SettingsOverlayData:
        return SettingsOverlayData(
            language_label=self._language_label(),
            language_button=LANGUAGE_BUTTON,
            music=VolumeControlData(
                y=112,
                label=self._t("Music volume"),
                value=self.settings.music_volume,
                down_button=MUSIC_DOWN_BUTTON,
                up_button=MUSIC_UP_BUTTON,
            ),
            sound=VolumeControlData(
                y=174,
                label=self._t("Effects volume"),
                value=self.settings.sound_volume,
                down_button=SOUND_DOWN_BUTTON,
                up_button=SOUND_UP_BUTTON,
            ),
            music_mute_checkbox=MUSIC_MUTE_CHECKBOX,
            sound_mute_checkbox=SOUND_MUTE_CHECKBOX,
            music_muted=self.settings.music_muted,
            sound_muted=self.settings.sound_muted,
            reset_button=RESET_PROGRESS_BUTTON,
            back_button=SETTINGS_BACK_BUTTON,
            reset_confirmation_open=self.reset_confirmation_open,
            reset_cancel_button=RESET_CANCEL_BUTTON,
            reset_confirm_button=RESET_CONFIRM_BUTTON,
        )

    def _request_progress_reset(self) -> None:
        self._play_sound(4)
        self.reset_confirmation_open = True
        self.state.status_message = "Reset requires confirmation."

    def _confirm_progress_reset(self) -> None:
        self.reset_confirmation_open = False
        self._reset_progression()

    def _reset_progression(self) -> None:
        self.state = GameState.create_initial()
        self.breeding = BreedingService(self.state)
        self.greenhouse_service = GreenhouseService(self.state)
        self.parent_picker_target = None
        self.specimen_overlay_open = False
        self.reset_confirmation_open = False
        self.shop_confirmation_open = False
        self.active_screen = SCREEN_MAIN
        self.collection_tab = "Species"
        self.collection_scroll_row = 0
        self.selected_collection_entry = 0
        self.selected_knowledge = "Phenotype"
        self.selected_greenhouse_slot = 0
        self.selected_shop_item = "slot"
        self._reveal_frames.clear()
        self.germination_started_frame = None
        self.state.status_message = "Progress reset."
        self._autosave()

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

    def _plant_trait_lines(
        self,
        plant: Plant,
        *,
        limit: int | None = None,
    ) -> list[str]:
        """Return display lines for visible plant traits."""
        return plant_trait_lines(plant, translate=self._t, limit=limit)

    def _format_phenotype_entry(
        self,
        species: str,
        traits: tuple[tuple[str, str], ...],
    ) -> str:
        values = " / ".join(self._trait(value) for _name, value in traits)
        return f"{species}: {values}"

    def _visible_genotype(self, plant: Plant) -> str:
        view_level = self.state.analyzer_level
        if view_level < ANALYZER_GENOTYPE_LEVEL:
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
        if contract.kind == "phenotype" and contract.trait_requirements:
            values = " ".join(
                self._trait(value)
                for value in contract.trait_requirements.values()
            )
            return self._t(
                "Deliver {target} {traits} {species}",
                target=contract.target_count,
                traits=values,
                species=contract.species,
            )
        if contract.kind == "genotype":
            return self._t(
                "Deliver {target} {genotype} {species}",
                target=contract.target_count,
                genotype=contract.genotype,
                species=contract.species,
            )
        return contract.title

    def _contract_instruction(self) -> str:
        contract = self.state.active_contract
        if contract.resolution_mode == "statistical":
            return self._t("Validate the whole generated batch.")
        if contract.kind == "genotype":
            return self._t("Analyzer level 2 reveals exact genotypes.")
        return self._t("Matching harvest specimens are rescued first.")

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
            ("Discovery rewards. +", " credits.", "credits"),
        ]
        for prefix, suffix, key in dynamic_templates:
            if message.startswith(prefix) and message.endswith(suffix):
                value = message.removeprefix(prefix).removesuffix(suffix)
                template = f"{prefix}{{{key}}}{suffix}"
                return self._t(template, **{key: value})
        if (
            message.startswith("Stored plant in slot ")
            and " +" in message
            and message.endswith(" credits.")
        ):
            slot, credits = (
                message.removeprefix("Stored plant in slot ")
                .removesuffix(" credits.")
                .split(". +", maxsplit=1)
            )
            return self._t(
                "Stored plant in slot {slot}. +{credits} credits.",
                slot=slot,
                credits=credits,
            )
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
