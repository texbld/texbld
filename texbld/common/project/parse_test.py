from texbld.common.exceptions import NoSuchImageVersion, NoVersionSpecified
from texbld.common.project.parse import parse_project
import pytest


def test_minimal_works():
    source = """
name = "myproject"
version = "1"

# inheritance patterns (all of them are mutually exclusive)
[image]
docker = "alpine"

[commands]
run = "echo 'hello world'"
    """
    parse_project(source)


def test_minimal_noversion():
    source = """
name = "myimage"

# inheritance patterns (all of them are mutually exclusive)
[image]
docker = "alpine"
    """
    with pytest.raises(NoVersionSpecified):
        parse_project(source)


def test_minimal_badversion():
    source = """
name = "myimage"
version = "gibberish"

# inheritance patterns (all of them are mutually exclusive)
[image]
docker = "alpine"
    """
    with pytest.raises(NoSuchImageVersion):
        parse_project(source)
