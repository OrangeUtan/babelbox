import re
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest
from typer.testing import CliRunner

from babelbox import cli


@pytest.fixture
def runner():
    return CliRunner()


class Test_main:
    def test_no_args(self, runner: CliRunner):
        assert "Missing argument" in runner.invoke(cli.app).output

    def test(self, runner):
        with patch(
            "babelbox.cli.write_language_files", new=MagicMock()
        ) as mock_write_lang_files:
            runner.invoke(cli.app, "tests/cli/res", catch_exceptions=False)

            assert mock_write_lang_files.call_args_list[0][0][0] == Path("tests/cli/res")
            assert mock_write_lang_files.call_args_list[0][0][1] == {
                "a": {"x": "1", "y": "10", "s": "1", "t": "10"},
                "b": {"x": "2", "y": "11", "s": "2", "t": "11"},
                "c": {"x": "3", "y": "12", "s": "3", "t": "12"},
            }

    def test_file_not_found(self, runner: CliRunner):
        result = runner.invoke(cli.app, "doesnt_exist")
        assert str(result.exception) == "2"
        assert "does not exist" in result.output

    def test_prefix_filename(self, runner: CliRunner):
        with patch(
            "babelbox.cli.write_language_files", new=MagicMock()
        ) as mock_write_lang_files:
            runner.invoke(cli.app, "tests/cli/res -n", catch_exceptions=False)

            mock_write_lang_files.assert_called_once()
            assert mock_write_lang_files.call_args_list[0][0][0] == Path("tests/cli/res")
            assert mock_write_lang_files.call_args_list[0][0][1] == {
                "a": {"a.x": "1", "a.y": "10", "b.s": "1", "b.t": "10"},
                "b": {"a.x": "2", "a.y": "11", "b.s": "2", "b.t": "11"},
                "c": {"a.x": "3", "a.y": "12", "b.s": "3", "b.t": "12"},
            }
