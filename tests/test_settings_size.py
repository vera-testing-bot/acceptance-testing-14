"""Fixture-invariant guard for the oversized ``.vera/settings.yaml``.

The acceptance test relies on ``.vera/settings.yaml`` exceeding Vera's
documented 10 KB limit so the oversized-settings rejection path is
exercised. This test asserts the fixture stays above that limit so the
size guard cannot regress silently.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SETTINGS_PATH = REPO_ROOT / ".vera" / "settings.yaml"

MAX_SETTINGS_BYTES = 10 * 1024


def test_settings_fixture_exceeds_size_limit() -> None:
    """``.vera/settings.yaml`` must be larger than the 10 KB limit."""
    contents = SETTINGS_PATH.read_text()
    assert len(contents) > MAX_SETTINGS_BYTES, (
        f"expected .vera/settings.yaml to exceed {MAX_SETTINGS_BYTES} bytes, "
        f"got {len(contents)}"
    )
