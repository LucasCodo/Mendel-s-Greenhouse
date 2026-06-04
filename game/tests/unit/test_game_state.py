"""Tests for MVP state, storage, and contract services."""

from mendels_greenhouse.core.contracts import create_tutorial_contract
from mendels_greenhouse.core.genetics import Plant
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
    assert "AaBb" in state.collection.genotypes
    assert state.credits == 0


def test_breeding_service_sells_non_contract_specimens_after_growth() -> None:
    state = GameState.create_initial()
    state.current_batch = [Plant("AaBb"), Plant("aabb")]
    state.visible_count = 2
    service = BreedingService(state)

    assert service.harvest_germination_batch()

    assert state.active_contract.delivered_count == 1
    assert state.credits == 2
    assert state.current_batch == []


def test_store_last_revealed_uses_empty_greenhouse_slot() -> None:
    state = GameState.create_initial()
    service = BreedingService(state)
    service.start_crossbreeding()

    assert service.store_last_revealed()

    assert state.greenhouse.used_slots == 3
    assert state.current_batch[state.selected_offspring_index] is None


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
        Plant("AABB", species="Snapdragon"),
        Plant("AaBb", species="Snapdragon"),
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
    assert state.credits == 0

    assert service.claim_contract_reward()

    assert state.credits == 50
    assert state.completed_contracts == 1
    assert not state.active_contract.completed
    assert state.active_contract.target_count == 4
    assert state.active_contract.seed_color == "yellow"
    assert state.active_contract.seed_texture == "smooth"


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

    assert state.credits == 0
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
    state.unlocked_species.update({"Snapdragon", "Corn"})
    scene = MainGameScene.__new__(MainGameScene)
    scene.state = state

    assert scene._species_card_data() == ("Species", "All unlocked", "DONE")


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
    assert scene.active_screen == "main"


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
