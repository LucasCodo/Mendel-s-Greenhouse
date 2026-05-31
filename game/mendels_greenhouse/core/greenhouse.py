"""Greenhouse storage rules."""

from dataclasses import dataclass

from mendels_greenhouse.core.genetics import Plant

INITIAL_CAPACITY = 4
MAX_CAPACITY = 20


@dataclass
class Greenhouse:
    """Fixed-capacity plant storage for the MVP."""

    slots: list[Plant | None]

    @classmethod
    def create_initial(cls) -> "Greenhouse":
        """Create the official starting greenhouse."""
        return cls(slots=[Plant("AABB"), Plant("aabb"), None, None])

    @property
    def capacity(self) -> int:
        """Return available slot count."""
        return len(self.slots)

    @property
    def used_slots(self) -> int:
        """Return occupied slot count."""
        return sum(plant is not None for plant in self.slots)

    @property
    def free_slots(self) -> int:
        """Return empty slot count."""
        return self.capacity - self.used_slots

    def plant_at(self, index: int) -> Plant | None:
        """Return the plant stored at a slot."""
        return self.slots[index]

    def first_empty_slot(self) -> int | None:
        """Return the first empty slot index, if one exists."""
        for index, plant in enumerate(self.slots):
            if plant is None:
                return index
        return None

    def store(self, plant: Plant) -> int | None:
        """Store a plant and return the slot index used."""
        slot_index = self.first_empty_slot()
        if slot_index is None:
            return None

        self.slots[slot_index] = plant
        return slot_index

    def remove(self, index: int) -> Plant | None:
        """Remove and return a plant from a slot."""
        plant = self.slots[index]
        self.slots[index] = None
        return plant

    def expand(self) -> bool:
        """Add one storage slot until the maximum capacity is reached."""
        if self.capacity >= MAX_CAPACITY:
            return False

        self.slots.append(None)
        return True
