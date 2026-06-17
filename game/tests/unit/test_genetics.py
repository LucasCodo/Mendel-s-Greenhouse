"""Tests for MVP Mendelian genetics rules."""

from random import Random

import pytest

from mendels_greenhouse.core.genetics import (
    Plant,
    combine_gametes,
    crossbreed,
    expected_distribution,
    expected_phenotype_probabilities,
    founder_genotypes,
    gametes,
    punnett_square,
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


def test_crossbreed_preserves_parent_species() -> None:
    offspring = crossbreed(
        Plant("AABBCC", species="Snapdragon"),
        Plant("aabbcc", species="Snapdragon"),
        count=1,
        rng=Random(1),
    )

    assert offspring[0].species == "Snapdragon"
    assert offspring[0].genotype == "AaBbCc"


def test_crossbreed_assigns_next_generation_from_parents() -> None:
    offspring = crossbreed(
        Plant("AaBb", generation=1),
        Plant("AaBb", generation=2),
        count=1,
        rng=Random(1),
    )

    assert offspring[0].generation == 3
    assert offspring[0].generation_label == "F3"


def test_founder_generation_label_is_p0() -> None:
    assert Plant("AABB").generation_label == "P0"


def test_founder_genotypes_use_dominant_and_recessive_pairs() -> None:
    assert founder_genotypes(3) == ("AABBCC", "aabbcc")


def test_distribution_rejects_mismatched_parent_species() -> None:
    with pytest.raises(ValueError, match="same species"):
        expected_distribution(
            Plant("AABB", species="Mendel Pea"),
            Plant("aabbcc", species="Snapdragon"),
        )


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


def test_expected_phenotype_probabilities_group_genotypes() -> None:
    probabilities = expected_phenotype_probabilities(
        Plant("AaBb"),
        Plant("AaBb"),
    )

    assert sorted(probabilities.values(), reverse=True) == [
        9 / 16,
        3 / 16,
        3 / 16,
        1 / 16,
    ]


def test_punnett_square_uses_parent_gamete_combinations() -> None:
    square = punnett_square(Plant("AaBb"), Plant("AABB"))

    assert square.parent_a_gametes == ("AB", "Ab", "aB", "ab")
    assert square.parent_b_gametes == ("AB",)
    assert square.cells == (("AABB", "AABb", "AaBB", "AaBb"),)


def test_phenotype_uses_dominant_allele_when_present() -> None:
    phenotype = Plant("AaBb").phenotype

    assert phenotype.seed_color == "yellow"
    assert phenotype.seed_texture == "smooth"


def test_phenotype_uses_recessive_trait_without_dominant_allele() -> None:
    phenotype = Plant("aabb").phenotype

    assert phenotype.seed_color == "green"
    assert phenotype.seed_texture == "wrinkled"


@pytest.mark.parametrize("genotype", ["AABB", "aabb"])
def test_fully_dominant_and_recessive_founders_are_protected(
    genotype: str,
) -> None:
    assert Plant(genotype).is_protected_founder


def test_mixed_genotype_is_not_protected_founder() -> None:
    assert not Plant("AaBb").is_protected_founder


def test_combine_gametes_normalizes_uppercase_alleles_first() -> None:
    assert combine_gametes("ab", "AB") == "AaBb"


@pytest.mark.parametrize("genotype", ["AAB", "AACc", "ZZZZ"])
def test_invalid_mvp_genotype_is_rejected(genotype: str) -> None:
    with pytest.raises(ValueError, match=r"Genotype|Invalid alleles"):
        Plant(genotype)
