"""Application service for crossbreeding and offspring reveal."""

from mendels_greenhouse.core.genetics import crossbreed
from mendels_greenhouse.state.game_state import BATCH_SIZE, GameState


class BreedingService:
    """Mutate game state through the official breeding loop."""

    def __init__(self, state: GameState) -> None:
        self.state = state

    def start_crossbreeding(self) -> bool:
        """Generate one shuffled offspring batch from selected parents."""
        if not self.state.can_crossbreed:
            self.state.status_message = "Select two stored parent plants."
            return False

        parent_a = self.state.parent_a
        parent_b = self.state.parent_b
        if parent_a is None or parent_b is None:
            self.state.status_message = "Select two stored parent plants."
            return False

        self.state.current_batch = crossbreed(
            parent_a,
            parent_b,
            count=BATCH_SIZE,
            rng=self.state.rng,
        )
        self.state.visible_count = 0
        self.state.status_message = "Generating offspring..."
        return True

    def reveal_next(self) -> bool:
        """Reveal the next offspring and apply discovery/contract checks."""
        if self.state.visible_count >= len(self.state.current_batch):
            return False

        self.state.visible_count += 1
        plant = self.state.last_visible_plant
        if plant is None:
            return False

        is_discovery = self.state.collection.register_plant(plant)
        delivered = self.state.active_contract.deliver(plant)
        reward = self.state.active_contract.claim_reward()
        self.state.credits += reward

        if reward:
            self.state.status_message = (
                f"Contract complete. +{reward} credits."
            )
        elif delivered:
            remaining = self.state.active_contract.remaining_count
            self.state.status_message = f"Contract match. {remaining} left."
        elif is_discovery:
            self.state.status_message = "New discovery registered."
        else:
            self.state.status_message = "Offspring revealed."

        return True

    def store_last_revealed(self) -> bool:
        """Store the latest revealed plant if there is greenhouse space."""
        plant = self.state.last_visible_plant
        if plant is None:
            self.state.status_message = "No revealed plant to store."
            return False

        slot_index = self.state.greenhouse.store(plant)
        if slot_index is None:
            self.state.status_message = "Greenhouse is full."
            return False

        self.state.status_message = f"Stored plant in slot {slot_index + 1}."
        return True
