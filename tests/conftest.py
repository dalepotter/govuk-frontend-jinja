
pytest_plugins = ['helpers_namespace']

import pytest

from itertools import filterfalse
import re
from textwrap import dedent
from typing import Iterator, Union, TextIO

import jinja2
import govuk_frontend


@pytest.helpers.register
def IS_LINE_JUNK(line):
    return bool(re.match(r'^\s*$', line))

@pytest.helpers.register
def readlines(buf: Union[str, TextIO]) -> Iterator[str]:
    if isinstance(buf, str):
        return buf.splitlines(keepends=True)
    else:
        return buf.readlines()

@pytest.helpers.register
def normalise_whitespace(buf: Union[str, TextIO]) -> str:
    """Delete lines that are empty/contain only whitespace"""
    lines = filterfalse(IS_LINE_JUNK, readlines(buf))
    return dedent(''.join(lines)).strip()


@pytest.fixture
def loader():
    return jinja2.FileSystemLoader([
        "node_modules/govuk-frontend",
        "node_modules/govuk-frontend/components",
    ])


@pytest.fixture
def env(loader):
    return govuk_frontend.Environment(
        loader=loader,
    )
