from dataclasses import dataclass, field
import hashlib
import json
from docker.errors import ImageNotFound
from texbld.common.exceptions import DockerNotFound
import texbld.parser as parser
from texbld.docker.client import dockerclient
from texbld.common.image.parse import parse_source_image
# import like this to prevent circular imports
from texbld.common.image.sourceimage import SourceImage
from texbld.utils.github import GitHubClient
from texbld.utils.local import LocalClient


@dataclass(order=True)
class Image:

    def image_hash(self):
        d = self.__dict__.copy()
        d['class'] = self.__class__.__name__
        d['source'] = d.get('source').image_hash() if d.get('source') else None
        return hashlib.sha256(
            bytes(json.dumps(d), 'utf-8')
        ).hexdigest()

    def pull(self) -> None:
        pass

    def get_source(self) -> 'SourceImage | None':
        return None

    # does it NOT inherit from something? (In which case we can cut the dependency chasing.)
    def is_base(self) -> bool:
        return False


@dataclass(order=True)
class DockerImage(Image):
    name: str

    def pull(self):
        try:
            return dockerclient.images.pull(self.name)
        except ImageNotFound:
            raise DockerNotFound(self.name)

    def is_base(self) -> bool:
        return True


@dataclass(order=True)
class GitHubImage(Image):
    owner: str
    repository: str
    revision: str
    sha256: str = None
    source: SourceImage = None
    client: GitHubClient = field(init=False)

    def __post_init__(self):
        self.client = GitHubClient(
            self.owner, self.repository, self.revision, self.sha256)

    def get_source(self):
        return self.source

    def pull(self) -> None:
        # pull only if we haven't pre-defined a source.
        if not self.source:
            self.client.unpack()
            self.client.get_browser()
            self.source = parse_source_image(self.client.read_config())


@dataclass(order=True)
class LocalImage(Image):
    name: str
    source: SourceImage = None
    client: LocalClient = None

    def get_source(self):
        return self.source

    # browse the local FS and use the corresponding image. Set self.source.
    # TODO: implement this

    def pull(self) -> None:
        # pull only if we haven't pre-defined a source.
        if not self.source:
            self.client = LocalClient(self.name)
            self.source = parse_source_image(self.client.read_config())


def main():
    x = SourceImage(name="hello", packages=[], setup=[], files={})
    y = SourceImage(name="hello", packages=[], setup=[], files={})
    print(x.image_hash())
    print(json.dumps(x.__dict__))
    print(y.image_hash())
    print(json.dumps(y.__dict__))


if __name__ == "__main__":
    main()
