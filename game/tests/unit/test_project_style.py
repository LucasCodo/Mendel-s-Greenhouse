"""Project-level style safeguards."""

import ast
from pathlib import Path

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
