import re
from texbld.common.image.image import DockerImage, GitHubImage, Image, LocalImage

from texbld.utils.github import get_github_rev


class ImageResource:
    github_regex = re.compile(r"github:([-_\w]+)/([-_\w]+)(#[-_.\w]*)?")
    docker_regex = re.compile(r"docker:(.*)")
    local_regex = re.compile(r"local:(.*)")

    @classmethod
    def get_image(cls, resource: str, config: str) -> 'Image':
        # GitHub images require fetching.
        if mch := cls.github_regex.fullmatch(resource):
            owner, repository, rev = mch.groups()
            rev = rev[1:] if rev is not None and len(rev) > 1 else None
            rev = get_github_rev(owner, repository, rev)
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
            image, = mch.groups()
            return LocalImage(name=image, config=config)
