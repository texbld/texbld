import toml
import json
from jsonschema import Draft7Validator
from texbld.common.image import DockerImage, LocalImage, GitHubImage, Image
from texbld.common.project import Project
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
schema = json.load(open(os.path.join(current_dir, "project_schema.json")))
validator = Draft7Validator(schema=schema)

# helper method to determine what type of image is depended upon.


def to_image(config: 'dict') -> Image:
    if 'docker' in config:
        return DockerImage(name=config['docker'])
    elif 'github' in config:
        g: dict = config['github']
        return GitHubImage(**g)
    elif 'local' in config:
        if type(config.get('local')) == str:
            return LocalImage(name=config['local'])
        else:
            return LocalImage(**config['local'])


# change this when the SourceImage spec changes over time.
def to_project(source: str) -> Project:
    config = toml.loads(source)
    if not validator.is_valid(config):
        raise next(validator.iter_errors(config))

    return Project(
        name=config.get("name"),
        image=to_image(config.get("image")),
        commands=config.get("commands")
    )
