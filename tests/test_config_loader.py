import json
import pytest
import click
from pathlib import Path
from unittest.mock import patch
from passtw.config_loader import ConfigurationManager
from passtw.preferences import Preferences

FAKE_CONFIG_PATH = Path("/fake/path/config.json")

@pytest.fixture
def mock_config_path(fs):
    fs.create_dir(FAKE_CONFIG_PATH.parent)
    with patch("passtw.config_loader.CONFIG_FILE", FAKE_CONFIG_PATH) as _path:
        yield _path

class TestConfigurationManager:

    def test_read_creates_default_file_if_missing(self, fs, mock_config_path):
        assert not FAKE_CONFIG_PATH.exists()

        manager = ConfigurationManager()
        prefs = manager.read_preferences()

        assert FAKE_CONFIG_PATH.exists()

        content = json.loads(FAKE_CONFIG_PATH.read_text())
        assert "upper" in content
        assert isinstance(prefs, Preferences)

    def test_read_loads_existing_valid_config(self, fs, mock_config_path):
        custom_config = {
            "upper": True,
            "lower": False,
            "nums": True,
            "sims": False
        }

        fs.create_file(FAKE_CONFIG_PATH, contents=json.dumps(custom_config))

        manager = ConfigurationManager()
        prefs = manager.read_preferences()

        assert prefs.upper is True
        assert prefs.lower is False
        assert prefs.nums is True

    def test_read_raises_error_if_all_false(self, fs, mock_config_path):
        bad_config = {
            "upper": False,
            "lower": False,
            "nums": False,
            "sims": False
        }
        fs.create_file(FAKE_CONFIG_PATH, contents=json.dumps(bad_config))

        manager = ConfigurationManager()

        with pytest.raises(click.ClickException) as excinfo:
            manager.read_preferences()

        assert "must be activated" in str(excinfo.value)

    def test_ensure_config_creates_directory_structure(self, fs, mock_config_path):
        manager = ConfigurationManager()

        path_returned = manager._ensure_config()

        assert path_returned == FAKE_CONFIG_PATH
        assert FAKE_CONFIG_PATH.exists()
        assert json.loads(FAKE_CONFIG_PATH.read_text()) is not None
