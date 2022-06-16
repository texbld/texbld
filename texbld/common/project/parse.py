from texbld.common.exceptions import NoSuchImageVersion, NoVersionSpecified
from .project import Project
import toml


def parse_project(source: str) -> 'Project':
    tomlobj = toml.loads(source)
    if not "version" in tomlobj:
        raise NoVersionSpecified
    if tomlobj["version"] == "1":
        import texbld.parser.v1.project as v1
        return v1.to_project(source)
    # add later versions.
    else:
        raise NoSuchImageVersion(tomlobj["version"])
