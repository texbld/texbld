from typing import TYPE_CHECKING
import texbld.logger as logger
import sys

if TYPE_CHECKING:
    from texbld.common.image import Image
    from texbld.common.solver import Solver


def build_image(image: 'Image', cache=False):
    from texbld.docker.client import dockerclient

    logger.progress(f"Copying {image.docker_image_name()}...")
    image.copy_to_builds(cache=cache)
    logger.done(f"Copied {image.docker_image_name()}")
    logger.progress(f"Building {image.docker_image_name()}...")
    generator = dockerclient.api.build(
        path=image.build_dir(), tag=image.docker_image_name(), decode=True)
    for line in generator:
        if x := line.get('stream'):
            sys.stdout.write(x)
    logger.done(f"Finished building {image.docker_image_name()}")


def build(solver: 'Solver', cache=False):
    # this step must be done SEQUENTIALLY!!!
    for image in reversed(solver.images()):
        # no need to build out a docker image from the registry.
        if image.is_base():
            image.pull()
            continue
        build_image(image, cache=cache)
