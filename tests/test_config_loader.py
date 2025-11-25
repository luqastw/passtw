from src.config_loader import ConfigurationManager

def test_ensure_file_exists():
    manager = ConfigurationManager()
    manager._ensure_config()

def test_read_preferences():
    manager = ConfigurationManager()
    manager.read_preferences()