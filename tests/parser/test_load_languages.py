import pytest

import babelbox


def test():
    languages = babelbox.load_languages("tests/parser/res")
    assert languages == {
        "a": {"k": "ඣ", "l": "3", "x": "1", "y": "3"},
        "b": {"k": "2", "l": "ผ", "x": "2", "y": "4"},
        "en_us": {"cat": "Cat", "spoon": ""},
        "de_de": {"cat": "", "spoon": "Löffel"},
    }


def test_prefix_filename():
    languages = babelbox.load_languages("tests/parser/res", True)
    assert languages == {
        "a": {"a.x": "1", "a.y": "3", "unicode.k": "ඣ", "unicode.l": "3"},
        "b": {"a.x": "2", "a.y": "4", "unicode.k": "2", "unicode.l": "ผ"},
        "en_us": {"missing_translations.cat": "Cat", "missing_translations.spoon": ""},
        "de_de": {"missing_translations.cat": "", "missing_translations.spoon": "Löffel"},
    }
