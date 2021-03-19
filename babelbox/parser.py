from __future__ import annotations

__all__ = ["load_languages_from_csv"]

import csv
import logging
import os
from collections import defaultdict
from typing import Optional, Type, Union

logger = logging.getLogger(__name__)

DialectLike = Union[str, csv.Dialect, Type[csv.Dialect]]
PathLike = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]


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
