from texbld.common.exceptions import NoSuchImageVersion, NoVersionSpecified
import toml
from typing import TYPE_CHECKING

from texbld.common.image.sourceimage import SourceImage


def parse_source_image(source: str) -> 'SourceImage':
    tomlobj = toml.loads(source)
    if not "version" in tomlobj:
        raise NoVersionSpecified
    if tomlobj["version"] == "1":
        import texbld.parser.v1.image as v1
        return v1.to_source_image(source)
    # add later versions.
    else:
        raise NoSuchImageVersion(tomlobj["version"])
