from texbld.utils.fs import ImageFsBrowser
from texbld.utils.local import LocalClient
from texbld.common.directory import LOCALPACKAGES_DIR
import pytest
import os
from texbld.common.exceptions import *


def test_fs_1():
    l = LocalClient(name="test_fs_1")
    assert os.path.exists(os.path.join(l.cache_path, "image.toml"))
    assert os.path.exists(os.path.join(l.cache_path, "hello.txt"))


def test_fs_2():
    l = LocalClient(name="test_fs_2")
    open(os.path.join(l.cache_path, "hello.txt"), 'w').write('hello world!')
    new = LocalClient(name="test_fs_2")
    assert os.path.exists(os.path.join(l.cache_path, "image.toml"))
    assert not os.path.exists(os.path.join(l.cache_path, "hello.txt"))


def test_fs_nonexistent():
    with pytest.raises(FileNotFoundError):
        l = LocalClient(name="test_fs_nonexistent")


def test_fs_no_imagetoml():
    with pytest.raises(FileNotFoundError):
        l = LocalClient(name="test_fs_no_imagetoml")
