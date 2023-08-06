# type: ignore[attr-defined]
from typing import Optional

import json
from enum import Enum
from random import choice

import typer
import yaml
from rich.console import Console

from data_manifestor import core, version
from data_manifestor.example import hello


class Color(str, Enum):
    white = "white"
    red = "red"
    cyan = "cyan"
    magenta = "magenta"
    yellow = "yellow"
    green = "green"


app = typer.Typer(
    name="data_manifestor",
    help="Awesome `data_manifestor` is a Python cli/package created with https://github.com/TezRomacH/python-package-template",
    add_completion=False,
)
console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[yellow]data_manifestor[/] version: [bold blue]{version}[/]")
        raise typer.Exit()


@app.command(name="")
def main(
    name: str = typer.Option(..., help="Person to greet."),
    color: Optional[Color] = typer.Option(
        None,
        "-c",
        "--color",
        "--colour",
        case_sensitive=False,
        help="Color for print. If not specified then choice will be random.",
    ),
    print_version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the data_manifestor package.",
    ),
) -> None:
    """Print a greeting with a giving name."""
    if color is None:
        color = choice(list(Color))

    greeting: str = hello(name)
    console.print(f"[bold {color}]{greeting}[/]")


@app.command()
def find_files(
    directory: str,
    template_path: str,
    lims_id: str,
    subject_id: str,
    date_str: str,
    output_path: str,
    fail_if_missing: bool = typer.Option(
        None,
        "-f",
        "--fail",
        help="Raise an exception if files are missing.",
    ),
):
    with open(template_path) as f:
        template = yaml.load(f, Loader=yaml.Loader)

    results = core.compare_manifest_to_local(
        template,
        directory,
        lims_id,
        subject_id,
        date_str,
    )

    filepaths = []
    for (
        pattern,
        paths,
    ) in results.resolved_paths:
        if fail_if_missing and not len(paths) > 0:
            raise Exception("Path not found for: %s" % pattern)
        filepaths.extend(paths)

    with open(output_path, "w") as f:
        json.dump(filepaths, f)


if __name__ == "__main__":
    app()
