from texbld.common.exceptions import NoSuchImageVersion, NoVersionSpecified
from texbld.common.image.parse import parse_source_image
import pytest


def test_minimal_works():
    source = """
name = "myimage"
version = "1"

# inheritance patterns (all of them are mutually exclusive)
[inherit]
docker = "alpine"
    """
    parse_source_image(source)


def test_minimal_noversion():
    source = """
name = "myimage"

# inheritance patterns (all of them are mutually exclusive)
[inherit]
docker = "alpine"
    """
    with pytest.raises(NoVersionSpecified):
        parse_source_image(source)


def test_minimal_badversion():
    source = """
name = "myimage"
version = "gibberish"

# inheritance patterns (all of them are mutually exclusive)
[inherit]
docker = "alpine"
    """
    with pytest.raises(NoSuchImageVersion):
        parse_source_image(source)
