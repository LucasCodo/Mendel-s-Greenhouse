"""File-backed profile-scoped autosave service."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Self

import pyxel

from mendels_greenhouse.core.save_data import (
    SaveMetadata,
    state_from_save_data,
    state_to_save_data,
)
from mendels_greenhouse.state.game_state import GameState

DEFAULT_PROFILE_ID = "local"
DEFAULT_SLOT_ID = "slot-1"
APP_AUTHOR = "LucasCodo"
APP_NAME = "MendelsGreenhouse"


@dataclass(frozen=True)
class SaveIdentity:
    """Profile and slot identity for one save file."""

    profile_id: str = DEFAULT_PROFILE_ID
    slot_id: str = DEFAULT_SLOT_ID


class SaveService:
    """Persist save payloads without exposing other profiles."""

    def __init__(
        self,
        root_dir: Path,
        identity: SaveIdentity | None = None,
    ) -> None:
        self.root_dir = root_dir
        self.identity = identity or SaveIdentity()

    @classmethod
    def for_pyxel_user_data(
        cls,
        identity: SaveIdentity | None = None,
    ) -> Self:
        """Create a save service rooted in Pyxel's user data directory."""
        root_dir = Path(pyxel.user_data_dir(APP_AUTHOR, APP_NAME)) / "saves"
        return cls(root_dir=root_dir, identity=identity)

    @property
    def save_path(self) -> Path:
        """Return the scoped path for the active profile and slot."""
        return self.path_for(self.identity)

    def path_for(self, identity: SaveIdentity) -> Path:
        """Return the path for a specific profile and slot."""
        return (
            self.root_dir
            / _safe_path_part(identity.profile_id)
            / f"{_safe_path_part(identity.slot_id)}.json"
        )

    def load(self) -> tuple[GameState, dict[str, Any]] | None:
        """Load only the active profile and slot."""
        path = self.save_path
        if not path.exists():
            return None

        with path.open("r", encoding="utf-8") as file:
            payload = json.load(file)
        return state_from_save_data(payload), payload.get("settings", {})

    def save(
        self,
        state: GameState,
        *,
        language: str,
        settings: dict[str, Any] | None = None,
    ) -> None:
        """Write the active save through atomic replacement."""
        path = self.save_path
        created_at = _existing_created_at(path)
        payload = state_to_save_data(
            state,
            SaveMetadata(
                profile_id=self.identity.profile_id,
                slot_id=self.identity.slot_id,
                language=language,
                settings=settings,
                created_at=created_at,
            ),
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = path.with_suffix(".tmp")
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2, sort_keys=True)
            file.write("\n")
        temporary_path.replace(path)


def _existing_created_at(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as file:
            payload = json.load(file)
    except (OSError, json.JSONDecodeError):
        return None
    created_at = payload.get("created_at")
    if isinstance(created_at, str):
        return created_at
    return None


def _safe_path_part(value: str) -> str:
    allowed = []
    for character in value.lower():
        if character.isalnum() or character in {"-", "_"}:
            allowed.append(character)
        else:
            allowed.append("-")
    safe = "".join(allowed).strip("-")
    return safe or "default"
