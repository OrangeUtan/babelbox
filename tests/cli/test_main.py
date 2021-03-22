import logging
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pytest_insta import SnapshotFixture
from typer.testing import CliRunner

from babelbox import cli


@pytest.fixture
def runner():
    return CliRunner()


class Test_sources_arg:
    def test_no_source(self, runner: CliRunner):
        """ No source passed. E.g. `babelbox`"""

        assert "Missing argument" in runner.invoke(cli.app).output

    def test_src_does_not_exist(self, runner: CliRunner):
        """ Passed source does not exist. E.g. `babelbox /unicorn/`"""

        result = runner.invoke(cli.app, "doesnt_exist")
        assert str(result.exception) == "2"
        assert "does not exist" in result.output

    @pytest.mark.parametrize("directory", ["ignore_non_csv", "multiple_csv", "tree"])
    def test_dir(self, directory, snapshot: SnapshotFixture, runner: CliRunner):
        """ Source arg is a directory. E.g. `babelbox ./dir/` """

        with patch(
            "babelbox.cli.write_language_files", new=MagicMock()
        ) as mock_write_lang_files:
            # No args
            runner.invoke(cli.app, "tests/cli/examples/" + directory, catch_exceptions=False)
            assert mock_write_lang_files.call_count == 1
            assert (
                snapshot("dest.txt")
                == Path(mock_write_lang_files.call_args_list[0][0][0]).as_posix()
            )
            assert snapshot("no_args.json") == mock_write_lang_files.call_args_list[0][0][1]

            mock_write_lang_files.reset_mock()

            # Prefixed
            runner.invoke(
                cli.app, ["tests/cli/examples/" + directory, "-p"], catch_exceptions=False
            )
            assert mock_write_lang_files.call_count == 1
            assert (
                snapshot("dest.txt")
                == Path(mock_write_lang_files.call_args_list[0][0][0]).as_posix()
            )
            assert snapshot("prefixed.json") == mock_write_lang_files.call_args_list[0][0][1]

    def test_file(self, runner: CliRunner):
        """ Source arg is a file. E.g. `babelbox test.csv` """

        with patch("babelbox.cli.write_language_files", new=MagicMock()) as mock_write:
            runner.invoke(
                cli.app, "tests/cli/examples/multiple_csv/a.csv", catch_exceptions=False
            )

            assert mock_write.call_count == 1
            assert mock_write.call_args_list[0][0][0] == Path(
                "tests/cli/examples/multiple_csv"
            )
            assert mock_write.call_args_list[0][0][1] == {
                "a": {"x": "1", "y": "10"},
                "b": {"x": "2", "y": "11"},
                "c": {"x": "3", "y": "12"},
            }

    def test_multiple(self, snapshot: SnapshotFixture, runner: CliRunner):
        """ Multiple sources. E.g. `babelbox file.csv dir/ -o <dir>` """

        with patch("babelbox.cli.write_language_files", new=MagicMock()) as mock_write:
            with patch("pathlib.Path.mkdir", new=MagicMock()) as mock_mkdir:
                args = [
                    "tests/cli/examples/tree/a.csv",
                    "tests/cli/examples/tree/node",
                    "-o",
                    "build",
                ]
                runner.invoke(cli.app, args, catch_exceptions=False)

                mock_mkdir.assert_called_once()

                assert mock_write.call_count == 1
                assert mock_write.call_args_list[0][0][0] == Path("build")
                assert snapshot("languages.json") == mock_write.call_args_list[0][0][1]

    def test_multiple_without_out(self, runner: CliRunner):
        """ Multiple sources but no --out option. E.g. E.g. `babelbox file.csv dir/` """

        with patch("babelbox.cli.write_language_files", new=MagicMock()) as mock_write:
            with patch("pathlib.Path.mkdir", new=MagicMock()) as mock_mkdir:
                args = [
                    "tests/cli/examples/tree/a.csv",
                    "tests/cli/examples/tree/node",
                ]
                results = runner.invoke(cli.app, args, catch_exceptions=False)

                mock_mkdir.assert_not_called()
                mock_write.assert_not_called()

                assert results.exit_code == 1
                assert results.stdout == "Multiple sources but no output specified\n"


def test_option_dry(runner: CliRunner):
    with patch("babelbox.cli.write_language_files", new=MagicMock()) as mock_write:
        with patch("pathlib.Path.mkdir", new=MagicMock()) as mock_mkdir:
            runner.invoke(cli.app, ["tests/cli/examples", "--dry"], catch_exceptions=False)

            mock_write.assert_not_called()
            mock_mkdir.assert_not_called()


class Test_csv_dialect_options:
    def test_pass_overwrites_to_load(self, runner: CliRunner):
        """ Check if the csv overwrites are passed to `babelbox.parser.load_languages_from_csv`"""

        with patch("babelbox.parser.load_languages_from_csv") as mock_load_csv:
            runner.invoke(
                cli.app,
                [
                    "tests/cli/examples/multiple_csv/a.csv",
                    "--dry",
                    "-d",
                    "|",
                ],
                catch_exceptions=False,
            )

            mock_load_csv.assert_called_once()
            assert mock_load_csv.call_args_list[0][0][2] == {"delimiter": "|"}

    def test_delimiter(self, runner: CliRunner):
        with patch("babelbox.cli.write_language_files", new=MagicMock()) as mock_write:
            runner.invoke(
                cli.app,
                ["tests/cli/examples/custom_dialects/pipe.csv", "-d", "|"],
                catch_exceptions=False,
            )

            assert mock_write.call_count == 1
            assert mock_write.call_args_list[0][0][1] == {
                "a": {"x": "1", "y": "3"},
                "b": {"x": "2", "y": "4"},
            }


class Test_logging:
    def test_default_loglevel(self, runner: CliRunner):
        with patch("logging.basicConfig") as mock_logconfig:
            runner.invoke(
                cli.app, ["tests/cli/examples/multiple_csv", "--dry"], catch_exceptions=False
            )

            mock_logconfig.assert_called_once()
            assert mock_logconfig.call_args_list[0][1]["level"] == logging.WARNING

    def test_quiet(self, runner: CliRunner):
        with patch("logging.basicConfig") as mock_logconfig:
            runner.invoke(
                cli.app,
                ["tests/cli/examples/multiple_csv", "--quiet", "--dry"],
                catch_exceptions=False,
            )

            mock_logconfig.assert_called_once()
            assert mock_logconfig.call_args_list[0][1]["level"] == logging.ERROR

    def test_verbose(self, runner: CliRunner):
        with patch("logging.basicConfig") as mock_logconfig:
            runner.invoke(
                cli.app,
                ["tests/cli/examples/multiple_csv", "--verbose", "--dry"],
                catch_exceptions=False,
            )

            mock_logconfig.assert_called_once()
            assert mock_logconfig.call_args_list[0][1]["level"] == logging.INFO
