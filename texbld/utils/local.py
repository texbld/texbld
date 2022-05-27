from dataclasses import dataclass, field
import os
import shutil
from texbld.common.directory import LOCALPACKAGES_DIR, PACKAGE_CACHE_DIR
from texbld.utils.fs import ImageFsBrowser, files_list, hash_dir
from texbld.common.exceptions import FsNotFound


@dataclass
class LocalClient:
    # it's stuff from your local fs, so no sha256 needed.
    name: str
    browser: ImageFsBrowser = field(init=False)
    path: str = field(init=False)

    def __post_init__(self):
        # change this name to a random string.
        self.browser = ImageFsBrowser(path=os.path.join(LOCALPACKAGES_DIR, self.name))
        name = f"{self.name}-{self.browser.config_hash}"
        self.path = os.path.join(PACKAGE_CACHE_DIR, name)
        self.copy()
        pass

    def copy(self):
        # only do if there is a hash mismatch.
        if os.path.isdir(self.path) and hash_dir(self.path) != self.browser.config_hash:
            shutil.rmtree(self.path)
        if not os.path.exists(self.path):
            shutil.copytree(self.browser.path, self.path)

    def read_config(self):
        return self.browser.read_config()
