from dataclasses import dataclass, field
from texbld.common.exceptions import CommandNotFound
from texbld.common.image import Image
from texbld.common.solver import Solver
from texbld.docker.build import build as build_dockerimage
from texbld.docker.client import dockerclient


@dataclass
class Project:
    title: str
    version: str
    image: Image
    commands: 'dict[str, str]'
    # should be absolute path
    directory: str = ""

    def build(self):
        build_dockerimage(Solver(self.image))

    def run(self, command_name: str):
        if command_name not in self.commands:
            raise CommandNotFound(command_name)
        container = dockerclient.containers.create(self.image.docker_image_name(),
                                                   volumes={self.directory: {'bind': '/texbld', 'mode': 'rw'}},
                                                   remove=True)
        container.exec_run(
            command=["sh", "-c", self.commands.get(command_name)],
        )
