from unittest.mock import Mock, patch

import pytest

from mendels_greenhouse.core.content import SPECIES_DEFINITIONS
from mendels_greenhouse.core.genetics import Plant
from mendels_greenhouse.ui.components import Rect
from mendels_greenhouse.ui.fonts import text_width
from mendels_greenhouse.ui.game_components import plant_trait_lines
from mendels_greenhouse.ui.game_components.garden import (
    GARDEN_DISCARD_BUTTON,
    GARDEN_PARENT_A_BUTTON,
    GARDEN_PARENT_B_BUTTON,
)
from mendels_greenhouse.ui.game_components.knowledge import (
    KnowledgeStage,
    knowledge_concept_rect,
    knowledge_stage_rect,
    selected_knowledge_stage,
)
from mendels_greenhouse.ui.game_components.main_game import (
    ANALYZER_PANEL,
    ANALYZER_SCREEN,
    CROSS_BUTTON,
    PARENT_A_CARD,
    PARENT_B_CARD,
    PARENT_CROSS_PANEL,
    parent_cross_panel,
    specimen_overlay,
)
from mendels_greenhouse.ui.game_components.overlays import runtime
from mendels_greenhouse.ui.game_components.overlays.runtime import (
    draw_intro_panel,
)
from mendels_greenhouse.ui.game_components.settings import (
    LANGUAGE_BUTTON,
    MUSIC_DOWN_BUTTON,
    MUSIC_MUTE_CHECKBOX,
    MUSIC_UP_BUTTON,
    RESET_PROGRESS_BUTTON,
    SETTINGS_BACK_BUTTON,
    SETTINGS_PANEL,
    SETTINGS_PREFERENCES_PANEL,
    SOUND_DOWN_BUTTON,
    SOUND_MUTE_CHECKBOX,
    SOUND_UP_BUTTON,
)
from mendels_greenhouse.ui.game_components.shared import DrawContext
from mendels_greenhouse.ui.game_components.shop import (
    SHOP_BUY_BUTTON,
    SHOP_CARD_RECTS,
    SHOP_CONFIRM_BUY_BUTTON,
    SHOP_CONFIRM_CANCEL_BUTTON,
)


def test_intro_panel_uses_display_font_for_all_instruction_text() -> None:
    display_font = Mock()
    context = DrawContext(
        translate=lambda text: text,
        display_font=display_font,
    )

    with (
        patch(
            "mendels_greenhouse.ui.game_components.overlays.runtime."
            "draw_modal_scrim",
        ),
        patch(
            "mendels_greenhouse.ui.game_components.overlays.runtime.draw_panel",
        ),
        patch(
            "mendels_greenhouse.ui.game_components.overlays.runtime."
            "draw_outlined_text",
        ),
        patch(
            "mendels_greenhouse.ui.game_components.overlays.runtime.draw_button",
        ),
        patch(
            "mendels_greenhouse.ui.game_components.overlays.runtime.pyxel.text",
        ) as text,
    ):
        draw_intro_panel(context, Rect(272, 294, 96, 24))

    assert text.call_count == 10
    assert all(call.args[4] is display_font for call in text.call_args_list)


def test_settings_controls_stay_inside_centered_panel() -> None:
    controls = (
        LANGUAGE_BUTTON,
        MUSIC_DOWN_BUTTON,
        MUSIC_UP_BUTTON,
        MUSIC_MUTE_CHECKBOX,
        SOUND_DOWN_BUTTON,
        SOUND_UP_BUTTON,
        SOUND_MUTE_CHECKBOX,
        RESET_PROGRESS_BUTTON,
        SETTINGS_BACK_BUTTON,
    )

    assert SETTINGS_PANEL.x == (640 - SETTINGS_PANEL.width) // 2
    assert SETTINGS_PREFERENCES_PANEL.x > SETTINGS_PANEL.x
    assert all(
        SETTINGS_PANEL.contains(control.x, control.y)
        and SETTINGS_PANEL.contains(
            control.x + control.width - 1,
            control.y + control.height - 1,
        )
        for control in controls
    )


def test_parent_cross_panel_matches_germination_bed_width() -> None:
    germination_bed = Rect(188, 196, 362, 152)
    left_inset = PARENT_A_CARD.x - PARENT_CROSS_PANEL.x
    right_inset = (
        PARENT_CROSS_PANEL.x
        + PARENT_CROSS_PANEL.width
        - PARENT_B_CARD.x
        - PARENT_B_CARD.width
    )

    assert PARENT_CROSS_PANEL.x == germination_bed.x
    assert PARENT_CROSS_PANEL.width == germination_bed.width
    assert CROSS_BUTTON.x == (
        PARENT_CROSS_PANEL.x
        + (PARENT_CROSS_PANEL.width - CROSS_BUTTON.width) // 2
    )
    assert left_inset == right_inset
    assert PARENT_CROSS_PANEL.y + PARENT_CROSS_PANEL.height < germination_bed.y


@pytest.mark.parametrize(
    ("species", "genotype"),
    [
        ("Mendel Pea", "AABB"),
        ("Snapdragon", "AABBCC"),
        ("Corn", "AABBCCDD"),
        ("Tomato", "AABBCCDDEE"),
        ("Orchid", "AABBCCDDEEFF"),
    ],
)
def test_parent_cross_panel_shows_one_phenotype_per_gene(
    species: str,
    genotype: str,
) -> None:
    plant = Plant(genotype, species=species)

    labels = parent_cross_panel.phenotype_labels(
        plant,
        trait=lambda value: value,
    )

    assert len(labels) == SPECIES_DEFINITIONS[species].gene_count
    assert labels == tuple(plant.phenotype.traits.values())


def test_parent_cross_panel_translates_phenotype_labels() -> None:
    plant = Plant("AABBCCDDEEFF", species="Orchid")
    translations = {
        "violet": "violeta",
        "large": "grande",
        "many-petal": "muitas petalas",
        "fragrant": "perfumada",
        "star": "estrela",
        "early": "precoce",
    }

    labels = parent_cross_panel.phenotype_labels(
        plant,
        trait=translations.__getitem__,
    )

    assert labels == tuple(translations.values())


def test_parent_cross_panel_fits_orchid_content_above_actions() -> None:
    plant = Plant("AABBCCDDEEFF", species="Orchid")

    genotype = parent_cross_panel.genotype_label(
        plant,
        visible_genotype=lambda selected: selected.genotype,
    )
    labels = parent_cross_panel.phenotype_labels(
        plant,
        trait=lambda value: value,
    )
    last_label_y = (
        PARENT_CROSS_PANEL.y
        + 40
        + (len(labels) - 1) * parent_cross_panel.PHENOTYPE_LINE_HEIGHT
    )

    assert genotype == "AABBCCDDEEFF"
    assert text_width(genotype) <= (
        parent_cross_panel.GENOTYPE_FIELD_WIDTH
        - parent_cross_panel.GENOTYPE_TEXT_INSET * 2
    )
    assert all(
        text_width(label) <= parent_cross_panel.PHENOTYPE_LABEL_WIDTH
        for label in labels
    )
    assert last_label_y + 8 <= CROSS_BUTTON.y
    assert PARENT_A_CARD.y + PARENT_A_CARD.height <= CROSS_BUTTON.y
    assert PARENT_B_CARD.y + PARENT_B_CARD.height <= CROSS_BUTTON.y
    assert CROSS_BUTTON.y + CROSS_BUTTON.height < PARENT_CROSS_PANEL.y + 119


def test_orchid_detail_surfaces_receive_all_six_traits() -> None:
    plant = Plant("AABBCCDDEEFF", species="Orchid")

    lines = plant_trait_lines(plant, translate=lambda text: text)

    assert lines == [
        "Flower color: violet",
        "Flower size: large",
        "Petal count: many-petal",
        "Aroma: fragrant",
        "Flower shape: star",
        "Blooming time: early",
    ]


def test_orchid_detail_surfaces_translate_trait_names() -> None:
    plant = Plant("AABBCCDDEEFF", species="Orchid")
    translations = {
        "flower color": "cor da flor",
        "flower size": "tamanho da flor",
        "petal count": "qtd. petalas",
        "aroma": "aroma",
        "flower shape": "forma da flor",
        "blooming time": "floracao",
        "violet": "violeta",
        "large": "grande",
        "many-petal": "muitas petalas",
        "fragrant": "perfumada",
        "star": "estrela",
        "early": "precoce",
    }

    lines = plant_trait_lines(plant, translate=translations.__getitem__)

    assert lines == [
        "Cor da flor: violeta",
        "Tamanho da flor: grande",
        "Qtd. petalas: muitas petalas",
        "Aroma: perfumada",
        "Forma da flor: estrela",
        "Floracao: precoce",
    ]


def test_specimen_overlay_uses_readable_phenotype_text_color() -> None:
    data = specimen_overlay.SpecimenOverlayData(
        panel=Rect(0, 0, 320, 240),
        store_button=Rect(20, 200, 120, 24),
        discard_button=Rect(160, 200, 120, 24),
        close_button=Rect(288, 8, 24, 24),
        plant=Plant("AABBCCDDEEFF", species="Orchid"),
        can_store=True,
        visible_genotype="AABBCCDDEEFF",
        trait_lines=["Flower Color: violet"],
    )
    context = DrawContext(translate=lambda text: text, display_font=None)

    with (
        patch(
            "mendels_greenhouse.ui.game_components.main_game.specimen_overlay."
            "draw_modal_scrim",
        ),
        patch(
            "mendels_greenhouse.ui.game_components.main_game.specimen_overlay."
            "draw_panel",
        ),
        patch(
            "mendels_greenhouse.ui.game_components.main_game.specimen_overlay."
            "draw_rounded_panel",
        ),
        patch(
            "mendels_greenhouse.ui.game_components.main_game.specimen_overlay."
            "draw_text",
        ),
        patch(
            "mendels_greenhouse.ui.game_components.main_game.specimen_overlay."
            "draw_button",
        ),
        patch(
            "mendels_greenhouse.ui.game_components.main_game.specimen_overlay."
            "_draw_preview_atmosphere",
        ),
        patch(
            "mendels_greenhouse.ui.game_components.main_game.specimen_overlay."
            "_draw_discard_button",
        ),
        patch(
            "mendels_greenhouse.ui.game_components.main_game.specimen_overlay."
            "_draw_detail_row",
            side_effect=[96, 136, 176],
        ) as draw_detail_row,
    ):
        specimen_overlay.draw_specimen_overlay(
            context,
            data,
            plant_preview=Mock(),
        )

    assert draw_detail_row.call_args_list[0].args[5] == (
        specimen_overlay.PHENOTYPE_VALUE_COLOR
    )


def test_garden_actions_leave_space_for_six_trait_lines() -> None:
    first_trait_y = 184
    last_trait_bottom = first_trait_y + 5 * 9 + 8

    assert last_trait_bottom <= GARDEN_PARENT_A_BUTTON.y
    assert GARDEN_PARENT_A_BUTTON.y + GARDEN_PARENT_A_BUTTON.height <= (
        GARDEN_PARENT_B_BUTTON.y
    )
    assert GARDEN_PARENT_B_BUTTON.y + GARDEN_PARENT_B_BUTTON.height <= (
        GARDEN_DISCARD_BUTTON.y
    )


def test_parent_picker_grid_and_details_fit_inside_panel() -> None:
    last_slot = runtime.parent_picker_slot_rect(19)
    detail = runtime.PARENT_PICKER_DETAIL_PANEL
    panel = runtime.PARENT_PICKER_PANEL

    assert last_slot.x + last_slot.width < detail.x
    assert last_slot.y + last_slot.height <= panel.y + panel.height
    assert detail.x + detail.width <= panel.x + panel.width
    assert detail.y + detail.height <= panel.y + panel.height


def test_analyzer_screen_uses_space_freed_by_hardware_controls() -> None:
    assert ANALYZER_PANEL.y == 68
    assert ANALYZER_PANEL.width == 170
    assert ANALYZER_SCREEN.y == 82
    assert ANALYZER_SCREEN.width == 138
    assert ANALYZER_SCREEN.height == 252
    assert (
        PARENT_CROSS_PANEL.x - (ANALYZER_PANEL.x + ANALYZER_PANEL.width) == 8
    )
    assert ANALYZER_SCREEN.y + ANALYZER_SCREEN.height <= (
        ANALYZER_PANEL.y + ANALYZER_PANEL.height - 14
    )


def test_shop_cards_and_actions_stay_clear_of_navigation_rail() -> None:
    content_right = 558

    assert all(
        card.x + card.width <= content_right for card in SHOP_CARD_RECTS
    )
    assert SHOP_BUY_BUTTON.x + SHOP_BUY_BUTTON.width <= content_right
    assert (
        SHOP_CONFIRM_CANCEL_BUTTON.x + SHOP_CONFIRM_CANCEL_BUTTON.width
        <= content_right
    )
    assert (
        SHOP_CONFIRM_BUY_BUTTON.x + SHOP_CONFIRM_BUY_BUTTON.width
        <= content_right
    )


def test_knowledge_layout_stays_clear_and_tracks_selected_stage() -> None:
    stages = (
        KnowledgeStage("Phenotype", ("Phenotype",), 1),
        KnowledgeStage("Genotype", ("Genotype",), 2),
        KnowledgeStage("Probability", ("Probability",), 3),
        KnowledgeStage("Genetic Planning", ("Planning",), 4),
    )

    assert selected_knowledge_stage(stages, "Probability") == stages[2]
    assert knowledge_stage_rect(3).x + knowledge_stage_rect(3).width <= 558
    assert (
        knowledge_concept_rect(4).y + knowledge_concept_rect(4).height <= 334
    )
