from texbld.common.image import Image
from texbld.common.project import Project
import toml

from texbld.common.solver import Solver


def project_toml_gen(name: str, image: 'Image') -> str:
    solver = Solver(image)
    commands = {}
    for img in reversed(solver.images()):
        if img.is_base():
            continue
        img.copy_to_builds()
        commands |= img.get_source().project_commands
    project = Project(name=name, image=image, commands=commands)
    return toml.dumps(project.project_dict())
