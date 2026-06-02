"""Mendelian genetics rules for the MVP pea species."""

from collections import Counter
from dataclasses import dataclass
from itertools import product
from random import Random

GENE_WIDTH = 2
MVP_GENES = ("A", "B")
SPECIES_MENDEL_PEA = "Mendel Pea"


@dataclass(frozen=True)
class Phenotype:
    """Visible MVP traits for Mendel pea plants."""

    seed_color: str
    seed_texture: str


@dataclass(frozen=True)
class Plant:
    """A plant specimen represented by a genotype string."""

    genotype: str
    species: str = SPECIES_MENDEL_PEA

    def __post_init__(self) -> None:
        validate_genotype(self.genotype)

    @property
    def phenotype(self) -> Phenotype:
        """Return visible traits for the MVP pea species."""
        pairs = genotype_pairs(self.genotype)
        return Phenotype(
            seed_color="yellow" if "A" in pairs["A"] else "green",
            seed_texture="smooth" if "B" in pairs["B"] else "wrinkled",
        )

    @property
    def is_protected_founder(self) -> bool:
        """Return whether this plant is a non-discardable founder genotype."""
        return self.genotype.isupper() or self.genotype.islower()


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
    """Validate an MVP genotype."""
    expected_length = len(MVP_GENES) * GENE_WIDTH
    if len(genotype) != expected_length:
        message = f"Genotype must have {expected_length} alleles."
        raise ValueError(message)

    pairs = [
        genotype[index : index + GENE_WIDTH]
        for index in range(0, expected_length, GENE_WIDTH)
    ]
    for gene, pair in zip(MVP_GENES, pairs, strict=True):
        allowed = {gene, gene.lower()}
        if set(pair) - allowed:
            message = f"Invalid alleles for gene {gene}: {pair}"
            raise ValueError(message)


def genotype_pairs(genotype: str) -> dict[str, str]:
    """Split a genotype string into gene pairs."""
    validate_genotype(genotype)
    return {
        gene: genotype[index : index + GENE_WIDTH]
        for gene, index in zip(
            MVP_GENES,
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
    pairs = []
    for gene, allele_a, allele_b in zip(
        MVP_GENES,
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
    return [
        Plant(genotype, species=parent_a.species) for genotype in genotypes
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
