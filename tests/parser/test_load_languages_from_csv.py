import csv
import inspect
import logging
import unittest.mock
from pathlib import Path
from re import match
from typing import Type, cast
from unittest.mock import MagicMock, patch

import pytest
from _pytest.logging import LogCaptureFixture

import babelbox


def mock_open(*args, **kwargs):
    m = unittest.mock.mock_open(*args, **kwargs)
    m.return_value.seek = m.side_effect  # Fix for seek(0)
    return m


class MockDialect:
    def __init__(
        self,
        delimiter=",",
        quotechar='"',
        escapechar=None,
        doublequote=False,
        skipinitialspace=False,
        lineterminator="\r\n",
        quoting=csv.QUOTE_MINIMAL,
    ):
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.escapechar = escapechar
        self.doublequote = doublequote
        self.skipinitialspace = skipinitialspace
        self.lineterminator = lineterminator
        self.quoting = quoting

    def __eq__(self, o: object) -> bool:
        if o is not None and isinstance(o, type) and issubclass(o, csv.Dialect):
            assert self.delimiter == o.delimiter  # type: ignore
            assert self.quotechar == o.quotechar  # type: ignore
            assert self.escapechar == o.escapechar  # type: ignore
            assert self.doublequote == o.doublequote  # type: ignore
            assert self.skipinitialspace == o.skipinitialspace  # type: ignore
            assert self.lineterminator == o.lineterminator  # type: ignore
            assert self.quoting == o.quoting  # type: ignore
            return True
        return False


class Test_parsing:
    @pytest.mark.parametrize(
        "data, expected",
        [
            (
                """Ident;a;b;c
                x;1;2;3
                y;4;5;6""",
                {
                    "a": {"x": "1", "y": "4"},
                    "b": {"x": "2", "y": "5"},
                    "c": {"x": "3", "y": "6"},
                },
            )
        ],
    )
    def test(self, data, expected):
        with patch("builtins.open", mock_open(read_data=inspect.cleandoc(data))):
            assert babelbox.load_languages_from_csv("test.csv") == expected

    @pytest.mark.parametrize(
        "data, expected",
        [
            (
                """Ident;a;b

                x;1;2

                y;3;4""",
                {
                    "a": {"x": "1", "y": "3"},
                    "b": {"x": "2", "y": "4"},
                },
            )
        ],
    )
    def test_blank_lines(self, data, expected):
        with patch("builtins.open", mock_open(read_data=inspect.cleandoc(data))):
            assert babelbox.load_languages_from_csv("test.csv") == expected

    @pytest.mark.parametrize(
        "data, expected",
        [
            (
                """Ident;a;b
                x;ඣ;2
                y;3;ผ""",
                {
                    "a": {"x": "ඣ", "y": "3"},
                    "b": {"x": "2", "y": "ผ"},
                },
            )
        ],
    )
    def test_encoding(self, data, expected):
        with patch("builtins.open", mock_open(read_data=inspect.cleandoc(data))):
            assert babelbox.load_languages_from_csv("test.csv") == expected

    @pytest.mark.parametrize(
        "data, expected",
        [
            (
                """;a;b;c
                x;1;2;3
                y;4;5;6""",
                {
                    "a": {"x": "1", "y": "4"},
                    "b": {"x": "2", "y": "5"},
                    "c": {"x": "3", "y": "6"},
                },
            )
        ],
    )
    def test_no_key(self, data, expected):
        with patch("builtins.open", mock_open(read_data=inspect.cleandoc(data))):
            assert babelbox.load_languages_from_csv("test.csv") == expected

    @pytest.mark.parametrize(
        "data, expected",
        [
            (
                """,a,b
                x,1,2
                y,3""",
                {"a": {"x": "1", "y": "3"}, "b": {"x": "2", "y": ""}},
            )
        ],
    )
    def test_missing_translation(self, data, expected, caplog: LogCaptureFixture):
        with caplog.at_level(logging.WARNING):
            with patch("builtins.open", mock_open(read_data=inspect.cleandoc(data))):
                assert babelbox.load_languages_from_csv("test.csv") == expected

            assert len(caplog.records) == 1
            assert caplog.record_tuples[0][0] == "babelbox.parser"
            assert caplog.record_tuples[0][1] == logging.WARNING
            assert match(
                "'test.csv': Locale '.' has no translation for '.'", caplog.record_tuples[0][2]
            )

    def test_empty_file(self):
        with patch("builtins.open", mock_open(read_data="")):
            assert babelbox.load_languages_from_csv("test.csv") == {}

    @pytest.mark.parametrize(
        "data, expected",
        [
            (
                """Ident,a,b
                x,1,2
                ,3,4""",
                {"a": {"x": "1"}, "b": {"x": "2"}},
            ),
            (
                """Ident,a,b
                x,1,2
                ,3,""",
                {"a": {"x": "1"}, "b": {"x": "2"}},
            ),
        ],
    )
    def test_no_empty_line_without_identifier(self, data, expected, caplog: LogCaptureFixture):
        with caplog.at_level(logging.WARNING):
            with patch("builtins.open", mock_open(read_data=inspect.cleandoc(data))):
                languages = babelbox.load_languages_from_csv("test.csv")
                assert languages == expected

            assert len(caplog.records) == 1
            assert caplog.record_tuples[0][0] == "babelbox.parser"
            assert caplog.record_tuples[0][1] == logging.WARNING
            assert match(
                "'test.csv'@3: Non-empty line is missing identifier",
                caplog.record_tuples[0][2],
            )

    def test_empty_line_without_identifier(self, caplog: LogCaptureFixture):
        data = """Ident,a,b
                x,1,2
                ,,"""
        with patch("builtins.open", mock_open(read_data=inspect.cleandoc(data))):
            languages = babelbox.load_languages_from_csv("test.csv")
            assert languages == {"a": {"x": "1"}, "b": {"x": "2"}}

            assert len(caplog.records) == 0

    def test_comments(self):
        data = """Ident,a,b
                # A Comment
                x,1,2
                # 1
                # 2
                # 3
                ,,"""
        with patch("builtins.open", mock_open(read_data=inspect.cleandoc(data))):
            languages = babelbox.load_languages_from_csv("test.csv")
            assert languages == {"a": {"x": "1"}, "b": {"x": "2"}}

    def test_comment_with_nonempty_columns(self):
        data = """Ident,a,b
                # A Comment, nonempty
                x,1,2
                ,,"""
        with patch("builtins.open", mock_open(read_data=inspect.cleandoc(data))):
            languages = babelbox.load_languages_from_csv("test.csv")
            assert languages == {
                "a": {"x": "1", "# A Comment": " nonempty"},
                "b": {"x": "2", "# A Comment": ""},
            }


class Test_prefix:
    def test(self):
        data = """Ident,a,b
                x,1,2
                y,3,4"""

        expected = {"a": {"w.x": "1", "w.y": "3"}, "b": {"w.x": "2", "w.y": "4"}}

        with patch("builtins.open", mock_open(read_data=inspect.cleandoc(data))):
            languages = babelbox.load_languages_from_csv("test.csv", prefix="w.")
            assert languages == expected


class Test_dialect:
    @pytest.mark.parametrize(
        "data, expected_dialect",
        [
            (
                """;a;b
                x;1;2
                y;3;4""",
                MockDialect(";"),
            ),
            (
                """,a,b
                x,1,2
                y,3,4""",
                MockDialect(","),
            ),
            (
                """.a.b
                x.1.2
                y.3.4""",
                MockDialect("."),
            ),
        ],
    )
    def test_sniff_dialect(self, data, expected_dialect):
        with patch("builtins.open", mock_open(read_data=inspect.cleandoc(data))):
            with patch("csv.DictReader.__init__", new=MagicMock()) as mock_reader:
                mock_reader.return_value = None

                with pytest.raises(AttributeError):
                    babelbox.load_languages_from_csv("test.csv")

                mock_reader.assert_called_once()
                dialect = cast(Type[csv.Dialect], mock_reader.call_args_list[0][1]["dialect"])
                assert expected_dialect == dialect

    def test_sniffing_fails(self, caplog: LogCaptureFixture):
        data = """,a,b
                x,1,2
                y,3,4"""

        def fail():
            yield
            raise Exception()

        with patch("builtins.open", mock_open(read_data=inspect.cleandoc(data))):
            with patch("csv.Sniffer.sniff", new_callable=fail):
                languages = babelbox.load_languages_from_csv("test.csv")
                assert languages == {"a": {"x": "1", "y": "3"}, "b": {"x": "2", "y": "4"}}

    @pytest.mark.parametrize(
        "data, delimiter, expected",
        [
            (
                """|a|b
                x|1|2
                y|3|4""",
                "|",
                {"a": {"x": "1", "y": "3"}, "b": {"x": "2", "y": "4"}},
            ),
            (
                """🙏a🙏b
                x🙏1🙏2
                y🙏3🙏4""",
                "🙏",
                {"a": {"x": "1", "y": "3"}, "b": {"x": "2", "y": "4"}},
            ),
        ],
    )
    def test_overwrite_delimiter(self, data, delimiter, expected):
        with patch("builtins.open", mock_open(read_data=inspect.cleandoc(data))):
            languages = babelbox.load_languages_from_csv(
                "test.csv", dialect_overwrites={"delimiter": delimiter}
            )
            assert languages == expected


class Test_load_file:
    def test_pathlib_path(self):
        languages = babelbox.load_languages_from_csv(Path("tests/parser/res/a.csv"))
        assert languages == {"a": {"x": "1", "y": "3"}, "b": {"x": "2", "y": "4"}}

    def test_string_path(self):
        languages = babelbox.load_languages_from_csv("tests/parser/res/a.csv")
        assert languages == {"a": {"x": "1", "y": "3"}, "b": {"x": "2", "y": "4"}}

    def test_unicode(self):
        languages = babelbox.load_languages_from_csv("tests/parser/res/unicode.csv")
        assert languages == {"a": {"k": "ඣ", "l": "3"}, "b": {"k": "2", "l": "ผ"}}

    def test_missing_translation(self, caplog: LogCaptureFixture):
        with caplog.at_level(logging.WARNING):
            languages = babelbox.load_languages_from_csv(
                "tests/parser/res/missing_translations.csv"
            )
            assert languages == {
                "en_us": {"cat": "Cat", "spoon": ""},
                "de_de": {"cat": "", "spoon": "Löffel"},
            }

            assert len(caplog.records) == 2
            for name, level, msg in caplog.record_tuples:
                assert name == "babelbox.parser"
                assert level == logging.WARNING
                assert match(
                    "'tests/parser/res/missing_translations.csv': Locale '.*' has no translation for '.*'",
                    msg,
                )
