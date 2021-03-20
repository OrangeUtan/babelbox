import os
from pathlib import Path


def relative_path_to(file: Path, dir: Path, path_delimiter=".") -> str:
    parts = list(file.relative_to(dir).parts)
    parts[-1] = parts[-1][: -len(file.suffix)]
    return path_delimiter.join(parts)


def files_in_dir(dir: Path):
    for dirname, _, filenames in os.walk(dir):
        for filename in filenames:
            yield Path(dirname, filename)
