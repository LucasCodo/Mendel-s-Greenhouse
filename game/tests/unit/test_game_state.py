"""Tests for MVP state, storage, and contract services."""

from mendels_greenhouse.core.contracts import create_tutorial_contract
from mendels_greenhouse.core.genetics import Plant
from mendels_greenhouse.core.save_data import (
    SaveMetadata,
    state_from_save_data,
    state_to_save_data,
)
from mendels_greenhouse.services.breeding_service import BreedingService
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


def test_breeding_service_generates_representative_batch_size() -> None:
    state = GameState.create_initial()
    service = BreedingService(state)

    assert service.start_crossbreeding()

    assert len(state.current_batch) == 20
    assert state.visible_count == 0


def test_breeding_service_reveal_updates_collection_and_contract() -> None:
    state = GameState.create_initial()
    service = BreedingService(state)
    service.start_crossbreeding()

    assert service.reveal_next()

    assert state.visible_count == 1
    assert state.active_contract.delivered_count == 1
    assert "AaBb" in state.collection.genotypes
    assert state.credits == 0


def test_store_last_revealed_uses_empty_greenhouse_slot() -> None:
    state = GameState.create_initial()
    service = BreedingService(state)
    service.start_crossbreeding()
    service.reveal_next()

    assert service.store_last_revealed()

    assert state.greenhouse.used_slots == 3
    assert state.current_batch[state.selected_offspring_index] is None


def test_sell_selected_offspring_clears_bed_cell_and_adds_credits() -> None:
    state = GameState.create_initial()
    service = BreedingService(state)
    service.start_crossbreeding()
    service.reveal_next()

    assert service.sell_selected_offspring()

    assert state.credits == 2
    assert state.current_batch[state.selected_offspring_index] is None


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
        assert service.reveal_next()

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


def test_save_data_round_trips_state_without_pyxel_objects() -> None:
    state = GameState.create_initial()
    state.credits = 25
    state.analyzer_level = 2
    state.greenhouse.store(Plant("AaBb"))
    service = BreedingService(state)
    service.start_crossbreeding()
    service.reveal_next()

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
    assert restored.current_batch[0] == state.current_batch[0]
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
