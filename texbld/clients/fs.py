from dataclasses import dataclass, field
import os
import hashlib
import shutil
from texbld.directory import PACKAGE_CACHE_DIR


# sort everything in the directory so it's in a deterministic order.
def files_list(path: str):
    if not os.path.isdir(path):
        raise FileNotFoundError(path)
    files = []
    for dirname, _, filenames in os.walk(path):
        for f in filenames:
            files.append(os.path.join(dirname, f))
    files.sort()
    return files

# walk through the entire directory tree and hash files.


def hash_dir(path: str):
    files = files_list(path)
    hsh = hashlib.sha256()
    for f in files:
        hsh.update(open(f, 'rb').read())
    return hsh.hexdigest()


@dataclass
class ImageFsBrowser:
    path: str
    config: str = "image.toml"
    name: str = field(init=False)
    hashed: str = field(init=False)
    imagepath: str = field(init=False)

    def __post_init__(self):
        self.path = os.path.abspath(self.path)
        self.imagepath = os.path.join(self.path, *(self.config.split('/')))
        self.name = os.path.basename(self.path)
        if not os.path.isfile(self.imagepath):
            raise FileNotFoundError(self.imagepath)
        self.hashed = hash_dir(self.path)

    def read_config(self):
        try:
            with open(self.imagepath) as r:
                return r.read()
        except FileNotFoundError:
            return FileNotFoundError(self.imagepath)
