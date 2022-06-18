import pytest
from texbld.common.image.image import DockerImage, GitHubImage, LocalImage
from texbld.common.exceptions import DependencyCycle
from texbld.common.solver import Solver


def test_success():
    # exists in the tests.
    s = Solver(LocalImage(name="test_dep1_2"))
    images = s.images()
    assert len(images) == 3
    assert images[0].__class__ == LocalImage
    assert images[1].__class__ == LocalImage
    assert images[2].__class__ == DockerImage


def test_depcycle():
    # test_dep2_1 -> test_dep2_2 -> test_dep2_3 -> test_dep2_1 (dependency cycle)
    with pytest.raises(DependencyCycle):
        s = Solver(LocalImage(name="test_dep2_1"))
    with pytest.raises(DependencyCycle):
        s = Solver(LocalImage(name="test_dep2_2"))
    with pytest.raises(DependencyCycle):
        s = Solver(LocalImage(name="test_dep2_3"))


def test_nodepcycle():
    # test_dep4_3 -> test_dep4_1 -> test_dep4_2 -> test_dep4_3 (at somethingelse.toml)
    s = Solver(LocalImage(name="test_dep4_3", config="image.toml"))


def test_github():
    s = Solver(
        GitHubImage(
            owner="texbld", repository="sample-image", revision="04f2b5a50d65eeb2b42f7329c7eea37d8c880c85",
            sha256="63a8827ae24969d0d829365f54fa4aa3e001a1f2f76b47fd96ac482894c35c00"))
    assert len(s.build_seq) == 2


def test_github_dependency():
    s = Solver(
        LocalImage(name="test_dep5"))
    assert len(s.build_seq) == 3
    assert s.build_seq[-2].__class__ == GitHubImage
    assert s.build_seq[-2].config == "markdown.toml"
    assert s.build_seq[-2].client.config == "markdown.toml"
    assert s.build_seq[-2].get_source().packages == ["pandoc"]


def test_notfound():
    with pytest.raises(FileNotFoundError):
        s = Solver(LocalImage(name="test_dep3"))
