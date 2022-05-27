from dataclasses import dataclass, field
import os
import hashlib
import shutil
from texbld.common.directory import PACKAGE_CACHE_DIR
from texbld.common.exceptions import FsNotFound


def files_list(path: str):
    if not os.path.isdir(path):
        raise FsNotFound(path)
    files = []
    for dirname, _, filenames in os.walk(path):
        for f in filenames:
            files.append(os.path.join(dirname, f))
    files.sort()
    return files

# walk through the entire tree and hash stuff.


def hash_dir(path: str):
    files = files_list(path)
    hsh = hashlib.sha256()
    for f in files:
        hsh.update(open(f, 'rb').read())
    return hsh.hexdigest()


@dataclass
class ImageFsBrowser:
    path: str
    name: str = field(init=False)
    config_hash: str = field(init=False)
    imagepath: str = field(init=False)

    def __post_init__(self):
        self.path = os.path.abspath(self.path)
        self.imagepath = os.path.join(self.path, "image.toml")
        self.name = os.path.basename(self.path)
        if not os.path.isfile(self.imagepath):
            raise FsNotFound(self.imagepath)
        self.config_hash = hash_dir(self.path)

    def read_config(self):
        try:
            with open(self.imagepath) as r:
                return r.read()
        except FileNotFoundError:
            return FsNotFound(self.imagepath)
