import os
from texbld.common.directory import BUILD_CACHE_DIR
from texbld.common.exceptions import FsNotFound
from texbld.common.image import Image
from texbld.common.image.image import GitHubImage, LocalImage
from texbld.common.solver import Solver
from jinja2 import Template

dockerfile_template = Template(open(os.path.join(os.path.dirname(__file__), "dockerfile_template.jinja")).read())


def generate_dockerfile(image: Image) -> str:
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


# for viewing purposes
def main():
    s = Solver(
        GitHubImage(
            owner="texbld", repository="sample-image", revision="04f2b5a50d65eeb2b42f7329c7eea37d8c880c85",
            sha256="63a8827ae24969d0d829365f54fa4aa3e001a1f2f76b47fd96ac482894c35c00"))
    print(generate_dockerfile(s.images()[0]))
