from texbld.common.directory import PACKAGE_CACHE_DIR, TARBALL_CACHE_DIR
from texbld.common.exceptions import FsNotFound, GitHubNotFound, HashMismatch
from dataclasses import dataclass, field
import urllib3
import shutil
import os
import hashlib
import tarfile

from texbld.utils.fs import ImageFsBrowser

http = urllib3.PoolManager()


@dataclass
class GitHubClient:
    owner: str
    repository: str
    revision: str
    sha256: str = None
    noconfirm: bool = False
    # there are times when we want to test file-fetching in git.
    testing: str = False
    browser: ImageFsBrowser = field(init=False)

    def __post_init__(self):
        pass

    def tarball_path(self) -> str:
        return os.path.join(TARBALL_CACHE_DIR, f"{self.repository}-{self.revision}.tar.gz")

    def decompressed_dir(self) -> str:
        return os.path.join(PACKAGE_CACHE_DIR, f"{self.repository}-{self.revision}")

    def fetch(self):
        # fetch only if our tarball doesn't exist.
        if not os.path.exists(self.tarball_path()) or self.getsha256() != self.sha256 or self.noconfirm:
            url = f"https://github.com/{self.owner}/{self.repository}/archive/{self.revision}.tar.gz"
            with http.request('GET', url, preload_content=False) as res:
                # TODO: raise GitHubNotFound if we get a 404.
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
            raise HashMismatch(f"Actual: {x}, Got: {self.sha256}")
        return True

    def unpack(self):
        self.confirmsha256()
        with tarfile.open(self.tarball_path(), 'r:gz') as archive:
            archive.extractall(path=PACKAGE_CACHE_DIR)
        if not self.testing:
            self.browser = ImageFsBrowser(path=self.decompressed_dir())

    def read_config(self):
        self.unpack()
        return self.browser.read_config()
