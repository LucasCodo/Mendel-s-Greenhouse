from unittest.mock import Mock, patch

from mendels_greenhouse.ui.components import Rect
from mendels_greenhouse.ui.game_components.main_game import (
    ANALYZER_PANEL,
    ANALYZER_SCREEN,
    CROSS_BUTTON,
    PARENT_A_CARD,
    PARENT_B_CARD,
    PARENT_CROSS_PANEL,
)
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
    germination_bed = Rect(188, 178, 362, 170)
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
