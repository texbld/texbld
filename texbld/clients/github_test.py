import os
from texbld.clients.github import GitHubClient
from texbld.exceptions import GitHubNotFound, HashMismatch
import pytest


def test_github():
    gth = GitHubClient(owner="octocat", repository="Hello-World", revision="7fd1a60b01f91b314f59955a4e4d4e80d8edf11d",
                       sha256="39a4b97b9d108782fa7466b07160a2c9227a7da07725ad4110c41be6014e4160")
    gth.unpack()
    assert os.path.isfile(os.path.join(gth.decompressed_dir(), "README"))


def test_github_noconfirm():
    gth = GitHubClient(owner="octocat", repository="Hello-World",
                       revision="7fd1a60b01f91b314f59955a4e4d4e80d8edf11d", sha256=None)
    gth.unpack()
    assert os.path.isfile(os.path.join(gth.decompressed_dir(), "README"))


def test_github_fail():
    gth = GitHubClient(
        owner="octocat", repository="Hello-World", revision="553c2077f0edc3d5dc5d17262f6aa498e69d6f8e",
        sha256="cc82fedd92d6fd783c9c6f984e4a67daa6c03f783e47016ba3610691b542df91")  # last should be 2
    with pytest.raises(HashMismatch):
        gth.unpack()
        gth.confirmsha256()


def test_github_download_fail():
    gth = GitHubClient(
        owner="octocat", repository="Hello-World2", revision="553c2077f0edc3d5dc5d17262f6aa498e69d6f8e",
        sha256="cc82fedd92d6fd783c9c6f984e4a67daa6c03f783e47016ba3610691b542df92")
    with pytest.raises(GitHubNotFound):
        gth.confirmsha256()
