from dataclasses import dataclass, field
import hashlib
import json
import os
from docker.errors import ImageNotFound
from texbld.directory import BUILD_CACHE_DIR
from texbld.common.exceptions import DockerNotFound
from texbld.config import LATEST_CONFIG_VERSION
from texbld.docker.client import dockerclient
from texbld.common.image.parse import parse_source_image
# import like this to prevent circular imports
from texbld.common.image.sourceimage import SourceImage
from texbld.clients.github import GitHubClient
from texbld.clients.local import LocalClient
from abc import ABC, abstractmethod


@dataclass(order=True)
class Image(ABC):

    def image_hash(self):
        return hashlib.sha256(
            bytes(json.dumps(self.serialized()), 'utf-8')
        ).hexdigest()

    @abstractmethod
    def docker_image_name(self):
        pass

    @abstractmethod
    def package_dir(self) -> str:
        pass

    # returns version and then a dictionary.
    # should be implemented for the latest version.

    @abstractmethod
    def project_dict(self) -> 'tuple[str, dict]':
        pass

    def build_dir(self) -> str:
        return os.path.join(BUILD_CACHE_DIR, self.docker_image_name())

    def copy_to_builds(self, cache=False):
        pass

    def serialized(self) -> 'dict':
        d = self.__dict__.copy()
        d['class'] = self.__class__.__name__
        d['source'] = d.get('source').image_hash() if d.get('source') else None
        return d

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
            print(f"Attempting to pull {self.name} from the registry...")
            return dockerclient.images.pull(self.name)
        except ImageNotFound:
            raise DockerNotFound(self.name)

    def is_base(self) -> bool:
        return True

    def docker_image_name(self):
        return self.name

    def package_dir(self) -> str:
        return None

    def build_dir(self) -> str:
        return None

    def project_dict(self) -> 'tuple[str, dict]':
        return (LATEST_CONFIG_VERSION, dict(docker=self.name))


@dataclass(order=True)
class GitHubImage(Image):
    owner: str
    repository: str
    revision: str
    sha256: str
    config: str = "image.toml"
    source: SourceImage = None
    client: GitHubClient = None

    def __post_init__(self):
        self.client = GitHubClient(
            self.owner, self.repository, self.revision, self.sha256, self.config
        )

    def get_source(self):
        return self.source

    def pull(self) -> None:
        # pull only if we haven't pre-defined a source.
        if not self.source or not self.client:
            self.client.unpack()
            self.client.get_browser()
            self.source = parse_source_image(self.client.read_config())

    # re-implement serialized to get rid of client (since it isn't JSON serializable)
    def serialized(self) -> 'dict':
        d = super().serialized()
        del d['client']
        return d

    def docker_image_name(self):
        if not self.client.browser:
            self.pull()
        return f"texbld-github-{self.repository}-{self.client.browser.hashed}-{self.source.image_hash()}"

    def package_dir(self) -> str:
        return self.client.browser.path

    def copy_to_builds(self, cache=False):
        self.client.copy_to_builds(self, cache=cache)

    def project_dict(self) -> 'tuple[str, dict]':
        return (LATEST_CONFIG_VERSION, dict(github=dict(
            owner=self.owner,
            repository=self.repository,
            revision=self.revision,
            sha256=self.sha256,
            config=self.config
        )))


@dataclass(order=True)
class LocalImage(Image):
    name: str
    config: str = "image.toml"
    source: SourceImage = None
    client: LocalClient = None

    def get_source(self):
        return self.source

    def pull(self) -> None:
        # pull only if we haven't pre-defined a source.
        if not self.source or not self.client:
            self.client = LocalClient(self.name, self.config)
            self.source = parse_source_image(self.client.read_config())

    def docker_image_name(self):
        if not self.client.browser:
            self.pull()
        return f"texbld-local-{self.name}-{self.client.browser.hashed}-{self.source.image_hash()}"

    # re-implement serialized to get rid of client (since it isn't JSON serializable)
    def serialized(self) -> 'dict':
        d = super().serialized()
        del d['client']
        return d

    def package_dir(self) -> str:
        return self.client.browser.path

    def copy_to_builds(self, cache=False):
        self.client.copy_to_builds(self, cache=cache)

    def project_dict(self) -> 'tuple[str, dict]':
        return (LATEST_CONFIG_VERSION, dict(local=dict(name=self.name, config=self.config)))
