import os
from pathlib import Path


def files_in_dir(dir: Path):
    for dirname, _, filenames in os.walk(dir):
        for filename in filenames:
            yield Path(dirname, filename)
