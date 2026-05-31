"""Tests for MVP Mendelian genetics rules."""

from random import Random

import pytest

from mendels_greenhouse.core.genetics import (
    Plant,
    combine_gametes,
    crossbreed,
    expected_distribution,
    gametes,
)


def test_pure_parent_cross_produces_only_double_heterozygotes() -> None:
    offspring = crossbreed(
        Plant("AABB"),
        Plant("aabb"),
        count=20,
        rng=Random(1),
    )

    assert {plant.genotype for plant in offspring} == {"AaBb"}
    assert len(offspring) == 20


def test_double_heterozygote_has_four_gamete_types() -> None:
    assert set(gametes(Plant("AaBb"))) == {"AB", "Ab", "aB", "ab"}


def test_expected_distribution_calculates_genotype_probabilities() -> None:
    distribution = expected_distribution(Plant("AABB"), Plant("AaBb"))

    assert distribution.genotype_counts == {
        "AABB": 1,
        "AABb": 1,
        "AaBB": 1,
        "AaBb": 1,
    }
    assert distribution.probabilities == {
        "AABB": 0.25,
        "AABb": 0.25,
        "AaBB": 0.25,
        "AaBb": 0.25,
    }


def test_phenotype_uses_dominant_allele_when_present() -> None:
    phenotype = Plant("AaBb").phenotype

    assert phenotype.seed_color == "yellow"
    assert phenotype.seed_texture == "smooth"


def test_phenotype_uses_recessive_trait_without_dominant_allele() -> None:
    phenotype = Plant("aabb").phenotype

    assert phenotype.seed_color == "green"
    assert phenotype.seed_texture == "wrinkled"


def test_combine_gametes_normalizes_uppercase_alleles_first() -> None:
    assert combine_gametes("ab", "AB") == "AaBb"


@pytest.mark.parametrize("genotype", ["AAB", "AACc", "ZZZZ"])
def test_invalid_mvp_genotype_is_rejected(genotype: str) -> None:
    with pytest.raises(ValueError, match=r"Genotype|Invalid alleles"):
        Plant(genotype)
