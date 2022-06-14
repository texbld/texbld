import pytest
from texbld.common.image.image import DockerImage, LocalImage, GitHubImage
from texbld.common.image.sourceimage import SourceImage
from texbld.common.solver import Solver
from texbld.common.exceptions import FsNotFound
from texbld.docker.dockergen import generate_dockerfile
import re


def almost_eq_str(s1: str, s2: str):
    regex = re.compile("\s*")
    l1, l2 = s1.splitlines(), s2.splitlines()
    l1 = filter(lambda s: not regex.fullmatch(s), l1)
    l2 = filter(lambda s: not regex.fullmatch(s), l2)
    l1 = list(map(lambda s: s.strip(), l1))
    l2 = list(map(lambda s: s.strip(), l2))
    return l1 == l2


def test_1():
    x = Solver(LocalImage(name="test_gen1")).images()[0]
    result = """FROM alpine
WORKDIR /texbld
RUN apk update
RUN apk add pandoc cowsay
COPY script.sh /s1.sh
COPY script2.sh /s2.sh
COPY directory/directory2/file.txt /usr/share/file.txt
RUN cowsay 'hello'
RUN cowsay 'world'"""
    assert almost_eq_str(generate_dockerfile(x), result)


def test_2():
    # has a nonexistent file in it.
    x = Solver(LocalImage(name="test_gen2")).images()[0]
    with pytest.raises(FsNotFound):
        generate_dockerfile(x)
