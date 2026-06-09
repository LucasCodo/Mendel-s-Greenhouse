"""Contract rules for delivery and statistical breeding goals."""

from collections import Counter
from dataclasses import dataclass, field
from itertools import combinations
from typing import Literal

from mendels_greenhouse.core.collection import (
    Collection,
    genotype_key,
    phenotype_key,
)
from mendels_greenhouse.core.content import (
    SPECIES_MENDEL_PEA,
    species_definition,
)
from mendels_greenhouse.core.genetics import Plant, expected_distribution
from mendels_greenhouse.core.greenhouse import Greenhouse

ContractKind = Literal["phenotype", "genotype", "probability"]
ResolutionMode = Literal["delivery", "statistical"]

LEVEL_1_TARGET_BASE = 3
LEVEL_1_TARGET_MAX = 10
LEVEL_1_REWARD_BASE = 50
LEVEL_1_REWARD_STEP = 25
GENOTYPE_TARGET_BASE = 2
GENOTYPE_REWARD_BASE = 300
PROBABILITY_REWARD_BASE = 1500
GENOTYPE_CONTRACT_LEVEL = 2
PROBABILITY_CONTRACT_LEVEL = 3
CONTRACT_MIX_PERIOD = 5
PROBABILITY_CONTRACT_SLOT = 4
GENOTYPE_CONTRACT_SLOTS = {2, 3}
MINIMUM_PROBABILITY_TARGET = 0.25


@dataclass
class PhenotypeContract:
    """A gameplay contract with delivery or statistical resolution."""

    title: str
    target_count: int
    reward_credits: int
    seed_color: str | None = None
    seed_texture: str | None = None
    delivered_count: int = 0
    completed: bool = False
    paid: bool = False
    kind: ContractKind = "phenotype"
    resolution_mode: ResolutionMode = "delivery"
    species: str = SPECIES_MENDEL_PEA
    trait_requirements: dict[str, str] = field(default_factory=dict)
    genotype: str | None = None
    min_probability: float | None = None
    ratio: tuple[int, ...] | None = None

    def __post_init__(self) -> None:
        if not self.trait_requirements:
            requirements = {}
            if self.seed_color is not None:
                requirements["seed color"] = self.seed_color
            if self.seed_texture is not None:
                requirements["seed texture"] = self.seed_texture
            self.trait_requirements = requirements

    @property
    def remaining_count(self) -> int:
        """Return the number of matching plants still required."""
        return max(self.target_count - self.delivered_count, 0)

    @property
    def progress_count(self) -> int:
        """Return display progress count."""
        if self.resolution_mode == "statistical":
            return int(self.completed)
        return self.delivered_count

    def matches(self, plant: Plant) -> bool:
        """Return whether a plant satisfies the per-specimen target."""
        if plant.species != self.species:
            return False
        if self.kind == "genotype":
            return plant.genotype == self.genotype
        phenotype = plant.phenotype
        return all(
            phenotype.traits.get(trait) == value
            for trait, value in self.trait_requirements.items()
        )

    def deliver(self, plant: Plant) -> bool:
        """Submit one plant to a delivery contract if it matches."""
        if (
            self.resolution_mode != "delivery"
            or self.completed
            or not self.matches(plant)
        ):
            return False

        self.delivered_count += 1
        self.completed = self.delivered_count >= self.target_count
        return True

    def validate_batch(self, plants: list[Plant]) -> bool:
        """Resolve a statistical contract against a generated batch."""
        if self.resolution_mode != "statistical" or self.completed:
            return False
        species_plants = [
            plant for plant in plants if plant.species == self.species
        ]
        if not species_plants:
            return False
        if self.ratio is not None:
            self.completed = _batch_matches_ratio(species_plants, self.ratio)
        elif self.min_probability is not None:
            self.completed = _batch_meets_minimum_probability(
                species_plants,
                self,
            )
        return self.completed

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
        species=SPECIES_MENDEL_PEA,
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

    mix_slot = completed_contracts % CONTRACT_MIX_PERIOD
    if (
        analyzer_level >= PROBABILITY_CONTRACT_LEVEL
        and mix_slot == PROBABILITY_CONTRACT_SLOT
    ):
        probability = _generate_probability_contract(greenhouse)
        if probability is not None:
            return probability
    if (
        analyzer_level >= GENOTYPE_CONTRACT_LEVEL
        and mix_slot in GENOTYPE_CONTRACT_SLOTS
    ):
        genotype = _generate_genotype_contract(
            collection=collection,
            greenhouse=greenhouse,
            completed_contracts=completed_contracts,
        )
        if genotype is not None:
            return genotype

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
        candidates = [
            (
                SPECIES_MENDEL_PEA,
                (("seed color", "yellow"), ("seed texture", "smooth")),
            ),
        ]

    species, traits = candidates[completed_contracts % len(candidates)]
    requirements = dict(traits)
    target_count = min(
        LEVEL_1_TARGET_BASE + completed_contracts // max(len(candidates), 1),
        LEVEL_1_TARGET_MAX,
    )
    reward = LEVEL_1_REWARD_BASE + completed_contracts * LEVEL_1_REWARD_STEP
    return PhenotypeContract(
        title=_phenotype_contract_title(target_count, species, requirements),
        target_count=target_count,
        reward_credits=reward,
        species=species,
        trait_requirements=requirements,
    )


def _generate_genotype_contract(
    *,
    collection: Collection,
    greenhouse: Greenhouse,
    completed_contracts: int,
) -> PhenotypeContract | None:
    candidates = sorted(
        collection.genotypes & _reachable_genotypes(greenhouse),
    )
    if not candidates:
        return None
    species, genotype = candidates[completed_contracts % len(candidates)]
    definition = species_definition(species)
    reward = GENOTYPE_REWARD_BASE * definition.complexity
    target_count = min(GENOTYPE_TARGET_BASE + completed_contracts // 5, 8)
    return PhenotypeContract(
        title=f"Deliver {target_count} {genotype} {species}",
        target_count=target_count,
        reward_credits=reward,
        kind="genotype",
        species=species,
        genotype=genotype,
    )


def _generate_probability_contract(
    greenhouse: Greenhouse,
) -> PhenotypeContract | None:
    for parent_a, parent_b in _stored_pairs(greenhouse):
        distribution = expected_distribution(parent_a, parent_b)
        phenotype_counts = Counter(
            phenotype_key(
                Plant(genotype, species=parent_a.species).phenotype,
            )
            for genotype, count in distribution.genotype_counts.items()
            for _ in range(count)
        )
        if tuple(sorted(phenotype_counts.values(), reverse=True)) == (
            9,
            3,
            3,
            1,
        ):
            return PhenotypeContract(
                title="Produce a 9:3:3:1 phenotype ratio",
                target_count=1,
                reward_credits=PROBABILITY_REWARD_BASE,
                kind="probability",
                resolution_mode="statistical",
                species=parent_a.species,
                ratio=(9, 3, 3, 1),
            )
    return _generate_minimum_probability_contract(greenhouse)


def _generate_minimum_probability_contract(
    greenhouse: Greenhouse,
) -> PhenotypeContract | None:
    for parent_a, parent_b in _stored_pairs(greenhouse):
        distribution = expected_distribution(parent_a, parent_b)
        for genotype, count in distribution.genotype_counts.items():
            probability = count / distribution.total_combinations
            if probability < MINIMUM_PROBABILITY_TARGET:
                continue
            plant = Plant(genotype, species=parent_a.species)
            trait_name, trait_value = next(
                iter(plant.phenotype.traits.items()),
            )
            return PhenotypeContract(
                title=f"Produce at least 25% {trait_value}",
                target_count=1,
                reward_credits=PROBABILITY_REWARD_BASE,
                kind="probability",
                resolution_mode="statistical",
                species=parent_a.species,
                trait_requirements={trait_name: trait_value},
                min_probability=MINIMUM_PROBABILITY_TARGET,
            )
    return None


def _reachable_phenotypes(greenhouse: Greenhouse) -> set[tuple[str, tuple]]:
    reachable: set[tuple[str, tuple]] = set()
    for parent_a, parent_b in _stored_pairs(greenhouse):
        distribution = expected_distribution(parent_a, parent_b)
        for genotype in distribution.genotype_counts:
            plant = Plant(genotype, species=parent_a.species)
            reachable.add(phenotype_key(plant.phenotype))
    return reachable


def _reachable_genotypes(greenhouse: Greenhouse) -> set[tuple[str, str]]:
    reachable: set[tuple[str, str]] = set()
    for parent_a, parent_b in _stored_pairs(greenhouse):
        distribution = expected_distribution(parent_a, parent_b)
        for genotype in distribution.genotype_counts:
            reachable.add(
                genotype_key(Plant(genotype, species=parent_a.species)),
            )
    return reachable


def _stored_pairs(greenhouse: Greenhouse) -> list[tuple[Plant, Plant]]:
    stored_plants = [plant for plant in greenhouse.slots if plant is not None]
    return [
        (parent_a, parent_b)
        for parent_a, parent_b in combinations(stored_plants, 2)
        if parent_a.species == parent_b.species
    ]


def _phenotype_contract_title(
    target_count: int,
    species: str,
    requirements: dict[str, str],
) -> str:
    values = " ".join(requirements.values())
    return f"Deliver {target_count} {values} {species}"


def _batch_matches_ratio(plants: list[Plant], ratio: tuple[int, ...]) -> bool:
    counts = Counter(phenotype_key(plant.phenotype) for plant in plants)
    return tuple(sorted(counts.values(), reverse=True)) == ratio


def _batch_meets_minimum_probability(
    plants: list[Plant],
    contract: PhenotypeContract,
) -> bool:
    matches = sum(contract.matches(plant) for plant in plants)
    return matches / len(plants) >= (contract.min_probability or 0)
