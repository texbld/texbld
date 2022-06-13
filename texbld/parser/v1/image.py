import toml
import json
from jsonschema import Draft7Validator
from texbld.common.image import SourceImage, DockerImage, LocalImage, GitHubImage, Image
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
schema = json.load(open(os.path.join(current_dir, "image_schema.json")))
validator = Draft7Validator(schema=schema)

# helper method to determine what type of image is depended upon.


def to_inherit(config: 'dict') -> Image:
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
def to_source_image(source: str) -> SourceImage:
    config = toml.loads(source)
    if not validator.is_valid(config):
        raise next(validator.iter_errors(config))

    return SourceImage(
        name=config.get("name"),
        packages=config.get("packages", []),
        setup=config.get("setup", []),
        files=config.get("files", {}),
        install=config.get("install", "apk add"),
        update=config.get("update", "apk update"),
        inherit=to_inherit(config.get("inherit")),
        project_files=config.get("project", {}).get("files", {}),
        project_commands=config.get("project", {}).get("commands", {}),
    )
