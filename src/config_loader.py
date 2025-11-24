import json
from src.paths import CONFIG_FILE
from src.preferences import Preferences

class ConfigurationManager():
    def _ensure_config(self):
        if not CONFIG_FILE.exists():
            self.default = Preferences()
            CONFIG_FILE.write_text(json.dumps(self.default.__dict__, indent=4))
            print("Configuration file not found. Creating default...") 

        return CONFIG_FILE

    def read_preferences(self):
        self._ensure_config()
        self.raw_json = CONFIG_FILE.read_text()
        self.data = json.loads(self.raw_json)

        if any(self.data.values()):
            return Preferences(
                upper=self.data["upper"], 
                lower=self.data["lower"],
                nums=self.data["nums"],
                sims=self.data["sims"]
            )
        else:
            raise ValueError("At least one type must be activated.")

    def save_preferences(self):
        self.data = {
            "upper": Preferences.upper,
            "lower": Preferences.lower,
            "nums": Preferences.nums,
            "sims": Preferences.sims
        }

        self.json_string = json.dumps(self.data, indent=4)
        return CONFIG_FILE.write_text(self.json_string)