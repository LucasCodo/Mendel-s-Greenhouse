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
