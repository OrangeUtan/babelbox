from pathlib import Path

import pytest

from babelbox import utils


class Test_relative_path_to:
    @pytest.mark.parametrize(
        "path, src, expected",
        [
            ("lang/abc.csv", "lang", "abc"),
            ("abc.csv", ".", "abc"),
            ("a/b/c/d/e/abc.csv", "a", "b.c.d.e.abc"),
            ("a/b/c/d/e/abc.csv", "a/b/c", "d.e.abc"),
            ("lang/a.dotted.filename.csv", "lang", "a.dotted.filename"),
        ],
    )
    def test(self, path, src, expected):
        assert utils.relative_path_to(Path(path), Path(src)) == expected
