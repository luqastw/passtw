import json
from src.paths import CONFIG_FILE
from src.preferences import Preferences

def read_preferences():
    raw_json = CONFIG_FILE.read_text()
    data = json.loads(raw_json)
    return Preferences(
        use_upper=data["use_upper"], 
        use_lower=data["use_lower"],
        use_nums=data["use_nums"],
        use_sims=data["use_sims"],
        length=data["length"]    
    )

def save_preferences(prefs: Preferences):
    data = {
        "length": prefs.length,
        "use_upper": prefs.use_upper,
        "use_lower": prefs.use_lower,
        "use_digits": prefs.use_digits,
        "use_symbols": prefs.use_symbols
    }

    json_string = json.dumps(data, indent=4)
    CONFIG_FILE.write_text(json_string)
