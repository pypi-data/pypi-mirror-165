from pathlib import Path

import typer

from .config import read_config, save_config
from .generation import generate, save_data


def init_cli() -> typer.Typer:
    cli = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})
    cli.command("create")(create_config)
    cli.command("c", hidden=True)(create_config)
    cli.command("generate")(generate_)
    cli.command("g", hidden=True)(generate_)
    return cli


def run_cli() -> None:
    cli = init_cli()
    cli()


def create_config(
    config: str = typer.Argument(
        ..., help="Path of the config to complete or create"
    ),
) -> None:
    """
    (c) Creates a config or completes it, saving it to the given file.
    """
    path = Path(config)
    config_ = read_config(path)
    save_config(config_, path)


def generate_(
    config: str = typer.Argument(..., help="Configuration file to use")
) -> None:
    """
    (g) Generates the data for the given config, saving it as a json file named
    "data.json".
    """
    config_ = read_config(Path(config))
    data = generate(config_)
    save_data(data)
