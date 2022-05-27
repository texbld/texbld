from texbld.common.directory import PACKAGE_CACHE_DIR, TARBALL_CACHE_DIR
from texbld.common.exceptions import GitHubNotFound, HashMismatch
from dataclasses import dataclass
import urllib3
import shutil
import os
import hashlib
import tarfile

http = urllib3.PoolManager()


@dataclass
class GitHubClient:
    owner: str
    repository: str
    revision: str
    sha256: str = None

    def tarball_path(self) -> str:
        return os.path.join(TARBALL_CACHE_DIR, f"{self.repository}-{self.revision}.tar.gz")

    def decompressed_dir(self) -> str:
        return os.path.join(PACKAGE_CACHE_DIR, f"{self.repository}-{self.revision}")

    def fetch(self):
        url = f"https://github.com/{self.owner}/{self.repository}/archive/{self.revision}.tar.gz"
        with http.request('GET', url, preload_content=False) as res:
            # TODO: raise GitHubNotFound if we get a 404.
            if res.status == 404:
                raise GitHubNotFound(url)
            with open(self.tarball_path(), 'wb') as w:
                shutil.copyfileobj(res, w)

    def getsha256(self):
        return hashlib.sha256(
            open(self.tarball_path(), 'rb').read()
        ).hexdigest()

    def confirmsha256(self):
        if not os.path.exists(self.tarball_path()) or self.getsha256() != self.sha256:
            self.fetch()
        else:
            return
        if (x := self.getsha256()) != self.sha256:
            raise HashMismatch(f"Actual: {x}, Got: {self.sha256}")

    # TODO: implement unpacking the tarball.
    def unpack(self):
        self.confirmsha256()
        with tarfile.open(self.tarball_path(), 'r:gz') as archive:
            archive.extractall(path=PACKAGE_CACHE_DIR)
