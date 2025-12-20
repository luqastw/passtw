import click
import json
import os
import platform
import pyperclip
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
    click.secho("[ ⏻ ] Succefully initialized!", fg='bright_green')
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
    click.secho("[ ⚙ ] Configuration updated.", fg='cyan')
    for option in options:
        if option == "all":
            set_all_values(True)
            click.secho(":     All options →  enabled.", fg='green')
            break

        if option in config_data:
            set_config_value(option, True)
            click.secho(f":     {full_name(option)} →> enabled.", fg='green')
        else:
            click.secho(f":     {option} →  not found.", fg='red')
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
    click.secho("[ ⚙ ] Configuration updated.", fg='cyan')
    for option in options:
        if option == "all":
            set_all_values(False)
            click.secho(":     All options →  disabled.", fg='green')
            break

        if option in config_data:
            set_config_value(option, False)
            click.secho(f":     {full_name(option)} →  disabled.", fg='green')
        else:
            click.secho(f":     {option} →  not found.", fg='red')
    click.echo("")


@passtw.command()
@require_init
def config():
    """Show actual configuration."""

    ensure_vault()
    config_data = json.loads(CONFIG_FILE.read_text())
    vault_data = json.loads(VAULT_FILE.read_text())

    click.echo("")
    click.secho("[ ⚙ ] Configuration:", fg='cyan')
    for name, value in config_data.items():
        symbol = "✓" if value else "✗"
        click.secho(f'  {symbol}   ', fg='white', nl=False)
        click.secho(f'{full_name(name)}', fg='bright_black')
    click.echo("")
    click.secho(f"[ {len(vault_data)} ] Passwords in vault.", fg='bright_black')
    if not KEY_FILE.exists():
        click.secho("[ ✗ ] Key not activated.", fg='red')
    else:
        click.secho("[ ✓ ] Key activated.", fg='green')
    click.echo("")


@passtw.command()
@require_init
def keygen():
    """Generate a new cryptographic key."""

    if not KEY_FILE.exists():
        generate_key()
        click.echo("")
        click.secho("[ ✓ ] Cryptgraphic key succefully generated.", fg='green')
        click.echo("")
    else:
        click.echo("")
        click.secho("[ ✗ ] Cryptgraphic key already exists.", fg='red')
        click.echo("")


@passtw.command()
@require_init
@click.argument("name")
def generate(name):
    """Generate new password."""
    create_password(name)
    click.echo("")
    click.secho("[ ✓ ] Password created.", fg='green')
    click.secho(f":     {name} allocated in your vault.", fg='bright_black')
    click.echo("")


@passtw.command()
@require_init
@click.argument("name")
@click.option('--copy', '-c', is_flag=True, help='Copy the selected password to clipboard.')
def get(name, copy):
    """Get password from vault."""
    password = get_password(name)
    if copy:
        pyperclip.copy(password)
        click.echo("")
        click.secho('[ ✓ ] ', fg='green', nl=False) 
        click.secho(f'Passtword for {name} copied to clipboard.', fg='bright_black')
        click.echo("")
    else:
        click.echo("")
        click.secho('[ ✓ ] ', fg='green', nl=False)
        click.secho('Vault unlocked succefully.', fg='bright_black')
        click.secho(':     Service  : ', fg='bright_black', nl=False)
        click.secho(f'{name}', fg='cyan', bold=True)
        click.secho(':     Password : ', fg='bright_black', nl=False)
        click.secho(f'{password}', fg='cyan', bold=True)
        click.echo("")


if __name__ == "__main__":
    passtw()

