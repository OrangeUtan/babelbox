import os
import shutil
from pathlib import Path

from invoke import task

SRC_DIR = Path("babelbox")


@task
def install(c):
    """ Setup develoment environment. Install dependencies etc """

    os.system("poetry lock -n")
    os.system("poetry install -n")
    os.system("poetry run pre-commit install --hook-type pre-commit")
    os.system("poetry run pre-commit install --hook-type pre-push")
    os.system("poetry run pre-commit install --hook-type commit-msg")


@task
def format(c):
    os.system("poetry run black . --config pyproject.toml")
    os.system(
        f"poetry run isort {str(SRC_DIR)} --settings-path pyproject.toml --profile black"
    )
    os.system("poetry run isort tests --settings-path pyproject.toml --profile black")


@task
def test(c, verbose=False, s=False):
    """ Run all tests with coverage """

    flags = " ".join(["-vv" if verbose else "", "-s" if s else ""])
    if os.system(f"poetry run pytest --cov={str(SRC_DIR)} --cov-report=xml {flags}") == 0:
        os.system("poetry run coverage report")
        os.system("poetry run coverage-badge -o coverage.svg -f")
