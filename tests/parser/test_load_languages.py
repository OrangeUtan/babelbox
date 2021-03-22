import os

import pytest
from pytest_insta import SnapshotFixture

import babelbox


def test_no_prefix(snapshot: SnapshotFixture):
    assert snapshot("languages.json") == babelbox.load_languages(
        "tests/parser/examples/misc", False
    )


def test_prefix_filename(snapshot: SnapshotFixture):
    assert snapshot("languages.json") == babelbox.load_languages(
        "tests/parser/examples/misc", True
    )
