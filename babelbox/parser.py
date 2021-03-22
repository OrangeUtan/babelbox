from __future__ import annotations

import json
from pathlib import Path

from . import utils

__all__ = [
    "load_languages",
    "load_languages_from_csv",
    "write_language_files",
    "merge_languages",
]

import csv
import logging
import os
from collections import defaultdict
from typing import Iterable, Optional, Type, Union

logger = logging.getLogger(__name__)

DialectLike = Union[str, csv.Dialect, Type[csv.Dialect]]


def write_language_files(
    dest_dir: Union[str, os.PathLike],
    languages: dict[str, dict[str, str]],
    indent: Optional[str] = None,
):
    for language_code, translations in languages.items():
        path = Path(dest_dir, language_code + ".json")
        logging.info(f"Writing language file {path!r}")
        with open(path, "w", encoding="utf8") as f:
            json.dump(translations, f, indent=indent, ensure_ascii=False)


def load_languages(
    src: Union[str, os.PathLike],
    prefix_identifiers=False,
    dialect: Optional[DialectLike] = None,
    csv_dialect_overwrites: Optional[dict] = None,
):
    """ Loads languages from directory """

    src = Path(src)

    if src.is_dir():
        files = list(utils.files_in_dir(src))
    else:
        # Source is a file. Only load languages from that file
        files = [src]
        src = src.parent

    file_languages: list[dict[str, dict[str, str]]] = []
    for f in files:
        prefix = utils.relative_path_to(f, src) + "." if prefix_identifiers else ""

        if f.suffix == ".csv":
            file_languages.append(
                load_languages_from_csv(
                    f, prefix, dialect=dialect, dialect_overwrites=csv_dialect_overwrites
                )
            )

    return merge_languages(file_languages)


def merge_languages(language_collections: Iterable[dict[str, dict[str, str]]]):
    result: dict[str, dict[str, str]] = defaultdict(dict)

    for languages in language_collections:
        for language_code, translations in languages.items():
            result[language_code].update(translations)

    return result


def load_languages_from_csv(
    path: Union[str, os.PathLike],
    prefix: str = "",
    dialect: Optional[DialectLike] = None,
    dialect_overwrites: Optional[dict] = None,
):
    """
    Loads csv file and parses it to a dictionary mapping each column to a language code.

    | Identifier | en_us | de_de |\n
    | car        | Car   | Auto  |\n
    | cat        | Cat   | Katze |

    => {"en_us": {"car": "Car", "cat": "Katze"}, "de_de": {"car": "Autor", "cat": "Katze"}}
    """

    with open(path, newline="", encoding="utf8") as csv_file:

        if dialect is None:
            try:
                dialect = csv.Sniffer().sniff(csv_file.read(1024))
            except Exception:
                dialect = csv.excel
            finally:
                csv_file.seek(0)

        reader = csv.DictReader(csv_file, dialect=dialect, **(dialect_overwrites or {}))
        indentifier_column, *language_codes = reader.fieldnames or [""]

        languages: dict[str, dict[str, str]] = defaultdict(dict)
        for i, row in enumerate(reader):
            if not (identifier := row[indentifier_column]):
                if any(row.values()):
                    logger.warning(f"{path!r}@{i+2}: Non-empty line is missing identifier")
                continue

            # Skip comments
            if identifier.startswith("#") and not any(map(lambda l: row[l], language_codes)):
                continue

            identifier = prefix + identifier

            for code in language_codes:
                if not (translation := row[code]):
                    logger.warning(
                        f"{path!r}: Locale {code!r} has no translation for {identifier!r}"
                    )
                    translation = ""

                languages[code][identifier] = translation

        return languages
