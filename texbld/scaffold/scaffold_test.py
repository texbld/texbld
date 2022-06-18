
import os
import shutil

import pytest
from texbld.common.directory import SCAFFOLD_TESTS
from texbld.common.image.image import LocalImage
from texbld.scaffold.scaffold import scaffold


def test_1():
    image = LocalImage(name="test_sc1_2")
    directory = os.path.join(SCAFFOLD_TESTS, "scaffold_1")
    if os.path.isdir(directory):
        shutil.rmtree(directory)
    scaffold(image, directory)


def test_2():
    image = LocalImage(name="test_sc1_2")
    directory = os.path.join(SCAFFOLD_TESTS, "scaffold_exists")
    os.makedirs(directory, exist_ok=True)
    with pytest.raises(FileExistsError):
        scaffold(image, directory)
