"""Contract rules for the MVP phenotype delivery loop."""

from dataclasses import dataclass

from mendels_greenhouse.core.genetics import Plant


@dataclass
class PhenotypeContract:
    """A delivery contract based on visible Mendel Pea traits."""

    title: str
    target_count: int
    reward_credits: int
    seed_color: str | None = None
    seed_texture: str | None = None
    delivered_count: int = 0
    completed: bool = False
    paid: bool = False

    @property
    def remaining_count(self) -> int:
        """Return the number of matching plants still required."""
        return max(self.target_count - self.delivered_count, 0)

    def matches(self, plant: Plant) -> bool:
        """Return whether a plant satisfies the contract phenotype."""
        phenotype = plant.phenotype
        color_matches = (
            self.seed_color is None or phenotype.seed_color == self.seed_color
        )
        texture_matches = (
            self.seed_texture is None
            or phenotype.seed_texture == self.seed_texture
        )
        return color_matches and texture_matches

    def deliver(self, plant: Plant) -> bool:
        """Submit one plant to the contract if it matches."""
        if self.completed or not self.matches(plant):
            return False

        self.delivered_count += 1
        self.completed = self.delivered_count >= self.target_count
        return True

    def claim_reward(self) -> int:
        """Return the reward exactly once after completion."""
        if not self.completed or self.paid:
            return 0

        self.paid = True
        return self.reward_credits


def create_tutorial_contract() -> PhenotypeContract:
    """Create the first MVP contract."""
    return PhenotypeContract(
        title="Deliver 3 yellow smooth peas",
        target_count=3,
        reward_credits=50,
        seed_color="yellow",
        seed_texture="smooth",
    )
