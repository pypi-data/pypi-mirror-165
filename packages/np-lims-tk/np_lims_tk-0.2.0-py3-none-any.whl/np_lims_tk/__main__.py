# type: ignore[attr-defined]
from typing import Optional

import json
from random import choice

import typer
from rich.console import Console

from np_lims_tk import core, version

app = typer.Typer(
    name="np_lims_tk",
    help="Awesome `np_lims_tk` is a Python cli/package created with https://github.com/TezRomacH/python-package-template",
    add_completion=False,
)
console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[yellow]np-lims-tk[/] version: [bold blue]{version}[/]")
        raise typer.Exit()


@app.command(name="")
def main(
    print_version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the np_lims_tk package.",
    ),
) -> None:
    """Print version."""


@app.command()
def find_lims_files(
    filepaths_json: str,
    output_path: str,
    db_uri: Optional[str] = typer.Option(
        None,
        "-d",
        "--db-uri",
        help="Database uri for lims connection. If not supplied, defaults to allen_config_auto_discovery.",
    ),
):
    with open(filepaths_json) as f:
        filepaths = json.load(f)

    results = []
    for filepath in filepaths:
        try:
            found = core.find_files(
                db_uri=db_uri,
                local_path=filepath,
            )
            error = None
        except Exception as e:
            found = None
            error = str(e)

        result = {
            "filepath": filepath,
            "found": found,
            "error": error,
        }
        results.append(result)

    with open(output_path, "w") as f:
        json.dump(results, f)


if __name__ == "__main__":
    app()
