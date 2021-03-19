import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import click
import pytest

import babelbox
from babelbox import cli


class Test_version_callback:
    def test(self):
        with pytest.raises(click.exceptions.Exit):
            assert cli.version_callback(True) == f"Babelbox: {babelbox.__version__}"


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
