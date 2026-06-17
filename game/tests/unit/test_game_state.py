"""Tests for MVP state, storage, and contract services."""

import sys
from types import SimpleNamespace

import pyxel

from mendels_greenhouse.core.contracts import (
    PhenotypeContract,
    create_tutorial_contract,
    generate_next_contract,
)
from mendels_greenhouse.core.genetics import Plant
from mendels_greenhouse.core.i18n import set_language
from mendels_greenhouse.core.save_data import (
    SaveMetadata,
    state_from_save_data,
    state_to_save_data,
)
from mendels_greenhouse.scenes.main_game import MainGameScene
from mendels_greenhouse.services.breeding_service import (
    BreedingService,
    representative_bed_size,
)
from mendels_greenhouse.services.greenhouse_service import GreenhouseService
from mendels_greenhouse.services.save_service import SaveIdentity, SaveService
from mendels_greenhouse.state.game_state import GameState
from mendels_greenhouse.ui.game_components.main_game import (
    ANALYZER_VIEW_BUTTONS,
    ANALYZER_VIEW_PUNNETT,
    ANALYZER_VIEW_TRAITS,
)


def test_initial_state_matches_official_mvp_setup() -> None:
    state = GameState.create_initial()

    assert state.credits == 0
    assert state.greenhouse.capacity == 4
    assert state.greenhouse.used_slots == 2
    assert state.greenhouse.plant_at(0) == Plant("AABB")
    assert state.greenhouse.plant_at(1) == Plant("aabb")
    assert "Mendel Pea" in state.collection.species


def test_tutorial_contract_accepts_matching_phenotypes_once() -> None:
    contract = create_tutorial_contract()

    assert contract.deliver(Plant("AABB"))
    assert contract.deliver(Plant("AaBb"))
    assert contract.deliver(Plant("AABb"))
    assert contract.completed
    assert contract.claim_reward() == 50
    assert contract.claim_reward() == 0


def test_tutorial_contract_rejects_non_matching_phenotypes() -> None:
    contract = create_tutorial_contract()

    assert not contract.deliver(Plant("aabb"))
    assert contract.delivered_count == 0


def test_breeding_service_uses_combination_count_for_simple_cross() -> None:
    state = GameState.create_initial()
    service = BreedingService(state)

    assert service.start_crossbreeding()

    assert len(state.current_batch) == 1
    assert state.visible_count == 1


def test_representative_bed_size_uses_available_combinations() -> None:
    parent_a = Plant("AaBb")
    parent_b = Plant("AaBb")

    assert representative_bed_size(parent_a, parent_b) == 16


def test_breeding_service_harvests_grown_batch() -> None:
    state = GameState.create_initial()
    service = BreedingService(state)
    service.start_crossbreeding()

    assert service.harvest_germination_batch()

    assert state.visible_count == 0
    assert state.current_batch == []
    assert state.active_contract.delivered_count == 1
    assert ("Mendel Pea", "AaBb") in state.collection.genotypes
    assert state.credits == 50


def test_breeding_service_sells_non_contract_specimens_after_growth() -> None:
    state = GameState.create_initial()
    state.current_batch = [Plant("AaBb"), Plant("aabb")]
    state.visible_count = 2
    service = BreedingService(state)

    assert service.harvest_germination_batch()

    assert state.active_contract.delivered_count == 1
    assert state.credits == 52
    assert state.current_batch == []


def test_store_last_revealed_uses_empty_greenhouse_slot() -> None:
    state = GameState.create_initial()
    service = BreedingService(state)
    service.start_crossbreeding()

    assert service.store_last_revealed()

    assert state.greenhouse.used_slots == 3
    assert state.current_batch == []
    assert state.visible_count == 0


def test_harvest_empty_batch_is_not_required_after_storing() -> None:
    state = GameState.create_initial()
    state.current_batch = [None]
    state.visible_count = 1
    service = BreedingService(state)

    assert not service.harvest_germination_batch()

    assert state.current_batch == []
    assert state.visible_count == 0
    assert state.status_message == "No specimens to harvest."


def test_greenhouse_rejects_duplicate_genotype_storage() -> None:
    state = GameState.create_initial()

    assert state.greenhouse.store(Plant("AABB")) is None

    assert state.greenhouse.used_slots == 2
    assert state.greenhouse.plant_at(2) is None


def test_store_selected_offspring_rejects_duplicate_genotype() -> None:
    state = GameState.create_initial()
    state.current_batch = [Plant("AABB")]
    state.visible_count = 1
    state.selected_offspring_index = 0
    service = BreedingService(state)

    assert not service.store_selected_offspring()

    assert state.status_message == "Genotype already stored."
    assert state.greenhouse.used_slots == 2
    assert state.current_batch[0] == Plant("AABB")


def test_greenhouse_service_discards_only_non_protected_plants() -> None:
    state = GameState.create_initial()
    service = GreenhouseService(state)
    state.greenhouse.store(Plant("AaBb"))

    assert not service.discard_plant(0)
    assert state.greenhouse.plant_at(0) == Plant("AABB")

    assert service.discard_plant(2)
    assert state.greenhouse.plant_at(2) is None


def test_parent_selection_repairs_incompatible_other_species() -> None:
    state = GameState.create_initial()
    service = GreenhouseService(state)
    state.greenhouse.slots = [
        Plant("AABB", species="Mendel Pea"),
        Plant("aabb", species="Mendel Pea"),
        Plant("AABBCC", species="Snapdragon"),
        Plant("AaBbCc", species="Snapdragon"),
    ]
    state.selected_parent_a = 0
    state.selected_parent_b = 1

    assert service.select_parent("a", 2)

    assert state.selected_parent_a == 2
    assert state.selected_parent_b == 3


def test_completed_contract_requires_manual_reward_claim() -> None:
    state = GameState.create_initial()
    service = BreedingService(state)

    for _ in range(3):
        service.start_crossbreeding()
        assert service.harvest_germination_batch()

    assert state.active_contract.completed
    assert state.credits == 50

    assert service.claim_contract_reward()

    assert state.credits == 100
    assert state.completed_contracts == 1
    assert not state.active_contract.completed
    assert state.active_contract.target_count == 4
    assert state.active_contract.trait_requirements == {
        "seed color": "yellow",
        "seed texture": "smooth",
    }


def test_claim_without_complete_contract_does_not_generate_next() -> None:
    state = GameState.create_initial()
    service = BreedingService(state)
    current_contract = state.active_contract

    assert not service.claim_contract_reward()

    assert state.credits == 0
    assert state.completed_contracts == 0
    assert state.active_contract is current_contract


def test_species_unlock_requires_two_free_greenhouse_slots() -> None:
    state = GameState.create_initial()
    state.credits = 3000
    state.greenhouse.store(Plant("AaBb"))
    scene = MainGameScene.__new__(MainGameScene)
    scene.state = state
    scene._play_sound = lambda _sound_index: None

    assert not scene._buy_species_unlock()

    assert state.credits == 3000
    assert "Snapdragon" not in state.unlocked_species
    assert state.status_message == "Requires two empty garden slots."


def test_species_unlock_adds_dominant_and_recessive_founders() -> None:
    state = GameState.create_initial()
    state.credits = 3000
    scene = MainGameScene.__new__(MainGameScene)
    scene.state = state
    scene._play_sound = lambda _sound_index: None

    assert scene._buy_species_unlock()

    assert state.credits == 200
    assert "Snapdragon" in state.unlocked_species
    assert state.greenhouse.plant_at(2) == Plant(
        "AABBCC",
        species="Snapdragon",
    )
    assert state.greenhouse.plant_at(3) == Plant(
        "aabbcc",
        species="Snapdragon",
    )


def test_species_shop_card_handles_all_unlocked_species() -> None:
    state = GameState.create_initial()
    state.unlocked_species.update({"Snapdragon", "Corn", "Tomato", "Orchid"})
    scene = MainGameScene.__new__(MainGameScene)
    scene.state = state

    assert scene._species_card_data() == ("Species", "All unlocked", "DONE")


def test_dynamic_species_and_upgrade_text_uses_i18n_placeholders() -> None:
    set_language("pt-BR")
    state = GameState.create_initial()
    scene = MainGameScene.__new__(MainGameScene)
    scene.state = state
    scene.selected_shop_item = "analyzer"

    assert "Sequenciamento genetico" in scene._shop_details()[0]

    scene.selected_shop_item = "species"
    assert scene._shop_details()[0] == "Desbloqueie Boca-de-leao."
    assert scene._status_text("Unlocked Orchid.") == "Orquidea desbloqueado."


def test_contract_titles_translate_dynamic_i18n_placeholders() -> None:
    set_language("pt-BR")
    state = GameState.create_initial()
    scene = MainGameScene.__new__(MainGameScene)
    scene.state = state
    state.active_contract = PhenotypeContract(
        title="",
        target_count=2,
        reward_credits=100,
        species="Orchid",
        trait_requirements={"flower color": "violet"},
    )

    assert scene._contract_title() == "Entregue 2 Orquidea violeta"

    state.active_contract = PhenotypeContract(
        title="",
        target_count=1,
        reward_credits=100,
        kind="probability",
        resolution_mode="statistical",
        species="Tomato",
        trait_requirements={"maturation": "early"},
        min_probability=0.25,
    )

    assert scene._contract_title() == "Produza pelo menos 25% precoce"


def test_shop_purchase_requires_confirmation_before_spending() -> None:
    state = GameState.create_initial()
    state.credits = 50
    scene = MainGameScene.__new__(MainGameScene)
    scene.state = state
    scene.save_service = None
    scene.selected_shop_item = "slot"
    scene.shop_confirmation_open = False
    scene._play_sound = lambda _sound_index: None

    scene._request_shop_purchase()

    assert scene.shop_confirmation_open
    assert state.credits == 50
    assert state.greenhouse.capacity == 4

    assert scene._confirm_shop_purchase()
    assert not scene.shop_confirmation_open
    assert state.credits == 0
    assert state.greenhouse.capacity == 5


def test_reset_progression_restores_initial_game_state() -> None:
    state = GameState.create_initial()
    state.credits = 500
    state.analyzer_level = 3
    state.current_batch = [Plant("AaBb", generation=1)]
    state.visible_count = 1
    scene = MainGameScene.__new__(MainGameScene)
    scene.state = state
    scene.breeding = BreedingService(state)
    scene.greenhouse_service = GreenhouseService(state)
    scene.save_service = None
    scene.collection_tab = "Genotypes"
    scene.selected_knowledge = "Genetic probability"
    scene.selected_greenhouse_slot = 2
    scene.selected_shop_item = "analyzer"
    scene.shop_confirmation_open = True
    scene.parent_picker_target = "a"
    scene.active_screen = "shop"
    scene._reveal_frames = {0: 10}
    scene.germination_started_frame = 10

    scene._reset_progression()

    assert scene.state.credits == 0
    assert scene.state.analyzer_level == 1
    assert scene.state.current_batch == []
    assert scene.state.greenhouse.plant_at(0) == Plant("AABB")
    assert scene.state.greenhouse.plant_at(1) == Plant("aabb")
    assert scene.state.status_message == "Progress reset."
    assert scene.parent_picker_target is None
    assert not scene.shop_confirmation_open
    assert scene.active_screen == "main"


def test_reset_progression_requires_confirmation() -> None:
    state = GameState.create_initial()
    state.credits = 500
    scene = MainGameScene.__new__(MainGameScene)
    scene.state = state
    scene.breeding = BreedingService(state)
    scene.greenhouse_service = GreenhouseService(state)
    scene.save_service = None
    scene.collection_tab = "Species"
    scene.selected_knowledge = "Phenotype"
    scene.selected_greenhouse_slot = 0
    scene.selected_shop_item = "slot"
    scene.parent_picker_target = None
    scene.active_screen = "settings"
    scene._reveal_frames = {}
    scene.germination_started_frame = None
    scene._play_sound = lambda _sound_index: None

    scene._request_progress_reset()

    assert scene.reset_confirmation_open
    assert scene.state.credits == 500
    assert scene.state.status_message == "Reset requires confirmation."

    scene._confirm_progress_reset()

    assert not scene.reset_confirmation_open
    assert scene.state.credits == 0
    assert scene.state.status_message == "Progress reset."


def test_tester_money_code_grants_large_credit_balance() -> None:
    state = GameState.create_initial()
    scene = MainGameScene.__new__(MainGameScene)
    scene.state = state
    scene.save_service = None
    scene.tester_code_buffer = ""
    scene._play_sound = lambda _sound_index: None

    for character in "MONEYTRE":
        scene._handle_tester_code_character(character)

    assert state.credits == 0

    scene._handle_tester_code_character("E")

    assert state.credits == 999_999
    assert state.status_message == "Tester money code enabled."


def test_analyzer_reports_follow_unlocked_experiment_levels() -> None:
    state = GameState.create_initial()
    state.greenhouse.store(Plant("AaBb"))
    state.selected_parent_a = 2
    state.selected_parent_b = 2
    scene = MainGameScene.__new__(MainGameScene)
    scene.state = state
    scene._trait = lambda value: value

    assert scene._analyzer_phenotype_lines() == [
        "A: yellow / smooth",
        "B: yellow / smooth",
    ]
    assert scene._analyzer_genotype_lines() == [
        "A: AaBb",
        "B: AaBb",
    ]
    assert scene._analyzer_gamete_lines() == [
        "A: AB Ab aB ab",
        "B: AB Ab aB ab",
    ]
    assert scene._analyzer_allele_lines() == [
        "A A: Aa  B A: Aa",
        "A B: Bb  B B: Bb",
    ]

    state.analyzer_level = 3
    assert sorted(scene._probability_lines()) == [
        "green / smooth: 19%",
        "green / wrinkled: 6%",
        "yellow / smooth: 56%",
        "yellow / wrinkled: 19%",
    ]
    assert scene._punnett_columns() == ["AB", "Ab", "aB", "ab"]
    assert scene._punnett_rows() == [
        ("AB", ["AABB", "AABb", "AaBB", "AaBb"]),
        ("Ab", ["AABb", "AAbb", "AaBb", "Aabb"]),
        ("aB", ["AaBB", "AaBb", "aaBB", "aaBb"]),
        ("ab", ["AaBb", "Aabb", "aaBb", "aabb"]),
    ]


def test_punnett_square_is_hidden_before_probability_level() -> None:
    state = GameState.create_initial()
    scene = MainGameScene.__new__(MainGameScene)
    scene.state = state

    assert scene._punnett_columns() == []
    assert scene._punnett_rows() == []


def test_analyzer_view_buttons_respect_unlock_levels(monkeypatch) -> None:
    state = GameState.create_initial()
    scene = MainGameScene.__new__(MainGameScene)
    scene.state = state
    scene.analyzer_view = ANALYZER_VIEW_TRAITS
    scene._play_sound = lambda _sound_index: None
    scene._t = lambda text, **kwargs: text.format(**kwargs)
    button = ANALYZER_VIEW_BUTTONS[2]
    monkeypatch.setattr(pyxel, "mouse_x", button.x + 1)
    monkeypatch.setattr(pyxel, "mouse_y", button.y + 1)
    monkeypatch.setattr(
        pyxel,
        "btnp",
        lambda key: key == pyxel.MOUSE_BUTTON_LEFT,
    )

    assert scene._update_analyzer_view_buttons()
    assert scene.analyzer_view == ANALYZER_VIEW_TRAITS
    assert state.status_message == "Analyzer L3 required."

    state.analyzer_level = 3
    assert scene._update_analyzer_view_buttons()
    assert scene.analyzer_view == ANALYZER_VIEW_PUNNETT
    assert state.status_message == "Punnett"


def test_level_four_analyzer_finds_best_stored_contract_cross() -> None:
    state = GameState.create_initial()
    state.analyzer_level = 4
    scene = MainGameScene.__new__(MainGameScene)
    scene.state = state
    scene._trait = lambda value: value
    scene._t = lambda text, **kwargs: text.format(**kwargs)

    assert scene._best_contract_cross_lines() == [
        "Plant 1: AABB yellow / smooth",
        "Plant 2: aabb green / wrinkled",
        "Chance: 100%",
    ]


def test_analyzer_compacts_large_gamete_sets() -> None:
    assert (
        MainGameScene._compact_gametes(
            ("ABC", "ABc", "AbC", "Abc", "aBC", "aBc", "abC", "abc"),
        )
        == "ABC ABc +6"
    )


def test_species_unlocks_use_distinct_plant_sprite_coordinates() -> None:
    scene = MainGameScene.__new__(MainGameScene)

    snapdragon_coords = scene._plant_sprite_coords(
        Plant("AABBCC", species="Snapdragon"),
    )

    assert snapdragon_coords == (
        0,
        192,
    )
    assert scene._plant_sprite_coords(Plant("AABB", species="Mendel Pea")) == (
        0,
        0,
    )


def test_save_data_round_trips_state_without_pyxel_objects() -> None:
    state = GameState.create_initial()
    state.credits = 25
    state.analyzer_level = 2
    state.greenhouse.store(Plant("AaBb", generation=1))
    service = BreedingService(state)
    service.start_crossbreeding()

    payload = state_to_save_data(
        state,
        SaveMetadata(
            profile_id="profile-a",
            slot_id="slot-1",
            language="en",
            settings={"music_volume": 3},
        ),
    )
    restored = state_from_save_data(payload)

    assert restored.credits == 25
    assert restored.analyzer_level == 2
    assert restored.greenhouse.used_slots == 3
    assert restored.greenhouse.plant_at(2) == Plant("AaBb", generation=1)
    assert restored.current_batch[0] == state.current_batch[0]
    assert restored.current_batch[0].generation == 1
    assert restored.visible_count == 1
    assert restored.collection.genotypes == state.collection.genotypes


def test_genotypic_contract_unlocks_at_analyzer_level_two() -> None:
    state = GameState.create_initial()
    state.analyzer_level = 2
    state.greenhouse.store(Plant("AaBb"))
    state.collection.register_plant(Plant("AaBb"))

    contract = generate_next_contract(
        analyzer_level=state.analyzer_level,
        collection=state.collection,
        greenhouse=state.greenhouse,
        completed_contracts=2,
    )

    assert contract.kind == "genotype"
    assert contract.genotype in {"AABB", "AaBb", "aabb"}


def test_statistical_probability_contract_validates_whole_batch() -> None:
    contract = PhenotypeContract(
        title="Produce a 9:3:3:1 phenotype ratio",
        target_count=1,
        reward_credits=1500,
        kind="probability",
        resolution_mode="statistical",
        ratio=(9, 3, 3, 1),
    )
    batch = cross_batch = BreedingService(GameState.create_initial())
    state = cross_batch.state
    state.greenhouse.store(Plant("AaBb"))
    state.selected_parent_a = 2
    state.selected_parent_b = 2
    state.active_contract = contract
    state.current_batch = [
        Plant("AABB"),
        Plant("AABb"),
        Plant("AABb"),
        Plant("AAbb"),
        Plant("AaBB"),
        Plant("AaBB"),
        Plant("AaBb"),
        Plant("AaBb"),
        Plant("AaBb"),
        Plant("AaBb"),
        Plant("Aabb"),
        Plant("Aabb"),
        Plant("aaBB"),
        Plant("aaBb"),
        Plant("aaBb"),
        Plant("aabb"),
    ]

    assert batch.harvest_germination_batch()

    assert state.active_contract.completed


def test_save_service_scopes_files_by_profile_and_slot(tmp_path) -> None:
    profile_a = SaveService(
        tmp_path,
        SaveIdentity(profile_id="profile-a", slot_id="slot-1"),
    )
    profile_b = SaveService(
        tmp_path,
        SaveIdentity(profile_id="profile-b", slot_id="slot-1"),
    )
    state_a = GameState.create_initial()
    state_b = GameState.create_initial()
    state_a.credits = 10
    state_b.credits = 99

    profile_a.save(state_a, language="en", settings={})
    profile_b.save(state_b, language="en", settings={})

    loaded_a = profile_a.load()
    loaded_b = profile_b.load()

    assert loaded_a is not None
    assert loaded_b is not None
    assert loaded_a[0].credits == 10
    assert loaded_b[0].credits == 99
    assert profile_a.save_path != profile_b.save_path


def test_save_service_uses_browser_storage_on_web(
    monkeypatch,
    tmp_path,
) -> None:
    storage_data = {}

    def get_item(key: str) -> str | None:
        return storage_data.get(key)

    def set_item(key: str, value: str) -> None:
        storage_data[key] = value

    browser_storage = SimpleNamespace(
        getItem=get_item,
        setItem=set_item,
    )

    monkeypatch.setattr(sys, "platform", "emscripten")
    monkeypatch.setitem(
        sys.modules,
        "js",
        SimpleNamespace(localStorage=browser_storage),
    )
    service = SaveService(
        root_dir=tmp_path,
        identity=SaveIdentity(profile_id="web-profile", slot_id="slot-1"),
    )
    state = GameState.create_initial()
    state.credits = 77

    service.save(
        state,
        language="pt-BR",
        settings={"language": "pt-BR", "music_volume": 4},
    )

    reloaded_service = SaveService(
        root_dir=tmp_path,
        identity=SaveIdentity(profile_id="web-profile", slot_id="slot-1"),
    )
    loaded = reloaded_service.load()

    assert loaded is not None
    loaded_state, loaded_settings = loaded
    assert loaded_state.credits == 77
    assert loaded_settings["music_volume"] == 4
    assert list(storage_data) == [
        "mendels-greenhouse:save:web-profile:slot-1",
    ]


def test_save_service_ignores_empty_browser_storage(
    monkeypatch,
    tmp_path,
) -> None:
    def get_item(_key: str) -> str:
        return "undefined"

    def set_item(_key: str, _value: str) -> None:
        return None

    browser_storage = SimpleNamespace(
        getItem=get_item,
        setItem=set_item,
    )
    monkeypatch.setattr(sys, "platform", "emscripten")
    monkeypatch.setitem(
        sys.modules,
        "js",
        SimpleNamespace(localStorage=browser_storage),
    )
    service = SaveService(
        root_dir=tmp_path,
        identity=SaveIdentity(profile_id="web-profile", slot_id="slot-1"),
    )

    assert service.load() is None
