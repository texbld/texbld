from texbld.directory import PACKAGE_CACHE_DIR, TARBALL_CACHE_DIR
from texbld.common.exceptions import GitHubNotFound, HashMismatch
from dataclasses import dataclass, field
import urllib3
import shutil
import os
import hashlib
import tarfile
from texbld.clients.client import Client

from texbld.clients.fs import ImageFsBrowser

http = urllib3.PoolManager()


@dataclass
class GitHubClient(Client):
    owner: str
    repository: str
    revision: str
    sha256: str = None
    config: str = "image.toml"
    # there are times when we want to test file-fetching in git.
    browser: ImageFsBrowser = None
    noconfirm: bool = field(init=False)

    def __post_init__(self):
        self.noconfirm = (self.sha256 is None)

    def tarball_path(self) -> str:
        return os.path.join(TARBALL_CACHE_DIR, f"{self.owner}-{self.repository}-{self.revision}.tar.gz")

    def decompressed_dir(self) -> str:
        return os.path.join(PACKAGE_CACHE_DIR, f"{self.owner}-{self.repository}-{self.revision}")

    # fetches a tarball and returns a boolean as to whether it actually happened.
    def fetch(self) -> bool:
        # fetch only if our tarball doesn't exist.
        if not os.path.exists(self.tarball_path()) or self.getsha256() != self.sha256 or self.noconfirm:
            url = f"https://github.com/{self.owner}/{self.repository}/archive/{self.revision}.tar.gz"
            with http.request('GET', url, preload_content=False) as res:
                if res.status == 404:
                    raise GitHubNotFound(url)
                with open(self.tarball_path(), 'wb') as w:
                    shutil.copyfileobj(res, w)
            return True
        return False

    def getsha256(self):
        return hashlib.sha256(
            open(self.tarball_path(), 'rb').read()
        ).hexdigest()

    def confirmsha256(self):
        # did we actually fetch something new?
        if not self.fetch() or self.noconfirm:
            return False
        if (x := self.getsha256()) != self.sha256:
            raise HashMismatch((x, self.sha256))
        return True

    def unpack(self):
        self.confirmsha256()
        original_dir = f"{self.repository}-{self.revision}/"
        with tarfile.open(self.tarball_path(), 'r:gz') as archive:
            # code to modify the member paths.
            members = [
                m
                for m in archive.getmembers()
                if m.path.startswith(original_dir)
            ]
            for m in members:
                m.path = m.path[len(original_dir):]
            os.makedirs(self.decompressed_dir(), exist_ok=True)
            archive.extractall(path=self.decompressed_dir(), members=members)

    def get_browser(self) -> 'ImageFsBrowser':
        self.browser = ImageFsBrowser(
            path=self.decompressed_dir(), config=self.config)
        return self.browser

    def read_config(self):
        self.unpack()
        return self.browser.read_config()
