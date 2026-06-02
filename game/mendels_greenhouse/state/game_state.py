"""Serializable runtime state for the playable MVP."""

from dataclasses import dataclass, field
from random import Random

from mendels_greenhouse.core.collection import Collection
from mendels_greenhouse.core.contracts import (
    PhenotypeContract,
    create_tutorial_contract,
)
from mendels_greenhouse.core.genetics import Plant
from mendels_greenhouse.core.greenhouse import Greenhouse

SPECIES_MENDEL_PEA = "Mendel Pea"


@dataclass
class GameState:
    """Current MVP game state independent from Pyxel drawing objects."""

    greenhouse: Greenhouse
    collection: Collection
    active_contract: PhenotypeContract
    credits: int = 0
    analyzer_level: int = 1
    completed_contracts: int = 0
    unlocked_species: set[str] = field(
        default_factory=lambda: {SPECIES_MENDEL_PEA},
    )
    selected_parent_a: int = 0
    selected_parent_b: int = 1
    current_batch: list[Plant] = field(default_factory=list)
    visible_count: int = 0
    rng: Random = field(default_factory=Random)
    status_message: str = "Select parents, then cross plants."

    @classmethod
    def create_initial(cls) -> "GameState":
        """Create the official MVP starting state."""
        greenhouse = Greenhouse.create_initial()
        collection = Collection()
        collection.register_species(SPECIES_MENDEL_PEA)
        for plant in greenhouse.slots:
            if plant is not None:
                collection.register_plant(plant)

        return cls(
            greenhouse=greenhouse,
            collection=collection,
            active_contract=create_tutorial_contract(),
        )

    @property
    def parent_a(self) -> Plant | None:
        """Return selected parent A."""
        return self.greenhouse.plant_at(self.selected_parent_a)

    @property
    def parent_b(self) -> Plant | None:
        """Return selected parent B."""
        return self.greenhouse.plant_at(self.selected_parent_b)

    @property
    def can_crossbreed(self) -> bool:
        """Return whether both parent slots contain plants."""
        return self.parent_a is not None and self.parent_b is not None

    @property
    def last_visible_plant(self) -> Plant | None:
        """Return the last revealed offspring."""
        if self.visible_count == 0:
            return None

        return self.current_batch[self.visible_count - 1]
