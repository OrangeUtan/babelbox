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
    src_dir: Path = typer.Argument(..., exists=True, file_okay=False, readable=True),
    out_dir: Optional[Path] = typer.Argument(
        None,
        help="The directory in which to generate the language localization files",
        file_okay=False,
        writable=True,
    ),
    indent: str = typer.Option("\t", "--indent", "-i", help="String used to indent json"),
    minify: bool = typer.Option(False, "--minify", "-m", is_flag=True, flag_value=True),
    prefix_identifiers: bool = typer.Option(
        False, "--prefix-identifiers", "-p", help="Prefix identifiers", is_flag=True
    ),
    version: bool = typer.Option(
        None, "--version", "-v", callback=version_callback, is_eager=True
    ),
    dry: bool = typer.Option(
        False, "--dry", help="Dry run. Don't create any files", is_flag=True
    ),
    verbose: bool = typer.Option(False, "-v", "--verbose", is_flag=True),
):
    """Create language localization files from csv files"""

    logging.basicConfig(
        level=logging.INFO if verbose else logging.WARNING,
        format="{levelname}: {message}",
        style="{",
    )

    out_dir = out_dir if out_dir is not None else src_dir
    if not dry:
        out_dir.mkdir(parents=True, exist_ok=True)

    languages = load_languages(src_dir, prefix_identifiers)
    write_language_files(out_dir, languages, indent if not minify else None)
