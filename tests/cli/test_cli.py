from pathlib import Path
from unittest.mock import MagicMock, patch

import click
import pytest
from typer.testing import CliRunner

import babelbox
from babelbox import cli


@pytest.fixture
def runner():
    return CliRunner()


class Test_main:
    def test_no_args(self, runner: CliRunner):
        assert "Missing argument" in runner.invoke(cli.app).output

    def test_file_not_found(self, runner: CliRunner):
        result = runner.invoke(cli.app, "doesnt_exist")
        assert str(result.exception) == "2"
        assert "does not exist" in result.output

    @pytest.mark.parametrize(
        "src, expected, expected_prefixed",
        [
            (
                "tests/cli/test_dirs/multiple_csv",
                {
                    "a": {"x": "1", "y": "10", "s": "1", "t": "10"},
                    "b": {"x": "2", "y": "11", "s": "2", "t": "11"},
                    "c": {"x": "3", "y": "12", "s": "3", "t": "12"},
                },
                {
                    "a": {"a.x": "1", "a.y": "10", "b.s": "1", "b.t": "10"},
                    "b": {"a.x": "2", "a.y": "11", "b.s": "2", "b.t": "11"},
                    "c": {"a.x": "3", "a.y": "12", "b.s": "3", "b.t": "12"},
                },
            ),
            (
                "tests/cli/test_dirs/read_only_csv",
                {
                    "a": {"x": "1", "y": "10", "s": "1", "t": "10"},
                    "b": {"x": "2", "y": "11", "s": "2", "t": "11"},
                    "c": {"x": "3", "y": "12", "s": "3", "t": "12"},
                },
                {
                    "a": {"a.x": "1", "a.y": "10", "b.s": "1", "b.t": "10"},
                    "b": {"a.x": "2", "a.y": "11", "b.s": "2", "b.t": "11"},
                    "c": {"a.x": "3", "a.y": "12", "b.s": "3", "b.t": "12"},
                },
            ),
        ],
    )
    def test_dirs(self, src, expected, expected_prefixed, runner: CliRunner):
        with patch(
            "babelbox.cli.write_language_files", new=MagicMock()
        ) as mock_write_lang_files:
            runner.invoke(cli.app, src, catch_exceptions=False)
            runner.invoke(cli.app, [src, "-p"], catch_exceptions=False)

            assert mock_write_lang_files.call_count == 2

            # Not prefixed
            assert mock_write_lang_files.call_args_list[0][0][0] == Path(src)
            assert mock_write_lang_files.call_args_list[0][0][1] == expected

            # Prefixed
            assert mock_write_lang_files.call_args_list[1][0][0] == Path(src)
            assert mock_write_lang_files.call_args_list[1][0][1] == expected_prefixed

    def test_src_is_file(self, runner: CliRunner):
        with patch("babelbox.cli.write_language_files", new=MagicMock()) as mock_write:
            runner.invoke(cli.app, "tests/cli/test_dirs/tree/a.csv", catch_exceptions=False)

            assert mock_write.call_count == 1
            assert mock_write.call_args_list[0][0][0] == Path("tests/cli/test_dirs/tree")
            assert mock_write.call_args_list[0][0][1] == {
                "a": {"x": "1", "y": "10"},
                "b": {"x": "2", "y": "11"},
                "c": {"x": "3", "y": "12"},
            }

    def test_dry(self, runner: CliRunner):
        with patch("babelbox.cli.write_language_files", new=MagicMock()) as mock_write:
            with patch("pathlib.Path.mkdir", new=MagicMock()) as mock_mkdir:
                runner.invoke(
                    cli.app, ["tests/cli/test_dirs", "--dry"], catch_exceptions=False
                )

                mock_write.assert_not_called()
                mock_mkdir.assert_not_called()

    def test_multiple_sources(self, runner: CliRunner):
        with patch("babelbox.cli.write_language_files", new=MagicMock()) as mock_write:
            with patch("pathlib.Path.mkdir", new=MagicMock()) as mock_mkdir:
                args = [
                    "tests/cli/test_dirs/multiple_sources/a.csv",
                    "tests/cli/test_dirs/multiple_sources/sourcedir",
                    "-o",
                    "build",
                ]
                runner.invoke(cli.app, args, catch_exceptions=False)

                mock_mkdir.assert_called_once()

                assert mock_write.call_count == 1
                assert mock_write.call_args_list[0][0][0] == Path("build")
                assert mock_write.call_args_list[0][0][1] == {
                    "a": {"x": "1", "y": "10"},
                    "b": {"x": "1", "y": "10"},
                    "c": {"x": "1", "y": "10"},
                }

    def test_multiple_sources_no_out(self, runner: CliRunner):
        with patch("babelbox.cli.write_language_files", new=MagicMock()) as mock_write:
            with patch("pathlib.Path.mkdir", new=MagicMock()) as mock_mkdir:
                args = [
                    "tests/cli/test_dirs/multiple_sources/a.csv",
                    "tests/cli/test_dirs/multiple_sources/sourcedir",
                ]
                results = runner.invoke(cli.app, args, catch_exceptions=False)

                mock_mkdir.assert_not_called()
                mock_write.assert_not_called()

                assert results.exit_code == 1
                assert results.stdout == "Multiple sources but no output specified\n"


class Test_version_callback:
    def test(self):
        with pytest.raises(click.exceptions.Exit):
            assert cli.version_callback(True) == f"Babelbox: {babelbox.__version__}"
