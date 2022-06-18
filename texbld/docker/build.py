from texbld.docker.client import dockerclient

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from texbld.common.image import Image
    from texbld.common.solver import Solver


def build_image(image: 'Image', cache=False):
    print(f"Copying {image.docker_image_name()}...")
    image.copy_to_builds(cache=cache)
    print(f"Building {image.docker_image_name()}...")
    dockerclient.images.build(path=image.build_dir(),
                              tag=image.docker_image_name(), quiet=False)


def build(solver: 'Solver', cache=False):
    # this step must be done SEQUENTIALLY!!!
    for image in reversed(solver.images()):
        # no need to build out a docker image from the registry.
        if image.is_base():
            image.pull()
            continue
        build_image(image, cache=cache)
