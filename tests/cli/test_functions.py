import unittest
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import click
import pytest
from typer.testing import CliRunner

import babelbox
from babelbox import __main__ as cli


class Test_version_callback:
    def test(self):
        with pytest.raises(click.exceptions.Exit):
            assert cli.version_callback(True) == f"Babelbox: {babelbox.__version__}"


class Test_get_csv_files_in_dir:
    def test(self):
        expected_files = [
            Path("tests/cli/res/a.csv"),
            Path("tests/cli/res/b.csv"),
            Path("tests/cli/res/subfolder/c.csv"),
        ]
        files = list(cli.get_csv_files_in_dir(Path("tests/cli/res")))
        assert len(files) == len(expected_files)
        assert set(files) == set(expected_files)


class Test_combine_locales_from_files:
    def test(self):
        expected_locales = {
            "a": {"x": "1", "y": "10", "s": "1", "t": "10", "ä": "1", "ö": "10"},
            "b": {"x": "2", "y": "11", "s": "2", "t": "11", "ä": "2", "ö": "11"},
            "c": {"x": "3", "y": "12", "s": "3", "t": "12", "ä": "3", "ö": "12"},
        }

        csv_files = [
            Path("tests/cli/res/a.csv"),
            Path("tests/cli/res/b.csv"),
            Path("tests/cli/res/subfolder/c.csv"),
        ]
        locales = cli.combine_locales_from_files(csv_files)

        assert locales == expected_locales


class Test_create_locale:
    def test(self):
        expected_locale_path = Path("tests/cli/res/en.json")
        expected_data = {"x": "1", "y": "2"}

        src_dir = Path("tests/cli/res")
        locale = "en"
        entries = {"x": "1", "y": "2"}
        with patch("io.open", new=MagicMock()) as mockfile:
            with patch("json.dump", new=MagicMock()) as mockdump:
                cli.write_locale(src_dir, locale, entries)

                mockfile.assert_called_once()
                assert mockfile.call_args[0][0] == expected_locale_path

                mockdump.assert_called_once()
                assert mockdump.call_args[0][0] == expected_data
