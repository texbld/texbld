from dataclasses import dataclass, field
import os
import shutil
from texbld.directory import LOCALPACKAGES_DIR, PACKAGE_CACHE_DIR
from texbld.clients.client import Client
import texbld.clients.fs as fs
from texbld.clients.fs import ImageFsBrowser


@dataclass
class LocalClient(Client):
    # it's stuff from your local fs, so no sha256 needed.
    name: str
    config: str = "image.toml"
    browser: ImageFsBrowser = None
    cache_path: str = field(init=False)

    def __post_init__(self):
        # change this name to a random string.
        self.browser = ImageFsBrowser(
            path=os.path.join(LOCALPACKAGES_DIR, self.name), config=self.config
        )
        self.cache_path = os.path.join(
            PACKAGE_CACHE_DIR, f"{self.name}-{self.browser.hashed}")
        self.unpack()

    def unpack(self):
        # only do if there is a hash mismatch.
        if os.path.isdir(self.cache_path) and fs.hash_dir(self.cache_path) != self.browser.hashed:
            shutil.rmtree(self.cache_path)
        if not os.path.exists(self.cache_path):
            shutil.copytree(self.browser.path, self.cache_path)

    def read_config(self):
        return self.browser.read_config()
