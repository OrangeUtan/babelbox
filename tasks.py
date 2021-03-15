import os
import shutil
from pathlib import Path

from invoke import task

SRC_DIR = Path("babelbox")


@task
def setup(c):
    os.system("poetry lock -n")
    os.system("poetry install -n")
    os.system("poetry run pre-commit install")


@task
def format(c):
    os.system("poetry run black . --config pyproject.toml")
    os.system(
        f"poetry run isort {str(SRC_DIR)} --settings-path pyproject.toml --profile black"
    )
    os.system("poetry run isort tests --settings-path pyproject.toml --profile black")


@task
def test(c, verbose=False, s=False):
    flags = " ".join(["-vv" if verbose else "", "-s" if s else ""])
    if os.system(f"poetry run pytest --cov={str(SRC_DIR)} --cov-report=xml {flags}") == 0:
        os.system("poetry run coverage report")
        os.system("poetry run coverage-badge -o coverage.svg -f")


@task
def publish(c):
    os.system("poetry build")
    os.system("poetry publish")
