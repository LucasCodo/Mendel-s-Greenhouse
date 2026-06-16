"""Profile-scoped autosave service."""

import importlib
import json
import sys
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
WEB_STORAGE_PREFIX = "mendels-greenhouse:save"


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
        payload = self._load_payload()
        if payload is None:
            return None

        return state_from_save_data(payload), payload.get("settings", {})

    def save(
        self,
        state: GameState,
        *,
        language: str,
        settings: dict[str, Any] | None = None,
    ) -> None:
        """Write the active save to the current runtime storage."""
        created_at = self._existing_created_at()
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
        self._write_payload(payload)

    def _load_payload(self) -> dict[str, Any] | None:
        if _is_web_runtime():
            return _web_load_payload(self._web_storage_key())

        path = self.save_path
        if not path.exists():
            return None

        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _write_payload(self, payload: dict[str, Any]) -> None:
        if _is_web_runtime():
            _web_save_payload(self._web_storage_key(), payload)
            return

        path = self.save_path
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = path.with_suffix(".tmp")
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2, sort_keys=True)
            file.write("\n")
        temporary_path.replace(path)

    def _existing_created_at(self) -> str | None:
        try:
            payload = self._load_payload()
        except (OSError, json.JSONDecodeError):
            return None
        if payload is None:
            return None
        created_at = payload.get("created_at")
        if isinstance(created_at, str):
            return created_at
        return None

    def _web_storage_key(self) -> str:
        return ":".join(
            (
                WEB_STORAGE_PREFIX,
                _safe_path_part(self.identity.profile_id),
                _safe_path_part(self.identity.slot_id),
            ),
        )


def _is_web_runtime() -> bool:
    return sys.platform == "emscripten"


def _web_storage() -> Any:
    js = importlib.import_module("js")
    return js.localStorage


def _web_load_payload(key: str) -> dict[str, Any] | None:
    saved = _web_storage().getItem(key)
    if saved is None:
        return None
    saved_text = str(saved)
    if saved_text in {"", "None", "null", "undefined"}:
        return None
    try:
        payload = json.loads(saved_text)
    except json.JSONDecodeError:
        return None
    if isinstance(payload, dict):
        return payload
    return None


def _web_save_payload(key: str, payload: dict[str, Any]) -> None:
    _web_storage().setItem(key, json.dumps(payload, sort_keys=True))


def _safe_path_part(value: str) -> str:
    allowed = []
    for character in value.lower():
        if character.isalnum() or character in {"-", "_"}:
            allowed.append(character)
        else:
            allowed.append("-")
    safe = "".join(allowed).strip("-")
    return safe or "default"
