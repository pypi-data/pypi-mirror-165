# type: ignore[attr-defined]
from typing import Literal, Optional

import json
import logging
from enum import Enum
from random import choice

import typer
import yaml
from rich.console import Console

from np_validator import version
from np_validator.core import run_validation
from np_validator.dataclasses import dump_ValidationResult, load_ValidationStep

logging.basicConfig()
app = typer.Typer(
    name="np_validator",
    help="Awesome `np_validator` is a Python cli/package created with https://github.com/TezRomacH/python-package-template",
    add_completion=False,
)
console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[yellow]np_validator[/] version: [bold blue]{version}[/]")
        raise typer.Exit()


@app.command(name="")
def main(
    print_version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the np_validator package.",
    ),
) -> None:
    """Prints version"""


@app.command()
def validate(
    file_list_path: str,
    validation_steps_path: str,
    results_path: str,
) -> None:
    with open(file_list_path) as f:
        file_list = json.load(f)

    with open(validation_steps_path) as f:
        validation_steps = [
            load_ValidationStep(step_dict)
            for step_dict in yaml.load(f.read(), Loader=yaml.Loader)
        ]

    results = run_validation(
        file_list,
        validation_steps,
    )

    with open(results_path, "w") as f:
        json.dump([dump_ValidationResult(result) for result in results], f)


if __name__ == "__main__":
    app()
