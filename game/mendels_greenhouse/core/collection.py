"""Discovery collection tracking."""

from dataclasses import dataclass, field
from itertools import product

from mendels_greenhouse.core.content import (
    SPECIES_DEFINITIONS,
    collection_total_entries,
)
from mendels_greenhouse.core.genetics import Phenotype, Plant

GenotypeKey = tuple[str, str]
PhenotypeKey = tuple[str, tuple[tuple[str, str], ...]]
CollectionKey = str | GenotypeKey | PhenotypeKey


@dataclass
class Collection:
    """Permanent MVP discovery registry."""

    species: set[str] = field(default_factory=set)
    genotypes: set[GenotypeKey] = field(default_factory=set)
    phenotypes: set[PhenotypeKey] = field(default_factory=set)

    def register_species(self, species_name: str) -> bool:
        """Register a discovered species."""
        before = len(self.species)
        self.species.add(species_name)
        return len(self.species) > before

    def register_plant(self, plant: Plant) -> bool:
        """Register genotype and phenotype discoveries for a plant."""
        before = self.total_entries
        self.genotypes.add(genotype_key(plant))
        self.phenotypes.add(phenotype_key(plant.phenotype))
        return self.total_entries > before

    @property
    def total_entries(self) -> int:
        """Return the total number of collection entries."""
        return len(self.species) + len(self.genotypes) + len(self.phenotypes)

    @property
    def completion_percent(self) -> int:
        """Return total official collection completion percentage."""
        total = collection_total_entries()
        if total == 0:
            return 0
        return min(int(self.total_entries * 100 / total), 100)


def genotype_key(plant: Plant) -> GenotypeKey:
    """Return the stable collection key for a genotype."""
    return (plant.species, plant.genotype)


def phenotype_key(phenotype: Phenotype) -> PhenotypeKey:
    """Return the stable collection key for a phenotype."""
    return (
        phenotype.species,
        tuple(sorted(phenotype.traits.items())),
    )


def official_collection_keys(category: str) -> tuple[CollectionKey, ...]:
    """Return every official album slot for one collection category."""
    if category == "Species":
        return tuple(SPECIES_DEFINITIONS)
    if category == "Phenotypes":
        return _official_phenotype_keys()
    if category == "Genotypes":
        return _official_genotype_keys()
    raise ValueError(category)


def _official_phenotype_keys() -> tuple[PhenotypeKey, ...]:
    keys: list[PhenotypeKey] = []
    for species, definition in SPECIES_DEFINITIONS.items():
        trait_values = (
            (rule.dominant, rule.recessive) for rule in definition.traits
        )
        for values in product(*trait_values):
            traits = tuple(
                sorted(
                    (rule.name, value)
                    for rule, value in zip(
                        definition.traits,
                        values,
                        strict=True,
                    )
                )
            )
            keys.append((species, traits))
    return tuple(keys)


def _official_genotype_keys() -> tuple[GenotypeKey, ...]:
    keys: list[GenotypeKey] = []
    for species, definition in SPECIES_DEFINITIONS.items():
        allele_pairs = tuple(
            (gene * 2, f"{gene}{gene.lower()}", gene.lower() * 2)
            for gene in (rule.gene for rule in definition.traits)
        )
        for pairs in product(*allele_pairs):
            keys.append((species, "".join(pairs)))
    return tuple(keys)
