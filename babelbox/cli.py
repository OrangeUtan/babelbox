import json
import logging
from pathlib import Path
from typing import Optional

import typer

import babelbox
from babelbox.parser import load_languages, write_language_files

logger = logging.getLogger("babelbox")


def version_callback(value: bool):
    if value:
        typer.echo(f"Babelbox: {babelbox.__version__}")
        raise typer.Exit()


app = typer.Typer()


@app.command()
def main(
    src: Path = typer.Argument(
        ..., exists=True, readable=True, help="File or directory containing languages"
    ),
    out: Optional[Path] = typer.Option(
        None,
        "-o",
        help="The output directory of the generated files",
        file_okay=False,
        writable=True,
    ),
    indent: str = typer.Option(
        "\t", "--indent", "-i", help="Indentation used when generating files"
    ),
    minify: bool = typer.Option(
        False, "--minify", "-m", is_flag=True, flag_value=True, help="Minify generated files"
    ),
    prefix_identifiers: bool = typer.Option(
        False,
        "--prefix-identifiers",
        "-p",
        is_flag=True,
        help="Prefix identifiers with their path relative to SRC",
    ),
    dry: bool = typer.Option(
        False, "--dry", help="Dry run. Don't generate any files", is_flag=True
    ),
    verbose: bool = typer.Option(
        False, "-v", "--verbose", is_flag=True, help="Increase verbosity"
    ),
    version: bool = typer.Option(None, "--version", callback=version_callback, is_eager=True),
):
    """Create language localization files from csv files"""

    logging.basicConfig(
        level=logging.INFO if verbose else logging.WARNING,
        format="{levelname}: {message}",
        style="{",
    )

    if out is None:
        out = src if src.is_dir() else src.parent

    languages = load_languages(src, prefix_identifiers)

    if not dry:
        out.mkdir(parents=True, exist_ok=True)
        write_language_files(out, languages, indent if not minify else None)
