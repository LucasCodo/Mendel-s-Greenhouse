"""Tests for MVP state, storage, and contract services."""

from mendels_greenhouse.core.contracts import create_tutorial_contract
from mendels_greenhouse.core.genetics import Plant
from mendels_greenhouse.services.breeding_service import BreedingService
from mendels_greenhouse.state.game_state import BATCH_SIZE, GameState


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


def test_breeding_service_generates_official_batch_size() -> None:
    state = GameState.create_initial()
    service = BreedingService(state)

    assert service.start_crossbreeding()

    assert len(state.current_batch) == BATCH_SIZE
    assert state.visible_count == 0


def test_breeding_service_reveal_updates_collection_and_contract() -> None:
    state = GameState.create_initial()
    service = BreedingService(state)
    service.start_crossbreeding()

    assert service.reveal_next()

    assert state.visible_count == 1
    assert state.active_contract.delivered_count == 1
    assert "AaBb" in state.collection.genotypes


def test_store_last_revealed_uses_empty_greenhouse_slot() -> None:
    state = GameState.create_initial()
    service = BreedingService(state)
    service.start_crossbreeding()
    service.reveal_next()

    assert service.store_last_revealed()

    assert state.greenhouse.used_slots == 3
