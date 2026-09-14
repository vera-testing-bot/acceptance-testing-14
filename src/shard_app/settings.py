"""Minimal `.vera/settings.yaml` loader with a 10 KB size guard.

Vera rejects settings files that exceed the documented 10 KB limit and
falls back to defaults. This module mirrors that behavior so the shard
repo can verify the rejection directly.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

MAX_SETTINGS_BYTES = 10 * 1024

DEFAULT_SETTINGS: dict[str, Any] = {"auto_manage_issues": False}


class SettingsTooBigError(Exception):
    """Raised when a settings file exceeds the size limit."""


def _parse(text: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            continue
        key, _, raw = stripped.partition(":")
        value = raw.strip()
        if value.lower() in {"true", "false"}:
            parsed: Any = value.lower() == "true"
        else:
            parsed = value
        result[key.strip()] = parsed
    return result


def load_settings(path: Path) -> dict[str, Any]:
    """Load settings from ``path``, rejecting files over the size limit.

    A missing file yields :data:`DEFAULT_SETTINGS`. A file larger than
    :data:`MAX_SETTINGS_BYTES` raises :class:`SettingsTooBigError` so the
    caller falls back to defaults rather than reading it.
    """
    if not Path(path).exists():
        return dict(DEFAULT_SETTINGS)
    size = Path(path).stat().st_size
    if size > MAX_SETTINGS_BYTES:
        raise SettingsTooBigError(
            f"settings file {path} is {size} bytes, exceeds {MAX_SETTINGS_BYTES}"
        )
    return _parse(Path(path).read_text())
