from argparse import ArgumentTypeError
import re
from texbld.common.image.image import DockerImage, GitHubImage, Image, LocalImage
import texbld.config

from texbld.utils.github import get_github_rev


def image_resource_type(arg: str):
    regexes = [ImageResource.github_regex,
               ImageResource.docker_regex, ImageResource.local_regex]
    for regex in regexes:
        if regex.fullmatch(arg):
            return arg
    raise ArgumentTypeError('Invalid Resource Type.')


class ImageResource:
    github_regex = re.compile(r"github:([-_\w]+)/([-_\w]+)(/.*?)?(#.*)?")
    docker_regex = re.compile(r"docker:(.*)")
    local_regex = re.compile(r"local:(.*?)(#.*)?")

    @classmethod
    def get_image(cls, resource: str) -> 'Image':
        resource = resource.strip()
        # GitHub images require fetching.
        if mch := cls.github_regex.fullmatch(resource):
            owner, repository, rev, config = mch.groups()
            rev = rev[1:] if rev is not None and len(rev) > 1 else None
            rev = get_github_rev(owner, repository, rev)

            config = config[1:] if config is not None and len(
                config) > 1 else "image.toml"
            # pull the image
            image = GitHubImage(owner=owner, repository=repository,
                                revision=rev, config=config, sha256=None)
            image.pull()
            # and then pass its sha256.
            return GitHubImage(owner=owner, repository=repository,
                               revision=rev, sha256=image.client.getsha256(), config=config)

        elif mch := cls.docker_regex.fullmatch(resource):
            image, = mch.groups()
            return DockerImage(name=image)

        elif mch := cls.local_regex.fullmatch(resource):
            image, config = mch.groups()
            config = config[1:] if config is not None and len(
                config) > 1 else "image.toml"
            return LocalImage(name=image, config=config)
