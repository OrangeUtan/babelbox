import pytest
import toml

import babelbox


def test():
    pyproject = toml.load("pyproject.toml")
    project_version = pyproject["tool"]["poetry"]["version"]
    assert project_version == babelbox.__version__
