import re
from texbld.cli.resource import ImageResource


def test_github_regex():
    assert re.fullmatch(ImageResource.github_regex, "github:owner/repository#branch-0.1")
    assert re.fullmatch(ImageResource.github_regex, "github:owner/repository#branch")
    assert re.fullmatch(ImageResource.github_regex, "github:owner/repository#")
    assert re.fullmatch(ImageResource.github_regex, "github:owner/repository")


def test_github_regex_fail():
    assert not re.fullmatch(ImageResource.github_regex, "github: owner/repository")
    assert not re.fullmatch(ImageResource.github_regex, "github:owner/repo~sitory")
