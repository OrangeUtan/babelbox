from __future__ import annotations

import csv
import warnings
from collections import defaultdict
from pathlib import Path
from typing import Iterator, List, Optional, Union, cast


class CSVError(Exception):
    pass


def repr_dialect(dialect: csv.Dialect):
    return f"Dialect(delimiter={repr(dialect.delimiter)}, escapechar={repr(dialect.escapechar)}, lineterminator={repr(dialect.lineterminator)}, quoting={repr(dialect.quoting)}, doublequote={repr(dialect.doublequote)}, skipinitialspace={repr(dialect.skipinitialspace)})"


def load_locales_from_csv(file: Union[str, Path], dialect: Optional[csv.Dialect] = None):
    file = Path(file)

    with file.open("r", encoding="utf-8") as f:
        if dialect is None:
            # Try to guess dialect or fall back to excel
            try:
                dialect = cast(csv.Dialect, csv.Sniffer().sniff(f.read(1024)))
            except Exception:
                warnings.warn(
                    f"Couldn't determine csv dialect of {repr(str(file))}. Falling back to 'excel'",
                    UserWarning,
                )
                dialect = csv.get_dialect("excel")
            finally:
                f.seek(0)

        reader = csv.reader(f, dialect=dialect)

        try:
            header = next(reader)
        except StopIteration as e:
            raise CSVError(
                f"Failed to read '{str(file)}'. Either file is empty or the dialect is wrong: '{repr_dialect(dialect)}'"
            ) from e

        id_column_name, locale_names = header[0], header[1:]
        locales = create_locales_from_csv(locale_names, reader)

    return locales


def create_locales_from_csv(locale_names: List[str], rows: Iterator[List[str]]):
    locales: defaultdict[str, dict[str, str]] = defaultdict(dict)
    for row in rows:
        entry, translations = row[0], row[1:]
        for name, translation in zip(locale_names, translations):
            locales[name][entry] = translation

    return locales
