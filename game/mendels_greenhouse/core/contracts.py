"""Contract rules for the MVP phenotype delivery loop."""

from dataclasses import dataclass
from itertools import combinations

from mendels_greenhouse.core.collection import Collection, phenotype_key
from mendels_greenhouse.core.genetics import Plant, expected_distribution
from mendels_greenhouse.core.greenhouse import Greenhouse

LEVEL_1_TARGET_BASE = 3
LEVEL_1_TARGET_MAX = 6
LEVEL_1_REWARD_BASE = 50
LEVEL_1_REWARD_STEP = 15


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


def generate_next_contract(
    *,
    analyzer_level: int,
    collection: Collection,
    greenhouse: Greenhouse,
    completed_contracts: int,
) -> PhenotypeContract:
    """Generate a valid next contract from unlocked progression."""
    if analyzer_level < 1:
        message = "Analyzer level must be at least 1."
        raise ValueError(message)

    return _generate_phenotype_contract(
        collection=collection,
        greenhouse=greenhouse,
        completed_contracts=completed_contracts,
    )


def _generate_phenotype_contract(
    *,
    collection: Collection,
    greenhouse: Greenhouse,
    completed_contracts: int,
) -> PhenotypeContract:
    candidates = sorted(
        collection.phenotypes & _reachable_phenotypes(greenhouse),
    )
    if not candidates:
        candidates = [("yellow", "smooth")]

    candidate_index = completed_contracts % len(candidates)
    seed_color, seed_texture = candidates[candidate_index]
    target_count = min(
        LEVEL_1_TARGET_BASE + completed_contracts // max(len(candidates), 1),
        LEVEL_1_TARGET_MAX,
    )
    reward = LEVEL_1_REWARD_BASE + completed_contracts * LEVEL_1_REWARD_STEP
    return PhenotypeContract(
        title=_phenotype_contract_title(
            target_count,
            seed_color,
            seed_texture,
        ),
        target_count=target_count,
        reward_credits=reward,
        seed_color=seed_color,
        seed_texture=seed_texture,
    )


def _reachable_phenotypes(greenhouse: Greenhouse) -> set[tuple[str, str]]:
    stored_plants = [plant for plant in greenhouse.slots if plant is not None]
    reachable: set[tuple[str, str]] = set()
    for parent_a, parent_b in combinations(stored_plants, 2):
        if parent_a.species != parent_b.species:
            continue
        distribution = expected_distribution(parent_a, parent_b)
        for genotype in distribution.genotype_counts:
            reachable.add(phenotype_key(Plant(genotype).phenotype))
    return reachable


def _phenotype_contract_title(
    target_count: int,
    seed_color: str,
    seed_texture: str,
) -> str:
    return f"Deliver {target_count} {seed_color} {seed_texture} peas"
