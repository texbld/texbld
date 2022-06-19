import os
from texbld.directory import BUILD_CACHE_DIR
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # dependency cycle otherwise
    from texbld.common.image.image import Image


def generate_dockerfile(image: 'Image') -> str:
    source, dr = image.get_source(), image.package_dir()
    for src, _ in source.files.items():
        src = os.path.join(dr, *src.split('/'))
        if not os.path.exists(src):
            raise FileNotFoundError(src)

    data = {
        'inherits': source.inherit.docker_image_name(),
        'update': source.update,
        'packages': source.packages,
        'install': source.install,
        'files': source.files,
        'setup': source.setup,
    }
    return render(data)


def render(d: 'dict') -> 'str':
    strings = [f'FROM {d["inherits"]}', 'WORKDIR /texbld']
    if len(d.get('packages', [])):
        strings.append(f'RUN {d["update"]}')
        strings.append(f'RUN {d["install"]} {" ".join(d["packages"])}')
    for source, target in d['files'].items():
        strings.append(f'COPY {source} {target}')
    for command in d['setup']:
        strings.append(f'RUN {command}')
    return "\n".join(strings)
