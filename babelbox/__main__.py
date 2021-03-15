import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Optional

import typer

import babelbox


def combine_locales_from_files(files):
    locales = defaultdict(dict)
    for f in files:
        for locale_name, translations in babelbox.load_locales_from_csv(f).items():
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
    src_dir: str,
    out_dir: Optional[str] = typer.Argument(
        None, help="The directory in which to generate the language localization files"
    ),
    indent: str = typer.Option("\t", help="String used to indent json"),
    no_indent: int = typer.Option(
        False, help="Don't pretty print json with indentation", is_flag=True, flag_value=True
    ),
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    ),
):
    src_dir_path = Path(src_dir)
    if not src_dir_path.exists():
        raise FileNotFoundError(src_dir_path)
    out_dir_path = Path(out_dir) if out_dir else Path(src_dir_path)
    out_dir_path.mkdir(parents=True, exist_ok=True)

    csv_files = get_csv_files_in_dir(src_dir_path)
    for locale_name, entries in combine_locales_from_files(csv_files).items():
        write_locale(out_dir_path, locale_name, entries, None if no_indent else indent)


if __name__ == "__main__":
    app()  # pragma: no cover
