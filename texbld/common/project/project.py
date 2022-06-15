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
    directory: str

    def build(self):
        build_dockerimage(Solver(self.image))

    def run(self, command_name: str):
        if command_name not in self.commands:
            raise CommandNotFound(command_name)
        dockerclient.containers.run(
            self.image.docker_image_name(),
            volumes={self.directory: {'bind': '/texbld', 'mode': 'rw'}},
            command=self.commands.get(command_name),
            remove=True)
