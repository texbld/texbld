import os
from texbld.common.image.image import LocalImage
from texbld.common.solver import Solver
from texbld.directory import BUILD_CACHE_DIR


def test_correct():
    x = Solver(LocalImage(name="test_gen1")).images()[0]
    x.copy_to_builds()
    dr = os.path.join(BUILD_CACHE_DIR, x.docker_image_name())
    assert os.path.isfile(os.path.join(
        dr, "directory", "directory2", "file.txt"))
    assert os.path.isfile(os.path.join(dr, "script.sh"))
    assert os.path.isfile(os.path.join(dr, "script2.sh"))
    assert not os.path.isfile(os.path.join(dr, "unnecessaryfile.txt"))
    assert not os.path.isfile(os.path.join(dr, "nonexistent.txt"))
