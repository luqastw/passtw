import click
import json
import os
import platform
from pathlib import Path
from functools import wraps
from passtw.keygen import generate_key
from passtw.generator import create_password, get_password
from passtw.config_loader import ConfigurationManager
from passtw.paths import CONFIG_FILE, VAULT_FILE, KEY_FILE

config_manager = ConfigurationManager()
OPTION_NAMES = {
    "upper": "Uppercase",
    "lower": "Lowercase",
    "nums": "Digits",
    "sims": "Symbols",
}


def ensure_vault():
    if VAULT_FILE.exists():
        return json.loads(VAULT_FILE.read_text())
    else:
        return VAULT_FILE.write_text(json.dumps({}, indent=4))


def full_name(option: str) -> str:
    return OPTION_NAMES.get(option, option)


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
    except (FileNotFoundError, json.JSONDecodeError):
        return False


def run_init():
    generate_key()
    ensure_vault()
    config_manager._ensure_config()
    f = get_state_file()
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps({"initialized": True}, indent=4))
    click.echo("")
    click.echo("[ ⏻ ] Succefully initialized!")
    click.echo("")


def set_config_value(key: str, value: bool):
    config_manager._ensure_config()
    config = json.loads(CONFIG_FILE.read_text())
    config[key] = value

    return CONFIG_FILE.write_text(json.dumps(config, indent=4))


def set_all_values(value: bool):
    config_manager._ensure_config()
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
            raise click.ClickException("[ ✖ ] Type 'passtw init' to start.")
        return f(*args, **kwargs)

    return wrapper


@click.group()
def passtw():
    """Command line interface of passtw."""
    pass


@passtw.command()
def init():
    """Initialize passtw dependencies."""
    run_init()


@passtw.command()
@require_init
@click.argument("options", nargs=-1)
def set(options):
    """Enable characters in password pool."""

    config_manager._ensure_config()
    config_data = json.loads(CONFIG_FILE.read_text())

    click.echo("")
    click.echo("[ ⚙ ] Configuration updated.")
    for option in options:
        if option == "all":
            set_all_values(True)
            click.echo(":     All options → enabled.")
            break

        if option in config_data:
            set_config_value(option, True)
            click.echo(f":     {full_name(option)} → enabled.")
        else:
            click.echo(f":     {option} → not found.")
    click.echo("")


@passtw.command()
@require_init
@click.argument("options", nargs=-1)
def unset(options):
    """Disable characters in password pool."""

    manager = ConfigurationManager()
    manager._ensure_config()
    config_data = json.loads(CONFIG_FILE.read_text())

    click.echo("")
    click.echo("[ ⚙ ] Configuration updated.")
    for option in options:
        if option == "all":
            set_all_values(False)
            click.echo(":     All options → disabled.")
            break

        if option in config_data:
            set_config_value(option, False)
            click.echo(f":     {full_name(option)} → disabled.")
        else:
            click.echo(f":     {option} → not found.")
    click.echo("")


@passtw.command()
@require_init
def config():
    """Show actual configuration."""

    ensure_vault()
    config_data = json.loads(CONFIG_FILE.read_text())
    vault_data = json.loads(VAULT_FILE.read_text())

    click.echo("")
    click.echo("[ ⚙ ] Configuration:")
    for name, value in config_data.items():
        symbol = "✓" if value else "✗"
        click.echo(f"  {symbol}   {full_name(name)}")
    click.echo("")
    click.echo(f"[ {len(vault_data)} ] Passwords in vault.")
    if not KEY_FILE.exists():
        click.echo("[ ✗ ] Key not activated.")
    else:
        click.echo("[ ✓ ] Key activated.")
    click.echo("")


@passtw.command()
@require_init
def keygen():
    """Generate a new cryptographic key."""

    if not KEY_FILE.exists():
        generate_key()
        click.echo("")
        click.echo("[ ✓ ] Cryptgraphic key succefully generated.")
        click.echo("")
    else:
        click.echo("")
        click.echo("[ ✗ ] Cryptgraphic key already exists.")
        click.echo("")


@passtw.command()
@require_init
@click.argument("name")
def generate(name):
    """Generate new password."""
    create_password(name)
    click.echo("")
    click.echo("[ ✓ ] Password created!")
    click.echo(f":     {name} allocated in your vault.")
    click.echo("")


@passtw.command()
@require_init
@click.argument("name")
def get(name):
    """Get password from vault."""
    password = get_password(name)
    click.echo("")
    click.echo("[ ✓ ] Vault open!")
    click.echo(f":     {name}: {password}")
    click.echo("")


if __name__ == "__main__":
    passtw()

