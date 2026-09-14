"""Verify an oversized `.vera/settings.yaml` is rejected.

These tests pin the documented product behavior that a settings file
larger than the 10 KB limit is rejected and the loader falls back to
defaults instead of reading it.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from shard_app.settings import (
    MAX_SETTINGS_BYTES,
    SettingsTooBigError,
    load_settings,
)


def test_oversized_settings_file_is_rejected(tmp_path: Path) -> None:
    """A settings file over the size limit must raise and not be read."""
    settings = tmp_path / "settings.yaml"
    settings.write_bytes(b"x" * (MAX_SETTINGS_BYTES + 1))

    raised = False
    try:
        load_settings(settings)
    except SettingsTooBigError:
        raised = True
    assert raised, "oversized settings file was not rejected"


def test_undersized_settings_file_is_accepted(tmp_path: Path) -> None:
    """A settings file under the size limit is read normally."""
    settings = tmp_path / "settings.yaml"
    settings.write_bytes(b"auto_manage_issues: false\n")

    result = load_settings(settings)
    assert result == {"auto_manage_issues": False}


def test_default_settings_used_when_file_missing(tmp_path: Path) -> None:
    """A missing settings file yields the documented defaults."""
    result = load_settings(tmp_path / "missing.yaml")
    assert result == {"auto_manage_issues": False}
