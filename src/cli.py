import click, json, os, platform
from pathlib import Path
from functools import wraps
from src.config_loader import ConfigurationManager
from src.generator import create_password, get_password
from src.paths import CONFIG_FILE

def get_state_file() -> Path:
    system = platform.system()

    if system == "Linux":
        return Path.home() / ".local/state/passtw/state.json"
    elif system == "Darwin":
        return Path.home() / "Library/Application Support/passtw/state.json"
    elif system.startswith(("CYGWIN", "MSYS", "Windows", "MINGW")):
        return Path(os.getenv("APPDATA", Path.home())) / "passtw/state.json"

    return Path.home() / "passtw_state.json"

def is_initialized() -> bool:
    f = get_state_file()
    if not f.exists():
        return False

    try:
        data = json.loads(f.read_text())
        return data.get("initialized", False)
    except:
        return False

def run_init():
    manager = ConfigurationManager()
    f = get_state_file()
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps({"initialized": True}, indent=4))
    manager._ensure_config()
    click.echo("[ ✓ ] Succefully initialized!")


def set_config_value(key: str, value: bool):
    manager = ConfigurationManager()
    manager._ensure_config()
    config = json.loads(CONFIG_FILE.read_text())
    config[key] = value

    return CONFIG_FILE.write_text(json.dumps(config, indent=4))

def set_all_values(value: bool):
    manager = ConfigurationManager()
    manager._ensure_config()
    config = json.loads(CONFIG_FILE.read_text())
    config["upper"] = value
    config["lower"] = value
    config["nums"] = value
    config["sims"] = value

    return CONFIG_FILE.write_text(json.dumps(config, indent=4))

def require_init(f):
    """Blocks any command until it's not initialized."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_initialized():
            raise click.ClickException(
                "[ ✖ ] Run 'passtw init' to start."
            )
        return f(*args, **kwargs)
    return wrapper

@click.group()
def passtw():
    """Command line interface of passtw."""
    pass

@passtw.command()
def init():
    """Initialize passtw."""
    run_init()

@passtw.command()
@require_init
@click.argument("options", nargs=-1)
def set(options):
    """Activate characters."""
    manager = ConfigurationManager()
    manager._ensure_config()
    config_data = json.loads(CONFIG_FILE.read_text())

    for option in options:
        if option == "all":
            set_all_values(True)
            click.echo("all chars activated.")
            break

        if option in config_data:
            set_config_value(option, True)
            click.echo(f"{option} activated.")
        else:
            click.echo(f"{option} not found.")

@passtw.command()
@require_init
@click.argument("options", nargs=-1)
def unset(options):
    """Disable characters."""
    manager = ConfigurationManager()
    manager._ensure_config()
    config_data = json.loads(CONFIG_FILE.read_text())

    for option in options:
        if option == "all":
            set_all_values(False)
            click.echo("all chars disabled.")
            break

        if option in config_data:
            set_config_value(option, False)
            click.echo(f"{option} disabled.")
        else:
            click.echo(f"{option} not found.")

@passtw.command()
@require_init
@click.argument("name")
def generate(name):
    """Generate new password."""
    create_password(name)
    click.echo(f"Password '{name}' created.")

@passtw.command()
@require_init
@click.argument("name")
def get(name):
    """Get password."""
    password = get_password(name)
    click.echo(f"{name}: {password}")

if __name__ == "__main__":
    passtw()
