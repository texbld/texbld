from dataclasses import dataclass, field
import hashlib
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from texbld.common.image import Image


@dataclass(order=True)
class SourceImage:
    inherit: 'Image'
    name: str
    packages: 'list[str]'
    setup: 'list[str]'
    files: 'dict[str,str]'
    project_files: 'dict[str, str]'
    project_commands: 'dict[str, str]'
    install: str
    update: str

    def image_hash(self):
        d = self.__dict__.copy()
        # DO NOT TRY TO GET THIS HASH!!! YOU WON'T DETECT DEPENDENCY CYCLES!
        d['inherit'] = None
        return hashlib.sha256(
            bytes(json.dumps(d), 'utf-8')
        ).hexdigest()
