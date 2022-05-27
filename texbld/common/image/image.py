from dataclasses import dataclass, field
import hashlib
import json
import docker
from texbld.utils.github import GitHubClient
from texbld.utils.local import LocalClient


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

    def get_source(self):
        return None


@dataclass(order=True)
class DockerImage(Image):
    name: str
    source: SourceImage = None

    # TODO: implement this (Docker SDK's)
    def pull(self) -> None:
        pass


@dataclass(order=True)
class GitHubImage(Image):
    owner: str
    repository: str
    revision: str
    sha256: str
    source: SourceImage = None
    client: GitHubClient = field(init=False)

    def __post_init__(self):
        self.client = GitHubClient(self.owner, self.repository, self.revision, self.sha256)

    def get_source(self):
        return self.source

    def pull(self) -> None:
        self.client.unpack()
        self.source = self.client.read_config()


@dataclass(order=True)
class LocalImage(Image):
    name: str
    # useful for mockup testing where we don't actually need to implement local fs clients.
    testing: bool = False
    source: SourceImage = None
    client: LocalClient = field(init=False)

    def __post_init__(self):
        if not self.testing:
            self.client = LocalClient(self.name)

    def get_source(self):
        return self.source

    # browse the local FS and use the corresponding image. Set self.source.
    # TODO: implement this

    def pull(self) -> None:
        pass


def main():
    x = SourceImage(name="hello", packages=[], setup=[], files={})
    y = SourceImage(name="hello", packages=[], setup=[], files={})
    print(x.image_hash())
    print(json.dumps(x.__dict__))
    print(y.image_hash())
    print(json.dumps(y.__dict__))


if __name__ == "__main__":
    main()
