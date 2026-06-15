from unittest.mock import Mock, patch

from mendels_greenhouse.scenes.main_game import MainGameScene
from mendels_greenhouse.ui.components import Rect
from mendels_greenhouse.ui.game_components.germination_bed import BedLayout


def _scene_with_visible_specimens() -> MainGameScene:
    scene = MainGameScene.__new__(MainGameScene)
    scene.state = Mock(
        current_batch=[Mock(), Mock()],
        visible_count=2,
        selected_offspring_index=0,
    )
    layout = BedLayout(
        x=0,
        y=0,
        columns=2,
        rows=1,
        cell_count=2,
        cell_width=10,
        cell_height=10,
        gap=0,
    )
    scene._germination_layout = Mock(return_value=layout)
    scene._germination_cell_rect = Mock(
        side_effect=lambda index, _layout: Rect(index * 10, 0, 10, 10),
    )
    scene._play_sound = Mock()
    scene.specimen_overlay_open = False
    return scene


def test_clicking_specimen_opens_overlay() -> None:
    scene = _scene_with_visible_specimens()

    with patch(
        "mendels_greenhouse.scenes.main_game.clicked",
        side_effect=[False, True],
    ):
        scene._update_germination_bed_selection()

    assert scene.state.selected_offspring_index == 1
    assert scene.specimen_overlay_open
    scene._play_sound.assert_called_once_with(0)


def test_hovering_specimen_does_not_open_overlay() -> None:
    scene = _scene_with_visible_specimens()

    with patch(
        "mendels_greenhouse.scenes.main_game.clicked",
        return_value=False,
    ):
        scene._update_germination_bed_selection()

    assert scene.state.selected_offspring_index == 0
    assert not scene.specimen_overlay_open
    scene._play_sound.assert_not_called()


def test_escape_closes_specimen_overlay() -> None:
    scene = _scene_with_visible_specimens()
    scene.specimen_overlay_open = True

    with (
        patch(
            "mendels_greenhouse.scenes.main_game.clicked",
            return_value=False,
        ),
        patch(
            "mendels_greenhouse.scenes.main_game.pyxel.btnp",
            return_value=True,
        ),
    ):
        scene._update_specimen_overlay()

    assert not scene.specimen_overlay_open
    scene._play_sound.assert_called_once_with(0)


def test_storing_specimen_closes_overlay() -> None:
    scene = _scene_with_visible_specimens()
    scene.specimen_overlay_open = True
    scene.breeding = Mock()
    scene.breeding.store_selected_offspring.return_value = True
    scene._reveal_frames = {}
    scene.germination_started_frame = 1
    scene._autosave = Mock()

    with (
        patch(
            "mendels_greenhouse.scenes.main_game.clicked",
            side_effect=[False, True],
        ),
        patch(
            "mendels_greenhouse.scenes.main_game.pyxel.btnp",
            return_value=False,
        ),
    ):
        scene._update_specimen_overlay()

    assert not scene.specimen_overlay_open
    scene.breeding.store_selected_offspring.assert_called_once_with()
    scene._autosave.assert_called_once_with()
    scene._play_sound.assert_called_once_with(3)
