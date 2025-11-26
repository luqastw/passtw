import click
from src.config_loader import ConfigurationManager
from src.generator import create_password, get_password
from src.paths import CONFIG_FILE
import json

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

@click.group()
def passtw():
    """Command line interface of passtw."""

@passtw.command()
@click.argument("name")
def generate(name):
    """Generate password."""
    create_password(name)
    click.echo(f"Password '{name}' created.")

@passtw.command()
@click.argument("options", nargs=-1)
def set(options):
    """Activate characters."""
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
@click.argument("options", nargs=-1)
def unset(options):
    """Disable characters."""
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
@click.argument("name")
def generate(name):
    """Generate new password."""
    create_password(name)
    click.echo(f"Password '{name}' created.")

@passtw.command()
@click.argument("name")
def get(name):
    """Get password."""
    password = get_password(name)
    click.echo(f"{name}: {password}")

if __name__ == "__main__":
    passtw()
