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
    os.system("poetry run pre-commit install")


@task
def format(c):
    """ Format all files  in project using black and isort"""

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


@task
def publish(c):
    """ Publish project from local """

    os.system("poetry build")
    os.system("poetry publish")


@task
def bump(c, version):
    """ Bump version and push tag to remote. Autmatically published project """

    os.system(f"poetry run tbump {version}")
