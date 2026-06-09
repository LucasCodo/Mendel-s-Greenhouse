"""Property-based tests for Mendelian inheritance invariants."""

from random import Random

from hypothesis import given
from hypothesis import strategies as st

from mendels_greenhouse.core.genetics import (
    Plant,
    crossbreed,
    expected_distribution,
)

A_PAIRS = st.sampled_from(("AA", "Aa", "aa"))
B_PAIRS = st.sampled_from(("BB", "Bb", "bb"))


@st.composite
def pea_genotypes(draw) -> str:
    """Generate valid Mendel Pea genotypes."""
    return f"{draw(A_PAIRS)}{draw(B_PAIRS)}"


@given(pea_genotypes(), pea_genotypes())
def test_crossbreed_generates_only_expected_genotypes(
    parent_a_genotype: str,
    parent_b_genotype: str,
) -> None:
    parent_a = Plant(parent_a_genotype)
    parent_b = Plant(parent_b_genotype)
    distribution = expected_distribution(parent_a, parent_b)

    offspring = crossbreed(parent_a, parent_b, count=16, rng=Random(1))

    assert {plant.genotype for plant in offspring} <= set(
        distribution.genotype_counts,
    )


@given(pea_genotypes(), pea_genotypes())
def test_expected_distribution_probabilities_sum_to_one(
    parent_a_genotype: str,
    parent_b_genotype: str,
) -> None:
    distribution = expected_distribution(
        Plant(parent_a_genotype),
        Plant(parent_b_genotype),
    )

    assert sum(distribution.probabilities.values()) == 1
