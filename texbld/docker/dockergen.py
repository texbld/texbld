import os
from texbld.common.directory import BUILD_CACHE_DIR
from texbld.common.exceptions import FsNotFound
from typing import TYPE_CHECKING
from jinja2 import Template

dockerfile_template = Template(open(os.path.join(os.path.dirname(__file__), "dockerfile_template.jinja")).read())

if TYPE_CHECKING:
    # dependency cycle otherwise
    from texbld.common.image.image import Image


def generate_dockerfile(image: 'Image') -> str:
    source, dr = image.get_source(), image.package_dir()
    for src, dest in source.files.items():
        src = os.path.join(dr, src)
        if not os.path.exists(src):
            raise FsNotFound(src)

    data = {
        'inherits': source.inherit.docker_image_name(),
        'update': source.update,
        'packages': source.packages,
        'install': source.install,
        'files': source.files,
        'setup': source.setup,
    }
    return dockerfile_template.render(**data)
