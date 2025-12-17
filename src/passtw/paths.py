import os
from platformdirs import user_data_dir
from pathlib import Path

def get_data_dir() -> Path:
    dev_mode = os.getenv('PASSTW_ENV') == 'dev'

    if dev_mode:
        ROOT_DIR = Path.cwd()
        DATA_DIR = ROOT_DIR / 'data'
        print('')
        print(f'[ ! ] Dev Mode Actived. Using: {DATA_DIR}')
        print('')
    else:
        SYS_PATH = user_data_dir(appname='passtw')
        DATA_DIR = Path(SYS_PATH)
    
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    return DATA_DIR

DATA_DIR = get_data_dir()

CONFIG_FILE = DATA_DIR / "config.json"
KEY_FILE = DATA_DIR / "secret.key"
VAULT_FILE = DATA_DIR / "vault.json"