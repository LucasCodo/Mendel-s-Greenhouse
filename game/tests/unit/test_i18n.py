"""Tests for gettext-backed runtime localization."""

from mendels_greenhouse.core.content import (
    ANALYZER_UPGRADES,
    SPECIES_DEFINITIONS,
)
from mendels_greenhouse.core.i18n import get_language, set_language, t
from mendels_greenhouse.scenes.main_game import (
    COLLECTION_TABS,
    KNOWLEDGE_DETAILS,
    KNOWLEDGE_STAGES,
    NAV_ITEMS,
)


def test_portuguese_catalog_translates_runtime_text() -> None:
    set_language("pt-BR")

    assert t("CROSS PLANTS") == "CRUZAR"
    assert t("Contract") == "Contrato"
    assert t("Learn") == "Saber"
    assert t("Config.") == "Config."
    assert t("Undiscovered") == "Nao descoberta"
    assert t("{found}/{total} found", found=3, total=9) == ("3/9 encontradas")
    assert t("Generation") == "Geracao"
    assert t("Gametes") == "Gametas"
    assert t("Punnett square") == "Quadro de Punnett"
    assert t("Traits") == "Tracos"
    assert t("Genes") == "Genes"
    assert t("Punnett") == "Punnett"
    assert t("Sim") == "Sim"
    assert t("Visible traits") == "Tracos visiveis"
    assert t("Alleles") == "Alelos"
    assert t("Plant {slot}: {genotype}", slot=3, genotype="AaBb") == (
        "Planta 3: AaBb"
    )
    assert t("Chance: {percentage}%", percentage=25) == "Chance: 25%"
    assert t("Expected outcomes") == "Resultados esperados"
    assert t("ONLINE") == "ATIVO"
    assert t("Slots: {used}/{capacity}", used=3, capacity=12) == (
        "Espacos: 3/12"
    )
    assert t("yellow") == "amarela"
    assert t("violet") == "violeta"
    assert t("large") == "grande"
    assert t("many-petal") == "muitas petalas"
    assert t("fragrant") == "perfumada"
    assert t("star") == "estrela"
    assert t("early") == "precoce"


def test_official_species_and_phenotypes_are_in_portuguese_catalog() -> None:
    expected_translations = {
        "Mendel Pea": "Ervilha de Mendel",
        "Snapdragon": "Boca-de-leao",
        "Corn": "Milho",
        "Tomato": "Tomate",
        "Orchid": "Orquidea",
        "seed color": "cor da semente",
        "seed texture": "textura da semente",
        "flower color": "cor da flor",
        "flower size": "tamanho da flor",
        "flower shape": "forma da flor",
        "petal count": "qtd. petalas",
        "petal shape": "forma da petala",
        "blooming time": "floracao",
        "plant height": "altura da planta",
        "kernel color": "cor do grao",
        "ear size": "tamanho da espiga",
        "row count": "qtd. fileiras",
        "fruit color": "cor do fruto",
        "fruit size": "tamanho do fruto",
        "fruit shape": "forma do fruto",
        "resistance": "resistencia",
        "maturation": "maturacao",
        "yellow": "amarela",
        "green": "verde",
        "smooth": "lisa",
        "wrinkled": "rugosa",
        "red": "vermelha",
        "white": "branca",
        "tall": "alta",
        "short": "baixa",
        "wide": "larga",
        "narrow": "estreita",
        "purple": "roxa",
        "large": "grande",
        "small": "pequena",
        "many-row": "muitas fileiras",
        "few-row": "poucas fileiras",
        "round": "redonda",
        "pear-shaped": "pera",
        "resistant": "resistente",
        "susceptible": "suscetivel",
        "early": "precoce",
        "late": "tardia",
        "violet": "violeta",
        "many-petal": "muitas petalas",
        "few-petal": "poucas petalas",
        "fragrant": "perfumada",
        "neutral": "neutra",
        "star": "estrela",
        "aroma": "aroma",
        "Genetic Sequencing": "Sequenciamento genetico",
        "Probabilistic Analysis": "Analise probabilistica",
        "Genetic Simulator": "Simulador genetico",
    }
    set_language("pt-BR")

    official_terms = set(SPECIES_DEFINITIONS)
    for definition in SPECIES_DEFINITIONS.values():
        for rule in definition.traits:
            official_terms.update((rule.name, rule.dominant, rule.recessive))
    official_terms.update(name for name, _cost in ANALYZER_UPGRADES.values())

    missing_expectations = official_terms - expected_translations.keys()
    assert missing_expectations == set()
    assert {term: t(term) for term in sorted(official_terms)} == {
        term: expected_translations[term] for term in sorted(official_terms)
    }


def test_indirect_ui_constants_are_in_portuguese_catalog() -> None:
    expected_translations = {
        "9:3:3:1 dihybrid ratio": "Proporcao diibrida 9:3:3:1",
        "Allele pair": "Par de alelos",
        "Allele segregation": "Segregacao dos alelos",
        "Collection": "Colecao",
        "Config.": "Config.",
        "Contract": "Contrato",
        "CROSS PLANTS": "CRUZAR",
        "Dominant allele": "Alelo dominante",
        "Garden": "Jardim",
        "Genetic Planning": "Planejamento genetico",
        "Genetic planning": "Planejamento genetico",
        "Genetic probability": "Probabilidade genetica",
        "Genotype": "Genótipo",
        "Genotypes": "Genotipos",
        "Heterozygous": "Heterozigoto",
        "Homozygous": "Homozigoto",
        "Independent assortment": "Segregacao independente",
        "Learn": "Saber",
        "Phenotype": "Fenótipo",
        "Phenotypes": "Fenotipos",
        "Probability": "Probabilidade",
        "Recessive allele": "Alelo recessivo",
        "Shop": "Loja",
        "Species": "Especies",
    }
    set_language("pt-BR")

    indirect_terms = {label for _screen, label, _sprite in NAV_ITEMS}
    indirect_terms.update(COLLECTION_TABS)
    for stage, concepts, _required_level in KNOWLEDGE_STAGES:
        indirect_terms.add(stage)
        indirect_terms.update(concepts)
    indirect_terms.update(KNOWLEDGE_DETAILS)

    missing_expectations = indirect_terms - expected_translations.keys()
    assert missing_expectations == set()
    assert {term: t(term) for term in sorted(indirect_terms)} == {
        term: expected_translations[term] for term in sorted(indirect_terms)
    }


def test_unknown_language_falls_back_to_english() -> None:
    set_language("fr")

    assert get_language() == "en"
    assert t("CROSS PLANTS") == "CROSS PLANTS"
