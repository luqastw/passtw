import json
import click
from passtw.paths import CONFIG_FILE
from passtw.preferences import Preferences


class ConfigurationManager:
    def _ensure_config(self):
        if not CONFIG_FILE.exists():
            default = Preferences()
            CONFIG_FILE.write_text(json.dumps(default.__dict__, indent=4))

        return CONFIG_FILE

    def read_preferences(self):
        self._ensure_config()
        raw_json = CONFIG_FILE.read_text()
        data = json.loads(raw_json)

        if not any(data.values()):
            raise click.ClickException("[ ✖ ] At least one type must be activated.")

        return Preferences(
            upper=data.get("upper", False),
            lower=data.get("lower", False),
            nums=data.get("nums", False),
            sims=data.get("sims", False),
        )

