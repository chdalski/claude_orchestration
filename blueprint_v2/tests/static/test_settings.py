"""Tests that settings.json contains required configuration."""

import json

import pytest

from blueprint_contracts import REQUIRED_SETTINGS
from conftest import SETTINGS_FILE

pytestmark = pytest.mark.static


@pytest.fixture
def settings():
    return json.loads(SETTINGS_FILE.read_text())


@pytest.mark.parametrize("key,expected", list(REQUIRED_SETTINGS.items()))
def test_top_level_setting(settings, key, expected):
    actual = settings.get(key)
    assert actual == expected, (
        f"settings.json[{key!r}] should be {expected!r}, got {actual!r}"
    )


def test_no_default_mode(settings):
    """settings.json must not set defaultMode — plan mode enforcement is unreliable."""
    permissions = settings.get("permissions", {})
    assert "defaultMode" not in permissions


def test_no_conditional_tool_loading(settings):
    """No defer_loading in settings (tool set must be fixed)."""
    settings_text = SETTINGS_FILE.read_text()
    assert "defer_loading" not in settings_text, (
        "settings.json must not use defer_loading (tool set must be fixed per caching rules)"
    )
