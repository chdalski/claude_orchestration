"""Tests that settings.json contains required configuration."""

import json

import pytest

from blueprint_contracts import REQUIRED_SETTINGS, REQUIRED_SETTINGS_NESTED
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


@pytest.mark.parametrize("dotted_key,expected", list(REQUIRED_SETTINGS_NESTED.items()))
def test_nested_setting(settings, dotted_key, expected):
    keys = dotted_key.split(".")
    value = settings
    for k in keys:
        assert isinstance(value, dict), (
            f"settings.json path {dotted_key!r}: expected dict at {k!r}, got {type(value).__name__}"
        )
        value = value.get(k)
    assert value == expected, (
        f"settings.json[{dotted_key!r}] should be {expected!r}, got {value!r}"
    )


def test_no_conditional_tool_loading(settings):
    """No defer_loading in settings (tool set must be fixed)."""
    settings_text = SETTINGS_FILE.read_text()
    assert "defer_loading" not in settings_text, (
        "settings.json must not use defer_loading (tool set must be fixed per caching rules)"
    )
