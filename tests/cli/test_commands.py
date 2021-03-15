import re
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest
from typer.testing import CliRunner

from babelbox import __main__ as cli


@pytest.fixture
def runner():
    return CliRunner()


class Test_main:
    def test(self, runner):
        expected_call_args_list = [
            call(
                Path("tests/cli/res"),
                "a",
                {"x": "1", "y": "10", "s": "1", "t": "10", "ä": "1", "ö": "10"},
                None,
            ),
            call(
                Path("tests/cli/res"),
                "b",
                {"x": "2", "y": "11", "s": "2", "t": "11", "ä": "2", "ö": "11"},
                None,
            ),
            call(
                Path("tests/cli/res"),
                "c",
                {"x": "3", "y": "12", "s": "3", "t": "12", "ä": "3", "ö": "12"},
                None,
            ),
        ]

        with patch("babelbox.__main__.write_locale", new=MagicMock()) as mock_write_locale:
            runner.invoke(cli.app, "tests/cli/res")

            assert mock_write_locale.call_count == 3
            assert mock_write_locale.call_args_list == expected_call_args_list

    def test_file_not_found(self, runner: CliRunner):
        result = runner.invoke(cli.app, "doesnt_exist")
        assert str(result.exception) == "2"
        assert "does not exist" in result.output

    def test_prepend_filename(self, runner: CliRunner):
        expected_call_args_list = [
            call(
                Path("tests/cli/res"),
                "a",
                {"a.x": "1", "a.y": "10", "b.s": "1", "b.t": "10", "c.ä": "1", "c.ö": "10"},
                None,
            ),
            call(
                Path("tests/cli/res"),
                "b",
                {"a.x": "2", "a.y": "11", "b.s": "2", "b.t": "11", "c.ä": "2", "c.ö": "11"},
                None,
            ),
            call(
                Path("tests/cli/res"),
                "c",
                {"a.x": "3", "a.y": "12", "b.s": "3", "b.t": "12", "c.ä": "3", "c.ö": "12"},
                None,
            ),
        ]

        with patch("babelbox.__main__.write_locale", new=MagicMock()) as mock_write_locale:
            runner.invoke(cli.app, "tests/cli/res -n")

            assert mock_write_locale.call_count == 3
            assert mock_write_locale.call_args_list == expected_call_args_list
