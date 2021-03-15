import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Optional

import typer

import babelbox


def combine_locales_from_files(files, prefix_filename=False):
    locales = defaultdict(dict)
    for f in files:
        for locale_name, translations in babelbox.load_locales_from_csv(
            f, prefix_filename=prefix_filename
        ).items():
            locales[locale_name].update(translations)

    return locales


def get_csv_files_in_dir(dir: Path):
    for entry in os.walk(dir):
        files = map(lambda f: Path(entry[0], f), entry[2])
        csv_files = filter(lambda f: f.name.endswith(".csv"), files)
        yield from csv_files


def write_locale(out_dir: Path, locale: str, entries: dict, indent: Optional[str] = None):
    with Path(out_dir, f"{locale}.json").open("w", encoding="utf-8") as f:
        json.dump(entries, f, indent=indent, ensure_ascii=False)


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
    pretty_print: bool = typer.Option(
        False, "--pretty-print", "-p", help="Pretty print json", is_flag=True
    ),
    indent: str = typer.Option(
        "\t", "--indent", "-i", help="String used to indent json", show_default=repr("\t")
    ),
    prefix_filename: bool = typer.Option(
        False,
        "--prefix-filename",
        "-n",
        help="Prefix variables with the filename (without extension)",
        is_flag=True,
    ),
    version: bool = typer.Option(
        None, "--version", "-v", callback=version_callback, is_eager=True
    ),
):
    """Create language localization files from csv files"""

    out_dir = out_dir if out_dir is not None else src_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_files = get_csv_files_in_dir(src_dir)
    for locale_name, entries in combine_locales_from_files(csv_files, prefix_filename).items():
        write_locale(out_dir, locale_name, entries, indent if pretty_print else None)


if __name__ == "__main__":
    app()  # pragma: no cover
