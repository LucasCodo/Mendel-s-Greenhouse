"""Application service for greenhouse selection and discard actions."""

from typing import Literal

from mendels_greenhouse.state.game_state import GameState

ParentSlot = Literal["a", "b"]


class GreenhouseService:
    """Mutate game state through greenhouse-related player actions."""

    def __init__(self, state: GameState) -> None:
        self.state = state

    def select_parent(self, parent: ParentSlot, slot_index: int) -> bool:
        """Select a parent plant and keep parent species compatible."""
        plant = self.state.greenhouse.plant_at(slot_index)
        if plant is None:
            self.state.status_message = "Choose an occupied garden slot."
            return False

        if parent == "a":
            self.state.selected_parent_a = slot_index
            self._randomize_incompatible_other_parent(
                selected_index=slot_index,
                other_parent="b",
            )
            self.state.status_message = "Parent A selected from garden."
            return True

        self.state.selected_parent_b = slot_index
        self._randomize_incompatible_other_parent(
            selected_index=slot_index,
            other_parent="a",
        )
        self.state.status_message = "Parent B selected from garden."
        return True

    def discard_plant(self, slot_index: int) -> bool:
        """Discard a non-protected plant from the greenhouse."""
        plant = self.state.greenhouse.plant_at(slot_index)
        if plant is None:
            self.state.status_message = "Choose an occupied garden slot."
            return False
        if plant.is_protected_founder:
            self.state.status_message = (
                "Founder genotypes cannot be discarded."
            )
            return False

        self.state.greenhouse.discard(slot_index)
        self._repair_parent_after_discard(slot_index)
        self.state.status_message = (
            f"Discarded plant from slot {slot_index + 1}."
        )
        return True

    def _randomize_incompatible_other_parent(
        self,
        *,
        selected_index: int,
        other_parent: ParentSlot,
    ) -> None:
        selected = self.state.greenhouse.plant_at(selected_index)
        if selected is None:
            return

        other_index = (
            self.state.selected_parent_b
            if other_parent == "b"
            else self.state.selected_parent_a
        )
        other = self.state.greenhouse.plant_at(other_index)
        if other is None or other.species == selected.species:
            return

        candidates = self.state.greenhouse.compatible_slot_indices(
            selected.species,
            exclude=selected_index,
        )
        if not candidates:
            return

        replacement = self.state.rng.choice(candidates)
        if other_parent == "b":
            self.state.selected_parent_b = replacement
        else:
            self.state.selected_parent_a = replacement

    def _repair_parent_after_discard(self, discarded_index: int) -> None:
        if self.state.selected_parent_a == discarded_index:
            self.state.selected_parent_a = self._first_occupied_slot()
        if self.state.selected_parent_b == discarded_index:
            self.state.selected_parent_b = self._first_occupied_slot()

    def _first_occupied_slot(self) -> int:
        for index, plant in enumerate(self.state.greenhouse.slots):
            if plant is not None:
                return index
        return 0
