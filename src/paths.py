from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

CONFIG_FILE = DATA_DIR / "config.json"
KEY_FILE = DATA_DIR / "secret.key"
VAULT_FILE = DATA_DIR / "vault.json"