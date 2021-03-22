import enum
import logging
from pathlib import Path
from typing import List, Optional

import typer

import babelbox

from .parser import load_languages, merge_languages, write_language_files


class CSVDialect(enum.Enum):
    EXCEL = "excel"
    EXCEL_TAB = "excel-tab"
    UNIX = "unix"


def version_callback(value: bool):
    if value:
        typer.echo(f"Babelbox: {babelbox.__version__}")
        raise typer.Exit()


app = typer.Typer()


@app.command()
def main(
    sources: List[Path] = typer.Argument(
        ..., exists=True, readable=True, help="File or directory containing languages"
    ),
    out: Optional[Path] = typer.Option(
        None,
        "-o",
        "--out",
        help="The output directory of the generated files",
        file_okay=False,
        writable=True,
    ),
    prefix_identifiers: bool = typer.Option(
        False,
        "--prefix-identifiers",
        "-p",
        is_flag=True,
        help="Prefix identifiers with their path relative to their SOURCES entry",
    ),
    dialect: Optional[CSVDialect] = typer.Option(
        None,
        "--dialect",
        help="CSV dialect used to parse CSV. Dialect will be automatically detected of omitted",
    ),
    delimiter: Optional[str] = typer.Option(
        None, "-d", "--delimiter", help="CSV delimiter overwrite"
    ),
    quotechar: Optional[str] = typer.Option(
        None, "--quotechar", help="CSV quote char overwrite"
    ),
    minify: bool = typer.Option(
        False, "--minify", "-m", is_flag=True, flag_value=True, help="Minify generated files"
    ),
    indent: str = typer.Option(
        "\t", "--indent", "-i", help="Indentation used when generating files"
    ),
    dry: bool = typer.Option(
        False, "--dry", help="Dry run. Don't generate any files", is_flag=True
    ),
    verbose: bool = typer.Option(
        False, "-v", "--verbose", is_flag=True, help="Increase verbosity"
    ),
    quiet: bool = typer.Option(
        False, "-q", "--quiet", is_flag=True, help="Only output errors"
    ),
    version: bool = typer.Option(None, "--version", callback=version_callback, is_eager=True),
):
    """Create language localization files from csv files"""

    if quiet:
        loglevel = logging.ERROR
    elif verbose:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING

    logging.basicConfig(
        level=loglevel,
        format="{levelname}: {message}",
        style="{",
    )

    if out is None:
        if len(sources) == 1:
            out = sources[0] if sources[0].is_dir() else sources[0].parent
        else:
            typer.secho(
                "Multiple sources but no output specified", err=True, fg=typer.colors.RED
            )
            raise typer.Exit(code=1)

    csv_dialect_overwrites = {}
    if delimiter:
        csv_dialect_overwrites["delimiter"] = delimiter
    if quotechar:
        csv_dialect_overwrites["quotechar"] = quotechar

    languages = merge_languages(
        map(
            lambda src: load_languages(
                src,
                prefix_identifiers,
                dialect=dialect.value if dialect else None,
                csv_dialect_overwrites=csv_dialect_overwrites,
            ),
            sources,
        )
    )

    if not dry:
        out.mkdir(parents=True, exist_ok=True)
        write_language_files(out, languages, indent if not minify else None)
