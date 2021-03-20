from __future__ import annotations

import json
from pathlib import Path

from . import utils

__all__ = ["load_languages", "load_languages_from_csv", "write_language_files"]

import csv
import itertools
import logging
import os
from collections import defaultdict
from enum import Enum
from typing import Optional, Type, Union

logger = logging.getLogger("babelbox")

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


def load_languages(src: Union[str, os.PathLike], prefix_identifiers=False):
    """ Loads languages from directory """

    src = Path(src)

    if src.is_dir():
        files = list(utils.files_in_dir(src))
    else:
        # Source is a file. Only load languages from that file
        files = [src]
        src = src.parent

    languages: dict[str, dict[str, str]] = defaultdict(dict)
    for f in files:
        if prefix_identifiers:
            parts = list(f.relative_to(src).parts)
            parts[-1] = parts[-1].removesuffix(f.suffix)
            prefix = ".".join(parts) + "."
        else:
            prefix = ""

        if f.suffix == ".csv":
            languages = merge_languages(languages, load_languages_from_csv(f, None, prefix))

    return languages


def merge_languages(lang1: dict[str, dict[str, str]], lang2: dict[str, dict[str, str]]):
    languages: dict[str, dict[str, str]] = defaultdict(dict)

    for lang_code, translations in itertools.chain(lang1.items(), lang2.items()):
        languages[lang_code].update(translations)

    return languages


def load_languages_from_csv(
    path: Union[str, os.PathLike], dialect: Optional[DialectLike] = None, prefix: str = ""
):
    """
    Loads csv file and parses it to a dictionary mapping each column to a language code.

    | Identifier | en_us | de_de |\n
    | car        | Car   | Auto  |\n
    | cat        | Cat   | Katze |

    => {"en_us": {"car": "Car", "cat": "Katze"}, "de_de": {"car": "Autor", "cat": "Katze"}}
    """

    with open(path, newline="", encoding="utf8") as csv_file:
        if not dialect:
            try:
                dialect = csv.Sniffer().sniff(csv_file.read(1024))
            except Exception:
                dialect = csv.excel
            finally:
                csv_file.seek(0)

        reader = csv.DictReader(csv_file, dialect=dialect)
        indentifier_column, *language_codes = reader.fieldnames or [""]

        languages: dict[str, dict[str, str]] = defaultdict(dict)
        for i, row in enumerate(reader):
            if not (identifier := row[indentifier_column]):
                if any(row.values()):
                    logger.warning(f"{path!r}@{i+2}: Non-empty line is missing identifier")
                continue

            identifier = prefix + identifier

            for code in language_codes:
                if translation := row[code]:
                    languages[code][identifier] = translation
                else:
                    logger.warning(
                        f"{path!r}: Locale {code!r} has no translation for {identifier!r}"
                    )

        return languages
