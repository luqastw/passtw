import json
from src.paths import CONFIG_FILE
from src.preferences import Preferences

def ensure_config():
    if not CONFIG_FILE.exists():
        default = Preferences()
        CONFIG_FILE.write_text(json.dumps(default.__dict__, indent=4))
        print("Configuration file not found. Creating default...")
        return default

def read_preferences():
    ensure_config()
    raw_json = CONFIG_FILE.read_text()
    data = json.loads(raw_json)
    return Preferences(
        upper=data["upper"], 
        lower=data["lower"],
        nums=data["nums"],
        sims=data["sims"]
    )

def save_preferences(prefs: Preferences):
    data = {
        "upper": prefs.upper,
        "lower": prefs.lower,
        "nums": prefs.nums,
        "sims": prefs.sims
    }

    json_string = json.dumps(data, indent=4)
    CONFIG_FILE.write_text(json_string)