"""Tests for MVP state, storage, and contract services."""

from mendels_greenhouse.core.contracts import create_tutorial_contract
from mendels_greenhouse.core.genetics import Plant
from mendels_greenhouse.services.breeding_service import BreedingService
from mendels_greenhouse.services.greenhouse_service import GreenhouseService
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

    assert len(state.current_batch) == 1
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
