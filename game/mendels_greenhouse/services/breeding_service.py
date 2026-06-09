"""Application service for crossbreeding and germination resolution."""

from mendels_greenhouse.core.content import (
    COLLECTION_MILESTONE_REWARDS,
    DISCOVERY_REWARDS,
)
from mendels_greenhouse.core.contracts import generate_next_contract
from mendels_greenhouse.core.genetics import (
    Plant,
    crossbreed,
    expected_distribution,
)
from mendels_greenhouse.state.game_state import GameState

MAX_GERMINATION_BED_SIZE = 20
SPECIMEN_SALE_VALUE = 2


class BreedingService:
    """Mutate game state through the official breeding loop."""

    def __init__(self, state: GameState) -> None:
        self.state = state

    def start_crossbreeding(self) -> bool:
        """Generate one shuffled offspring batch from selected parents."""
        if self.state.current_batch:
            self.state.status_message = "Generating offspring..."
            return False
        if not self.state.can_crossbreed:
            self.state.status_message = "Select two stored parent plants."
            return False

        parent_a = self.state.parent_a
        parent_b = self.state.parent_b
        if parent_a is None or parent_b is None:
            self.state.status_message = "Select two stored parent plants."
            return False
        if parent_a.species != parent_b.species:
            self.state.status_message = "Select parents from the same species."
            return False

        batch_size = representative_bed_size(parent_a, parent_b)
        self.state.current_batch = crossbreed(
            parent_a,
            parent_b,
            count=batch_size,
            rng=self.state.rng,
        )
        self.state.visible_count = len(self.state.current_batch)
        self.state.selected_offspring_index = 0
        self.state.status_message = "Generating offspring..."
        return True

    def harvest_germination_batch(self) -> bool:
        """Harvest grown specimens into contract delivery or sale."""
        if not self.state.current_batch:
            return False

        plants = [
            plant for plant in self.state.current_batch if plant is not None
        ]
        statistical_completed = self.state.active_contract.validate_batch(
            plants,
        )
        delivered_count = 0
        sold_count = 0
        discovery_reward = 0
        for plant in self.state.current_batch:
            if plant is None:
                continue
            discovery_reward += self._register_plant_discoveries(plant)
            if (
                not statistical_completed
                and not self.state.active_contract.completed
                and self.state.active_contract.deliver(plant)
            ):
                delivered_count += 1
            else:
                sold_count += 1

        milestone_reward = self._claim_collection_milestones()
        reward_total = discovery_reward + milestone_reward
        if reward_total:
            self.state.credits += reward_total
        if sold_count:
            self.state.credits += sold_count * SPECIMEN_SALE_VALUE
        self.state.current_batch = []
        self.state.visible_count = 0
        self.state.selected_offspring_index = 0

        self._set_harvest_status(
            statistical_completed=statistical_completed,
            delivered_count=delivered_count,
            reward_total=reward_total,
            sold_count=sold_count,
        )

        return (
            delivered_count > 0
            or sold_count > 0
            or reward_total > 0
            or statistical_completed
        )

    def reveal_next(self) -> bool:
        """Reveal the next offspring and apply discovery/contract checks."""
        if self.state.visible_count >= len(self.state.current_batch):
            return False

        self.state.visible_count += 1
        revealed_index = self.state.visible_count - 1
        self.state.selected_offspring_index = revealed_index
        plant = self.state.current_batch[revealed_index]
        if plant is None:
            return False

        discovery_reward = self._register_plant_discoveries(plant)
        milestone_reward = self._claim_collection_milestones()
        reward = discovery_reward + milestone_reward
        if reward:
            self.state.credits += reward
        delivered = self.state.active_contract.deliver(plant)

        if delivered and self.state.active_contract.completed:
            self.state.status_message = "Contract complete. Claim reward."
        elif delivered:
            remaining = self.state.active_contract.remaining_count
            self.state.status_message = f"Contract match. {remaining} left."
        elif reward:
            self.state.status_message = (
                f"Discovery rewards. +{reward} credits."
            )
        else:
            self.state.status_message = "Offspring revealed."

        return True

    def _set_harvest_status(
        self,
        *,
        statistical_completed: bool,
        delivered_count: int,
        reward_total: int,
        sold_count: int,
    ) -> None:
        if statistical_completed:
            self.state.status_message = "Statistical contract complete."
        elif delivered_count and self.state.active_contract.completed:
            self.state.status_message = "Contract complete. Claim reward."
        elif delivered_count:
            remaining = self.state.active_contract.remaining_count
            self.state.status_message = f"Contract match. {remaining} left."
        elif reward_total:
            self.state.status_message = (
                f"Discovery rewards. +{reward_total} credits."
            )
        elif sold_count:
            credits = sold_count * SPECIMEN_SALE_VALUE
            self.state.status_message = f"Sold specimen for {credits} credits."
        else:
            self.state.status_message = "Offspring revealed."

    def claim_contract_reward(self) -> bool:
        """Claim a completed contract reward and generate the next contract."""
        reward = self.state.active_contract.claim_reward()
        if reward == 0:
            self.state.status_message = "No completed contract to claim."
            return False

        self.state.credits += reward
        self.state.completed_contracts += 1
        self.state.active_contract = generate_next_contract(
            analyzer_level=self.state.analyzer_level,
            collection=self.state.collection,
            greenhouse=self.state.greenhouse,
            completed_contracts=self.state.completed_contracts,
        )
        self.state.status_message = (
            f"Reward claimed. +{reward} credits. New contract ready."
        )
        return True

    def store_last_revealed(self) -> bool:
        """Store the latest revealed plant if there is greenhouse space."""
        return self.store_selected_offspring()

    def store_selected_offspring(self) -> bool:
        """Store the selected offspring and clear its bed cell."""
        plant = self.state.selected_offspring
        if plant is None:
            self.state.status_message = "No selected specimen to store."
            return False

        if self.state.greenhouse.has_genotype(plant.genotype):
            self.state.status_message = "Genotype already stored."
            return False

        slot_index = self.state.greenhouse.store(plant)
        if slot_index is None:
            self.state.status_message = "Greenhouse is full."
            return False

        discovery_reward = self._register_plant_discoveries(plant)
        milestone_reward = self._claim_collection_milestones()
        reward = discovery_reward + milestone_reward
        if reward:
            self.state.credits += reward
        self.state.current_batch[self.state.selected_offspring_index] = None
        if reward:
            self.state.status_message = (
                f"Stored plant in slot {slot_index + 1}. +{reward} credits."
            )
        else:
            self.state.status_message = (
                f"Stored plant in slot {slot_index + 1}."
            )
        return True

    def _register_plant_discoveries(self, plant: Plant) -> int:
        before_genotypes = len(self.state.collection.genotypes)
        before_phenotypes = len(self.state.collection.phenotypes)
        self.state.collection.register_plant(plant)
        reward = 0
        if len(self.state.collection.genotypes) > before_genotypes:
            reward += DISCOVERY_REWARDS["genotype"]
        if len(self.state.collection.phenotypes) > before_phenotypes:
            reward += DISCOVERY_REWARDS["phenotype"]
        return reward

    def _claim_collection_milestones(self) -> int:
        completion = self.state.collection.completion_percent
        reward = 0
        for milestone, credits in COLLECTION_MILESTONE_REWARDS.items():
            if milestone > completion:
                continue
            if milestone in self.state.claimed_collection_milestones:
                continue
            self.state.claimed_collection_milestones.add(milestone)
            reward += credits
        return reward


def representative_bed_size(parent_a: Plant, parent_b: Plant) -> int:
    """Return the displayed batch size for a parent cross."""
    total_combinations = expected_distribution(
        parent_a,
        parent_b,
    ).total_combinations
    return min(total_combinations, MAX_GERMINATION_BED_SIZE)
