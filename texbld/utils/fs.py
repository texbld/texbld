from dataclasses import dataclass, field
import os
import hashlib
import shutil
from texbld.common.directory import PACKAGE_CACHE_DIR
from texbld.common.exceptions import FsNotFound


# walk through the entire tree and hash stuff.
def hash_dir(path: str):
    if not os.path.isdir(path):
        raise FsNotFound(path)
    hsh = hashlib.sha256()
    for dirname, _, filenames in os.walk(path):
        for f in filenames:
            hsh.update(bytes(f, 'utf-8'))
            hsh.update(open(os.path.join(dirname, f), 'rb').read())
    return hsh.hexdigest()


@dataclass
class ImageFsBrowser:
    path: str
    name: str = field(init=False)
    config_hash: str = field(init=False)

    def __post_init__(self):
        self.path = os.path.abspath(self.path)
        self.name = os.path.basename(self.path)
        if not os.path.isfile(os.path.join(self.path, "image.toml")):
            raise FsNotFound(os.path.join(self.path, "image.toml"))
        self.config_hash = hash_dir(self.path)

    def read_image(self):
        return open(os.path.join(self.path, "image.toml")).read()
