"""Versioned JSON save payloads for runtime game state."""

from dataclasses import dataclass
from datetime import UTC, datetime
from random import Random
from typing import Any

from mendels_greenhouse.core.collection import Collection
from mendels_greenhouse.core.contracts import (
    PhenotypeContract,
    create_tutorial_contract,
)
from mendels_greenhouse.core.genetics import SPECIES_MENDEL_PEA, Plant
from mendels_greenhouse.core.greenhouse import Greenhouse
from mendels_greenhouse.state.game_state import GameState

SCHEMA_VERSION = 1
DEFAULT_LANGUAGE = "pt-BR"


@dataclass(frozen=True)
class SaveMetadata:
    """Metadata needed to serialize one save document."""

    profile_id: str
    slot_id: str
    language: str = DEFAULT_LANGUAGE
    settings: dict[str, Any] | None = None
    created_at: str | None = None


def state_to_save_data(
    state: GameState,
    metadata: SaveMetadata,
) -> dict[str, Any]:
    """Serialize game state into the schema-versioned save document."""
    timestamp = _now()
    return {
        "schema_version": SCHEMA_VERSION,
        "language": metadata.language,
        "created_at": metadata.created_at or timestamp,
        "updated_at": timestamp,
        "profile": {
            "id": metadata.profile_id,
            "slot_id": metadata.slot_id,
        },
        "greenhouse": {
            "slots": [
                _plant_to_data(plant) for plant in state.greenhouse.slots
            ],
        },
        "collection": {
            "species": sorted(state.collection.species),
            "genotypes": sorted(state.collection.genotypes),
            "phenotypes": [
                {"seed_color": color, "seed_texture": texture}
                for color, texture in sorted(state.collection.phenotypes)
            ],
        },
        "progression": {
            "credits": state.credits,
            "analyzer_level": state.analyzer_level,
            "completed_contracts": state.completed_contracts,
            "unlocked_species": sorted(state.unlocked_species),
            "selected_parent_a": state.selected_parent_a,
            "selected_parent_b": state.selected_parent_b,
        },
        "contracts": {"active": _contract_to_data(state.active_contract)},
        "batch": {
            "visible_count": state.visible_count,
            "selected_offspring_index": state.selected_offspring_index,
            "plants": [_plant_to_data(plant) for plant in state.current_batch],
        },
        "settings": metadata.settings or {},
    }


def state_from_save_data(payload: dict[str, Any]) -> GameState:
    """Deserialize a save document into runtime game state."""
    schema_version = payload.get("schema_version")
    if schema_version != SCHEMA_VERSION:
        message = f"Unsupported save schema version: {schema_version}"
        raise ValueError(message)

    greenhouse_data = payload.get("greenhouse", {})
    greenhouse = Greenhouse(
        slots=[
            _plant_from_data(plant_data)
            for plant_data in greenhouse_data.get("slots", [])
        ],
    )
    if not greenhouse.slots:
        greenhouse = Greenhouse.create_initial()

    collection_data = payload.get("collection", {})
    collection = Collection(
        species=set(collection_data.get("species", [])),
        genotypes=set(collection_data.get("genotypes", [])),
        phenotypes={
            (
                phenotype_data["seed_color"],
                phenotype_data["seed_texture"],
            )
            for phenotype_data in collection_data.get("phenotypes", [])
        },
    )
    if not collection.species:
        collection.register_species(SPECIES_MENDEL_PEA)

    progression = payload.get("progression", {})
    batch = payload.get("batch", {})
    contracts = payload.get("contracts", {})
    state = GameState(
        greenhouse=greenhouse,
        collection=collection,
        active_contract=_contract_from_data(contracts.get("active")),
        credits=int(progression.get("credits", 0)),
        analyzer_level=int(progression.get("analyzer_level", 1)),
        completed_contracts=int(progression.get("completed_contracts", 0)),
        unlocked_species=set(
            progression.get("unlocked_species", [SPECIES_MENDEL_PEA]),
        ),
        selected_parent_a=int(progression.get("selected_parent_a", 0)),
        selected_parent_b=int(progression.get("selected_parent_b", 1)),
        current_batch=[
            _plant_from_data(plant_data)
            for plant_data in batch.get("plants", [])
        ],
        visible_count=int(batch.get("visible_count", 0)),
        selected_offspring_index=int(batch.get("selected_offspring_index", 0)),
        rng=Random(),
        status_message="Autosave loaded.",
    )
    _clamp_selection(state)
    return state


def save_settings_from_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Return saved settings from a payload."""
    settings = payload.get("settings", {})
    if not isinstance(settings, dict):
        return {}
    return settings


def _plant_to_data(plant: Plant | None) -> dict[str, str | int] | None:
    if plant is None:
        return None
    return {
        "genotype": plant.genotype,
        "species": plant.species,
        "generation": plant.generation,
    }


def _plant_from_data(data: object) -> Plant | None:
    if data is None:
        return None
    if not isinstance(data, dict):
        message = "Invalid plant payload."
        raise ValueError(message)
    return Plant(
        genotype=str(data["genotype"]),
        species=str(data.get("species", SPECIES_MENDEL_PEA)),
        generation=int(data.get("generation", 0)),
    )


def _contract_to_data(contract: PhenotypeContract) -> dict[str, Any]:
    return {
        "kind": "phenotype",
        "title": contract.title,
        "target_count": contract.target_count,
        "reward_credits": contract.reward_credits,
        "seed_color": contract.seed_color,
        "seed_texture": contract.seed_texture,
        "delivered_count": contract.delivered_count,
        "completed": contract.completed,
        "paid": contract.paid,
    }


def _contract_from_data(data: object) -> PhenotypeContract:
    if not isinstance(data, dict):
        return create_tutorial_contract()
    if data.get("kind", "phenotype") != "phenotype":
        return create_tutorial_contract()
    return PhenotypeContract(
        title=str(data.get("title", "Deliver 3 yellow smooth peas")),
        target_count=int(data.get("target_count", 3)),
        reward_credits=int(data.get("reward_credits", 50)),
        seed_color=data.get("seed_color"),
        seed_texture=data.get("seed_texture"),
        delivered_count=int(data.get("delivered_count", 0)),
        completed=bool(data.get("completed", False)),
        paid=bool(data.get("paid", False)),
    )


def _clamp_selection(state: GameState) -> None:
    capacity = max(state.greenhouse.capacity, 1)
    state.selected_parent_a = min(
        max(state.selected_parent_a, 0),
        capacity - 1,
    )
    state.selected_parent_b = min(
        max(state.selected_parent_b, 0),
        capacity - 1,
    )
    state.visible_count = min(
        max(state.visible_count, 0),
        len(state.current_batch),
    )
    if state.current_batch:
        state.selected_offspring_index = min(
            max(state.selected_offspring_index, 0),
            len(state.current_batch) - 1,
        )
    else:
        state.selected_offspring_index = 0


def _now() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat()
