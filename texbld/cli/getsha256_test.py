
from argparse import ArgumentTypeError
import pytest
from texbld.cli.getsha256 import getsha256


def test_works():
    resource = "github:octocat/Hello-World#553c2077f0edc3d5dc5d17262f6aa498e69d6f8e"
    sha256 = "cc82fedd92d6fd783c9c6f984e4a67daa6c03f783e47016ba3610691b542df92"
    assert getsha256(resource) == sha256


def test_nongithub_fails():
    resource = "local:hello"
    with pytest.raises(ArgumentTypeError):
        getsha256(resource)
