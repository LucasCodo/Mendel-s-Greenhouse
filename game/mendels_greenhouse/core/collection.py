"""Discovery collection tracking."""

from dataclasses import dataclass, field

from mendels_greenhouse.core.genetics import Phenotype, Plant


@dataclass
class Collection:
    """Permanent MVP discovery registry."""

    species: set[str] = field(default_factory=set)
    genotypes: set[str] = field(default_factory=set)
    phenotypes: set[tuple[str, str]] = field(default_factory=set)

    def register_species(self, species_name: str) -> bool:
        """Register a discovered species."""
        before = len(self.species)
        self.species.add(species_name)
        return len(self.species) > before

    def register_plant(self, plant: Plant) -> bool:
        """Register genotype and phenotype discoveries for a plant."""
        before = self.total_entries
        self.genotypes.add(plant.genotype)
        self.phenotypes.add(phenotype_key(plant.phenotype))
        return self.total_entries > before

    @property
    def total_entries(self) -> int:
        """Return the total number of collection entries."""
        return len(self.species) + len(self.genotypes) + len(self.phenotypes)


def phenotype_key(phenotype: Phenotype) -> tuple[str, str]:
    """Return the stable collection key for a phenotype."""
    return (phenotype.seed_color, phenotype.seed_texture)
