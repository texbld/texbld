import re
from texbld.cli.resource import ImageResource


def test_github_regex():
    assert re.fullmatch(
        ImageResource.github_regex, "github:owner/repository/branch-0.1#image.toml").groups() ==\
        ('owner', 'repository', '/branch-0.1', '#image.toml')
    assert re.fullmatch(ImageResource.github_regex,
                        "github:owner/repository/branch").groups() == ('owner', 'repository', '/branch', None)
    assert re.fullmatch(ImageResource.github_regex,
                        "github:owner/repository#world/hello.toml")
    assert re.fullmatch(ImageResource.github_regex, "github:owner/repository")
    assert re.fullmatch(ImageResource.github_regex, "github:owner/repository")


def test_github_regex_fail():
    assert not re.fullmatch(ImageResource.github_regex,
                            "github: owner/repository")
    assert not re.fullmatch(ImageResource.github_regex,
                            "github:owner/repo~sitory")


def test_local_regex():
    assert re.fullmatch(ImageResource.local_regex, "local:mypackage#name.toml").groups(
    ) == ('mypackage', '#name.toml')
    assert re.fullmatch(ImageResource.local_regex,
                        "local:mypackage").groups() == ('mypackage', None)
