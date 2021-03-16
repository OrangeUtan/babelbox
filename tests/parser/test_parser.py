import csv
import logging
import unittest.mock
from typing import Iterator, List, cast
from unittest.mock import patch

import pytest
from _pytest.logging import LogCaptureFixture

import babelbox
from babelbox.parser import ParserError


def row(variable: str, *columns: str):
    return (variable, *columns)


def mock_open(*args, **kwargs):
    m = unittest.mock.mock_open(*args, **kwargs)
    m.return_value.seek = m.side_effect  # Fix for seek(0)
    return m


class Test_create_locales_from_csv:
    @pytest.mark.parametrize(
        "locale_names, rows, expected_locales",
        [
            (
                ["en", "de"],
                [row("greet", "hello", "hallo")],
                {"en": {"greet": "hello"}, "de": {"greet": "hallo"}},
            )
        ],
    )
    def test(self, locale_names, rows, expected_locales):
        locales = babelbox.create_locales_from_csv(locale_names, rows)
        assert locales == expected_locales

    def test_missing_translation(self, caplog: LogCaptureFixture):
        locale_names = ["en", "de"]
        rows = [row("x", "a", "b"), row("y", "1", "")]

        with caplog.at_level(logging.WARNING):
            babelbox.create_locales_from_csv(locale_names, iter(rows))

        assert len(caplog.records) == 1
        assert caplog.record_tuples[0] == (
            "root",
            logging.WARNING,
            "Locale 'de' has no translation for 'y'",
        )

    def test_no_variable(self):
        locale_names = ["en", "de"]
        rows = [row("", "a", "b"), row("y", "1", "")]

        with pytest.raises(ParserError, match="Row 2: Variable cannot be empty"):
            babelbox.create_locales_from_csv(locale_names, iter(rows))


class Test_load_locales_from_csv:
    def test_works_on_real_file(self):
        expected_locales = {
            "b": {"x": "1", "y": "7"},
            "c": {"x": "2", "y": "8"},
            "d": {"x": "3", "y": "9"},
            "e": {"x": "4", "y": "10"},
            "f": {"x": "5", "y": "11"},
            "g": {"x": "6", "y": "12"},
        }
        locales = babelbox.load_locales_from_csv("tests/parser/res/test_seek.csv")
        assert locales == expected_locales

    @pytest.mark.parametrize(
        "csv_data, expected_locales",
        [
            (
                ("String,b,c,d,e\n" "x,2,3,4\n" "y,9,10,11\n"),
                {
                    "b": {"x": "2", "y": "9"},
                    "c": {"x": "3", "y": "10"},
                    "d": {"x": "4", "y": "11"},
                },
            )
        ],
    )
    def test_dialect_fallback(self, csv_data, expected_locales):
        with patch("io.open", mock_open(read_data=csv_data)):
            with pytest.warns(UserWarning, match="Couldn't determine csv dialect.*"):
                locales = babelbox.load_locales_from_csv("test.csv")
                assert locales == expected_locales

    def test_semicolon_delimited(self):
        csv_data = "String;a;b;c\n" "x;1;2;3\n" "y;10;11;12"
        expected_locales = {
            "a": {"x": "1", "y": "10"},
            "b": {"x": "2", "y": "11"},
            "c": {"x": "3", "y": "12"},
        }
        with patch("io.open", mock_open(read_data=csv_data)):
            locales = babelbox.load_locales_from_csv("test.csv")
            assert locales == expected_locales

    def test_pass_custom_dialect(self):
        class CustomDialect(csv.Dialect):
            delimiter = "|"
            quotechar = '"'
            doublequote = True
            skipinitialspace = False
            lineterminator = "\r\n"
            quoting = csv.QUOTE_MINIMAL

        csv_data = "String|a|b|c\n" "x|1|2|3\n" "y|10|11|12"
        expected_locales = {
            "a": {"x": "1", "y": "10"},
            "b": {"x": "2", "y": "11"},
            "c": {"x": "3", "y": "12"},
        }

        with patch("io.open", mock_open(read_data=csv_data)):
            locales = babelbox.load_locales_from_csv("test.csv", CustomDialect)
            assert locales == expected_locales

    def test_empty_file(self):
        with patch("io.open", mock_open(read_data="")):
            with pytest.warns(UserWarning, match="Couldn't determine csv dialect.*"):
                with pytest.raises(ParserError, match="Failed to read.*"):
                    babelbox.load_locales_from_csv("test.csv")

    def test_missing_translation(self, caplog: LogCaptureFixture):
        with caplog.at_level(logging.WARNING):
            babelbox.load_locales_from_csv("tests/parser/res/missing_translations.csv")

        assert len(caplog.records) == 2
        assert caplog.record_tuples[0] == (
            "root",
            logging.WARNING,
            "Locale 'en_us' has no translation for 'cat'",
        )
        assert caplog.record_tuples[1] == (
            "root",
            logging.WARNING,
            "Locale 'es' has no translation for 'spoon'",
        )
