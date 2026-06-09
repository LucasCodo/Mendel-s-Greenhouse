"""Mendelian genetics rules for playable plant species."""

from collections import Counter
from dataclasses import dataclass
from itertools import product
from random import Random

from mendels_greenhouse.core.content import (
    SPECIES_MENDEL_PEA,
    species_definition,
)

GENE_WIDTH = 2
SECOND_TRAIT_COUNT = 2
MVP_GENES = ("A", "B")
GENE_SYMBOLS = tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


@dataclass(frozen=True)
class Phenotype:
    """Visible trait expression for one plant."""

    species: str
    traits: dict[str, str]

    @property
    def seed_color(self) -> str:
        """Return the Mendel Pea seed color compatibility field."""
        return self.traits.get("seed color", self.primary_trait_value)

    @property
    def seed_texture(self) -> str:
        """Return the Mendel Pea seed texture compatibility field."""
        return self.traits.get("seed texture", self.secondary_trait_value)

    @property
    def primary_trait_value(self) -> str:
        """Return the first visible trait value."""
        return next(iter(self.traits.values()), "unknown")

    @property
    def secondary_trait_value(self) -> str:
        """Return the second visible trait value."""
        values = tuple(self.traits.values())
        if len(values) < SECOND_TRAIT_COUNT:
            return self.primary_trait_value
        return values[1]

    @property
    def summary(self) -> str:
        """Return a compact phenotype summary."""
        return ", ".join(self.traits.values())


@dataclass(frozen=True)
class Plant:
    """A plant specimen represented by a genotype string."""

    genotype: str
    species: str = SPECIES_MENDEL_PEA
    generation: int = 0

    def __post_init__(self) -> None:
        validate_genotype(self.genotype)
        expected_gene_count = species_definition(self.species).gene_count
        actual_gene_count = len(self.genotype) // GENE_WIDTH
        if actual_gene_count != expected_gene_count:
            message = (
                f"{self.species} requires {expected_gene_count} genes, "
                f"got {actual_gene_count}."
            )
            raise ValueError(message)
        if self.generation < 0:
            message = "Plant generation cannot be negative."
            raise ValueError(message)

    @property
    def phenotype(self) -> Phenotype:
        """Return visible traits for this plant species."""
        pairs = genotype_pairs(self.genotype)
        definition = species_definition(self.species)
        traits = {}
        for rule in definition.traits:
            traits[rule.name] = (
                rule.dominant
                if rule.gene in pairs[rule.gene]
                else rule.recessive
            )
        return Phenotype(species=self.species, traits=traits)

    @property
    def is_protected_founder(self) -> bool:
        """Return whether this plant is a non-discardable founder genotype."""
        return self.genotype.isupper() or self.genotype.islower()

    @property
    def generation_label(self) -> str:
        """Return the display label for the plant generation."""
        if self.generation == 0:
            return "P0"
        return f"F{self.generation}"


@dataclass(frozen=True)
class CrossbreedingDistribution:
    """Expected genotype counts and probabilities for one cross."""

    genotype_counts: dict[str, int]
    total_combinations: int

    @property
    def probabilities(self) -> dict[str, float]:
        """Return expected probabilities by genotype."""
        return {
            genotype: count / self.total_combinations
            for genotype, count in self.genotype_counts.items()
        }


def validate_genotype(genotype: str) -> None:
    """Validate a Mendelian genotype made of ordered allele pairs."""
    if len(genotype) % GENE_WIDTH != 0:
        message = "Genotype must be made of allele pairs."
        raise ValueError(message)
    gene_count = len(genotype) // GENE_WIDTH
    if gene_count < len(MVP_GENES):
        message = f"Genotype must have at least {len(MVP_GENES)} genes."
        raise ValueError(message)
    if gene_count > len(GENE_SYMBOLS):
        message = f"Genotype supports at most {len(GENE_SYMBOLS)} genes."
        raise ValueError(message)

    pairs = [
        genotype[index : index + GENE_WIDTH]
        for index in range(0, len(genotype), GENE_WIDTH)
    ]
    for gene, pair in zip(_genes_for_count(gene_count), pairs, strict=True):
        allowed = {gene, gene.lower()}
        if set(pair) - allowed:
            message = f"Invalid alleles for gene {gene}: {pair}"
            raise ValueError(message)


def genotype_pairs(genotype: str) -> dict[str, str]:
    """Split a genotype string into gene pairs."""
    validate_genotype(genotype)
    genes = _genes_for_count(len(genotype) // GENE_WIDTH)
    return {
        gene: genotype[index : index + GENE_WIDTH]
        for gene, index in zip(
            genes,
            range(0, len(genotype), 2),
            strict=True,
        )
    }


def gametes(plant: Plant) -> tuple[str, ...]:
    """Return all possible gametes produced by a plant."""
    pairs = genotype_pairs(plant.genotype)
    allele_options = [tuple(dict.fromkeys(pair)) for pair in pairs.values()]
    return tuple("".join(alleles) for alleles in product(*allele_options))


def combine_gametes(gamete_a: str, gamete_b: str) -> str:
    """Combine two gametes into a normalized genotype."""
    if len(gamete_a) != len(gamete_b):
        message = "Gametes must have the same gene count."
        raise ValueError(message)
    pairs = []
    for gene, allele_a, allele_b in zip(
        _genes_for_count(len(gamete_a)),
        gamete_a,
        gamete_b,
        strict=True,
    ):
        alleles = sorted(
            (allele_a, allele_b),
            key=lambda allele: (allele.islower(), allele),
        )
        if alleles[0].upper() != gene:
            message = f"Invalid allele for gene {gene}."
            raise ValueError(message)
        pairs.append("".join(alleles))
    return "".join(pairs)


def expected_distribution(
    parent_a: Plant,
    parent_b: Plant,
) -> CrossbreedingDistribution:
    """Calculate all expected offspring genotypes before shuffling."""
    if parent_a.species != parent_b.species:
        message = "Parents must belong to the same species."
        raise ValueError(message)

    counts: Counter[str] = Counter()
    parent_a_gametes = gametes(parent_a)
    parent_b_gametes = gametes(parent_b)

    for gamete_a in parent_a_gametes:
        for gamete_b in parent_b_gametes:
            counts[combine_gametes(gamete_a, gamete_b)] += 1

    return CrossbreedingDistribution(
        genotype_counts=dict(sorted(counts.items())),
        total_combinations=len(parent_a_gametes) * len(parent_b_gametes),
    )


def crossbreed(
    parent_a: Plant,
    parent_b: Plant,
    *,
    count: int,
    rng: Random | None = None,
) -> list[Plant]:
    """Generate a shuffled offspring batch from two parents."""
    if count < 1:
        message = "Offspring count must be positive."
        raise ValueError(message)

    randomizer = rng or Random()
    distribution = expected_distribution(parent_a, parent_b)
    genotypes = _expand_distribution(distribution, count)
    randomizer.shuffle(genotypes)
    offspring_generation = max(parent_a.generation, parent_b.generation) + 1
    return [
        Plant(
            genotype,
            species=parent_a.species,
            generation=offspring_generation,
        )
        for genotype in genotypes
    ]


def _expand_distribution(
    distribution: CrossbreedingDistribution,
    count: int,
) -> list[str]:
    genotypes = []
    for genotype, combinations in distribution.genotype_counts.items():
        expected = count * combinations / distribution.total_combinations
        genotypes.extend([genotype] * round(expected))

    while len(genotypes) < count:
        genotypes.append(_most_likely_genotype(distribution))

    return genotypes[:count]


def _most_likely_genotype(distribution: CrossbreedingDistribution) -> str:
    return max(
        distribution.genotype_counts,
        key=lambda genotype: distribution.genotype_counts[genotype],
    )


def founder_genotypes(gene_count: int) -> tuple[str, str]:
    """Return fully dominant and recessive founder genotypes."""
    genes = _genes_for_count(gene_count)
    dominant = "".join(gene * GENE_WIDTH for gene in genes)
    recessive = "".join(gene.lower() * GENE_WIDTH for gene in genes)
    return dominant, recessive


def _genes_for_count(gene_count: int) -> tuple[str, ...]:
    if gene_count < 1:
        message = "Gene count must be positive."
        raise ValueError(message)
    if gene_count > len(GENE_SYMBOLS):
        message = f"Gene count supports at most {len(GENE_SYMBOLS)} genes."
        raise ValueError(message)
    return GENE_SYMBOLS[:gene_count]
