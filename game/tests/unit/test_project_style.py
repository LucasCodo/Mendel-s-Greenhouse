"""Project-level style safeguards."""

import ast
from pathlib import Path

from mendels_greenhouse.scenes.main_game import (
    HARVEST_BUTTON,
    NAV_BUTTON_GAP,
    NAV_BUTTON_H,
    NAV_BUTTON_W,
    NAV_BUTTON_X,
    NAV_BUTTON_Y,
    NAV_ITEMS,
    NAV_RAIL,
    Rect,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FORBIDDEN_FUTURE_MODULE = "".join(("__", "future__"))
FONT_HELPER_PATH = Path("mendels_greenhouse/ui/fonts.py")
DIRECT_UI_TEXT_ALLOWLIST = {"CR", "X"}
DIRECT_UI_TEMPLATE_ALLOWLIST = {"{} CR", "L{}"}


def iter_python_files() -> list[Path]:
    ignored_parts = {
        ".pytest_cache",
        ".ruff_cache",
        "__pycache__",
        ".venv",
        "dist",
    }
    return [
        path
        for path in PROJECT_ROOT.rglob("*.py")
        if not ignored_parts.intersection(path.parts)
    ]


def test_project_does_not_use_future_imports() -> None:
    offenders: list[str] = []

    for path in iter_python_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.ImportFrom)
                and node.module == FORBIDDEN_FUTURE_MODULE
            ):
                offenders.append(
                    f"{path.relative_to(PROJECT_ROOT)}:{node.lineno}",
                )

    assert offenders == []


def test_ui_text_uses_project_font_helpers() -> None:
    offenders: list[str] = []

    for path in iter_python_files():
        relative_path = path.relative_to(PROJECT_ROOT)
        if relative_path == FONT_HELPER_PATH:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            function = node.func
            if (
                isinstance(function, ast.Attribute)
                and isinstance(function.value, ast.Name)
                and function.value.id == "pyxel"
                and function.attr == "text"
            ):
                offenders.append(f"{relative_path}:{node.lineno}")

    assert offenders == []


def test_ui_text_does_not_bypass_localization() -> None:
    offenders: list[str] = []
    ui_root = PROJECT_ROOT / "mendels_greenhouse" / "ui"

    for path in ui_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            function = node.func
            name = (
                function.id
                if isinstance(function, ast.Name)
                else function.attr
                if isinstance(function, ast.Attribute)
                else ""
            )
            text_index = {
                "draw_bold_spaced_text": 2,
                "draw_button": 1,
                "draw_text": 2,
            }.get(name)
            if text_index is None or len(node.args) <= text_index:
                continue
            text = node.args[text_index]
            if isinstance(text, ast.Constant) and isinstance(text.value, str):
                if (
                    any(character.isalpha() for character in text.value)
                    and text.value not in DIRECT_UI_TEXT_ALLOWLIST
                ):
                    offenders.append(
                        f"{path.relative_to(PROJECT_ROOT)}:{node.lineno}",
                    )
            elif isinstance(text, ast.JoinedStr):
                template = "".join(
                    value.value if isinstance(value, ast.Constant) else "{}"
                    for value in text.values
                )
                if (
                    any(character.isalpha() for character in template)
                    and template not in DIRECT_UI_TEMPLATE_ALLOWLIST
                ):
                    offenders.append(
                        f"{path.relative_to(PROJECT_ROOT)}:{node.lineno}",
                    )

    assert offenders == []


def test_literal_status_messages_are_marked_for_extraction() -> None:
    markers: set[str] = set()
    statuses: list[tuple[str, Path, int]] = []

    for path in iter_python_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                function = node.func
                if (
                    isinstance(function, ast.Name)
                    and function.id == "gettext_noop"
                    and node.args
                    and isinstance(node.args[0], ast.Constant)
                    and isinstance(node.args[0].value, str)
                ):
                    markers.add(node.args[0].value)
            if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                continue
            targets = (
                node.targets if isinstance(node, ast.Assign) else [node.target]
            )
            if not any(
                isinstance(target, ast.Attribute)
                and target.attr == "status_message"
                for target in targets
            ):
                continue
            value = node.value
            if isinstance(value, ast.Constant) and isinstance(
                value.value, str
            ):
                statuses.append((value.value, path, node.lineno))

    offenders = [
        f"{path.relative_to(PROJECT_ROOT)}:{line}: {message}"
        for message, path, line in statuses
        if message not in markers
    ]
    assert offenders == []


def test_navigation_rail_bounds_all_destinations() -> None:
    nav_rects = [
        Rect(
            NAV_BUTTON_X,
            NAV_BUTTON_Y + index * (NAV_BUTTON_H + NAV_BUTTON_GAP),
            NAV_BUTTON_W,
            NAV_BUTTON_H,
        )
        for index, _item in enumerate(NAV_ITEMS)
    ]

    assert all(NAV_RAIL.contains(rect.x, rect.y) for rect in nav_rects)
    assert all(
        NAV_RAIL.contains(
            rect.x + rect.width - 1,
            rect.y + rect.height - 1,
        )
        for rect in nav_rects
    )
    assert HARVEST_BUTTON.x + HARVEST_BUTTON.width <= NAV_RAIL.x
