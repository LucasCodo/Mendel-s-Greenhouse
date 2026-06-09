"""Official content and balance data used by gameplay systems."""

from dataclasses import dataclass

SPECIES_MENDEL_PEA = "Mendel Pea"
SPECIES_SNAPDRAGON = "Snapdragon"
SPECIES_CORN = "Corn"
SPECIES_TOMATO = "Tomato"
SPECIES_ORCHID = "Orchid"


@dataclass(frozen=True)
class TraitRule:
    """Complete-dominance phenotype rule for one gene."""

    gene: str
    name: str
    dominant: str
    recessive: str


@dataclass(frozen=True)
class SpeciesDefinition:
    """Playable species content definition."""

    name: str
    gene_count: int
    traits: tuple[TraitRule, ...]
    unlock_cost: int | None
    complexity: int


SPECIES_DEFINITIONS = {
    SPECIES_MENDEL_PEA: SpeciesDefinition(
        name=SPECIES_MENDEL_PEA,
        gene_count=2,
        unlock_cost=0,
        complexity=1,
        traits=(
            TraitRule("A", "seed color", "yellow", "green"),
            TraitRule("B", "seed texture", "smooth", "wrinkled"),
        ),
    ),
    SPECIES_SNAPDRAGON: SpeciesDefinition(
        name=SPECIES_SNAPDRAGON,
        gene_count=3,
        unlock_cost=3000,
        complexity=2,
        traits=(
            TraitRule("A", "flower color", "red", "white"),
            TraitRule("B", "plant height", "tall", "short"),
            TraitRule("C", "petal shape", "wide", "narrow"),
        ),
    ),
    SPECIES_CORN: SpeciesDefinition(
        name=SPECIES_CORN,
        gene_count=4,
        unlock_cost=10000,
        complexity=3,
        traits=(
            TraitRule("A", "kernel color", "purple", "yellow"),
            TraitRule("B", "ear size", "large", "small"),
            TraitRule("C", "plant height", "tall", "short"),
            TraitRule("D", "row count", "many-row", "few-row"),
        ),
    ),
    SPECIES_TOMATO: SpeciesDefinition(
        name=SPECIES_TOMATO,
        gene_count=5,
        unlock_cost=25000,
        complexity=4,
        traits=(
            TraitRule("A", "fruit color", "red", "yellow"),
            TraitRule("B", "fruit size", "large", "small"),
            TraitRule("C", "fruit shape", "round", "pear-shaped"),
            TraitRule("D", "resistance", "resistant", "susceptible"),
            TraitRule("E", "maturation", "early", "late"),
        ),
    ),
    SPECIES_ORCHID: SpeciesDefinition(
        name=SPECIES_ORCHID,
        gene_count=6,
        unlock_cost=60000,
        complexity=5,
        traits=(
            TraitRule("A", "flower color", "violet", "white"),
            TraitRule("B", "flower size", "large", "small"),
            TraitRule("C", "petal count", "many-petal", "few-petal"),
            TraitRule("D", "aroma", "fragrant", "neutral"),
            TraitRule("E", "flower shape", "star", "round"),
            TraitRule("F", "blooming time", "early", "late"),
        ),
    ),
}

SPECIES_UNLOCK_ORDER = tuple(SPECIES_DEFINITIONS)

GREENHOUSE_EXPANSION_COSTS = {
    5: 50,
    6: 75,
    7: 100,
    8: 125,
    9: 150,
    10: 200,
    11: 250,
    12: 300,
    13: 400,
    14: 500,
    15: 600,
    16: 700,
    17: 850,
    18: 1000,
    19: 1200,
    20: 1500,
}

ANALYZER_UPGRADES = {
    2: ("Genetic Sequencing", 500),
    3: ("Probabilistic Analysis", 2000),
    4: ("Genetic Simulator", 5000),
}

DISCOVERY_REWARDS = {
    "phenotype": 20,
    "genotype": 50,
    "species": 200,
}

COLLECTION_MILESTONE_REWARDS = {
    25: 250,
    50: 500,
    75: 1000,
    100: 5000,
}

SPECIES_UNLOCK_REQUIRED_FREE_SLOTS = 2


def species_definition(species: str) -> SpeciesDefinition:
    """Return content data for a species."""
    try:
        return SPECIES_DEFINITIONS[species]
    except KeyError as error:
        message = f"Unknown species: {species}"
        raise ValueError(message) from error


def trait_names(species: str) -> tuple[str, ...]:
    """Return trait names in genotype order."""
    return tuple(rule.name for rule in species_definition(species).traits)


def collection_total_entries(unlocked_only: bool = False) -> int:
    """Return total collection entries for the official content set."""
    definitions = (
        (SPECIES_DEFINITIONS[SPECIES_MENDEL_PEA],)
        if unlocked_only
        else SPECIES_DEFINITIONS.values()
    )
    total = 0
    for definition in definitions:
        total += 1
        total += 2**definition.gene_count
        total += 3**definition.gene_count
    return total
